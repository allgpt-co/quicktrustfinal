"""SSO Configuration + SCIM Token management API."""

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.dependencies import DB, AdminUser, VerifiedOrgId
from app.services import sso_service

router = APIRouter(
    prefix="/organizations/{org_id}/sso",
    tags=["sso"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SSOConfigRequest(BaseModel):
    provider: str = Field(..., pattern="^(saml|oidc)$")
    enabled: bool = False
    enforced: bool = False
    entity_id: str | None = None
    sso_url: str | None = None
    certificate: str | None = None
    oidc_client_id: str | None = None
    oidc_client_secret: str | None = None
    oidc_issuer: str | None = None
    email_domains: str | None = None
    attribute_mapping: dict | None = None


class SSOConfigResponse(BaseModel):
    id: UUID
    org_id: UUID
    provider: str
    enabled: bool
    enforced: bool
    entity_id: str | None = None
    sso_url: str | None = None
    certificate_configured: bool = False
    oidc_client_id: str | None = None
    oidc_issuer: str | None = None
    email_domains: str | None = None
    attribute_mapping: dict | None = None
    scim_enabled: bool = False

    model_config = {"from_attributes": True}


class SCIMTokenCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class SCIMTokenResponse(BaseModel):
    id: UUID
    name: str
    is_active: bool
    last_used_at: str | None = None
    created_at: str

    model_config = {"from_attributes": True}


class SCIMTokenCreatedResponse(BaseModel):
    token: SCIMTokenResponse
    raw_token: str  # Only shown once!


# ---------------------------------------------------------------------------
# SSO Configuration endpoints
# ---------------------------------------------------------------------------

@router.get("/config", response_model=SSOConfigResponse | None)
async def get_sso_config(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    config = await sso_service.get_sso_config(db, org_id)
    if not config:
        return None
    return _config_response(config)


@router.put("/config", response_model=SSOConfigResponse)
async def upsert_sso_config(
    org_id: VerifiedOrgId, data: SSOConfigRequest, db: DB, current_user: AdminUser
):
    config = await sso_service.upsert_sso_config(
        db, org_id,
        provider=data.provider,
        enabled=data.enabled,
        enforced=data.enforced,
        entity_id=data.entity_id,
        sso_url=data.sso_url,
        certificate=data.certificate,
        oidc_client_id=data.oidc_client_id,
        oidc_client_secret=data.oidc_client_secret,
        oidc_issuer=data.oidc_issuer,
        email_domains=data.email_domains,
        attribute_mapping=data.attribute_mapping,
    )
    return _config_response(config)


@router.delete("/config")
async def delete_sso_config(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    await sso_service.delete_sso_config(db, org_id)
    return {"message": "SSO configuration deleted"}


# ---------------------------------------------------------------------------
# SCIM Token endpoints
# ---------------------------------------------------------------------------

@router.get("/scim-tokens", response_model=list[SCIMTokenResponse])
async def list_scim_tokens(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    tokens = await sso_service.list_scim_tokens(db, org_id)
    return [
        SCIMTokenResponse(
            id=t.id,
            name=t.name,
            is_active=t.is_active,
            last_used_at=t.last_used_at.isoformat() if t.last_used_at else None,
            created_at=t.created_at.isoformat(),
        )
        for t in tokens
    ]


@router.post("/scim-tokens", response_model=SCIMTokenCreatedResponse, status_code=201)
async def create_scim_token(
    org_id: VerifiedOrgId, data: SCIMTokenCreateRequest, db: DB, current_user: AdminUser
):
    token, raw_token = await sso_service.create_scim_token(db, org_id, data.name)
    return SCIMTokenCreatedResponse(
        token=SCIMTokenResponse(
            id=token.id,
            name=token.name,
            is_active=token.is_active,
            last_used_at=None,
            created_at=token.created_at.isoformat(),
        ),
        raw_token=raw_token,
    )


@router.delete("/scim-tokens/{token_id}")
async def revoke_scim_token(
    org_id: VerifiedOrgId, token_id: UUID, db: DB, current_user: AdminUser
):
    await sso_service.revoke_scim_token(db, org_id, token_id)
    return {"message": "SCIM token revoked"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _config_response(config) -> SSOConfigResponse:
    return SSOConfigResponse(
        id=config.id,
        org_id=config.org_id,
        provider=config.provider,
        enabled=config.enabled,
        enforced=config.enforced,
        entity_id=config.entity_id,
        sso_url=config.sso_url,
        certificate_configured=bool(config.certificate),
        oidc_client_id=config.oidc_client_id,
        oidc_issuer=config.oidc_issuer,
        email_domains=config.email_domains,
        attribute_mapping=config.attribute_mapping,
        scim_enabled=config.scim_enabled,
    )
