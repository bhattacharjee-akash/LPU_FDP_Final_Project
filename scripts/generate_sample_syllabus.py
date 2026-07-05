import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "sample_syllabus.pdf")
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'SyllabusTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A252C"),
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SyllabusH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#E77817"),
        spaceBefore=10,
        spaceAfter=5
    )
    
    body_style = ParagraphStyle(
        'SyllabusBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6
    )
    
    story = []
    
    # Header
    story.append(Paragraph("LOVELY PROFESSIONAL UNIVERSITY", title_style))
    story.append(Paragraph("<b>Course Code:</b> CSE402 &nbsp;&nbsp;&nbsp;&nbsp; <b>Course Title:</b> Modern AI Systems & Agentic Orchestration", body_style))
    story.append(Paragraph("<b>Credits:</b> 4 (L:3, T:0, P:2) &nbsp;&nbsp;&nbsp;&nbsp; <b>Department:</b> Computer Science & Engineering", body_style))
    story.append(Spacer(1, 10))
    
    # Course Outcomes
    story.append(Paragraph("Course Outcomes (COs)", h2_style))
    story.append(Paragraph("• <b>CO1:</b> Understand the foundations of Large Language Models and prompting paradigms.", body_style))
    story.append(Paragraph("• <b>CO2:</b> Apply single-agent design patterns (ReAct, Planning) to code execution tasks.", body_style))
    story.append(Paragraph("• <b>CO3:</b> Build multi-agent communication networks for collaborative software design.", body_style))
    story.append(Paragraph("• <b>CO4:</b> Set up CI/CD workflows and dockerized testing environments for agent systems.", body_style))
    story.append(Paragraph("• <b>CO5:</b> Audit applications using Bloom's Taxonomy cognitive standards and monitoring tools.", body_style))
    story.append(Spacer(1, 10))
    
    # Units Table
    story.append(Paragraph("Syllabus Units Breakdown", h2_style))
    
    headers = [
        Paragraph("<b>Unit</b>", body_style),
        Paragraph("<b>Title & Description</b>", body_style),
        Paragraph("<b>Topics Covered</b>", body_style)
    ]
    data = [headers]
    
    units = [
        ("Unit 1", "Basics of LLMs & API Drivers", "Transformers, tokenizations, system instructions, temperature, Gemini/Groq APIs."),
        ("Unit 2", "Prompt Engineering & RAG", "Few-shot templates, Chain of Thought, vector databases, Semantic Search, chunking."),
        ("Unit 3", "Autonomous Agent Loops", "ReAct loop architectures, tool binding parameters, execution loops, state variables."),
        ("Unit 4", "Multi-Agent Collaboration", "GroupChat orchestrators, AutoGen communication models, reviewer-critic patterns."),
        ("Unit 5", "CI/CD Deployment & Telemetry", "GitHub Actions workflows, Docker containers, Prometheus dashboards, Sentry tracking.")
    ]
    
    for u, t, c in units:
        data.append([
            Paragraph(u, body_style),
            Paragraph(t, body_style),
            Paragraph(c, body_style)
        ])
        
    table = Table(data, colWidths=[60, 160, 284])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F2F2F2")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D0D0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))
    
    # Textbooks
    story.append(Paragraph("Suggested Textbooks & Readings", h2_style))
    story.append(Paragraph("1. <i>Introduction to Agentic Software Engineering</i>, LPU Academic Press, 2026.", body_style))
    story.append(Paragraph("2. <i>Large Language Models in Action</i>, Manning Publications, 2025.", body_style))
    
    doc.build(story)
    print(f"Sample syllabus PDF compiled at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
