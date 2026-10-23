from __future__ import annotations

import hashlib
import re
from pathlib import Path

from docx import Document as DocxDocument
import fitz

ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def validate_upload(filename: str, content_type: str | None, file_size: int, max_size: int) -> list[str]:
    warnings: list[str] = []
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {filename}")
    if file_size > max_size:
        raise ValueError(f"File exceeds maximum size of {max_size} bytes")
    if content_type and content_type not in {"text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}:
        warnings.append(f"Content-Type mismatch: {content_type}")
    return warnings


def compute_hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_txt_text(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def extract_pdf_text(data: bytes) -> str:
    try:
        doc = fitz.open(stream=data, filetype="pdf")
        fragments: list[str] = []
        for page in doc:
            text = page.get_text()
            fragments.append(text)
        return "\n".join(fragments)
    except Exception as exc:  # pragma: no cover - fail closed for parse issues
        raise ValueError(f"PDF extraction failed: {exc}") from exc


def extract_docx_text(data: bytes) -> str:
    try:
        import io

        doc = DocxDocument(io.BytesIO(data))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
    except Exception as exc:  # pragma: no cover - fail closed
        raise ValueError(f"DOCX extraction failed: {exc}") from exc


def extract_document_text(filename: str, data: bytes) -> tuple[str, list[str]]:
    suffix = Path(filename).suffix.lower()
    warnings: list[str] = []
    if suffix == ".txt":
        text = extract_txt_text(data)
    elif suffix == ".pdf":
        text = extract_pdf_text(data)
    elif suffix == ".docx":
        text = extract_docx_text(data)
    else:
        raise ValueError(f"Unsupported file type: {filename}")

    if len(text.strip()) < 20:
        warnings.append("Extracted text is unusually short; confirm the document was not blank or OCR is needed.")

    return text, warnings


def split_into_clauses(document_text: str) -> list[str]:
    clauses = re.split(r"(?=\n\s*(?:[0-9]+[.\)]|[A-Z][A-Za-z0-9 ,;()\-]{3,}:|Section|Part|Clause))", document_text)
    cleaned = [clause.strip() for clause in clauses if clause.strip()]
    return cleaned


def detect_defined_terms(document_text: str) -> list[str]:
    matches = re.findall(r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b\s+means\s+", document_text)
    return matches


def detect_broad_language(document_text: str) -> list[str]:
    phrases = ["reasonable", "appropriate", "as needed", "may", "where practicable", "to the extent permitted"]
    matches = [p for p in phrases if p.lower() in document_text.lower()]
    return matches
