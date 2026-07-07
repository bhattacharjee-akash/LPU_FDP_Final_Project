import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_presentation():
    prs = Presentation()
    
    # Define color scheme (LPU Orange & Charcoal theme)
    ORANGE = RGBColor(231, 120, 23)   # LPU Orange
    CHARCOAL = RGBColor(26, 37, 44)   # Charcoal Dark
    LIGHT_GRAY = RGBColor(245, 245, 245)
    
    slides_data = [
        # Slide 1: Title
        {
            "layout": 0,
            "title": "LPU HRDC Nexus",
            "subtitle": "An AI-Powered Training Lifecycle Management Platform\nLovely Professional University (LPU) HRDC Leadership Capstone",
            "notes": "Good morning members of the HRDC leadership panel. Today, we present LPU HRDC Nexus, an enterprise-grade AI-powered training lifecycle management platform designed to automate and digitize the complete training program pipeline."
        },
        # Slide 2: Project Objectives
        {
            "layout": 1,
            "title": "Objectives of LPU HRDC Nexus",
            "bullets": [
                "Manage the complete lifecycle of faculty development (FDPs), workshops, refresher courses, and orientations.",
                "Automate classroom check-in via geofenced QR Code scanning.",
                "Provide multi-format academic evaluations (MCQ, Subjective, Coding, Project Submissions).",
                "Integrate digital certificate compilation with QR verification page and digital signatures.",
                "Establish a corporate training module to log client invoices and contract agreements."
            ],
            "notes": "LPU HRDC conducts dozens of programmes annually. Nexus aims to provide a centralized hub for managing attendees, materials, grades, attendance, certificates, and corporate clients."
        },
        # Slide 3: Problem Statement
        {
            "layout": 1,
            "title": "Problem Statement & Existing Challenges",
            "bullets": [
                "Paper-based attendance is slow, prone to proxy inputs, and lacks geographical verification.",
                "Drafting quizzes, grading projects, and compiling certificates manually consumes extensive administrative time.",
                "Syllabus files and lecture documents exist as scattered files, making knowledge retrieval difficult.",
                "Tracking corporate revenue, contracts, and clients invoices is managed in disconnected spreadsheets."
            ],
            "notes": "Administrators spend over 15 hours per training cycle on manual documentation, attendance verification, scoring, and certificate compilation."
        },
        # Slide 4: Tech Stack
        {
            "layout": 1,
            "title": "Enterprise-Grade Technology Stack",
            "bullets": [
                "Frontend: Next.js 15 (App Router), React 19, TypeScript, TailwindCSS, Framer Motion.",
                "Backend: FastAPI (Python 3.12 ASGI), SQLAlchemy ORM core database logic.",
                "Storage & Auth: Supabase PostgreSQL database, Object Storage buckets, and JWT authentication.",
                "AI Reasoning & Indexing: Groq Cloud API LLMs, LangGraph multi-agent orchestration, and pgvector HNSW database indexes."
            ],
            "notes": "Our technology stack ensures security, speed, and standard compliance. The frontend runs React 19, and the backend leverages Python and pgvector."
        },
        # Slide 5: System Architecture
        {
            "layout": 1,
            "title": "System Architecture Overview",
            "bullets": [
                "Decoupled Layout: Next.js frontend deployed to Vercel, FastAPI backend deployed to Render.",
                "Database Connection Pooler: Supabase pooler over port 6543 handles high concurrent queries.",
                "Asynchronous Pipeline: Large documents parsing and pgvector RAG indexing run in background threads.",
                "PWA Standalone: Installable directly from the browser with cached offline pages."
            ],
            "notes": "The architecture is built to be resilient and cloud-native, decoupling compute and storage services."
        },
        # Slide 6: Database Schema & Models
        {
            "layout": 1,
            "title": "PostgreSQL Relational DB Design",
            "bullets": [
                "users & profiles: Synchronized roles mapping (Admin, Staff, Trainer, Participant).",
                "programmes & sessions: Relational training structures and dynamic timetables.",
                "attendance: Logs location coordinates, timestamps, and override justifications.",
                "corporate_contracts: Tracks corporate consulting client invoices and billings."
            ],
            "notes": "The schema supports complex cascades. For safety, the SQLAlchemy setup automatically falls back to local SQLite if remote PostgreSQL is unreachable."
        },
        # Slide 7: LangGraph Multi-Agent reasoning
        {
            "layout": 1,
            "title": "LangGraph Multi-Agent reasoning Engine",
            "bullets": [
                "Intent Classification: Detects if the user query is about attendance, programs, docs, or analytics.",
                "Routing Node: Dynamically dispatches task to designated agent.",
                "Specialized Agents: Attendance Agent, Programme Agent, RAG Document Agent, Analytics Agent.",
                "Validation Node: Cross-checks output facts against DB records to prevent hallucination.",
                "Response Synthesis: Groq LLM drafts final cited response."
            ],
            "notes": "By using LangGraph, we move away from simple chatbot completion towards specialized reasoning agents, ensuring higher accuracy and citation validity."
        },
        # Slide 8: Document RAG & pgvector Indexing
        {
            "layout": 1,
            "title": "Document RAG & pgvector Indexing",
            "bullets": [
                "Automatic Parsing: PDF, DOCX, and PPT files uploaded are automatically parsed using PDFParser.",
                "Ingestion & Chunking: Text is split into 600-word blocks with a 150-word overlap.",
                "Embedding: Chunks are encoded into 1536-dimensional vectors.",
                "Similarity Query: Uses PostgreSQL cosine distance operators supported by HNSW indexes."
            ],
            "notes": "The RAG pipeline provides contextual answering. The HNSW index ensures search response times under 50 milliseconds."
        },
        # Slide 9: Classroom Attendance Verification
        {
            "layout": 1,
            "title": "Geofenced QR Code Attendance",
            "bullets": [
                "Dynamic Time-Windows: Attendance check-in is restricted to configurable timing windows.",
                "QR Token Checking: QR hashes change dynamically to prevent student code sharing.",
                "GPS Geofencing: Calculates user distance against classroom coordinates (LPU block center).",
                "Manual Override: HRDC staff can manually force logs, writing notes."
            ],
            "notes": "This geofenced QR check-in stops classroom proxies, locking logs to actual classroom boundaries."
        },
        # Slide 10: Assessments & Auto Evaluation
        {
            "layout": 1,
            "title": "Assessments Module & MCQ grading",
            "bullets": [
                "Multi-format Tests: Supports MCQ, Subjective assignments, and Code submissions.",
                "MCQ Auto Evaluation: Student MCQ sheets are graded instantly, saving trainer hours.",
                "Project Submittals: Logs Title, Abstract, GitHub URL, and presentation slideshow links.",
                "Gamified Leaderboard: Tracks class performance, displaying top participants."
            ],
            "notes": "Auto-grading saves faculty extensive evaluation time. The leaderboard fosters a healthy learning dynamic."
        },
        # Slide 11: Feedback & ROI Impact Assessment
        {
            "layout": 1,
            "title": "Feedback Index & Pre-Post surveys",
            "bullets": [
                "Ratings System: Participants rate trainer, content, venue, and facilities (1 to 5 scale).",
                "Competency Surveys: Tracks knowledge before and after programs to calculate gain percentages.",
                "ROI index: Automatically computes organizational performance metrics.",
                "Improvement Recommendations: Generates feedback trends summaries."
            ],
            "notes": "Nexus evaluates training return-on-investment (ROI) by assessing pre-post test score differences."
        },
        # Slide 12: Digital Certificates Registry
        {
            "layout": 1,
            "title": "Auto-Generated Digital Certificates",
            "bullets": [
                "ReportLab PDF Compilation: Dynamically compiles certificates with participant name and date.",
                "QR Code Verification: Includes QR verification hash linking to public checker page.",
                "Digital Signature: Signs certificate PDFs for authenticity.",
                "Verification Search Page: Allows employers to verify certificate validity."
            ],
            "notes": "Certificates are issued automatically upon meeting attendance and assessment requirements."
        },
        # Slide 13: Corporate Training CRM
        {
            "layout": 1,
            "title": "Corporate CRM Contract & Billing",
            "bullets": [
                "Clients registry: Catalog corporate contacts, phone numbers and companies.",
                "Billing Invoices: Logs invoice details, contract URL and billing totals.",
                "Payment Tracking: Manages invoice status tags (Paid, Pending, Cancelled).",
                "Financial Dashboard: Displays revenue rollups on the homepage."
            ],
            "notes": "Nexus provides HRDC with a CRM module to log consulting contracts and client invoices."
        },
        # Slide 14: Mobile PWA stand-alone features
        {
            "layout": 1,
            "title": "Mobile Installable PWA Experience",
            "bullets": [
                "No App Store Required: Users install the app directly from browser options.",
                "Stand-alone display: App opens in standalone window, hiding browser navigation.",
                "Offline Caching: sw.js service worker caches essential pages and styles.",
                "Responsive Layouts: Mobile, Tablet, and Desktop responsive CSS design tokens."
            ],
            "notes": "PWA compatibility makes classroom check-ins faster. Users install it with one click."
        },
        # Slide 15: Security & Best Practices
        {
            "layout": 1,
            "title": "Security & OWASP Compliance",
            "bullets": [
                "Row Level Security (RLS): Supabase table access checks protect student/financial files.",
                "JWT Token validation: Endpoints verify authentication tokens before querying database.",
                "Input Validation: Pydantic schemas and Zod constraints sanitize data entry.",
                "Docker isolation: Containers prevent local file-system vulnerabilities."
            ],
            "notes": "Security is enforced at all levels. RLS ensures trainers only see their courses, and participants only see their profiles."
        },
        # Slide 16: Deployment Strategy
        {
            "layout": 1,
            "title": "Cloud-Native Deployment Pipeline",
            "bullets": [
                "Vercel (Frontend): Continuous integration build linked to GitHub repo branches.",
                "Render (Backend): Containerized FastAPI Docker service auto-building on git push.",
                "Supabase Cloud: Hosts Postgres, Auth, pgvector, and Object storage.",
                "Alembic DB migrations: Triggers migrations automatically during start commands."
            ],
            "notes": "Our deployment pipeline is fully automated. Commits to the repository automatically redeploy the stack."
        },
        # Slide 17: Platform Benefits
        {
            "layout": 1,
            "title": "Institutional Benefits & Key Results",
            "bullets": [
                "Time Saving: Reduces administrative documentation hours by 85% per course cycle.",
                "Accuracy: Geofencing eliminates attendance proxies and certificate fraud.",
                "Knowledge Retrieval: LangGraph/pgvector lets staff query training details instantly.",
                "Agility: Replaces five legacy systems with a single consolidated web workspace."
            ],
            "notes": "Nexus consolidates attendance, evaluations, certificates, corporate CRM, and AI support."
        },
        # Slide 18: Summary & Future Scope
        {
            "layout": 1,
            "title": "Future Scope & Platform Roadmap",
            "bullets": [
                "Biometric Attendance Integration: Connect face/fingerprint scanners directly via IoT APIs.",
                "AI Proctoring: Enable webcam analysis during subjective assessment submissions.",
                "External Vendor API integration: Expose training courses to corporate job boards.",
                "Automated Email Reminders: Trigger reminders via Sengrid/SMTP integration."
            ],
            "notes": "Future iterations will include proctoring, payment portal gateways, and biometric device bindings."
        }
    ]
    
    for slide_info in slides_data:
        layout_idx = slide_info["layout"]
        slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
        
        # Title
        if "title" in slide_info:
            title_box = slide.shapes.title
            title_box.text = slide_info["title"]
            title_box.text_frame.paragraphs[0].font.color.rgb = ORANGE
            title_box.text_frame.paragraphs[0].font.bold = True
            
        # Subtitle
        if layout_idx == 0 and "subtitle" in slide_info:
            subtitle_box = slide.placeholders[1]
            subtitle_box.text = slide_info["subtitle"]
            subtitle_box.text_frame.paragraphs[0].font.color.rgb = CHARCOAL
            
        # Bullets
        if "bullets" in slide_info and layout_idx == 1:
            body_box = slide.placeholders[1]
            tf = body_box.text_frame
            tf.clear()
            for idx, bullet in enumerate(slide_info["bullets"]):
                p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
                p.text = bullet
                p.level = 0
                p.font.size = Pt(14)
                p.font.color.rgb = CHARCOAL
                
        # Speaker notes
        if "notes" in slide_info:
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = slide_info["notes"]
            
    # Save PPTX
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root_dir, "LPU_FDP_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    create_presentation()
