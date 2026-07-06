# Local Installation & Configuration Guide
> **LPU Academic Copilot — Prerequisites, Environment Setup, and Local Execution**

This document provides step-by-step instructions to configure and run the LPU Academic Copilot on your local development machine.

---

## 1. Prerequisites
Ensure you have the following software installed:
* **Python** (version 3.10, 3.11, or 3.12/3.14)
* **Node.js LTS** (version 20 or later, npm 10+)
* **Git** CLI
* **PostgreSQL** or a **Supabase Project** account

---

## 2. Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/bhattacharjee-akash/LPU_FDP_Final_Project.git
cd LPU_FDP_Final_Project
```

---

## 3. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file inside the `backend` folder matching these environment variables:
   ```env
   DATABASE_URL=sqlite:///./local_copilot.db # Fallback local database
   SUPABASE_URL=https://iqytwvoyignnohsyhhdn.supabase.co
   SUPABASE_ANON_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
   GEMINI_API_KEY=your-gemini-api-key
   FRONTEND_URL=http://localhost:3000
   ```
5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```
   *(FastAPI will also automatically create SQLite tables if a local DB is not found).*
6. Start the FastAPI backend:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## 4. Frontend Setup
1. Open a new terminal window and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install the frontend dependencies:
   ```bash
   npm install --legacy-peer-deps
   ```
3. Create a `.env.local` file inside the `frontend` folder matching these variables:
   ```env
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   NEXT_PUBLIC_SUPABASE_URL=https://iqytwvoyignnohsyhhdn.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Open your web browser and navigate to **`http://localhost:3000`**.

---

## 5. Running the Pipeline Tests
You can verify the backend is compiling and communicating locally without running the UI:
1. Navigate to the root directory.
2. Run:
   ```bash
   python scripts/test_pipeline.py
   ```
   This will parse the sample syllabus PDF located in `/scripts` and execute the 10 agents sequentially, saving the output logs to the local SQLite database.
