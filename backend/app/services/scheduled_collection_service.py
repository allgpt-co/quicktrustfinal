"""Scheduled evidence collection — connects the scheduler to the collection service."""
from __future__ import annotations

import logging
from datetime import datetime, timezone, timedelta
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.integration import Integration
from app.schemas.integration import CollectionTrigger

logger = logging.getLogger(__name__)

_SCHEDULE_INTERVALS: dict[str, timedelta] = {
    "hourly": timedelta(hours=1),
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


async def get_due_integrations(db: AsyncSession) -> list[Integration]:
    """Return integrations whose scheduled collection is due."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(Integration).where(
            Integration.schedule_enabled.is_(True),
            Integration.collection_schedule.isnot(None),
            Integration.schedule_collector_type.isnot(None),
            Integration.deleted_at.is_(None),
            # Due if next_run_at is null (never run) or in the past
            (Integration.next_run_at.is_(None)) | (Integration.next_run_at <= now),
        )
    )
    return list(result.scalars().all())


async def run_scheduled_collections(db: AsyncSession) -> int:
    """Execute all due scheduled collections. Returns count of jobs triggered."""
    from app.services import collection_service

    due = await get_due_integrations(db)
    triggered = 0

    for integration in due:
        try:
            trigger = CollectionTrigger(
                collector_type=integration.schedule_collector_type,
                control_id=integration.schedule_control_id,
            )
            job = await collection_service.trigger_collection(
                db, integration.org_id, integration.id, trigger
            )
            # Calculate next run time
            interval = _SCHEDULE_INTERVALS.get(
                integration.collection_schedule, timedelta(days=1)
            )
            integration.next_run_at = datetime.now(timezone.utc) + interval
            integration.last_schedule_error = None
            await db.commit()
            triggered += 1
            logger.info(
                "Scheduled collection completed for integration %s (job %s, status=%s)",
                integration.id, job.id, job.status,
            )
        except Exception as exc:
            integration.last_schedule_error = str(exc)
            await db.commit()
            logger.error(
                "Scheduled collection failed for integration %s: %s",
                integration.id, exc,
            )

    return triggered


async def enable_schedule(
    db: AsyncSession, org_id: UUID, integration_id: UUID,
    schedule: str, collector_type: str, control_id: UUID | None = None,
) -> Integration:
    """Enable scheduled collection for an integration."""
    result = await db.execute(
        select(Integration).where(
            Integration.id == integration_id,
            Integration.org_id == org_id,
        )
    )
    integration = result.scalar_one_or_none()
    if not integration:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(f"Integration {integration_id} not found")

    integration.collection_schedule = schedule
    integration.schedule_collector_type = collector_type
    integration.schedule_control_id = control_id
    integration.schedule_enabled = True
    integration.next_run_at = datetime.now(timezone.utc)  # Run immediately on next tick
    integration.last_schedule_error = None
    await db.commit()
    await db.refresh(integration)
    return integration


async def disable_schedule(
    db: AsyncSession, org_id: UUID, integration_id: UUID,
) -> Integration:
    """Disable scheduled collection for an integration."""
    result = await db.execute(
        select(Integration).where(
            Integration.id == integration_id,
            Integration.org_id == org_id,
        )
    )
    integration = result.scalar_one_or_none()
    if not integration:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(f"Integration {integration_id} not found")

    integration.schedule_enabled = False
    integration.next_run_at = None
    await db.commit()
    await db.refresh(integration)
    return integration
