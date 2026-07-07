from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app import models, schemas
import datetime
from typing import List, Dict, Any, Optional

# --- User & Profile Operations ---
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id=user.id, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_profile(db: Session, user_id: str):
    return db.query(models.Profile).filter(models.Profile.user_id == user_id).first()

def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(
        user_id=profile.user_id,
        name=profile.name,
        role=profile.role,
        department=profile.department,
        phone=profile.phone,
        designation=profile.designation
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, user_id: str, profile_update: schemas.ProfileBase):
    db_profile = get_profile(db, user_id)
    if db_profile:
        db_profile.name = profile_update.name
        db_profile.role = profile_update.role
        db_profile.department = profile_update.department
        db_profile.phone = profile_update.phone
        db_profile.designation = profile_update.designation
        db.commit()
        db.refresh(db_profile)
    return db_profile


# --- Settings Operations ---
def get_settings(db: Session, user_id: str):
    settings = db.query(models.ApplicationSetting).filter(models.ApplicationSetting.user_id == user_id).first()
    if not settings:
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


# --- Programme Operations ---
def get_programme(db: Session, programme_id: int):
    return db.query(models.Programme).filter(models.Programme.id == programme_id).first()

def get_programmes(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None, status: Optional[str] = None):
    query = db.query(models.Programme)
    if category:
        query = query.filter(models.Programme.category == category)
    if status:
        query = query.filter(models.Programme.status == status)
    return query.order_by(models.Programme.start_date.desc()).offset(skip).limit(limit).all()

def create_programme(db: Session, programme: schemas.ProgrammeCreate):
    db_programme = models.Programme(
        title=programme.title,
        description=programme.description,
        objectives=programme.objectives,
        category=programme.category,
        mode=programme.mode,
        venue=programme.venue,
        coordinator_id=programme.coordinator_id,
        start_date=programme.start_date,
        end_date=programme.end_date,
        duration_days=programme.duration_days,
        max_capacity=programme.max_capacity,
        status=programme.status,
        tags=programme.tags
    )
    db.add(db_programme)
    db.commit()
    db.refresh(db_programme)
    return db_programme

def update_programme(db: Session, programme_id: int, programme: schemas.ProgrammeUpdate):
    db_programme = get_programme(db, programme_id)
    if not db_programme:
        return None
    for key, value in programme.model_dump(exclude_unset=True).items():
        setattr(db_programme, key, value)
    db.commit()
    db.refresh(db_programme)
    return db_programme

def delete_programme(db: Session, programme_id: int):
    db_programme = get_programme(db, programme_id)
    if db_programme:
        db.delete(db_programme)
        db.commit()
        return True
    return False

def enroll_participant(db: Session, programme_id: int, participant_id: str):
    # Check if already enrolled
    enrolment = db.query(models.ProgrammeParticipant).filter(
        and_(
            models.ProgrammeParticipant.programme_id == programme_id,
            models.ProgrammeParticipant.participant_id == participant_id
        )
    ).first()
    if enrolment:
        return enrolment
    
    db_enrolment = models.ProgrammeParticipant(
        programme_id=programme_id,
        participant_id=participant_id,
        status="Approved"
    )
    db.add(db_enrolment)
    
    # Increment enrolment counter
    prog = get_programme(db, programme_id)
    if prog:
        prog.current_enrolment += 1
        
    db.commit()
    db.refresh(db_enrolment)
    return db_enrolment

def assign_trainer_to_programme(db: Session, programme_id: int, trainer_id: str):
    existing = db.query(models.ProgrammeTrainer).filter(
        and_(
            models.ProgrammeTrainer.programme_id == programme_id,
            models.ProgrammeTrainer.trainer_id == trainer_id
        )
    ).first()
    if existing:
        return existing
    db_pt = models.ProgrammeTrainer(programme_id=programme_id, trainer_id=trainer_id)
    db.add(db_pt)
    db.commit()
    db.refresh(db_pt)
    return db_pt


# --- Session Operations ---
def get_session(db: Session, session_id: int):
    return db.query(models.Session).filter(models.Session.id == session_id).first()

def get_programme_sessions(db: Session, programme_id: int):
    return db.query(models.Session).filter(models.Session.programme_id == programme_id).order_by(models.Session.session_number.asc()).all()

def create_session(db: Session, session: schemas.SessionCreate):
    db_session = models.Session(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_session(db: Session, session_id: int, session_update: dict):
    db_session = get_session(db, session_id)
    if not db_session:
        return None
    for key, value in session_update.items():
        if hasattr(db_session, key):
            setattr(db_session, key, value)
    db.commit()
    db.refresh(db_session)
    return db_session

def delete_session(db: Session, session_id: int):
    db_session = get_session(db, session_id)
    if db_session:
        db.delete(db_session)
        db.commit()
        return True
    return False


# --- Attendance Operations ---
def get_attendance(db: Session, session_id: int, participant_id: str):
    return db.query(models.Attendance).filter(
        and_(
            models.Attendance.session_id == session_id,
            models.Attendance.participant_id == participant_id
        )
    ).first()

def mark_attendance(db: Session, attendance_in: schemas.AttendanceBase, session_id: int, participant_id: str):
    db_att = get_attendance(db, session_id, participant_id)
    if db_att:
        db_att.status = attendance_in.status
        db_att.gps_lat = attendance_in.gps_lat
        db_att.gps_lng = attendance_in.gps_lng
        db_att.verified_by_gps = attendance_in.verified_by_gps
        db_att.verified_by_qr = attendance_in.verified_by_qr
        db_att.timestamp = datetime.datetime.utcnow()
    else:
        db_att = models.Attendance(
            session_id=session_id,
            participant_id=participant_id,
            status=attendance_in.status,
            gps_lat=attendance_in.gps_lat,
            gps_lng=attendance_in.gps_lng,
            verified_by_gps=attendance_in.verified_by_gps,
            verified_by_qr=attendance_in.verified_by_qr,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return db_att

def override_attendance(db: Session, session_id: int, participant_id: str, override_in: schemas.AttendanceOverride, admin_user_id: str):
    db_att = get_attendance(db, session_id, participant_id)
    if not db_att:
        db_att = models.Attendance(
            session_id=session_id,
            participant_id=participant_id,
            status=override_in.status,
            manual_override=True,
            overridden_by=admin_user_id,
            notes=override_in.notes,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(db_att)
    else:
        db_att.status = override_in.status
        db_att.manual_override = True
        db_att.overridden_by = admin_user_id
        db_att.notes = override_in.notes
        db_att.timestamp = datetime.datetime.utcnow()
    db.commit()
    db.refresh(db_att)
    return db_att

def get_programme_attendance_analytics(db: Session, programme_id: int):
    # Total participants enrolled
    participants = db.query(models.ProgrammeParticipant).filter(models.ProgrammeParticipant.programme_id == programme_id).all()
    participant_ids = [p.participant_id for p in participants]
    
    # Sessions list
    sessions = db.query(models.Session).filter(models.Session.programme_id == programme_id).all()
    session_ids = [s.id for s in sessions]
    
    if not session_ids or not participant_ids:
        return {"average_attendance": 0.0, "present_count": 0, "absent_count": 0, "late_count": 0}
        
    records = db.query(models.Attendance).filter(models.Attendance.session_id.in_(session_ids)).all()
    
    present = sum(1 for r in records if r.status == "Present")
    absent = sum(1 for r in records if r.status == "Absent")
    late = sum(1 for r in records if r.status == "Late")
    
    total_slots = len(session_ids) * len(participant_ids)
    average = ((present + late) / total_slots * 100.0) if total_slots > 0 else 0.0
    
    return {
        "average_attendance": round(average, 1),
        "present_count": present,
        "absent_count": absent,
        "late_count": late
    }


# --- Material (Content) Operations ---
def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def get_materials(db: Session, programme_id: Optional[int] = None, session_id: Optional[int] = None):
    query = db.query(models.Material)
    if programme_id:
        query = query.filter(models.Material.programme_id == programme_id)
    if session_id:
        query = query.filter(models.Material.session_id == session_id)
    return query.order_by(models.Material.created_at.desc()).all()


# --- Assessments & Submissions ---
def create_assessment(db: Session, assessment: schemas.AssessmentCreate):
    db_assessment = models.Assessment(**assessment.model_dump())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def get_assessments(db: Session, programme_id: int):
    return db.query(models.Assessment).filter(models.Assessment.programme_id == programme_id).all()

def get_assessment(db: Session, assessment_id: int):
    return db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()

def get_submission(db: Session, assessment_id: int, participant_id: str):
    return db.query(models.AssessmentSubmission).filter(
        and_(
            models.AssessmentSubmission.assessment_id == assessment_id,
            models.AssessmentSubmission.participant_id == participant_id
        )
    ).first()

def create_submission(db: Session, submission: schemas.AssessmentSubmissionCreate, participant_id: str):
    db_sub = get_submission(db, submission.assessment_id, participant_id)
    if db_sub:
        db_sub.submission_data = submission.submission_data
        db_sub.file_url = submission.file_url
        db_sub.submitted_at = datetime.datetime.utcnow()
    else:
        db_sub = models.AssessmentSubmission(
            assessment_id=submission.assessment_id,
            participant_id=participant_id,
            submission_data=submission.submission_data,
            file_url=submission.file_url,
            submitted_at=datetime.datetime.utcnow()
        )
        db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def grade_submission(db: Session, submission_id: int, grade_in: schemas.AssessmentSubmissionGrade, evaluator_id: str):
    db_sub = db.query(models.AssessmentSubmission).filter(models.AssessmentSubmission.id == submission_id).first()
    if db_sub:
        db_sub.score = grade_in.score
        db_sub.grade = grade_in.grade
        db_sub.feedback = grade_in.feedback
        db_sub.evaluated_by = evaluator_id
        db_sub.evaluated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(db_sub)
    return db_sub


# --- Project Submissions ---
def get_project_submission(db: Session, programme_id: int, participant_id: str):
    return db.query(models.ProjectSubmission).filter(
        and_(
            models.ProjectSubmission.programme_id == programme_id,
            models.ProjectSubmission.participant_id == participant_id
        )
    ).first()

def create_project_submission(db: Session, project: schemas.ProjectSubmissionCreate, participant_id: str):
    db_proj = get_project_submission(db, project.programme_id, participant_id)
    if db_proj:
        db_proj.title = project.title
        db_proj.abstract = project.abstract
        db_proj.description = project.description
        db_proj.github_link = project.github_link
        db_proj.presentation_url = project.presentation_url
        db_proj.report_url = project.report_url
        db_proj.demo_video_url = project.demo_video_url
        db_proj.submitted_at = datetime.datetime.utcnow()
    else:
        db_proj = models.ProjectSubmission(
            programme_id=project.programme_id,
            participant_id=participant_id,
            title=project.title,
            abstract=project.abstract,
            description=project.description,
            github_link=project.github_link,
            presentation_url=project.presentation_url,
            report_url=project.report_url,
            demo_video_url=project.demo_video_url,
            submitted_at=datetime.datetime.utcnow()
        )
        db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj

def grade_project(db: Session, project_id: int, grade_in: schemas.ProjectSubmissionGrade, evaluator_id: str):
    db_proj = db.query(models.ProjectSubmission).filter(models.ProjectSubmission.id == project_id).first()
    if db_proj:
        db_proj.score = grade_in.score
        db_proj.grade = grade_in.grade
        db_proj.feedback = grade_in.feedback
        db_proj.evaluated_by = evaluator_id
        db_proj.evaluated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(db_proj)
    return db_proj


# --- Feedback Operations ---
def create_feedback(db: Session, feedback: schemas.FeedbackCreate, participant_id: str):
    db_fb = models.Feedback(
        programme_id=feedback.programme_id,
        session_id=feedback.session_id,
        participant_id=participant_id,
        rating_trainer=feedback.rating_trainer,
        rating_content=feedback.rating_content,
        rating_venue=feedback.rating_venue,
        rating_facilities=feedback.rating_facilities,
        rating_overall=feedback.rating_overall,
        feedback_text=feedback.feedback_text,
        suggestions=feedback.suggestions
    )
    db.add(db_fb)
    db.commit()
    db.refresh(db_fb)
    return db_fb

def get_feedbacks(db: Session, programme_id: int, session_id: Optional[int] = None):
    query = db.query(models.Feedback).filter(models.Feedback.programme_id == programme_id)
    if session_id:
        query = query.filter(models.Feedback.session_id == session_id)
    return query.all()


# --- Impact Assessment Operations ---
def create_impact_assessment(db: Session, impact: schemas.ImpactAssessmentCreate, participant_id: str):
    db_ia = db.query(models.ImpactAssessment).filter(
        and_(
            models.ImpactAssessment.programme_id == impact.programme_id,
            models.ImpactAssessment.participant_id == participant_id
        )
    ).first()
    if db_ia:
        db_ia.pre_survey_score = impact.pre_survey_score
        db_ia.post_survey_score = impact.post_survey_score
        db_ia.skill_improvement = impact.skill_improvement
        db_ia.knowledge_gain = impact.knowledge_gain
        db_ia.behaviour_change = impact.behaviour_change
        db_ia.organizational_impact = impact.organizational_impact
        db_ia.roi_score = impact.roi_score
    else:
        db_ia = models.ImpactAssessment(
            programme_id=impact.programme_id,
            participant_id=participant_id,
            pre_survey_score=impact.pre_survey_score,
            post_survey_score=impact.post_survey_score,
            skill_improvement=impact.skill_improvement,
            knowledge_gain=impact.knowledge_gain,
            behaviour_change=impact.behaviour_change,
            organizational_impact=impact.organizational_impact,
            roi_score=impact.roi_score
        )
        db.add(db_ia)
    db.commit()
    db.refresh(db_ia)
    return db_ia


# --- Certificates Operations ---
def create_certificate(db: Session, programme_id: int, participant_id: str, cert_no: str, file_path: str, file_url: str, qr_hash: str, sig: Optional[str] = None):
    # Remove existing
    db.query(models.Certificate).filter(
        and_(
            models.Certificate.programme_id == programme_id,
            models.Certificate.participant_id == participant_id
        )
    ).delete()
    db_cert = models.Certificate(
        programme_id=programme_id,
        participant_id=participant_id,
        certificate_number=cert_no,
        file_path=file_path,
        file_url=file_url,
        qr_hash=qr_hash,
        digital_signature=sig,
        is_verified=True
    )
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

def get_certificate(db: Session, programme_id: int, participant_id: str):
    return db.query(models.Certificate).filter(
        and_(
            models.Certificate.programme_id == programme_id,
            models.Certificate.participant_id == participant_id
        )
    ).first()

def verify_certificate(db: Session, qr_hash: str):
    return db.query(models.Certificate).filter(models.Certificate.qr_hash == qr_hash).first()


# --- Corporate Operations ---
def create_corporate_client(db: Session, client: schemas.CorporateClientCreate):
    db_client = models.CorporateClient(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_corporate_clients(db: Session):
    return db.query(models.CorporateClient).order_by(models.CorporateClient.company_name.asc()).all()

def create_corporate_contract(db: Session, contract: schemas.CorporateContractCreate):
    db_contract = models.CorporateContract(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def get_corporate_contracts(db: Session, client_id: Optional[int] = None):
    query = db.query(models.CorporateContract)
    if client_id:
        query = query.filter(models.CorporateContract.client_id == client_id)
    return query.order_by(models.CorporateContract.created_at.desc()).all()


# --- Analytics & Dashboard Stats ---
def get_dashboard_stats(db: Session) -> Dict[str, Any]:
    total_p = db.query(models.Programme).count()
    active_p = db.query(models.Programme).filter(models.Programme.status == "Active").count()
    upcoming_p = db.query(models.Programme).filter(models.Programme.status == "Upcoming").count()
    completed_p = db.query(models.Programme).filter(models.Programme.status == "Completed").count()
    
    total_participants = db.query(models.User).join(models.Profile).filter(models.Profile.role == "Participant").count()
    
    # Average attendance across all sessions
    avg_att_sub = db.query(
        func.sum(
            models.Attendance.status.in_(["Present", "Late"])
        ).label("present_sum"),
        func.count(models.Attendance.id).label("total_count")
    ).first()
    
    avg_att = 0.0
    if avg_att_sub and avg_att_sub.total_count and avg_att_sub.total_count > 0:
        avg_att = (avg_att_sub.present_sum / avg_att_sub.total_count) * 100.0
        
    # Average overall feedback rating
    avg_fb = db.query(func.avg(models.Feedback.rating_overall)).scalar() or 4.5
    
    # Corporate trainings count & Revenue
    corp_count = db.query(models.CorporateContract).count()
    total_rev = db.query(func.sum(models.CorporateContract.invoice_amount)).filter(models.CorporateContract.invoice_status == "Paid").scalar() or 0.0
    
    return {
        "total_programmes": total_p,
        "active_programmes": active_p,
        "upcoming_programmes": upcoming_p,
        "completed_programmes": completed_p,
        "total_participants": total_participants,
        "average_attendance": round(float(avg_att), 1),
        "average_feedback_rating": round(float(avg_fb), 1),
        "corporate_trainings_count": corp_count,
        "total_revenue": float(total_rev)
    }


# --- RAG Embeddings Storage & Query ---
def save_document_embedding(db: Session, material_id: Optional[int], filename: str, chunk_text: str, embedding_vector: List[float]):
    db_emb = models.DocumentEmbedding(
        material_id=material_id,
        filename=filename,
        text_chunk=chunk_text,
        embedding=embedding_vector
    )
    db.add(db_emb)
    db.commit()
    return db_emb

def query_similar_chunks(db: Session, query_vector: List[float], limit: int = 4) -> List[models.DocumentEmbedding]:
    # Custom similarity function or standard query
    # Since we installed pgvector, if Vector is active we can query using distance operators.
    # Otherwise, if Vector is fallback (JSON), we'll do similarity calculation in Python or direct DB search.
    # To support pgvector, we can run a raw SQL query or check models.Vector.
    if models.Vector is not None:
        # standard pgvector query: embedding.cosine_distance(query_vector)
        # using SQLAlchemy order_by
        return db.query(models.DocumentEmbedding).order_by(
            models.DocumentEmbedding.embedding.cosine_distance(query_vector)
        ).limit(limit).all()
    else:
        # Fallback to returning all chunks for matching in Python, capped to a reasonable number
        return db.query(models.DocumentEmbedding).limit(50).all()
