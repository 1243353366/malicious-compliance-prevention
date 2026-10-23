from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

from fastapi import UploadFile

from app.schemas import extract_document_text, validate_upload


def compute_file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


async def ingest_upload(upload: UploadFile, max_size: int) -> dict:
    content = await upload.read()
    warnings = validate_upload(upload.filename or "unknown", upload.content_type, len(content), max_size)
    text, extraction_warnings = extract_document_text(upload.filename or "unknown", content)
    warnings.extend(extraction_warnings)
    return {
        "document_hash": compute_file_hash(content),
        "document_type": Path(upload.filename or "unknown").suffix.lower().lstrip("."),
        "text": text,
        "warnings": warnings,
    }


def list_authority_types() -> Iterable[str]:
    return [
        "statute",
        "regulation",
        "binding_judicial_decision",
        "persuasive_judicial_decision",
        "official_agency_guidance",
        "contractual_obligation",
        "internal_policy",
        "approved_drafting_standard",
        "secondary_commentary",
    ]
