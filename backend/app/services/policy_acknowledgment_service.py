"""Service for policy acknowledgment tracking."""
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.policy import Policy
from app.models.policy_acknowledgment import PolicyAcknowledgment


async def list_acknowledgments(
    db: AsyncSession, org_id: UUID, policy_id: UUID | None = None,
    user_id: UUID | None = None, status: str | None = None,
    page: int = 1, page_size: int = 50,
) -> tuple[list[PolicyAcknowledgment], int]:
    base = select(PolicyAcknowledgment).where(PolicyAcknowledgment.org_id == org_id)
    count_q = select(func.count()).select_from(PolicyAcknowledgment).where(
        PolicyAcknowledgment.org_id == org_id
    )
    if policy_id:
        base = base.where(PolicyAcknowledgment.policy_id == policy_id)
        count_q = count_q.where(PolicyAcknowledgment.policy_id == policy_id)
    if user_id:
        base = base.where(PolicyAcknowledgment.user_id == user_id)
        count_q = count_q.where(PolicyAcknowledgment.user_id == user_id)
    if status:
        base = base.where(PolicyAcknowledgment.status == status)
        count_q = count_q.where(PolicyAcknowledgment.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base.offset((page - 1) * page_size).limit(page_size).order_by(
        PolicyAcknowledgment.created_at.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def request_acknowledgment(
    db: AsyncSession, org_id: UUID, policy_id: UUID,
    user_id: UUID, due_date: datetime | None = None,
) -> PolicyAcknowledgment:
    """Create a pending acknowledgment request for a user."""
    # Get policy version
    policy_result = await db.execute(
        select(Policy).where(Policy.id == policy_id, Policy.org_id == org_id)
    )
    policy = policy_result.scalar_one_or_none()
    if not policy:
        raise NotFoundError(f"Policy {policy_id} not found")

    # Check if already exists for this version
    existing = await db.execute(
        select(PolicyAcknowledgment).where(
            PolicyAcknowledgment.org_id == org_id,
            PolicyAcknowledgment.policy_id == policy_id,
            PolicyAcknowledgment.user_id == user_id,
            PolicyAcknowledgment.policy_version == policy.version,
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError("Acknowledgment already exists for this policy version")

    ack = PolicyAcknowledgment(
        org_id=org_id,
        policy_id=policy_id,
        user_id=user_id,
        policy_version=policy.version,
        status="pending",
        due_date=due_date,
    )
    db.add(ack)
    await db.commit()
    await db.refresh(ack)
    return ack


async def bulk_request_acknowledgment(
    db: AsyncSession, org_id: UUID, policy_id: UUID,
    user_ids: list[UUID], due_date: datetime | None = None,
) -> int:
    """Send acknowledgment requests to multiple users. Returns count created."""
    policy_result = await db.execute(
        select(Policy).where(Policy.id == policy_id, Policy.org_id == org_id)
    )
    policy = policy_result.scalar_one_or_none()
    if not policy:
        raise NotFoundError(f"Policy {policy_id} not found")

    count = 0
    for uid in user_ids:
        existing = await db.execute(
            select(PolicyAcknowledgment).where(
                PolicyAcknowledgment.org_id == org_id,
                PolicyAcknowledgment.policy_id == policy_id,
                PolicyAcknowledgment.user_id == uid,
                PolicyAcknowledgment.policy_version == policy.version,
            )
        )
        if existing.scalar_one_or_none():
            continue
        ack = PolicyAcknowledgment(
            org_id=org_id,
            policy_id=policy_id,
            user_id=uid,
            policy_version=policy.version,
            status="pending",
            due_date=due_date,
        )
        db.add(ack)
        count += 1
    if count:
        await db.commit()
    return count


async def acknowledge(
    db: AsyncSession, org_id: UUID, acknowledgment_id: UUID,
    user_id: UUID, ip_address: str | None = None, notes: str | None = None,
) -> PolicyAcknowledgment:
    """Mark an acknowledgment as acknowledged.

    First tries matching by user_id (self-acknowledge). Falls back to
    org-only lookup so compliance managers can acknowledge on behalf of users
    whose Keycloak sub differs from the backend user id.
    """
    # Try exact match first (user acknowledging their own)
    result = await db.execute(
        select(PolicyAcknowledgment).where(
            PolicyAcknowledgment.id == acknowledgment_id,
            PolicyAcknowledgment.org_id == org_id,
            PolicyAcknowledgment.user_id == user_id,
        )
    )
    ack = result.scalar_one_or_none()
    if not ack:
        # Fallback: allow compliance manager to acknowledge any pending item in their org
        result2 = await db.execute(
            select(PolicyAcknowledgment).where(
                PolicyAcknowledgment.id == acknowledgment_id,
                PolicyAcknowledgment.org_id == org_id,
            )
        )
        ack = result2.scalar_one_or_none()
    if not ack:
        raise NotFoundError(f"Acknowledgment {acknowledgment_id} not found")

    ack.status = "acknowledged"
    ack.acknowledged_at = datetime.now(timezone.utc)
    ack.ip_address = ip_address
    ack.notes = notes
    await db.commit()
    await db.refresh(ack)
    return ack


async def get_stats(
    db: AsyncSession, org_id: UUID, policy_id: UUID | None = None,
) -> dict:
    """Get acknowledgment statistics."""
    base = select(PolicyAcknowledgment).where(PolicyAcknowledgment.org_id == org_id)
    if policy_id:
        base = base.where(PolicyAcknowledgment.policy_id == policy_id)

    result = await db.execute(base)
    acks = list(result.scalars().all())
    total = len(acks)
    acknowledged = sum(1 for a in acks if a.status == "acknowledged")
    overdue = sum(
        1 for a in acks
        if a.status == "pending" and a.due_date and a.due_date < datetime.now(timezone.utc)
    )
    pending = total - acknowledged

    return {
        "total": total,
        "acknowledged": acknowledged,
        "pending": pending,
        "overdue": overdue,
        "acknowledgment_rate": round(acknowledged / max(total, 1) * 100, 1),
    }


async def check_overdue(db: AsyncSession, org_id: UUID) -> int:
    """Mark overdue acknowledgments. Returns count newly marked overdue."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(PolicyAcknowledgment).where(
            PolicyAcknowledgment.org_id == org_id,
            PolicyAcknowledgment.status == "pending",
            PolicyAcknowledgment.due_date.isnot(None),
            PolicyAcknowledgment.due_date < now,
        )
    )
    overdue = list(result.scalars().all())
    for ack in overdue:
        ack.status = "overdue"
    if overdue:
        await db.commit()
    return len(overdue)
