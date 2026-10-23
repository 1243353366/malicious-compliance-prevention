from __future__ import annotations

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.__init__ import Base


class DocumentRecordModel(Base):
    __tablename__ = "documents"

    document_id: Mapped[str] = mapped_column(String, primary_key=True)
    document_hash: Mapped[str] = mapped_column(String, nullable=False)
    document_type: Mapped[str] = mapped_column(String, nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String, nullable=False)
    review_date: Mapped[str] = mapped_column(Date, nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False, default="1.0")
    ingestion_status: Mapped[str] = mapped_column(String, nullable=False)
    extraction_warnings: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)


class RuleSourceModel(Base):
    __tablename__ = "rule_sources"

    source_id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    authority_type: Mapped[str] = mapped_column(String, nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String, nullable=False)
    citation: Mapped[str | None] = mapped_column(String, nullable=True)
    canonical_url: Mapped[str | None] = mapped_column(String, nullable=True)
    publication_date: Mapped[str | None] = mapped_column(Date, nullable=True)
    effective_from: Mapped[str | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[str | None] = mapped_column(Date, nullable=True)
    source_status: Mapped[str] = mapped_column(String, nullable=False, default="current")
    official_source: Mapped[bool] = mapped_column(String, nullable=False, default=False)
    retrieval_timestamp: Mapped[str] = mapped_column(String, nullable=False)
    content_hash: Mapped[str] = mapped_column(String, nullable=False)
    text_version: Mapped[str] = mapped_column(String, nullable=False)
    source_provenance: Mapped[str] = mapped_column(String, nullable=False)
    relevant_document_categories: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_source_id: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)


class PrincipleModel(Base):
    __tablename__ = "principles"

    principle_id: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    provenance_type: Mapped[str] = mapped_column(String, nullable=False)
    supporting_sources: Mapped[str | None] = mapped_column(Text, nullable=True)
    supporting_quotes: Mapped[str | None] = mapped_column(Text, nullable=True)
    alternative_interpretations: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(String, nullable=False, default=0.0)
    review_status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
