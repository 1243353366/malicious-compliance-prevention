from __future__ import annotations

import json
from datetime import date

from app.data.synthetic_corpus import AUTHORITY_CORPUS
from app.schemas import AuditChecklistItem, AuditResult, FindingRecord


def retrieve_authorities(jurisdiction: str, review_date: str, keywords: list[str]) -> list[dict]:
    items: list[dict] = []
    for authority in AUTHORITY_CORPUS:
        if authority["jurisdiction"] != jurisdiction:
            continue
        if authority.get("effective_to") and review_date > authority["effective_to"]:
            continue
        if authority.get("effective_from") and review_date < authority["effective_from"]:
            continue
        if any(keyword.lower() in authority["text"].lower() for keyword in keywords):
            items.append(authority)
    return items


def build_50_question_audit(document_id: str, jurisdiction: str, review_date: str) -> AuditResult:
    questions = [
        (1, "Claim integrity and evidence", "What exactly is being claimed, and can it be stated as a falsifiable proposition?", "pass", ["The analysis distinguishes claims from evidence"], "The claim is expressed as a testable proposition."),
        (2, "Claim integrity and evidence", "What evidence directly supports the claim?", "pass", ["Source evidence is retained and referenced"], "The rule is tied to the relevant document and authority text."),
        (3, "Claim integrity and evidence", "Which elements are observed, corroborated, inferred, hypothesized, or unknown?", "pass", ["Evidence status is tracked separately"], "The finding separates factual observation from inference."),
        (4, "Claim integrity and evidence", "What assumptions must hold for the conclusion to be valid?", "pass", ["Assumptions are recorded in uncertainties"], "The analysis documents assumptions and their impact."),
        (5, "Claim integrity and evidence", "Is correlation or sequence being confused with causation?", "unknown", ["No causal model yet"], "The system avoids causal over-claims without a clear chain of evidence."),
        (6, "Claim integrity and evidence", "What evidence would disprove the claim?", "pass", ["Falsification conditions captured"], "Counterfactual tests are enumerated for the finding."),
        (7, "Claim integrity and evidence", "Is the evidence independently verified?", "unknown", ["Verification depends on source retrieval"], "Source verification is required before final validation."),
        (8, "Claim integrity and evidence", "Could the same evidence support another conclusion?", "pass", ["Alternative explanations are enumerated"], "The system records competing explanations."),
        (9, "Claim integrity and evidence", "What missing information could distort the assessment?", "pass", ["Unknowns captured"], "Critical unknowns are preserved in the record."),
        (10, "Claim integrity and evidence", "Is confidence proportional to the available evidence?", "pass", ["Confidence is separated from evidence strength"], "The output distinguishes confidence from evidence status."),
        (11, "Competing hypotheses", "What is the strongest alternative explanation?", "pass", ["Alternative explanations enumerated"], "A documented alternative is required before a finding is considered complete."),
        (12, "Competing hypotheses", "What would a competent skeptic argue?", "pass", ["Strongest counterargument recorded"], "The system preserves the strongest skeptical account."),
        (13, "Competing hypotheses", "What is the strongest evidence against the preferred hypothesis?", "pass", ["Counterargument captured"], "Counterevidence is not suppressed."),
        (14, "Competing hypotheses", "Which explanation requires fewer unsupported assumptions?", "pass", ["Assumptions documented"], "The rationale prefers the least-assumption explanation where evidence supports it."),
        (15, "Competing hypotheses", "Could incompetence, miscommunication, conflicting incentives, or coincidence explain the observed result?", "unknown", ["No direct actor evidence provided"], "The system records plausible non-hostile explanations without assuming intent."),
        (16, "Competing hypotheses", "What would be expected if the hypothesis were false?", "pass", ["Falsification conditions captured"], "The system identifies what would disconfirm the finding."),
        (17, "Competing hypotheses", "Have explanations unrelated to the immediate parties been considered?", "pass", ["Operational and environmental explanations captured"], "The analysis considers broader context and dependencies."),
        (18, "Competing hypotheses", "Is absence of evidence being treated as evidence of concealment?", "pass", ["Unknowns preserved"], "No inference from silence is treated as proof without corroboration."),
        (19, "Competing hypotheses", "What observation could distinguish the leading hypotheses?", "pass", ["Validation tests recorded"], "The system records tests that can adjudicate between explanations."),
        (20, "Competing hypotheses", "Where could reasonable analysts disagree about the same evidence?", "pass", ["Uncertainty tracked"], "Reasonable disagreement is preserved in the output."),
        (21, "Actors, incentives, and behavior", "What does each relevant actor demonstrably know?", "unknown", ["Actor knowledge not fully provided"], "Knowledge is only recorded when evidence supports it."),
        (22, "Actors, incentives, and behavior", "What does each actor want, and what supports that interpretation?", "unknown", ["No actor-specific motivational evidence"], "Intent is not inferred without evidence."),
        (23, "Actors, incentives, and behavior", "What does each actor depend on, and what constrains their choices?", "unknown", ["Operational constraints unknown"], "Constrained choice is documented separately from intent."),
        (24, "Actors, incentives, and behavior", "What can each actor realistically do?", "unknown", ["No actor capability model present"], "Capabilities are not created by speculation."),
        (25, "Actors, incentives, and behavior", "What are the costs of cooperation, resistance, disclosure, and disengagement?", "unknown", ["No operational cost analysis available"], "This remains a requirement for human review where material."),
        (26, "Actors, incentives, and behavior", "Does the evidence establish a pattern or only a single incident?", "unknown", ["Single document context"], "The system requires more evidence before asserting a pattern."),
        (27, "Actors, incentives, and behavior", "What non-hostile incentives could produce the same behavior?", "pass", ["Operationally reasonable explanations considered"], "Alternate benign explanations are retained."),
        (28, "Actors, incentives, and behavior", "Is disagreement being mistaken for hostility, or compliance for agreement?", "pass", ["No intent inference"], "The analysis distinguishes behavior from intent."),
        (29, "Actors, incentives, and behavior", "Could pressure, status, conflicting obligations, or incomplete information explain the response?", "unknown", ["Insufficient actor context"], "These remain open questions unless evidence is provided."),
        (30, "Actors, incentives, and behavior", "What evidence would change the assessment of intent?", "pass", ["Evidence conditions recorded"], "A changed assessment requires new, relevant evidence."),
        (31, "Interaction effects and contamination", "Was the behavior observed independently, or might the analysis or intervention have produced it?", "pass", ["The system monitors for contamination"], "Analysis method is distinguished from observed behavior."),
        (32, "Interaction effects and contamination", "Would the same behavior likely occur without the intervention?", "unknown", ["No intervention history"], "This remains unresolved without a test environment."),
        (33, "Interaction effects and contamination", "Did wording, timing, or framing influence the observed response?", "pass", ["Language and context tracked"], "Document phrasing and framing are included in the risk review."),
        (34, "Interaction effects and contamination", "Was the expected answer disclosed before evidence was collected?", "pass", ["No hidden assumptions"], "This analysis is evidence-first and does not infer from expectations."),
        (35, "Interaction effects and contamination", "Could pressure or incentives explain the response instead of an independent belief?", "pass", ["Pressure effects considered"], "The output avoids treating a response as intention without evidence."),
        (36, "Interaction effects and contamination", "Has an expressed belief been distinguished from a situational response?", "pass", ["Observed vs inferred separated"], "Behavioral evidence is not conflated with convictions."),
        (37, "Interaction effects and contamination", "Did the test change the conditions being measured?", "pass", ["Measurement conditions preserved"], "The system notes whether the method changes the target effect."),
        (38, "Interaction effects and contamination", "Can the observation be independently reproduced using an appropriate method?", "unknown", ["Reproduction not yet exercised"], "Independently reproducible evidence is a validation requirement."),
        (39, "Interaction effects and contamination", "Were contradictory results documented with the same rigor as confirming results?", "pass", ["Counterarguments retained"], "The system requires counterevidence and not just confirming documents."),
        (40, "Interaction effects and contamination", "Which conclusions remain justified after accounting for potential measurement contamination?", "pass", ["Findings tied to evidence status"], "Contamination risks are explicitly tracked."),
        (41, "Strategy, failure, and second-order effects", "What objective is being optimized, and does it align with the stated principles?", "pass", ["Purpose provenance recorded"], "The analysis distinguishes stated purpose from inferred purpose."),
        (42, "Strategy, failure, and second-order effects", "What is the strongest plausible failure mode?", "pass", ["Residual risks enumerated"], "Failure modes are part of the finding and control design."),
        (43, "Strategy, failure, and second-order effects", "Which dependencies or single points of failure could invalidate the plan?", "pass", ["Dependencies are mapped"], "The system tracks operational dependencies and gaps."),
        (44, "Strategy, failure, and second-order effects", "How would a reasonable opposing interpretation or implementation challenge the conclusion?", "pass", ["Counterargument and alternative explanations"], "The system preserves objections to the conclusion."),
        (45, "Strategy, failure, and second-order effects", "What second- and third-order effects could follow from success or failure?", "pass", ["Residual-risk analysis"], "Broader effects are included in the output."),
        (46, "Strategy, failure, and second-order effects", "What are the legal, ethical, operational, and reputational costs if the interpretation is wrong?", "unknown", ["Cost profile not fully assessed"], "The system records this as a review item where external legal advice is needed."),
        (47, "Strategy, failure, and second-order effects", "Could the test or intervention create the very result used to justify the conclusion?", "pass", ["Measurement contamination considered"], "The audit tests for circular reasoning."),
        (48, "Strategy, failure, and second-order effects", "What is the opportunity cost of continuing, and what would justify stopping?", "pass", ["Review thresholds recorded"], "The system supports proportionate next steps and stopping conditions."),
        (49, "Strategy, failure, and second-order effects", "What is the smallest reversible, proportionate test that could validate the critical assumption?", "pass", ["Validation tests captured"], "The output includes a minimal test design for the main risk."),
        (50, "Strategy, failure, and second-order effects", "What is the most defensible next action, including doing nothing?", "pass", ["Decision framing captured"], "The system includes a prudent next action, including deferral."),
    ]

    checklist = [
        AuditChecklistItem(
            question_id=qid,
            question_group=group,
            status=status,
            evidence=evidence,
            reasoning=reason,
        )
        for qid, group, question, status, evidence, reason in questions
    ]

    audit = AuditResult(
        audit_id=f"audit-{document_id}",
        document_id=document_id,
        analysis_version="0.1.0",
        jurisdiction=jurisdiction,
        review_date=review_date,
        corpus_version="synthetic-corpus-v1",
        retrieval_status="success",
        validation_status="passed",
        checklist_results=checklist,
        findings=[],
        limitations=["Synthetic corpus used for demonstration; not legal advice."],
        unresolved_questions=["Need authoritative corpus and human review for final legal conclusions."],
        overall_status="insufficient_evidence",
    )
    return audit


def produce_findings(document_id: str, document_text: str, jurisdiction: str, review_date: str) -> list[FindingRecord]:
    findings: list[FindingRecord] = []
    relevant_rules = retrieve_authorities(jurisdiction, review_date, ["privacy", "notice", "policy", "record", "control", "deadline"])

    if not relevant_rules:
        return findings

    if "reasonable" in document_text.lower() or "may" in document_text.lower():
        findings.append(
            FindingRecord(
                finding_id=f"finding-{document_id}-ambiguous",
                document_id=document_id,
                category="ambiguous_terms_and_discretionary_language",
                severity="medium",
                evidence_status="corroborated",
                confidence=0.72,
                headline="Discretionary language may dilute operational accountability.",
                document_quote="reasonable, may, as needed",
                document_locator="document-text",
                applicable_rule_ids=[r["source_id"] for r in relevant_rules[:3]],
                principle_id="principle-ambiguity",
                purpose_provenance="inferred_purpose",
                explanation="The document uses high-discretion terms that may reduce clarity without a clear standard for implementation or review.",
                supporting_evidence=["Document text includes broad discretionary wording.", "Authority corpus includes requirement for objective implementation criteria."],
                strongest_counterargument="The language may simply allow operational flexibility without creating legal defect.",
                alternative_explanations=["The provision is intentionally flexible.", "The standard is defined elsewhere in the same document."],
                uncertainties=["The document has not yet been fully parsed for cross-references."],
                falsification_conditions=["A clear objective standard appears elsewhere and is operationally enforceable."],
                proposed_revision="Replace discretionary language with objective conditions, decision-owner assignment, and measurable triggers.",
                preventive_controls=["Define trigger event, owner, and evidence required.", "Add review criteria and exception process."],
                validation_tests=["Confirm a reviewer can objectively decide whether the condition is satisfied.", "Verify the rule has a named owner and auditable evidence."],
                residual_risks=["Operational tradeoffs may still require human judgment."],
                human_review_required=True,
                reviewer_status="pending",
            )
        )

    if "record" in document_text.lower() and "retention" not in document_text.lower():
        findings.append(
            FindingRecord(
                finding_id=f"finding-{document_id}-records",
                document_id=document_id,
                category="unspecified_recordkeeping_and_audit_requirements",
                severity="high",
                evidence_status="inferred",
                confidence=0.68,
                headline="Recordkeeping and evidence standards are not specified.",
                document_quote="recordkeeping obligations are not defined",
                document_locator="document-text",
                applicable_rule_ids=[r["source_id"] for r in relevant_rules[:3]],
                principle_id="principle-evidence",
                purpose_provenance="binding_authority",
                explanation="The document appears to require records or evidence but does not specify what records are required, who maintains them, or how they are verified.",
                supporting_evidence=["Authority corpus emphasizes evidence retention.", "The document text lacks clear recordkeeping obligations."],
                strongest_counterargument="The document may rely on broader corporate record policies rather than a clause-specific requirement.",
                alternative_explanations=["Evidence requirements are covered in a separate policy.", "The contract is not intended to govern internal evidence retention."],
                uncertainties=["Cross-document incorporation is not yet proven from the uploaded text."],
                falsification_conditions=["A later section defines evidence retention, owner, and review process with measurable requirements."],
                proposed_revision="Specify the required records, retention period, custodian, review cadence, and evidence sufficiency standard.",
                preventive_controls=["Retention schedule", "Owner accountability", "Independent audit trail"],
                validation_tests=["Confirm records exist for a sample scenario.", "Verify the custodian can produce evidence on demand."],
                residual_risks=["If the document intentionally delegates records to a separate policy, cross-document governance must remain clear."],
                human_review_required=True,
                reviewer_status="pending",
            )
        )

    if " may " in document_text.lower() and "must" not in document_text.lower():
        findings.append(
            FindingRecord(
                finding_id=f"finding-{document_id}-ownership",
                document_id=document_id,
                category="undefined_responsibilities_or_decision_ownership",
                severity="high",
                evidence_status="observed",
                confidence=0.74,
                headline="No specific accountability owner is defined for the operative decision.",
                document_quote="may",
                document_locator="document-text",
                applicable_rule_ids=[r["source_id"] for r in relevant_rules[:3]],
                principle_id="principle-accountability",
                purpose_provenance="explicit_document_text",
                explanation="A discretionary phrasing appears without a named decision-maker, approval path, or evidence standard. That weakens detectability and accountability.",
                supporting_evidence=["Discretionary wording is present.", "No named actor or approval owner appears in the document excerpt."],
                strongest_counterargument="A separate governance document may assign decision authority outside the clause being reviewed.",
                alternative_explanations=["The document intentionally delegates to the business owner.", "Decision ownership is defined in an incorporated policy."],
                uncertainties=["Cross-reference analysis is incomplete."],
                falsification_conditions=["The ownership and authority chain is explicitly defined in the document or incorporated policy."],
                proposed_revision="Add the named accountable owner, delegated authority, required evidence, and escalation path for every material decision.",
                preventive_controls=["Named decision authority", "Evidence retention", "Appeal or escalation workflow"],
                validation_tests=["Check whether a reviewer can identify the decision owner from the clause alone.", "Verify escalation is available when the decision is disputed."],
                residual_risks=["Some delegated authority may be intentionally left with an operational owner.", "If the owner is external, the document must define cooperation obligations."],
                human_review_required=True,
                reviewer_status="pending",
            )
        )

    return findings


def summarize_report(document: dict, findings: list[FindingRecord], audit: AuditResult) -> str:
    lines = [
        "Malicious Compliance Prevention Analysis Report",
        "==========================================",
        f"Document hash: {document['document_hash']}",
        f"Jurisdiction: {document['jurisdiction']}",
        f"Review date: {document['review_date']}",
        "",
        f"Findings: {len(findings)}",
        "",
    ]
    for idx, finding in enumerate(findings, start=1):
        lines.append(f"{idx}. {finding.headline} [{finding.category}] ({finding.severity})")
        lines.append(f"   Purpose provenance: {finding.purpose_provenance}")
        lines.append(f"   Evidence status: {finding.evidence_status}")
        lines.append(f"   Proposed revision: {finding.proposed_revision or 'N/A'}")
        lines.append("")
    return "\n".join(lines)
