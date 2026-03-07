from uuid import UUID

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.cross_framework_mapping import CrossFrameworkMapping
from app.schemas.cross_framework_mapping import CrossFrameworkMappingCreate


async def list_mappings(
    db: AsyncSession,
    requirement_id: UUID | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[CrossFrameworkMapping], int]:
    base_q = select(CrossFrameworkMapping)
    count_q = select(func.count()).select_from(CrossFrameworkMapping)

    if requirement_id:
        filt = or_(
            CrossFrameworkMapping.requirement_a_id == requirement_id,
            CrossFrameworkMapping.requirement_b_id == requirement_id,
        )
        base_q = base_q.where(filt)
        count_q = count_q.where(filt)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        CrossFrameworkMapping.created_at.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_mapping(
    db: AsyncSession, data: CrossFrameworkMappingCreate
) -> CrossFrameworkMapping:
    mapping = CrossFrameworkMapping(**data.model_dump())
    db.add(mapping)
    await db.commit()
    await db.refresh(mapping)
    return mapping


async def get_mapping(db: AsyncSession, mapping_id: UUID) -> CrossFrameworkMapping:
    result = await db.execute(
        select(CrossFrameworkMapping).where(CrossFrameworkMapping.id == mapping_id)
    )
    mapping = result.scalar_one_or_none()
    if not mapping:
        raise NotFoundError(f"CrossFrameworkMapping {mapping_id} not found")
    return mapping


async def delete_mapping(db: AsyncSession, mapping_id: UUID) -> None:
    mapping = await get_mapping(db, mapping_id)
    await db.delete(mapping)
    await db.commit()
