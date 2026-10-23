from __future__ import annotations

from pathlib import Path

from fastapi import UploadFile

from app.services.analysis import build_50_question_audit, produce_findings, retrieve_authorities, summarize_report
from app.services.ingestion import ingest_upload


def test_ingest_text_and_analyze(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("This policy states that it may be reasonable to retain records as needed for compliance review.")

    file = UploadFile(filename=sample.name, file=sample.open("rb"))
    result = __import__("asyncio").run(ingest_upload(file, 15 * 1024 * 1024))
    assert result["document_hash"]
    assert "reasonable" in result["text"].lower()

    findings = produce_findings("doc-123", result["text"], "US", "2026-10-23")
    assert findings
    assert findings[0].category

    audit = build_50_question_audit("doc-123", "US", "2026-10-23")
    assert len(audit.checklist_results) == 50


def test_retrieval_filters_by_jurisdiction():
    matches = retrieve_authorities("EU", "2026-10-23", ["accountability", "record"])
    assert matches
    assert all(item["jurisdiction"] == "EU" for item in matches)

    us_matches = retrieve_authorities("US", "2026-10-23", ["accountability", "record"])
    assert us_matches


def test_report_export_renders_summary():
    findings = produce_findings("doc-456", "This policy may require record retention for compliance review.", "US", "2026-10-23")
    audit = build_50_question_audit("doc-456", "US", "2026-10-23")
    report = summarize_report({"document_hash": "abc", "jurisdiction": "US", "review_date": "2026-10-23"}, findings, audit)
    assert "Malicious Compliance Prevention Analysis Report" in report
    assert "Findings:" in report


def test_schema_validation_can_instantiate_models():
    from app.schemas import AuditResult, AuditChecklistItem, FindingRecord

    item = AuditChecklistItem(question_id=1, question_group="Claim integrity and evidence", status="pass", evidence=["example"], reasoning="Example")
    finding = FindingRecord(
        finding_id="f-1",
        document_id="d-1",
        category="ambiguous_terms_and_discretionary_language",
        severity="medium",
        evidence_status="corroborated",
        confidence=0.8,
        headline="Example finding",
        explanation="Example explanation",
        strongest_counterargument="Need more evidence.",
    )
    audit = AuditResult(
        audit_id="a-1",
        document_id="d-1",
        analysis_version="0.1.0",
        jurisdiction="US",
        review_date="2026-10-23",
        corpus_version="test-v1",
        retrieval_status="success",
        validation_status="passed",
        checklist_results=[item],
        findings=[finding],
        limitations=[],
        unresolved_questions=[],
        overall_status="adequate_for_tested_scope",
    )
    assert audit.overall_status == "adequate_for_tested_scope"
