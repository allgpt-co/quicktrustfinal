import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class ControlException(BaseModel):
    __tablename__ = "control_exceptions"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    compensating_control: Mapped[str | None] = mapped_column(Text)
    risk_acceptance: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, approved, denied, expired, revoked
    requested_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    approved_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    denied_by_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    denied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    denial_reason: Mapped[str | None] = mapped_column(Text)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization = relationship("Organization", lazy="selectin")
    control = relationship("Control", lazy="selectin")
    requested_by = relationship("User", foreign_keys=[requested_by_id], lazy="selectin")
    approved_by = relationship("User", foreign_keys=[approved_by_id], lazy="selectin")
    denied_by = relationship("User", foreign_keys=[denied_by_id], lazy="selectin")
