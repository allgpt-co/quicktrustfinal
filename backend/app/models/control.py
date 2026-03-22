import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class Control(BaseModel):
    __tablename__ = "controls"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("control_templates.id")
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    implementation_details: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    status: Mapped[str] = mapped_column(String(50), default="draft")
    effectiveness: Mapped[str | None] = mapped_column(String(50))
    automation_level: Mapped[str] = mapped_column(String(50), default="manual")
    test_procedure: Mapped[str | None] = mapped_column(Text)
    last_test_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_test_result: Mapped[str | None] = mapped_column(String(50))
    agent_run_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("agent_runs.id")
    )
    # Phase 5: Maturity & Assessment
    maturity_level: Mapped[int | None] = mapped_column(Integer)  # 1-5 CMMI scale
    test_frequency: Mapped[str | None] = mapped_column(String(20))  # quarterly, annually
    next_test_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    findings: Mapped[str | None] = mapped_column(Text)
    remediation_plan: Mapped[str | None] = mapped_column(Text)
    remediation_due: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    organization = relationship("Organization", back_populates="controls", lazy="selectin")
    template = relationship("ControlTemplate", lazy="selectin")
    owner = relationship("User", back_populates="owned_controls", lazy="selectin")
    agent_run = relationship("AgentRun", back_populates="controls", lazy="selectin")
    framework_mappings = relationship(
        "ControlFrameworkMapping", back_populates="control", lazy="selectin"
    )
    evidence = relationship("Evidence", back_populates="control", lazy="selectin")
    risk_mappings = relationship(
        "RiskControlMapping", back_populates="control", lazy="selectin"
    )
