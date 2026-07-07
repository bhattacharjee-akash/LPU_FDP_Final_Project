# LPU Academic Copilot — Development Blueprint (Layman's Guide)
> **A Comprehensive, Step-by-Step Guide to Building LPU Academic Copilot From Scratch**

Imagine a faculty coordinator who has to spend 8 hours preparing a curriculum pack (schedules, assignments, exam papers, quizzes) for a new semester. 

The **LPU Academic Copilot** solves this by letting the coordinator upload a syllabus PDF. In the background, **10 specialized AI agents** collaborate to parse the document, generate the weekly content, verify academic quality, and compile a publication-ready PDF in 30 seconds.

---

## 📂 Part 1: Folders and Workspace Setup

We build this using a **decoupled monorepo** structure. This means the frontend user interface and the backend processing engine live in the same project folder but run as completely separate systems.

```text
lpu-academic-copilot/          # Project Root
├── backend/                   # Python FastAPI Backend (Processing Engine)
│   ├── app/
│   │   ├── agents/            # The 10 AI Agent Nodes
│   │   ├── prompts/           # Text instructions for the AI
│   │   ├── main.py            # API Routes and Orchestrator
│   │   ├── models.py          # Database Schema tables
│   │   └── database.py        # Database Connector
│   └── requirements.txt       # Python Libraries needed
├── frontend/                  # Next.js 15 Client App (Visual Interface)
│   ├── src/
│   │   ├── app/               # Uploader, History, and Settings Pages
│   │   └── lib/               # API and Supabase connectors
│   └── package.json           # Node.js Libraries needed
└── scripts/                   # Local verification testing scripts
```

---

## 🗄️ Part 2: Database and Authentication Setup

To store the generated academic packs, user logins, and progress logs, we connect our backend to a **Supabase PostgreSQL database**.

### 1. The Database Tables (in Simple Terms)
* **`users`**: Remembers who is logged in.
* **`faculty_profiles`**: Holds the faculty coordinator’s name and department to sign the footer of the generated PDF reports.
* **`application_settings`**: Saves configurations like which AI model to use (Gemini 1.5 Flash vs. Gemini 1.5 Pro) and the reasoning temperature.
* **`syllabi`**: Stores the parsed text of the syllabus PDF you uploaded.
* **`generation_histories`**: Tracks whether the multi-agent task is `PENDING`, `PROCESSING`, `COMPLETED`, or `FAILED`.
* **`agent_execution_logs`**: Stores real-time status updates from the agents (e.g. *"QuizAgent started generating 20 MCQs"*). **This table feeds the animated timeline in the browser.**

### 2. Local Fallback Database
To ensure developers can test without installing databases:
* The backend code checks if a remote database URL is present.
* If missing, it automatically creates a local **SQLite** file (`local_copilot.db`) in your project folder, so the app runs without external configurations.

---

## 🤖 Part 3: The 10 AI Agents (The Brains)

Instead of using one massive AI prompt, we divide the work among **10 specialized agent files** in `backend/app/agents/`. Each agent gets a targeted template prompt (stored in `backend/app/prompts/`) and is configured to return structured **JSON data**.

```text
            [ Uploaded Syllabus PDF ]
                       │
                       ▼
               1. Planning Agent (Extracts Units & Outcomes)
                       │
      ┌────────────────┼────────────────┬────────────────┐
      ▼                ▼                ▼                ▼
2. Lesson Plan   3. Assignment      4. Quiz        5. Exam Paper
    Agent            Agent           Agent             Agent
  (15 Weeks)      (3 Projects)     (20 MCQs)       (Mid/End-Sem)
      │                │                │                │
      └────────────────┼────────────────┴────────────────┘
                       ▼
               6. Bloom Taxonomy Agent (Calculates Cognitive Depth)
                       │
                       ▼
               7. Course Outcome (CO) Mapping Agent
                       │
                       ▼
               8. Reviewer Agent (Checks for Typos & Consistency)
                       │
                       ▼
               9. Academic Quality Agent (Gives Grade Score 0-100)
                       │
                       ▼
              10. PDF Generator Node (Compiles ReportLab PDF)
```

1. **Planning Agent**: Reads the raw text of the syllabus, extracts the course name/code, and returns a structured map of units and Course Outcomes (COs).
2. **Lesson Plan Agent**: Creates a 15-week delivery schedule detailing lecture topics, teaching methods, and textbook page references.
3. **Assignment Agent**: Formulates three progressive academic assignments (Recall, Application, Design).
4. **Quiz Agent**: Generates 20 high-quality multiple-choice questions (MCQs) with an answer key and explanations.
5. **Question Paper Agent**: Drafts the Mid-Semester (50 marks) and End-Semester (100 marks) exam papers aligned to university patterns.
6. **Bloom Agent**: Scans the syllabus and maps each generated item to a cognitive depth level (L1: Remember ➔ L6: Create).
7. **CO Mapping Agent**: Maps the exam questions back to the Course Outcomes.
8. **Reviewer Agent**: Acts as an editor, verifying that there are no formatting bugs, inconsistencies, or typos.
9. **Academic Quality Agent**: Checklist auditor that evaluates the completed pack and awards a final compliance score (0-100) with written recommendations.
10. **PDF Generator Node**: Takes all the generated JSON contents and compiles them into a publication-ready PDF using the **ReportLab** layout engine.

---

## ⚙️ Part 4: The Backend Engine (FastAPI)

The backend handles requests, validates database operations, and triggers background workers.

### 1. Dependencies (`backend/requirements.txt`)
* `fastapi`, `uvicorn`: Web framework and server runner.
* `sqlalchemy`, `psycopg2-binary`: Database operations and PostgreSQL driver.
* `alembic`: Database migrations.
* `pypdf`: Extracts text from syllabus PDFs.
* `reportlab`: Compiles PDF layout elements.
* `google-generativeai`: Official SDK to call Google Gemini models.

### 2. Main API Flow (`backend/app/main.py`)
When you click upload, the API processes requests asynchronously:
```python
@app.post("/api/upload")
def upload_syllabus_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. Parse text from the uploaded PDF
    raw_text = PDFParser.extract_text(file.file)
    
    # 2. Save a pending syllabus record in the database
    syllabus = crud.create_syllabus(db, raw_text, file.filename, current_user["id"])
    crud.create_history_entry(db, current_user["id"], syllabus.id)
    
    # 3. Trigger the Multi-Agent orchestrator as a background task
    background_tasks.add_task(run_agent_orchestration, syllabus.id, current_user["id"])
    
    # 4. Instantly respond 200 OK so the user doesn't wait on the browser
    return {"syllabus_id": syllabus.id, "status": "PROCESSING"}
```

---

## 🖥️ Part 5: The Frontend User Interface (Next.js)

The frontend is a web page built with **Next.js 15** and **Tailwind CSS**.

### 1. Dependencies (`frontend/package.json`)
* `react`, `react-dom` (v19): Component rendering.
* `@supabase/supabase-js`: Client SDK to manage logins and signup widget tokens.
* `lucide-react`: Icon set.
* `framer-motion`: Animated page and progress bar transitions.

### 2. File Upload & Status Polling (`frontend/src/app/dashboard/upload/page.tsx`)
Once the file is uploaded, the frontend enters a polling loop. It makes a request to `/api/status/{syllabus_id}` every 3 seconds:
* It reads the progress logs in `agent_execution_logs`.
* It updates the progress bar and transitions the icons from gray (pending) to spinning orange (processing) to green checkmarks (completed).
* When all agents complete, it displays a download button pointing to the public PDF download route.

---

## 🚀 Part 6: How to Deploy the Project

### 1. Database & Auth Setup (Supabase)
1. Create a free project on [Supabase](https://supabase.com/).
2. Under **Project Settings -> API**, copy your `URL` and `anon public` key.
3. Under **Authentication -> Providers -> Email**, turn **OFF** "Confirm email" so users can register and test instantly without waiting for verification emails.

### 2. Backend Hosting (Render)
1. Connect your GitHub repository to [Render](https://render.com/).
2. Create a new **Web Service** and choose **Python** as the runtime.
3. Add the following environment variables:
   - `DATABASE_URL`: *Your Supabase connection pooler string (Port 6543).*
   - `GEMINI_API_KEY`: *Your Google Gemini API Key.*
   - `SUPABASE_URL` / `SUPABASE_ANON_KEY`: *Your Supabase credentials.*
4. Set the Start Command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Frontend Hosting (Vercel)
1. Import your repository into [Vercel](https://vercel.com/).
2. Choose **`frontend`** as the Root Directory.
3. Configure these environment variables:
   - `NEXT_PUBLIC_BACKEND_URL`: *Your Render backend URL.*
   - `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`: *Your Supabase credentials.*
4. Click **Deploy**.

---

## 💡 Part 7: Hard-Won Real-World Fixes (And Why They Matter)

If you copy-paste generic multi-agent code, it will crash in production. Here are the 5 critical problems we solved to make this app stable:

1. **The `pgbouncer` Parameter Issue**:
   * *Problem*: Supabase connection pooler URLs require `?pgbouncer=true` to manage traffic, but Python's database driver (`psycopg2`) throws an error because it doesn't recognize that parameter.
   * *Solution*: We wrote a string sanitizer in `backend/app/config.py` that intercepts the connection URL and automatically strips the `pgbouncer` query parameter before passing it to SQLAlchemy.
2. **Render IPv6 Connection Blocks**:
   * *Problem*: Render’s free tier containers do not support IPv6 routing. Direct Supabase connections (port `5432`) resolve to IPv6, resulting in a `Network is unreachable` crash.
   * *Solution*: We routed all database traffic through the **Supabase Transaction Pooler** (which operates on port **`6543`** and resolves to an IPv4 address).
3. **Browser Download Auth Loop**:
   * *Problem*: If you restrict the PDF download route to authorized users, clicking the download button in the browser will return a `401 Unauthorized` error because browser link clicks cannot send authorization headers.
   * *Solution*: We made the `/api/download/{syllabus_id}` endpoint public and fetched the faculty profile of the syllabus owner (`syllabus.user_id`) on-the-fly to sign the PDF footer.
4. **Namespace Imports**:
   * *Problem*: Uploads and PDF compilations crashed with a `NameError` in production.
   * *Solution*: Added missing standard library imports (`import datetime` and `import io`) to the top of `main.py`.
5. **Timeline Stuck on "Processing"**:
   * *Problem*: The final PDF compilation completed, but the timeline card in the browser remained stuck.
   * *Solution*: Added a log statement (`crud.create_log(db, syllabus_id, "PDFGenerator", "COMPLETED", ...)`) right after the ReportLab compiler finishes writing PDF bytes.
