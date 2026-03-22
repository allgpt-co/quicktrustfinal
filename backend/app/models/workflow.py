"""Durable workflow execution model — persists task state for crash recovery."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class WorkflowExecution(BaseModel):
    """Tracks a long-running background workflow with durable state."""
    __tablename__ = "workflow_executions"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False, index=True
    )
    workflow_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # agent_run, scan, collection, control_test, onboarding
    reference_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    # ID of the related entity (agent_run_id, scan_result_id, etc.)
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True)
    # pending, running, completed, failed, cancelled, retrying
    current_step: Mapped[int] = mapped_column(Integer, default=0)
    total_steps: Mapped[int] = mapped_column(Integer, default=1)
    step_name: Mapped[str | None] = mapped_column(String(255))
    # human-readable name of the current step
    input_data: Mapped[dict | None] = mapped_column(JSONType())
    output_data: Mapped[dict | None] = mapped_column(JSONType())
    error_message: Mapped[str | None] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    triggered_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )

    organization = relationship("Organization", lazy="selectin")
