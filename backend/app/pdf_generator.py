import io
import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfgen import canvas
import urllib.parse

# Theme Palette (LPU-inspired Orange and Charcoal)
PRIMARY_COLOR = colors.HexColor("#E77817")  # Orange
SECONDARY_COLOR = colors.HexColor("#1A252C")  # Charcoal
TEXT_COLOR = colors.HexColor("#333333")
LIGHT_BG = colors.HexColor("#F9F9F9")
BORDER_COLOR = colors.HexColor("#E0E0E0")

class PDFGenerator:
    @staticmethod
    def generate_certificate(
        participant_name: str,
        programme_title: str,
        certificate_number: str,
        date_str: str,
        qr_verification_url: str,
        digital_signature: str = "LPU_HRDC_OFFICIAL_SIGNATURE"
    ) -> bytes:
        """
        Generates an elegant, landscape-oriented training completion certificate in PDF.
        """
        buffer = io.BytesIO()
        
        # Use landscape letter size
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CertTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=32,
            leading=38,
            textColor=PRIMARY_COLOR,
            alignment=1,
            spaceAfter=20
        )
        
        subtitle_style = ParagraphStyle(
            'CertSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=16,
            leading=20,
            textColor=SECONDARY_COLOR,
            alignment=1,
            spaceAfter=30
        )
        
        body_style = ParagraphStyle(
            'CertBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=14,
            leading=22,
            textColor=TEXT_COLOR,
            alignment=1,
            spaceAfter=30
        )
        
        meta_style = ParagraphStyle(
            'CertMeta',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=SECONDARY_COLOR,
            alignment=1
        )
        
        story = []
        
        # Outer Border & Design
        story.append(Spacer(1, 40))
        story.append(Paragraph("LOVELY PROFESSIONAL UNIVERSITY", subtitle_style))
        story.append(Paragraph("HUMAN RESOURCE DEVELOPMENT CENTER (HRDC)", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("CERTIFICATE OF COMPLETION", title_style))
        story.append(Spacer(1, 10))
        
        body_text = (
            f"This is to certify that <b>{participant_name}</b> has successfully completed the <br/>"
            f"<b>{programme_title}</b> conducted by the LPU Human Resource Development Center.<br/>"
            f"The training was held from the scheduled timeline and complied with all institutional benchmarks."
        )
        story.append(Paragraph(body_text, body_style))
        story.append(Spacer(1, 20))
        
        # Footer section with verification details
        sig_text = (
            f"<b>Digital Verification Code:</b> {digital_signature}<br/>"
            f"<b>Certificate ID:</b> {certificate_number}<br/>"
            f"<b>Date of Issue:</b> {date_str}"
        )
        
        qr_text = (
            f"<b>Verification Page:</b><br/>"
            f"<font color='#E77817'>{qr_verification_url}</font>"
        )
        
        data = [
            [Paragraph(sig_text, meta_style), Paragraph(qr_text, meta_style)]
        ]
        
        t = Table(data, colWidths=[360, 360])
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
            ('TOPPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('BOX', (0,0), (-1,-1), 1, PRIMARY_COLOR),
        ]))
        
        story.append(t)
        
        # Build Document
        doc.build(story)
        return buffer.getvalue()

    @staticmethod
    def generate_programme_report(
        programme_title: str,
        category: str,
        coordinator_name: str,
        start_date: str,
        end_date: str,
        analytics: dict,
        feedback_list: list = None
    ) -> bytes:
        """
        Generates a summary audit PDF report of a completed training programme.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        h1_style = ParagraphStyle(
            'ReportH1',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=PRIMARY_COLOR,
            spaceAfter=15
        )
        
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=15,
            textColor=TEXT_COLOR,
            spaceAfter=10
        )
        
        header_style = ParagraphStyle(
            'ReportHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=SECONDARY_COLOR
        )
        
        story = []
        
        # Header Logo Block
        story.append(Paragraph("LPU HRDC NEXUS — PROGRAMME SUMMARY REPORT", header_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"{programme_title} ({category})", h1_style))
        story.append(Spacer(1, 10))
        
        # Overview metadata table
        metadata = [
            [Paragraph("<b>Coordinator:</b>", body_style), Paragraph(coordinator_name, body_style)],
            [Paragraph("<b>Start Date:</b>", body_style), Paragraph(start_date, body_style)],
            [Paragraph("<b>End Date:</b>", body_style), Paragraph(end_date, body_style)],
            [Paragraph("<b>Average Attendance:</b>", body_style), Paragraph(f"{analytics.get('average_attendance', 0.0)}%", body_style)],
            [Paragraph("<b>Feedback Rating:</b>", body_style), Paragraph(f"{analytics.get('average_feedback_rating', 0.0)} / 5.0", body_style)]
        ]
        
        t_meta = Table(metadata, colWidths=[150, 350])
        t_meta.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('BACKGROUND', (0,0), (0,-1), LIGHT_BG),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_meta)
        story.append(Spacer(1, 20))
        
        # Feedback analysis section
        story.append(Paragraph("<b>Participant Feedback Index & Suggestions:</b>", header_style))
        story.append(Spacer(1, 5))
        
        if feedback_list:
            fb_rows = [[Paragraph("<b>Rating</b>", body_style), Paragraph("<b>Comments / Suggestions</b>", body_style)]]
            for fb in feedback_list[:10]:
                rating_str = f"Overall: {fb.get('rating_overall', 5)}★ (Trainer: {fb.get('rating_trainer', 5)}★)"
                comment = fb.get("feedback_text") or fb.get("suggestions") or "No comments provided."
                fb_rows.append([Paragraph(rating_str, body_style), Paragraph(comment, body_style)])
                
            t_fb = Table(fb_rows, colWidths=[180, 320])
            t_fb.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t_fb)
        else:
            story.append(Paragraph("No participant feedback submitted yet.", body_style))
            
        doc.build(story)
        return buffer.getvalue()
