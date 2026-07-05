# LPU Academic Copilot — Testing & Demo Guide

This guide covers testing instructions, a 3-minute presentation script, and sample generated JSON payloads.

---

## 1. Complete Testing Guide

### 1.1. Backend Unit Testing
We use `pytest` for backend testing. Install development packages:
```bash
cd backend
pip install pytest httpx
```

Create a test file `backend/tests/test_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.pdf_parser import PDFParser

client = TestClient(app)

def test_root_and_cors():
    # Test fallback settings route without auth headers returns 401
    res = client.get("/api/settings")
    assert res.status_code == 401

def test_pdf_cleaner():
    raw_text = "  Unit 1:   Basics  \n\n\n  Transformer architectures "
    cleaned = PDFParser.clean_text(raw_text)
    assert cleaned == "Unit 1: Basics\nTransformer architectures"

def test_mock_bypass_profile():
    # If Supabase is disabled, mock token validation bypasses 401
    headers = {"Authorization": "Bearer dev-token-mock"}
    res = client.get("/api/settings", headers=headers)
    assert res.status_code == 200
    assert res.json()["llm_provider"] == "gemini"
```
Run tests with:
```bash
pytest
```

---

## 2. 3-Minute Live Demo Script

| Time | Slide/Screen | Action & Talking Points |
| :--- | :--- | :--- |
| **0:00 - 0:30** | Landing Page | "Welcome to LPU Academic Copilot, a multi-agent AI system designed to automate faculty workflows. Instead of writing syllabus documents manually, we upload a syllabus PDF and let ten specialized agents coordinate to generate a complete course plan." |
| **0:30 - 1:00** | Login & Settings | "Let's log in. If Supabase is not configured, we can click 'Instant FDP Demo Access' to enter a demo session. In the settings page, we can configure our primary LLM settings (Gemini or Groq) and set model parameters." |
| **1:00 - 2:00** | Syllabus Upload | "Now, let's upload a syllabus PDF. We select our file and click 'Trigger Multi-Agent Workflow'. FastAPI runs the agents in the background, updating the dashboard logs. We can see the progress of each agent in real time." |
| **2:00 - 2:45** | Report Tab Panel | "Once complete, we can review the generated materials: the 15-Week Lesson Plan, 3 Assignments, 20 MCQs with answers, Exam Papers, Bloom's Taxonomy Mappings, and CO Weightages." |
| **2:45 - 3:00** | PDF Download | "Finally, we can click 'Download Publication PDF' to download the compiled ReportLab PDF report, complete with headers, footers, page numbers, and custom tables." |

---

## 3. Sample Generated Outputs (JSON)

### 3.1. Planning Agent Output
```json
{
  "course_name": "Modern AI Systems & Agentic Orchestration",
  "course_code": "CSE402",
  "units": [
    {
      "unit_number": 1,
      "title": "Basics of LLMs & API Drivers",
      "topics": ["Transformers", "System instructions", "Gemini/Groq APIs"]
    }
  ],
  "course_outcomes": [
    {
      "co_code": "CO1",
      "description": "Understand foundations of Large Language Models and prompting paradigms."
    }
  ]
}
```

### 3.2. Quiz Agent Output (MCQ Bank)
```json
{
  "quiz_title": "Assessment MCQ Quiz - CSE402",
  "questions": [
    {
      "question_number": 1,
      "unit_number": 1,
      "question_text": "What does temperature configuration adjust in LLMs?",
      "options": {
        "A": "Model inference speed",
        "B": "Context window limits",
        "C": "Output randomness",
        "D": "Token embedding size"
      },
      "correct_option": "C",
      "explanation": "Higher temperatures increase randomness; lower values yield deterministic results."
    }
  ]
}
```

### 3.3. Academic Quality Report Output
```json
{
  "overall_score": 88.5,
  "dimensions": {
    "alignment": 92.0,
    "coverage": 89.0,
    "clarity_and_rigor": 85.0,
    "pedagogy": 88.0
  },
  "suggestions": [
    {
      "dimension": "coverage",
      "issue": "Week 14 has very little coding exercises.",
      "recommendation": "Add a Git repository template link for hands-on practice."
    }
  ],
  "conclusion": "The generated course package meets academic quality compliance."
}
```
