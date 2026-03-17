"""Dashboard aggregation service for Phase 5.

Collects data from multiple tables to power the five specialized dashboards.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select, func, case, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.control import Control
from app.models.evidence import Evidence
from app.models.risk import Risk
from app.models.incident import Incident
from app.models.policy import Policy
from app.models.training import TrainingCourse, TrainingAssignment
from app.models.monitoring import MonitorRule, MonitorAlert
from app.models.access_review import AccessReviewCampaign, AccessReviewEntry
from app.models.compliance_snapshot import ComplianceSnapshot
from app.models.control_framework_mapping import ControlFrameworkMapping
from app.models.framework import Framework
from app.models.scan import ScanResult, ScanFinding
from app.schemas.dashboard import (
    ExecutiveDashboard,
    ComplianceDashboard,
    SecurityDashboard,
    AuditReadinessDashboard,
    ControlOwnerDashboard,
    FrameworkCompliance,
    RiskHeatmapCell,
    ComplianceTrend,
    EvidenceGap,
    ScannerSummary,
    VulnerabilityTrend,
    AuditReadinessBreakdown,
    ControlOwnerControl,
)


async def _get_control_stats(db: AsyncSession, org_id: UUID) -> dict:
    """Get basic control statistics."""
    result = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(Control.status == "implemented").label("implemented"),
            func.count().filter(Control.status == "partially_implemented").label("partial"),
            func.count().filter(Control.status == "not_implemented").label("not_impl"),
            func.count().filter(Control.status == "not_applicable").label("na"),
        ).where(Control.org_id == org_id)
    )
    row = result.one()
    total = row.total or 0
    impl = row.implemented or 0
    return {
        "total": total,
        "implemented": impl,
        "partially_implemented": row.partial or 0,
        "not_implemented": row.not_impl or 0,
        "not_applicable": row.na or 0,
        "compliance_pct": round((impl / total * 100), 1) if total > 0 else 0.0,
    }


async def _get_risk_heatmap(db: AsyncSession, org_id: UUID) -> list[RiskHeatmapCell]:
    """Build 5x5 risk heatmap data."""
    result = await db.execute(
        select(Risk.likelihood, Risk.impact, func.count().label("cnt"), func.array_agg(Risk.id).label("ids"))
        .where(Risk.org_id == org_id)
        .group_by(Risk.likelihood, Risk.impact)
    )
    cells = []
    for row in result.all():
        if row.likelihood is not None and row.impact is not None:
            cells.append(RiskHeatmapCell(
                likelihood=row.likelihood,
                impact=row.impact,
                count=row.cnt,
                risk_ids=[str(rid) for rid in (row.ids or [])],
            ))
    return cells


async def _get_compliance_trend(db: AsyncSession, org_id: UUID) -> list[ComplianceTrend]:
    """Get compliance score trend from snapshots."""
    result = await db.execute(
        select(ComplianceSnapshot)
        .where(ComplianceSnapshot.org_id == org_id)
        .order_by(ComplianceSnapshot.created_at.desc())
        .limit(12)
    )
    snapshots = list(result.scalars().all())
    trends = []
    for s in reversed(snapshots):
        score = s.implementation_percentage if s.implementation_percentage else 0.0
        total = s.total_controls if s.total_controls else 0
        impl = s.implemented_controls if s.implemented_controls else 0
        date_str = s.snapshot_date.strftime("%Y-%m-%d") if s.snapshot_date else (
            s.created_at.strftime("%Y-%m-%d") if s.created_at else ""
        )
        trends.append(ComplianceTrend(
            date=date_str,
            score=score,
            controls_total=total,
            controls_implemented=impl,
        ))

    # If no snapshots, generate a single point from current data
    if not trends:
        stats = await _get_control_stats(db, org_id)
        trends.append(ComplianceTrend(
            date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            score=stats["compliance_pct"],
            controls_total=stats["total"],
            controls_implemented=stats["implemented"],
        ))

    return trends


async def _get_frameworks_compliance(db: AsyncSession, org_id: UUID) -> list[FrameworkCompliance]:
    """Get compliance stats per framework."""
    frameworks_result = await db.execute(select(Framework).where(Framework.is_active == True))
    frameworks = list(frameworks_result.scalars().all())

    items = []
    for fw in frameworks:
        # Count controls mapped to this framework
        mapped_q = (
            select(func.count(func.distinct(ControlFrameworkMapping.control_id)))
            .where(ControlFrameworkMapping.framework_id == fw.id)
        )
        total = (await db.execute(mapped_q)).scalar() or 0

        if total == 0:
            items.append(FrameworkCompliance(
                framework_id=str(fw.id),
                framework_name=fw.name,
                version=fw.version or "",
                total_controls=0,
                implemented=0,
                partially_implemented=0,
                not_implemented=0,
                not_applicable=0,
                compliance_pct=0.0,
            ))
            continue

        # Get status breakdown for mapped controls
        status_q = (
            select(
                Control.status,
                func.count().label("cnt"),
            )
            .join(ControlFrameworkMapping, ControlFrameworkMapping.control_id == Control.id)
            .where(
                ControlFrameworkMapping.framework_id == fw.id,
                Control.org_id == org_id,
            )
            .group_by(Control.status)
        )
        status_result = await db.execute(status_q)
        status_map = {row.status: row.cnt for row in status_result.all()}

        impl = status_map.get("implemented", 0)
        actual_total = sum(status_map.values())
        items.append(FrameworkCompliance(
            framework_id=str(fw.id),
            framework_name=fw.name,
            version=fw.version or "",
            total_controls=actual_total,
            implemented=impl,
            partially_implemented=status_map.get("partially_implemented", 0),
            not_implemented=status_map.get("not_implemented", 0),
            not_applicable=status_map.get("not_applicable", 0),
            compliance_pct=round((impl / actual_total * 100), 1) if actual_total > 0 else 0.0,
        ))

    return items


async def get_executive_dashboard(db: AsyncSession, org_id: UUID) -> ExecutiveDashboard:
    """Aggregate data for the executive dashboard."""
    control_stats = await _get_control_stats(db, org_id)

    # Risks
    risk_result = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(Risk.risk_level == "critical").label("critical"),
            func.count().filter(Risk.risk_level == "high").label("high"),
        ).where(Risk.org_id == org_id)
    )
    risk_row = risk_result.one()

    # Incidents
    incident_result = await db.execute(
        select(
            func.count().filter(Incident.status.in_(["open", "investigating"])).label("open"),
            func.count().filter(
                and_(Incident.status.in_(["open", "investigating"]), Incident.severity.in_(["critical", "high"]))
            ).label("p1"),
        ).where(Incident.org_id == org_id)
    )
    inc_row = incident_result.one()

    # Policies
    policy_result = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(Policy.status == "published").label("published"),
        ).where(Policy.org_id == org_id)
    )
    pol_row = policy_result.one()

    # Training completion
    training_total = (await db.execute(
        select(func.count()).select_from(TrainingAssignment).where(TrainingAssignment.org_id == org_id)
    )).scalar() or 0
    training_completed = (await db.execute(
        select(func.count()).select_from(TrainingAssignment).where(
            TrainingAssignment.org_id == org_id, TrainingAssignment.status == "completed"
        )
    )).scalar() or 0
    training_pct = round((training_completed / training_total * 100), 1) if training_total > 0 else 0.0

    # Monitoring
    open_alerts = (await db.execute(
        select(func.count()).select_from(MonitorAlert).where(
            MonitorAlert.org_id == org_id, MonitorAlert.status == "open"
        )
    )).scalar() or 0

    risk_heatmap = await _get_risk_heatmap(db, org_id)
    compliance_trend = await _get_compliance_trend(db, org_id)
    frameworks = await _get_frameworks_compliance(db, org_id)

    return ExecutiveDashboard(
        compliance_score=control_stats["compliance_pct"],
        total_controls=control_stats["total"],
        implemented_controls=control_stats["implemented"],
        total_risks=risk_row.total or 0,
        critical_risks=risk_row.critical or 0,
        high_risks=risk_row.high or 0,
        open_incidents=inc_row.open or 0,
        p1_incidents=inc_row.p1 or 0,
        policies_published=pol_row.published or 0,
        policies_total=pol_row.total or 0,
        training_completion_pct=training_pct,
        open_alerts=open_alerts,
        risk_heatmap=risk_heatmap,
        compliance_trend=compliance_trend,
        frameworks=frameworks,
    )


async def get_compliance_dashboard(db: AsyncSession, org_id: UUID) -> ComplianceDashboard:
    """Aggregate data for the compliance manager dashboard."""
    frameworks = await _get_frameworks_compliance(db, org_id)

    # Evidence stats
    now = datetime.now(timezone.utc)
    stale_threshold = now - timedelta(days=90)

    total_evidence = (await db.execute(
        select(func.count()).select_from(Evidence).where(Evidence.org_id == org_id)
    )).scalar() or 0

    fresh_evidence = (await db.execute(
        select(func.count()).select_from(Evidence).where(
            Evidence.org_id == org_id,
            Evidence.collected_at >= stale_threshold,
        )
    )).scalar() or 0

    stale_evidence = total_evidence - fresh_evidence

    # Evidence coverage: controls that have at least 1 evidence
    controls_with_evidence = (await db.execute(
        select(func.count(func.distinct(Evidence.control_id)))
        .where(Evidence.org_id == org_id, Evidence.control_id.isnot(None))
    )).scalar() or 0
    total_controls = (await db.execute(
        select(func.count()).select_from(Control)
        .where(Control.org_id == org_id, Control.status != "not_applicable")
    )).scalar() or 0
    evidence_coverage = round((controls_with_evidence / total_controls * 100), 1) if total_controls > 0 else 0.0

    # Policies
    pol_result = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(Policy.status == "published").label("published"),
            func.count().filter(Policy.status == "draft").label("draft"),
        ).where(Policy.org_id == org_id)
    )
    pol = pol_result.one()

    # Policy acknowledgments
    from app.models.policy_acknowledgment import PolicyAcknowledgment
    total_acks = (await db.execute(
        select(func.count()).select_from(PolicyAcknowledgment).where(PolicyAcknowledgment.org_id == org_id)
    )).scalar() or 0
    pending_acks = (await db.execute(
        select(func.count()).select_from(PolicyAcknowledgment).where(
            PolicyAcknowledgment.org_id == org_id, PolicyAcknowledgment.status == "pending"
        )
    )).scalar() or 0

    # Evidence gaps: controls missing or with stale evidence
    gaps_q = (
        select(
            Control.id,
            Control.title,
            Control.status,
            func.count(Evidence.id).label("ev_count"),
            func.max(Evidence.collected_at).label("latest_ev"),
        )
        .outerjoin(Evidence, and_(Evidence.control_id == Control.id, Evidence.org_id == org_id))
        .where(Control.org_id == org_id, Control.status != "not_applicable")
        .group_by(Control.id, Control.title, Control.status)
        .having(
            (func.count(Evidence.id) == 0) |
            (func.max(Evidence.collected_at) < stale_threshold)
        )
        .limit(20)
    )
    gaps_result = await db.execute(gaps_q)
    evidence_gaps = []
    for row in gaps_result.all():
        days = None
        if row.latest_ev:
            days = (now - row.latest_ev).days
        evidence_gaps.append(EvidenceGap(
            control_id=str(row.id),
            control_title=row.title or "",
            status=row.status or "",
            evidence_count=row.ev_count or 0,
            freshest_evidence_days=days,
        ))

    compliance_trend = await _get_compliance_trend(db, org_id)

    return ComplianceDashboard(
        frameworks=frameworks,
        total_evidence=total_evidence,
        fresh_evidence=fresh_evidence,
        stale_evidence=stale_evidence,
        evidence_coverage_pct=evidence_coverage,
        policies_total=pol.total or 0,
        policies_published=pol.published or 0,
        policies_draft=pol.draft or 0,
        pending_acknowledgments=pending_acks,
        total_acknowledgments=total_acks,
        evidence_gaps=evidence_gaps,
        compliance_trend=compliance_trend,
    )


async def get_security_dashboard(db: AsyncSession, org_id: UUID) -> SecurityDashboard:
    """Aggregate data for the security posture dashboard."""
    # Scan findings
    severity_q = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(ScanFinding.severity == "critical").label("critical"),
            func.count().filter(ScanFinding.severity == "high").label("high"),
            func.count().filter(ScanFinding.severity == "medium").label("medium"),
            func.count().filter(ScanFinding.severity == "low").label("low"),
            func.count().filter(ScanFinding.status.in_(["open", "new"])).label("open"),
            func.count().filter(ScanFinding.status.in_(["resolved", "fixed"])).label("resolved"),
        ).where(ScanFinding.org_id == org_id)
    )
    sev = severity_q.one()

    # Scanner breakdown
    scanner_q = await db.execute(
        select(
            ScanResult.scanner,
            func.count(ScanFinding.id).label("total"),
            func.count().filter(ScanFinding.severity == "critical").label("critical"),
            func.count().filter(ScanFinding.severity == "high").label("high"),
            func.count().filter(ScanFinding.severity == "medium").label("medium"),
            func.count().filter(ScanFinding.severity == "low").label("low"),
            func.max(ScanResult.created_at).label("last_scan"),
        )
        .join(ScanFinding, ScanFinding.scan_result_id == ScanResult.id)
        .where(ScanResult.org_id == org_id)
        .group_by(ScanResult.scanner)
    )
    scanners = []
    for row in scanner_q.all():
        scanners.append(ScannerSummary(
            scanner_name=row.scanner or "unknown",
            total_findings=row.total or 0,
            critical=row.critical or 0,
            high=row.high or 0,
            medium=row.medium or 0,
            low=row.low or 0,
            last_scan_date=row.last_scan.strftime("%Y-%m-%d") if row.last_scan else None,
        ))

    # Vulnerability trend (last 8 weeks)
    now = datetime.now(timezone.utc)
    vuln_trend = []
    for i in range(7, -1, -1):
        week_start = now - timedelta(weeks=i + 1)
        week_end = now - timedelta(weeks=i)
        week_q = await db.execute(
            select(
                func.count().filter(ScanFinding.severity == "critical").label("critical"),
                func.count().filter(ScanFinding.severity == "high").label("high"),
                func.count().filter(ScanFinding.severity == "medium").label("medium"),
                func.count().filter(ScanFinding.severity == "low").label("low"),
            ).where(
                ScanFinding.org_id == org_id,
                ScanFinding.created_at >= week_start,
                ScanFinding.created_at < week_end,
            )
        )
        wr = week_q.one()
        vuln_trend.append(VulnerabilityTrend(
            date=week_end.strftime("%Y-%m-%d"),
            critical=wr.critical or 0,
            high=wr.high or 0,
            medium=wr.medium or 0,
            low=wr.low or 0,
        ))

    # Monitoring
    open_alerts = (await db.execute(
        select(func.count()).select_from(MonitorAlert).where(
            MonitorAlert.org_id == org_id, MonitorAlert.status == "open"
        )
    )).scalar() or 0

    total_rules = (await db.execute(
        select(func.count()).select_from(MonitorRule).where(MonitorRule.org_id == org_id)
    )).scalar() or 0

    active_rules = (await db.execute(
        select(func.count()).select_from(MonitorRule).where(
            MonitorRule.org_id == org_id, MonitorRule.is_active == True
        )
    )).scalar() or 0

    return SecurityDashboard(
        total_findings=sev.total or 0,
        critical_findings=sev.critical or 0,
        high_findings=sev.high or 0,
        medium_findings=sev.medium or 0,
        low_findings=sev.low or 0,
        open_findings=sev.open or 0,
        resolved_findings=sev.resolved or 0,
        scanners=scanners,
        vulnerability_trend=vuln_trend,
        open_alerts=open_alerts,
        total_monitor_rules=total_rules,
        active_rules=active_rules,
    )


async def get_audit_readiness_dashboard(db: AsyncSession, org_id: UUID) -> AuditReadinessDashboard:
    """Aggregate data for the audit readiness dashboard."""
    control_stats = await _get_control_stats(db, org_id)

    # Controls passing
    applicable = control_stats["total"] - control_stats["not_applicable"]
    controls_pct = round((control_stats["implemented"] / applicable * 100), 1) if applicable > 0 else 0.0

    # Evidence freshness
    now = datetime.now(timezone.utc)
    stale_threshold = now - timedelta(days=90)
    total_ev = (await db.execute(
        select(func.count()).select_from(Evidence).where(Evidence.org_id == org_id)
    )).scalar() or 0
    fresh_ev = (await db.execute(
        select(func.count()).select_from(Evidence).where(
            Evidence.org_id == org_id, Evidence.collected_at >= stale_threshold
        )
    )).scalar() or 0
    evidence_pct = round((fresh_ev / total_ev * 100), 1) if total_ev > 0 else 0.0

    # Policies acknowledged
    from app.models.policy_acknowledgment import PolicyAcknowledgment
    total_acks = (await db.execute(
        select(func.count()).select_from(PolicyAcknowledgment).where(PolicyAcknowledgment.org_id == org_id)
    )).scalar() or 0
    acked = (await db.execute(
        select(func.count()).select_from(PolicyAcknowledgment).where(
            PolicyAcknowledgment.org_id == org_id, PolicyAcknowledgment.status == "acknowledged"
        )
    )).scalar() or 0
    ack_pct = round((acked / total_acks * 100), 1) if total_acks > 0 else 0.0

    # Risks treated
    total_risks = (await db.execute(
        select(func.count()).select_from(Risk).where(Risk.org_id == org_id)
    )).scalar() or 0
    treated_risks = (await db.execute(
        select(func.count()).select_from(Risk).where(
            Risk.org_id == org_id, Risk.treatment_status.in_(["mitigated", "transferred", "accepted"])
        )
    )).scalar() or 0
    risks_pct = round((treated_risks / total_risks * 100), 1) if total_risks > 0 else 0.0

    # Training completion
    training_total = (await db.execute(
        select(func.count()).select_from(TrainingAssignment).where(TrainingAssignment.org_id == org_id)
    )).scalar() or 0
    training_done = (await db.execute(
        select(func.count()).select_from(TrainingAssignment).where(
            TrainingAssignment.org_id == org_id, TrainingAssignment.status == "completed"
        )
    )).scalar() or 0
    training_pct = round((training_done / training_total * 100), 1) if training_total > 0 else 0.0

    # Open audit findings
    from app.models.audit_finding import AuditFinding
    open_findings = (await db.execute(
        select(func.count()).select_from(AuditFinding).where(
            AuditFinding.org_id == org_id, AuditFinding.status.in_(["open", "in_progress"])
        )
    )).scalar() or 0

    # Pending access reviews
    pending_reviews = (await db.execute(
        select(func.count()).select_from(AccessReviewEntry).where(
            AccessReviewEntry.org_id == org_id, AccessReviewEntry.decision == "pending"
        )
    )).scalar() or 0

    # Weighted score: controls 40%, evidence 30%, policies 20%, risks 10%
    weights = [
        ("controls", "Controls Passing", controls_pct, 0.4),
        ("evidence", "Evidence Freshness", evidence_pct, 0.3),
        ("policies", "Policies Acknowledged", ack_pct, 0.2),
        ("risks", "Risks Treated", risks_pct, 0.1),
    ]

    breakdown = []
    overall = 0.0
    for cat, label, score, weight in weights:
        weighted = round(score * weight, 1)
        overall += weighted
        detail_map = {
            "controls": f"{control_stats['implemented']}/{applicable} controls implemented",
            "evidence": f"{fresh_ev}/{total_ev} evidence items fresh (<90 days)",
            "policies": f"{acked}/{total_acks} policies acknowledged",
            "risks": f"{treated_risks}/{total_risks} risks treated",
        }
        breakdown.append(AuditReadinessBreakdown(
            category=cat,
            label=label,
            score=score,
            weight=weight,
            weighted_score=weighted,
            detail=detail_map[cat],
        ))

    return AuditReadinessDashboard(
        overall_score=round(overall, 1),
        breakdown=breakdown,
        controls_passing_pct=controls_pct,
        evidence_fresh_pct=evidence_pct,
        policies_acknowledged_pct=ack_pct,
        risks_treated_pct=risks_pct,
        training_completion_pct=training_pct,
        open_findings=open_findings,
        pending_access_reviews=pending_reviews,
    )


async def get_control_owner_dashboard(
    db: AsyncSession, org_id: UUID, user_id: UUID
) -> ControlOwnerDashboard:
    """Dashboard for a specific control owner showing their controls."""
    now = datetime.now(timezone.utc)
    stale_threshold = now - timedelta(days=90)

    # Get controls owned by this user (or all if user owns none — fallback to all org controls)
    controls_q = (
        select(
            Control.id,
            Control.title,
            Control.status,
            Control.owner_id,
            func.count(Evidence.id).label("ev_count"),
            func.max(Evidence.collected_at).label("latest_ev"),
        )
        .outerjoin(Evidence, and_(Evidence.control_id == Control.id, Evidence.org_id == org_id))
        .where(Control.org_id == org_id)
        .group_by(Control.id, Control.title, Control.status, Control.owner_id)
        .order_by(Control.title)
    )

    # Try owner-specific first
    owned_q = controls_q.where(Control.owner_id == user_id)
    result = await db.execute(owned_q)
    rows = list(result.all())

    # If no owned controls, show all org controls (limited)
    if not rows:
        result = await db.execute(controls_q.limit(50))
        rows = list(result.all())

    controls = []
    needs_attention = 0
    pending_uploads = 0
    overdue = 0

    for row in rows:
        days = None
        fresh = True
        if row.latest_ev:
            days = (now - row.latest_ev).days
            fresh = days < 90
        elif row.ev_count == 0:
            fresh = False

        if not fresh or row.status not in ("implemented", "not_applicable"):
            needs_attention += 1

        if row.ev_count == 0 and row.status != "not_applicable":
            pending_uploads += 1

        if days is not None and days > 90:
            overdue += 1
        elif row.ev_count == 0 and row.status != "not_applicable":
            overdue += 1

        controls.append(ControlOwnerControl(
            control_id=str(row.id),
            title=row.title or "",
            status=row.status or "draft",
            evidence_count=row.ev_count or 0,
            evidence_fresh=fresh,
            days_since_last_evidence=days,
            framework_name=None,
        ))

    implemented = sum(1 for c in controls if c.status == "implemented")

    return ControlOwnerDashboard(
        total_owned=len(controls),
        implemented=implemented,
        needs_attention=needs_attention,
        controls=controls,
        pending_evidence_uploads=pending_uploads,
        overdue_items=overdue,
    )
