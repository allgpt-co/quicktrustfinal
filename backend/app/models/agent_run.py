import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class AgentRun(BaseModel):
    __tablename__ = "agent_runs"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    trigger: Mapped[str] = mapped_column(String(50), default="manual")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    input_data: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    output_data: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    tokens_used: Mapped[int | None] = mapped_column(Integer)

    # AI governance — human-in-the-loop review
    approval_status: Mapped[str] = mapped_column(
        String(50), default="auto"
    )  # auto, pending_review, approved, rejected, modified
    approved_by: Mapped[uuid.UUID | None] = mapped_column(GUID())
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_notes: Mapped[str | None] = mapped_column(Text)
    original_output: Mapped[dict | None] = mapped_column(JSONType())

    # AI quality tracking
    model_version: Mapped[str | None] = mapped_column(String(100))
    prompt_version: Mapped[str | None] = mapped_column(String(50))
    response_time_ms: Mapped[int | None] = mapped_column(Integer)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    cost_usd: Mapped[float | None] = mapped_column(Float)

    organization = relationship("Organization", back_populates="agent_runs", lazy="noload")
    controls = relationship("Control", back_populates="agent_run", lazy="noload")
    policies = relationship("Policy", back_populates="agent_run", lazy="noload")
