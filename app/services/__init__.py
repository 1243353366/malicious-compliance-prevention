from __future__ import annotations

import uuid

from app.data.synthetic_corpus import AUTHORITY_CORPUS


def retrieve_relevant_sources(jurisdiction: str, review_date: str, query_terms: list[str]) -> list[dict]:
    matches: list[dict] = []
    for item in AUTHORITY_CORPUS:
        if item["jurisdiction"] != jurisdiction:
            continue
        if item.get("effective_to") and review_date > item["effective_to"]:
            continue
        if item.get("effective_from") and review_date < item["effective_from"]:
            continue
        text = (item["text"] or "").lower()
        if any(term.lower() in text for term in query_terms):
            matches.append(item)
    return matches


def build_document_locator(location: str, section: str | None = None) -> str:
    return f"{location}:{section}" if section else location


def generate_source_id() -> str:
    return str(uuid.uuid4())
