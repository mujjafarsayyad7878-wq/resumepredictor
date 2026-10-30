"""
PDF Report Generator Service
Generates an executive PDF report using ReportLab.
Safely handles Unicode / non-Latin characters to prevent encoding crashes.
"""
import io
import re
from typing import Dict, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

def safe_pdf_str(text: Any) -> str:
    """
    Safely sanitizes text for ReportLab's standard Helvetica/Latin-1 encoding.
    """
    if text is None:
        return ""
    s = str(text)
    try:
        s.encode('latin-1')
        return s
    except UnicodeEncodeError:
        # Replace characters that cannot be encoded in Latin-1
        sanitized = []
        for ch in s:
            try:
                ch.encode('latin-1')
                sanitized.append(ch)
            except UnicodeEncodeError:
                sanitized.append('?')
        return "".join(sanitized)

def generate_pdf_report(analysis_data: Dict[str, Any]) -> bytes:
    """
    Builds a professional executive assessment PDF report from analysis results.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold'
    )
    
    subhead_style = ParagraphStyle(
        'SubHeaderStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#64748B')
    )

    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # 1. Title Banner
    story.append(Paragraph("Smart Resume Skill-Gap & Career Predictor", header_style))
    story.append(Paragraph("Executive Match & Learning Roadmap Report", subhead_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=14))

    # 2. Candidate & Target Role Summary Card
    profile = analysis_data.get("profile", {})
    fit = analysis_data.get("fit_analysis", {})
    salary = analysis_data.get("salary_prediction", {})
    
    cand_name = safe_pdf_str(profile.get("candidate_name") or "Candidate")
    contacts = profile.get("contact_info", {})
    email_str = safe_pdf_str(contacts.get("email") or "Not Specified")
    phone_str = safe_pdf_str(contacts.get("phone") or "Not Specified")
    exp_str = f"{profile.get('experience', {}).get('estimated_years', 0)} Years ({safe_pdf_str(profile.get('experience', {}).get('seniority_level', 'Professional'))})"
    target_role = safe_pdf_str(fit.get("target_role", "Target Role"))
    match_score = fit.get("overall_match_score", 0.0)
    tier = safe_pdf_str(fit.get("match_tier", "Match"))

    summary_data = [
        [
            Paragraph(f"<b>Candidate:</b> {cand_name}", body_style),
            Paragraph(f"<b>Target Role:</b> {target_role}", body_style)
        ],
        [
            Paragraph(f"<b>Contact:</b> {email_str} | {phone_str}", body_style),
            Paragraph(f"<b>Experience:</b> {exp_str}", body_style)
        ],
        [
            Paragraph(f"<b>Overall Match Score:</b> <font color='#2563EB'><b>{match_score}%</b></font> ({tier})", body_style),
            Paragraph(f"<b>Est. Compensation:</b> {safe_pdf_str(salary.get('formatted_median', 'N/A'))} ({salary.get('market_percentile', 50)}th percentile)", body_style)
        ]
    ]

    t_summary = Table(summary_data, colWidths=[270, 270])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#EDF2F7')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 14))

    # 3. Score Breakdown Matrix
    story.append(Paragraph("Assessment Metrics Breakdown", section_style))
    edu_str = safe_pdf_str(", ".join(profile.get("education", [])) or "Experience verified")
    metrics_data = [
        ["Metric", "Score / Weight", "Status / Details"],
        ["Hard Skills Coverage", f"{fit.get('skill_match_percentage', 0)}%", f"{len(fit.get('matched_skills', []))} Matched / {len(fit.get('missing_skills', []))} Missing"],
        ["Content Similarity", f"{fit.get('tfidf_similarity', 0)}%", "Evaluated via Vectorized Cosine Match"],
        ["Experience Match", f"{fit.get('experience_match_score', 0)}%", safe_pdf_str(fit.get("experience_status", "Evaluated"))],
        ["Education Alignment", f"{fit.get('education_match_score', 0)}%", edu_str]
    ]
    t_metrics = Table(metrics_data, colWidths=[180, 120, 240])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F5F9')]),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 14))

    # 4. Matched vs. Missing Skills
    story.append(Paragraph("Skills Breakdown", section_style))
    matched_skills_str = safe_pdf_str(", ".join(fit.get("matched_skills", [])) or "None detected")
    missing_skills_str = safe_pdf_str(", ".join(fit.get("missing_skills", [])) or "No critical gaps identified")
    
    skills_table_data = [
        [
            Paragraph("<b>Identified Matching Skills</b>", ParagraphStyle('GreenHead', parent=body_style, textColor=colors.HexColor('#059669'))),
            Paragraph(matched_skills_str, body_style)
        ],
        [
            Paragraph("<b>Missing Skills (To Learn)</b>", ParagraphStyle('RedHead', parent=body_style, textColor=colors.HexColor('#DC2626'))),
            Paragraph(missing_skills_str, body_style)
        ]
    ]
    t_skills = Table(skills_table_data, colWidths=[160, 380])
    t_skills.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#ECFDF5')),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor('#FEF2F2')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 14))

    # 5. Recommended Learning Roadmap
    recs = analysis_data.get("recommendations", [])
    if recs:
        story.append(Paragraph("Recommended Free Learning Courses & Practice", section_style))
        rec_rows = [["Skill", "Course / Tutorial", "Duration", "Practice Project"]]
        for r in recs[:5]:
            rec_rows.append([
                Paragraph(f"<b>{safe_pdf_str(r.get('skill', ''))}</b>", body_style),
                Paragraph(f"{safe_pdf_str(r.get('title', ''))}<br/><font color='#64748B'>{safe_pdf_str(r.get('provider', ''))}</font>", body_style),
                Paragraph(safe_pdf_str(r.get('duration', '')), body_style),
                Paragraph(safe_pdf_str(r.get('capstone_project', '')), body_style)
            ])
        t_recs = Table(rec_rows, colWidths=[80, 180, 80, 200])
        t_recs.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('PADDING', (0,0), (-1,-1), 5),
            ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ]))
        story.append(t_recs)

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
