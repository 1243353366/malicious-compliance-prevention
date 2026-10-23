from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal


class RuleInterpretationType(str, Enum):
    LITERAL = "literal"
    INTENDED = "intended"
    INCENTIVE = "incentive"
    BEHAVIORAL = "behavioral"
    OUTCOME = "outcome"


class RuleRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RuleGapRecord:
    rule_id: str
    rule_text: str
    intent: str
    loophole: str
    exploit_strategy: str
    impact: str
    proposed_fix: str
    confidence: float
    historical_examples: list[str] = field(default_factory=list)
    content_hash: str = ""


@dataclass
class MaliciousComplianceStrategy:
    rule_id: str
    interpretation: RuleInterpretationType
    strategy: str
    legality: Literal["legal", "gray_area", "likely_illegal"]
    plausibility: Literal["low", "medium", "high"]
    damage_potential: Literal["low", "medium", "high", "critical"]
    confidence: float


@dataclass
class AdversarialInterpretation:
    actor: str
    interpretation: str
    conclusion: str
    evidence: str


@dataclass
class FailureMemoryEntry:
    exploit_pattern: str
    affected_rule_type: str
    severity: RuleRiskLevel
    mitigation: str
    test_created: bool = False
    sentinel_created: bool = False
    content_hash: str = ""


@dataclass
class SentinelRule:
    name: str
    purpose: str
    trigger: str
    response: str
    monitoring_target: str
    action: str
    content_hash: str = ""


RULE_GAP_DIRECTIVE = """
Rule-Gap Intelligence Directive

The system must not treat rules as static text alone.
Instead, each rule must be evaluated across five dimensions:
- literal interpretation
- intended meaning
- incentive alignment
- behavioral consequence
- outcome impact

The true question is not merely whether a rule is violated.
The true question is whether a rule can be satisfied while defeating its purpose.

Every discovered loophole becomes knowledge.
Every exploit becomes a mitigated pattern.
Every repeated gap becomes a sentinel.
"""


def canonicalize_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_sha256(data: str | bytes) -> str:
    if isinstance(data, str):
        payload = data.encode("utf-8")
    else:
        payload = data
    return hashlib.sha256(payload).hexdigest()


def bind_rule_gap_hash(record: RuleGapRecord) -> RuleGapRecord:
    payload = canonicalize_json(
        {
            "rule_id": record.rule_id,
            "rule_text": record.rule_text,
            "intent": record.intent,
            "loophole": record.loophole,
            "exploit_strategy": record.exploit_strategy,
            "impact": record.impact,
            "proposed_fix": record.proposed_fix,
            "confidence": record.confidence,
            "historical_examples": record.historical_examples,
        }
    )
    record.content_hash = compute_sha256(payload)
    return record


def bind_failure_hash(entry: FailureMemoryEntry) -> FailureMemoryEntry:
    payload = canonicalize_json(
        {
            "exploit_pattern": entry.exploit_pattern,
            "affected_rule_type": entry.affected_rule_type,
            "severity": entry.severity,
            "mitigation": entry.mitigation,
            "test_created": entry.test_created,
            "sentinel_created": entry.sentinel_created,
        }
    )
    entry.content_hash = compute_sha256(payload)
    return entry


def bind_sentinel_hash(rule: SentinelRule) -> SentinelRule:
    payload = canonicalize_json(
        {
            "name": rule.name,
            "purpose": rule.purpose,
            "trigger": rule.trigger,
            "response": rule.response,
            "monitoring_target": rule.monitoring_target,
            "action": rule.action,
        }
    )
    rule.content_hash = compute_sha256(payload)
    return rule


def create_rule_gap_record(
    *,
    rule_id: str,
    rule_text: str,
    intent: str,
    loophole: str,
    exploit_strategy: str,
    impact: str,
    proposed_fix: str,
    confidence: float,
    historical_examples: list[str] | None = None,
) -> RuleGapRecord:
    record = RuleGapRecord(
        rule_id=rule_id,
        rule_text=rule_text,
        intent=intent,
        loophole=loophole,
        exploit_strategy=exploit_strategy,
        impact=impact,
        proposed_fix=proposed_fix,
        confidence=confidence,
        historical_examples=historical_examples or [],
    )
    return bind_rule_gap_hash(record)


def create_malicious_compliance_strategy(
    *,
    rule_id: str,
    interpretation: RuleInterpretationType,
    strategy: str,
    legality: Literal["legal", "gray_area", "likely_illegal"],
    plausibility: Literal["low", "medium", "high"],
    damage_potential: Literal["low", "medium", "high", "critical"],
    confidence: float,
) -> MaliciousComplianceStrategy:
    return MaliciousComplianceStrategy(
        rule_id=rule_id,
        interpretation=interpretation,
        strategy=strategy,
        legality=legality,
        plausibility=plausibility,
        damage_potential=damage_potential,
        confidence=confidence,
    )


def create_adversarial_interpretation(
    *,
    actor: str,
    interpretation: str,
    conclusion: str,
    evidence: str,
) -> AdversarialInterpretation:
    return AdversarialInterpretation(
        actor=actor,
        interpretation=interpretation,
        conclusion=conclusion,
        evidence=evidence,
    )


def create_failure_memory_entry(
    *,
    exploit_pattern: str,
    affected_rule_type: str,
    severity: RuleRiskLevel,
    mitigation: str,
    test_created: bool = False,
    sentinel_created: bool = False,
) -> FailureMemoryEntry:
    entry = FailureMemoryEntry(
        exploit_pattern=exploit_pattern,
        affected_rule_type=affected_rule_type,
        severity=severity,
        mitigation=mitigation,
        test_created=test_created,
        sentinel_created=sentinel_created,
    )
    return bind_failure_hash(entry)


def create_sentinel_for_loophole(*, loophole: str, rule_id: str) -> SentinelRule:
    rule = SentinelRule(
        name=f"{rule_id}_loophole_sentinel",
        purpose="Detect when a rule is being interpreted in a way that defeats the intended purpose.",
        trigger=f"Observed pattern matching: {loophole}",
        response="Flag the behavior, log the exploit path, create a regression test, and require review before continuing.",
        monitoring_target="rule_enforcement_and_policy_execution",
        action="detect + test + require review + update mitigation",
    )
    return bind_sentinel_hash(rule)


def create_rule_gap_system() -> dict[str, Any]:
    return {
        "directive": RULE_GAP_DIRECTIVE,
        "analysis_layers": [
            "Rule",
            "Intent",
            "Incentive",
            "Behavior",
            "Outcome",
        ],
        "adversarial_council": [
            "Lawyer",
            "Auditor",
            "Bureaucrat",
            "Engineer",
            "Attacker",
            "Economist",
            "Psychologist",
        ],
        "decision_questions": [
            "What does the rule literally permit?",
            "What was the rule intended to prevent or require?",
            "What behavior does the rule incentivize?",
            "What outcome does that behavior actually produce?",
        ],
    }
