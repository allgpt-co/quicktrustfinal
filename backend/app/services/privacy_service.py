"""Service layer for GDPR data-export, data-deletion, and retention enforcement."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.agent_run import AgentRun
from app.models.data_retention import DataRetentionPolicy, DeletionRequest
from app.models.evidence import Evidence
from app.models.user import User

logger = logging.getLogger(__name__)

# Map entity_type → (model, date_column, has_deleted_at) for retention purging
_RETENTION_TARGETS: dict[str, tuple] = {
    "audit_logs": (AuditLog, AuditLog.timestamp, False),
    "agent_runs": (AgentRun, AgentRun.created_at, True),
    "evidences": (Evidence, Evidence.created_at, True),
}


# ---------------------------------------------------------------------------
# Data Retention Policies CRUD
# ---------------------------------------------------------------------------

async def list_policies(db: AsyncSession, org_id: UUID) -> list[DataRetentionPolicy]:
    result = await db.execute(
        select(DataRetentionPolicy)
        .where(DataRetentionPolicy.org_id == org_id)
        .order_by(DataRetentionPolicy.entity_type)
    )
    return list(result.scalars().all())


async def create_policy(
    db: AsyncSession, org_id: UUID, entity_type: str, retention_days: int, description: str | None
) -> DataRetentionPolicy:
    policy = DataRetentionPolicy(
        org_id=org_id,
        entity_type=entity_type,
        retention_days=retention_days,
        description=description,
    )
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    return policy


# ---------------------------------------------------------------------------
# Retention Enforcement (called by scheduler)
# ---------------------------------------------------------------------------

async def enforce_retention(db: AsyncSession) -> int:
    """Delete records older than their org's retention policy.  Returns total purged count."""
    result = await db.execute(
        select(DataRetentionPolicy).where(DataRetentionPolicy.is_active.is_(True))
    )
    policies = list(result.scalars().all())
    total_purged = 0

    for policy in policies:
        target = _RETENTION_TARGETS.get(policy.entity_type)
        if not target:
            continue
        model, date_col, has_deleted_at = target
        cutoff = datetime.now(timezone.utc) - timedelta(days=policy.retention_days)

        if has_deleted_at:
            # Soft-delete: set deleted_at instead of hard delete
            stmt = (
                update(model)
                .where(date_col < cutoff, model.org_id == policy.org_id, model.deleted_at.is_(None))
                .values(deleted_at=datetime.now(timezone.utc))
            )
        else:
            # Models without deleted_at (e.g. AuditLog): hard delete
            stmt = (
                delete(model)
                .where(date_col < cutoff, model.org_id == policy.org_id)
            )
        res = await db.execute(stmt)
        total_purged += res.rowcount
        if res.rowcount:
            logger.info(
                "Retention: purged %d %s records for org %s (cutoff=%s)",
                res.rowcount, policy.entity_type, policy.org_id, cutoff.isoformat(),
            )

    await db.commit()
    return total_purged


# ---------------------------------------------------------------------------
# GDPR Data Export (Right of Access)
# ---------------------------------------------------------------------------

async def export_user_data(db: AsyncSession, user: User) -> dict:
    """Gather all data associated with a user for GDPR export."""
    audit_count = (
        await db.execute(
            select(func.count()).where(AuditLog.actor_id == str(user.id))
        )
    ).scalar() or 0

    evidence_count = (
        await db.execute(
            select(func.count()).where(Evidence.collected_by == user.id)
        )
    ).scalar() or 0

    agent_run_count = (
        await db.execute(
            select(func.count()).where(AgentRun.created_by == user.id)
        )
    ).scalar() or 0

    return {
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "org_id": user.org_id,
        "audit_log_count": audit_count,
        "evidence_count": evidence_count,
        "agent_run_count": agent_run_count,
        "exported_at": datetime.now(timezone.utc),
    }


# ---------------------------------------------------------------------------
# GDPR Data Deletion (Right to Erasure)
# ---------------------------------------------------------------------------

async def create_deletion_request(
    db: AsyncSession, org_id: UUID, requested_by: UUID, target_user_id: UUID, reason: str | None
) -> DeletionRequest:
    req = DeletionRequest(
        org_id=org_id,
        requested_by=requested_by,
        target_user_id=target_user_id,
        reason=reason,
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


async def process_deletion_request(db: AsyncSession, request_id: UUID) -> DeletionRequest:
    """Anonymize/soft-delete user data for a GDPR deletion request."""
    result = await db.execute(
        select(DeletionRequest).where(DeletionRequest.id == request_id)
    )
    req = result.scalar_one()
    req.status = "processing"
    await db.flush()

    target_id = req.target_user_id

    # Anonymize user record
    await db.execute(
        update(User)
        .where(User.id == target_id)
        .values(
            email=f"deleted-{target_id}@anonymized.local",
            full_name="[Deleted User]",
            is_active=False,
            deleted_at=datetime.now(timezone.utc),
        )
    )

    # Anonymize audit log actor references
    await db.execute(
        update(AuditLog)
        .where(AuditLog.actor_id == str(target_id))
        .values(actor_id="[anonymized]")
    )

    req.status = "completed"
    req.completed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(req)
    logger.info("GDPR deletion completed for user %s (request %s)", target_id, request_id)
    return req


async def list_deletion_requests(db: AsyncSession, org_id: UUID) -> list[DeletionRequest]:
    result = await db.execute(
        select(DeletionRequest)
        .where(DeletionRequest.org_id == org_id)
        .order_by(DeletionRequest.created_at.desc())
    )
    return list(result.scalars().all())
