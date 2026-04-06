import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class ApprovalChain(BaseModel):
    __tablename__ = "approval_chains"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    policy_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("policies.id"), nullable=False
    )
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)  # 1, 2, 3...
    approver_role: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # "compliance_manager", "legal", "ciso"
    approver_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True
    )  # specific user or null for role-based
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, approved, rejected
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)

    organization = relationship("Organization", lazy="selectin")
    policy = relationship("Policy", lazy="selectin")
    approver = relationship("User", lazy="selectin")
