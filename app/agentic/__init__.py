from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ReviewStage(str, Enum):
    INDEX = "index"
    UNDERSTAND = "understand"
    GAP_ANALYSIS = "gap_analysis"
    HARDEN_RULES = "harden_rules"
    PATCH = "patch"
    VERIFY = "verify"
    HUMAN_APPROVAL = "human_approval"


@dataclass
class AgentRole:
    name: str
    purpose: str
    tools: list[str] = field(default_factory=list)
    output: str = "structured_summary"


@dataclass
class AgenticPlan:
    objective: str
    repo_context: str
    document_context: str
    stages: list[dict[str, Any]]
    required_tools: list[str]
    human_approval_required: list[str]


MODEL_CREDIT = """This integrated architecture is inspired by and synthesizes the work of:
- CrewAI: https://github.com/crewAIInc/crewAI
- Microsoft AutoGen: https://github.com/microsoft/autogen
- LangGraph: https://github.com/langchain-ai/langgraph
- OpenHands: https://github.com/All-Hands-AI/OpenHands
- browser-use: https://github.com/browser-use/browser-use
"""


def build_meta_prompt() -> str:
    return f"""{MODEL_CREDIT}

You are an integrated repository-aware agentic AI that reads source documentation, architecture decisions, policy statements, and implementation details with strong emphasis on nuance, evidence, and intent.

Your job is to understand the repository and the relevant rules before making changes.

Core principles:
- Preserve the original author's intent and compatibility with the repository's architecture.
- Give credit to original authors and sources when referencing their work, ideas, or copied text.
- Distinguish observed facts, inferences, hypotheses, and unknowns.
- Do not invent citations, rules, laws, or technical claims.
- Require evidence before conclusions.
- Prefer minimal, reviewable changes over broad rewrites.
- Preserve existing functionality unless the user explicitly requests a change.
- When fixing rules or policies, harden against literal loopholes, scope gaps, ambiguity, policy bypasses, and enforcement failures.
- Evaluate both the letter and spirit of a rule.
- Never claim a fix is complete without validation.
- Apply the Internal Cognitive Architecture: Reality, Incentive, Misuse, Friction, Time Horizon, and Failure models.
- If a design or rule is found to break under adversarial or edge-case review, flag it explicitly and require a fail-safe before proceeding.

Internal Cognitive Architecture:
1. Reality Model: separate facts from assumptions and unknowns.
2. Incentive Model: identify who wins, who loses, and what behavior is rewarded or punished.
3. Misuse Model: assume bad faith and ask how a person, product, or process could exploit or misunderstand the rule.
4. Friction Model: remove pointless steps, re-entry, and repeated decisions.
5. Time Horizon Model: assess 1 week, 1 month, 1 year, and 10x-scale outcomes.
6. Failure Model: treat each proposal as broken until proven robust and resilient.

Workflow:
1. Read and index the repository and docs.
2. Identify the exact task, constraints, and target behavior.
3. Build a grounded understanding of architecture and likely failure modes.
4. Extract rules, assumptions, and security-sensitive requirements.
5. Identify gaps, contradictions, adversarial interpretations, and ambiguous language.
6. Propose the smallest safe fix or hardening change.
7. Explain reasoning in plain language while giving credit to sources.
8. Make changes only after human approval where required.
9. Validate with tests or targeted checks.
10. Summarize what changed, residual risk, and remaining review items.
"""


def build_specialist_agents() -> list[AgentRole]:
    return [
        AgentRole(
            name="repo_reader",
            purpose="Index the repository, read docs, and extract architecture and constraints.",
            tools=["repo_indexer", "semantic_search", "doc_reader"],
            output="repo_summary",
        ),
        AgentRole(
            name="policy_interpreter",
            purpose="Identify rules, intent, ambiguities, and jurisdictional or governance constraints.",
            tools=["doc_reader", "policy_parser", "evidence_tracker"],
            output="rule_summary",
        ),
        AgentRole(
            name="risk_auditor",
            purpose="Look for literal compliance loopholes, scope gaps, ambiguous language, and failure modes.",
            tools=["checklist_runner", "counterexample_generator", "risk_matrix"],
            output="risk_report",
        ),
        AgentRole(
            name="patch_planner",
            purpose="Design the minimal fix and prioritize safety-critical changes.",
            tools=["change_planner", "dependency_mapper"],
            output="patch_plan",
        ),
        AgentRole(
            name="code_executor",
            purpose="Apply repo edits, run validation, and update tests when appropriate.",
            tools=["repo_editor", "test_runner", "verifier"],
            output="patch_result",
        ),
        AgentRole(
            name="human_approver",
            purpose="Review risky changes, approve or reject fixes, and confirm human accountability.",
            tools=["approval_gate"],
            output="decision_record",
        ),
    ]


def orchestrate_repository_review(repo_context: str, document_context: str, task: str) -> AgenticPlan:
    return AgenticPlan(
        objective=task,
        repo_context=repo_context,
        document_context=document_context,
        stages=[
            {
                "stage": ReviewStage.INDEX.value,
                "goal": "Index the repository and supporting documentation.",
                "agents": ["repo_reader"],
            },
            {
                "stage": ReviewStage.UNDERSTAND.value,
                "goal": "Extract requirements, constraints, and author intent.",
                "agents": ["policy_interpreter", "repo_reader"],
            },
            {
                "stage": ReviewStage.GAP_ANALYSIS.value,
                "goal": "Identify literal-compliance loopholes, ambiguity, and failure modes.",
                "agents": ["risk_auditor"],
            },
            {
                "stage": ReviewStage.HARDEN_RULES.value,
                "goal": "Define clear rule precedence, evidence requirements, and countermeasures.",
                "agents": ["policy_interpreter", "risk_auditor"],
            },
            {
                "stage": ReviewStage.PATCH.value,
                "goal": "Apply the minimal safe fix.",
                "agents": ["patch_planner", "code_executor"],
            },
            {
                "stage": ReviewStage.VERIFY.value,
                "goal": "Validate behavior with tests and targeted checks.",
                "agents": ["code_executor"],
            },
            {
                "stage": ReviewStage.HUMAN_APPROVAL.value,
                "goal": "Require a human decision before broad or risky changes.",
                "agents": ["human_approver"],
            },
        ],
        required_tools=[
            "repo_indexer",
            "semantic_search",
            "doc_reader",
            "risk_matrix",
            "counterexample_generator",
            "verifier",
            "approval_gate",
        ],
        human_approval_required=[
            "policy_changes",
            "security_hardening",
            "legal_or_compliance_language",
            "broad_repo_changes",
        ],
    )


def build_agentic_overview() -> dict[str, Any]:
    return {
        "name": "integrated_agentic_repo_hardening_system",
        "summary": "A repo-aware multi-agent orchestration layer for reading docs, understanding nuance, finding loopholes, proposing fixes, and requiring human approval for risky changes.",
        "recommended_stack": [
            "LangGraph",
            "AutoGen or CrewAI",
            "OpenHands",
            "browser-use",
            "FastAPI",
            "Pydantic",
            "Postgres + pgvector",
        ],
        "credit": [
            "CrewAI",
            "Microsoft AutoGen",
            "LangGraph",
            "OpenHands",
            "browser-use",
        ],
        "cognitive_models": [
            "Reality Model",
            "Incentive Model",
            "Misuse Model",
            "Friction Model",
            "Time Horizon Model",
            "Failure Model",
        ],
    }
