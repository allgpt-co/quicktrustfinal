"""Alert Engine — Evidence freshness, auto-incidents, compliance regression.

Called by the scheduler to detect issues and create alerts/incidents automatically.
"""

import logging
from datetime import datetime, timezone, timedelta
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

# Evidence freshness threshold (days)
DEFAULT_STALENESS_DAYS = 30


async def check_evidence_freshness(db: AsyncSession) -> int:
    """Check all orgs for stale evidence and create alerts. Returns alert count."""
    from app.models.evidence import Evidence
    from app.models.organization import Organization
    from app.services import notification_service

    threshold = datetime.now(timezone.utc) - timedelta(days=DEFAULT_STALENESS_DAYS)
    alerts_created = 0

    # Get all orgs
    orgs = list((await db.execute(select(Organization))).scalars().all())

    for org in orgs:
        # Count stale evidence
        stale_q = select(func.count()).select_from(Evidence).where(
            Evidence.org_id == org.id,
            Evidence.collected_at < threshold,
            Evidence.deleted_at.is_(None),
        )
        stale_count = (await db.execute(stale_q)).scalar() or 0

        if stale_count > 0:
            await notification_service.send_system_notification(
                db=db,
                org_id=org.id,
                category="evidence_freshness",
                title=f"{stale_count} Evidence Items Are Stale",
                message=f"{stale_count} evidence items haven't been collected in {DEFAULT_STALENESS_DAYS}+ days. "
                        f"Stale evidence will be rejected by auditors. Review and re-collect.",
                severity="warning" if stale_count < 10 else "critical",
                entity_type="evidence",
            )
            alerts_created += 1
            logger.info("Org %s: %d stale evidence items flagged", org.id, stale_count)

    return alerts_created


async def check_compliance_regression(db: AsyncSession) -> int:
    """Compare latest compliance snapshots with previous ones. Alert on drops >5%."""
    from app.models.compliance_snapshot import ComplianceSnapshot
    from app.models.organization import Organization
    from app.services import notification_service, incident_service

    alerts_created = 0
    orgs = list((await db.execute(select(Organization))).scalars().all())

    for org in orgs:
        # Get last 2 snapshots per framework
        snapshots_q = (
            select(ComplianceSnapshot)
            .where(ComplianceSnapshot.org_id == org.id)
            .order_by(ComplianceSnapshot.snapshot_date.desc())
            .limit(20)
        )
        snapshots = list((await db.execute(snapshots_q)).scalars().all())

        # Group by framework
        by_framework: dict[str, list] = {}
        for s in snapshots:
            fw_id = str(s.framework_id)
            if fw_id not in by_framework:
                by_framework[fw_id] = []
            by_framework[fw_id].append(s)

        for fw_id, fw_snapshots in by_framework.items():
            if len(fw_snapshots) < 2:
                continue

            latest = fw_snapshots[0]
            previous = fw_snapshots[1]

            latest_pct = latest.implementation_percentage or 0
            previous_pct = previous.implementation_percentage or 0
            drop = previous_pct - latest_pct

            if drop >= 5:  # 5% or more drop
                severity = "critical" if drop >= 15 else "warning"

                await notification_service.send_system_notification(
                    db=db,
                    org_id=org.id,
                    category="compliance_regression",
                    title=f"Compliance Score Dropped {drop:.0f}%",
                    message=f"Compliance score dropped from {previous_pct:.0f}% to {latest_pct:.0f}% "
                            f"(framework {fw_id[:8]}...). Review failing controls immediately.",
                    severity=severity,
                    entity_type="compliance_snapshot",
                    entity_id=str(latest.id),
                )

                # Auto-create incident for significant drops
                if drop >= 10:
                    await _create_auto_incident(
                        db=db,
                        org_id=org.id,
                        title=f"Compliance Regression: Score dropped {drop:.0f}%",
                        description=f"Automated alert: Compliance score dropped from {previous_pct:.0f}% to "
                                    f"{latest_pct:.0f}%. This exceeds the 10% threshold for automatic incident creation.",
                        severity="P2",
                        category="compliance_regression",
                    )

                alerts_created += 1
                logger.warning(
                    "Org %s: Compliance dropped %.0f%% → %.0f%% (framework %s)",
                    org.id, previous_pct, latest_pct, fw_id[:8],
                )

    return alerts_created


async def create_auto_incident_from_finding(
    db: AsyncSession,
    org_id: UUID,
    finding_title: str,
    finding_severity: str,
    scanner_name: str,
    finding_id: str | None = None,
) -> None:
    """Create an incident automatically from a scanner finding."""
    severity_map = {"critical": "P1", "high": "P2", "medium": "P3", "low": "P4"}
    incident_severity = severity_map.get(finding_severity.lower(), "P3")

    # Only auto-create for critical and high
    if incident_severity not in ("P1", "P2"):
        return

    await _create_auto_incident(
        db=db,
        org_id=org_id,
        title=f"[{scanner_name}] {finding_title}",
        description=f"Auto-created from {scanner_name} scanner finding.\n\n"
                    f"Severity: {finding_severity}\n"
                    f"Finding: {finding_title}\n"
                    f"Finding ID: {finding_id or 'N/A'}\n\n"
                    f"This incident was automatically created because the finding severity "
                    f"is {finding_severity}. Review and respond according to your incident "
                    f"response playbook.",
        severity=incident_severity,
        category=f"scanner_{scanner_name.lower()}",
    )


async def create_auto_incident_from_monitor(
    db: AsyncSession,
    org_id: UUID,
    rule_title: str,
    rule_id: str,
    alert_count: int,
) -> None:
    """Create an incident from a monitoring rule failure."""
    await _create_auto_incident(
        db=db,
        org_id=org_id,
        title=f"Monitoring Alert: {rule_title}",
        description=f"Auto-created from monitoring rule failure.\n\n"
                    f"Rule: {rule_title}\n"
                    f"Rule ID: {rule_id}\n"
                    f"Alerts generated: {alert_count}\n\n"
                    f"This incident was automatically created because a monitoring "
                    f"rule detected a compliance issue.",
        severity="P3",
        category="monitoring_alert",
    )


async def _create_auto_incident(
    db: AsyncSession,
    org_id: UUID,
    title: str,
    description: str,
    severity: str,
    category: str,
) -> None:
    """Create an incident with auto-detection metadata."""
    from app.models.incident import Incident, IncidentTimelineEvent

    # Check for duplicate (same title in last 24h)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    existing = await db.execute(
        select(func.count()).select_from(Incident).where(
            Incident.org_id == org_id,
            Incident.title == title,
            Incident.created_at > cutoff,
        )
    )
    if (existing.scalar() or 0) > 0:
        logger.debug("Skipping duplicate auto-incident: %s", title)
        return

    incident = Incident(
        org_id=org_id,
        title=title,
        description=description,
        severity=severity,
        status="open",
        category=category,
        detected_at=datetime.now(timezone.utc),
    )
    db.add(incident)
    await db.flush()

    # Add timeline event
    event = IncidentTimelineEvent(
        incident_id=incident.id,
        event_type="auto_detection",
        description=f"Incident auto-created by QuickTrust alert engine. Category: {category}",
        occurred_at=datetime.now(timezone.utc),
    )
    db.add(event)
    await db.commit()

    # Send notification
    from app.services import notification_service
    await notification_service.send_system_notification(
        db=db,
        org_id=org_id,
        category="auto_incident",
        title=f"Auto-Incident Created: {title}",
        message=f"A {severity} incident was automatically created. Review and respond immediately.",
        severity="critical" if severity in ("P1", "P2") else "warning",
        entity_type="incident",
        entity_id=str(incident.id),
    )

    logger.info("Auto-incident created: %s (org=%s, severity=%s)", title, org_id, severity)


# ---------------------------------------------------------------------------
# Notification helpers (used by other services)
# ---------------------------------------------------------------------------

async def send_notification(
    db: AsyncSession,
    org_id: UUID,
    title: str,
    message: str,
    severity: str = "info",
    category: str = "general",
    user_id: UUID | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
) -> None:
    """Create an in-app notification."""
    from app.services import notification_service
    try:
        await notification_service.send_system_notification(
            db=db, org_id=org_id,
            category=category, title=title, message=message,
            severity=severity,
            entity_type=entity_type, entity_id=entity_id,
            user_id=user_id,
        )
    except Exception as exc:
        logger.warning("Failed to send notification: %s", exc)


async def send_slack_if_configured(
    db: AsyncSession,
    org_id: UUID,
    title: str,
    message: str,
    severity: str = "info",
) -> None:
    """Send a Slack message if the org has a webhook configured."""
    import httpx
    from app.models.notification import SlackWebhookConfig

    try:
        result = await db.execute(
            select(SlackWebhookConfig).where(SlackWebhookConfig.org_id == org_id)
        )
        config = result.scalar_one_or_none()
        if not config or not config.webhook_url:
            return

        color = "#36a64f" if severity == "info" else "#ff9900" if severity == "warning" else "#ff0000"
        payload = {
            "attachments": [{
                "color": color,
                "title": title,
                "text": message,
                "footer": "QuickTrust GRC Platform",
                "ts": int(datetime.now(timezone.utc).timestamp()),
            }]
        }

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(config.webhook_url, json=payload)
            if resp.status_code == 200:
                logger.info("Slack notification sent: %s", title)
            else:
                logger.warning("Slack webhook returned %s", resp.status_code)

    except Exception as exc:
        logger.warning("Failed to send Slack notification: %s", exc)
