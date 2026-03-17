"""Service for control exception/waiver management."""
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.control_exception import ControlException
from app.schemas.control_exception import (
    ControlExceptionCreate,
    ControlExceptionUpdate,
)


async def list_exceptions(
    db: AsyncSession, org_id: UUID, control_id: UUID | None = None,
    status: str | None = None, page: int = 1, page_size: int = 50,
) -> tuple[list[ControlException], int]:
    base = select(ControlException).where(ControlException.org_id == org_id)
    count_q = select(func.count()).select_from(ControlException).where(
        ControlException.org_id == org_id
    )
    if control_id:
        base = base.where(ControlException.control_id == control_id)
        count_q = count_q.where(ControlException.control_id == control_id)
    if status:
        base = base.where(ControlException.status == status)
        count_q = count_q.where(ControlException.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base.offset((page - 1) * page_size).limit(page_size).order_by(
        ControlException.created_at.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_exception(
    db: AsyncSession, org_id: UUID, data: ControlExceptionCreate,
    requested_by_id: UUID | None = None,
) -> ControlException:
    exc = ControlException(
        org_id=org_id,
        control_id=data.control_id,
        title=data.title,
        reason=data.reason,
        compensating_control=data.compensating_control,
        risk_acceptance=data.risk_acceptance,
        expires_at=data.expires_at,
        status="pending",
        requested_by_id=requested_by_id,
    )
    db.add(exc)
    await db.commit()
    await db.refresh(exc)
    return exc


async def get_exception(
    db: AsyncSession, org_id: UUID, exception_id: UUID
) -> ControlException:
    result = await db.execute(
        select(ControlException).where(
            ControlException.id == exception_id, ControlException.org_id == org_id
        )
    )
    exc = result.scalar_one_or_none()
    if not exc:
        raise NotFoundError(f"Control exception {exception_id} not found")
    return exc


async def update_exception(
    db: AsyncSession, org_id: UUID, exception_id: UUID,
    data: ControlExceptionUpdate,
) -> ControlException:
    exc = await get_exception(db, org_id, exception_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(exc, field, value)
    await db.commit()
    await db.refresh(exc)
    return exc


async def approve_exception(
    db: AsyncSession, org_id: UUID, exception_id: UUID,
    approved_by_id: UUID, expires_at: datetime | None = None,
) -> ControlException:
    exc = await get_exception(db, org_id, exception_id)
    exc.status = "approved"
    exc.approved_by_id = approved_by_id
    exc.approved_at = datetime.now(timezone.utc)
    exc.is_active = True
    if expires_at:
        exc.expires_at = expires_at
    await db.commit()
    await db.refresh(exc)
    return exc


async def deny_exception(
    db: AsyncSession, org_id: UUID, exception_id: UUID,
    denied_by_id: UUID, denial_reason: str,
) -> ControlException:
    exc = await get_exception(db, org_id, exception_id)
    exc.status = "denied"
    exc.denied_by_id = denied_by_id
    exc.denied_at = datetime.now(timezone.utc)
    exc.denial_reason = denial_reason
    exc.is_active = False
    await db.commit()
    await db.refresh(exc)
    return exc


async def revoke_exception(
    db: AsyncSession, org_id: UUID, exception_id: UUID
) -> ControlException:
    exc = await get_exception(db, org_id, exception_id)
    exc.status = "revoked"
    exc.is_active = False
    await db.commit()
    await db.refresh(exc)
    return exc


async def check_expired_exceptions(db: AsyncSession, org_id: UUID) -> int:
    """Mark expired exceptions. Returns count of newly expired."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(ControlException).where(
            ControlException.org_id == org_id,
            ControlException.status == "approved",
            ControlException.is_active.is_(True),
            ControlException.expires_at.isnot(None),
            ControlException.expires_at < now,
        )
    )
    expired = list(result.scalars().all())
    for exc in expired:
        exc.status = "expired"
        exc.is_active = False
    if expired:
        await db.commit()
    return len(expired)
