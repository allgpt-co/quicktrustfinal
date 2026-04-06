"""API key management endpoints — create, list, and revoke API keys."""

import hashlib
import secrets
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DB, AdminUser, AnyInternalUser, VerifiedOrgId
from app.models.api_key import ApiKey

router = APIRouter(
    prefix="/organizations/{org_id}/api-keys",
    tags=["api-keys"],
)

API_KEY_PREFIX = "qt_"
API_KEY_LENGTH = 48  # total length of the raw key


# ---------- Schemas ----------

class ApiKeyCreate(PydanticBaseModel):
    name: str
    scopes: list[str] = ["read"]
    expires_at: datetime | None = None


class ApiKeyCreateResponse(PydanticBaseModel):
    """Returned only once at creation time — includes the raw key."""

    id: UUID
    name: str
    key: str  # full key, shown only once
    key_prefix: str
    scopes: list[str] | None
    expires_at: str | None = None
    created_at: str | None = None

    model_config = {"from_attributes": True}


class ApiKeyListResponse(PydanticBaseModel):
    id: UUID
    name: str
    key_prefix: str
    scopes: list[str] | None
    is_active: bool
    expires_at: str | None = None
    last_used_at: str | None = None
    created_at: str | None = None

    model_config = {"from_attributes": True}


# ---------- Helpers ----------

def _generate_api_key() -> str:
    """Generate a cryptographically secure API key."""
    random_part = secrets.token_urlsafe(API_KEY_LENGTH)
    return f"{API_KEY_PREFIX}{random_part}"


def _hash_key(raw_key: str) -> str:
    """Hash an API key using SHA-256."""
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


# ---------- Endpoints ----------

@router.post("", response_model=ApiKeyCreateResponse, status_code=201)
async def create_api_key(
    org_id: VerifiedOrgId, data: ApiKeyCreate, db: DB, current_user: AdminUser,
):
    """Create a new API key. The raw key is returned only once."""
    raw_key = _generate_api_key()
    key_hash = _hash_key(raw_key)
    key_prefix = raw_key[:8]

    api_key = ApiKey(
        org_id=org_id,
        user_id=current_user.id,
        name=data.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        scopes=data.scopes,
        is_active=True,
        expires_at=data.expires_at,
    )
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)

    return ApiKeyCreateResponse(
        id=api_key.id,
        name=api_key.name,
        key=raw_key,
        key_prefix=key_prefix,
        scopes=api_key.scopes,
        expires_at=api_key.expires_at.isoformat() if api_key.expires_at else None,
        created_at=api_key.created_at.isoformat() if api_key.created_at else None,
    )


@router.get("", response_model=list[ApiKeyListResponse])
async def list_api_keys(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
):
    """List all API keys for the organization (prefix + name only, NOT full key)."""
    result = await db.execute(
        select(ApiKey)
        .where(ApiKey.org_id == org_id)
        .order_by(ApiKey.created_at.desc())
    )
    keys = list(result.scalars().all())
    return [ApiKeyListResponse.model_validate(k) for k in keys]


@router.delete("/{key_id}", status_code=204)
async def revoke_api_key(
    org_id: VerifiedOrgId, key_id: UUID, db: DB, current_user: AdminUser,
):
    """Revoke (deactivate) an API key."""
    from app.core.exceptions import NotFoundError

    result = await db.execute(
        select(ApiKey).where(ApiKey.id == key_id, ApiKey.org_id == org_id)
    )
    api_key = result.scalar_one_or_none()
    if not api_key:
        raise NotFoundError("API key not found")

    api_key.is_active = False
    await db.commit()
