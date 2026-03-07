import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, GUID


class CrossFrameworkMapping(BaseModel):
    __tablename__ = "cross_framework_mappings"

    requirement_a_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("framework_requirements.id"), nullable=False
    )
    requirement_b_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("framework_requirements.id"), nullable=False
    )
    mapping_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # equivalent, partial, related
    notes: Mapped[str | None] = mapped_column(String(1000))
