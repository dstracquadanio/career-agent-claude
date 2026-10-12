#!/usr/bin/env python3
"""
Example: Company-Specific Cover Letter Generator
=================================================

This shows the full pattern for creating a tailored cover letter for a
specific company and role. Each company gets its own generator script
that imports the base template's function, then passes custom body text.

Company: Acme Corp (fake example)
Role: Business Analyst

To generate:
    python3 build_doc.py example_cover_letter_generator.py

The build_doc.py wrapper runs validation first (banned words, contractions,
sign-off check, length check), then generates the PDF only if validation passes.
"""

import os
from generate_cover_letter import generate_cover_letter

# ── Cover Letter Body ──
# Rules (from writing-rules.md):
#   - Story first, stats never
#   - Contractions always
#   - No banned words/phrases/transitions
#   - Open with what you built, not "I'm interested in..."
#   - 3-5 paragraphs, 200-350 words
#   - Greet with "Dear [Company] Hiring Team,"
#   - Close with "Best," and your full name on the next line (closing/signature args)
#   - Hyperlink projects with <a> tags
#   - One opinion minimum
#   - Vary paragraph lengths (don't make every paragraph 4 sentences)

BODY = """I've spent the last year and a half building reporting systems and fixing broken data workflows. The Business Analyst role at Acme Corp, especially the process improvement and stakeholder communication pieces, maps directly to what I've been doing.

At my current company, I inherited a reporting setup where three teams defined the same metric differently. I ran structured interviews with each team, mapped the discrepancies, and built a unified definitions doc that finance and product both signed off on. That cleared up a recurring quarterly argument and cut ad-hoc data requests by 40%. The dashboard I built on top of it is still what leadership uses for weekly reviews.

The data validation side is equally natural. I built automated pipelines that caught errors before they hit production, reducing manual review time by 40% and error rates by 30%. I work in SQL and Python daily, build in Tableau, and I've coordinated UAT cycles where I'm triaging defects with engineering while keeping stakeholders updated on timelines. It's not glamorous work but it's the work that actually makes products reliable.

Before that, I managed a project portfolio where the main challenge was getting five different teams to agree on priorities. I ran the weekly status reviews, maintained the risk logs, and built the executive dashboards leadership used to track delivery. The billing reconciliation work alone saved $170K annually.

I think Acme's approach to data infrastructure is right. Most companies I've seen treat BI as an afterthought. Building it into the product from day one changes what's possible downstream."""

if __name__ == "__main__":
    output = os.path.join(
        os.path.dirname(__file__), "output", "AcmeCorp_BA_CoverLetter.pdf"
    )
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generate_cover_letter(
        output,
        body_text=BODY,
        recipient="Dear Acme Corp Hiring Team,",
        closing="Best,",
        signature="Your Name",
        location="New York, NY",
        # ATS metadata — always set these
        title="Your Name - Cover Letter - Acme Corp Business Analyst",
        subject="Cover Letter for Business Analyst position at Acme Corp",
        keywords=["business analyst", "data analysis", "process improvement", "Acme Corp"],
    )
    print("Done!")
