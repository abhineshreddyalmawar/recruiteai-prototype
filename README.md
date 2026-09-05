# RecruiteAI Prototype

An AI-assisted resume screening pipeline built for TechClub Inc. — resume parsing, fraud detection, and candidate matching, powered by Claude's tool-use and structured JSON schemas.

**Status:** Prototype in active development. Fraud Detection module complete as of Sep 5, 2026 (checkpoint 1 of 2). Not production software — see [Scope](#scope-prd-vs-prototype) below.

---

## Pipeline

```
Resume file (PDF/DOCX)
        │
        ▼
Text extraction (extract_text.py)
        │
        ▼
Structured JSON via Claude tool_use (structure_resume.py)
        │
        ▼
Fraud Detection scorecard (fraud_detection.py)
   ├─ Timeline overlap check (deterministic)
   ├─ Tech-stack plausibility (Claude reasoning)
   ├─ Title progression consistency (Claude reasoning)
   └─ Unified scorecard synthesis (deterministic aggregation)
        │
        ▼
Candidate Matching  ← in progress
        │
        ▼
Coordinator / Integration  ← planned
```

## Scope: PRD vs. Prototype

The full product PRD describes a 6-module, multi-tenant SaaS platform with live ATS integrations. This prototype deliberately builds only the differentiated, highest-value core.

| Module | PRD (full product) | This prototype | Status |
|---|---|---|---|
| Resume Parsing | pyresparser + Claude 6-pass enhancement | pdfplumber + Claude structuring | ✅ Complete |
| Fraud Detection | Full multi-signal pipeline | Same core signals, explicit criteria | ✅ Complete |
| Candidate Matching | pgvector semantic search + Claude scoring | Claude scoring only, no vector DB | 🔨 In progress |
| ATS Integration (Ceipal, Bullhorn) | Live API sync | Not built | ⛔ Out of scope |
| Job Board Aggregation | TheirStack, Ceipal feeds | Not built | ⛔ Out of scope |
| Outreach Automation | Claude personalization + mass email/SMS | Not built | ⛔ Out of scope |
| Infrastructure | AWS ECS Fargate, CDK, multi-tenant | Single EC2/Lambda, minimal Flask UI | 📅 Planned (Polish phase) |

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
pip install pdfplumber python-docx anthropic python-dotenv
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

## Progress tracking

Progress is tracked by work item (16 total across the full prototype), not calendar days. Detailed daily build logs — including design decisions, debugging narratives, and interview-style Q&A for each concept — are maintained separately and available on request.

**As of Sep 5, 2026: 8/16 items complete (50%).**

---

*Private repository — TechClub Inc. internal prototype.*
