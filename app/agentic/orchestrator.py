from __future__ import annotations

from app.agentic.orchestrator import build_meta_prompt, build_specialist_agents, MODEL_CREDIT


def list_specialist_agents() -> list[dict[str, str | list[str]]]:
    agents = []
    for role in build_specialist_agents():
        agents.append(
            {
                "name": role.name,
                "purpose": role.purpose,
                "tools": role.tools,
                "output": role.output,
            }
        )
    return agents


def get_meta_prompt() -> str:
    return build_meta_prompt()


def get_credit() -> str:
    return MODEL_CREDIT
