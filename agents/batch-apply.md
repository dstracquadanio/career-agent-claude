# Batch Application Agent

You process multiple job descriptions in parallel, generating a complete application package for each: tailored resume, cover letter, and draft form answers. Every PDF goes through `build_doc.py` validation. Every text answer follows writing-rules.md.

## CONFIG

Generator scripts: `{{PROJECT_ROOT}}/`
Resume folder: `{{PROJECT_ROOT}}/resumes/`
Writing rules: `{{PROJECT_ROOT}}/writing-rules.md`
Validation: `python3 {{PROJECT_ROOT}}/build_doc.py <script>`
Measurement: `python3 {{PROJECT_ROOT}}/measure_resume.py <script>`
Application tracker: `{{PROJECT_ROOT}}/applications.md`
Output names: `output/{{FILE_PREFIX}}_{Company}_{Role}.pdf` and `..._CoverLetter.pdf` (`file_prefix` in config.yml, e.g. First_Last)

## MASTER RESUMES (read the actual PDF before choosing)

| JD signals | Master |
|---|---|
| product manager, PM, APM, product owner, product strategy | pm_master.pdf |
| business analyst, BA, systems analyst, process analyst | ba_master.pdf |
| data analyst, data science, SQL analyst, BI analyst | da_master.pdf |
| strategy, operations, consulting, chief of staff | stratops_master.pdf |
| project manager, TPM, program manager | project_mgr_master.pdf |

## INPUT FORMAT

User provides a list of JDs. Accept any of these formats:

**URLs:**
```
batch these:
1. https://boards.greenhouse.io/company1/jobs/12345
2. https://jobs.lever.co/company2/abcdef
3. https://company3.com/careers/role-title
```

**Pasted JDs:**
```
batch these:

---JOB 1---
[full JD text]

---JOB 2---
[full JD text]
```

**Mixed:**
```
batch these:
1. https://url-to-jd.com
2. [pasted JD text]
3. https://another-url.com
```

**Pinloop ids or tab:**
```
batch these: pinloop 154a6760-e853-4a2f-bf25-5e1fc5d59fc7, 4f188c1e-...
batch my to-apply tab
```
- Ids -> `pinloop fetch <ids> --json`
- Tab -> `pinloop tab get to-apply --all --json | pinloop fetch --json`
- Both are free for postings the account already holds. Use `description_text` as the JD (clean HTML entities), and keep the Pinloop id and posting URL for the tracker. See `pinloop-scan.md`.

## WORKFLOW

### Step 1: Parse All JDs

For each input:
- If URL -> fetch the JD using WebFetch or Playwright MCP
- If text -> use directly
- Extract: company name, role title, location, key requirements, best frame

Present a summary table for user confirmation:

```
BATCH: 5 roles parsed

# | Company        | Role                    | Frame  | Location
1 | Company A      | Associate PM            | APM    | NYC
2 | Company B      | Business Analyst        | BA     | NYC
3 | Company C      | Product Ops Associate   | APM    | Remote
4 | Company D      | AI Product Analyst      | DA     | SF
5 | Company E      | Strategy & Ops Assoc    | StratOps| NYC

Proceed with all 5? (or drop/change any)
```

Wait for user confirmation before proceeding.

### Step 2: Check Existing Materials

For each role, search resume folder for existing company-specific resumes.
Report what already exists and ask whether to regenerate or skip.

### Step 3: Generate in Parallel

For each role that needs generation, spawn parallel Agent workers. Each worker does:

#### 3a. Write Resume Generator Script
- Read the appropriate master resume PDF
- Create `generate_{company}_{role}_resume.py` following the exact template format
- All formatting constants from the template (margins, font sizes, leading)
- Summary tailored to JD
- Skills reframed for JD keywords
- Bullets reframed per role (bold key metrics and JD-matching terms)
- Hyperlink projects
- "to" for date ranges (NO en-dashes)
- Inline bullet lists (`for b in [...]`) so the validator can count them

#### 3b. Measure and Adjust Page Fill
- Run `measure_resume.py` on the generator script
- Target: 1 page, 95-99% fill
- If underfilled: increase leading, bump SECTION_GAP, add bullets
- If overflowed: decrease leading, reduce SECTION_GAP, trim bullets
- Iterate until 1 page and >= 95% fill

#### 3c. Build Resume Through Validator
- Run `build_doc.py` on the generator script
- If validation fails: fix and retry
- Must pass before proceeding

#### 3d. Write Cover Letter Generator Script
- Create `generate_{company}_{role}_cover_letter.py`
- Import from `generate_cover_letter.py`
- Write body text following ALL writing rules
- Greet with "Dear [Company] Hiring Team," (pass as `recipient`)
- Close with `closing="Best,"` and `signature="{{NAME}}"` so the name sits on its own line
- Hyperlink projects

#### 3e. Build Cover Letter Through Validator
- Run `build_doc.py` on the cover letter script
- Fix any banned word/phrase issues and retry until it passes

#### 3f. Draft Form Answers
- Check if the application has a form (navigate to apply URL if available)
- If form found via Playwright, extract questions
- If no form accessible, generate answers for common questions
- Write answers following writing-rules.md
- Save as `{{FILE_PREFIX}}_{Company}_{Role}_form_answers.md`

### Step 4: Present Results

After all workers complete, present a summary table with status per role, generated file paths, and next steps.

### Step 5: Update Tracker

Append each processed role to `applications.md`.

For roles that came from Pinloop, once the user confirms they submitted, remove the posting from the `to-apply` tab (`pinloop tab remove to-apply <item id>`).

## PARALLELIZATION RULES

1. **Spawn one Agent per role** using the Agent tool with separate prompts
2. Each agent is self-contained: it reads the master, writes the generator, validates, builds
3. Run up to 5 agents in parallel (to avoid overwhelming the system)
4. If more than 5 roles, process in waves of 5
5. Each agent MUST pass validation before marking complete
6. If an agent fails after 3 retries, mark that role as Failed and move on

## IMPORTANT RULES

1. **ALWAYS use `build_doc.py`** for PDF generation. NEVER call generator scripts directly.
2. **ALWAYS check `measure_resume.py`** before building to avoid overflow/underfill loops.
3. **Read the master resume PDF** before writing the generator script. Never guess at content.
4. **Load writing-rules.md** before writing any cover letter or form answer.
5. **Inline bullet lists** (`for b in [...]`) not named variables, so the validator can count them.
6. **No en-dashes** anywhere. Use "to" for date ranges.
7. **Never auto-submit applications.** Generate packages only.
