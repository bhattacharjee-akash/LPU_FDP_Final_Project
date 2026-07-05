# LPU Academic Copilot — Presentation Slides
> **FDP on Modern AI and Agentic Systems: Multi-Agent Orchestration in Higher Education**

---

## Slide 1: Title Slide
### **LPU Academic Copilot**
*A Multi-Agent AI Platform for Faculty Workflow Automation*
- **Objective:** Streamline syllabus parsing, week-by-week lesson design, progressive assignment formulation, MCQ compilations, Bloom's Taxonomy alignment, and exam drafting.
- **Audience:** Lovely Professional University Faculty & FDP Attendees.
- **Presenter:** Faculty Development Coordinator.

---

## Slide 2: The Problem
### **Manual Syllabus Management & Assessment Drafting**
- **Time Consuming:** Faculty spend hours compiling weekly delivery plans, drafting progressive assignments, and writing balanced exams.
- **Outcome Mapping Complexity:** Aligning exam questions to designated Course Outcomes (COs) requires complex mappings.
- **Bloom's Taxonomy Audit:** Manually balancing cognitive levels (Remembering, Applying, Evaluating) across assessments is error-prone.

---

## Slide 3: The Solution
### **Collaborative AI Agent Orchestrator**
- **Automated Processing:** Upload your syllabus PDF and get a complete academic package in under 3 minutes.
- **Collaborative Intelligence:** Uses a network of **ten autonomous agents** working sequentially, instead of a single chatbot.
- **Quality Auditing:** Integrated checker agents review materials and calculate an academic compliance rating (0-100).

---

## Slide 4: Multi-Agent Architecture
### **Why Multi-Agent Systems are Superior**
- **Single Chatbot Limitation:** Hard to enforce multi-step guidelines, maintain consistency, and perform quality checks.
- **Specialized Roles:** Each agent is a dedicated Python class with specialized system instructions.
- **Orchestration Workflow:**
  1. *Planning Agent* extracts core elements.
  2. *Creator Agents* build components.
  3. *Reviewer Agent* validates drafts.
  4. *Quality Agent* scores compliance.

---

## Slide 5: The 10-Agent Pipeline
### **Meet the Agents**
1. **PlanningAgent:** Extract metadata, units, and outcomes (COs).
2. **LessonPlanAgent:** Generates weekly pedagogical plans (Weeks 1-15).
3. **AssignmentAgent:** Drafts 3 sets of coursework questions.
4. **QuizAgent:** Compiles 20 detailed MCQs with explanations.
5. **QuestionPaperAgent:** Drafts Mid Semester & End Semester exams.
6. **BloomAgent:** Aligns curriculum to K1-K6 cognitive levels.
7. **COMappingAgent:** Maps exam questions to Course Outcomes.
8. **ReviewerAgent:** Checks for errors and consistency.
9. **AcademicQualityAgent:** Calculates compliance score & recommendations.
10. **PDF Generator:** Compiles and uploads a publication-ready report.

---

## Slide 6: Tech Stack Summary
### **Enterprise-Ready Infrastructure**
- **Frontend App:**
  - Next.js 15 & React 19 (Modern App Router)
  - Tailwind CSS & Glassmorphism design tokens
  - Framer Motion micro-animations
- **Backend API:**
  - FastAPI (Fast Python ASGI framework)
  - SQLAlchemy ORM with Alembic PostgreSQL migrations
  - ReportLab engine for PDF layout compiling
- **LLM Engine:** Google Gemini 2.5 Flash & Groq Cloud API
- **Cloud Database:** Supabase PostgreSQL with RLS and Storage Bucket support.

---

## Slide 7: Demonstration Mode
### **Seamless Testing & Evaluation**
- **Zero Configuration Setup:** You can start local evaluations without active database connections or API keys.
- **Mock Bypass Mode:** Click "Instant FDP Demo Access" on the login page to enter a simulated session.
- **Intelligent Fallbacks:** Agents fall back to predefined mock curriculum packages if LLM connections are offline, preventing connection errors.

---

## Slide 8: Real-Time Stream Monitoring
### **Timeline & Logging Stream**
- **Polling Loop:** The Next.js frontend queries the API status endpoint every 2 seconds.
- **Live Output Stream:** Displays a scrolling terminal log that outputs agent statuses (STARTED, COMPLETED) in real time.
- **Timeline Connector:** A visual node connector shows progress as agents complete their tasks.

---

## Slide 9: Audit and Quality Review
### **Bloom's & Course Outcome Auditing**
- **Rigor Validation:** Shows a breakdown of question weights mapped to Course Outcomes.
- **Cognitive Level Alignment:** Unit mappings classify topics into Bloom's taxonomy categories.
- **Quality Scorecard:** Provides ratings for alignment, coverage, rigor, and pedagogy, along with a suggestions checklist.

---

## Slide 10: Conclusion & Next Steps
### **The Future of Academic Orchestrations**
- **Immediate Efficiency:** Reclaims an estimated 8.5 hours per course setup.
- **Consistent Standards:** Ensures all department assessments meet taxonomy guidelines.
- **Future Enhancements:**
  - Import direct LMS integrations (Moodle, Blackboard).
  - Add multi-language translation support.
  - Multi-faculty review dashboards.
