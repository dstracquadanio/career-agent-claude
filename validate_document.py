#!/usr/bin/env python3
"""
Resume & Cover Letter Validator

Runs as a PreToolUse hook on Bash commands. When Claude tries to run
`python3 generate_*resume*.py` or `generate_*cover*.py`, this script:
1. Reads the Python generator script
2. Extracts all text content
3. Checks against banned words, phrases, AI slop patterns, formatting rules
4. BLOCKS generation if issues found (non-zero exit)

Also runs standalone: python3 validate_document.py <script_path.py>
"""

import sys
import re
import json
import os
import subprocess
import tempfile

# ── BANNED WORDS (from writing-rules.md) ──
BANNED_WORDS = {
    "delve", "tapestry", "realm", "landscape", "embark", "multifaceted",
    "nuanced", "pivotal", "underscore", "meticulous", "vibrant", "whimsical",
    "gossamer", "labyrinth", "indelible", "leverage", "synergies", "facilitate",
    "utilize", "optimize", "robust", "comprehensive", "seamless", "cutting-edge",
    "revolutionary", "transformative", "illuminate", "elucidate", "commence",
    "endeavor", "intersection", "incredibly", "passionate", "excited", "thrilled",
    "spearheaded",
}

# ── BANNED PHRASES ──
BANNED_PHRASES = [
    "aligns perfectly",
    "resonated deeply",
    "i was particularly drawn to",
    "i'd love to explore",
    "unique combination",
    "well-positioned",
    "it's worth noting",
    "i'm confident that",
    "that got my attention",
    "that's exactly",
    "i'm reaching out because",
    "this role is a perfect fit",
    "i bring a unique blend",
    "thrilled at the opportunity",
    "i believe my experience",
    "i am writing to express",
    "i would welcome the opportunity",
    "in today's ever-evolving",
    "that's how i work",
    "that's been the day to day",
    "that's been the shape of my work",
    "that's the kind of",
    "that's where i do my best work",
    "what makes this role interesting",
    "the part i kept coming back to",
    "enabled non technical stakeholders",
]

# ── BANNED TRANSITIONS ──
BANNED_TRANSITIONS = [
    "moreover,", "furthermore,", "additionally,", "subsequently,",
    "nonetheless,", "it's worth noting that", "it is important to note",
    "that being said", "in conclusion,", "in summary,",
]

# ── PERMANENT RULES ──
# Customize these for your own fact-checking needs.
# Each rule has bad_patterns (regexes) and context (error message).
# Example: catching common date errors, misattributed facts, etc.
PERMANENT_CHECKS = {
    # Example: Prevent a common date error
    # "company_date": {
    #     "bad_patterns": [r"(?:apr|april)\s*2025"],
    #     "context": "Company X start date must be Mar 2025, NOT Apr 2025",
    # },
    # Example: Prevent misattributing an accomplishment
    # "achievement_misattribution": {
    #     "bad_patterns": [r"university.*\$?34\s*m"],
    #     "context": "$34M portfolio was at Company Y, NOT the university",
    # },
    "bad_signoff": {
        "bad_patterns": [r"best regards", r"sincerely,", r"warm regards", r"kind regards"],
        "context": "Sign off simply (e.g., 'Best, Name') — never 'Best regards', 'Sincerely', etc.",
    },
}


def extract_text_from_script(filepath):
    """Extract all user-facing text content from a Python generator script."""
    with open(filepath, "r") as f:
        content = f.read()

    texts = []
    excluded_ranges = []

    # Triple-quoted strings (cover letter body text, etc.)
    for match in re.finditer(r'"""(.*?)"""', content, re.DOTALL):
        texts.append(match.group(1))
        excluded_ranges.append((match.start(), match.end()))
    for match in re.finditer(r"'''(.*?)'''", content, re.DOTALL):
        texts.append(match.group(1))
        excluded_ranges.append((match.start(), match.end()))

    def in_excluded(pos):
        return any(s <= pos < e for s, e in excluded_ranges)

    # All string literals longer than 15 chars (skip if inside triple-quoted region)
    for match in re.finditer(r'"([^"]{15,})"', content):
        if not in_excluded(match.start()):
            texts.append(match.group(1))
    for match in re.finditer(r"'([^']{15,})'", content):
        if not in_excluded(match.start()):
            texts.append(match.group(1))

    return "\n".join(texts)


def check_banned_words(text):
    issues = []
    text_lower = text.lower()
    # Tokenize to check whole words
    words = set(re.findall(r'\b[a-z]+(?:-[a-z]+)*\b', text_lower))
    for word in BANNED_WORDS:
        if word in words:
            issues.append(f"BANNED WORD: '{word}'")
    return issues


def check_banned_phrases(text):
    issues = []
    text_lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            issues.append(f"BANNED PHRASE: '{phrase}'")
    return issues


def check_banned_transitions(text):
    issues = []
    text_lower = text.lower()
    for trans in BANNED_TRANSITIONS:
        if trans in text_lower:
            issues.append(f"BANNED TRANSITION: '{trans}'")
    return issues


def check_permanent_rules(text):
    issues = []
    text_lower = text.lower()
    for rule_name, rule in PERMANENT_CHECKS.items():
        for pattern in rule["bad_patterns"]:
            if re.search(pattern, text_lower):
                issues.append(f"RULE VIOLATION ({rule_name}): {rule['context']}")
                break  # One match per rule is enough
    return issues


def check_em_dashes(text):
    count = text.count("\u2014") + text.count("\u2013")
    # Also check for -- used as em dash (not in code like variable--)
    prose_dashes = len(re.findall(r'(?<=[a-zA-Z]) ?-- ?(?=[a-zA-Z])', text))
    total = count + prose_dashes
    if total > 1:
        return [f"EM DASH ABUSE: {total} em dashes found (max 1 per document)"]
    return []


def check_no_contractions(text):
    """Flag formal non-contractions in prose (skip code/variable names)."""
    issues = []
    formal_patterns = [
        (r'\bI am\b', "I'm"),
        (r'\bI have\b', "I've"),
        (r'\bdid not\b', "didn't"),
        (r'\bdo not\b', "don't"),
        (r'\bI will\b', "I'll"),
        (r'\bcannot\b', "can't"),
    ]
    for pattern, contraction in formal_patterns:
        if re.search(pattern, text):
            issues.append(f"USE CONTRACTION: Found formal form, use '{contraction}'")
    return issues


def render_check(script_path):
    """Build PDF and measure page count + fill percentage.

    Returns (pages, fill_pct) or (None, None) on error.
    Delegates to measure_resume.py which uses reportlab to compute
    actual content height vs frame height.
    """
    measure_script = os.path.join(os.path.dirname(__file__), "measure_resume.py")

    try:
        result = subprocess.run(
            [sys.executable, measure_script, script_path],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None, None

        # Parse last line (earlier lines are "Resume generated:" prints)
        last_line = result.stdout.strip().splitlines()[-1]
        parts = last_line.split(",")
        pages = int(parts[0])
        fill_pct = int(parts[1]) if len(parts) > 1 else -1
        return pages, fill_pct
    except Exception:
        return None, None


def _count_string_items(block):
    """Count string literal items in a list block (handles concatenated multi-line strings)."""
    items = re.findall(r'(?:^|\n)\s*(?:f?)"', block)
    items2 = re.findall(r"(?:^|\n)\s*(?:f?)'", block)
    return len(items) + len(items2)


def check_resume_completeness(script_content, script_path=None):
    """Resume-specific: enough bullets, required sections, links, page count."""
    issues = []

    # Count jobs (job_row calls)
    job_count = len(re.findall(r'job_row\(', script_content))

    # Count bullet items across ALL list patterns
    total_bullets = 0

    # Pattern 1: inline lists in for-loops
    inline_lists = re.findall(
        r'for\s+b\s+in\s+\[(.*?)\]:', script_content, re.DOTALL
    )
    for block in inline_lists:
        total_bullets += _count_string_items(block)

    # Pattern 2: named list variables used in for-loops
    named_loops = re.findall(r'for\s+b\s+in\s+(\w+):', script_content)
    for varname in named_loops:
        var_match = re.search(
            rf'{varname}\s*=\s*\[(.*?)\]', script_content, re.DOTALL
        )
        if var_match:
            total_bullets += _count_string_items(var_match.group(1))

    if total_bullets < 12 and job_count >= 3:
        issues.append(
            f"THIN RESUME: ~{total_bullets} bullet points across {job_count} jobs "
            f"(expect 12+ for a full resume)"
        )

    # Page check: render PDF and measure actual page count + fill percentage
    if script_path:
        pages, fill_pct = render_check(script_path)
        if pages is None:
            issues.append(
                "PAGE CHECK FAILED: could not render PDF to measure page count/fill. "
                "Fix render errors before generating."
            )
        elif pages is not None:
            if pages > 1:
                issues.append(
                    f"PAGE OVERFLOW: renders to {pages} pages (must be exactly 1). "
                    f"Trim bullets or tighten spacing."
                )
            elif pages == 1 and fill_pct >= 0 and fill_pct < 95:
                issues.append(
                    f"PAGE UNDERFILLED: content fills ~{fill_pct}% of the page (minimum 95%). "
                    f"Add more bullets, skills, or increase spacing to fill the page."
                )
            elif pages == 0:
                issues.append("RENDER ERROR: PDF generated with 0 pages.")

    # Required sections
    required = ["EXPERIENCE", "EDUCATION"]
    for sec in required:
        if sec not in script_content.upper():
            issues.append(f"MISSING SECTION: '{sec}'")

    return issues


def check_metadata(script_content):
    """Check that PDF metadata (title, author, subject, keywords) is set.
    ATS systems use this for parsing and indexing."""
    issues = []

    uses_base_template = bool(re.search(
        r'from\s+generate_(?:cover_letter|resume)\s+import', script_content
    ))

    has_title = bool(re.search(r'title\s*=\s*["\']', script_content))
    has_author = bool(re.search(r'author\s*=\s*["\']', script_content))
    has_subject = bool(re.search(r'subject\s*=\s*["\']', script_content))
    has_keywords = bool(re.search(r'keywords\s*=\s*[\["\']', script_content))

    if not has_title:
        issues.append("MISSING METADATA: No PDF title set (ATS needs this)")
    if not has_author and not uses_base_template:
        issues.append("MISSING METADATA: No PDF author set (ATS needs this)")
    if not has_subject:
        issues.append("MISSING METADATA: No PDF subject set (ATS needs this)")
    if not has_keywords:
        issues.append("MISSING METADATA: No PDF keywords set (ATS needs this)")

    return issues


def check_cover_letter_completeness(text):
    """Cover letter specific: sign-off, length."""
    issues = []

    # Length check (strip HTML)
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\\n', '\n', clean)
    if len(clean) > 2500:
        issues.append(f"TOO LONG: ~{len(clean)} chars (keep under 2000 for cover letters)")

    return issues


def validate_script(filepath):
    """Run all validations. Returns list of issues (empty = passed)."""
    with open(filepath, "r") as f:
        script_content = f.read()

    text = extract_text_from_script(filepath)
    is_resume = "resume" in filepath.lower()
    is_cover = "cover" in filepath.lower()

    all_issues = []

    # Universal checks
    all_issues.extend(check_banned_words(text))
    all_issues.extend(check_banned_phrases(text))
    all_issues.extend(check_banned_transitions(text))
    all_issues.extend(check_permanent_rules(text))
    all_issues.extend(check_em_dashes(text))
    all_issues.extend(check_metadata(script_content))

    # Cover letters get contraction check (resumes are more terse)
    if is_cover:
        all_issues.extend(check_no_contractions(text))
        all_issues.extend(check_cover_letter_completeness(text))

    # Resume completeness (render-based page count check)
    if is_resume:
        all_issues.extend(check_resume_completeness(script_content, script_path=filepath))

    return all_issues


def format_report(filepath, issues):
    """Format a human-readable validation report."""
    name = os.path.basename(filepath)
    if not issues:
        return f"VALIDATION PASSED: {name} (0 issues)"

    lines = [
        f"VALIDATION FAILED: {name} ({len(issues)} issues)",
        "Fix these before generating the PDF:",
    ]
    for i, issue in enumerate(issues, 1):
        lines.append(f"  {i}. {issue}")
    return "\n".join(lines)


def resolve_script_path(command):
    """Extract and resolve the generator script path from a bash command."""
    match = re.search(r'([\w/._~-]*generate_[\w]+\.py)', command)
    if not match:
        return None

    script_path = match.group(1)
    if script_path.startswith("~"):
        script_path = os.path.expanduser(script_path)

    if os.path.isabs(script_path) and os.path.exists(script_path):
        return script_path

    # Try common locations
    candidates = [
        os.path.join(os.path.dirname(__file__), script_path),
        os.path.join(os.getcwd(), script_path),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return None


def run_hook_mode():
    """PreToolUse hook mode. Reads JSON stdin, validates, blocks if needed."""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Only trigger on resume/cover letter generation
    if not re.search(r'python3?\s+.*generate_.*(?:resume|cover)', command, re.IGNORECASE):
        sys.exit(0)

    script_path = resolve_script_path(command)
    if not script_path:
        sys.exit(0)

    issues = validate_script(script_path)

    if issues:
        report = format_report(script_path, issues)
        print(report, file=sys.stderr)
        sys.exit(1)  # BLOCK the generation
    else:
        print(f"VALIDATION PASSED: {os.path.basename(script_path)}", file=sys.stderr)
        sys.exit(0)


def main():
    """Standalone mode."""
    if len(sys.argv) < 2:
        print("Usage: python3 validate_document.py <script_path.py>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    issues = validate_script(filepath)
    report = format_report(filepath, issues)
    print(report)
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] != "--hook":
        main()
    else:
        # Hook mode: called with --hook or no args + stdin
        run_hook_mode()
