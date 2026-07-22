from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services import auth_service


async def list_users(
    db: AsyncSession, org_id: UUID, page: int = 1, page_size: int = 50
) -> tuple[list[User], int]:
    count_q = select(func.count()).select_from(User).where(User.org_id == org_id)
    total = (await db.execute(count_q)).scalar() or 0
    q = (
        select(User)
        .where(User.org_id == org_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(User.created_at.desc())
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_user(db: AsyncSession, org_id: UUID, data: UserCreate) -> User:
    normalized_email = str(data.email).strip().lower()
    existing = await db.execute(
        select(User).where(func.lower(User.email) == normalized_email)
    )
    if existing.scalar_one_or_none():
        raise ConflictError(f"User with email '{data.email}' already exists")

    user = User(
        org_id=org_id,
        email=normalized_email,
        full_name=data.full_name,
        role=data.role.value if hasattr(data.role, "value") else str(data.role),
        department=data.department,
        password_hash=None,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await auth_service.request_password_reset(db, user.email)
    return user


async def get_user(db: AsyncSession, org_id: UUID, user_id: UUID) -> User:
    result = await db.execute(
        select(User).where(User.id == user_id, User.org_id == org_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError(f"User {user_id} not found")
    return user


async def update_user(
    db: AsyncSession, org_id: UUID, user_id: UUID, data: UserUpdate
) -> User:
    user = await get_user(db, org_id, user_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value.value if hasattr(value, "value") else value)
    if update_data.get("is_active") is False:
        await auth_service.revoke_all_sessions(db, user.id)
    else:
        await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, org_id: UUID, user_id: UUID) -> None:
    user = await get_user(db, org_id, user_id)
    user.is_active = False
    await auth_service.revoke_all_sessions(db, user.id)
