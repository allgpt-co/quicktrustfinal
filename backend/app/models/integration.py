import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class Integration(BaseModel):
    __tablename__ = "integrations"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="connected")
    config: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    credentials_ref: Mapped[str | None] = mapped_column(String(500))
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Scheduled collection fields
    collection_schedule: Mapped[str | None] = mapped_column(String(20))
    # hourly, daily, weekly, or null (manual only)
    schedule_collector_type: Mapped[str | None] = mapped_column(String(100))
    # which collector to run on schedule
    schedule_control_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    # optional: link collected evidence to a specific control
    schedule_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_schedule_error: Mapped[str | None] = mapped_column(Text)

    organization = relationship("Organization", back_populates="integrations", lazy="selectin")
    collection_jobs = relationship(
        "CollectionJob", back_populates="integration", lazy="selectin"
    )
