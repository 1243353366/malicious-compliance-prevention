from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from app.agentic import AgentTaskRequest
from app.agentic.models import build_agentic_plan
from app.agentic.orchestrator import build_agentic_overview


app = FastAPI(title="malicious-compliance-prevention")


@app.get("/api/agentic/overview")
async def get_agentic_overview() -> dict:
    return build_agentic_overview()


@app.post("/api/agentic/plan")
async def generate_agentic_plan(request: AgentTaskRequest) -> dict:
    return build_agentic_plan(request).model_dump(mode="json")
