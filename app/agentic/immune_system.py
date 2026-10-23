from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal


class SentinelType(str, Enum):
    OCR_FRICTION = "ocr_friction"
    SYNTAX_EATER = "syntax_eater"
    FAILURE_IMMUNITY = "failure_immunity"
    ATTACK_ISOLATION = "attack_isolation"


@dataclass
class IncidentRecord:
    incident_id: str
    timestamp: str
    source: str
    category: str
    severity: Literal["low", "medium", "high", "critical"]
    description: str
    observed_behavior: str
    reproduction_steps: list[str] = field(default_factory=list)
    sandboxed: bool = False
    classification: Literal["benign", "accidental", "malicious", "unknown"] = "unknown"
    detection_rule_created: bool = False
    sentinel_created: bool = False
    status: Literal["observed", "isolated", "classified", "sentinelized", "closed"] = "observed"


@dataclass
class SentinelRule:
    name: str
    sentinel_type: SentinelType
    purpose: str
    trigger: str
    response: str
    monitoring_target: str
    action: str


IMMUINE_SYSTEM_DIRECTIVE = """
Software Immune System Directive

The system must not punish or trap real traffic on production systems.
Instead, suspicious activity, malformed input, and recurring failures should be:
- detected
- isolated
- redirected to a controlled sandbox
- observed
- classified
- converted into detection rules
- converted into sentinels
- converted into permanent defensive capabilities

No incident should be discarded.
Every incident must become learning data.
The goal is not punishment.
The goal is intelligence collection, protection, and prevention.
"""


def create_incident_record(
    *,
    incident_id: str,
    timestamp: str,
    source: str,
    category: str,
    severity: Literal["low", "medium", "high", "critical"],
    description: str,
    observed_behavior: str,
    reproduction_steps: list[str] | None = None,
    sandboxed: bool = False,
    classification: Literal["benign", "accidental", "malicious", "unknown"] = "unknown",
    detection_rule_created: bool = False,
    sentinel_created: bool = False,
    status: Literal["observed", "isolated", "classified", "sentinelized", "closed"] = "observed",
) -> IncidentRecord:
    return IncidentRecord(
        incident_id=incident_id,
        timestamp=timestamp,
        source=source,
        category=category,
        severity=severity,
        description=description,
        observed_behavior=observed_behavior,
        reproduction_steps=reproduction_steps or [],
        sandboxed=sandboxed,
        classification=classification,
        detection_rule_created=detection_rule_created,
        sentinel_created=sentinel_created,
        status=status,
    )


def build_ocr_friction_sentinel() -> SentinelRule:
    return SentinelRule(
        name="ocr_friction_sentinel",
        sentinel_type=SentinelType.OCR_FRICTION,
        purpose="Detect suspicious automated OCR or high-friction extraction behaviors and slow or redirect them into monitored environments.",
        trigger="Pattern matches repeated automated OCR attempts, suspicious extraction bursts, or unverifiable input behavior.",
        response="Increase verification requirements, add extra analysis steps, require human review, slow the request, and redirect to a sandboxed environment.",
        monitoring_target="ocr_and_input_processing",
        action="warning + redirect + human review",
    )


def build_syntax_eater_sentinel() -> SentinelRule:
    return SentinelRule(
        name="syntax_eater_sentinel",
        sentinel_type=SentinelType.SYNTAX_EATER,
        purpose="Take malformed syntax, classify it, match historical errors, and propose repair options before failure spreads.",
        trigger="Syntax error, malformed parser input, invalid JSON/YAML/XML, or malformed code structure.",
        response="Classify the syntax issue, match to historical patterns, suggest repair candidates, validate them, and create a detection rule.",
        monitoring_target="code_and_parser_inputs",
        action="repair + classification + detection rule",
    )


def build_failure_immunity_sentinel() -> SentinelRule:
    return SentinelRule(
        name="failure_immunity_sentinel",
        sentinel_type=SentinelType.FAILURE_IMMUNITY,
        purpose="Ensure every failure becomes a record, a regression test, and a defensive capability.",
        trigger="Any failure, malformed event, or recurring bad behavior appears in the system.",
        response="Store the event, reproduce it in isolation, classify it, convert it to a test and detection rule, and create a monitor.",
        monitoring_target="all_system_failures",
        action="record + test + monitor + training example",
    )


def build_attack_isolation_sentinel() -> SentinelRule:
    return SentinelRule(
        name="attack_isolation_sentinel",
        sentinel_type=SentinelType.ATTACK_ISOLATION,
        purpose="Separate malicious or suspicious traffic from production, route it to a controlled environment, and collect intelligence without harming real systems.",
        trigger="Suspicious automated behavior, exploit pattern, abusive input, or a likely malicious sequence.",
        response="Route to sandbox, collect indicators, classify the threat, and create new detection rules.",
        monitoring_target="external_inputs_and_untrusted_traffic",
        action="isolate + sandbox + intelligence collection",
    )


def convert_incident_to_defense(record: IncidentRecord) -> dict[str, Any]:
    return {
        "incident_id": record.incident_id,
        "stored": True,
        "sandboxed": record.sandboxed,
        "classification": record.classification,
        "detection_rule": "Create a new detection rule for the observed pattern.",
        "regression_test": "Create a regression test that reproduces the event in isolation.",
        "sentinel": "Create a dedicated sentinel for the recurring pattern.",
        "training_example": "Use the incident as a permanent learning artifact.",
    }


def build_sentinel_layer() -> dict[str, Any]:
    return {
        "directive": IMMUINE_SYSTEM_DIRECTIVE,
        "sentinels": [
            build_ocr_friction_sentinel(),
            build_syntax_eater_sentinel(),
            build_failure_immunity_sentinel(),
            build_attack_isolation_sentinel(),
        ],
        "pipeline": [
            "Detection",
            "Isolation",
            "Decoy Environment",
            "Observation",
            "Intelligence Collection",
            "Detection Rule",
            "Sentinel",
            "Prevention",
        ],
    }
