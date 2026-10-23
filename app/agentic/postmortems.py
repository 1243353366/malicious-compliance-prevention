from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class FailurePattern:
    pattern: str
    description: str
    signal: str
    countermeasure: str
    observed_frequency: int = 0


@dataclass
class PostmortemRecord:
    failure_pattern: str
    root_cause: str
    affected_component: str
    detected_at: str
    impact: str
    corrective_action: str
    validated: bool = False


POSTMORTEM_PROMPT = """
Periodic review question:
What mistakes keep repeating?

Over time, the system develops a theory of failure.
Most AI improves from training.
A truly agentic system improves from postmortems.
Just like elite engineering organizations.

The system must continuously inspect recurring failure patterns, classify them, and harden the design against future recurrence.
"""


def build_failure_theory() -> list[FailurePattern]:
    return [
        FailurePattern(
            pattern="assumption_gap",
            description="A plan or system depends on an unstated assumption that later proves false.",
            signal="Missing fact or undocumented assumption is treated as certainty.",
            countermeasure="Separate facts from assumptions; require evidence before moving forward.",
            observed_frequency=0,
        ),
        FailurePattern(
            pattern="incentive_mismatch",
            description="The system rewards the wrong behavior or punishes the right behavior.",
            signal="Short-term metric improvement is achieved at cost to long-term goals.",
            countermeasure="Review incentives and add outcome-based safeguards.",
            observed_frequency=0,
        ),
        FailurePattern(
            pattern="misuse_exploitation",
            description="A legitimate workflow can be abused or gamed in a way that defeats the rule's purpose.",
            signal="People can comply literally while still defeating the underlying objective.",
            countermeasure="Add adversarial tests, boundary controls, and purpose-based validation.",
            observed_frequency=0,
        ),
        FailurePattern(
            pattern="friction_repeat",
            description="Repeated manual work creates fatigue, inconsistency, and failure retries.",
            signal="The same decision or data entry occurs multiple times without value.",
            countermeasure="Remove redundant steps and centralize approvals or decisions.",
            observed_frequency=0,
        ),
        FailurePattern(
            pattern="scale_breakage",
            description="The design works in small cases but fails at higher volume or longer time horizons.",
            signal="Performance or reliability degrades dramatically under increased scale.",
            countermeasure="Run load, edge-case, and long-horizon tests before approval.",
            observed_frequency=0,
        ),
        FailurePattern(
            pattern="failure_containment_gap",
            description="The system lacks containment, rollback, or recovery when a dependency or assumption fails.",
            signal="No safe path exists when a critical dependency disappears.",
            countermeasure="Add isolation, rollback, and operational recovery controls.",
            observed_frequency=0,
        ),
    ]


def record_postmortem(
    failure_pattern: str,
    root_cause: str,
    affected_component: str,
    detected_at: str,
    impact: str,
    corrective_action: str,
    validated: bool = False,
) -> PostmortemRecord:
    return PostmortemRecord(
        failure_pattern=failure_pattern,
        root_cause=root_cause,
        affected_component=affected_component,
        detected_at=detected_at,
        impact=impact,
        corrective_action=corrective_action,
        validated=validated,
    )


def summarize_failure_theory(postmortems: list[PostmortemRecord]) -> dict[str, Any]:
    patterns: dict[str, int] = {}
    for record in postmortems:
        patterns[record.failure_pattern] = patterns.get(record.failure_pattern, 0) + 1
    return {
        "periodic_review_prompt": POSTMORTEM_PROMPT,
        "theory_of_failure": {
            "recurring_patterns": [
                {
                    "pattern": key,
                    "frequency": value,
                }
                for key, value in sorted(patterns.items(), key=lambda item: (-item[1], item[0]))
            ],
        },
        "postmortems": [
            {
                "failure_pattern": record.failure_pattern,
                "root_cause": record.root_cause,
                "affected_component": record.affected_component,
                "detected_at": record.detected_at,
                "impact": record.impact,
                "corrective_action": record.corrective_action,
                "validated": record.validated,
            }
            for record in postmortems
        ],
        "policy": "The system must learn from recurring failures and use postmortems to harden rules, processes, and safeguards before the same failure repeats.",
    }
