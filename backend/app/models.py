import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # Links directly to Supabase User ID (UUID string)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("FacultyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    syllabi = relationship("Syllabus", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("ApplicationSetting", back_populates="user", uselist=False, cascade="all, delete-orphan")
    histories = relationship("GenerationHistory", back_populates="user", cascade="all, delete-orphan")


class FacultyProfile(Base):
    __tablename__ = "faculty_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Syllabus(Base):
    __tablename__ = "syllabi"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Supabase Storage bucket path
    raw_text = Column(Text, nullable=True)
    course_name = Column(String, nullable=True)
    course_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="syllabi")
    lesson_plans = relationship("LessonPlan", back_populates="syllabus", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="syllabus", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="syllabus", cascade="all, delete-orphan")
    question_papers = relationship("QuestionPaper", back_populates="syllabus", cascade="all, delete-orphan")
    bloom_reports = relationship("BloomTaxonomyReport", back_populates="syllabus", cascade="all, delete-orphan")
    co_mappings = relationship("COMappingReport", back_populates="syllabus", cascade="all, delete-orphan")
    quality_reports = relationship("AcademicQualityReport", back_populates="syllabus", cascade="all, delete-orphan")
    pdf_reports = relationship("GeneratedPDFReport", back_populates="syllabus", cascade="all, delete-orphan")
    logs = relationship("AgentExecutionLog", back_populates="syllabus", cascade="all, delete-orphan")
    history_entries = relationship("GenerationHistory", back_populates="syllabus", cascade="all, delete-orphan")


class LessonPlan(Base):
    __tablename__ = "lesson_plans"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)  # List of weekly topics, objectives, methodologies
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="lesson_plans")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)  # List of assignments with questions and instructions
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="assignments")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)  # List of MCQs with options and correct answers
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="quizzes")


class QuestionPaper(Base):
    __tablename__ = "question_papers"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    exam_type = Column(String, nullable=False)  # "Mid-Semester" or "End-Semester"
    content = Column(JSON, nullable=False)  # Structure containing sections and questions
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="question_papers")


class BloomTaxonomyReport(Base):
    __tablename__ = "bloom_taxonomy_reports"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    content = Column(JSON, nullable=False)  # Mapping of modules to Bloom levels
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="bloom_reports")


class COMappingReport(Base):
    __tablename__ = "co_mapping_reports"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    content = Column(JSON, nullable=False)  # Course Outcome mapping metrics and correlation matrix
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="co_mappings")


class AcademicQualityReport(Base):
    __tablename__ = "academic_quality_reports"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)
    suggestions = Column(JSON, nullable=False)  # List of suggested improvements
    content = Column(JSON, nullable=False)  # Comprehensive quality check breakdown
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="quality_reports")


class GeneratedPDFReport(Base):
    __tablename__ = "generated_pdf_reports"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String, nullable=False)  # Path in Supabase storage
    file_url = Column(String, nullable=False)  # Public URL or signed URL
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="pdf_reports")


class AgentExecutionLog(Base):
    __tablename__ = "agent_execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # "STARTED", "COMPLETED", "FAILED"
    log_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    syllabus = relationship("Syllabus", back_populates="logs")


class ApplicationSetting(Base):
    __tablename__ = "application_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    llm_provider = Column(String, default="gemini")
    model_name = Column(String, default="gemini-1.5-flash")
    temperature = Column(Float, default=0.7)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="settings")


class GenerationHistory(Base):
    __tablename__ = "generation_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    syllabus_id = Column(Integer, ForeignKey("syllabi.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="PENDING")  # "PENDING", "COMPLETED", "FAILED"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="histories")
    syllabus = relationship("Syllabus", back_populates="history_entries")
