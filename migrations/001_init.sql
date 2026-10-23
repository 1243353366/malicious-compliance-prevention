CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_hash TEXT NOT NULL,
    document_type TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    review_date DATE NOT NULL,
    version TEXT NOT NULL,
    ingestion_status TEXT NOT NULL,
    extraction_warnings JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rule_sources (
    source_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    authority_type TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    citation TEXT,
    canonical_url TEXT,
    publication_date DATE,
    effective_from DATE,
    effective_to DATE,
    source_status TEXT NOT NULL,
    official_source BOOLEAN NOT NULL DEFAULT FALSE,
    retrieval_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    content_hash TEXT NOT NULL,
    text_version TEXT NOT NULL,
    source_provenance TEXT NOT NULL,
    relevant_document_categories JSONB,
    parent_source_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rule_chunks (
    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES rule_sources(source_id),
    chunk_text TEXT NOT NULL,
    chunk_hash TEXT NOT NULL,
    embedding VECTOR(768),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS principles (
    principle_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description TEXT NOT NULL,
    provenance_type TEXT NOT NULL,
    supporting_sources JSONB,
    supporting_quotes JSONB,
    alternative_interpretations JSONB,
    confidence DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    review_status TEXT NOT NULL DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS findings (
    finding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(document_id),
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    headline TEXT NOT NULL,
    document_quote TEXT,
    document_locator TEXT,
    applicable_rule_ids JSONB,
    principle_id UUID REFERENCES principles(principle_id),
    purpose_provenance TEXT,
    explanation TEXT NOT NULL,
    supporting_evidence JSONB,
    strongest_counterargument TEXT,
    alternative_explanations JSONB,
    uncertainties JSONB,
    falsification_conditions JSONB,
    proposed_revision TEXT,
    preventive_controls JSONB,
    validation_tests JSONB,
    residual_risks JSONB,
    human_review_required BOOLEAN NOT NULL DEFAULT FALSE,
    reviewer_status TEXT NOT NULL DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS audit_checklist_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(document_id),
    question_id INTEGER NOT NULL,
    question_group TEXT NOT NULL,
    status TEXT NOT NULL,
    evidence JSONB,
    reasoning TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, question_id)
);

CREATE TABLE IF NOT EXISTS analysis_runs (
    analysis_run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(document_id),
    analysis_version TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    review_date DATE NOT NULL,
    corpus_version TEXT,
    retrieval_status TEXT NOT NULL,
    validation_status TEXT NOT NULL,
    checklist_results JSONB,
    findings JSONB,
    limitations JSONB,
    unresolved_questions JSONB,
    overall_status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviewer_decisions (
    decision_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    finding_id UUID NOT NULL REFERENCES findings(finding_id),
    reviewer_name TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID,
    finding_id UUID,
    event_type TEXT NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
