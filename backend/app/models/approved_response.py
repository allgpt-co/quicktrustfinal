import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class ApprovedResponse(BaseModel):
    __tablename__ = "approved_responses"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    tags: Mapped[dict | None] = mapped_column(JSONType(), default=list)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    use_count: Mapped[int] = mapped_column(Integer, default=0)

    organization = relationship("Organization", lazy="selectin")
    approver = relationship("User", foreign_keys=[approved_by], lazy="selectin")
