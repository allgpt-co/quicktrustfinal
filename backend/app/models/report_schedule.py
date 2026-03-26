"""Scheduled report delivery configuration."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class ReportSchedule(BaseModel):
    __tablename__ = "report_schedules"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)  # compliance_summary, risk_report, etc.
    frequency: Mapped[str] = mapped_column(String(50), nullable=False)  # weekly, monthly
    day_of_week: Mapped[int] = mapped_column(Integer, default=0)  # 0=Monday
    recipients: Mapped[dict | None] = mapped_column(JSONType(), default=list)  # list of email addresses
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    organization = relationship("Organization", lazy="selectin")
