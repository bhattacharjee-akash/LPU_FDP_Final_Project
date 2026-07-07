from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, date, time

# User Schemas
class UserBase(BaseModel):
    id: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    created_at: datetime
    class Config:
        from_attributes = True


# Profile Schemas
class ProfileBase(BaseModel):
    name: str
    role: str = "Participant"
    department: Optional[str] = None
    phone: Optional[str] = None
    designation: Optional[str] = None

class ProfileCreate(ProfileBase):
    user_id: str

class ProfileResponse(ProfileBase):
    id: int
    user_id: str
    created_at: datetime
    class Config:
        from_attributes = True


# Settings
class SettingsBase(BaseModel):
    llm_provider: str = "groq"
    model_name: str = "llama3-8b-8192"
    temperature: float = 0.2

class SettingsUpdate(SettingsBase):
    pass

class SettingsResponse(SettingsBase):
    id: int
    user_id: str
    updated_at: datetime
    class Config:
        from_attributes = True


# Programme Schemas
class ProgrammeBase(BaseModel):
    title: str
    description: Optional[str] = None
    objectives: Optional[str] = None
    category: str
    mode: str
    venue: Optional[str] = None
    start_date: datetime
    end_date: datetime
    duration_days: int = 1
    max_capacity: int = 50
    status: str = "Upcoming"
    tags: Optional[List[str]] = None

class ProgrammeCreate(ProgrammeBase):
    coordinator_id: Optional[str] = None

class ProgrammeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    objectives: Optional[str] = None
    category: Optional[str] = None
    mode: Optional[str] = None
    venue: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    duration_days: Optional[int] = None
    max_capacity: Optional[int] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None

class ProgrammeResponse(ProgrammeBase):
    id: int
    coordinator_id: Optional[str] = None
    current_enrolment: int
    created_at: datetime
    class Config:
        from_attributes = True


# Session Schemas
class SessionBase(BaseModel):
    session_number: int
    title: str
    date: date
    start_time: str
    end_time: str
    venue: Optional[str] = None
    learning_objectives: Optional[str] = None
    presentation_url: Optional[str] = None
    pdf_notes_url: Optional[str] = None
    video_url: Optional[str] = None
    recording_url: Optional[str] = None
    reference_links: Optional[List[Dict[str, str]]] = None
    attendance_qr_code: Optional[str] = None
    attendance_window_start: Optional[datetime] = None
    attendance_window_end: Optional[datetime] = None
    gps_verification: bool = False
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None
    gps_radius_meters: float = 50.0

class SessionCreate(SessionBase):
    programme_id: int
    trainer_id: Optional[str] = None

class SessionResponse(SessionBase):
    id: int
    programme_id: int
    trainer_id: Optional[str] = None
    class Config:
        from_attributes = True


# Attendance Schemas
class AttendanceBase(BaseModel):
    status: str  # "Present", "Absent", "Late"
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None
    verified_by_gps: bool = False
    verified_by_qr: bool = False

class AttendanceCreate(AttendanceBase):
    session_id: int

class AttendanceVerify(BaseModel):
    session_id: int
    qr_code: Optional[str] = None
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None

class AttendanceOverride(BaseModel):
    status: str
    notes: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    id: int
    session_id: int
    participant_id: str
    timestamp: datetime
    manual_override: bool
    overridden_by: Optional[str] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True


# Material Schemas
class MaterialBase(BaseModel):
    title: str
    file_type: str  # "PPT", "PDF", "Word", "Excel", "Video", "Assignment", "Code File", "Reference Link", "Image", "Research Paper"
    programme_id: Optional[int] = None
    session_id: Optional[int] = None

class MaterialCreate(MaterialBase):
    file_path: str
    file_url: str
    uploaded_by: str

class MaterialResponse(MaterialBase):
    id: int
    file_path: str
    file_url: str
    uploaded_by: str
    is_indexed: bool
    created_at: datetime
    class Config:
        from_attributes = True


# Assessment Schemas
class AssessmentBase(BaseModel):
    type: str  # "MCQ", "Subjective", "Coding Assignment", "Case Study", "File Upload", "Quiz", "Viva", "Project Submission"
    title: str
    instructions: Optional[str] = None
    max_marks: float = 100.0
    passing_marks: float = 40.0
    content: Any  # JSON configuration for questions/tests

class AssessmentCreate(AssessmentBase):
    programme_id: int
    session_id: Optional[int] = None

class AssessmentResponse(AssessmentBase):
    id: int
    programme_id: int
    session_id: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True


# Assessment Submission Schemas
class AssessmentSubmissionBase(BaseModel):
    submission_data: Optional[Any] = None
    file_url: Optional[str] = None

class AssessmentSubmissionCreate(AssessmentSubmissionBase):
    assessment_id: int

class AssessmentSubmissionGrade(BaseModel):
    score: float
    grade: str
    feedback: Optional[str] = None

class AssessmentSubmissionResponse(AssessmentSubmissionBase):
    id: int
    assessment_id: int
    participant_id: str
    submitted_at: datetime
    score: Optional[float] = None
    grade: Optional[str] = None
    feedback: Optional[str] = None
    evaluated_by: Optional[str] = None
    evaluated_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# Project Submission Schemas
class ProjectSubmissionBase(BaseModel):
    title: str
    abstract: Optional[str] = None
    description: Optional[str] = None
    github_link: Optional[str] = None
    presentation_url: Optional[str] = None
    report_url: Optional[str] = None
    demo_video_url: Optional[str] = None

class ProjectSubmissionCreate(ProjectSubmissionBase):
    programme_id: int

class ProjectSubmissionGrade(BaseModel):
    score: float
    grade: str
    feedback: Optional[str] = None

class ProjectSubmissionResponse(ProjectSubmissionBase):
    id: int
    programme_id: int
    participant_id: str
    submitted_at: datetime
    score: Optional[float] = None
    grade: Optional[str] = None
    feedback: Optional[str] = None
    evaluated_by: Optional[str] = None
    evaluated_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# Feedback Schemas
class FeedbackBase(BaseModel):
    rating_trainer: int = 5
    rating_content: int = 5
    rating_venue: int = 5
    rating_facilities: int = 5
    rating_overall: int = 5
    feedback_text: Optional[str] = None
    suggestions: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    programme_id: int
    session_id: Optional[int] = None

class FeedbackResponse(FeedbackBase):
    id: int
    programme_id: int
    session_id: Optional[int] = None
    participant_id: str
    created_at: datetime
    class Config:
        from_attributes = True


# Impact Assessment Schemas
class ImpactAssessmentBase(BaseModel):
    pre_survey_score: Optional[float] = None
    post_survey_score: Optional[float] = None
    skill_improvement: Optional[int] = None
    knowledge_gain: Optional[str] = None
    behaviour_change: Optional[str] = None
    organizational_impact: Optional[str] = None
    roi_score: Optional[float] = None

class ImpactAssessmentCreate(ImpactAssessmentBase):
    programme_id: int

class ImpactAssessmentResponse(ImpactAssessmentBase):
    id: int
    programme_id: int
    participant_id: str
    created_at: datetime
    class Config:
        from_attributes = True


# Certificate Schemas
class CertificateBase(BaseModel):
    certificate_number: str
    file_path: str
    file_url: str
    qr_hash: str
    digital_signature: Optional[str] = None
    is_verified: bool = True

class CertificateResponse(CertificateBase):
    id: int
    programme_id: int
    participant_id: str
    issue_date: datetime
    class Config:
        from_attributes = True


# Corporate Schemas
class CorporateClientBase(BaseModel):
    company_name: str
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class CorporateClientCreate(CorporateClientBase):
    pass

class CorporateClientResponse(CorporateClientBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class CorporateContractBase(BaseModel):
    contract_url: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_amount: Optional[float] = None
    invoice_status: str = "Pending"

class CorporateContractCreate(CorporateContractBase):
    client_id: int
    programme_id: Optional[int] = None

class CorporateContractResponse(CorporateContractBase):
    id: int
    client_id: int
    programme_id: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True


# Analytics Response Schemas
class DashboardStats(BaseModel):
    total_programmes: int
    active_programmes: int
    upcoming_programmes: int
    completed_programmes: int
    total_participants: int
    average_attendance: float
    average_feedback_rating: float
    corporate_trainings_count: int
    total_revenue: float


# RAG Schemas
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
