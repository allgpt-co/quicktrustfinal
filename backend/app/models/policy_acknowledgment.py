import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class PolicyAcknowledgment(BaseModel):
    __tablename__ = "policy_acknowledgments"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    policy_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("policies.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), nullable=False
    )
    policy_version: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, acknowledged, overdue
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str | None] = mapped_column(String(45))
    notes: Mapped[str | None] = mapped_column(Text)

    policy = relationship("Policy", lazy="selectin")
