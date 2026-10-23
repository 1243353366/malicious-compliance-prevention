from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal


class SentinelType(str, Enum):
    OCR_FRICTION = "ocr_friction"
    SYNTAX_EATER = "syntax_eater"
    FAILURE_IMMUNITY = "failure_immunity"
    ATTACK_ISOLATION = "attack_isolation"
    RESOURCE_TARPIT = "resource_tarpit"
    DDoS_GUARD = "ddos_guard"
    PROMPT_INJECTION = "prompt_injection"
    DEPENDENCY = "dependency"


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
    content_hash: str = ""


@dataclass
class SentinelRule:
    name: str
    sentinel_type: SentinelType
    purpose: str
    trigger: str
    response: str
    monitoring_target: str
    action: str
    content_hash: str = ""


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

The architecture has three responsibilities:
- Python = brain: reasoning, orchestration, analysis, repair planning, pattern recognition
- Go = nervous system: real-time detection, rate limiting, traffic classification, anomaly detection, enforcement
- SQL = memory: failures, attacks, sentinels, behavior patterns, repair patterns, threat scores

No incident should be discarded.
Every incident must become learning data.
The goal is not punishment.
The goal is intelligence collection, protection, and prevention.

High-friction decoy design:
When suspicious automated behavior is detected, the system should consume the attacker's resources instead of the real system's resources.
This means slowing automated requests, increasing work cost, and redirecting activity into a monitored sandbox where the attacker burns time, tokens, CPU, or bandwidth without impacting legitimate users.

DDoS defense principle:
Attack
→ classify
→ throttle
→ cache
→ challenge
→ isolate
→ redirect to decoy
→ collect intelligence
→ learn and harden

Final safeguard:
Every incident, sentinel, and defensive artifact must carry a deterministic SHA-256 fingerprint.
This prevents mutation, tampering, and silent drift in the intelligence layer and ensures all defensive knowledge can be verified before use.
"""


def compute_sha256(data: str | bytes) -> str:
    if isinstance(data, str):
        payload = data.encode("utf-8")
    else:
        payload = data
    return hashlib.sha256(payload).hexdigest()


def canonicalize_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def bind_content_hash_to_record(record: IncidentRecord) -> IncidentRecord:
    payload = canonicalize_json(
        {
            "incident_id": record.incident_id,
            "timestamp": record.timestamp,
            "source": record.source,
            "category": record.category,
            "severity": record.severity,
            "description": record.description,
            "observed_behavior": record.observed_behavior,
            "reproduction_steps": record.reproduction_steps,
            "sandboxed": record.sandboxed,
            "classification": record.classification,
            "detection_rule_created": record.detection_rule_created,
            "sentinel_created": record.sentinel_created,
            "status": record.status,
        }
    )
    record.content_hash = compute_sha256(payload)
    return record


def verify_record_hash(record: IncidentRecord, expected_hash: str) -> bool:
    return record.content_hash == expected_hash and record.content_hash


def bind_content_hash_to_rule(rule: SentinelRule) -> SentinelRule:
    payload = canonicalize_json(
        {
            "name": rule.name,
            "sentinel_type": rule.sentinel_type,
            "purpose": rule.purpose,
            "trigger": rule.trigger,
            "response": rule.response,
            "monitoring_target": rule.monitoring_target,
            "action": rule.action,
        }
    )
    rule.content_hash = compute_sha256(payload)
    return rule


def verify_rule_hash(rule: SentinelRule, expected_hash: str) -> bool:
    return rule.content_hash == expected_hash and rule.content_hash


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
    record = IncidentRecord(
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
    return bind_content_hash_to_record(record)


def build_python_brain_summary() -> dict[str, list[str]]:
    return {
        "roles": [
            "Builder Agent",
            "Adversary Agent",
            "Historian Agent",
            "Auditor Agent",
            "Psychology Agent",
        ],
        "responsibilities": [
            "reasoning",
            "agent orchestration",
            "LLM interactions",
            "failure analysis",
            "pattern recognition",
            "sentinel generation",
            "risk scoring",
        ],
    }


def build_go_guardian_summary() -> dict[str, list[str]]:
    return {
        "responsibilities": [
            "connection monitoring",
            "rate limiting",
            "traffic classification",
            "request analysis",
            "behavior analysis",
            "anomaly detection",
            "real-time enforcement",
        ],
        "pipeline": [
            "internet",
            "go_gateway",
            "python_intelligence",
            "sql_memory",
        ],
    }


def build_sql_memory_schema() -> dict[str, list[str]]:
    return {
        "tables": [
            "failures",
            "attacks",
            "sentinels",
            "behavior_patterns",
            "repair_patterns",
            "threat_scores",
            "historical_incidents",
        ],
        "example_columns": [
            "failure_id",
            "failure_type",
            "input",
            "output",
            "environment",
            "repair",
            "test_case",
            "sentinel_generated",
        ],
    }


def build_ocr_friction_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="ocr_friction_sentinel",
        sentinel_type=SentinelType.OCR_FRICTION,
        purpose="Detect suspicious automated OCR or high-friction extraction behaviors and slow or redirect them into monitored environments.",
        trigger="Pattern matches repeated automated OCR attempts, suspicious extraction bursts, or unverifiable input behavior.",
        response="Increase verification requirements, add extra analysis steps, require human review, slow the request, and redirect to a sandboxed environment.",
        monitoring_target="ocr_and_input_processing",
        action="warning + redirect + human review + resource burn",
    )
    return bind_content_hash_to_rule(rule)


def build_syntax_eater_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="syntax_eater_sentinel",
        sentinel_type=SentinelType.SYNTAX_EATER,
        purpose="Take malformed syntax, classify it, match historical errors, and propose repair options before failure spreads.",
        trigger="Syntax error, malformed parser input, invalid JSON/YAML/XML, or malformed code structure.",
        response="Classify the syntax issue, match to historical patterns, suggest repair candidates, validate them, and create a detection rule.",
        monitoring_target="code_and_parser_inputs",
        action="repair + classification + detection rule",
    )
    return bind_content_hash_to_rule(rule)


def build_failure_immunity_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="failure_immunity_sentinel",
        sentinel_type=SentinelType.FAILURE_IMMUNITY,
        purpose="Ensure every failure becomes a record, a regression test, and a defensive capability.",
        trigger="Any failure, malformed event, or recurring bad behavior appears in the system.",
        response="Store the event, reproduce it in isolation, classify it, convert it to a test and detection rule, and create a monitor.",
        monitoring_target="all_system_failures",
        action="record + test + monitor + training example",
    )
    return bind_content_hash_to_rule(rule)


def build_attack_isolation_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="attack_isolation_sentinel",
        sentinel_type=SentinelType.ATTACK_ISOLATION,
        purpose="Separate malicious or suspicious traffic from production, route it to a controlled environment, and collect intelligence without harming real systems.",
        trigger="Suspicious automated behavior, exploit pattern, abusive input, or a likely malicious sequence.",
        response="Route to sandbox, collect indicators, classify the threat, and create new detection rules.",
        monitoring_target="external_inputs_and_untrusted_traffic",
        action="isolate + sandbox + intelligence collection",
    )
    return bind_content_hash_to_rule(rule)


def build_resource_tarpit_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="resource_tarpit_sentinel",
        sentinel_type=SentinelType.RESOURCE_TARPIT,
        purpose="Force suspicious actors to burn their own resources in a monitored environment instead of consuming production resources.",
        trigger="Repeated failed auth, excessive automation, bot-like patterns, suspicious volume, or exploit attempts.",
        response="Introduce computational friction: slow requests, expand challenge cost, delay token generation, route to a decoy system, and increase verification steps while preserving real service availability.",
        monitoring_target="abuse_signals_and_suspicious_automation",
        action="delay + challenge + sandbox + cost amplification",
    )
    return bind_content_hash_to_rule(rule)


def build_ddos_guard_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="ddos_guard_sentinel",
        sentinel_type=SentinelType.DDoS_GUARD,
        purpose="Protect the system from volumetric abuse by classifying traffic and escalating cost before it reaches critical infrastructure.",
        trigger="Traffic spike, abnormal request rate, bot signature, or repeat request pattern.",
        response="Throttle traffic, clear cache aggressively, challenge suspicious clients, and isolate abusive sources from production.",
        monitoring_target="network_and_http_traffic",
        action="classify + throttle + challenge + isolate",
    )
    return bind_content_hash_to_rule(rule)


def build_prompt_injection_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="prompt_injection_sentinel",
        sentinel_type=SentinelType.PROMPT_INJECTION,
        purpose="Identify I/O manipulation, adversarial prompts, and prompt injection patterns before they impact the model or downstream systems.",
        trigger="Adversarial prompt structure, role-override attempts, context poisoning signals, or prompt manipulation heuristics.",
        response="Block suspicious payloads, quarantine prompt context, and generate reclassification rules for future runs.",
        monitoring_target="model_inputs_and_prompts",
        action="sanitize + quarantine + detect + learn",
    )
    return bind_content_hash_to_rule(rule)


def build_dependency_sentinel() -> SentinelRule:
    rule = SentinelRule(
        name="dependency_sentinel",
        sentinel_type=SentinelType.DEPENDENCY,
        purpose="Detect dependency drift, vulnerable versions, and unsafe package changes before they become production issues.",
        trigger="Version mismatch, package drift, vulnerable library signatures, or risky dependency changes.",
        response="Flag the dependency, recommend an upgrade or pin, generate a repair plan, and create a monitoring signal for future drift detection.",
        monitoring_target="dependency_manifest_and_runtime_environment",
        action="scan + alert + repair plan + monitor",
    )
    return bind_content_hash_to_rule(rule)


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
        "resource_tarpit": "Route suspicious activity into a controlled decoy that consumes attacker effort instead of production capacity.",
        "sha256_fingerprint": record.content_hash,
    }


def build_sentinel_layer() -> dict[str, Any]:
    sentinels = [
        build_ocr_friction_sentinel(),
        build_syntax_eater_sentinel(),
        build_failure_immunity_sentinel(),
        build_attack_isolation_sentinel(),
        build_resource_tarpit_sentinel(),
        build_ddos_guard_sentinel(),
        build_prompt_injection_sentinel(),
        build_dependency_sentinel(),
    ]
    return {
        "directive": IMMUINE_SYSTEM_DIRECTIVE,
        "sentinels": sentinels,
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
        "final_safeguard": "sha256_fingerprint_required_for_all_incidents_and_sentinels",
        "system_layers": {
            "python": build_python_brain_summary(),
            "go": build_go_guardian_summary(),
            "sql": build_sql_memory_schema(),
        },
    }
