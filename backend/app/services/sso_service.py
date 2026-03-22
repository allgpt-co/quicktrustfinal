"""SSO Configuration + SCIM token management service."""

import hashlib
import secrets
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.sso_config import SSOConfiguration, SCIMToken


# ---------------------------------------------------------------------------
# SSO Configuration
# ---------------------------------------------------------------------------

async def get_sso_config(db: AsyncSession, org_id: UUID) -> SSOConfiguration | None:
    result = await db.execute(
        select(SSOConfiguration).where(SSOConfiguration.org_id == org_id)
    )
    return result.scalar_one_or_none()


async def upsert_sso_config(
    db: AsyncSession,
    org_id: UUID,
    provider: str,
    enabled: bool,
    enforced: bool = False,
    entity_id: str | None = None,
    sso_url: str | None = None,
    certificate: str | None = None,
    oidc_client_id: str | None = None,
    oidc_client_secret: str | None = None,
    oidc_issuer: str | None = None,
    email_domains: str | None = None,
    attribute_mapping: dict | None = None,
) -> SSOConfiguration:
    existing = await get_sso_config(db, org_id)

    if existing:
        existing.provider = provider
        existing.enabled = enabled
        existing.enforced = enforced
        existing.entity_id = entity_id
        existing.sso_url = sso_url
        if certificate is not None:
            existing.certificate = certificate
        existing.oidc_client_id = oidc_client_id
        if oidc_client_secret is not None:
            existing.oidc_client_secret = oidc_client_secret
        existing.oidc_issuer = oidc_issuer
        existing.email_domains = email_domains
        existing.attribute_mapping = attribute_mapping
        await db.commit()
        await db.refresh(existing)
        return existing

    config = SSOConfiguration(
        org_id=org_id,
        provider=provider,
        enabled=enabled,
        enforced=enforced,
        entity_id=entity_id,
        sso_url=sso_url,
        certificate=certificate,
        oidc_client_id=oidc_client_id,
        oidc_client_secret=oidc_client_secret,
        oidc_issuer=oidc_issuer,
        email_domains=email_domains,
        attribute_mapping=attribute_mapping,
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


async def delete_sso_config(db: AsyncSession, org_id: UUID) -> None:
    config = await get_sso_config(db, org_id)
    if config:
        await db.delete(config)
        await db.commit()


# ---------------------------------------------------------------------------
# SCIM Token Management
# ---------------------------------------------------------------------------

def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


async def create_scim_token(
    db: AsyncSession, org_id: UUID, name: str
) -> tuple[SCIMToken, str]:
    """Create a SCIM token. Returns (token_record, raw_token).
    The raw token is only shown once — it's stored as a hash."""
    raw_token = f"scim_{secrets.token_urlsafe(48)}"
    token_hash = _hash_token(raw_token)

    token = SCIMToken(
        org_id=org_id,
        name=name,
        token_hash=token_hash,
        is_active=True,
    )
    db.add(token)
    await db.commit()
    await db.refresh(token)
    return token, raw_token


async def list_scim_tokens(db: AsyncSession, org_id: UUID) -> list[SCIMToken]:
    result = await db.execute(
        select(SCIMToken)
        .where(SCIMToken.org_id == org_id)
        .order_by(SCIMToken.created_at.desc())
    )
    return list(result.scalars().all())


async def revoke_scim_token(db: AsyncSession, org_id: UUID, token_id: UUID) -> SCIMToken:
    result = await db.execute(
        select(SCIMToken).where(SCIMToken.id == token_id, SCIMToken.org_id == org_id)
    )
    token = result.scalar_one_or_none()
    if not token:
        raise NotFoundError("SCIM token not found")
    token.is_active = False
    await db.commit()
    await db.refresh(token)
    return token


async def validate_scim_token(db: AsyncSession, raw_token: str) -> UUID | None:
    """Validate a SCIM bearer token. Returns org_id if valid, None otherwise."""
    token_hash = _hash_token(raw_token)
    result = await db.execute(
        select(SCIMToken).where(
            SCIMToken.token_hash == token_hash,
            SCIMToken.is_active.is_(True),
        )
    )
    token = result.scalar_one_or_none()
    if not token:
        return None

    # Check expiry
    if token.expires_at and token.expires_at < datetime.now(timezone.utc):
        return None

    # Update last_used_at
    token.last_used_at = datetime.now(timezone.utc)
    await db.commit()
    return token.org_id
