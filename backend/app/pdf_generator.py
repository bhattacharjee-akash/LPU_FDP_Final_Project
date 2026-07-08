import io
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

# Theme Palette (LPU-inspired Orange and Charcoal)
PRIMARY_COLOR = colors.HexColor("#E77817")  # Orange
SECONDARY_COLOR = colors.HexColor("#1A252C")  # Charcoal
TEXT_COLOR = colors.HexColor("#333333")
LIGHT_BG = colors.HexColor("#F9F9F9")
BORDER_COLOR = colors.HexColor("#E0E0E0")

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count in the footer.
    """
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress headers/footers on the cover page
        if self._pageNumber == 1:
            self.restoreState()
            return
            
        # Draw Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(SECONDARY_COLOR)
        self.drawString(54, 750, "LPU ACADEMIC COPILOT — FACULTY AUTOMATION PLATFORM")
        self.setStrokeColor(PRIMARY_COLOR)
        self.setLineWidth(1)
        self.line(54, 742, 558, 742)
        
        # Draw Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 55, 558, 55)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#777777"))
        self.drawString(54, 42, "Confidential — For Internal Academic Review Only")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 42, page_str)
        self.restoreState()


class PDFGenerator:
    @staticmethod
    def generate_report(
        course_name: str,
        course_code: str,
        faculty_name: str,
        department: str,
        lesson_plan: dict,
        assignments: dict,
        quiz: dict,
        question_papers: dict,
        bloom_mapping: dict,
        co_mapping: dict,
        quality_report: dict
    ) -> bytes:
        """
        Creates a structured PDF report returned as bytes.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        
        # Custom Typography Styles
        title_style = ParagraphStyle(
            'CoverTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=28,
            leading=34,
            textColor=PRIMARY_COLOR,
            alignment=0,
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            'CoverSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=16,
            leading=22,
            textColor=SECONDARY_COLOR,
            alignment=0,
            spaceAfter=40
        )
        
        meta_style = ParagraphStyle(
            'CoverMeta',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=16,
            textColor=colors.HexColor("#555555")
        )
        
        h1_style = ParagraphStyle(
            'SectionH1',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=PRIMARY_COLOR,
            spaceBefore=15,
            spaceAfter=15,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=SECONDARY_COLOR,
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            'BodyTextCustom',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=TEXT_COLOR,
            spaceAfter=8
        )
        
        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.white
        )

        table_body_style = ParagraphStyle(
            'TableBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=TEXT_COLOR
        )

        story = []
        
        # ==========================================
        # 1. COVER PAGE
        # ==========================================
        story.append(Spacer(1, 100))
        story.append(Paragraph("LPU ACADEMIC COPILOT", title_style))
        story.append(Paragraph("Course Execution Plan & Assessment Suite", subtitle_style))
        
        # Decorative Colored Accent Bar
        d = Table([[""]], colWidths=[504], rowHeights=[4])
        d.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), PRIMARY_COLOR),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(d)
        story.append(Spacer(1, 40))
        
        # Meta Info Box
        meta_text = f"""
        <b>Course Name:</b> {course_name}<br/>
        <b>Course Code:</b> {course_code}<br/>
        <b>Faculty Coordinator:</b> {faculty_name}<br/>
        <b>Department:</b> {department}<br/>
        <b>Generated On:</b> {datetime.date.today().strftime('%B %d, %Y')}<br/>
        <b>Compliance Status:</b> Approved by Quality Agent ({quality_report.get('overall_score', 0)}/100)
        """
        story.append(Paragraph(meta_text, meta_style))
        
        story.append(Spacer(1, 180))
        story.append(Paragraph("Lovely Professional University (LPU) — Faculty Workflow Platform", meta_style))
        story.append(PageBreak())
        
        # ==========================================
        # 2. LESSON PLAN (15 WEEKS)
        # ==========================================
        story.append(Paragraph("1. Weekly Teaching Plan (15 Weeks)", h1_style))
        story.append(Paragraph(
            "Below is the complete 15-week academic calendar teaching plan containing weekly objectives, topics, pedagogical tools, and resources.",
            body_style
        ))
        
        # Setup Weeks Table
        lp_headers = [
            Paragraph("Week", table_header_style),
            Paragraph("Topics / Core Focus", table_header_style),
            Paragraph("Learning Objectives", table_header_style),
            Paragraph("Pedagogy & Materials", table_header_style)
        ]
        
        lp_data = [lp_headers]
        weeks_list = lesson_plan.get("weeks", [])
        for w in weeks_list:
            topics_txt = "<br/>".join([f"• {t}" for t in w.get("topics", [])])
            obj_txt = "<br/>".join([f"• {o}" for o in w.get("learning_objectives", [])])
            ped_res = f"<b>Pedagogy:</b> {w.get('pedagogy', '')}<br/><b>Resources:</b> {w.get('resources', '')}"
            
            lp_data.append([
                Paragraph(f"W{w.get('week_number', '')} (Unit {w.get('unit_number', '')})", table_body_style),
                Paragraph(topics_txt, table_body_style),
                Paragraph(obj_txt, table_body_style),
                Paragraph(ped_res, table_body_style)
            ])
            
        lp_table = Table(lp_data, colWidths=[60, 140, 164, 140])
        lp_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), SECONDARY_COLOR),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(lp_table)
        story.append(PageBreak())
        
        # ==========================================
        # 3. ASSIGNMENTS
        # ==========================================
        story.append(Paragraph("2. Course Assignments Suite", h1_style))
        story.append(Paragraph("Three structured assignments covering progressive phases of the syllabus.", body_style))
        
        for asn in assignments.get("assignments", []):
            story.append(Paragraph(f"Assignment {asn.get('assignment_number', '')}: {asn.get('title', '')}", h2_style))
            meta_info = f"<b>Marks:</b> {asn.get('total_marks', '')} | <b>Units Covered:</b> {', '.join(map(str, asn.get('units_covered', [])))}"
            story.append(Paragraph(meta_info, body_style))
            story.append(Paragraph(f"<b>Instructions:</b> {asn.get('instructions', '')}", body_style))
            
            # List of questions
            for q in asn.get("questions", []):
                q_text = f"<b>Q{q.get('question_number', '')}.</b> {q.get('question_text', '')} <i>({q.get('marks', '')} Marks)</i>"
                story.append(Paragraph(q_text, body_style))
                sol_guideline = f"<i>Evaluation criteria: {q.get('suggested_solution_guideline', '')}</i>"
                story.append(Paragraph(sol_guideline, table_body_style))
                story.append(Spacer(1, 4))
            story.append(Spacer(1, 10))
            
        story.append(PageBreak())
        
        # ==========================================
        # 4. MCQ QUIZ
        # ==========================================
        story.append(Paragraph("3. Multiple Choice Question Bank", h1_style))
        story.append(Paragraph("A comprehensive assessment bank containing 20 MCQs distributed over the curriculum units.", body_style))
        
        quiz_list = quiz.get("questions", [])
        for idx, q in enumerate(quiz_list):
            q_head = f"<b>Q{q.get('question_number', idx+1)}.</b> {q.get('question_text', '')} (Unit {q.get('unit_number', 1)})"
            story.append(Paragraph(q_head, body_style))
            
            opts = q.get("options", {})
            opt_str = f"A) {opts.get('A', '')} &nbsp;&nbsp;&nbsp;&nbsp; B) {opts.get('B', '')} &nbsp;&nbsp;&nbsp;&nbsp; C) {opts.get('C', '')} &nbsp;&nbsp;&nbsp;&nbsp; D) {opts.get('D', '')}"
            story.append(Paragraph(opt_str, body_style))
            
            answer_str = f"<b>Correct Answer:</b> {q.get('correct_option', '')} | <i>Explanation: {q.get('explanation', '')}</i>"
            story.append(Paragraph(answer_str, table_body_style))
            story.append(Spacer(1, 8))
            
        story.append(PageBreak())
        
        # ==========================================
        # 5. QUESTION PAPERS
        # ==========================================
        story.append(Paragraph("4. Semester Evaluation Papers", h1_style))
        
        # Mid Semester
        mid_sem = question_papers.get("mid_semester", {})
        story.append(Paragraph("Mid-Semester Examination Draft", h2_style))
        mid_meta = f"<b>Total Marks:</b> {mid_sem.get('total_marks', 50)} | <b>Duration:</b> {mid_sem.get('duration', '2 Hours')}"
        story.append(Paragraph(mid_meta, body_style))
        story.append(Paragraph(f"<b>Instructions:</b> {mid_sem.get('instructions', '')}", body_style))
        story.append(Spacer(1, 5))
        
        for sec in mid_sem.get("sections", []):
            story.append(Paragraph(f"<b>{sec.get('section_name', '')} ({sec.get('marks_per_question', 2)} Marks each)</b>", body_style))
            for q in sec.get("questions", []):
                q_line = f"Q{q.get('question_number', '')}. {q.get('text', '')} [Unit {q.get('unit_reference', '')}]"
                story.append(Paragraph(q_line, table_body_style))
            story.append(Spacer(1, 6))
            
        story.append(Spacer(1, 15))
        
        # End Semester
        end_sem = question_papers.get("end_semester", {})
        story.append(Paragraph("End-Semester Examination Draft", h2_style))
        end_meta = f"<b>Total Marks:</b> {end_sem.get('total_marks', 100)} | <b>Duration:</b> {end_sem.get('duration', '3 Hours')}"
        story.append(Paragraph(end_meta, body_style))
        story.append(Paragraph(f"<b>Instructions:</b> {end_sem.get('instructions', '')}", body_style))
        story.append(Spacer(1, 5))
        
        for sec in end_sem.get("sections", []):
            story.append(Paragraph(f"<b>{sec.get('section_name', '')} ({sec.get('marks_per_question', 2)} Marks each)</b>", body_style))
            for q in sec.get("questions", []):
                q_line = f"Q{q.get('question_number', '')}. {q.get('text', '')} [Unit {q.get('unit_reference', '')}]"
                story.append(Paragraph(q_line, table_body_style))
            story.append(Spacer(1, 6))
            
        story.append(PageBreak())
        
        # ==========================================
        # 6. BLOOM'S TAXONOMY MAPPING
        # ==========================================
        story.append(Paragraph("5. Bloom's Taxonomy Classification", h1_style))
        story.append(Paragraph("Cognitive levels mapping for each curriculum unit and Course Outcome (CO).", body_style))
        
        bloom_headers = [
            Paragraph("Unit / outcome", table_header_style),
            Paragraph("Bloom Level", table_header_style),
            Paragraph("Justification / Verbs", table_header_style)
        ]
        bloom_data = [bloom_headers]
        
        for u in bloom_mapping.get("unit_mappings", []):
            verbs = ", ".join(u.get("action_verbs", []))
            bloom_data.append([
                Paragraph(f"Unit {u.get('unit_number', '')}", table_body_style),
                Paragraph(u.get("cognitive_level", ""), table_body_style),
                Paragraph(f"<b>Verbs:</b> {verbs}<br/><i>{u.get('justification', '')}</i>", table_body_style)
            ])
            
        for co in bloom_mapping.get("co_mappings", []):
            bloom_data.append([
                Paragraph(co.get("co_code", ""), table_body_style),
                Paragraph(co.get("cognitive_level", ""), table_body_style),
                Paragraph(co.get("justification", ""), table_body_style)
            ])
            
        bloom_table = Table(bloom_data, colWidths=[110, 130, 264])
        bloom_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), SECONDARY_COLOR),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(bloom_table)
        
        # Target Distribution
        story.append(Spacer(1, 15))
        story.append(Paragraph("Target Cognitive Distribution Chart", h2_style))
        dist = bloom_mapping.get("target_distribution", {})
        dist_text = ", ".join([f"<b>{k.title()}:</b> {v}%" for k, v in dist.items()])
        story.append(Paragraph(dist_text, body_style))
        
        story.append(PageBreak())
        
        # ==========================================
        # 7. CO MAPPING & QUALITY SCORE
        # ==========================================
        story.append(Paragraph("6. Course Outcome Alignment & Quality Report", h1_style))
        
        # CO weightage table
        story.append(Paragraph("Course Outcomes Weightage Breakdown", h2_style))
        co_headers = [
            Paragraph("CO Code", table_header_style),
            Paragraph("Assessment Marks Allocated", table_header_style),
            Paragraph("Percentage Weightage", table_header_style)
        ]
        co_tbl_data = [co_headers]
        for item in co_mapping.get("co_weightage", []):
            co_tbl_data.append([
                Paragraph(item.get("co_code", ""), table_body_style),
                Paragraph(str(item.get("marks_allocated", "")), table_body_style),
                Paragraph(f"{item.get('percentage_weightage', '')}%", table_body_style)
            ])
            
        co_table = Table(co_tbl_data, colWidths=[100, 204, 200])
        co_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), SECONDARY_COLOR),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(co_table)
        
        story.append(Spacer(1, 15))
        
        # Quality report details
        story.append(Paragraph("Academic Quality Score Card", h2_style))
        q_scores = quality_report.get("dimensions", {})
        score_info = f"""
        <b>Overall Compliance Score:</b> {quality_report.get('overall_score', 0)}/100<br/>
        • <b>CO-Exam Alignment:</b> {q_scores.get('alignment', 0)}/100<br/>
        • <b>Curriculum Coverage:</b> {q_scores.get('coverage', 0)}/100<br/>
        • <b>Clarity & Rigor:</b> {q_scores.get('clarity_and_rigor', 0)}/100<br/>
        • <b>Pedagogical Innovation:</b> {q_scores.get('pedagogy', 0)}/100
        """
        story.append(Paragraph(score_info, body_style))
        
        story.append(Spacer(1, 10))
        story.append(Paragraph("Suggestions for Continuous Improvement", h2_style))
        for sug in quality_report.get("suggestions", []):
            sug_p = f"• <b>[{sug.get('dimension', '').upper()}] Issue:</b> {sug.get('issue', '')}<br/>&nbsp;&nbsp;<b>Recommendation:</b> {sug.get('recommendation', '')}"
            story.append(Paragraph(sug_p, body_style))
            story.append(Spacer(1, 4))
            
        # Build PDF
        doc.build(story, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer.getvalue()
