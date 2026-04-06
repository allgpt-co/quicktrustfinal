"""Credential rotation — tracks and alerts on credential age."""

import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.integration import Integration

logger = logging.getLogger(__name__)

ROTATION_THRESHOLD_DAYS = 90


async def check_credential_rotation(
    db: AsyncSession, org_id: UUID
) -> list[dict]:
    """Check all integrations for credentials needing rotation.

    Returns a list of integrations whose credentials are older than
    the rotation threshold (90 days by default).
    """
    result = await db.execute(
        select(Integration).where(
            Integration.org_id == org_id,
            Integration.status == "connected",
        )
    )
    integrations = list(result.scalars().all())

    now = datetime.now(timezone.utc)
    rotation_needed: list[dict] = []

    for integration in integrations:
        if not integration.created_at:
            continue
        age_days = (now - integration.created_at).days
        if age_days > ROTATION_THRESHOLD_DAYS:
            rotation_needed.append(
                {
                    "integration_id": str(integration.id),
                    "name": integration.name,
                    "provider": integration.provider,
                    "age_days": age_days,
                    "created_at": integration.created_at.isoformat(),
                    "status": "rotation_needed",
                    "recommendation": (
                        f"Credentials for {integration.name} ({integration.provider}) "
                        f"are {age_days} days old. Rotate within 7 days."
                    ),
                }
            )

    return rotation_needed


async def run_rotation_check_all_orgs() -> int:
    """Run credential rotation check across all organizations.

    Returns the total number of integrations needing rotation.
    """
    from app.core.database import async_session
    from app.models.organization import Organization
    from app.services.notification_service import send_system_notification

    total_flagged = 0
    try:
        async with async_session() as db:
            result = await db.execute(select(Organization))
            orgs = list(result.scalars().all())

            for org in orgs:
                try:
                    needing_rotation = await check_credential_rotation(db, org.id)
                    if needing_rotation:
                        total_flagged += len(needing_rotation)
                        await send_system_notification(
                            db,
                            org_id=org.id,
                            category="credential_rotation",
                            title="Credential Rotation Required",
                            message=(
                                f"{len(needing_rotation)} integration(s) have credentials "
                                f"older than {ROTATION_THRESHOLD_DAYS} days and should be rotated."
                            ),
                            severity="warning",
                            entity_type="integration",
                            entity_id=None,
                        )
                except Exception as exc:
                    logger.error(
                        "Credential rotation check failed for org %s: %s",
                        org.id,
                        exc,
                    )
    except Exception as exc:
        logger.error("Credential rotation check failed: %s", exc)

    return total_flagged
