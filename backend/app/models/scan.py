"""Database models for security scanner results and findings."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class ScanResult(BaseModel):
    """Represents a single scan execution (e.g. one Trivy run on an image)."""
    __tablename__ = "scan_results"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    scanner: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # trivy, semgrep, gitleaks, checkov, zap, nuclei
    scan_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # container, sast, secrets, iac, dast, template
    target: Mapped[str] = mapped_column(String(500), nullable=False)
    # docker image, repo path, URL, etc.
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True)
    # pending, running, completed, failed
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    total_findings: Mapped[int] = mapped_column(Integer, default=0)
    critical_count: Mapped[int] = mapped_column(Integer, default=0)
    high_count: Mapped[int] = mapped_column(Integer, default=0)
    medium_count: Mapped[int] = mapped_column(Integer, default=0)
    low_count: Mapped[int] = mapped_column(Integer, default=0)
    info_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    raw_output_url: Mapped[str | None] = mapped_column(String(1000))
    config: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    triggered_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )

    organization = relationship("Organization", lazy="selectin")
    findings = relationship(
        "ScanFinding", back_populates="scan_result",
        cascade="all, delete-orphan", lazy="selectin",
    )


class ScanFinding(BaseModel):
    """Individual vulnerability or issue found by a scanner."""
    __tablename__ = "scan_findings"

    scan_result_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("scan_results.id", ondelete="CASCADE"), nullable=False
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    scanner: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    # critical, high, medium, low, info
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(1000))
    # file path, image layer, URL, etc.
    line_number: Mapped[int | None] = mapped_column(Integer)
    rule_id: Mapped[str | None] = mapped_column(String(255))
    # CVE-2024-XXXX, semgrep rule id, etc.
    cve_id: Mapped[str | None] = mapped_column(String(255))
    cwe_id: Mapped[str | None] = mapped_column(String(500))
    remediation: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="open", index=True)
    # open, acknowledged, resolved, false_positive
    package_name: Mapped[str | None] = mapped_column(String(255))
    package_version: Mapped[str | None] = mapped_column(String(100))
    fixed_version: Mapped[str | None] = mapped_column(String(100))
    confidence: Mapped[str | None] = mapped_column(String(20))
    # high, medium, low (for SAST tools)
    extra_data: Mapped[dict | None] = mapped_column(JSONType(), default=dict)

    scan_result = relationship("ScanResult", back_populates="findings")
