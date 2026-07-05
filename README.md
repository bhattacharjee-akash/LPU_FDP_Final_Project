# LPU Academic Copilot
> **A Multi-Agent AI Platform for Faculty Workflow Automation**

Developed for the **Lovely Professional University (LPU) Faculty Development Program (FDP)** to demonstrate multi-agent orchestration, continuous quality checks, and structured academic package compilation.

---

## Architecture Overview
The platform decouples the **Next.js 15** frontend and the **FastAPI** backend, communicating over a RESTful API.
A syllabus PDF uploaded by a faculty member triggers a **10-Agent pipeline** running in the background.

```mermaid
graph TD
    User([Faculty Member]) -->|Upload Syllabus PDF| API[FastAPI Upload Route]
    API -->|1. Parse Text| PDFParser[PDF Parser]
    PDFParser -->|2. Extract Structure| PlanningAgent[Planning Agent]
    
    subgraph Multi-Agent Pipeline (Parallel Tasks)
        PlanningAgent --> LP[Lesson Plan Agent]
        PlanningAgent --> AS[Assignment Agent]
        PlanningAgent --> QZ[Quiz Agent]
        PlanningAgent --> QP[Question Paper Agent]
        PlanningAgent --> BL[Bloom taxonomy Agent]
    end
    
    LP & AS & QZ & QP & BL --> CO[CO Mapping Agent]
    CO --> Reviewer[Reviewer Agent]
    Reviewer --> Quality[Academic Quality Agent]
    Quality --> PDF[PDF Report Generator]
    
    PDF -->|Upload Report| S3[Supabase Storage]
    PDF -->|Complete| User
```

### Agents Mapping
1. **PlanningAgent**: Extracts units, Course Outcomes, and code metadata.
2. **LessonPlanAgent**: Builds weekly teaching plans spanning 15 weeks.
3. **AssignmentAgent**: Formulates three sets of progressive coursework questions.
4. **QuizAgent**: Compiles a bank of 20 detailed MCQs with explanations.
5. **QuestionPaperAgent**: Drafts Mid Semester (50 marks) and End Semester (100 marks) papers.
6. **BloomAgent**: Aligns curriculum modules to targeted cognitive levels.
7. **COMappingAgent**: Correlates questions and weights to Course Outcomes.
8. **ReviewerAgent**: Performs checks for typos and academic consistency.
9. **AcademicQualityAgent**: Evaluates the package to compute a compliance rating (0-100).
10. **PDF Report Generator**: Packages all results into a publication-ready PDF.

---

## Tech Stack
- **Frontend**: Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI (Python 3.12), SQLAlchemy, Uvicorn, PyPDF, ReportLab
- **Database**: Supabase PostgreSQL (utilizing SQLAlchemy and official Supabase Python SDK)
- **Primary LLM**: Google Gemini 2.5 Flash
- **Secondary LLM**: Groq Cloud API

---

## Configuration & Environments
Copy the `.env.example` file in the project root to `.env` in both folders or globally:

```bash
# Database Setup
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres

# Supabase Auth & Storage Setup
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-public-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# LLM Providers (At least GEMINI_API_KEY is recommended)
GEMINI_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...

# Next.js configurations
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-public-key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## Installation & Local Execution

### 1. Database Migrations (Alembic)
Launch a local PostgreSQL database or hook to your Supabase instance, then run:
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```
*(FastAPI's startup scripts contain `Base.metadata.create_all(bind=engine)` which automatically bootstraps all required tables if Alembic isn't run).*

### 2. Run Python Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API endpoints will run at `http://localhost:8000`.

### 3. Run Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your web browser.

---

## Docker Container Launch
Execute the complete environment via docker-compose (a sample Dockerfile is included inside the `/backend` folder):
```bash
# Build and run container
cd backend
docker build -t lpu-academic-copilot-backend .
docker run -p 8000:8000 --env-file .env lpu-academic-copilot-backend
```

---

## Hosting Deployments

### Backend (Render / Railway)
1. Link your repository.
2. Select **Python Web Service**.
3. Set Build Command: `pip install -r requirements.txt && alembic upgrade head`
4. Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Configure environment variables matching `.env.example`.

### Frontend (Vercel)
1. Link your repository.
2. Deploy the Next.js workspace.
3. Configure `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, and `NEXT_PUBLIC_BACKEND_URL` environment variables.
