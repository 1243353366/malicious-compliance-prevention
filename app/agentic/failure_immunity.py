from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal


class FailureCategory(str, Enum):
    SYNTAX = "syntax"
    COMPILATION = "compilation"
    RUNTIME = "runtime"
    LOGIC = "logic"
    STATE = "state"
    SECURITY = "security"
    DATA = "data"
    INFRASTRUCTURE = "infrastructure"
    HUMAN = "human"
    AI = "ai"


@dataclass
class FailureRecord:
    failure_id: str
    timestamp: str
    severity: Literal["low", "medium", "high", "critical"]
    component: str
    category: FailureCategory
    description: str
    reproduction_steps: list[str] = field(default_factory=list)
    trigger: str = ""
    expected_behavior: str = ""
    actual_behavior: str = ""
    risk_level: Literal["low", "medium", "high", "critical"] = "medium"
    exploitability: str = "unknown"
    repair_strategy: str = ""
    sentinel_created: bool = False
    status: Literal["open", "reproduced", "fixed", "sentinelized"] = "open"


@dataclass
class SentinelRule:
    name: str
    description: str
    monitor_target: str
    signal: str
    response: str
    action: Literal["test", "monitor", "warning", "repair_rule", "training_example"]


FAILURE_CATEGORIES = {
    FailureCategory.SYNTAX: [
        "missing semicolon",
        "missing brace",
        "invalid indentation",
        "unclosed quotes",
        "malformed JSON",
        "malformed XML",
        "malformed YAML",
        "improper escaping",
        "invalid regex",
        "reserved keyword misuse",
    ],
    FailureCategory.COMPILATION: [
        "missing dependency",
        "type mismatch",
        "unknown symbol",
        "circular dependency",
        "interface mismatch",
        "version conflict",
        "build script failure",
        "invalid import",
    ],
    FailureCategory.RUNTIME: [
        "null pointer",
        "none reference",
        "segmentation fault",
        "memory corruption",
        "stack overflow",
        "infinite recursion",
        "infinite loop",
        "unexpected exception",
        "unhandled exception",
    ],
    FailureCategory.LOGIC: [
        "wrong output",
        "incorrect assumptions",
        "boundary errors",
        "false positives",
        "false negatives",
        "calculation errors",
        "broken business logic",
    ],
    FailureCategory.STATE: [
        "race condition",
        "deadlock",
        "resource starvation",
        "state corruption",
        "lost updates",
        "ordering violations",
    ],
    FailureCategory.SECURITY: [
        "injection",
        "privilege escalation",
        "path traversal",
        "credential leaks",
        "authentication bypass",
        "authorization bypass",
        "session hijacking",
        "csrf",
        "ssrf",
        "deserialization issues",
    ],
    FailureCategory.DATA: [
        "corrupted records",
        "duplicate records",
        "lost records",
        "invalid transformations",
        "parsing failures",
        "schema mismatch",
    ],
    FailureCategory.INFRASTRUCTURE: [
        "network partition",
        "container crash",
        "dns failure",
        "api outage",
        "disk full",
        "cpu exhaustion",
        "memory exhaustion",
    ],
    FailureCategory.HUMAN: [
        "wrong configuration",
        "accidental deletion",
        "misunderstood prompt",
        "bad requirements",
        "documentation gaps",
    ],
    FailureCategory.AI: [
        "hallucinations",
        "prompt injection",
        "context poisoning",
        "unauthorized reasoning paths",
        "goal drift",
        "over-optimization",
        "false confidence",
    ],
}


IMMUINE_SYSTEM_DIRECTIVE = """
Observe Failure
→ Store Failure
→ Reproduce Failure
→ Classify Failure
→ Determine Risk
→ Convert Failure into Test
→ Convert Failure into Sentinel
→ Prevent Reoccurrence

The crucial insight:
Every bug should become an asset.
A bug should never die.
It should either become:
- A test
- A monitor
- A repair rule
- A warning system
- A training example

The goal is not bug fixing.
The goal is bug domestication.
Every failure is captured, classified, studied, and transformed into a permanent defensive capability.
"""


def classify_failure(description: str, hints: list[str] | None = None) -> FailureCategory:
    text = (description + " " + " ".join(hints or [])).lower()
    for category, examples in FAILURE_CATEGORIES.items():
        for example in examples:
            if example in text:
                return category
    return FailureCategory.LOGIC


def build_failure_record(
    *,
    failure_id: str,
    timestamp: str,
    component: str,
    description: str,
    severity: Literal["low", "medium", "high", "critical"],
    reproduction_steps: list[str] | None = None,
    trigger: str = "",
    expected_behavior: str = "",
    actual_behavior: str = "",
    risk_level: Literal["low", "medium", "high", "critical"] = "medium",
    exploitability: str = "unknown",
    repair_strategy: str = "",
    status: Literal["open", "reproduced", "fixed", "sentinelized"] = "open",
) -> FailureRecord:
    return FailureRecord(
        failure_id=failure_id,
        timestamp=timestamp,
        severity=severity,
        component=component,
        category=classify_failure(description, reproduction_steps or []),
        description=description,
        reproduction_steps=reproduction_steps or [],
        trigger=trigger,
        expected_behavior=expected_behavior,
        actual_behavior=actual_behavior,
        risk_level=risk_level,
        exploitability=exploitability,
        repair_strategy=repair_strategy,
        sentinel_created=False,
        status=status,
    )


def create_sentinel_for_failure(record: FailureRecord) -> SentinelRule:
    return SentinelRule(
        name=f"{record.component.replace(' ', '_').lower()}_{record.category.value}_sentinel",
        description=f"Monitor repeated {record.category.value} failures in {record.component}.",
        monitor_target=record.component,
        signal=f"{record.category.value} failure pattern observed: {record.description}",
        response=f"Create warning, capture reproduction artifact, run validation, and route to repair workflow.",
        action="monitor",
    )


def convert_failure_to_assets(record: FailureRecord) -> dict[str, Any]:
    sentinel = create_sentinel_for_failure(record)
    return {
        "failure_id": record.failure_id,
        "database_record": True,
        "reproducible_artifact": bool(record.reproduction_steps),
        "regression_test": "Create regression test for the observed failure path.",
        "sentinel": sentinel,
        "repair_rule": record.repair_strategy or "Add explicit validation and guardrail before deployment.",
        "warning_system": "Emit warning when the failure signature reappears.",
        "training_example": f"Use {record.category.value} failure as a learning example for future prevention.",
    }


def build_failure_taxonomy() -> dict[str, Any]:
    return {
        "directive": IMMUINE_SYSTEM_DIRECTIVE,
        "categories": {key.value: value for key, value in FAILURE_CATEGORIES.items()},
        "pipeline": [
            "Observe Failure",
            "Store Failure",
            "Reproduce Failure",
            "Classify Failure",
            "Determine Risk",
            "Convert Failure into Test",
            "Convert Failure into Sentinel",
            "Prevent Reoccurrence",
        ],
    }


def build_failure_database_summary(records: list[FailureRecord]) -> dict[str, Any]:
    category_counts: dict[str, int] = {}
    for record in records:
        category_counts[record.category.value] = category_counts.get(record.category.value, 0) + 1
    return {
        "failure_count": len(records),
        "category_counts": category_counts,
        "policy": "No failure may be discarded. Every failure must become a record, a test, a safeguard, or an intelligence asset.",
    }
