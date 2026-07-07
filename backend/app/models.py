import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON, Boolean, Date, Time
from sqlalchemy.orm import relationship
from app.database import Base

# Conditionally import pgvector Vector type
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    Vector = None

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # Links directly to Supabase User ID (UUID string)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings = relationship("ApplicationSetting", back_populates="user", uselist=False, cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="uploader", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", foreign_keys="[Attendance.participant_id]", back_populates="participant", cascade="all, delete-orphan")
    submissions = relationship("AssessmentSubmission", back_populates="participant", cascade="all, delete-orphan")
    projects = relationship("ProjectSubmission", back_populates="participant", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="participant", cascade="all, delete-orphan")
    impact_assessments = relationship("ImpactAssessment", back_populates="participant", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="participant", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="Participant")  # "HRDC Administrator", "HRDC Staff", "Faculty", "Trainer", "External Trainer", "Corporate Client", "Vendor", "Participant"
    department = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Programme(Base):
    __tablename__ = "programmes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    objectives = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # e.g., "FDP", "Workshop", "Orientation Programme", "Refresher Course", "Administrative Training", "Technical Training", "Certification Programme", "Research Methodology Workshop", "Guest Lecture", "Industry Session", "Corporate Training", "Vendor Training", "Consultancy Programme"
    mode = Column(String, nullable=False)  # "Online", "Offline", "Hybrid"
    venue = Column(String, nullable=True)
    coordinator_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    duration_days = Column(Integer, default=1)
    max_capacity = Column(Integer, default=50)
    current_enrolment = Column(Integer, default=0)
    status = Column(String, default="Upcoming")  # "Upcoming", "Active", "Completed", "Archived", "Draft"
    tags = Column(JSON, nullable=True)  # JSON list of tags
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    sessions = relationship("Session", back_populates="programme", cascade="all, delete-orphan")
    participants = relationship("ProgrammeParticipant", back_populates="programme", cascade="all, delete-orphan")
    trainers = relationship("ProgrammeTrainer", back_populates="programme", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="programme", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="programme", cascade="all, delete-orphan")
    projects = relationship("ProjectSubmission", back_populates="programme", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="programme", cascade="all, delete-orphan")
    impact_assessments = relationship("ImpactAssessment", back_populates="programme", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="programme", cascade="all, delete-orphan")
    contracts = relationship("CorporateContract", back_populates="programme", cascade="all, delete-orphan")


class ProgrammeTrainer(Base):
    __tablename__ = "programme_trainers"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    trainer_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    programme = relationship("Programme", back_populates="trainers")
    trainer = relationship("User")


class ProgrammeParticipant(Base):
    __tablename__ = "programme_participants"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="Registered")  # "Registered", "Approved", "Completed", "Cancelled"
    enrolled_at = Column(DateTime, default=datetime.datetime.utcnow)

    programme = relationship("Programme", back_populates="participants")
    participant = relationship("User")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    session_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)  # "09:00 AM"
    end_time = Column(String, nullable=False)    # "11:00 AM"
    venue = Column(String, nullable=True)
    trainer_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    learning_objectives = Column(Text, nullable=True)
    
    # Session Resources
    presentation_url = Column(String, nullable=True)
    pdf_notes_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    recording_url = Column(String, nullable=True)
    reference_links = Column(JSON, nullable=True)  # list of URLs/titles

    # Attendance Config
    attendance_qr_code = Column(String, nullable=True)
    attendance_window_start = Column(DateTime, nullable=True)
    attendance_window_end = Column(DateTime, nullable=True)
    gps_verification = Column(Boolean, default=False)
    gps_lat = Column(Float, nullable=True)
    gps_lng = Column(Float, nullable=True)
    gps_radius_meters = Column(Float, default=50.0)

    programme = relationship("Programme", back_populates="sessions")
    trainer = relationship("User")
    attendance_records = relationship("Attendance", back_populates="session", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="session", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="session", cascade="all, delete-orphan")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)  # "Present", "Absent", "Late"
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Verification details
    gps_lat = Column(Float, nullable=True)
    gps_lng = Column(Float, nullable=True)
    verified_by_gps = Column(Boolean, default=False)
    verified_by_qr = Column(Boolean, default=False)
    
    # Manual overrides
    manual_override = Column(Boolean, default=False)
    overridden_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes = Column(Text, nullable=True)

    session = relationship("Session", back_populates="attendance_records")
    participant = relationship("User", foreign_keys=[participant_id], back_populates="attendance_records")
    override_user = relationship("User", foreign_keys=[overridden_by])


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Supabase storage path
    file_url = Column(String, nullable=False)   # Public url
    file_type = Column(String, nullable=False)  # "PPT", "PDF", "Word", "Excel", "Video", "Assignment", "Code File", "Reference Link", "Image", "Research Paper"
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=True)
    uploaded_by = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_indexed = Column(Boolean, default=False)  # For RAG
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    programme = relationship("Programme", back_populates="materials")
    session = relationship("Session", back_populates="materials")
    uploader = relationship("User", back_populates="materials")
    embeddings = relationship("DocumentEmbedding", back_populates="material", cascade="all, delete-orphan")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=True)
    type = Column(String, nullable=False)  # "MCQ", "Subjective", "Coding Assignment", "Case Study", "File Upload", "Quiz", "Viva", "Project Submission"
    title = Column(String, nullable=False)
    instructions = Column(Text, nullable=True)
    max_marks = Column(Float, default=100.0)
    passing_marks = Column(Float, default=40.0)
    content = Column(JSON, nullable=False)  # Questions & Answer configurations
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    programme = relationship("Programme", back_populates="assessments")
    session = relationship("Session", back_populates="assessments")
    submissions = relationship("AssessmentSubmission", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentSubmission(Base):
    __tablename__ = "assessment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    submission_data = Column(JSON, nullable=True)  # Student answers
    file_url = Column(String, nullable=True)       # For file upload tasks
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Grading
    score = Column(Float, nullable=True)
    grade = Column(String, nullable=True)
    feedback = Column(Text, nullable=True)
    evaluated_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    evaluated_at = Column(DateTime, nullable=True)

    assessment = relationship("Assessment", back_populates="submissions")
    participant = relationship("User", back_populates="submissions")
    evaluator = relationship("User", foreign_keys=[evaluated_by])


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    github_link = Column(String, nullable=True)
    presentation_url = Column(String, nullable=True)
    report_url = Column(String, nullable=True)
    demo_video_url = Column(String, nullable=True)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Grading
    score = Column(Float, nullable=True)
    grade = Column(String, nullable=True)
    feedback = Column(Text, nullable=True)
    evaluated_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    evaluated_at = Column(DateTime, nullable=True)

    programme = relationship("Programme", back_populates="projects")
    participant = relationship("User", back_populates="projects")
    evaluator = relationship("User", foreign_keys=[evaluated_by])


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=True)
    participant_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Ratings (1 to 5 scale)
    rating_trainer = Column(Integer, default=5)
    rating_content = Column(Integer, default=5)
    rating_venue = Column(Integer, default=5)
    rating_facilities = Column(Integer, default=5)
    rating_overall = Column(Integer, default=5)
    
    feedback_text = Column(Text, nullable=True)
    suggestions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    programme = relationship("Programme", back_populates="feedbacks")
    participant = relationship("User", back_populates="feedbacks")


class ImpactAssessment(Base):
    __tablename__ = "impact_assessments"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    pre_survey_score = Column(Float, nullable=True)
    post_survey_score = Column(Float, nullable=True)
    skill_improvement = Column(Integer, nullable=True)  # Difference in skill level self-rating (e.g. 1-5 scale)
    knowledge_gain = Column(Text, nullable=True)
    behaviour_change = Column(Text, nullable=True)
    organizational_impact = Column(Text, nullable=True)
    roi_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    programme = relationship("Programme", back_populates="impact_assessments")
    participant = relationship("User", back_populates="impact_assessments")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    certificate_number = Column(String, unique=True, nullable=False)
    issue_date = Column(DateTime, default=datetime.datetime.utcnow)
    file_path = Column(String, nullable=False)  # Storage path
    file_url = Column(String, nullable=False)   # Verification/Download url
    qr_hash = Column(String, nullable=False)    # Hash for verification page
    digital_signature = Column(String, nullable=True)
    is_verified = Column(Boolean, default=True)

    programme = relationship("Programme", back_populates="certificates")
    participant = relationship("User", back_populates="certificates")


class CorporateClient(Base):
    __tablename__ = "corporate_clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_person = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    contracts = relationship("CorporateContract", back_populates="client", cascade="all, delete-orphan")


class CorporateContract(Base):
    __tablename__ = "corporate_contracts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("corporate_clients.id", ondelete="CASCADE"), nullable=False)
    programme_id = Column(Integer, ForeignKey("programmes.id", ondelete="SET NULL"), nullable=True)
    contract_url = Column(String, nullable=True)
    invoice_number = Column(String, nullable=True)
    invoice_amount = Column(Float, nullable=True)
    invoice_status = Column(String, default="Pending")  # "Pending", "Paid", "Cancelled"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    client = relationship("CorporateClient", back_populates="contracts")
    programme = relationship("Programme", back_populates="contracts")


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id", ondelete="CASCADE"), nullable=True)
    filename = Column(String, nullable=False)
    text_chunk = Column(Text, nullable=False)
    
    # Store pgvector Vector if imported, else fallback to standard JSON representation
    if Vector is not None:
        embedding = Column(Vector(1536), nullable=False)
    else:
        embedding = Column(JSON, nullable=False)

    material = relationship("Material", back_populates="embeddings")


class ApplicationSetting(Base):
    __tablename__ = "application_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    llm_provider = Column(String, default="groq")
    model_name = Column(String, default="llama3-8b-8192")
    temperature = Column(Float, default=0.2)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="settings")
