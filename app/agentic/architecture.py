from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AgentRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str
    summary: str
    why_it_matters: str


class IntegratedAgentArchitecture(BaseModel):
    model_config = ConfigDict(extra="forbid")
    orchestrator: str = "LangGraph"
    specialist_agents: list[str] = [
        "Repo Reader",
        "Policy Interpreter",
        "Risk Auditor",
        "Patch Planner",
        "Code Executor",
        "Human Approver",
    ]
    supporting_frameworks: list[str] = [
        "CrewAI",
        "Microsoft AutoGen",
        "OpenHands",
        "browser-use",
    ]
    recommended_for: str = "Repository understanding, rule hardening, and human-supervised remediation."
    credit: list[str] = [
        "CrewAI",
        "Microsoft AutoGen",
        "LangGraph",
        "OpenHands",
        "browser-use",
    ]
