from __future__ import annotations

from app.agentic import AgentTaskRequest, AgenticPlanResponse
from app.agentic.orchestrator import build_meta_prompt, orchestrate_repository_review


def build_agentic_plan(request: AgentTaskRequest) -> AgenticPlanResponse:
    plan = orchestrate_repository_review(
        repo_context=request.repo_context,
        document_context=request.document_context,
        task=request.task,
    )
    return AgenticPlanResponse(
        objective=plan.objective,
        repo_context=plan.repo_context,
        document_context=plan.document_context,
        stages=[
            AgentStageResult(
                stage=item["stage"],
                goal=item["goal"],
                agents=item["agents"],
            )
            for item in plan.stages
        ],
        required_tools=plan.required_tools,
        human_approval_required=plan.human_approval_required,
        meta_prompt=build_meta_prompt(),
    )
