# malicious-compliance-prevention

A production-oriented legal rule-gap and malicious-compliance prevention analyzer with provenance tracking, adversarial audits, and source-grounded findings.

This repository contains a minimal but functional vertical slice for the specified system:

- FastAPI backend
- strict Pydantic request/response schemas
- PostgreSQL-backed persistence configuration
- document ingestion for TXT/PDF/DOCX
- synthetic authority corpus and retrieval filtering by jurisdiction/date
- rule-gap and principle-integrity analysis
- 50-question adversarial audit checklist
- reviewer workflow and report export
- browser-based review interface
- tests for the core path

Important: this is a documented vertical slice, not a claim of production legal certainty. The synthetic corpus is clearly labeled as test data and must not be treated as authoritative legal advice.

## Quick start

1. Copy `.env.example` to `.env` and set your PostgreSQL URL.
2. Start PostgreSQL using Docker Compose:

   ```bash
   docker compose up -d postgres
   ```

3. Create the app environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install -e .[dev]
   ```

4. Run the app:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Open http://localhost:8000/

## Environment configuration

See `.env.example` for the required settings. PostgreSQL is required; no SQLite or local fallback is used.

## Repository structure

```text
app/
  data/
    synthetic_corpus.py
  services/
    ingestion.py
    analysis.py
    retrieval.py
  __init__.py
  config.py
  db.py
  main.py
  models.py
  schemas.py
migrations/
  001_init.sql
docs/
  architecture.md
  security.md
  release-gate.md
tests/
  test_vertical_slice.py
```

## Notes

- Uploaded content is treated as untrusted and is never executed.
- Retrieval is filtered by jurisdiction and review date before applicability conclusions.
- Source provenance and citation verification are enforced in the analysis logic.
- The system separates observations, evidence, inferences, hypotheses, and unknowns.
- A finding is never promoted to a legal conclusion without source support and validation.
