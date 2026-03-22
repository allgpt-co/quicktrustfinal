"""Drift detection service — compares scan/collection results against baselines."""
from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.drift import DriftBaseline, DriftEvent
from app.models.scan import ScanResult, ScanFinding

logger = logging.getLogger(__name__)


def _hash_data(data: dict | list | None) -> str:
    """Compute a deterministic SHA-256 hash of JSON-serializable data."""
    raw = json.dumps(data or {}, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

async def get_baseline(
    db: AsyncSession, org_id: UUID, resource_type: str, resource_id: UUID,
) -> DriftBaseline | None:
    """Get the active baseline for a resource."""
    result = await db.execute(
        select(DriftBaseline).where(
            DriftBaseline.org_id == org_id,
            DriftBaseline.resource_type == resource_type,
            DriftBaseline.resource_id == resource_id,
            DriftBaseline.is_active.is_(True),
        )
    )
    return result.scalar_one_or_none()


async def create_or_update_baseline(
    db: AsyncSession, org_id: UUID, resource_type: str, resource_id: UUID,
    data: dict, finding_count: int = 0,
) -> DriftBaseline:
    """Create a new baseline or update the existing one."""
    # Deactivate old baseline
    await db.execute(
        update(DriftBaseline).where(
            DriftBaseline.org_id == org_id,
            DriftBaseline.resource_type == resource_type,
            DriftBaseline.resource_id == resource_id,
            DriftBaseline.is_active.is_(True),
        ).values(is_active=False)
    )
    baseline = DriftBaseline(
        org_id=org_id,
        resource_type=resource_type,
        resource_id=resource_id,
        baseline_hash=_hash_data(data),
        baseline_data=data,
        finding_count=finding_count,
        captured_at=datetime.now(timezone.utc),
        is_active=True,
    )
    db.add(baseline)
    await db.flush()
    return baseline


# ---------------------------------------------------------------------------
# Drift detection for scans
# ---------------------------------------------------------------------------

async def detect_scan_drift(
    db: AsyncSession, org_id: UUID, scan_result: ScanResult,
) -> list[DriftEvent]:
    """Compare a new scan result against its baseline and generate drift events."""
    events: list[DriftEvent] = []

    baseline = await get_baseline(db, org_id, "scan", scan_result.id)

    # Build a set of current findings (by title + location as key)
    current_findings: dict[str, ScanFinding] = {}
    for f in scan_result.findings:
        key = f"{f.title}|{f.location or ''}|{f.rule_id or ''}"
        current_findings[key] = f

    if baseline is None:
        # First scan — set this as the baseline, no drift to report
        baseline_data = {
            "scanner": scan_result.scanner,
            "target": scan_result.target,
            "finding_keys": list(current_findings.keys()),
            "total_findings": scan_result.total_findings,
            "critical": scan_result.critical_count,
            "high": scan_result.high_count,
        }
        await create_or_update_baseline(
            db, org_id, "scan", scan_result.id,
            baseline_data, scan_result.total_findings,
        )
        logger.info("Created initial scan baseline for %s (%s)", scan_result.scanner, scan_result.target)
        await db.commit()
        return events

    # Compare against baseline
    previous_keys = set(baseline.baseline_data.get("finding_keys", []))
    current_keys = set(current_findings.keys())

    new_keys = current_keys - previous_keys
    resolved_keys = previous_keys - current_keys

    # New findings
    for key in new_keys:
        finding = current_findings[key]
        event = DriftEvent(
            org_id=org_id,
            baseline_id=baseline.id,
            resource_type="scan",
            resource_id=scan_result.id,
            drift_type="new_finding",
            severity=finding.severity,
            title=f"New {finding.severity} finding: {finding.title}",
            description=finding.description,
            previous_value=None,
            current_value={
                "title": finding.title,
                "location": finding.location,
                "severity": finding.severity,
                "rule_id": finding.rule_id,
            },
        )
        db.add(event)
        events.append(event)

    # Resolved findings
    for key in resolved_keys:
        event = DriftEvent(
            org_id=org_id,
            baseline_id=baseline.id,
            resource_type="scan",
            resource_id=scan_result.id,
            drift_type="resolved_finding",
            severity="info",
            title=f"Finding resolved: {key.split('|')[0]}",
            description=f"This finding was present in the previous scan but is no longer detected.",
            previous_value={"key": key},
            current_value=None,
        )
        db.add(event)
        events.append(event)

    # Check for count regression
    prev_count = baseline.baseline_data.get("total_findings", 0)
    if scan_result.total_findings > prev_count and (scan_result.total_findings - prev_count) >= 3:
        event = DriftEvent(
            org_id=org_id,
            baseline_id=baseline.id,
            resource_type="scan",
            resource_id=scan_result.id,
            drift_type="regression",
            severity="high",
            title=f"Finding count regression: {prev_count} → {scan_result.total_findings}",
            description=f"Total findings increased by {scan_result.total_findings - prev_count} since last baseline.",
            previous_value={"total_findings": prev_count},
            current_value={"total_findings": scan_result.total_findings},
        )
        db.add(event)
        events.append(event)

    # Update baseline with new state
    baseline_data = {
        "scanner": scan_result.scanner,
        "target": scan_result.target,
        "finding_keys": list(current_keys),
        "total_findings": scan_result.total_findings,
        "critical": scan_result.critical_count,
        "high": scan_result.high_count,
    }
    await create_or_update_baseline(
        db, org_id, "scan", scan_result.id,
        baseline_data, scan_result.total_findings,
    )

    if events:
        logger.info(
            "Drift detected for scan %s: %d new, %d resolved, %d total events",
            scan_result.id, len(new_keys), len(resolved_keys), len(events),
        )

    await db.commit()
    return events


# ---------------------------------------------------------------------------
# Drift detection for evidence collection
# ---------------------------------------------------------------------------

async def detect_collection_drift(
    db: AsyncSession, org_id: UUID, integration_id: UUID,
    collector_type: str, result_data: dict,
) -> list[DriftEvent]:
    """Compare collection result against previous baseline."""
    events: list[DriftEvent] = []
    current_hash = _hash_data(result_data.get("data", {}))

    baseline = await get_baseline(db, org_id, "integration", integration_id)

    if baseline is None:
        await create_or_update_baseline(
            db, org_id, "integration", integration_id,
            {"collector_type": collector_type, "data_hash": current_hash, "data": result_data.get("data", {})},
        )
        logger.info("Created initial collection baseline for integration %s", integration_id)
        await db.commit()
        return events

    # If hash changed, configuration drifted
    prev_hash = baseline.baseline_data.get("data_hash", "")
    if current_hash != prev_hash:
        event = DriftEvent(
            org_id=org_id,
            baseline_id=baseline.id,
            resource_type="integration",
            resource_id=integration_id,
            drift_type="config_change",
            severity="medium",
            title=f"Configuration drift detected in {collector_type}",
            description="Collected data differs from the previous baseline. Review changes below.",
            previous_value=baseline.baseline_data.get("data"),
            current_value=result_data.get("data", {}),
        )
        db.add(event)
        events.append(event)

        # Update baseline
        await create_or_update_baseline(
            db, org_id, "integration", integration_id,
            {"collector_type": collector_type, "data_hash": current_hash, "data": result_data.get("data", {})},
        )
        logger.info("Configuration drift detected for integration %s", integration_id)

    await db.commit()
    return events


# ---------------------------------------------------------------------------
# Query drift events
# ---------------------------------------------------------------------------

async def list_drift_events(
    db: AsyncSession, org_id: UUID,
    resource_type: str | None = None,
    status: str | None = None,
    severity: str | None = None,
    page: int = 1, page_size: int = 50,
) -> tuple[list[DriftEvent], int]:
    """List drift events with filters."""
    base_q = select(DriftEvent).where(DriftEvent.org_id == org_id)
    count_q = select(func.count()).select_from(DriftEvent).where(DriftEvent.org_id == org_id)

    if resource_type:
        base_q = base_q.where(DriftEvent.resource_type == resource_type)
        count_q = count_q.where(DriftEvent.resource_type == resource_type)
    if status:
        base_q = base_q.where(DriftEvent.status == status)
        count_q = count_q.where(DriftEvent.status == status)
    if severity:
        base_q = base_q.where(DriftEvent.severity == severity)
        count_q = count_q.where(DriftEvent.severity == severity)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(DriftEvent.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def acknowledge_drift_event(
    db: AsyncSession, org_id: UUID, event_id: UUID, user_id: UUID,
) -> DriftEvent:
    """Mark a drift event as acknowledged."""
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(DriftEvent).where(DriftEvent.id == event_id, DriftEvent.org_id == org_id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise NotFoundError(f"Drift event {event_id} not found")
    event.status = "acknowledged"
    event.acknowledged_by = user_id
    await db.commit()
    await db.refresh(event)
    return event


async def resolve_drift_event(
    db: AsyncSession, org_id: UUID, event_id: UUID,
) -> DriftEvent:
    """Mark a drift event as resolved."""
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(DriftEvent).where(DriftEvent.id == event_id, DriftEvent.org_id == org_id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise NotFoundError(f"Drift event {event_id} not found")
    event.status = "resolved"
    event.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(event)
    return event


async def get_drift_summary(db: AsyncSession, org_id: UUID) -> dict:
    """Get a summary of drift events for the org."""
    total_q = select(func.count()).select_from(DriftEvent).where(DriftEvent.org_id == org_id)
    open_q = total_q.where(DriftEvent.status == "open")
    critical_q = open_q.where(DriftEvent.severity.in_(["critical", "high"]))

    total = (await db.execute(total_q)).scalar() or 0
    open_count = (await db.execute(open_q)).scalar() or 0
    critical_count = (await db.execute(critical_q)).scalar() or 0

    return {
        "total_events": total,
        "open_events": open_count,
        "critical_high_open": critical_count,
    }
