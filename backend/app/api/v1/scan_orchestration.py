"""Scanner orchestration — one-click run all scanners with real execution."""

import logging
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.dependencies import DB, ComplianceUser, VerifiedOrgId
from app.core.task_runner import create_safe_task

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/organizations/{org_id}/scan-orchestration",
    tags=["scan-orchestration"],
)


class OrchestratedScanResponse(BaseModel):
    scan_id: str
    status: str
    scanners_triggered: list[str]
    scanners_skipped: list[str]
    message: str


# Scanners that can run against our own codebase without external credentials
SELF_SCAN_TARGETS = {
    "trivy": {"target": "python:3.12-slim", "config": {}},
    "semgrep": {"target": "/app", "config": {}},
    "gitleaks": {"target": "/app", "config": {}},
    "checkov": {"target": "/app", "config": {}},
}

# Scanners that need external targets/credentials
EXTERNAL_SCANNERS = {
    "zap": {"target": "http://localhost:8000", "config": {}},
    "nuclei": {"target": "http://localhost:8000", "config": {}},
    "prowler": {"target": "default", "config": {}},
}


@router.post("/run-all", response_model=OrchestratedScanResponse)
async def run_all_scanners(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser,
):
    """Trigger all available security scanners with real execution."""
    import uuid as _uuid
    from app.services import scanner_service

    scan_id = str(_uuid.uuid4())
    triggered = []
    skipped = []

    # Run self-scan scanners (these work without external setup)
    for scanner_name, scan_config in SELF_SCAN_TARGETS.items():
        try:
            scan = await scanner_service.trigger_scan(
                db, org_id, scanner_name,
                target=scan_config["target"],
                config={**scan_config["config"], "orchestration_id": scan_id},
                triggered_by=current_user.id,
            )
            # Execute in background
            create_safe_task(
                scanner_service.execute_scan(scan.id, org_id),
                org_id=org_id,
            )
            triggered.append(scanner_name)
            logger.info("Orchestration: triggered %s scan (id=%s)", scanner_name, scan.id)
        except Exception as exc:
            logger.warning("Orchestration: failed to trigger %s: %s", scanner_name, exc)
            skipped.append(f"{scanner_name} (error: {str(exc)[:100]})")

    # Try external scanners (may fail if targets aren't reachable)
    for scanner_name, scan_config in EXTERNAL_SCANNERS.items():
        try:
            scan = await scanner_service.trigger_scan(
                db, org_id, scanner_name,
                target=scan_config["target"],
                config={**scan_config["config"], "orchestration_id": scan_id},
                triggered_by=current_user.id,
            )
            create_safe_task(
                scanner_service.execute_scan(scan.id, org_id),
                org_id=org_id,
            )
            triggered.append(scanner_name)
        except Exception as exc:
            skipped.append(f"{scanner_name} (not available)")

    # Send notification
    try:
        from app.services import alert_engine
        await alert_engine.send_notification(
            db, org_id,
            title="Security Scan Started",
            message=f"Full security scan triggered: {len(triggered)} scanners running. {len(skipped)} skipped.",
            severity="info",
            category="scan_started",
        )
    except Exception:
        pass

    # Publish agent bus event for inter-agent communication
    try:
        from app.services.agent_bus import publish_agent_event
        await publish_agent_event("scan_complete", {
            "org_id": str(org_id),
            "scan_id": scan_id,
            "scanners_triggered": triggered,
        })
    except Exception:
        pass

    return OrchestratedScanResponse(
        scan_id=scan_id,
        status="running",
        scanners_triggered=triggered,
        scanners_skipped=skipped,
        message=f"{len(triggered)} scanners running in background. {len(skipped)} skipped.",
    )


@router.get("/status")
async def get_scan_status(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser,
):
    """Get status of all scanners including last run time and findings."""
    from sqlalchemy import select, func
    from app.models.scan import ScanResult

    all_scanners = list(SELF_SCAN_TARGETS.keys()) + list(EXTERNAL_SCANNERS.keys())
    statuses = []

    for scanner_name in all_scanners:
        result = await db.execute(
            select(ScanResult)
            .where(ScanResult.org_id == org_id, ScanResult.scanner == scanner_name)
            .order_by(ScanResult.created_at.desc())
            .limit(1)
        )
        last_scan = result.scalar_one_or_none()

        count_q = await db.execute(
            select(func.count()).select_from(ScanResult)
            .where(ScanResult.org_id == org_id, ScanResult.scanner == scanner_name)
        )
        total_scans = count_q.scalar() or 0

        statuses.append({
            "scanner": scanner_name,
            "last_status": last_scan.status if last_scan else "never_run",
            "last_run": last_scan.created_at.isoformat() if last_scan and last_scan.created_at else None,
            "last_findings": last_scan.total_findings if last_scan else 0,
            "critical": last_scan.critical_count if last_scan else 0,
            "high": last_scan.high_count if last_scan else 0,
            "total_scans": total_scans,
            "can_self_scan": scanner_name in SELF_SCAN_TARGETS,
        })

    return {"scanners": statuses}
