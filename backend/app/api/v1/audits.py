import math
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import func, select

from app.core.dependencies import (
    DB,
    CurrentUser,
    AnyInternalUser,
    ComplianceUser,
    VerifiedOrgId,
    INTERNAL_ROLES,
    RoleChecker,
)
from app.core.exceptions import NotFoundError
from app.models.audit import Audit
from app.models.audit_finding import AuditFinding
from app.models.control import Control
from app.models.evidence import Evidence
from app.schemas.common import PaginatedResponse
from app.schemas.audit import (
    AuditCreate, AuditUpdate, AuditResponse,
    FindingCreate, FindingUpdate, FindingResponse,
    TokenCreate, TokenResponse,
    ReadinessScoreResponse,
)
from app.services import audit_service, auditor_access_service

router = APIRouter(
    prefix="/organizations/{org_id}/audits",
    tags=["audits"],
)

# ---------------------------------------------------------------------------
# Standalone utility routes (no org_id) — registered via utility_router
# ---------------------------------------------------------------------------

utility_router = APIRouter(tags=["audit-utilities"])

Z_VALUES: dict[float, float] = {
    90.0: 1.645,
    95.0: 1.96,
    99.0: 2.576,
}

WORKPAPER_TEMPLATES = [
    {
        "id": "soc2",
        "name": "SOC 2 Type II Workpaper",
        "framework": "SOC 2",
        "sections": [
            "Control Testing",
            "Evidence Review",
            "Gap Analysis",
            "Management Assertions",
        ],
    },
    {
        "id": "iso27001",
        "name": "ISO 27001 Workpaper",
        "framework": "ISO 27001",
        "sections": [
            "ISMS Scope",
            "Risk Assessment",
            "Statement of Applicability",
            "Control Audit",
        ],
    },
    {
        "id": "hipaa",
        "name": "HIPAA Security Rule Workpaper",
        "framework": "HIPAA",
        "sections": [
            "Administrative Safeguards",
            "Physical Safeguards",
            "Technical Safeguards",
        ],
    },
    {
        "id": "pci_dss",
        "name": "PCI DSS Workpaper",
        "framework": "PCI DSS",
        "sections": [
            "Network Security",
            "Cardholder Data Protection",
            "Vulnerability Management",
            "Access Control",
        ],
    },
    {
        "id": "nist_csf",
        "name": "NIST CSF Workpaper",
        "framework": "NIST CSF",
        "sections": [
            "Identify",
            "Protect",
            "Detect",
            "Respond",
            "Recover",
        ],
    },
]


@utility_router.get("/audits/sampling-calculator")
async def sampling_calculator(
    current_user: AnyInternalUser,
    population_size: int = Query(..., ge=1),
    confidence_level: float = Query(95.0),
    margin_of_error: float = Query(5.0),
):
    """Calculate the required audit sample size for a given population.

    Uses the standard formula: n = (Z^2 * p * (1-p)) / E^2, adjusted
    for finite population with the correction factor:
    n_adj = n / (1 + (n - 1) / N)
    """
    z = Z_VALUES.get(confidence_level)
    if z is None:
        closest = min(Z_VALUES.keys(), key=lambda k: abs(k - confidence_level))
        z = Z_VALUES[closest]

    p = 0.5
    e = margin_of_error / 100.0

    if e <= 0:
        return {
            "population_size": population_size,
            "confidence_level": confidence_level,
            "margin_of_error": margin_of_error,
            "sample_size": population_size,
            "formula_used": "margin_of_error is 0 — full population required",
        }

    # Infinite population sample size
    n_infinite = (z ** 2 * p * (1 - p)) / (e ** 2)

    # Finite population correction
    n_adjusted = n_infinite / (1 + (n_infinite - 1) / population_size)

    sample_size = min(math.ceil(n_adjusted), population_size)

    return {
        "population_size": population_size,
        "confidence_level": confidence_level,
        "margin_of_error": margin_of_error,
        "sample_size": sample_size,
        "formula_used": (
            f"n = (Z^2 * p * (1-p)) / E^2 with finite correction; "
            f"Z={z}, p=0.5, E={e}, N={population_size}"
        ),
    }


@utility_router.get("/audits/workpaper-templates")
async def list_workpaper_templates(
    current_user: AnyInternalUser,
):
    """Return available workpaper templates."""
    return WORKPAPER_TEMPLATES


@router.get("", response_model=PaginatedResponse)
async def list_audits(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    items, total = await audit_service.list_audits(db, org_id, page, page_size)
    return PaginatedResponse(
        items=[AuditResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=AuditResponse, status_code=201)
async def create_audit(org_id: VerifiedOrgId, data: AuditCreate, db: DB, current_user: ComplianceUser):
    return await audit_service.create_audit(db, org_id, data)


@router.get("/readiness", response_model=ReadinessScoreResponse)
async def get_readiness_score(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await audit_service.compute_readiness_score(db, org_id)


@router.get("/{audit_id}/workpapers")
async def generate_workpapers(
    org_id: VerifiedOrgId,
    audit_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
):
    """Generate a workpaper JSON for the given audit.

    Aggregates audit metadata, controls, evidence, and findings into a single
    structured document that auditors can use as a working paper.
    """
    audit = await audit_service.get_audit(db, org_id, audit_id)

    # Load controls for the org
    controls_result = await db.execute(
        select(Control).where(
            Control.org_id == org_id,
            Control.deleted_at.is_(None),
        )
    )
    controls = list(controls_result.scalars().all())

    # Load evidence for the org
    evidence_result = await db.execute(
        select(Evidence).where(
            Evidence.org_id == org_id,
            Evidence.deleted_at.is_(None),
        )
    )
    evidence_items = list(evidence_result.scalars().all())

    # Count evidence per control
    evidence_by_control: dict[str, int] = {}
    evidence_by_status: dict[str, int] = {}
    for ev in evidence_items:
        if ev.control_id is not None:
            key = str(ev.control_id)
            evidence_by_control[key] = evidence_by_control.get(key, 0) + 1
        status = ev.status or "unknown"
        evidence_by_status[status] = evidence_by_status.get(status, 0) + 1

    controls_payload: list[dict] = []
    implemented_count = 0
    for control in controls:
        evidence_count = evidence_by_control.get(str(control.id), 0)
        if control.status == "implemented":
            implemented_count += 1
        controls_payload.append(
            {
                "id": str(control.id),
                "title": control.title,
                "status": control.status,
                "evidence_count": evidence_count,
                "has_gap": evidence_count == 0 or control.status != "implemented",
            }
        )

    # Load findings for this audit
    findings_result = await db.execute(
        select(AuditFinding).where(
            AuditFinding.audit_id == audit_id,
            AuditFinding.org_id == org_id,
            AuditFinding.deleted_at.is_(None),
        )
    )
    findings = list(findings_result.scalars().all())
    findings_payload = [
        {
            "id": str(f.id),
            "title": f.title,
            "severity": f.severity,
            "status": f.status,
        }
        for f in findings
    ]

    framework_name: str | None = None
    framework = getattr(audit, "framework", None)
    if framework is not None:
        framework_name = getattr(framework, "name", None)

    return {
        "audit": {
            "id": str(audit.id),
            "name": audit.title,
            "framework": framework_name,
            "start_date": (
                audit.scheduled_start.isoformat()
                if audit.scheduled_start is not None
                else None
            ),
            "end_date": (
                audit.scheduled_end.isoformat()
                if audit.scheduled_end is not None
                else None
            ),
            "status": audit.status,
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "controls": controls_payload,
        "evidence_summary": {
            "total": len(evidence_items),
            "by_status": evidence_by_status,
        },
        "findings": findings_payload,
        "summary": {
            "total_controls": len(controls),
            "implemented": implemented_count,
            "total_evidence": len(evidence_items),
            "total_findings": len(findings),
        },
    }


@router.get("/{audit_id}", response_model=AuditResponse)
async def get_audit(org_id: VerifiedOrgId, audit_id: UUID, db: DB, current_user: AnyInternalUser):
    return await audit_service.get_audit(db, org_id, audit_id)


@router.patch("/{audit_id}", response_model=AuditResponse)
async def update_audit(
    org_id: VerifiedOrgId, audit_id: UUID, data: AuditUpdate,
    db: DB, current_user: ComplianceUser,
):
    return await audit_service.update_audit(db, org_id, audit_id, data)


@router.delete("/{audit_id}", status_code=204)
async def delete_audit(org_id: VerifiedOrgId, audit_id: UUID, db: DB, current_user: ComplianceUser):
    await audit_service.delete_audit(db, org_id, audit_id)


# --- Findings ---
@router.get("/{audit_id}/findings", response_model=list[FindingResponse])
async def list_findings(
    org_id: VerifiedOrgId, audit_id: UUID, db: DB, current_user: AnyInternalUser
):
    return await audit_service.list_findings(db, audit_id, org_id)


@router.post("/{audit_id}/findings", response_model=FindingResponse, status_code=201)
async def create_finding(
    org_id: VerifiedOrgId, audit_id: UUID, data: FindingCreate,
    db: DB, current_user: ComplianceUser,
):
    return await audit_service.create_finding(db, org_id, audit_id, data)


@router.patch("/{audit_id}/findings/{finding_id}", response_model=FindingResponse)
async def update_finding(
    org_id: VerifiedOrgId, audit_id: UUID, finding_id: UUID,
    data: FindingUpdate, db: DB, current_user: ComplianceUser,
):
    return await audit_service.update_finding(db, org_id, finding_id, data)


# --- Access Tokens ---
@router.get("/{audit_id}/tokens", response_model=list[TokenResponse])
async def list_tokens(
    org_id: VerifiedOrgId, audit_id: UUID, db: DB, current_user: ComplianceUser
):
    return await auditor_access_service.list_tokens(db, audit_id)


@router.post("/{audit_id}/tokens", response_model=TokenResponse, status_code=201)
async def create_token(
    org_id: VerifiedOrgId, audit_id: UUID, data: TokenCreate,
    db: DB, current_user: ComplianceUser,
):
    token_model, raw_token = await auditor_access_service.create_access_token(
        db, org_id, audit_id, data
    )
    response = TokenResponse.model_validate(token_model)
    response.token = raw_token  # Only visible once
    return response


@router.delete("/{audit_id}/tokens/{token_id}", status_code=204)
async def revoke_token(
    org_id: VerifiedOrgId, audit_id: UUID, token_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    await auditor_access_service.revoke_token(db, org_id, audit_id, token_id)


# --- Evidence Package ---
@router.get("/{audit_id}/evidence-package")
async def get_evidence_package(
    org_id: VerifiedOrgId, audit_id: UUID, db: DB, current_user: AnyInternalUser
):
    await audit_service.get_audit(db, org_id, audit_id)  # verify exists
    return await audit_service.generate_evidence_package(db, org_id)
