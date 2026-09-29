# Job Application System

AI-powered job application pipeline built on Claude Code. Generates tailored resumes and cover letters with built-in validation that catches AI slop before it leaves your machine.

## What This Does

You paste a job description. The system:
1. Picks the right master resume for the role type (PM, BA, DA, Strategy, etc.)
2. Generates a tailored resume as a PDF (reportlab, not HTML-to-PDF)
3. Generates a cover letter in your voice
4. Validates everything against 50+ banned words, 25+ banned phrases, AI detection patterns, and page fill requirements
5. Only produces the PDF if validation passes

No resume gets generated with "delve", "leverage", or "I am writing to express my strong interest." Ever.

## Why This Exists

Most AI resume tools generate text that reads like ChatGPT wrote it. Recruiters can tell. AI detectors can tell. This system has a 223-line writing playbook and a validation pipeline that blocks generation if the output contains AI patterns.

The validation catches:
- **Banned words**: delve, tapestry, leverage, synergies, passionate, spearheaded, etc.
- **Banned phrases**: "aligns perfectly", "unique combination", "I'm reaching out because", etc.
- **AI structural tells**: em dash abuse, rule-of-three, tidy summary closers, uniform sentence length
- **Page fill**: renders the PDF to a temp file and measures actual content height (not char-count heuristics)
- **Overflow**: catches resumes that spill to page 2

If any check fails, the PDF doesn't get built. Fix the issues, re-run.

## What's Different From Other Tools

| Feature | This system | Typical AI resume tool |
|---------|------------|----------------------|
| PDF generation | Python reportlab (pixel-precise control) | HTML-to-PDF (fragile) |
| Validation | Pre-build validator blocks AI slop | None, hope for the best |
| Voice enforcement | 223-line writing playbook + banned word/phrase lists | Generic tone |
| Page fill check | Actually renders PDF and measures height | Char count heuristic (always wrong) |
| Resume per role | Dedicated generator script per company/role | One template, keyword swap |
| Cover letters | Story-first, human voice, anti-AI-detection | "I am writing to express..." |

## Architecture

```
You paste a JD
    ↓
Claude picks master resume + frame
    ↓
Writes generate_{company}_{role}_resume.py
    ↓
measure_resume.py → checks page count + fill %
    ↓ (adjust until 1 page, 95%+ fill)
build_doc.py → validate_document.py → generate PDF
    ↓ (blocks if banned words, overflow, underfill)
Resume + Cover Letter PDFs ready
```

### Core Files

| File | Purpose |
|------|---------|
| `generate_resume.py` | Base resume PDF generator (Carlito font, black headers, justified text) |
| `generate_cover_letter.py` | Base cover letter PDF generator |
| `build_doc.py` | Validation wrapper — runs validator, then generates PDF only if it passes |
| `validate_document.py` | Checks banned words, phrases, transitions, AI patterns, page fill, metadata |
| `measure_resume.py` | Renders PDF to temp file, measures actual page count + fill percentage |
| `writing-rules.md` | The full anti-AI writing playbook (banned words, structural tells, smell tests) |
| `portals.yml` | 130+ career portal URLs for the scanner agent |
| `config.example.yml` | Your personal info template |

### Agents (Claude Code)

| Agent | Trigger | What it does |
|-------|---------|-------------|
| `job-apply` | Paste a JD | Full application orchestrator |
| `pinloop-scan` | "find jobs" | Search, count, pull and judge postings with [Pinloop](https://pinloop.ai), shortlist into a tab |
| `portal-scan` | "scan jobs" | Crawl career pages via Playwright for matching roles (fallback for companies Pinloop doesn't cover) |
| `form-fill` | "fill [URL]" | Read application forms, generate + fill answers |
| `batch-apply` | "batch these:" | Process multiple JDs in parallel |
| `resume-search` | "resume?" | Search existing resumes |
| `contact-find` | "find contact" | Find hiring manager emails |
| `cover-letter` | "cover" | Write cover letter |
| `email-draft` | "email" | Draft outreach email |

## Setup

### Prerequisites
- [Claude Code](https://claude.ai/claude-code) installed
- Python 3.10+
- reportlab (`pip install reportlab`)
- Carlito font (bundled on macOS, install on Linux: `apt install fonts-crosextra-carlito`)

### Install

```bash
git clone https://github.com/YOUR_USERNAME/job-application-system.git
cd job-application-system

# Install Python deps
pip install reportlab

# Configure your profile
cp config.example.yml config.yml
# Edit config.yml with your info

# Copy agents to Claude Code
cp agents/*.md ~/.claude/agents/

# Update paths in agent files to point to your install location
```

### First Resume

```bash
# 1. Look at the example
python3 example_resume_generator.py
open output/example_resume.pdf

# 2. Create your own
# Copy example_resume_generator.py, replace placeholder content with your info
# Run through the validator:
python3 build_doc.py your_resume_generator.py
```

## Finding Jobs with Pinloop

[Pinloop](https://pinloop.ai) is a terminal job board that searches postings from employers' career sites and job boards, and judges them against your resume. The `pinloop-scan` agent uses it as the front of the pipeline:

```
pinloop count → pull → quick screen → full judge → "to-apply" tab
    ↓
pinloop fetch (full JD text)
    ↓
batch-apply → tailored resume + cover letter PDFs → applications.md
```

Setup:

```bash
npm install -g pinloop
pinloop login
pinloop profile put resume --file masters/pm_master.pdf
```

Then tell Claude "find jobs" or "batch my to-apply tab". The free plan hands over 5 new postings a day; run bare `pinloop` to see what's left. Your resume and profile documents are stored on Pinloop's servers and sent to an AI model when postings are judged.

## Writing Rules

The `writing-rules.md` file is the core of what makes this system different. It enforces:

- **Story first, stats never** — lead with a real moment, not a pitch
- **Contractions always** — "I've" not "I have"
- **50+ banned words** — delve, tapestry, leverage, synergies, passionate, etc.
- **25+ banned phrases** — "aligns perfectly", "unique combination", "I'm reaching out because"
- **12 cover letter anti-patterns** — caught by audit, each one repeats if not banned
- **AI structural tells** — em dash abuse, rule-of-three, uniform sentence length, tidy summary closers
- **Smell test** — substitution test, aloud test, AI bingo, burstiness, screenshot test

## Portal Scanner

The system includes a Playwright-based career portal scanner covering 130+ companies across:
- Fintech (30): Stripe, Ramp, Robinhood, Coinbase, etc.
- Tech/SaaS (35): Notion, Figma, Databricks, Palantir, etc.
- AI/ML (20): Anthropic, OpenAI, Perplexity, Scale AI, etc.
- Marketplaces (15): DoorDash, Uber, Airbnb, Spotify, etc.
- Healthcare (15): Spring Health, Oscar Health, Zocdoc, etc.
- Big Tech (10): Google, Microsoft, Amazon, Apple, Meta, etc.
- Aggregators (8): YC Work at a Startup, Greenhouse/Lever/Ashby meta-search, Built In, Otta

## License

MIT
