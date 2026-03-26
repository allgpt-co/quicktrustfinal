import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class Framework(BaseModel):
    __tablename__ = "frameworks"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    previous_version_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("frameworks.id"), nullable=True
    )

    domains = relationship("FrameworkDomain", back_populates="framework", lazy="selectin")
    previous_version = relationship(
        "Framework", remote_side="Framework.id", uselist=False, lazy="selectin"
    )
