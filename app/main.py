from __future__ import annotations

from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.config import settings
from app.data.synthetic_corpus import AUTHORITY_CORPUS
from app.db import init_db
from app.services.analysis import build_50_question_audit, produce_findings, retrieve_authorities, summarize_report
from app.services.ingestion import ingest_upload

app = FastAPI(title=settings.app_name)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def startup() -> None:
    await init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.app_name})


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.post("/api/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    document_type: str = Form("policy"),
    jurisdiction: str = Form("US"),
    review_date: str = Form("2026-10-23"),
    analysis_scope: str = Form("full-document"),
) -> JSONResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="A file is required.")

    upload_result = await ingest_upload(file, settings.upload_max_bytes)
    if not upload_result["text"].strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the uploaded file.")

    authorities = retrieve_authorities(jurisdiction, review_date, ["notice", "record", "purpose", "owner", "policy"])
    if not authorities:
        return JSONResponse({
            "status": "incomplete",
            "message": "No applicable authority was found for the selected jurisdiction and review date.",
            "findings": [],
            "audit": build_50_question_audit("document-1", jurisdiction, review_date).model_dump(mode="json"),
            "report_text": "No applicable authority was found for the selected jurisdiction and review date.",
        })

    findings = produce_findings("document-1", upload_result["text"], jurisdiction, review_date)
    audit = build_50_question_audit("document-1", jurisdiction, review_date)
    audit.findings = findings
    audit.overall_status = "supported_issue" if findings else "adequate_for_tested_scope"
    report_text = summarize_report({
        "document_hash": upload_result["document_hash"],
        "jurisdiction": jurisdiction,
        "review_date": review_date,
    }, findings, audit)

    payload = {
        "status": "ok",
        "document_hash": upload_result["document_hash"],
        "warnings": upload_result["warnings"],
        "authorities_found": len(authorities),
        "findings": [finding.model_dump(mode="json") for finding in findings],
        "audit": audit.model_dump(mode="json"),
        "report_text": report_text,
    }
    return JSONResponse(payload)
