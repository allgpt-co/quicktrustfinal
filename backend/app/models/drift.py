"""Models for configuration drift detection."""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class DriftBaseline(BaseModel):
    """Stores the 'known good' state for a specific resource (control, integration, scan)."""
    __tablename__ = "drift_baselines"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # scan, integration, control
    resource_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False, index=True)
    baseline_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    # SHA-256 of the baseline data
    baseline_data: Mapped[dict | None] = mapped_column(JSONType())
    # snapshot of the baseline state
    finding_count: Mapped[int] = mapped_column(Integer, default=0)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization = relationship("Organization", lazy="selectin")
    events = relationship(
        "DriftEvent", back_populates="baseline",
        cascade="all, delete-orphan", lazy="selectin",
    )


class DriftEvent(BaseModel):
    """Records a detected change from the baseline."""
    __tablename__ = "drift_events"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    baseline_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("drift_baselines.id", ondelete="CASCADE"), nullable=False
    )
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)
    drift_type: Mapped[str] = mapped_column(String(30), nullable=False)
    # new_finding, resolved_finding, config_change, regression
    severity: Mapped[str] = mapped_column(String(20), default="medium")
    # critical, high, medium, low, info
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    previous_value: Mapped[dict | None] = mapped_column(JSONType())
    current_value: Mapped[dict | None] = mapped_column(JSONType())
    status: Mapped[str] = mapped_column(String(30), default="open", index=True)
    # open, acknowledged, resolved, accepted
    acknowledged_by: Mapped[uuid.UUID | None] = mapped_column(GUID())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    baseline = relationship("DriftBaseline", back_populates="events")
    organization = relationship("Organization", lazy="selectin")
