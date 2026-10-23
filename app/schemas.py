from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class RuleSource(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_id: str
    title: str
    authority_type: Literal[
        "statute",
        "regulation",
        "binding_judicial_decision",
        "persuasive_judicial_decision",
        "official_agency_guidance",
        "contractual_obligation",
        "internal_policy",
        "approved_drafting_standard",
        "secondary_commentary",
    ]
    jurisdiction: str
    citation: str | None = None
    canonical_url: str | None = None
    publication_date: str | None = None
    effective_from: str | None = None
    effective_to: str | None = None
    source_status: Literal["current", "superseded", "draft", "unknown"] = "current"
    official_source: bool = False
    retrieval_timestamp: str
    content_hash: str
    text_version: str
    source_provenance: str
    relevant_document_categories: list[str] = Field(default_factory=list)
    parent_source_id: str | None = None


class DocumentUploadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document_type: str = "policy"
    jurisdiction: str = "US"
    review_date: str = "2026-10-23"
    analysis_scope: str = "full-document"


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document_type: str = "policy"
    jurisdiction: str = "US"
    review_date: str = "2026-10-23"
    analysis_scope: str = "full-document"


class PrincipleRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    principle_id: str
    description: str
    provenance_type: Literal[
        "explicit_document_text",
        "binding_authority",
        "persuasive_authority",
        "documented_policy_intent",
        "inferred_purpose",
        "unknown_purpose",
    ]
    supporting_sources: list[str]
    supporting_quotes: list[str]
    alternative_interpretations: list[str]
    confidence: float
    review_status: Literal["pending", "accepted", "rejected", "requires_review"]


class FindingRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    finding_id: str
    document_id: str
    category: str
    severity: Literal["low", "medium", "high", "critical"]
    evidence_status: Literal["observed", "corroborated", "inferred", "hypothesized", "unknown"]
    confidence: float
    headline: str
    document_quote: str | None = None
    document_locator: str | None = None
    applicable_rule_ids: list[str] = Field(default_factory=list)
    principle_id: str | None = None
    purpose_provenance: Literal[
        "explicit_document_text",
        "binding_authority",
        "persuasive_authority",
        "documented_policy_intent",
        "inferred_purpose",
        "unknown_purpose",
    ]
    explanation: str
    supporting_evidence: list[str] = Field(default_factory=list)
    strongest_counterargument: str
    alternative_explanations: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    falsification_conditions: list[str] = Field(default_factory=list)
    proposed_revision: str | None = None
    preventive_controls: list[str] = Field(default_factory=list)
    validation_tests: list[str] = Field(default_factory=list)
    residual_risks: list[str] = Field(default_factory=list)
    human_review_required: bool = True
    reviewer_status: Literal["pending", "accepted", "rejected", "needs_more_evidence", "deferred"] = "pending"


class AuditChecklistItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question_id: int
    question_group: str
    status: Literal["pass", "fail", "unknown", "not_applicable", "requires_review"]
    evidence: list[str] = Field(default_factory=list)
    reasoning: str


class AuditResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audit_id: str
    document_id: str
    analysis_version: str
    jurisdiction: str
    review_date: str
    corpus_version: str
    retrieval_status: Literal["success", "incomplete", "failed"]
    validation_status: Literal["passed", "failed", "incomplete"]
    checklist_results: list[AuditChecklistItem]
    findings: list[FindingRecord]
    limitations: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    overall_status: Literal["supported_issue", "plausible_risk", "insufficient_evidence", "adequate_for_tested_scope", "no_issue_identified"]


class DocumentRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document_id: str
    document_hash: str
    document_type: str
    jurisdiction: str
    review_date: str
    version: str
    ingestion_status: Literal["success", "warning", "failed"]
    extraction_warnings: list[str] = Field(default_factory=list)
    created_at: str


class RuleRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rule_id: str
    source_id: str
    rule_text: str
    authority_type: str
    jurisdiction: str
    effective_from: str | None = None
    effective_to: str | None = None
    source_status: str = "current"
    source_locator: str | None = None
    source_hash: str


class AnalysisReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document: DocumentRecord
    findings: list[FindingRecord]
    audit: AuditResult
    report_json: str
    report_text: str
