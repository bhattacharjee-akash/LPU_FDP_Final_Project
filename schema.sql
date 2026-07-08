-- LPU Academic Copilot - Supabase SQL Schema & RLS Setup
-- Copy and run this script in your Supabase SQL Editor.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY, -- Maps directly to auth.users.id
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS on users
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Create policies for users
CREATE POLICY "Users can view their own record" ON public.users 
    FOR SELECT USING (auth.uid()::text = id);

CREATE POLICY "Users can insert their own record" ON public.users 
    FOR INSERT WITH CHECK (auth.uid()::text = id);


-- 2. Faculty Profiles Table
CREATE TABLE IF NOT EXISTS public.faculty_profiles (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE UNIQUE,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.faculty_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own profile" ON public.faculty_profiles 
    FOR ALL USING (auth.uid()::text = user_id);


-- 3. Syllabi Table
CREATE TABLE IF NOT EXISTS public.syllabi (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    raw_text TEXT,
    course_name TEXT,
    course_code TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.syllabi ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own syllabi" ON public.syllabi 
    FOR ALL USING (auth.uid()::text = user_id);


-- 4. Lesson Plans Table
CREATE TABLE IF NOT EXISTS public.lesson_plans (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.lesson_plans ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view lesson plans of their syllabi" ON public.lesson_plans 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.lesson_plans.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 5. Assignments Table
CREATE TABLE IF NOT EXISTS public.assignments (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.assignments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view assignments of their syllabi" ON public.assignments 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.assignments.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 6. Quizzes Table
CREATE TABLE IF NOT EXISTS public.quizzes (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.quizzes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view quizzes of their syllabi" ON public.quizzes 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.quizzes.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 7. Question Papers Table
CREATE TABLE IF NOT EXISTS public.question_papers (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    exam_type TEXT NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.question_papers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view question papers of their syllabi" ON public.question_papers 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.question_papers.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 8. Bloom Taxonomy Reports Table
CREATE TABLE IF NOT EXISTS public.bloom_taxonomy_reports (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.bloom_taxonomy_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view bloom reports of their syllabi" ON public.bloom_taxonomy_reports 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.bloom_taxonomy_reports.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 9. CO Mapping Reports Table
CREATE TABLE IF NOT EXISTS public.co_mapping_reports (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.co_mapping_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view co mapping of their syllabi" ON public.co_mapping_reports 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.co_mapping_reports.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 10. Academic Quality Reports Table
CREATE TABLE IF NOT EXISTS public.academic_quality_reports (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    score FLOAT NOT NULL,
    suggestions JSONB NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.academic_quality_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view quality reports of their syllabi" ON public.academic_quality_reports 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.academic_quality_reports.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 11. Generated PDF Reports Table
CREATE TABLE IF NOT EXISTS public.generated_pdf_reports (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    file_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.generated_pdf_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view pdf reports of their syllabi" ON public.generated_pdf_reports 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.generated_pdf_reports.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 12. Agent Execution Logs Table
CREATE TABLE IF NOT EXISTS public.agent_execution_logs (
    id SERIAL PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    status TEXT NOT NULL,
    log_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.agent_execution_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view logs of their syllabi" ON public.agent_execution_logs 
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.syllabi 
            WHERE public.syllabi.id = public.agent_execution_logs.syllabus_id 
            AND public.syllabi.user_id = auth.uid()::text
        )
    );


-- 13. Application Settings Table
CREATE TABLE IF NOT EXISTS public.application_settings (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE UNIQUE,
    llm_provider TEXT DEFAULT 'gemini',
    model_name TEXT DEFAULT 'gemini-1.5-flash',
    temperature FLOAT DEFAULT 0.7,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.application_settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their settings" ON public.application_settings 
    FOR ALL USING (auth.uid()::text = user_id);


-- 14. Generation History Table
CREATE TABLE IF NOT EXISTS public.generation_histories (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    syllabus_id INTEGER NOT NULL REFERENCES public.syllabi(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.generation_histories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their history" ON public.generation_histories 
    FOR ALL USING (auth.uid()::text = user_id);
