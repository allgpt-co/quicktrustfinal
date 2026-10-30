"""Immutable consumption receipts and transactionally maintained period totals."""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import GUID

KINDS = ("LLM_COMPLETION", "EMBEDDING", "VECTOR_QUERY", "VECTOR_UPSERT", "STORAGE_BYTES",
         "EMAIL", "QUESTION_ANSWERED", "QUESTION_MATCHED", "QUESTIONNAIRE_PROCESSED")
PERIOD_SOURCES = ("subscription", "calendar_month", "legacy_calendar_month")


class PeriodColumns:
    org_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("organizations.id"), nullable=False)
    kind: Mapped[str] = mapped_column(String(40), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_source: Mapped[str] = mapped_column(String(30), nullable=False)


class UsageEvent(PeriodColumns, Base):
    __tablename__ = "usage_events"
    __table_args__ = (
        UniqueConstraint("org_id", "kind", "idempotency_key", name="uq_usage_event_key"),
        Index("ix_usage_events_org_occurred", "org_id", "occurred_at"),
        CheckConstraint("period_end > period_start", name="ck_usage_event_period"),
        CheckConstraint("quantity >= 0 OR kind = 'STORAGE_BYTES'", name="ck_usage_event_quantity"),
        CheckConstraint("cost_micros IS NULL OR cost_micros >= 0", name="ck_usage_event_cost"),
        CheckConstraint("prompt_tokens IS NULL OR prompt_tokens >= 0", name="ck_usage_event_prompt"),
        CheckConstraint("completion_tokens IS NULL OR completion_tokens >= 0", name="ck_usage_event_completion"),
        CheckConstraint(f"kind IN {KINDS}", name="ck_usage_event_kind"),
        CheckConstraint(f"period_source IN {PERIOD_SOURCES}", name="ck_usage_event_period_source"),
    )
    id: Mapped[UUID] = mapped_column(GUID(), primary_key=True, default=uuid4)
    idempotency_key: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[UUID | None] = mapped_column(GUID())
    source_type: Mapped[str] = mapped_column(String(40), nullable=False)
    source_id: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    prompt_tokens: Mapped[int | None] = mapped_column(BigInteger)
    completion_tokens: Mapped[int | None] = mapped_column(BigInteger)
    cost_micros: Mapped[int | None] = mapped_column(BigInteger)
    is_mock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class UsageCounter(PeriodColumns, Base):
    __tablename__ = "usage_counters"
    __table_args__ = (
        UniqueConstraint("org_id", "kind", "period_start", "period_end", "period_source", name="uq_usage_counter_period"),
        Index("ix_usage_counters_org_period", "org_id", "period_start"),
        CheckConstraint("period_end > period_start", name="ck_usage_counter_period"),
        CheckConstraint("quantity >= 0 OR kind = 'STORAGE_BYTES'", name="ck_usage_counter_quantity"),
        CheckConstraint("event_count >= 0 AND known_prompt_tokens >= 0 AND known_completion_tokens >= 0 AND known_cost_micros >= 0 AND unknown_token_events >= 0 AND unpriced_events >= 0", name="ck_usage_counter_totals"),
        CheckConstraint(f"kind IN {KINDS}", name="ck_usage_counter_kind"),
        CheckConstraint(f"period_source IN {PERIOD_SOURCES}", name="ck_usage_counter_period_source"),
    )
    id: Mapped[UUID] = mapped_column(GUID(), primary_key=True, default=uuid4)
    event_count: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    known_prompt_tokens: Mapped[int] = mapped_column(BigInteger, nullable=False)
    known_completion_tokens: Mapped[int] = mapped_column(BigInteger, nullable=False)
    known_cost_micros: Mapped[int] = mapped_column(BigInteger, nullable=False)
    unknown_token_events: Mapped[int] = mapped_column(BigInteger, nullable=False)
    unpriced_events: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
