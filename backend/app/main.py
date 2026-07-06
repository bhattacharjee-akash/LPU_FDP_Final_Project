import os
from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import datetime
import io

from app.config import settings
from app.database import get_db, engine, Base, supabase_client
from app import models, schemas, crud
from app.auth import get_current_user
from app.pdf_parser import PDFParser
from app.pdf_generator import PDFGenerator

# Import Agents
from app.agents.planning_agent import PlanningAgent
from app.agents.lesson_plan_agent import LessonPlanAgent
from app.agents.assignment_agent import AssignmentAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.question_paper_agent import QuestionPaperAgent
from app.agents.bloom_agent import BloomAgent
from app.agents.co_mapping_agent import COMappingAgent
from app.agents.reviewer_agent import ReviewerAgent
from app.agents.academic_quality_agent import AcademicQualityAgent

# Create DB Tables if they don't exist (Fallback if migrations aren't run manually)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "*"], # allow all in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Multi-Agent Workflow runner executed in BackgroundTask
def run_agentic_workflow(syllabus_id: int, user_id: str, provider: str, model_name: str, temp: float):
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        # 1. Fetch Syllabus
        syllabus = crud.get_syllabus(db, syllabus_id)
        if not syllabus:
            return
            
        crud.create_log(db, syllabus_id, "System", "STARTED", "Starting multi-agent orchestration pipeline.")
        crud.update_history_status(db, syllabus_id, "PROCESSING")

        # Hotfix override for invalid default model names
        if model_name == "gemini-2.5-flash":
            model_name = "gemini-1.5-flash"

        # Initialize agents with loaded user settings
        planner = PlanningAgent(provider, model_name, temp)
        lesson_planner = LessonPlanAgent(provider, model_name, temp)
        assignment_generator = AssignmentAgent(provider, model_name, temp)
        quiz_generator = QuizAgent(provider, model_name, temp)
        paper_generator = QuestionPaperAgent(provider, model_name, temp)
        bloom_mapper = BloomAgent(provider, model_name, temp)
        co_mapper = COMappingAgent(provider, model_name, temp)
        reviewer = ReviewerAgent(provider, model_name, temp)
        quality_evaluator = AcademicQualityAgent(provider, model_name, temp)

        # -- STEP 1: Planning Agent --
        crud.create_log(db, syllabus_id, "PlanningAgent", "STARTED", "Extracting Course Outlines, outcomes and unit sections.")
        planning_data = planner.run(syllabus.raw_text)
        # Update syllabus metadata in DB
        syllabus.course_name = planning_data.get("course_name")
        syllabus.course_code = planning_data.get("course_code")
        db.commit()
        crud.create_log(db, syllabus_id, "PlanningAgent", "COMPLETED", "Extracted syllabus details successfully.")

        # -- STEP 2: Lesson Plan Agent --
        crud.create_log(db, syllabus_id, "LessonPlanAgent", "STARTED", "Constructing 15-week weekly delivery schedule.")
        lesson_plan_data = lesson_planner.run(planning_data)
        crud.create_lesson_plan(db, syllabus_id, "Weekly Teaching Plan", lesson_plan_data)
        crud.create_log(db, syllabus_id, "LessonPlanAgent", "COMPLETED", "Created 15-week teaching plan.")

        # -- STEP 3: Assignment Agent --
        crud.create_log(db, syllabus_id, "AssignmentAgent", "STARTED", "Formulating three academic assignments.")
        assignments_data = assignment_generator.run(planning_data)
        crud.create_assignment(db, syllabus_id, "Course Assignments", assignments_data)
        crud.create_log(db, syllabus_id, "AssignmentAgent", "COMPLETED", "Formulated 3 assignments successfully.")

        # -- STEP 4: Quiz Agent --
        crud.create_log(db, syllabus_id, "QuizAgent", "STARTED", "Generating 20 course-specific MCQs.")
        quiz_data = quiz_generator.run(planning_data)
        crud.create_quiz(db, syllabus_id, "Assessment MCQ Quiz", quiz_data)
        crud.create_log(db, syllabus_id, "QuizAgent", "COMPLETED", "Generated 20 MCQs.")

        # -- STEP 5: Question Paper Agent --
        crud.create_log(db, syllabus_id, "QuestionPaperAgent", "STARTED", "Drafting Mid-Semester and End-Semester exam drafts.")
        question_papers_data = paper_generator.run(planning_data)
        crud.create_question_paper(db, syllabus_id, "Mid-Semester", question_papers_data.get("mid_semester", {}))
        crud.create_question_paper(db, syllabus_id, "End-Semester", question_papers_data.get("end_semester", {}))
        crud.create_log(db, syllabus_id, "QuestionPaperAgent", "COMPLETED", "Drafted exam papers successfully.")

        # -- STEP 6: Bloom Agent --
        crud.create_log(db, syllabus_id, "BloomAgent", "STARTED", "Aligning curriculum elements to Bloom's Taxonomy levels.")
        bloom_data = bloom_mapper.run(planning_data)
        crud.create_bloom_report(db, syllabus_id, bloom_data)
        crud.create_log(db, syllabus_id, "BloomAgent", "COMPLETED", "Syllabus Bloom's alignment complete.")

        # -- STEP 7: CO Mapping Agent --
        crud.create_log(db, syllabus_id, "COMappingAgent", "STARTED", "Mapping generated exam questions to Course Outcomes.")
        co_data = co_mapper.run(planning_data, question_papers_data)
        crud.create_co_mapping(db, syllabus_id, co_data)
        crud.create_log(db, syllabus_id, "COMappingAgent", "COMPLETED", "Mapped questions to outcomes.")

        # -- STEP 8: Reviewer Agent --
        crud.create_log(db, syllabus_id, "ReviewerAgent", "STARTED", "Performing consistency check across generated plans.")
        review_data = reviewer.run(
            planning_data, lesson_plan_data, assignments_data, 
            quiz_data, question_papers_data, bloom_data, co_data
        )
        crud.create_log(db, syllabus_id, "ReviewerAgent", "COMPLETED", f"Artifacts check completed. Status: {review_data.get('overall_status', 'APPROVED')}")

        # -- STEP 9: Academic Quality Agent --
        crud.create_log(db, syllabus_id, "AcademicQualityAgent", "STARTED", "Evaluating syllabus compliance score and drafting improvements.")
        quality_data = quality_evaluator.run(
            planning_data, lesson_plan_data, assignments_data,
            quiz_data, question_papers_data, bloom_data, co_data, review_data
        )
        crud.create_quality_report(
            db, syllabus_id, 
            score=quality_data.get("overall_score", 85.0),
            suggestions=quality_data.get("suggestions", []),
            content=quality_data
        )
        crud.create_log(db, syllabus_id, "AcademicQualityAgent", "COMPLETED", f"Academic score calculated: {quality_data.get('overall_score')}/100")

        # -- STEP 10: PDF Generator --
        crud.create_log(db, syllabus_id, "PDFGenerator", "STARTED", "Compiling all documents into a publication-ready PDF report.")
        
        # Get Faculty profile details for cover page
        profile = crud.get_profile(db, user_id)
        faculty_name = profile.name if profile else "Faculty Member"
        dept_name = profile.department if profile else "Academic Department"
        
        pdf_bytes = PDFGenerator.generate_report(
            course_name=syllabus.course_name,
            course_code=syllabus.course_code,
            faculty_name=faculty_name,
            department=dept_name,
            lesson_plan=lesson_plan_data,
            assignments=assignments_data,
            quiz=quiz_data,
            question_papers=question_papers_data,
            bloom_mapping=bloom_data,
            co_mapping=co_data,
            quality_report=quality_data
        )
        
        # Upload generated PDF to Supabase Storage if configured, else store in DB dummy url
        file_path = f"reports/{user_id}/report_{syllabus_id}.pdf"
        file_url = f"/api/download/{syllabus_id}"  # default relative path downloads from backend API
        
        if supabase_client:
            try:
                # Create bucket if it doesn't exist
                try:
                    supabase_client.storage.create_bucket("reports")
                except:
                    pass
                
                # Upload bytes
                supabase_client.storage.from_("reports").upload(
                    file_path,
                    pdf_bytes,
                    file_options={"content-type": "application/pdf", "x-upsert": "true"}
                )
                # Obtain public url
                res_url = supabase_client.storage.from_("reports").get_public_url(file_path)
                if res_url:
                    file_url = res_url
            except Exception as e:
                print(f"Supabase PDF upload error: {str(e)}. Using fallback download route.")

        crud.create_pdf_report(db, syllabus_id, file_path, file_url)
        crud.create_log(db, syllabus_id, "System", "COMPLETED", "All agents completed execution successfully. Course Pack is ready!")
        crud.update_history_status(db, syllabus_id, "COMPLETED")

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Pipeline crashed:\n{error_trace}")
        try:
            crud.create_log(db, syllabus_id, "System", "FAILED", f"Workflow execution failed: {str(e)}")
            crud.update_history_status(db, syllabus_id, "FAILED")
        except:
            pass
    finally:
        db.close()


# --- REST API Endpoints ---

@app.post("/api/profile", response_model=schemas.ProfileResponse)
def save_profile(profile_data: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Ensure user exists in users table first
    db_user = crud.get_user(db, current_user["id"])
    if not db_user:
        crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))
        
    profile_data.user_id = current_user["id"]
    db_profile = crud.get_profile(db, current_user["id"])
    if db_profile:
        db_profile.name = profile_data.name
        db_profile.department = profile_data.department
        db.commit()
        db.refresh(db_profile)
        return db_profile
    return crud.create_profile(db, profile_data)

@app.get("/api/profile", response_model=schemas.ProfileResponse)
def get_profile(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_profile = crud.get_profile(db, current_user["id"])
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not configured.")
    return db_profile

@app.get("/api/settings", response_model=schemas.SettingsResponse)
def get_user_settings(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Ensure user exists
    db_user = crud.get_user(db, current_user["id"])
    if not db_user:
        crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))
    return crud.get_settings(db, current_user["id"])

@app.put("/api/settings", response_model=schemas.SettingsResponse)
def update_user_settings(settings_data: schemas.SettingsUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Ensure user exists
    db_user = crud.get_user(db, current_user["id"])
    if not db_user:
        crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))
    return crud.update_settings(db, current_user["id"], settings_data)

@app.post("/api/upload")
def upload_syllabus_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Ensure user exists
    db_user = crud.get_user(db, current_user["id"])
    if not db_user:
        crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF syllabus uploads are supported.")
        
    try:
        file_bytes = file.file.read()
        parsed_text = PDFParser.parse_pdf(file_bytes)
        
        # Save file to Supabase Storage if configured
        storage_path = f"syllabi/{current_user['id']}/{datetime.datetime.now().timestamp()}_{file.filename}"
        
        if supabase_client:
            try:
                try:
                    supabase_client.storage.create_bucket("syllabi")
                except:
                    pass
                
                supabase_client.storage.from_("syllabi").upload(
                    storage_path,
                    file_bytes,
                    file_options={"content-type": "application/pdf"}
                )
            except Exception as e:
                print(f"Supabase Syllabus upload error: {str(e)}")
                
        # Insert Syllabus details into DB
        syllabus_create = schemas.SyllabusCreate(
            user_id=current_user["id"],
            filename=file.filename,
            file_path=storage_path,
            raw_text=parsed_text,
            course_name=file.filename.replace(".pdf", ""),
            course_code=""
        )
        
        db_syllabus = crud.create_syllabus(db, syllabus_create)
        
        # Create PENDING entry in generation history
        crud.create_history_entry(db, current_user["id"], db_syllabus.id)
        
        # Fetch user application settings to run LLM
        settings_info = crud.get_settings(db, current_user["id"])
        
        # Trigger Multi-Agent Workflow in Background
        background_tasks.add_task(
            run_agentic_workflow,
            syllabus_id=db_syllabus.id,
            user_id=current_user["id"],
            provider=settings_info.llm_provider,
            model_name=settings_info.model_name,
            temp=settings_info.temperature
        )
        
        return {
            "syllabus_id": db_syllabus.id,
            "filename": db_syllabus.filename,
            "status": "PROCESSING",
            "message": "Syllabus parsing done. Agent workflow running in the background."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Syllabus upload failed: {str(e)}")

@app.get("/api/status/{syllabus_id}")
def get_execution_status(syllabus_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    syllabus = crud.get_syllabus(db, syllabus_id)
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found.")
    if syllabus.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized access.")
        
    logs = crud.get_logs(db, syllabus_id)
    history_entry = db.query(models.GenerationHistory).filter(models.GenerationHistory.syllabus_id == syllabus_id).first()
    
    return {
        "syllabus_id": syllabus_id,
        "status": history_entry.status if history_entry else "PENDING",
        "logs": [schemas.LogResponse.model_validate(l) for l in logs]
    }

@app.get("/api/report/{syllabus_id}", response_model=schemas.FullReportResponse)
def get_full_compiled_report(syllabus_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    report_data = crud.get_full_report(db, syllabus_id)
    if not report_data:
        raise HTTPException(status_code=404, detail="Report not generated.")
    if report_data["syllabus"].user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized access.")
    return report_data

@app.get("/api/download/{syllabus_id}")
def download_pdf_report(syllabus_id: int, db: Session = Depends(get_db)):
    syllabus = crud.get_syllabus(db, syllabus_id)
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found.")
        
    # Get details
    report = crud.get_full_report(db, syllabus_id)
    if not report or not report.get("lesson_plan"):
        raise HTTPException(status_code=400, detail="Report generation has not completed yet.")
        
    # Fetch profile based on syllabus owner
    profile = crud.get_profile(db, syllabus.user_id)
    faculty_name = profile.name if profile else "Faculty Coordinator"
    dept_name = profile.department if profile else "Academic Department"
    
    # Re-generate PDF on the fly or download from storage
    # Re-generating is extremely safe and fast, avoiding expiring Supabase storage signatures
    try:
        # Mock quality report structure if not fully saved
        q_rep = report.get("quality_report") or {"score": 85.0, "dimensions": {}, "suggestions": []}
        
        pdf_bytes = PDFGenerator.generate_report(
            course_name=syllabus.course_name,
            course_code=syllabus.course_code,
            faculty_name=faculty_name,
            department=dept_name,
            lesson_plan=report.get("lesson_plan"),
            assignments=report.get("assignments"),
            quiz=report.get("quiz"),
            question_papers={
                "mid_semester": report.get("mid_sem_paper"),
                "end_semester": report.get("end_sem_paper")
            },
            bloom_mapping=report.get("bloom_mapping"),
            co_mapping=report.get("co_mapping"),
            quality_report=q_rep
        )
        
        filename = f"LPU_Course_Package_{syllabus.course_code or 'Report'}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download report: {str(e)}")

@app.get("/api/history", response_model=List[schemas.HistoryResponse])
def get_user_generation_history(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.get_history(db, current_user["id"])

@app.get("/api/analytics")
def get_user_dashboard_analytics(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Ensure user exists
    db_user = crud.get_user(db, current_user["id"])
    if not db_user:
        crud.create_user(db, schemas.UserCreate(id=current_user["id"], email=current_user["email"]))
    return crud.get_analytics(db, current_user["id"])

@app.get("/api/debug-logs")
def get_debug_logs(db: Session = Depends(get_db)):
    logs = db.query(models.AgentExecutionLog).order_by(models.AgentExecutionLog.created_at.desc()).limit(50).all()
    histories = db.query(models.GenerationHistory).order_by(models.GenerationHistory.created_at.desc()).limit(10).all()
    return {
        "logs": [
            {
                "id": l.id, 
                "syllabus_id": l.syllabus_id, 
                "agent_name": l.agent_name, 
                "status": l.status, 
                "log_message": l.log_message, 
                "created_at": l.created_at
            } for l in logs
        ],
        "histories": [
            {
                "id": h.id, 
                "user_id": h.user_id, 
                "syllabus_id": h.syllabus_id, 
                "status": h.status, 
                "created_at": h.created_at
            } for h in histories
        ]
    }
