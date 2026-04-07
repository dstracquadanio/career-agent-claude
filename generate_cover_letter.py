#!/usr/bin/env python3
"""
Cover Letter PDF Generator — Base Template
Gold name, Carlito font, clean formatting.

Replace all {{PLACEHOLDER}} values with your own information.
See config.example.yml for the full list of fields to customize.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import date

# ── Font Setup ──
CARLITO_PATH = "/System/Library/PrivateFrameworks/FontServices.framework/Versions/A/Resources/Fonts/ApplicationSupport/Carlito.ttc"

GOLD = HexColor("#D4A017")
BLACK = HexColor("#000000")
PW, PH = letter

# Cover letter specific sizes
SZ_NAME = 13
SZ_BODY = 10
SZ_SMALL = 9
LH = 13.5

MARGIN_LR = 54
MARGIN_TB = 40


def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont("Carlito", CARLITO_PATH, subfontIndex=0))
        pdfmetrics.registerFont(TTFont("Carlito-Bold", CARLITO_PATH, subfontIndex=3))
        return "Carlito"
    except Exception:
        return "Helvetica"


def generate_cover_letter(output_path, body_text, recipient="Hi,", location="New York, NY",
                          title=None, subject=None, keywords=None):
    font_name = register_fonts()
    fnb = f"{font_name}-Bold" if font_name == "Carlito" else "Helvetica-Bold"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN_LR,
        rightMargin=MARGIN_LR,
        topMargin=MARGIN_TB,
        bottomMargin=MARGIN_TB,
        title=title or "{{NAME}} - Cover Letter",
        author="{{NAME}}",
        subject=subject or "Cover Letter",
        keywords=keywords or [],
    )

    styles = {
        "name": ParagraphStyle(
            "name", fontName=fnb, fontSize=SZ_NAME,
            alignment=TA_LEFT, leading=SZ_NAME + 4,
            textColor=GOLD,
        ),
        "contact": ParagraphStyle(
            "contact", fontName=font_name, fontSize=SZ_SMALL,
            alignment=TA_LEFT, leading=SZ_SMALL + 3,
            textColor=BLACK,
        ),
        "date": ParagraphStyle(
            "date", fontName=font_name, fontSize=SZ_BODY,
            alignment=TA_LEFT, leading=LH,
            textColor=BLACK,
        ),
        "body": ParagraphStyle(
            "body", fontName=font_name, fontSize=SZ_BODY,
            alignment=TA_LEFT, leading=LH,
            textColor=BLACK, spaceBefore=0, spaceAfter=8,
        ),
        "greeting": ParagraphStyle(
            "greeting", fontName=font_name, fontSize=SZ_BODY,
            alignment=TA_LEFT, leading=LH,
            textColor=BLACK, spaceBefore=12, spaceAfter=8,
        ),
    }

    story = []

    # ── Header: Gold name ──
    story.append(Paragraph("YOUR NAME", styles["name"]))
    story.append(Paragraph(
        f"{location} | {{{{PHONE}}}} | {{{{EMAIL}}}} | "
        f'<a href="{{{{LINKEDIN_URL}}}}" '
        f'color="#{GOLD.hexval()[2:]}">LinkedIn</a> | '
        f'<a href="{{{{PORTFOLIO_URL}}}}" '
        f'color="#{GOLD.hexval()[2:]}">Portfolio</a>',
        styles["contact"],
    ))

    # ── Date ──
    story.append(Spacer(1, 20))
    today = date.today().strftime("%B %d, %Y")
    story.append(Paragraph(today, styles["date"]))

    # ── Greeting ──
    story.append(Paragraph(recipient, styles["greeting"]))

    # ── Body paragraphs ──
    paragraphs = [p.strip() for p in body_text.strip().split("\n\n") if p.strip()]
    for para in paragraphs:
        # Replace newlines within paragraphs with spaces
        clean = para.replace("\n", " ")
        story.append(Paragraph(clean, styles["body"]))

    # ── Build ──
    doc.build(story)
    print(f"Cover letter generated: {output_path}")


if __name__ == "__main__":
    # Example usage with placeholder text
    cover_letter_text = """This is a sample cover letter body. Replace this with your actual cover letter text tailored to the specific role and company.

Your cover letter should be 3-5 paragraphs, conversational in tone, and specific to the company you're applying to. Lead with what you've built, not what you want.

Best, {{FIRST_NAME}}"""

    output = os.path.join(os.path.dirname(__file__), "output", "cover_letter.pdf")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generate_cover_letter(output, cover_letter_text, recipient="Hi,", location="New York, NY")
    print("Done!")
