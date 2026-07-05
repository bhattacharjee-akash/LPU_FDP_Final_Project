import os
import sys

# Add backend and root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.pdf_parser import PDFParser
from app.main import run_agentic_workflow
from app import crud, models, schemas

def test():
    db = SessionLocal()
    try:
        # Create a mock user if not exists
        user_id = "test-user-id"
        email = "test@lpu.co.in"
        db_user = crud.get_user(db, user_id)
        if not db_user:
            crud.create_user(db, schemas.UserCreate(id=user_id, email=email))
            print(f"Created test user: {user_id}")
            
        # Create mock profile
        profile = crud.get_profile(db, user_id)
        if not profile:
            crud.create_profile(db, schemas.ProfileCreate(user_id=user_id, name="Test Faculty", department="CSE"))
            print("Created test faculty profile")

        # Read sample syllabus
        syllabus_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "sample_syllabus.pdf")
        if not os.path.exists(syllabus_path):
            print(f"Sample syllabus PDF not found at: {syllabus_path}")
            # Generate it first
            from scripts.generate_sample_syllabus import generate_pdf
            generate_pdf()
            
        with open(syllabus_path, "rb") as f:
            file_bytes = f.read()
            
        parsed_text = PDFParser.parse_pdf(file_bytes)
        print("Syllabus parsed successfully.")
        
        # Save Syllabus row
        syllabus_create = schemas.SyllabusCreate(
            user_id=user_id,
            filename="sample_syllabus.pdf",
            file_path="syllabi/test/sample_syllabus.pdf",
            raw_text=parsed_text,
            course_name="Modern AI Systems",
            course_code="CSE402"
        )
        db_syllabus = crud.create_syllabus(db, syllabus_create)
        print(f"Created syllabus row with ID: {db_syllabus.id}")
        
        # Run workflow synchronously to catch traceback
        settings_info = crud.get_settings(db, user_id)
        print("Starting multi-agent workflow...")
        
        # Run
        run_agentic_workflow(
            syllabus_id=db_syllabus.id,
            user_id=user_id,
            provider=settings_info.llm_provider,
            model_name=settings_info.model_name,
            temp=settings_info.temperature
        )
        
        print("\nWorkflow run completed. Checking logs:")
        logs = crud.get_logs(db, db_syllabus.id)
        for log in logs:
            print(f"[{log.created_at.strftime('%H:%M:%S')}] {log.agent_name} ({log.status}): {log.log_message}")
            
    except Exception as e:
        import traceback
        print("\nPipeline failed with exception:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test()
