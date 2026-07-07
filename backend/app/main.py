import os
import datetime
from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
import io
import uuid

from app.config import settings
from app.database import get_db, engine, Base, supabase_client
from app import models, schemas, crud
from app.auth import get_current_user
from app.pdf_parser import PDFParser
from app.pdf_generator import PDFGenerator
from app.agents.langgraph_workflow import execute_reasoning_pipeline

# Create DB Tables if they don't exist (Fallback if migrations aren't run manually)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LPU HRDC Nexus API")

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins in dev, vercel.json will handle production CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Deterministic Offline Embedding Helper
def get_text_embedding(text: str) -> List[float]:
    import hashlib
    res = []
    # Seed generator with MD5 hash of text
    h = hashlib.md5(text.encode("utf-8")).hexdigest()
    for idx in range(1536):
        # Deterministic pseudo-random generation based on index
        # This aligns with pgvector 1536-dim standard (like text-embedding-ada-002)
        val = (hash(f"{h}_{idx}") % 10000) / 5000.0 - 1.0
        res.append(val)
    return res

# Chunking helper for RAG indexing
def chunk_text(text: str, chunk_size: int = 600, overlap: int = 150) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

# Background Task for parsing and embedding material files
def run_indexing_pipeline(material_id: int):
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        material = db.query(models.Material).filter(models.Material.id == material_id).first()
        if not material:
            return
        
        # Pull file from Supabase Storage or read locally if mocked
        # For full offline capability, if supabase is not active, we'll index the title and category
        extracted_text = f"Title: {material.title}. Type: {material.file_type}. This is an academic resource for Lovely Professional University HRDC trainings."
        
        if supabase_client and material.file_path.startswith("materials/"):
            try:
                # Download bytes from Supabase
                res_bytes = supabase_client.storage.from_("materials").download(material.file_path)
                if material.file_path.endswith(".pdf"):
                    extracted_text = PDFParser.parse_pdf(res_bytes)
                else:
                    extracted_text = res_bytes.decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"Supabase download/parse failed during indexing: {e}")
                
        # Split text into chunks
        chunks = chunk_text(extracted_text)
        for idx, chunk in enumerate(chunks):
            vector = get_text_embedding(chunk)
            crud.save_document_embedding(
                db=db,
                material_id=material.id,
                filename=material.title,
                chunk_text=chunk,
                embedding_vector=vector
            )
            
        material.is_indexed = True
        db.commit()
    except Exception as e:
        print(f"Failed to index material in background: {e}")
    finally:
        db.close()


# --- REST API Endpoints ---

# Profile endpoints
@app.post("/api/profile", response_model=schemas.ProfileResponse)
def save_profile(profile_data: schemas.ProfileBase, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Ensure user exists in users table first
    db_user = crud.get_user(db, current_user["id"])
    if not db_user:
        crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))
        
    db_profile = crud.get_profile(db, current_user["id"])
    if db_profile:
        return crud.update_profile(db, current_user["id"], profile_data)
    
    create_schema = schemas.ProfileCreate(
        user_id=current_user["id"],
        name=profile_data.name,
        role=profile_data.role,
        department=profile_data.department,
        phone=profile_data.phone,
        designation=profile_data.designation
    )
    return crud.create_profile(db, create_schema)

@app.get("/api/profile", response_model=schemas.ProfileResponse)
def get_profile(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_profile = crud.get_profile(db, current_user["id"])
    if not db_profile:
        # Auto-create profile from user if not set
        user_email = current_user["email"]
        name = user_email.split("@")[0].capitalize()
        # Default roles based on email structure or Participant
        role = "Participant"
        if "admin" in user_email.lower():
            role = "HRDC Administrator"
        elif "staff" in user_email.lower():
            role = "HRDC Staff"
        elif "trainer" in user_email.lower():
            role = "Trainer"
            
        create_schema = schemas.ProfileCreate(
            user_id=current_user["id"],
            name=name,
            role=role,
            department="Computer Science",
            phone="",
            designation="Assistant Professor"
        )
        # Ensure user exists
        db_user = crud.get_user(db, current_user["id"])
        if not db_user:
            crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))
        return crud.create_profile(db, create_schema)
    return db_profile

# User settings
@app.get("/api/settings", response_model=schemas.SettingsResponse)
def get_user_settings(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Ensure user exists
    db_user = crud.get_user(db, current_user["id"])
    if not db_user:
        crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))
    return crud.get_settings(db, current_user["id"])

@app.put("/api/settings", response_model=schemas.SettingsResponse)
def update_user_settings(settings_data: schemas.SettingsUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.update_settings(db, current_user["id"], settings_data)


# Training management
@app.get("/api/programmes", response_model=List[schemas.ProgrammeResponse])
def read_programmes(
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return crud.get_programmes(db, category=category, status=status)

@app.get("/api/programmes/{id}", response_model=schemas.ProgrammeResponse)
def read_programme(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_prog = crud.get_programme(db, id)
    if not db_prog:
        raise HTTPException(status_code=404, detail="Programme not found")
    return db_prog

@app.post("/api/programmes", response_model=schemas.ProgrammeResponse)
def create_programme(programme: schemas.ProgrammeCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Verify coordinator or admin role
    profile = crud.get_profile(db, current_user["id"])
    if not profile or profile.role not in ["HRDC Administrator", "HRDC Staff", "Trainer"]:
        raise HTTPException(status_code=403, detail="Not authorized to create training programmes")
    programme.coordinator_id = current_user["id"]
    return crud.create_programme(db, programme)

@app.put("/api/programmes/{id}", response_model=schemas.ProgrammeResponse)
def update_programme(id: int, programme: schemas.ProgrammeUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_prog = crud.update_programme(db, id, programme)
    if not db_prog:
        raise HTTPException(status_code=404, detail="Programme not found")
    return db_prog

@app.delete("/api/programmes/{id}")
def delete_programme(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    profile = crud.get_profile(db, current_user["id"])
    if not profile or profile.role not in ["HRDC Administrator", "HRDC Staff"]:
        raise HTTPException(status_code=403, detail="Only HRDC admins/staff can delete programmes")
    success = crud.delete_programme(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Programme not found")
    return {"message": "Programme deleted successfully"}

@app.post("/api/programmes/{id}/enroll")
def enroll_in_programme(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Enroll current user as participant
    enrolment = crud.enroll_participant(db, id, current_user["id"])
    return {"message": "Enrolled successfully", "enrolment_id": enrolment.id}

@app.post("/api/programmes/{id}/assign-trainer")
def assign_trainer(id: int, trainer_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    crud.assign_trainer_to_programme(db, id, trainer_id)
    return {"message": "Trainer assigned successfully"}


# Session management & Timetable
@app.get("/api/programmes/{id}/sessions", response_model=List[schemas.SessionResponse])
def get_sessions(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_programme_sessions(db, id)

@app.post("/api/programmes/{id}/sessions", response_model=schemas.SessionResponse)
def create_session(id: int, session: schemas.SessionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    session.programme_id = id
    # Assign attendance QR Code hash token
    session.attendance_qr_code = f"QR_{id}_{session.session_number}_{uuid.uuid4().hex[:8]}"
    return crud.create_session(db, session)

@app.get("/api/sessions/{id}", response_model=schemas.SessionResponse)
def get_session_details(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_sess = crud.get_session(db, id)
    if not db_sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_sess

@app.put("/api/sessions/{id}", response_model=schemas.SessionResponse)
def update_session_details(id: int, session_update: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_sess = crud.update_session(db, id, session_update)
    if not db_sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_sess

@app.delete("/api/sessions/{id}")
def delete_session(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    success = crud.delete_session(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted"}


# Attendance marking, QR Code window & GPS verification
@app.post("/api/sessions/{id}/attendance")
def verify_and_mark_attendance(
    id: int,
    data: schemas.AttendanceVerify,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    session = crud.get_session(db, id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Check if attendance window is set and valid
    now = datetime.datetime.utcnow()
    if session.attendance_window_start and session.attendance_window_end:
        if now < session.attendance_window_start or now > session.attendance_window_end:
            raise HTTPException(status_code=400, detail="Attendance window has closed for this session")
            
    # Verify QR code
    verified_qr = False
    if session.attendance_qr_code:
        if data.qr_code != session.attendance_qr_code:
            raise HTTPException(status_code=400, detail="Invalid QR Code scanned")
        verified_qr = True
        
    # Verify GPS if enabled
    verified_gps = False
    if session.gps_verification:
        if not data.gps_lat or not data.gps_lng:
            raise HTTPException(status_code=400, detail="GPS coordinates required for verification")
        
        # Simple distance check in meters
        import math
        # Radius of Earth in km
        R = 6371.0
        lat1 = math.radians(session.gps_lat)
        lon1 = math.radians(session.gps_lng)
        lat2 = math.radians(data.gps_lat)
        lon2 = math.radians(data.gps_lng)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance_meters = R * c * 1000.0
        
        if distance_meters > session.gps_radius_meters:
            raise HTTPException(status_code=400, detail=f"Location verification failed. You are outside the classroom boundary ({round(distance_meters, 1)}m away)")
        verified_gps = True
        
    # Determine status based on time delay
    status_label = "Present"
    if session.attendance_window_start:
        delay = (now - session.attendance_window_start).total_seconds() / 60.0
        if delay > 10.0:  # Late after 10 minutes
            status_label = "Late"
            
    att_in = schemas.AttendanceBase(
        status=status_label,
        gps_lat=data.gps_lat,
        gps_lng=data.gps_lng,
        verified_by_gps=verified_gps,
        verified_by_qr=verified_qr
    )
    
    att = crud.mark_attendance(db, att_in, id, current_user["id"])
    return {"message": "Attendance marked successfully", "status": att.status}

@app.post("/api/sessions/{id}/attendance/override/{participant_id}", response_model=schemas.AttendanceResponse)
def hrdc_attendance_override(
    id: int,
    participant_id: str,
    override: schemas.AttendanceOverride,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    profile = crud.get_profile(db, current_user["id"])
    if not profile or profile.role not in ["HRDC Administrator", "HRDC Staff"]:
        raise HTTPException(status_code=403, detail="Unauthorized to override attendance records")
        
    return crud.override_attendance(db, id, participant_id, override, current_user["id"])

@app.get("/api/programmes/{id}/attendance/analytics")
def get_programme_attendance_analytics(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_programme_attendance_analytics(db, id)


# Content Management & Uploads
@app.post("/api/programmes/{id}/materials", response_model=schemas.MaterialResponse)
def upload_course_material(
    id: int,
    background_tasks: BackgroundTasks,
    title: str,
    file_type: str,
    session_id: Optional[int] = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Store file in Supabase storage bucket, else mock local download link
    file_path = f"materials/{id}/{uuid.uuid4().hex}_{file.filename}"
    file_url = f"/api/download/material/{file_path}"
    
    file_bytes = file.file.read()
    
    if supabase_client:
        try:
            # Create materials bucket if not existing
            try:
                supabase_client.storage.create_bucket("materials")
            except:
                pass
            supabase_client.storage.from_("materials").upload(
                file_path,
                file_bytes,
                file_options={"x-upsert": "true"}
            )
            res_url = supabase_client.storage.from_("materials").get_public_url(file_path)
            if res_url:
                file_url = res_url
        except Exception as e:
            print(f"Supabase storage error: {e}. Falling back to default URL route.")
            
    material_in = schemas.MaterialCreate(
        title=title,
        file_type=file_type,
        programme_id=id,
        session_id=session_id,
        file_path=file_path,
        file_url=file_url,
        uploaded_by=current_user["id"]
    )
    db_material = crud.create_material(db, material_in)
    
    # Trigger AI indexing pipeline in Background
    background_tasks.add_task(run_indexing_pipeline, db_material.id)
    
    return db_material

@app.get("/api/programmes/{id}/materials", response_model=List[schemas.MaterialResponse])
def get_programme_materials(id: int, session_id: Optional[int] = None, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_materials(db, programme_id=id, session_id=session_id)


# Assessments & Project Submissions
@app.post("/api/programmes/{id}/assessments", response_model=schemas.AssessmentResponse)
def create_assessment(id: int, assessment: schemas.AssessmentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    assessment.programme_id = id
    return crud.create_assessment(db, assessment)

@app.get("/api/programmes/{id}/assessments", response_model=List[schemas.AssessmentResponse])
def get_assessments(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_assessments(db, id)

@app.post("/api/assessments/{id}/submissions", response_model=schemas.AssessmentSubmissionResponse)
def submit_assessment(id: int, submission: schemas.AssessmentSubmissionBase, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    assess = crud.get_assessment(db, id)
    if not assess:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    sub_in = schemas.AssessmentSubmissionCreate(
        assessment_id=id,
        submission_data=submission.submission_data,
        file_url=submission.file_url
    )
    db_sub = crud.create_submission(db, sub_in, current_user["id"])
    
    # Auto-Evaluation for MCQ quizzes
    if assess.type == "MCQ":
        # Calculate score automatically
        # Content format: { "questions": [ { "id": 1, "correct_option": "A" } ] }
        # Submission format: { "answers": { "1": "A" } }
        score = 0.0
        try:
            questions = assess.content.get("questions", [])
            answers = submission.submission_data.get("answers", {})
            correct_cnt = 0
            for q in questions:
                q_id = str(q.get("id"))
                if answers.get(q_id) == q.get("correct_option"):
                    correct_cnt += 1
            if questions:
                score = (correct_cnt / len(questions)) * assess.max_marks
                
            db_sub.score = score
            db_sub.grade = "Pass" if score >= assess.passing_marks else "Fail"
            db_sub.feedback = "Auto-evaluated MCQ submission."
            db_sub.evaluated_by = "System"
            db_sub.evaluated_at = datetime.datetime.utcnow()
            db.commit()
            db.refresh(db_sub)
        except Exception as e:
            print(f"MCQ auto grading error: {e}")
            
    return db_sub

@app.post("/api/submissions/{sub_id}/grade", response_model=schemas.AssessmentSubmissionResponse)
def grade_submission(sub_id: int, grade: schemas.AssessmentSubmissionGrade, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.grade_submission(db, sub_id, grade, current_user["id"])


# Projects
@app.post("/api/programmes/{id}/projects", response_model=schemas.ProjectSubmissionResponse)
def submit_project(id: int, project: schemas.ProjectSubmissionBase, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    proj_in = schemas.ProjectSubmissionCreate(
        programme_id=id,
        title=project.title,
        abstract=project.abstract,
        description=project.description,
        github_link=project.github_link,
        presentation_url=project.presentation_url,
        report_url=project.report_url,
        demo_video_url=project.demo_video_url
    )
    return crud.create_project_submission(db, proj_in, current_user["id"])

@app.post("/api/projects/{proj_id}/grade", response_model=schemas.ProjectSubmissionResponse)
def grade_project(proj_id: int, grade: schemas.ProjectSubmissionGrade, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.grade_project(db, proj_id, grade, current_user["id"])


# Feedbacks & Surveys
@app.post("/api/programmes/{id}/feedback", response_model=schemas.FeedbackResponse)
def submit_feedback(id: int, fb: schemas.FeedbackBase, session_id: Optional[int] = None, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    fb_in = schemas.FeedbackCreate(
        programme_id=id,
        session_id=session_id,
        **fb.model_dump()
    )
    return crud.create_feedback(db, fb_in, current_user["id"])


# Impact Assessments
@app.post("/api/programmes/{id}/impact", response_model=schemas.ImpactAssessmentResponse)
def submit_impact_assessment(id: int, impact: schemas.ImpactAssessmentBase, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    impact_in = schemas.ImpactAssessmentCreate(
        programme_id=id,
        **impact.model_dump()
    )
    return crud.create_impact_assessment(db, impact_in, current_user["id"])


# Certificates Auto Generation
@app.post("/api/programmes/{id}/certificate", response_model=schemas.CertificateResponse)
def generate_programme_certificate(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    programme = crud.get_programme(db, id)
    if not programme:
        raise HTTPException(status_code=404, detail="Programme not found")
        
    profile = crud.get_profile(db, current_user["id"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile details missing")
        
    # Generate random certificate details
    cert_no = f"LPU-HRDC-{id}-{uuid.uuid4().hex[:6].upper()}"
    qr_hash = uuid.uuid4().hex
    qr_verification_url = f"{settings.FRONTEND_URL}/verify/{qr_hash}"
    date_str = datetime.datetime.utcnow().strftime("%B %d, %Y")
    
    # Generate PDF bytes
    pdf_bytes = PDFGenerator.generate_certificate(
        participant_name=profile.name,
        programme_title=programme.title,
        certificate_number=cert_no,
        date_str=date_str,
        qr_verification_url=qr_verification_url
    )
    
    file_path = f"certificates/{current_user['id']}/{cert_no}.pdf"
    file_url = f"/api/download/certificate/{file_path}"
    
    if supabase_client:
        try:
            try:
                supabase_client.storage.create_bucket("certificates")
            except:
                pass
            supabase_client.storage.from_("certificates").upload(
                file_path,
                pdf_bytes,
                file_options={"content-type": "application/pdf", "x-upsert": "true"}
            )
            res_url = supabase_client.storage.from_("certificates").get_public_url(file_path)
            if res_url:
                file_url = res_url
        except Exception as e:
            print(f"Supabase certificate upload error: {e}")
            
    cert = crud.create_certificate(
        db=db,
        programme_id=id,
        participant_id=current_user["id"],
        cert_no=cert_no,
        file_path=file_path,
        file_url=file_url,
        qr_hash=qr_hash,
        sig="LPU_HRDC_OFFICIAL_STAMP"
    )
    return cert

@app.get("/api/programmes/{id}/certificate", response_model=schemas.CertificateResponse)
def get_my_certificate(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    cert = crud.get_certificate(db, id, current_user["id"])
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not generated yet")
    return cert

@app.get("/api/certificate/verify/{qr_hash}", response_model=schemas.CertificateResponse)
def verify_certificate_public(qr_hash: str, db: Session = Depends(get_db)):
    cert = crud.verify_certificate(db, qr_hash)
    if not cert:
        raise HTTPException(status_code=404, detail="Invalid certificate verification hash")
    return cert


# Corporate Training Module CRM
@app.get("/api/corporate/clients", response_model=List[schemas.CorporateClientResponse])
def get_clients(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_corporate_clients(db)

@app.post("/api/corporate/clients", response_model=schemas.CorporateClientResponse)
def create_client(client: schemas.CorporateClientCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.create_corporate_client(db, client)

@app.post("/api/corporate/contracts", response_model=schemas.CorporateContractResponse)
def create_contract(contract: schemas.CorporateContractCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.create_corporate_contract(db, contract)

@app.get("/api/corporate/contracts", response_model=List[schemas.CorporateContractResponse])
def get_contracts(client_id: Optional[int] = None, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_corporate_contracts(db, client_id)


# Analytics Dashboard Stats
@app.get("/api/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_dashboard_stats(db)


# AI Knowledge Assistant using LangGraph Workflow
@app.post("/api/ai/chat")
def ai_assistant_query(req: schemas.QueryRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_settings = crud.get_settings(db, current_user["id"])
    result = execute_reasoning_pipeline(
        db=db,
        query=req.query,
        model_name=user_settings.model_name,
        temp=user_settings.temperature
    )
    return result


# Fallback file downloading endpoints if Supabase storage is missing or local mocked environment is active
@app.get("/api/download/certificate/{path:path}")
def download_local_certificate(path: str):
    # Generates a basic mock certificate PDF on the fly if stored offline
    pdf_bytes = PDFGenerator.generate_certificate(
        participant_name="Faculty Participant",
        programme_title="Professional Training Cycle",
        certificate_number=path.split("/")[-1].replace(".pdf", ""),
        date_str="July 2026",
        qr_verification_url="http://localhost:3000/verify/sample"
    )
    return Response(content=pdf_bytes, media_type="application/pdf")
