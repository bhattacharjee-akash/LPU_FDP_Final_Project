# Multi-Agent Workflow Documentation
> **LPU Academic Copilot — Agent Nodes, Responsibilities, and Prompt Architecture**

The backend orchestrates a 10-Agent network to parse, generate, align, and grade academic course packages. This document outlines the role, behavior, and configurations of each agent node.

---

## 1. BaseAgent Class Design
All agents inherit from [`BaseAgent`](file:///C:/Users/AKASH%20PC/lpu-academic-copilot/backend/app/agents/base_agent.py). The base agent provides shared utilities:
* **Prompt Loading**: `read_prompt_template(filename)` loads the text prompt from `/backend/app/prompts/`.
* **Inference Routing**: Calls Google Gemini or Groq Cloud depending on the faculty configuration.
* **JSON Cleaning**: `clean_json_response(text)` cleans markdown code block wrappers (like ` ```json `) to prevent parsing crashes.

---

## 2. Agent Node Specifications

### **1. PlanningAgent**
* **Responsibility**: Parses raw syllabus text, identifies course name/code, and extracts units, topics, and course outcomes (COs).
* **Prompt Strategy**: Structured to identify divisions in the syllabus and output a clean JSON map of Course Outcomes and units.

### **2. LessonPlanAgent**
* **Responsibility**: Builds a 15-week weekly delivery plan.
* **Outputs**: Lecture numbers, topics, specific learning objectives, teaching pedagogy (e.g. Flipped Classroom, Case Study), and reference book pages.

### **3. AssignmentAgent**
* **Responsibility**: Designs 3 course assignments.
* **Outputs**: Assignment 1 (basic modules, recall), Assignment 2 (mid-level, application), and Assignment 3 (complex, design-oriented).

### **4. QuizAgent**
* **Responsibility**: Generates a bank of 20 multiple-choice questions (MCQs).
* **Outputs**: Questions, 4 distinct options, correct key, and a detailed academic explanation.

### **5. QuestionPaperAgent**
* **Responsibility**: Drafts the Mid-Semester (50 marks) and End-Semester (100 marks) exam papers.
* **Outputs**: Structured question parts, marks allocations, and instructions aligned to Lovely Professional University exam patterns.

### **6. BloomAgent**
* **Responsibility**: Audits the syllabus and assignments, and maps each element to a cognitive level in Bloom's Taxonomy (e.g., L1: Remember, L3: Apply, L6: Create).

### **7. COMappingAgent**
* **Responsibility**: Correlates the generated exam questions to the Course Outcomes (COs) extracted by the Planning Agent.

### **8. ReviewerAgent**
* **Responsibility**: Double-checks all generated modules for typos, spelling mistakes, or logical inconsistencies (e.g., ensuring assignments do not test units not covered in the lesson plan).

### **9. AcademicQualityAgent**
* **Responsibility**: Performs a checklist audit of the completed pack. It awards a final compliance score (0-100) and drafts concrete improvement recommendations.

### **10. PDFGenerator Node**
* **Responsibility**: Takes the aggregated JSON from all preceding 9 agents, compiles it, and uses **ReportLab** to write a publication-ready PDF Course Pack.
* **Outputs**: Styled PDF binary stream containing page numbers, cover pages, tables, and borders.
