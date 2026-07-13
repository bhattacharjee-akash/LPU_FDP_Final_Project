from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

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


# Faculty Profile Schemas
class ProfileBase(BaseModel):
    name: str
    department: str

class ProfileCreate(ProfileBase):
    user_id: str

class ProfileResponse(ProfileBase):
    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Application Settings
class SettingsBase(BaseModel):
    llm_provider: str = "gemini"
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7

class SettingsUpdate(SettingsBase):
    pass

class SettingsResponse(SettingsBase):
    id: int
    user_id: str
    updated_at: datetime

    class Config:
        from_attributes = True


# Syllabus Schemas
class SyllabusBase(BaseModel):
    filename: str
    file_path: str
    course_name: Optional[str] = None
    course_code: Optional[str] = None

class SyllabusCreate(SyllabusBase):
    user_id: str
    raw_text: Optional[str] = None

class SyllabusResponse(SyllabusBase):
    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Agent Output Contents
class LessonPlanResponse(BaseModel):
    id: int
    syllabus_id: int
    title: str
    content: Any  # List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

class AssignmentResponse(BaseModel):
    id: int
    syllabus_id: int
    title: str
    content: Any  # List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    id: int
    syllabus_id: int
    title: str
    content: Any  # List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

class QuestionPaperResponse(BaseModel):
    id: int
    syllabus_id: int
    exam_type: str
    content: Any  # Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

class BloomTaxonomyResponse(BaseModel):
    id: int
    syllabus_id: int
    content: Any  # Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

class COMappingResponse(BaseModel):
    id: int
    syllabus_id: int
    content: Any  # Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

class AcademicQualityResponse(BaseModel):
    id: int
    syllabus_id: int
    score: float
    suggestions: Any
    content: Any
    created_at: datetime

    class Config:
        from_attributes = True


# Logs & History
class LogResponse(BaseModel):
    id: int
    syllabus_id: int
    agent_name: str
    status: str
    log_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    id: int
    user_id: str
    syllabus_id: int
    status: str
    created_at: datetime
    syllabus: SyllabusResponse

    class Config:
        from_attributes = True


# Response models for aggregation/full report
class FullReportResponse(BaseModel):
    syllabus: SyllabusResponse
    lesson_plan: Optional[Any] = None
    assignments: Optional[Any] = None
    quiz: Optional[Any] = None
    mid_sem_paper: Optional[Any] = None
    end_sem_paper: Optional[Any] = None
    bloom_mapping: Optional[Any] = None
    co_mapping: Optional[Any] = None
    quality_report: Optional[Any] = None
    pdf_report_url: Optional[str] = None
