from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Request
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import select

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import NotFoundError
from app.schemas.trust_center import (
    TrustCenterConfigCreate,
    TrustCenterConfigUpdate,
    TrustCenterConfigResponse,
    TrustCenterDocumentCreate,
    TrustCenterDocumentUpdate,
    TrustCenterDocumentResponse,
    PublicTrustCenterResponse,
)
from app.services import trust_center_service

# Authenticated routes
router = APIRouter(
    prefix="/organizations/{org_id}/trust-center",
    tags=["trust-center"],
)


# ---------------------------------------------------------------------------
# Compliance badge mapping (framework name → public-facing badge)
# ---------------------------------------------------------------------------
BADGE_MAP: dict[str, dict[str, str]] = {
    "SOC 2": {"name": "SOC 2 Type II", "color": "#1a237e", "icon": "shield-check"},
    "ISO 27001": {"name": "ISO 27001:2022", "color": "#1b5e20", "icon": "globe"},
    "HIPAA": {"name": "HIPAA Compliant", "color": "#b71c1c", "icon": "heart-pulse"},
    "PCI DSS": {"name": "PCI DSS v4.0", "color": "#e65100", "icon": "credit-card"},
    "GDPR": {"name": "GDPR Compliant", "color": "#0d47a1", "icon": "shield"},
    "SOX": {"name": "SOX Compliant", "color": "#4a148c", "icon": "building"},
    "CCPA": {"name": "CCPA Ready", "color": "#006064", "icon": "shield"},
    "NIST CSF": {"name": "NIST CSF", "color": "#bf360c", "icon": "shield-check"},
}


def _build_badges_from_frameworks(frameworks: list) -> list[dict]:
    """Return a deduplicated list of compliance badges derived from active frameworks."""
    badges: list[dict] = []
    seen: set[str] = set()
    for framework in frameworks:
        for key, badge in BADGE_MAP.items():
            if key.lower() in framework.name.lower() and key not in seen:
                badges.append(
                    {
                        **badge,
                        "framework_id": str(framework.id),
                        "framework_name": framework.name,
                        "framework_version": framework.version,
                    }
                )
                seen.add(key)
                break
    return badges


# ---------------------------------------------------------------------------
# Static routes — MUST come before any /{id} routes to avoid UUID collisions
# ---------------------------------------------------------------------------


@router.get("/badges")
async def get_compliance_badges(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser
):
    """Return compliance badges for the org derived from active frameworks."""
    from app.models.framework import Framework

    result = await db.execute(select(Framework).where(Framework.is_active.is_(True)))
    frameworks = list(result.scalars().all())
    badges = _build_badges_from_frameworks(frameworks)
    return {"total": len(badges), "badges": badges}


@router.get("/nda/signatures")
async def list_nda_signatures(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser
):
    """List all NDA signatures for the org (admin view)."""
    from app.models.nda_signature import NdaSignature

    result = await db.execute(
        select(NdaSignature)
        .where(NdaSignature.org_id == org_id)
        .order_by(NdaSignature.signed_at.desc())
    )
    signatures = list(result.scalars().all())

    return {
        "total": len(signatures),
        "signatures": [
            {
                "id": str(s.id),
                "signer_name": s.signer_name,
                "signer_email": s.signer_email,
                "signer_company": s.signer_company,
                "signed_at": s.signed_at.isoformat() if s.signed_at else None,
                "ip_address": s.ip_address,
            }
            for s in signatures
        ],
    }


@router.get("/config", response_model=TrustCenterConfigResponse)
async def get_config(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await trust_center_service.get_or_create_config(db, org_id)


@router.post("/config", response_model=TrustCenterConfigResponse, status_code=201)
async def create_config(org_id: VerifiedOrgId, data: TrustCenterConfigCreate, db: DB, current_user: ComplianceUser):
    return await trust_center_service.get_or_create_config(db, org_id, data)


@router.patch("/config", response_model=TrustCenterConfigResponse)
async def update_config(org_id: VerifiedOrgId, data: TrustCenterConfigUpdate, db: DB, current_user: ComplianceUser):
    return await trust_center_service.update_config(db, org_id, data)


@router.get("/documents", response_model=list[TrustCenterDocumentResponse])
async def list_documents(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await trust_center_service.list_documents(db, org_id)


@router.post("/documents", response_model=TrustCenterDocumentResponse, status_code=201)
async def create_document(org_id: VerifiedOrgId, data: TrustCenterDocumentCreate, db: DB, current_user: ComplianceUser):
    return await trust_center_service.create_document(db, org_id, data)


@router.get("/documents/{doc_id}", response_model=TrustCenterDocumentResponse)
async def get_document(org_id: VerifiedOrgId, doc_id: UUID, db: DB, current_user: AnyInternalUser):
    return await trust_center_service.get_document(db, org_id, doc_id)


@router.patch("/documents/{doc_id}", response_model=TrustCenterDocumentResponse)
async def update_document(
    org_id: VerifiedOrgId, doc_id: UUID, data: TrustCenterDocumentUpdate, db: DB, current_user: ComplianceUser
):
    return await trust_center_service.update_document(db, org_id, doc_id, data)


@router.delete("/documents/{doc_id}", status_code=204)
async def delete_document(org_id: VerifiedOrgId, doc_id: UUID, db: DB, current_user: ComplianceUser):
    await trust_center_service.delete_document(db, org_id, doc_id)


# ---------------------------------------------------------------------------
# Public router (no auth) — registered separately in router.py
# ---------------------------------------------------------------------------
public_router = APIRouter(tags=["trust-center-public"])


class NdaSignRequest(PydanticBaseModel):
    signer_name: str
    signer_email: str
    signer_company: str | None = None


@public_router.get("/trust/{slug}", response_model=PublicTrustCenterResponse)
async def get_public_trust_center(slug: str, db: DB):
    result = await trust_center_service.get_public_trust_center(db, slug)
    if not result:
        raise NotFoundError("Trust center not found or not published")
    return result


@public_router.get("/trust-center/{org_slug}/public")
async def get_public_trust_page(org_slug: str, db: DB):
    """Public endpoint returning full trust center data for an organization.

    No authentication required — intended for customer-facing trust pages.
    """
    from app.models.framework import Framework
    from app.models.organization import Organization
    from app.models.trust_center import TrustCenterConfig, TrustCenterDocument

    org_result = await db.execute(select(Organization).where(Organization.slug == org_slug))
    org = org_result.scalar_one_or_none()
    if not org:
        raise NotFoundError(f"Organization '{org_slug}' not found")

    cfg_result = await db.execute(
        select(TrustCenterConfig).where(TrustCenterConfig.org_id == org.id)
    )
    config = cfg_result.scalar_one_or_none()

    docs_result = await db.execute(
        select(TrustCenterDocument).where(
            TrustCenterDocument.org_id == org.id,
            TrustCenterDocument.is_public.is_(True),
        )
    )
    documents = list(docs_result.scalars().all())

    fw_result = await db.execute(select(Framework).where(Framework.is_active.is_(True)))
    frameworks = list(fw_result.scalars().all())
    badges = [
        {"name": b["name"], "color": b["color"], "icon": b["icon"], "framework_name": b["framework_name"]}
        for b in _build_badges_from_frameworks(frameworks)
    ]

    config_payload: dict = {}
    if config:
        branding = config.branding or {}
        config_payload = {
            "headline": config.headline,
            "description": config.description,
            "welcome_message": config.description,
            "contact_email": config.contact_email,
            "logo_url": config.logo_url,
            "primary_color": branding.get("primary_color") if isinstance(branding, dict) else None,
            "is_published": config.is_published,
            "slug": config.slug,
        }

    return {
        "organization": {
            "name": org.name,
            "slug": org.slug,
            "industry": org.industry,
        },
        "config": config_payload,
        "badges": badges,
        "documents": [
            {
                "id": str(d.id),
                "title": d.title,
                "description": d.description,
                "document_type": d.document_type,
                "requires_nda": d.requires_nda,
            }
            for d in documents
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@public_router.post("/trust-center/{org_slug}/nda/sign")
async def sign_nda(
    org_slug: str,
    data: NdaSignRequest,
    request: Request,
    db: DB,
):
    """Record an NDA signature from a public trust center visitor.

    Returns a short-lived access token that the caller can use to view
    NDA-gated documents. The token is opaque random bytes — NDA verification
    is enforced separately when accessing gated resources.
    """
    import secrets

    from app.models.nda_signature import NdaSignature
    from app.models.organization import Organization

    org_result = await db.execute(select(Organization).where(Organization.slug == org_slug))
    org = org_result.scalar_one_or_none()
    if not org:
        raise NotFoundError(f"Organization '{org_slug}' not found")

    signature = NdaSignature(
        org_id=org.id,
        signer_name=data.signer_name,
        signer_email=data.signer_email,
        signer_company=data.signer_company,
        signed_at=datetime.now(timezone.utc),
        ip_address=request.client.host if request.client else None,
    )
    db.add(signature)
    await db.commit()
    await db.refresh(signature)

    token = secrets.token_urlsafe(32)

    return {
        "signature_id": str(signature.id),
        "access_token": token,
        "expires_in": 86400,
        "signed_at": signature.signed_at.isoformat(),
    }
