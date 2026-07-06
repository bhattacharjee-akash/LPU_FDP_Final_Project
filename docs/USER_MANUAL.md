# Faculty User Manual
> **LPU Academic Copilot — Platform User Guide and Feature Walkthrough**

Welcome to the LPU Academic Copilot user manual. This guide is written for university faculty and coordinators to help them generate comprehensive, high-quality, and compliant academic course packs.

---

## 1. Landing Page & Authentication
When you visit the application URL (**[https://frontend-five-gules-38.vercel.app](https://frontend-five-gules-38.vercel.app)**):
1. Click **"Get Started"** or **"Faculty Login"**.
2. **Registration / Login**: Enter your Lovely Professional University email address and set a secure password.
3. Click **Login** (or click Register if using the app for the first time). Once authenticated, you will be redirected to the **Faculty Dashboard**.

---

## 2. The Faculty Dashboard Overview
The dashboard displays four core performance cards:
- **Total Syllabi Processed**: The count of syllabus files you have successfully parsed.
- **Average Quality Score**: The average compliance score graded by the **Academic Quality Agent** across your generated packages (LPU target: **>80%**).
- **Hours Saved (Est.)**: Estimated administrative hours saved (calculated based on an average of 8.5 hours per manual planning cycle).
- **Assessments Made**: Total count of Mid-Sem/End-Sem papers, assignments, and MCQs generated.

---

## 3. Creating a New Course Pack (Step-by-Step)
1. In the sidebar, click on **"Upload Syllabus"**.
2. Drag and drop your syllabus PDF file (or click the dashed area to select the file).
   * *Note: The syllabus should contain course codes, course outcomes (COs), unit topics, and reference textbooks.*
3. Click the orange **"Trigger Multi-Agent Workflow"** button.
4. **Execution Tracking**:
   * The screen will transition to the **Orchestration Flow Timeline**.
   * You will see all 10 agents transition from `PENDING` ➔ `PROCESSING` ➔ `COMPLETED` sequentially.
   * The **Live Agent Output Stream** window on the right will display text snippets of exactly what each agent is outputting (e.g. weekly lecture items, MCQ keys, compliance scores).
5. **Download Report**: Once the timeline shows the green `COMPLETED` status for all agents, click **"Download Report"** to save the formatted Course Pack PDF.

---

## 4. Dashboard Settings & Calibration
You can calibrate the reasoning engines and adjust faculty metadata:
1. In the sidebar, click on **"Settings"**.
2. **Faculty Profile**: Update your Name and Department to customize the footer signature of your generated PDF packs.
3. **AI Orchestrator Engine**:
   - Choose between **Google Gemini (Recommended)** and **Groq API** as the primary provider.
   - Select the model name (e.g. `gemini-1.5-flash` or `gemini-1.5-pro` for highly logical generations).
   - Adjust the **Temperature** slider (lower temperature makes the outputs more deterministic and structured; higher temperature makes them more creative).
4. Click **"Save Settings"**.

---

## 5. Reviewing Generated History
- Click **"Generation History"** in the sidebar to review all past uploads.
- You will see a list of syllabus entries, dates, quality scores, and download buttons.
- Click **"View Details"** to inspect a specific syllabus's parsed modules directly in the browser.
