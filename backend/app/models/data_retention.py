"""Data retention policy and GDPR deletion request models."""

import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, GUID


class DataRetentionPolicy(BaseModel):
    """Per-org configurable data retention rules.

    Example: "Delete audit_logs older than 730 days" →
        entity_type="audit_logs", retention_days=730
    """

    __tablename__ = "data_retention_policies"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    retention_days: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True)


class DeletionRequest(BaseModel):
    """GDPR right-to-erasure request tracking.

    status flow: pending → processing → completed / failed
    """

    __tablename__ = "deletion_requests"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    requested_by: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False
    )
    target_user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )
    reason: Mapped[str | None] = mapped_column(String(1000))
    completed_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
