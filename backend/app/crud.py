from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
import datetime

# User Operations
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id=user.id, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Faculty Profile Operations
def get_profile(db: Session, user_id: str):
    return db.query(models.FacultyProfile).filter(models.FacultyProfile.user_id == user_id).first()

def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.FacultyProfile(
        user_id=profile.user_id,
        name=profile.name,
        department=profile.department
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Settings Operations
def get_settings(db: Session, user_id: str):
    settings = db.query(models.ApplicationSetting).filter(models.ApplicationSetting.user_id == user_id).first()
    if not settings:
        # Create default settings
        settings = models.ApplicationSetting(user_id=user_id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

def update_settings(db: Session, user_id: str, settings_update: schemas.SettingsUpdate):
    db_settings = get_settings(db, user_id)
    db_settings.llm_provider = settings_update.llm_provider
    db_settings.model_name = settings_update.model_name
    db_settings.temperature = settings_update.temperature
    db_settings.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(db_settings)
    return db_settings

# Syllabus Operations
def create_syllabus(db: Session, syllabus: schemas.SyllabusCreate):
    db_syllabus = models.Syllabus(
        user_id=syllabus.user_id,
        filename=syllabus.filename,
        file_path=syllabus.file_path,
        raw_text=syllabus.raw_text,
        course_name=syllabus.course_name,
        course_code=syllabus.course_code
    )
    db.add(db_syllabus)
    db.commit()
    db.refresh(db_syllabus)
    return db_syllabus

def get_syllabus(db: Session, syllabus_id: int):
    return db.query(models.Syllabus).filter(models.Syllabus.id == syllabus_id).first()

def get_user_syllabi(db: Session, user_id: str):
    return db.query(models.Syllabus).filter(models.Syllabus.user_id == user_id).order_by(models.Syllabus.created_at.desc()).all()

# Artifact Database Inserts
def create_lesson_plan(db: Session, syllabus_id: int, title: str, content: dict):
    # Remove existing if any
    db.query(models.LessonPlan).filter(models.LessonPlan.syllabus_id == syllabus_id).delete()
    db_lp = models.LessonPlan(syllabus_id=syllabus_id, title=title, content=content)
    db.add(db_lp)
    db.commit()
    db.refresh(db_lp)
    return db_lp

def create_assignment(db: Session, syllabus_id: int, title: str, content: dict):
    db.query(models.Assignment).filter(models.Assignment.syllabus_id == syllabus_id).delete()
    db_as = models.Assignment(syllabus_id=syllabus_id, title=title, content=content)
    db.add(db_as)
    db.commit()
    db.refresh(db_as)
    return db_as

def create_quiz(db: Session, syllabus_id: int, title: str, content: dict):
    db.query(models.Quiz).filter(models.Quiz.syllabus_id == syllabus_id).delete()
    db_q = models.Quiz(syllabus_id=syllabus_id, title=title, content=content)
    db.add(db_q)
    db.commit()
    db.refresh(db_q)
    return db_q

def create_question_paper(db: Session, syllabus_id: int, exam_type: str, content: dict):
    # Delete matching exam type if existing
    db.query(models.QuestionPaper).filter(
        models.QuestionPaper.syllabus_id == syllabus_id, 
        models.QuestionPaper.exam_type == exam_type
    ).delete()
    db_qp = models.QuestionPaper(syllabus_id=syllabus_id, exam_type=exam_type, content=content)
    db.add(db_qp)
    db.commit()
    db.refresh(db_qp)
    return db_qp

def create_bloom_report(db: Session, syllabus_id: int, content: dict):
    db.query(models.BloomTaxonomyReport).filter(models.BloomTaxonomyReport.syllabus_id == syllabus_id).delete()
    db_br = models.BloomTaxonomyReport(syllabus_id=syllabus_id, content=content)
    db.add(db_br)
    db.commit()
    db.refresh(db_br)
    return db_br

def create_co_mapping(db: Session, syllabus_id: int, content: dict):
    db.query(models.COMappingReport).filter(models.COMappingReport.syllabus_id == syllabus_id).delete()
    db_co = models.COMappingReport(syllabus_id=syllabus_id, content=content)
    db.add(db_co)
    db.commit()
    db.refresh(db_co)
    return db_co

def create_quality_report(db: Session, syllabus_id: int, score: float, suggestions: list, content: dict):
    db.query(models.AcademicQualityReport).filter(models.AcademicQualityReport.syllabus_id == syllabus_id).delete()
    db_qr = models.AcademicQualityReport(syllabus_id=syllabus_id, score=score, suggestions=suggestions, content=content)
    db.add(db_qr)
    db.commit()
    db.refresh(db_qr)
    return db_qr

def create_pdf_report(db: Session, syllabus_id: int, file_path: str, file_url: str):
    db.query(models.GeneratedPDFReport).filter(models.GeneratedPDFReport.syllabus_id == syllabus_id).delete()
    db_pdf = models.GeneratedPDFReport(syllabus_id=syllabus_id, file_path=file_path, file_url=file_url)
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)
    return db_pdf

# Logging & Pipeline Execution Monitoring
def create_log(db: Session, syllabus_id: int, agent_name: str, status: str, log_message: str = None):
    db_log = models.AgentExecutionLog(
        syllabus_id=syllabus_id,
        agent_name=agent_name,
        status=status,
        log_message=log_message
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, syllabus_id: int):
    return db.query(models.AgentExecutionLog).filter(models.AgentExecutionLog.syllabus_id == syllabus_id).order_by(models.AgentExecutionLog.created_at.asc()).all()

# Generation History
def create_history_entry(db: Session, user_id: str, syllabus_id: int, status: str = "PENDING"):
    db_history = models.GenerationHistory(user_id=user_id, syllabus_id=syllabus_id, status=status)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def update_history_status(db: Session, syllabus_id: int, status: str):
    db_history = db.query(models.GenerationHistory).filter(models.GenerationHistory.syllabus_id == syllabus_id).first()
    if db_history:
        db_history.status = status
        db.commit()
        db.refresh(db_history)
    return db_history

def get_history(db: Session, user_id: str):
    return db.query(models.GenerationHistory).filter(models.GenerationHistory.user_id == user_id).order_by(models.GenerationHistory.created_at.desc()).all()

# Aggregated Analytics dashboard stats
def get_analytics(db: Session, user_id: str):
    # Fetch count of syllabi uploaded
    syllabi_count = db.query(models.Syllabus).filter(models.Syllabus.user_id == user_id).count()
    
    # Total lesson plans generated
    lp_count = db.query(models.LessonPlan).join(models.Syllabus).filter(models.Syllabus.user_id == user_id).count()
    
    # Assignments generated
    as_count = db.query(models.Assignment).join(models.Syllabus).filter(models.Syllabus.user_id == user_id).count()
    
    # Quizzes
    qz_count = db.query(models.Quiz).join(models.Syllabus).filter(models.Syllabus.user_id == user_id).count()
    
    # Question Papers
    qp_count = db.query(models.QuestionPaper).join(models.Syllabus).filter(models.Syllabus.user_id == user_id).count()

    # Average quality score
    avg_score = db.query(func.avg(models.AcademicQualityReport.score)).join(models.Syllabus).filter(models.Syllabus.user_id == user_id).scalar() or 0.0
    
    # Hours saved estimate (roughly 8 hours per syllabus process)
    hours_saved = syllabi_count * 8.5
    
    return {
        "syllabi_count": syllabi_count,
        "lesson_plans_count": lp_count,
        "assignments_count": as_count,
        "quizzes_count": qz_count,
        "question_papers_count": qp_count,
        "average_quality_score": round(float(avg_score), 1),
        "estimated_hours_saved": round(hours_saved, 1)
    }

# Complete Course packet fetching
def get_full_report(db: Session, syllabus_id: int):
    syllabus = get_syllabus(db, syllabus_id)
    if not syllabus:
        return None
        
    lesson_plan = db.query(models.LessonPlan).filter(models.LessonPlan.syllabus_id == syllabus_id).first()
    assignments = db.query(models.Assignment).filter(models.Assignment.syllabus_id == syllabus_id).first()
    quiz = db.query(models.Quiz).filter(models.Quiz.syllabus_id == syllabus_id).first()
    mid_sem_paper = db.query(models.QuestionPaper).filter(models.QuestionPaper.syllabus_id == syllabus_id, models.QuestionPaper.exam_type == "Mid-Semester").first()
    end_sem_paper = db.query(models.QuestionPaper).filter(models.QuestionPaper.syllabus_id == syllabus_id, models.QuestionPaper.exam_type == "End-Semester").first()
    bloom_mapping = db.query(models.BloomTaxonomyReport).filter(models.BloomTaxonomyReport.syllabus_id == syllabus_id).first()
    co_mapping = db.query(models.COMappingReport).filter(models.COMappingReport.syllabus_id == syllabus_id).first()
    quality_report = db.query(models.AcademicQualityReport).filter(models.AcademicQualityReport.syllabus_id == syllabus_id).first()
    pdf_report = db.query(models.GeneratedPDFReport).filter(models.GeneratedPDFReport.syllabus_id == syllabus_id).first()

    return {
        "syllabus": syllabus,
        "lesson_plan": lesson_plan.content if lesson_plan else None,
        "assignments": assignments.content if assignments else None,
        "quiz": quiz.content if quiz else None,
        "mid_sem_paper": mid_sem_paper.content if mid_sem_paper else None,
        "end_sem_paper": end_sem_paper.content if end_sem_paper else None,
        "bloom_mapping": bloom_mapping.content if bloom_mapping else None,
        "co_mapping": co_mapping.content if co_mapping else None,
        "quality_report": {
            "score": quality_report.score,
            "suggestions": quality_report.suggestions,
            "content": quality_report.content
        } if quality_report else None,
        "pdf_report_url": pdf_report.file_url if pdf_report else None
    }
