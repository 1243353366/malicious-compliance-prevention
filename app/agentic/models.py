from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class AgentTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    repo_context: str = ""
    document_context: str = ""
    task: str = "Understand the repo and harden the relevant rules against adversarial loopholes."


class AgentStageResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    stage: str
    goal: str
    agents: list[str]


class AgenticPlanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    objective: str
    repo_context: str
    document_context: str
    stages: list[AgentStageResult]
    required_tools: list[str]
    human_approval_required: list[str]
    meta_prompt: str
