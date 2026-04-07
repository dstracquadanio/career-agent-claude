#!/usr/bin/env python3
"""
Example: Company-Specific Resume Generator
==========================================

This shows the full pattern for creating a tailored resume for a specific
company and role. Each company gets its own generator script that imports
the base template's styles and helpers, then customizes the content.

Company: Acme Corp (fake example)
Role: Business Analyst
Frame: BA — process improvement, data analysis, stakeholder communication

To generate:
    python3 build_doc.py example_resume_generator.py

The build_doc.py wrapper runs validation first (banned words, page fill,
metadata checks), then generates the PDF only if validation passes.
"""

import os
from generate_resume import (
    register_fonts, build_styles, make_link, job_row, edu_row,
    GOLD, BLACK, PW, PH, MARGIN_LR, MARGIN_TB,
    SZ_NAME, SZ_HDR, SZ_JOB, SZ_BODY, LH_BODY, LH_TIGHT, SECTION_GAP,
)
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
)

# ── Tuning knobs ──
# Adjust these to hit exactly 1 page at 95-99% fill.
# Run: python3 measure_resume.py example_resume_generator.py
# Output: pages,fill_pct (e.g., "1,97")
BODY_LEADING = LH_BODY       # 11.5 default — increase to fill, decrease to trim
TIGHT_LEADING = LH_TIGHT     # 11.0 default
SECTION_SPACING = SECTION_GAP # 5 default


def generate_resume(output_path):
    font_name = register_fonts()
    styles = build_styles(font_name)

    # ── PDF Metadata (ATS needs these) ──
    doc = BaseDocTemplate(
        output_path,
        pagesize=(PW, PH),
        leftMargin=MARGIN_LR,
        rightMargin=MARGIN_LR,
        topMargin=MARGIN_TB,
        bottomMargin=MARGIN_TB,
        title="Your Name - Business Analyst Resume - Acme Corp",      # ATS: title
        author="Your Name",                                            # ATS: author
        subject="Business Analyst application for Acme Corp",          # ATS: subject
        keywords=["business analyst", "data analysis", "process improvement",
                  "stakeholder management", "SQL", "Tableau"],         # ATS: keywords
    )
    frame = Frame(
        MARGIN_LR, MARGIN_TB,
        PW - 2 * MARGIN_LR, PH - 2 * MARGIN_TB,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    story = []

    # ══════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════
    story.append(Paragraph("YOUR NAME", styles["name"]))

    # Build contact line with clickable links
    linkedin = make_link("https://linkedin.com/in/yourprofile", "LinkedIn")
    portfolio = make_link("https://yourportfolio.com", "Portfolio")
    email_link = make_link("mailto:you@email.com", "you@email.com")
    story.append(Paragraph(
        f"New York, NY | (555) 555-5555 | {email_link} | {linkedin} | {portfolio}",
        styles["contact"],
    ))

    # ══════════════════════════════════════════════
    # SUMMARY
    # Tailored to the JD. Mirror their language.
    # "Business analyst" because that's the role.
    # ══════════════════════════════════════════════
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Business analyst with <b>3+ years</b> driving <b>process improvement</b> and "
        "<b>data-driven decision making</b> across product and operations teams. "
        "I've built reporting systems used by leadership for real-time decisions and "
        "coordinated cross-functional projects from requirements through delivery.",
        styles["summary"],
    ))

    # ══════════════════════════════════════════════
    # SKILLS
    # 3 categories max. Mirror JD keywords.
    # Bold the category label, plain items.
    # ══════════════════════════════════════════════
    story.append(Paragraph("SKILLS", styles["section_header"]))

    skills = [
        (
            "Analysis & Reporting",
            "SQL (Oracle, MySQL), Python (Pandas, NumPy), Tableau, Power BI, "
            "Excel (VBA, Pivot Tables, Financial Models), Statistical Analysis"
        ),
        (
            "Process & Delivery",
            "Requirements Gathering, Stakeholder Interviews, UAT Coordination, "
            "Agile/Scrum, JIRA, Confluence, Process Mapping"
        ),
        (
            "Communication",
            "Executive Dashboards, Scorecards, Cross-Functional Facilitation, "
            "Vendor Coordination, Technical Documentation"
        ),
    ]
    for label, items in skills:
        story.append(Paragraph(f"<b>{label}</b>", styles["skill_label"]))
        story.append(Paragraph(items, styles["skill_items"]))

    # ══════════════════════════════════════════════
    # PROFESSIONAL EXPERIENCE
    #
    # Each job: job_row() for the title line, then bullets.
    # Bullets use inline lists so the validator can count them.
    # Every bullet answers "so what?" — action + context + impact.
    # Bold the key metric or JD-matching term in each bullet.
    # ══════════════════════════════════════════════
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles["section_header"]))

    # --- Job 1: Current Role ---
    story.append(job_row(
        "<b>Business Analyst</b>, Current Company",
        "Jan 2024 – Present", styles,
    ))
    # IMPORTANT: Use inline lists (for b in [...]) so the validator can count bullets.
    for b in [
        "Diagnosed <b>conversion decline</b> by analyzing data across multiple systems, "
        "identifying root cause patterns, and coordinating phased remediation with engineering",
        "Built automated <b>data validation pipelines</b> reducing manual review by <b>40%</b> "
        "and error rates by <b>30%</b>, standardizing quality control across teams",
        "Designed executive <b>dashboards</b> tracking operational KPIs, used by leadership "
        "for real-time decisions on product performance and project health",
        "Standardized <b>metric definitions</b> across business and finance teams through "
        "structured stakeholder interviews, eliminating reporting inconsistencies",
    ]:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # --- Job 2: Previous Role ---
    story.append(Spacer(1, 3))
    # Hyperlink a project if you have one
    project_link = make_link("https://yourproject.com", "Your Project")
    story.append(job_row(
        f"<b>Founder & Product Lead</b>, {project_link}",
        "Jan 2023 – Dec 2023", styles,
    ))
    for b in [
        "Managed full product lifecycle from <b>requirements gathering</b> through "
        "implementation, testing, and weekly production releases serving 3 markets",
        "Ran <b>100+ stakeholder interviews</b>, synthesizing feedback into prioritized "
        "requirements and maintaining transparent communication on scope and tradeoffs",
        "Redesigned data architecture to reduce <b>API costs by 95%</b> and cut "
        "page load time from 7 minutes to <b>15 seconds</b>",
    ]:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # --- Job 3: Earlier Career ---
    story.append(Spacer(1, 3))
    story.append(job_row(
        "<b>Associate Analyst</b>, Earlier Company, City, Country",
        "Jan 2021 – Dec 2022", styles,
    ))
    for b in [
        "Managed <b>$XM project portfolio</b> across multiple concurrent programs, "
        "coordinating cross-functional teams spanning engineering, operations, and vendors",
        "Built automated reconciliation tools reducing <b>billing errors by 20%</b>, "
        "protecting <b>$170K+</b> in annual revenue",
        "Compiled weekly <b>executive dashboards</b> on portfolio performance, risk status, "
        "resource forecasts, and delivery milestones for senior leadership",
        "Led <b>process improvement</b> initiative using structured methodology that "
        "reduced cycle time and improved delivery predictability",
    ]:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # --- Job 4: Academic Role (optional, for recent grads) ---
    story.append(Spacer(1, 3))
    story.append(job_row(
        "<b>Graduate Associate, Analytics</b>, Your University",
        "Jan 2022 – Dec 2023", styles,
    ))
    for b in [
        "Built analytics platform serving <b>200+</b> stakeholders, improving forecast "
        "accuracy by <b>18%</b> and satisfaction scores from <b>75% to 90%</b>",
    ]:
        story.append(Paragraph(f'<bullet>\u25cf</bullet>{b}', styles["bullet"]))

    # ══════════════════════════════════════════════
    # EDUCATION
    # ══════════════════════════════════════════════
    story.append(Paragraph("EDUCATION", styles["section_header"]))
    story.append(edu_row(
        "<b>Master of Engineering Management</b>, Your University | 3.67/4.0",
        "Jan 2022 – Dec 2023", styles,
    ))
    story.append(Paragraph(
        "Coursework: Decision Analysis, Corporate Finance, Statistical Methods, Financial Statement Analysis",
        styles["cert"],
    ))
    story.append(edu_row(
        "<b>Bachelor of Engineering</b>, Your Undergrad | 3.3/4.0",
        "Aug 2018 – Aug 2022", styles,
    ))

    # ══════════════════════════════════════════════
    # CERTIFICATIONS (optional — include if JD values them)
    # ══════════════════════════════════════════════
    story.append(Paragraph("CERTIFICATIONS", styles["section_header"]))
    story.append(Paragraph(
        "Relevant Certification 1 | Relevant Certification 2 | Relevant Certification 3",
        styles["cert"],
    ))

    # ── Build PDF ──
    doc.build(story)
    print(f"Resume generated: {output_path}")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(__file__), "output", "AcmeCorp_BA_Resume.pdf")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generate_resume(output)
    print("Done!")
