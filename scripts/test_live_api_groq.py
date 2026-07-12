import requests
import json
import time
import os

SUPABASE_URL = "https://iqytwvoyignnohsyhhdn.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxeXR3dm95aWdubm9oc3loaGRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODMyNjUyNjYsImV4cCI6MjA5ODg0MTI2Nn0.P7_5Ca9Zy_SQfk6tviyB8guhq0Vzwzo1S0KFtbl9dgs"
BACKEND_URL = "https://lpu-academic-copilot-backend.onrender.com"
SYLLABUS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "sample_syllabus.pdf")

def run_production_test():
    print("--- STARTING PRODUCTION GROQ END-TO-END VALIDATION ---")
    
    access_token = "fdp-test-bypass-token"
    user_id = "dev-user-id"
    print(f"Bypassing Supabase login. Using developer test token: {access_token}. Mock User ID: {user_id}")
    
    backend_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 1. Update user settings to Groq with llama-3.3-70b-versatile
    print("\nUpdating user settings to Groq (llama-3.3-70b-versatile)...")
    settings_payload = {
        "llm_provider": "groq",
        "model_name": "llama-3.1-8b-instant",
        "temperature": 0.7
    }
    settings_res = requests.put(f"{BACKEND_URL}/api/settings", headers=backend_headers, json=settings_payload)
    if settings_res.status_code != 200:
        print(f"Failed to update settings: {settings_res.status_code} - {settings_res.text}")
        return
    print("Settings updated successfully!")

    # 2. Upload sample syllabus PDF to the live Render Backend
    print(f"\nUploading syllabus PDF: {SYLLABUS_FILE}...")
    upload_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    with open(SYLLABUS_FILE, "rb") as f:
        files = {
            "file": (os.path.basename(SYLLABUS_FILE), f, "application/pdf")
        }
        upload_res = requests.post(f"{BACKEND_URL}/api/upload", headers=upload_headers, files=files)
        
    if upload_res.status_code != 200:
        print(f"Upload failed: {upload_res.status_code} - {upload_res.text}")
        return
        
    upload_data = upload_res.json()
    syllabus_id = upload_data.get("syllabus_id")
    print(f"Upload successful! Created Syllabus ID: {syllabus_id}. Status: {upload_data.get('status')}")
    
    # 3. Poll the execution status on the live backend
    print("\nStarting polling loop against Render backend...")
    status_url = f"{BACKEND_URL}/api/status/{syllabus_id}"
    
    printed_logs = set()
    
    for attempt in range(60): # Poll for up to 5 minutes
        status_res = requests.get(status_url, headers=upload_headers)
        if status_res.status_code != 200:
            print(f"Status poll failed: {status_res.status_code}")
            time.sleep(5)
            continue
            
        status_data = status_res.json()
        current_status = status_data.get("status")
        logs = status_data.get("logs", [])
        
        # Print new logs as they stream
        for log in logs:
            log_key = (log.get("agent_name"), log.get("status"), log.get("log_message"))
            if log_key not in printed_logs:
                print(f"[{log.get('agent_name')}] ({log.get('status')}): {log.get('log_message')}")
                printed_logs.add(log_key)
                
        if current_status == "COMPLETED":
            print("\n🎉 ORCHESTRATION COMPLETED SUCCESSFULLY IN PRODUCTION!")
            break
        elif current_status == "FAILED":
            print("\n❌ ORCHESTRATION FAILED IN PRODUCTION.")
            break
            
        time.sleep(5)
    else:
        print("\nTimeout waiting for orchestration to finish.")

if __name__ == "__main__":
    run_production_test()
