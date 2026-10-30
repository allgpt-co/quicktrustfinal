"""Durable provider-call ledger; references survive questionnaire/job deletion."""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import GUID


class AiUsageEvent(Base):
    __tablename__ = "ai_usage_events"
    __table_args__ = (Index("ix_ai_usage_org_created", "org_id", "created_at"),)

    # One ID per attempted provider invocation; finalization updates this row once.
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    questionnaire_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)
    job_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    batch_index: Mapped[int] = mapped_column(Integer, nullable=False)
    model: Mapped[str | None] = mapped_column(String(255))
    # started = outcome unknown (including crashes); reported = provider usage received.
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="started")
    prompt_tokens: Mapped[int | None] = mapped_column(BigInteger)
    completion_tokens: Mapped[int | None] = mapped_column(BigInteger)
    cost_micros: Mapped[int | None] = mapped_column(BigInteger)
    input_rate_per_million: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    output_rate_per_million: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    recorded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
