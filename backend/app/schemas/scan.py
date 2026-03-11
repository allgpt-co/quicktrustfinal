"""Pydantic schemas for security scanner API."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ScanTrigger(BaseModel):
    """Request to trigger a scan."""
    scanner: str = Field(..., description="Scanner type: trivy, semgrep, gitleaks, checkov, zap, nuclei")
    target: str = Field(..., description="Scan target: Docker image, repo path, URL, etc.")
    config: dict | None = Field(default=None, description="Scanner-specific configuration")


class ScanResultResponse(BaseModel):
    id: UUID
    org_id: UUID
    scanner: str
    scan_type: str
    target: str
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    duration_seconds: float | None
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    error_message: str | None
    raw_output_url: str | None
    config: dict | None
    triggered_by: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ScanResultSummary(BaseModel):
    """Lightweight scan result for list views."""
    id: UUID
    scanner: str
    scan_type: str
    target: str
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    duration_seconds: float | None
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ScanFindingResponse(BaseModel):
    id: UUID
    scan_result_id: UUID
    org_id: UUID
    scanner: str
    severity: str
    title: str
    description: str | None
    location: str | None
    line_number: int | None
    rule_id: str | None
    cve_id: str | None
    cwe_id: str | None
    remediation: str | None
    status: str
    package_name: str | None
    package_version: str | None
    fixed_version: str | None
    confidence: str | None
    extra_data: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ScanDashboard(BaseModel):
    """Aggregate stats for the scanner dashboard."""
    total_scans: int = 0
    total_findings: int = 0
    open_findings: int = 0
    critical_findings: int = 0
    high_findings: int = 0
    medium_findings: int = 0
    low_findings: int = 0
    scanners_active: list[str] = []
    recent_scans: list[ScanResultSummary] = []
    findings_by_scanner: dict[str, int] = {}


class FindingStatusUpdate(BaseModel):
    status: str = Field(..., description="New status: open, acknowledged, resolved, false_positive")
