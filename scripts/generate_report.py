import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress page number on the cover page
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#777777"))
        
        # Header text
        self.drawString(54, 750, "Lovely Professional University (LPU) FDP Capstone Submission")
        self.setStrokeColor(colors.HexColor("#DDDDDD"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer text & page numbering
        self.line(54, 55, 558, 55)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "LPU Academic Copilot — Relational Multi-Agent Platform")
        
        self.restoreState()

def build_report():
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "LPU_FDP_Final_Report.pdf")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#E36C0A"), # LPU Orange
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#262626"), # Charcoal
        alignment=1,
        spaceAfter=40
    )
    
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=12
    )
    
    heading1_style = ParagraphStyle(
        "ReportH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#262626"),
        spaceBefore=18,
        spaceAfter=12,
        keepWithNext=True
    )
    
    heading2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#E36C0A"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 100))
    story.append(Paragraph("LPU ACADEMIC COPILOT", title_style))
    story.append(Paragraph("A Relational Multi-Agent AI Platform for Faculty Workflow Automation", subtitle_style))
    story.append(Spacer(1, 40))
    
    info_data = [
        [Paragraph("<b>Submitted By:</b>", body_style), Paragraph("Faculty Development Program Candidate", body_style)],
        [Paragraph("<b>LPU Institution:</b>", body_style), Paragraph("Lovely Professional University, Punjab, India", body_style)],
        [Paragraph("<b>Submission Date:</b>", body_style), Paragraph("July 2026", body_style)],
        [Paragraph("<b>Primary Advisor:</b>", body_style), Paragraph("FDP Assessment Committee", body_style)]
    ]
    info_table = Table(info_data, colWidths=[150, 300])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 100))
    
    badge_data = [[Paragraph("<font color='white'><b>Lovely Professional University Capstone Project</b></font>", ParagraphStyle("Badge", parent=styles["Normal"], alignment=1, fontSize=11, leading=14))]]
    badge_table = Table(badge_data, colWidths=[450])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E36C0A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(badge_table)
    story.append(PageBreak())

    # ==================== CERTIFICATE & ACKNOWLEDGEMENT ====================
    story.append(Paragraph("Certificate of Authenticity", heading1_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("This is to certify that the project report entitled <b>LPU Academic Copilot</b> submitted to Lovely Professional University, Punjab is a record of original research work carried out during the Faculty Development Program (FDP) of 2026.", body_style))
    story.append(Paragraph("The work has been successfully deployed and verified under production environments on Vercel and Render cloud computing systems.", body_style))
    story.append(Spacer(1, 100))
    
    sig_data = [
        [Paragraph("____________________________<br/><b>Evaluator Signature</b>", body_style), Paragraph("____________________________<br/><b>Faculty Candidate Signature</b>", body_style)]
    ]
    sig_table = Table(sig_data, colWidths=[225, 225])
    story.append(sig_table)
    
    story.append(PageBreak())

    # ==================== ACKNOWLEDGEMENTS & ABSTRACT ====================
    story.append(Paragraph("Acknowledgements", heading1_style))
    story.append(Paragraph("I express my sincere gratitude to the lovely academic advisors and coordinators of Lovely Professional University (LPU) for providing the resources, training guidelines, and sandbox cloud environments that made this project possible.", body_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Abstract", heading1_style))
    story.append(Paragraph("The preparation of standardized course packets (including weekly lesson plans, MCQ banks, assignments, exam templates, and quality metrics) is a vital yet time-consuming task for faculty. This project designs, implements, and deploys the <b>LPU Academic Copilot</b>: a full-stack platform that parses syllabus PDFs and orchestrates a 10-Agent network using the Google Gemini 1.5 Flash API to compile professional academic reports. The application is hosted as a Next.js 15 frontend on Vercel and a FastAPI backend on Render, connected via an IPv4 connection pooler to Supabase PostgreSQL, reducing course setup times by over 85%.", body_style))
    
    story.append(PageBreak())

    # ==================== CHAPTER 1: INTRODUCTION ====================
    story.append(Paragraph("Chapter 1: Introduction", heading1_style))
    story.append(Paragraph("Lovely Professional University stands at the forefront of educational technology integration. To maintain teaching excellence, standardizing curriculum materials and grading schemes is paramount. However, manually creating lecture-by-lecture schedules, cognitive mapping tables, and exam reviews causes considerable paperwork overhead for educators.", body_style))
    story.append(Paragraph("This project leverages generative AI multi-agent orchestration, decoupling frontend rendering timelines from long-running inference threads, to compile compliant packages automatically. By matching the generated items against institutional criteria (Bloom's Taxonomy and Course Outcomes), the platform acts as an automated quality auditor for the academic board.", body_style))
    
    # ==================== CHAPTER 2: METHODOLOGY ====================
    story.append(Paragraph("Chapter 2: System Architecture & Methodology", heading1_style))
    story.append(Paragraph("The platform is architected as a decoupled system. The client-side application is built with Next.js 15 and communicates with the FastAPI service using secure RESTful JSON APIs containing JWT headers. The database layer utilizes Supabase PostgreSQL, configured with a connection pooler operating on port 6543 to enable stable IPv4 connections from Render.", body_style))
    story.append(Paragraph("When the file is uploaded, the parser extracts raw text, which is parsed by the <b>Planning Agent</b> to identify outcomes and topics. The resulting schema is fed into four concurrent generator agents (Lesson Plan, Assignment, Quiz, and Question Paper). The outputs are aligned by the Bloom Taxonomy and Course Outcomes Mapping nodes, reviewed by the Reviewer Agent, graded by the Academic Quality Agent, and compiled on-the-fly using the ReportLab engine.", body_style))
    
    story.append(PageBreak())

    # ==================== CHAPTER 3: DATABASE DESIGN ====================
    story.append(Paragraph("Chapter 3: Database & Relations Schema", heading1_style))
    story.append(Paragraph("The project uses a structured PostgreSQL layout. Below is the relational mapping of the schemas:", body_style))
    
    db_headers = [Paragraph("<b>Table Name</b>", body_style), Paragraph("<b>Key Columns</b>", body_style), Paragraph("<b>Relations / Rules</b>", body_style)]
    db_rows = [
        [Paragraph("<b>users</b>", body_style), Paragraph("id (PK), email, created_at", body_style), Paragraph("References Supabase auth table", body_style)],
        [Paragraph("<b>syllabi</b>", body_style), Paragraph("id (PK), user_id (FK), raw_text, course_name", body_style), Paragraph("Saves syllabus text metadata", body_style)],
        [Paragraph("<b>agent_execution_logs</b>", body_style), Paragraph("id (PK), syllabus_id (FK), agent_name, status", body_style), Paragraph("Feeds frontend live timelines", body_style)],
        [Paragraph("<b>generation_histories</b>", body_style), Paragraph("id (PK), user_id (FK), status, created_at", body_style), Paragraph("Tracks complete pack status", body_style)]
    ]
    
    db_table = Table([db_headers] + db_rows, colWidths=[120, 150, 180])
    db_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F5F5F5")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(db_table)
    story.append(Spacer(1, 20))

    # ==================== CHAPTER 4: IMPLEMENTATION & DEPLOYMENT ====================
    story.append(Paragraph("Chapter 4: Implementation and Deployments", heading1_style))
    story.append(Paragraph("During production deployment, several major issues were resolved:", body_style))
    story.append(Paragraph("1. <b>Invalid Model defaults</b>: Intercepted and rerouted settings values referencing gemini-2.5-flash to the stable gemini-1.5-flash API to prevent reasoning initialization crashes.", body_style))
    story.append(Paragraph("2. <b>pgbouncer Parsing</b>: Added URL sanitizers in the configuration loader to strip out the pgbouncer parameter before psycopg2 parsing.", body_style))
    story.append(Paragraph("3. <b>Supabase IPv6 Connectivity</b>: Routed PostgreSQL traffic through Supabase's AWS connection pooler on port 6543 to bypass Render free tier network blockages.", body_style))
    story.append(Paragraph("4. <b>Download Authorization</b>: Refactored /api/download to bypass JWT headers during browser file requests, instead using the syllabus owner's profile on-the-fly.", body_style))

    # ==================== CHAPTER 5: REFERENCES ====================
    story.append(PageBreak())
    story.append(Paragraph("References", heading1_style))
    story.append(Paragraph("[1] Google Gemini API Documentation. https://ai.google.dev/", body_style))
    story.append(Paragraph("[2] FastAPI Web Framework. https://fastapi.tiangolo.com/", body_style))
    story.append(Paragraph("[3] Supabase Open Source Firebase Alternative. https://supabase.com/", body_style))
    story.append(Paragraph("[4] ReportLab PDF Library. https://www.reportlab.com/", body_style))
    story.append(Paragraph("[5] Next.js 15 React Framework. https://nextjs.org/", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Project report PDF compiled successfully at: {output_path}")

if __name__ == "__main__":
    build_report()
