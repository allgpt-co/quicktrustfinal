from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.core.field_encryption import encrypt_field, decrypt_field
from app.models.integration import Integration
from app.schemas.integration import IntegrationCreate, IntegrationUpdate

# Fields that contain sensitive data and should be encrypted at rest
_SENSITIVE_FIELDS = ["credentials_ref"]


def _encrypt_on_write(data: dict) -> dict:
    """Encrypt sensitive fields before database write."""
    for field in _SENSITIVE_FIELDS:
        if field in data and data[field] and isinstance(data[field], str):
            data[field] = encrypt_field(data[field])
    return data


def _decrypt_credentials(integration: Integration) -> Integration:
    """Decrypt credentials_ref after database read (in-place, no DB write)."""
    if integration.credentials_ref:
        try:
            integration.credentials_ref = decrypt_field(integration.credentials_ref)
        except Exception:
            pass  # Legacy plaintext or missing key — leave as-is
    return integration


async def list_integrations(
    db: AsyncSession, org_id: UUID, page: int = 1, page_size: int = 50
) -> tuple[list[Integration], int]:
    base_q = select(Integration).where(Integration.org_id == org_id)
    count_q = select(func.count()).select_from(Integration).where(Integration.org_id == org_id)
    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Integration.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_integration(db: AsyncSession, org_id: UUID, data: IntegrationCreate) -> Integration:
    fields = _encrypt_on_write(data.model_dump())
    integration = Integration(org_id=org_id, **fields)
    db.add(integration)
    await db.commit()
    await db.refresh(integration)
    return _decrypt_credentials(integration)


async def get_integration(db: AsyncSession, org_id: UUID, integration_id: UUID) -> Integration:
    result = await db.execute(
        select(Integration).where(
            Integration.id == integration_id, Integration.org_id == org_id
        )
    )
    integration = result.scalar_one_or_none()
    if not integration:
        raise NotFoundError(f"Integration {integration_id} not found")
    return integration


async def update_integration(
    db: AsyncSession, org_id: UUID, integration_id: UUID, data: IntegrationUpdate
) -> Integration:
    integration = await get_integration(db, org_id, integration_id)
    updates = _encrypt_on_write(data.model_dump(exclude_unset=True))
    for key, value in updates.items():
        setattr(integration, key, value)
    await db.commit()
    await db.refresh(integration)
    return _decrypt_credentials(integration)


async def delete_integration(db: AsyncSession, org_id: UUID, integration_id: UUID) -> None:
    integration = await get_integration(db, org_id, integration_id)
    await db.delete(integration)
    await db.commit()
