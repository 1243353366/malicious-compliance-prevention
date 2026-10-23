from __future__ import annotations

from typing import Any


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
    }
