from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.compliance_snapshot import ComplianceSnapshot
from app.models.control import Control
from app.models.control_framework_mapping import ControlFrameworkMapping
from app.models.evidence import Evidence


async def create_snapshot(
    db: AsyncSession,
    org_id: UUID,
    framework_id: UUID,
    triggered_by: str = "manual",
) -> ComplianceSnapshot:
    """Compute current compliance posture and save a point-in-time snapshot."""

    # Count total controls mapped to this framework for this org
    total_q = (
        select(func.count(func.distinct(ControlFrameworkMapping.control_id)))
        .join(Control, Control.id == ControlFrameworkMapping.control_id)
        .where(
            ControlFrameworkMapping.framework_id == framework_id,
            Control.org_id == org_id,
        )
    )
    total_controls = (await db.execute(total_q)).scalar() or 0

    # Count implemented controls
    implemented_q = (
        select(func.count(func.distinct(ControlFrameworkMapping.control_id)))
        .join(Control, Control.id == ControlFrameworkMapping.control_id)
        .where(
            ControlFrameworkMapping.framework_id == framework_id,
            Control.org_id == org_id,
            Control.status == "implemented",
        )
    )
    implemented_controls = (await db.execute(implemented_q)).scalar() or 0

    impl_pct = round((implemented_controls / total_controls * 100), 1) if total_controls > 0 else 0.0

    # Evidence coverage: controls with at least one evidence item
    controls_with_evidence_q = (
        select(func.count(func.distinct(ControlFrameworkMapping.control_id)))
        .join(Control, Control.id == ControlFrameworkMapping.control_id)
        .where(
            ControlFrameworkMapping.framework_id == framework_id,
            Control.org_id == org_id,
            Control.id.in_(
                select(Evidence.control_id).where(
                    Evidence.org_id == org_id,
                    Evidence.control_id.isnot(None),
                )
            ),
        )
    )
    controls_with_evidence = (await db.execute(controls_with_evidence_q)).scalar() or 0
    evidence_pct = round((controls_with_evidence / total_controls * 100), 1) if total_controls > 0 else 0.0

    snapshot = ComplianceSnapshot(
        org_id=org_id,
        framework_id=framework_id,
        snapshot_date=datetime.now(timezone.utc),
        total_controls=total_controls,
        implemented_controls=implemented_controls,
        implementation_percentage=impl_pct,
        evidence_coverage_percentage=evidence_pct,
        triggered_by=triggered_by,
        details={
            "controls_with_evidence": controls_with_evidence,
        },
    )
    db.add(snapshot)
    await db.commit()
    await db.refresh(snapshot)
    return snapshot


async def list_snapshots(
    db: AsyncSession,
    org_id: UUID,
    framework_id: UUID | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[ComplianceSnapshot], int]:
    base_q = select(ComplianceSnapshot).where(ComplianceSnapshot.org_id == org_id)
    count_q = select(func.count()).select_from(ComplianceSnapshot).where(
        ComplianceSnapshot.org_id == org_id
    )

    if framework_id:
        base_q = base_q.where(ComplianceSnapshot.framework_id == framework_id)
        count_q = count_q.where(ComplianceSnapshot.framework_id == framework_id)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        ComplianceSnapshot.snapshot_date.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_snapshot(
    db: AsyncSession, org_id: UUID, snapshot_id: UUID
) -> ComplianceSnapshot:
    result = await db.execute(
        select(ComplianceSnapshot).where(
            ComplianceSnapshot.id == snapshot_id,
            ComplianceSnapshot.org_id == org_id,
        )
    )
    snapshot = result.scalar_one_or_none()
    if not snapshot:
        raise NotFoundError(f"ComplianceSnapshot {snapshot_id} not found")
    return snapshot
