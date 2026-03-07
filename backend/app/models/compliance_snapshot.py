import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, GUID, JSONType


class ComplianceSnapshot(BaseModel):
    __tablename__ = "compliance_snapshots"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    framework_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("frameworks.id"), nullable=False
    )
    snapshot_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    total_controls: Mapped[int] = mapped_column(Integer, default=0)
    implemented_controls: Mapped[int] = mapped_column(Integer, default=0)
    implementation_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    evidence_coverage_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score_avg: Mapped[float | None] = mapped_column(Float)
    details: Mapped[dict | None] = mapped_column(JSONType())
    triggered_by: Mapped[str] = mapped_column(
        String(50), default="manual"
    )  # manual, scheduled, audit_start
