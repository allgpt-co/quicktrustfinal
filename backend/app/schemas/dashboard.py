"""Dashboard aggregation response schemas for Phase 5."""

from pydantic import BaseModel


class FrameworkCompliance(BaseModel):
    framework_id: str
    framework_name: str
    version: str
    total_controls: int
    implemented: int
    partially_implemented: int
    not_implemented: int
    not_applicable: int
    compliance_pct: float


class RiskHeatmapCell(BaseModel):
    likelihood: int
    impact: int
    count: int
    risk_ids: list[str]


class ComplianceTrend(BaseModel):
    date: str
    score: float
    controls_total: int
    controls_implemented: int


class ExecutiveDashboard(BaseModel):
    compliance_score: float
    total_controls: int
    implemented_controls: int
    total_risks: int
    critical_risks: int
    high_risks: int
    open_incidents: int
    p1_incidents: int
    policies_published: int
    policies_total: int
    training_completion_pct: float
    open_alerts: int
    risk_heatmap: list[RiskHeatmapCell]
    compliance_trend: list[ComplianceTrend]
    frameworks: list[FrameworkCompliance]


class EvidenceGap(BaseModel):
    control_id: str
    control_title: str
    status: str
    evidence_count: int
    freshest_evidence_days: int | None


class ComplianceDashboard(BaseModel):
    frameworks: list[FrameworkCompliance]
    total_evidence: int
    fresh_evidence: int
    stale_evidence: int
    evidence_coverage_pct: float
    policies_total: int
    policies_published: int
    policies_draft: int
    pending_acknowledgments: int
    total_acknowledgments: int
    evidence_gaps: list[EvidenceGap]
    compliance_trend: list[ComplianceTrend]


class ScannerSummary(BaseModel):
    scanner_name: str
    total_findings: int
    critical: int
    high: int
    medium: int
    low: int
    last_scan_date: str | None


class VulnerabilityTrend(BaseModel):
    date: str
    critical: int
    high: int
    medium: int
    low: int


class SecurityDashboard(BaseModel):
    total_findings: int
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int
    open_findings: int
    resolved_findings: int
    scanners: list[ScannerSummary]
    vulnerability_trend: list[VulnerabilityTrend]
    open_alerts: int
    total_monitor_rules: int
    active_rules: int


class AuditReadinessBreakdown(BaseModel):
    category: str
    label: str
    score: float
    weight: float
    weighted_score: float
    detail: str


class AuditReadinessDashboard(BaseModel):
    overall_score: float
    breakdown: list[AuditReadinessBreakdown]
    controls_passing_pct: float
    evidence_fresh_pct: float
    policies_acknowledged_pct: float
    risks_treated_pct: float
    training_completion_pct: float
    open_findings: int
    pending_access_reviews: int


class ControlOwnerControl(BaseModel):
    control_id: str
    title: str
    status: str
    evidence_count: int
    evidence_fresh: bool
    days_since_last_evidence: int | None
    framework_name: str | None


class ControlOwnerDashboard(BaseModel):
    total_owned: int
    implemented: int
    needs_attention: int
    controls: list[ControlOwnerControl]
    pending_evidence_uploads: int
    overdue_items: int
