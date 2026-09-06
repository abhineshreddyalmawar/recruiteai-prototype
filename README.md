# VerifyHire Prototype

An AI-assisted resume screening pipeline built for Northline Talent Systems — resume parsing, fraud detection, and candidate matching, powered by Claude's tool-use and structured JSON schemas.

**Status:** Prototype fully integrated and deployed as of Sep 6, 2026. Resume Parsing, Fraud Detection, Candidate Matching, multi-candidate Integration, and a live web UI are all complete and running on AWS. Not production-hardened software — see [Scope](#scope-prd-vs-prototype) below.

**Live demo:** [http://3.133.99.163:5001](http://3.133.99.163:5001) — upload one or more resumes (PDF) and a job description, get back ranked, explained match scores and fraud checks for each candidate. This is a development server on a temporary IP-based link, not a production deployment — it may occasionally need a restart.

---

## Pipeline

```
Resume file(s) (PDF/DOCX)                Job description text
        │                                        │
        ▼                                        ▼
Text extraction (extract_text.py)     Structured JD (matching.py)
        │                                        │
        ▼                                        │
Structured JSON (structure_resume.py)             │
        │                                        │
        ▼                                        │
Fraud Detection scorecard (fraud_detection.py)    │
   ├─ Timeline overlap check (deterministic)      │
   ├─ Tech-stack plausibility (Claude reasoning)   │
   ├─ Title progression consistency (Claude)       │
   └─ Unified scorecard synthesis (deterministic)  │
        │                                        │
        └───────────────┬────────────────────────┘
                         ▼
        Candidate Matching (matching.py) — repeated per resume
                         │
                         ▼
        Coordinator (coordinator.py) — ranks all candidates
                         │
                         ▼
        Flask web app (app.py + templates/index.html)
                         │
                         ▼
        Deployed on AWS EC2 — live, public URL
```

## Scope: PRD vs. Prototype

The full product PRD describes a 6-module, multi-tenant SaaS platform with live ATS integrations. This prototype deliberately builds only the differentiated, highest-value core.

| Module | PRD (full product) | This prototype | Status |
|---|---|---|---|
| Resume Parsing | pyresparser + Claude 6-pass enhancement | pdfplumber + Claude structuring | ✅ Complete |
| Fraud Detection | Full multi-signal pipeline | Same core signals, explicit criteria | ✅ Complete |
| Candidate Matching | pgvector semantic search + Claude scoring | Claude scoring only, no vector DB | ✅ Complete |
| Integration | Full orchestration layer | Coordinator ranks multiple candidates per job | ✅ Complete |
| Web UI | Full production frontend | Flask + Jinja, multi-resume dashboard | ✅ Complete |
| Deployment | AWS ECS Fargate, CDK, multi-tenant | Single EC2 instance, IP-based demo link | ✅ Live (demo-grade) |
| ATS Integration (Ceipal, Bullhorn) | Live API sync | Not built | ⛔ Out of scope |
| Job Board Aggregation | TheirStack, Ceipal feeds | Not built | ⛔ Out of scope |
| Outreach Automation | Claude personalization + mass email/SMS | Not built | ⛔ Out of scope |

## Engineering practices used throughout

- **`.gitignore` committed before any other file** — secrets (API keys) and the virtual environment are structurally excluded from version history from commit one, not cleaned up after the fact.
- **Single-responsibility modules** — extraction, structuring, and fraud checks are separate files, each independently testable.
- **Deterministic logic vs. LLM judgment, split deliberately** — date math (timeline overlaps, career-span calculations) runs in plain Python; Claude is only used for genuine judgment calls (plausibility, consistency), always with explicit criteria rather than open-ended instructions.
- **Nullable, schema-enforced fields** — missing resume data is reported honestly (`null`), never fabricated, via `tool_use` JSON schemas.
- **Every module ships with permanent regression tests** — not just a single successful run; each check is verified against clean cases, deliberate true positives, and known edge cases (e.g. a single-job resume, simultaneous overlaps).
- **Known limitations are documented, not hidden** — e.g. self-reported LLM confidence scores are not yet calibrated against a validation set; flagged explicitly in the build log rather than assumed reliable.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install pdfplumber python-docx anthropic python-dotenv flask
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

## Running it

```bash
python3 app.py
```
Visit `http://localhost:5001`, upload one or more resumes (PDF) and paste a job description. Results are ranked by match score with expandable per-category detail and fraud check status for each candidate.

## Progress tracking

Progress is tracked by work item (16 total across the full prototype), not calendar days. Detailed daily build logs — including design decisions, debugging narratives, and interview-style Q&A for each concept — are maintained separately and available on request.

**As of Sep 6, 2026: 14/16 items complete (87.5%).** Remaining: broader real-resume testing, demo rehearsal.

---

