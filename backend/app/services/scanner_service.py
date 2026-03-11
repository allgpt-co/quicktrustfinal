"""Business logic for security scanner operations."""
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select, func, desc, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan import ScanResult, ScanFinding
from app.scanners import SCANNER_REGISTRY
from app.scanners.base import ScanOutput

logger = logging.getLogger(__name__)


async def trigger_scan(
    db: AsyncSession,
    org_id: UUID,
    scanner_name: str,
    target: str,
    config: dict | None = None,
    triggered_by: UUID | None = None,
) -> ScanResult:
    """Create a scan record and return it.

    The actual scan execution happens in a background task.
    """
    if scanner_name not in SCANNER_REGISTRY:
        raise ValueError(f"Unknown scanner: {scanner_name}. Available: {list(SCANNER_REGISTRY.keys())}")

    scanner_cls = SCANNER_REGISTRY[scanner_name]
    scan = ScanResult(
        org_id=org_id,
        scanner=scanner_name,
        scan_type=scanner_cls.scan_type,
        target=target,
        status="pending",
        config=config or {},
        triggered_by=triggered_by,
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    return scan


async def execute_scan(scan_id: UUID, org_id: UUID) -> dict:
    """Execute a scan in the background. Called by the task runner."""
    from app.core.database import bg_async_session

    async with bg_async_session() as db:
        scan = await db.get(ScanResult, scan_id)
        if not scan:
            logger.error("Scan %s not found", scan_id)
            return {"error": "Scan not found"}

        scanner_name = scan.scanner
        if scanner_name not in SCANNER_REGISTRY:
            scan.status = "failed"
            scan.error_message = f"Unknown scanner: {scanner_name}"
            await db.commit()
            return {"error": scan.error_message}

        scanner = SCANNER_REGISTRY[scanner_name]()
        scan.status = "running"
        scan.started_at = datetime.now(timezone.utc)
        await db.commit()

        try:
            output: ScanOutput = await scanner.run(scan.target, scan.config)

            scan.completed_at = datetime.now(timezone.utc)
            scan.duration_seconds = output.duration_seconds

            if output.error:
                scan.status = "failed"
                scan.error_message = output.error[:2000]
            else:
                scan.status = "completed"

            counts = output.severity_counts
            scan.total_findings = len(output.findings)
            scan.critical_count = counts["critical"]
            scan.high_count = counts["high"]
            scan.medium_count = counts["medium"]
            scan.low_count = counts["low"]
            scan.info_count = counts["info"]

            # Persist findings
            for f in output.findings:
                finding = ScanFinding(
                    scan_result_id=scan.id,
                    org_id=org_id,
                    scanner=scanner_name,
                    severity=f["severity"],
                    title=f["title"][:500],
                    description=f.get("description"),
                    location=(f.get("location") or "")[:1000] or None,
                    line_number=f.get("line_number"),
                    rule_id=(f.get("rule_id") or "")[:255] or None,
                    cve_id=(f.get("cve_id") or "")[:255] or None,
                    cwe_id=(f.get("cwe_id") or "")[:500] or None,
                    remediation=f.get("remediation"),
                    package_name=(f.get("package_name") or "")[:255] or None,
                    package_version=(f.get("package_version") or "")[:100] or None,
                    fixed_version=(f.get("fixed_version") or "")[:100] or None,
                    confidence=(f.get("confidence") or "")[:20] or None,
                    extra_data=f.get("metadata", {}),
                )
                db.add(finding)

            await db.commit()

            return {
                "scan_id": str(scan.id),
                "status": scan.status,
                "total_findings": scan.total_findings,
                "critical": scan.critical_count,
                "high": scan.high_count,
            }

        except Exception as e:
            logger.error("Scan %s failed: %s", scan_id, e, exc_info=True)
            await db.rollback()
            # Re-fetch scan after rollback to update status
            scan = await db.get(ScanResult, scan_id)
            if scan:
                scan.status = "failed"
                scan.error_message = str(e)[:2000]
                scan.completed_at = datetime.now(timezone.utc)
                await db.commit()
            return {"error": str(e)}


async def list_scans(
    db: AsyncSession,
    org_id: UUID,
    scanner: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[ScanResult], int]:
    """List scan results with optional filters."""
    query = select(ScanResult).where(
        ScanResult.org_id == org_id,
        ScanResult.deleted_at.is_(None),
    )
    count_query = select(func.count(ScanResult.id)).where(
        ScanResult.org_id == org_id,
        ScanResult.deleted_at.is_(None),
    )

    if scanner:
        query = query.where(ScanResult.scanner == scanner)
        count_query = count_query.where(ScanResult.scanner == scanner)
    if status:
        query = query.where(ScanResult.status == status)
        count_query = count_query.where(ScanResult.status == status)

    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(desc(ScanResult.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def list_findings(
    db: AsyncSession,
    org_id: UUID,
    scan_id: UUID | None = None,
    scanner: str | None = None,
    severity: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[ScanFinding], int]:
    """List scan findings with optional filters."""
    query = select(ScanFinding).where(
        ScanFinding.org_id == org_id,
        ScanFinding.deleted_at.is_(None),
    )
    count_query = select(func.count(ScanFinding.id)).where(
        ScanFinding.org_id == org_id,
        ScanFinding.deleted_at.is_(None),
    )

    if scan_id:
        query = query.where(ScanFinding.scan_result_id == scan_id)
        count_query = count_query.where(ScanFinding.scan_result_id == scan_id)
    if scanner:
        query = query.where(ScanFinding.scanner == scanner)
        count_query = count_query.where(ScanFinding.scanner == scanner)
    if severity:
        query = query.where(ScanFinding.severity == severity)
        count_query = count_query.where(ScanFinding.severity == severity)
    if status:
        query = query.where(ScanFinding.status == status)
        count_query = count_query.where(ScanFinding.status == status)

    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(desc(ScanFinding.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def get_scan(db: AsyncSession, org_id: UUID, scan_id: UUID) -> ScanResult | None:
    """Get a single scan result."""
    result = await db.execute(
        select(ScanResult).where(
            ScanResult.id == scan_id,
            ScanResult.org_id == org_id,
            ScanResult.deleted_at.is_(None),
        )
    )
    return result.scalar_one_or_none()


async def update_finding_status(
    db: AsyncSession, org_id: UUID, finding_id: UUID, new_status: str
) -> ScanFinding | None:
    """Update the status of a finding."""
    result = await db.execute(
        select(ScanFinding).where(
            ScanFinding.id == finding_id,
            ScanFinding.org_id == org_id,
        )
    )
    finding = result.scalar_one_or_none()
    if finding:
        finding.status = new_status
        await db.commit()
        await db.refresh(finding)
    return finding


async def _cleanup_stuck_scans(db: AsyncSession, org_id: UUID) -> None:
    """Mark scans stuck in 'running' for >10 minutes as failed."""
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=10)
    await db.execute(
        update(ScanResult)
        .where(
            ScanResult.org_id == org_id,
            ScanResult.status == "running",
            ScanResult.started_at < cutoff,
        )
        .values(status="failed", error_message="Scan timed out")
    )
    await db.commit()


async def get_dashboard(db: AsyncSession, org_id: UUID) -> dict:
    """Get aggregate dashboard data for all scanners."""
    await _cleanup_stuck_scans(db, org_id)

    # Total scans
    total_scans = (await db.execute(
        select(func.count(ScanResult.id)).where(
            ScanResult.org_id == org_id,
            ScanResult.deleted_at.is_(None),
        )
    )).scalar() or 0

    # Open findings by severity
    severity_counts = {}
    for sev in ["critical", "high", "medium", "low", "info"]:
        count = (await db.execute(
            select(func.count(ScanFinding.id)).where(
                ScanFinding.org_id == org_id,
                ScanFinding.severity == sev,
                ScanFinding.status == "open",
                ScanFinding.deleted_at.is_(None),
            )
        )).scalar() or 0
        severity_counts[sev] = count

    total_findings = sum(severity_counts.values())

    # Findings by scanner
    scanner_counts = {}
    for scanner_name in SCANNER_REGISTRY:
        count = (await db.execute(
            select(func.count(ScanFinding.id)).where(
                ScanFinding.org_id == org_id,
                ScanFinding.scanner == scanner_name,
                ScanFinding.status == "open",
                ScanFinding.deleted_at.is_(None),
            )
        )).scalar() or 0
        if count > 0:
            scanner_counts[scanner_name] = count

    # Active scanners (have at least one scan)
    active_scanners_result = await db.execute(
        select(ScanResult.scanner).where(
            ScanResult.org_id == org_id,
            ScanResult.deleted_at.is_(None),
        ).distinct()
    )
    active_scanners = [r[0] for r in active_scanners_result.all()]

    # Recent scans
    recent_result = await db.execute(
        select(ScanResult).where(
            ScanResult.org_id == org_id,
            ScanResult.deleted_at.is_(None),
        ).order_by(desc(ScanResult.created_at)).limit(10)
    )
    recent_scans = list(recent_result.scalars().all())

    return {
        "total_scans": total_scans,
        "total_findings": total_findings,
        "open_findings": total_findings,
        "critical_findings": severity_counts.get("critical", 0),
        "high_findings": severity_counts.get("high", 0),
        "medium_findings": severity_counts.get("medium", 0),
        "low_findings": severity_counts.get("low", 0),
        "scanners_active": active_scanners,
        "recent_scans": recent_scans,
        "findings_by_scanner": scanner_counts,
    }
