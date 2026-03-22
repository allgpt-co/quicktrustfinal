"""Models for automated control test execution."""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class ControlTestDefinition(BaseModel):
    """Defines an automated test for a control — maps control to a collector check."""
    __tablename__ = "control_test_definitions"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    collector_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # which collector to use (e.g., okta_mfa_enrollment, aws_iam_mfa_report)
    assertion_field: Mapped[str] = mapped_column(String(255), nullable=False)
    # JSON path in result to check (e.g., "data.compliant", "data.mfa_coverage")
    assertion_operator: Mapped[str] = mapped_column(String(20), nullable=False, default="eq")
    # eq, neq, gt, gte, lt, lte, contains, not_contains, exists
    assertion_value: Mapped[str] = mapped_column(String(500), nullable=False)
    # expected value (e.g., "true", "100", "enabled")
    schedule: Mapped[str] = mapped_column(String(20), default="daily")
    # hourly, daily, weekly
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    integration_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("integrations.id")
    )

    organization = relationship("Organization", lazy="selectin")
    control = relationship("Control", lazy="selectin")
    integration = relationship("Integration", lazy="selectin")
    results = relationship(
        "ControlTestResult", back_populates="test_definition",
        cascade="all, delete-orphan", lazy="selectin",
        order_by="ControlTestResult.created_at.desc()",
    )


class ControlTestResult(BaseModel):
    """Records the result of a single control test execution."""
    __tablename__ = "control_test_results"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    test_definition_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("control_test_definitions.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id"), nullable=False, index=True
    )
    result: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    # pass, fail, error, skipped
    actual_value: Mapped[str | None] = mapped_column(String(500))
    expected_value: Mapped[str] = mapped_column(String(500), nullable=False)
    evidence_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("evidence.id")
    )
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    details: Mapped[dict | None] = mapped_column(JSONType())
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    test_definition = relationship("ControlTestDefinition", back_populates="results")
    control = relationship("Control", lazy="selectin")
    evidence = relationship("Evidence", lazy="selectin")
    organization = relationship("Organization", lazy="selectin")
