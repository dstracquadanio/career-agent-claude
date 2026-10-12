#!/usr/bin/env python3
"""
Resume PDF Generator — Base Template
Carlito font, black headers, one page, justified text.

Replace all {{PLACEHOLDER}} values with your own information.
See config.example.yml for the full list of fields to customize.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Font Setup ──
# Carlito is a metric-compatible replacement for Calibri (common on macOS).
# Falls back to Helvetica if not found.
CARLITO_PATH = "/System/Library/PrivateFrameworks/FontServices.framework/Versions/A/Resources/Fonts/ApplicationSupport/Carlito.ttc"

def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont("Carlito", CARLITO_PATH, subfontIndex=0))
        pdfmetrics.registerFont(TTFont("Carlito-Bold", CARLITO_PATH, subfontIndex=3))
        pdfmetrics.registerFontFamily(
            "Carlito", normal="Carlito", bold="Carlito-Bold",
        )
        return "Carlito"
    except Exception:
        return "Helvetica"

# ── Constants ──
GOLD = HexColor("#D4A017")
BLACK = HexColor("#000000")
# Color for section headers and links. Black by default; set to GOLD or another
# HexColor for an accent.
ACCENT = BLACK
PW, PH = letter

SZ_NAME = 15
SZ_HDR = 10.5
SZ_JOB = 10
SZ_BODY = 9.5

MARGIN_LR = 27
MARGIN_TB = 20

LH_BODY = 11.5
LH_TIGHT = 11.0
SECTION_GAP = 5


def build_styles(font_name):
    fn = font_name
    fnb = f"{font_name}-Bold" if font_name == "Carlito" else "Helvetica-Bold"

    styles = {
        "name": ParagraphStyle(
            "name", fontName=fnb, fontSize=SZ_NAME,
            alignment=TA_CENTER, leading=SZ_NAME + 3,
            textColor=BLACK,
        ),
        "contact": ParagraphStyle(
            "contact", fontName=fn, fontSize=SZ_BODY,
            alignment=TA_CENTER, leading=LH_BODY,
            textColor=BLACK,
        ),
        "summary": ParagraphStyle(
            "summary", fontName=fn, fontSize=SZ_BODY,
            alignment=TA_JUSTIFY, leading=LH_BODY,
            textColor=BLACK,
        ),
        "section_header": ParagraphStyle(
            "section_header", fontName=fnb, fontSize=SZ_HDR,
            alignment=TA_LEFT, leading=SZ_HDR + 3,
            textColor=ACCENT, spaceBefore=SECTION_GAP, spaceAfter=2,
        ),
        "job_line": ParagraphStyle(
            "job_line", fontName=fn, fontSize=SZ_JOB,
            alignment=TA_LEFT, leading=SZ_JOB + 2,
            textColor=BLACK,
        ),
        "job_sub": ParagraphStyle(
            "job_sub", fontName=fn, fontSize=SZ_BODY - 0.5,
            alignment=TA_LEFT, leading=LH_TIGHT,
            textColor=BLACK,
        ),
        "job_date": ParagraphStyle(
            "job_date", fontName=fn, fontSize=SZ_BODY,
            alignment=TA_RIGHT, leading=SZ_BODY + 2,
            textColor=BLACK,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName=fn, fontSize=SZ_BODY,
            alignment=TA_JUSTIFY, leading=LH_TIGHT,
            leftIndent=14, bulletIndent=6, bulletFontSize=5,
            textColor=BLACK,
        ),
        "skill_label": ParagraphStyle(
            "skill_label", fontName=fnb, fontSize=SZ_BODY,
            alignment=TA_LEFT, leading=LH_TIGHT,
            textColor=BLACK, spaceBefore=2,
        ),
        "skill_items": ParagraphStyle(
            "skill_items", fontName=fn, fontSize=SZ_BODY,
            alignment=TA_LEFT, leading=LH_TIGHT,
            leftIndent=0, textColor=BLACK,
        ),
        "cert": ParagraphStyle(
            "cert", fontName=fn, fontSize=SZ_BODY,
            alignment=TA_LEFT, leading=LH_TIGHT,
            textColor=BLACK,
        ),
    }
    return styles


def make_link(url, text, color=ACCENT):
    return f'<a href="{url}" color="#{color.hexval()[2:]}">{text}</a>'


def job_row(title_company_text, date_text, styles):
    """Title + Company on same line, date right-aligned."""
    title_para = Paragraph(title_company_text, styles["job_line"])
    date_para = Paragraph(date_text, styles["job_date"])
    t = Table(
        [[title_para, date_para]],
        colWidths=[PW - 2 * MARGIN_LR - 110, 110],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def edu_row(degree_text, date_text, styles):
    deg = Paragraph(degree_text, styles["cert"])
    dt = Paragraph(date_text, styles["job_date"])
    t = Table(
        [[deg, dt]],
        colWidths=[PW - 2 * MARGIN_LR - 120, 120],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def generate_resume(output_path, title=None, subject=None, keywords=None):
    font_name = register_fonts()
    styles = build_styles(font_name)

    doc = BaseDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN_LR,
        rightMargin=MARGIN_LR,
        topMargin=MARGIN_TB,
        bottomMargin=MARGIN_TB,
        title=title or "{{NAME}} - Resume",
        author="{{NAME}}",
        subject=subject or "Resume",
        keywords=keywords or [],
    )
    frame = Frame(
        MARGIN_LR, MARGIN_TB,
        PW - 2 * MARGIN_LR, PH - 2 * MARGIN_TB,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    story = []

    # ── HEADER ──
    # Replace with your name and credentials
    story.append(Paragraph("YOUR NAME, CERTIFICATION", styles["name"]))
    linkedin = make_link("{{LINKEDIN_URL}}", "LinkedIn")
    portfolio = make_link("{{PORTFOLIO_URL}}", "Portfolio")
    email_link = make_link("mailto:{{EMAIL}}", "{{EMAIL}}")
    story.append(Paragraph(
        f"City, ST | {{{{PHONE}}}} | {email_link} | {linkedin} | {portfolio}",
        styles["contact"],
    ))

    # ── CERTIFICATIONS ──
    story.append(Paragraph("CERTIFICATIONS", styles["section_header"]))
    story.append(Paragraph(
        "Certification 1 | Certification 2 | Certification 3",
        styles["cert"],
    ))

    # ── SUMMARY (justified) ──
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Professional summary with <b>years of experience</b> in your domain. "
        "Describe your core competency and what you bring to roles. Include a "
        "<b>key achievement</b> and your professional focus areas like "
        "<b>skill area 1</b>, <b>skill area 2</b>, and <b>skill area 3</b>.",
        styles["summary"],
    ))

    # ── SKILLS ──
    story.append(Paragraph("SKILLS", styles["section_header"]))

    skills = [
        (
            "Category 1",
            "Skill A, Skill B, Skill C, Skill D, Skill E"
        ),
        (
            "Category 2",
            "Skill F, Skill G, Skill H, Skill I"
        ),
        (
            "Tools & Technical",
            "Tool A, Tool B, Tool C, Tool D, Tool E"
        ),
    ]
    for label, items in skills:
        story.append(Paragraph(f"<b>{label}</b>", styles["skill_label"]))
        story.append(Paragraph(items, styles["skill_items"]))

    # ── PROFESSIONAL EXPERIENCE ──
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles["section_header"]))

    # --- Current Role ---
    story.append(job_row(
        "<b>Your Title</b>, {{CURRENT_COMPANY}}",
        "Start Date – Present", styles,
    ))
    current_bullets = [
        "Accomplishment description with <b>key metric</b> and impact on the business "
        "or team, demonstrating your contribution to the organization's goals",
        "Second accomplishment with <b>quantified result</b> showing how you delivered "
        "value through specific actions and collaboration",
        "Third accomplishment describing <b>process improvement</b> or technical "
        "contribution with measurable outcome",
    ]
    for b in current_bullets:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # --- Previous Role 1 ---
    story.append(Spacer(1, 3))
    story.append(job_row(
        "<b>Previous Title</b>, {{PREV_COMPANY_1}}, Location",
        "Start Date – End Date", styles,
    ))
    prev1_bullets = [
        "Accomplishment with <b>cross-functional</b> collaboration, translating "
        "requirements into deliverables through structured processes",
        "Achievement involving <b>data analysis</b> or <b>process optimization</b> "
        "with measurable improvement metrics",
        "Contribution to <b>stakeholder communication</b> and reporting that "
        "improved decision-making across the organization",
        "Technical or operational improvement that reduced <b>errors by X%</b> "
        "or saved <b>$X</b> annually",
    ]
    for b in prev1_bullets:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # --- Project / Founder Role ---
    story.append(Spacer(1, 3))
    project_link = make_link("{{PROJECT_URL}}", "{{PROJECT_NAME}}")
    story.append(job_row(
        f"<b>Your Role</b>, {project_link}",
        "Start Date – End Date", styles,
    ))
    project_bullets = [
        "Managed the full development lifecycle from <b>discovery</b> and design through "
        "implementation, testing, and production releases",
        "Built and maintained project <b>schedules</b> with milestone tracking, "
        "dependency mapping, and resource forecasts",
        "Identified and resolved critical <b>performance issues</b>, reducing "
        "infrastructure costs by <b>X%</b>",
        "Managed <b>N+ stakeholder</b> engagements, synthesizing feedback into "
        "prioritized requirements",
    ]
    for b in project_bullets:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # --- Earlier Career ---
    story.append(Spacer(1, 3))
    story.append(job_row(
        "<b>Earlier Title</b>, {{PREV_COMPANY_2}}, Location",
        "Start Date – End Date", styles,
    ))
    earlier_bullets = [
        "Major accomplishment with <b>portfolio value or scope</b> across multiple "
        "concurrent projects or programs",
        "Schedule and milestone management with <b>Gantt charts</b>, critical path "
        "monitoring, and leadership reporting",
        "Risk and issue management with active tracking, <b>stakeholder reviews</b>, "
        "and escalation processes",
        "Process improvement initiative that saved <b>$X</b> annually through "
        "error reduction and efficiency gains",
        "Executive reporting with <b>dashboards</b> and scorecards on portfolio "
        "performance and delivery milestones",
    ]
    for b in earlier_bullets:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # --- Academic Role (optional) ---
    story.append(Spacer(1, 3))
    story.append(job_row(
        "<b>Graduate Associate, Focus Area</b>, {{UNIVERSITY}}",
        "Start Date – End Date", styles,
    ))
    academic_bullets = [
        "Built analytics platform serving <b>N+</b> stakeholders, improving "
        "forecast accuracy by <b>X%</b> through structured feedback and delivery",
    ]
    for b in academic_bullets:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # ── EDUCATION ──
    story.append(Paragraph("EDUCATION", styles["section_header"]))
    story.append(edu_row(
        "<b>Master of Your Degree</b>, {{UNIVERSITY}} | GPA/4.0",
        "Start Date – End Date", styles,
    ))
    story.append(Paragraph(
        "Coursework: Relevant Course 1, Relevant Course 2, Relevant Course 3",
        styles["cert"],
    ))
    story.append(edu_row(
        "<b>Bachelor of Your Degree</b>, {{UNDERGRAD}} | GPA/4.0",
        "Start Date – End Date", styles,
    ))

    # ── Build PDF ──
    doc.build(story)
    print(f"Resume generated: {output_path}")
    print(f"Page size: {PW}x{PH}, Margins: {MARGIN_LR}lr {MARGIN_TB}tb")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(__file__), "output", "resume.pdf")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generate_resume(output)
    print("Done!")
