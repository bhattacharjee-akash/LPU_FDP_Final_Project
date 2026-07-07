-- LPU HRDC Nexus - Supabase SQL Schema & RLS Setup
-- Copy and run this script in your Supabase SQL Editor.

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Users Table
CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY, -- Maps directly to auth.users.id
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS on users
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own record" ON public.users 
    FOR SELECT USING (auth.uid()::text = id);

CREATE POLICY "Users can insert their own record" ON public.users 
    FOR INSERT WITH CHECK (auth.uid()::text = id);


-- 2. Profiles Table
CREATE TABLE IF NOT EXISTS public.profiles (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE UNIQUE,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'Participant' NOT NULL, -- 'HRDC Administrator', 'HRDC Staff', 'Faculty', 'Trainer', 'External Trainer', 'Corporate Client', 'Vendor', 'Participant'
    department TEXT,
    phone TEXT,
    designation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Profiles are viewable by authenticated users" ON public.profiles 
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "Users can manage their own profile" ON public.profiles 
    FOR ALL USING (auth.uid()::text = user_id);


-- 3. Programmes Table
CREATE TABLE IF NOT EXISTS public.programmes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    objectives TEXT,
    category TEXT NOT NULL, -- 'FDP', 'Workshop', 'Orientation Programme', 'Refresher Course', etc.
    mode TEXT NOT NULL, -- 'Online', 'Offline', 'Hybrid'
    venue TEXT,
    coordinator_id TEXT REFERENCES public.users(id) ON DELETE SET NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_days INTEGER DEFAULT 1,
    max_capacity INTEGER DEFAULT 50,
    current_enrolment INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Upcoming' NOT NULL, -- 'Upcoming', 'Active', 'Completed', 'Archived', 'Draft'
    tags JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.programmes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Programmes are viewable by authenticated users" ON public.programmes 
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "HRDC admins and staff can manage programmes" ON public.programmes 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE public.profiles.user_id = auth.uid()::text 
            AND public.profiles.role IN ('HRDC Administrator', 'HRDC Staff')
        )
    );


-- 4. Programme Trainers Table (Many-to-Many join)
CREATE TABLE IF NOT EXISTS public.programme_trainers (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    trainer_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE
);

ALTER TABLE public.programme_trainers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Trainers join viewable by authenticated" ON public.programme_trainers
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "HRDC manages trainers assignments" ON public.programme_trainers
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE public.profiles.user_id = auth.uid()::text 
            AND public.profiles.role IN ('HRDC Administrator', 'HRDC Staff')
        )
    );


-- 5. Programme Participants Table (Enrolment)
CREATE TABLE IF NOT EXISTS public.programme_participants (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'Registered' NOT NULL, -- 'Registered', 'Approved', 'Completed', 'Cancelled'
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.programme_participants ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Participants can view their own enrolments" ON public.programme_participants 
    FOR SELECT USING (auth.uid()::text = participant_id);

CREATE POLICY "HRDC can view and edit all enrolments" ON public.programme_participants 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE public.profiles.user_id = auth.uid()::text 
            AND public.profiles.role IN ('HRDC Administrator', 'HRDC Staff')
        )
    );


-- 6. Sessions Table
CREATE TABLE IF NOT EXISTS public.sessions (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    session_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    date DATE NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    venue TEXT,
    trainer_id TEXT REFERENCES public.users(id) ON DELETE SET NULL,
    learning_objectives TEXT,
    presentation_url TEXT,
    pdf_notes_url TEXT,
    video_url TEXT,
    recording_url TEXT,
    reference_links JSONB,
    attendance_qr_code TEXT,
    attendance_window_start TIMESTAMP WITH TIME ZONE,
    attendance_window_end TIMESTAMP WITH TIME ZONE,
    gps_verification BOOLEAN DEFAULT false NOT NULL,
    gps_lat DOUBLE PRECISION,
    gps_lng DOUBLE PRECISION,
    gps_radius_meters DOUBLE PRECISION DEFAULT 50.0
);

ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Sessions are viewable by authenticated" ON public.sessions 
    FOR SELECT TO authenticated USING (true);


-- 7. Attendance Table
CREATE TABLE IF NOT EXISTS public.attendance (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES public.sessions(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    status TEXT NOT NULL, -- 'Present', 'Absent', 'Late'
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    gps_lat DOUBLE PRECISION,
    gps_lng DOUBLE PRECISION,
    verified_by_gps BOOLEAN DEFAULT false NOT NULL,
    verified_by_qr BOOLEAN DEFAULT false NOT NULL,
    manual_override BOOLEAN DEFAULT false NOT NULL,
    overridden_by TEXT REFERENCES public.users(id) ON DELETE SET NULL,
    notes TEXT
);

ALTER TABLE public.attendance ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Participants can view their own attendance" ON public.attendance 
    FOR SELECT USING (auth.uid()::text = participant_id);

CREATE POLICY "Participants can submit attendance details" ON public.attendance 
    FOR INSERT WITH CHECK (auth.uid()::text = participant_id);

CREATE POLICY "HRDC can manage all attendance" ON public.attendance 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE public.profiles.user_id = auth.uid()::text 
            AND public.profiles.role IN ('HRDC Administrator', 'HRDC Staff', 'Trainer')
        )
    );


-- 8. Materials Table (RAG documents storage)
CREATE TABLE IF NOT EXISTS public.materials (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_type TEXT NOT NULL, -- 'PPT', 'PDF', 'Word', 'Excel', etc.
    programme_id INTEGER REFERENCES public.programmes(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES public.sessions(id) ON DELETE CASCADE,
    uploaded_by TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    is_indexed BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.materials ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Materials viewable by authenticated users" ON public.materials 
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "Trainers and HRDC can upload materials" ON public.materials 
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE public.profiles.user_id = auth.uid()::text 
            AND public.profiles.role IN ('HRDC Administrator', 'HRDC Staff', 'Trainer', 'External Trainer')
        )
    );


-- 9. Assessments Table
CREATE TABLE IF NOT EXISTS public.assessments (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES public.sessions(id) ON DELETE CASCADE,
    type TEXT NOT NULL, -- 'MCQ', 'Subjective', 'Coding Assignment', 'Case Study', etc.
    title TEXT NOT NULL,
    instructions TEXT,
    max_marks DOUBLE PRECISION DEFAULT 100.0 NOT NULL,
    passing_marks DOUBLE PRECISION DEFAULT 40.0 NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.assessments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Assessments viewable by authenticated" ON public.assessments 
    FOR SELECT TO authenticated USING (true);


-- 10. Assessment Submissions Table
CREATE TABLE IF NOT EXISTS public.assessment_submissions (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER NOT NULL REFERENCES public.assessments(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    submission_data JSONB,
    file_url TEXT,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    score DOUBLE PRECISION,
    grade TEXT,
    feedback TEXT,
    evaluated_by TEXT REFERENCES public.users(id) ON DELETE SET NULL,
    evaluated_at TIMESTAMP WITH TIME ZONE
);

ALTER TABLE public.assessment_submissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Submissions viewable by owner" ON public.assessment_submissions 
    FOR SELECT USING (auth.uid()::text = participant_id);

CREATE POLICY "Submissions insertable by owner" ON public.assessment_submissions 
    FOR INSERT WITH CHECK (auth.uid()::text = participant_id);

CREATE POLICY "HRDC can grade submissions" ON public.assessment_submissions 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.profiles 
            WHERE public.profiles.user_id = auth.uid()::text 
            AND public.profiles.role IN ('HRDC Administrator', 'HRDC Staff', 'Trainer', 'External Trainer')
        )
    );


-- 11. Project Submissions Table
CREATE TABLE IF NOT EXISTS public.project_submissions (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    abstract TEXT,
    description TEXT,
    github_link TEXT,
    presentation_url TEXT,
    report_url TEXT,
    demo_video_url TEXT,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    score DOUBLE PRECISION,
    grade TEXT,
    feedback TEXT,
    evaluated_by TEXT REFERENCES public.users(id) ON DELETE SET NULL,
    evaluated_at TIMESTAMP WITH TIME ZONE
);

ALTER TABLE public.project_submissions ENABLE ROW LEVEL SECURITY;


-- 12. Feedbacks Table
CREATE TABLE IF NOT EXISTS public.feedbacks (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES public.sessions(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    rating_trainer INTEGER DEFAULT 5 NOT NULL,
    rating_content INTEGER DEFAULT 5 NOT NULL,
    rating_venue INTEGER DEFAULT 5 NOT NULL,
    rating_facilities INTEGER DEFAULT 5 NOT NULL,
    rating_overall INTEGER DEFAULT 5 NOT NULL,
    feedback_text TEXT,
    suggestions TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.feedbacks ENABLE ROW LEVEL SECURITY;


-- 13. Impact Assessments Table
CREATE TABLE IF NOT EXISTS public.impact_assessments (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    pre_survey_score DOUBLE PRECISION,
    post_survey_score DOUBLE PRECISION,
    skill_improvement INTEGER,
    knowledge_gain TEXT,
    behaviour_change TEXT,
    organizational_impact TEXT,
    roi_score DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.impact_assessments ENABLE ROW LEVEL SECURITY;


-- 14. Certificates Table
CREATE TABLE IF NOT EXISTS public.certificates (
    id SERIAL PRIMARY KEY,
    programme_id INTEGER NOT NULL REFERENCES public.programmes(id) ON DELETE CASCADE,
    participant_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    certificate_number TEXT NOT NULL UNIQUE,
    issue_date TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    file_path TEXT NOT NULL,
    file_url TEXT NOT NULL,
    qr_hash TEXT NOT NULL,
    digital_signature TEXT,
    is_verified BOOLEAN DEFAULT true NOT NULL
);

ALTER TABLE public.certificates ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public certificates verification" ON public.certificates
    FOR SELECT USING (true);


-- 15. Corporate Clients & Contracts
CREATE TABLE IF NOT EXISTS public.corporate_clients (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    contact_person TEXT,
    email TEXT,
    phone TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.corporate_contracts (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES public.corporate_clients(id) ON DELETE CASCADE,
    programme_id INTEGER REFERENCES public.programmes(id) ON DELETE SET NULL,
    contract_url TEXT,
    invoice_number TEXT,
    invoice_amount DOUBLE PRECISION,
    invoice_status TEXT DEFAULT 'Pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);


-- 16. Document Embeddings Table (RAG pgvector storage)
CREATE TABLE IF NOT EXISTS public.document_embeddings (
    id SERIAL PRIMARY KEY,
    material_id INTEGER REFERENCES public.materials(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    text_chunk TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL
);

-- HNSW Vector Index for efficient cosine similarity
CREATE INDEX IF NOT EXISTS document_embeddings_embedding_idx 
ON public.document_embeddings USING hnsw (embedding vector_cosine_ops);


-- 17. Application Settings Table
CREATE TABLE IF NOT EXISTS public.application_settings (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE UNIQUE,
    llm_provider TEXT DEFAULT 'groq' NOT NULL,
    model_name TEXT DEFAULT 'llama3-8b-8192' NOT NULL,
    temperature DOUBLE PRECISION DEFAULT 0.2 NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);


-- Indexes for high-performance CRUD queries
CREATE INDEX IF NOT EXISTS idx_sessions_programme ON public.sessions(programme_id);
CREATE INDEX IF NOT EXISTS idx_attendance_session ON public.attendance(session_id);
CREATE INDEX IF NOT EXISTS idx_attendance_participant ON public.attendance(participant_id);
CREATE INDEX IF NOT EXISTS idx_materials_programme ON public.materials(programme_id);
CREATE INDEX IF NOT EXISTS idx_submissions_assessment ON public.assessment_submissions(assessment_id);
CREATE INDEX IF NOT EXISTS idx_feedbacks_programme ON public.feedbacks(programme_id);
CREATE INDEX IF NOT EXISTS idx_certificates_participant ON public.certificates(participant_id);
