"""Approved response library — reusable answers to common security questions.

Compliance teams can build a library of pre-approved responses that can be
used to auto-fill questionnaires (SIG Lite, CAIQ, HECVAT, etc.).
"""
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import or_, select

from app.core.dependencies import DB, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import NotFoundError
from app.models.approved_response import ApprovedResponse


router = APIRouter(
    prefix="/organizations/{org_id}/response-library",
    tags=["response-library"],
)


# ---------------------------------------------------------------------------
# Seed data — 15 canonical security answers
# ---------------------------------------------------------------------------
SEED_RESPONSES: tuple[dict, ...] = (
    {
        "category": "encryption",
        "question": "How do you encrypt data at rest?",
        "answer": (
            "All data at rest is encrypted using AES-256-GCM. Database-level encryption is enabled "
            "via the storage layer (AWS RDS/KMS), and application-level field encryption is used for "
            "sensitive PII fields. Encryption keys are managed through AWS KMS with automatic rotation "
            "every 365 days."
        ),
        "tags": ["aes-256", "kms", "data-at-rest"],
    },
    {
        "category": "encryption",
        "question": "How do you encrypt data in transit?",
        "answer": (
            "All data in transit is encrypted using TLS 1.3 (TLS 1.2 minimum). We enforce HSTS with a "
            "1-year max-age, use modern cipher suites, and disable legacy protocols. Internal "
            "service-to-service communication also uses mTLS."
        ),
        "tags": ["tls", "https", "mtls"],
    },
    {
        "category": "access_control",
        "question": "How do you manage user access?",
        "answer": (
            "We use role-based access control (RBAC) with least-privilege principles. All access is "
            "managed through our identity provider (Okta/Keycloak) with SSO and MFA enforced. Access "
            "reviews are conducted quarterly, and privileged access requires just-in-time approval."
        ),
        "tags": ["rbac", "mfa", "sso"],
    },
    {
        "category": "incident_response",
        "question": "What is your incident response process?",
        "answer": (
            "Our incident response plan follows NIST SP 800-61 with 4 phases: (1) Preparation — "
            "documented runbooks and on-call rotations, (2) Detection & Analysis — 24/7 SIEM monitoring "
            "with automated alerting, (3) Containment, Eradication & Recovery — defined escalation "
            "paths and communication templates, (4) Post-Incident — root cause analysis and lessons "
            "learned within 5 business days."
        ),
        "tags": ["nist", "siem", "runbooks"],
    },
    {
        "category": "compliance",
        "question": "Do you have a SOC 2 report?",
        "answer": (
            "Yes, we maintain SOC 2 Type II certification, audited annually by a Big 4 auditing firm. "
            "Our report covers all five trust service criteria: Security, Availability, Processing "
            "Integrity, Confidentiality, and Privacy. The report is available under NDA upon request."
        ),
        "tags": ["soc2", "audit", "certification"],
    },
    {
        "category": "compliance",
        "question": "Are you GDPR compliant?",
        "answer": (
            "Yes, we are fully GDPR compliant. We have appointed a DPO, maintain records of processing "
            "activities, implement privacy by design, and provide all data subject rights (access, "
            "rectification, erasure, portability). Our DPA is available for all customers processing "
            "EU personal data."
        ),
        "tags": ["gdpr", "dpo", "dpa"],
    },
    {
        "category": "business_continuity",
        "question": "What is your RPO and RTO?",
        "answer": (
            "Our Recovery Point Objective (RPO) is 1 hour (maximum data loss) and our Recovery Time "
            "Objective (RTO) is 4 hours (maximum downtime). These targets are validated through "
            "quarterly DR drills with documented results."
        ),
        "tags": ["rpo", "rto", "dr"],
    },
    {
        "category": "business_continuity",
        "question": "Do you have a disaster recovery plan?",
        "answer": (
            "Yes, we maintain a comprehensive disaster recovery plan with multi-region failover "
            "capability. Backups are taken daily, stored in a geographically separate region, and "
            "tested quarterly through full DR drills. The plan is reviewed and updated annually."
        ),
        "tags": ["dr", "backups", "multi-region"],
    },
    {
        "category": "data_privacy",
        "question": "How do you handle data deletion requests?",
        "answer": (
            "We honor all data deletion requests within 30 days (GDPR Article 17). Our process "
            "includes: (1) identity verification, (2) data discovery across all systems, (3) secure "
            "deletion with cryptographic erasure, (4) confirmation to the data subject, (5) audit log "
            "retention per legal requirements."
        ),
        "tags": ["gdpr", "deletion", "privacy"],
    },
    {
        "category": "data_privacy",
        "question": "Where is customer data stored?",
        "answer": (
            "Customer data is stored in AWS data centers in the region selected by the customer "
            "(US-East, US-West, EU-West, AP-Southeast). We offer data residency options for regulated "
            "industries and support customer-managed encryption keys (CMK) for enterprise customers."
        ),
        "tags": ["data-residency", "aws", "cmk"],
    },
    {
        "category": "vulnerability_management",
        "question": "How often do you conduct penetration testing?",
        "answer": (
            "We conduct annual third-party penetration testing by a qualified firm (CREST or OSCP "
            "certified). Critical findings are remediated within 30 days, high within 60 days, and "
            "medium within 90 days. Reports are available under NDA to enterprise customers."
        ),
        "tags": ["pentest", "crest", "oscp"],
    },
    {
        "category": "vulnerability_management",
        "question": "How do you manage security patches?",
        "answer": (
            "Security patches are applied based on CVSS severity: Critical within 7 days, High within "
            "30 days, Medium within 60 days, Low within 90 days. We use automated vulnerability "
            "scanning (Trivy, Snyk) and subscribe to security advisories for all major dependencies."
        ),
        "tags": ["patching", "cvss", "cve"],
    },
    {
        "category": "secure_development",
        "question": "Do you conduct security code reviews?",
        "answer": (
            "Yes, all code changes require peer review before merging. Security-sensitive changes "
            "require review by a senior engineer or security team member. We use automated SAST tools "
            "(Semgrep, CodeQL) in our CI/CD pipeline to catch vulnerabilities early."
        ),
        "tags": ["sast", "code-review", "semgrep"],
    },
    {
        "category": "training",
        "question": "Do you conduct security awareness training?",
        "answer": (
            "Yes, all employees complete security awareness training within 30 days of onboarding and "
            "annually thereafter. Training covers phishing recognition, password security, data "
            "handling, and incident reporting. We also conduct quarterly phishing simulations."
        ),
        "tags": ["training", "awareness", "phishing"],
    },
    {
        "category": "monitoring",
        "question": "How do you monitor for security events?",
        "answer": (
            "We use a centralized SIEM (Datadog/Splunk) to collect and analyze logs from all systems. "
            "Real-time alerts notify our 24/7 on-call team of suspicious activity. Logs are retained "
            "for 1 year (hot) and 7 years (cold storage) to support forensic analysis."
        ),
        "tags": ["siem", "logging", "monitoring"],
    },
)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class ApprovedResponseCreate(PydanticBaseModel):
    question: str
    answer: str
    category: str
    tags: list[str] = []


class ApprovedResponseUpdate(PydanticBaseModel):
    question: str | None = None
    answer: str | None = None
    category: str | None = None
    tags: list[str] | None = None


def _serialize(response: ApprovedResponse) -> dict:
    return {
        "id": str(response.id),
        "question": response.question,
        "answer": response.answer,
        "category": response.category,
        "tags": list(response.tags) if response.tags else [],
        "use_count": response.use_count,
        "approved_at": response.approved_at.isoformat() if response.approved_at else None,
        "created_at": response.created_at.isoformat() if response.created_at else None,
    }


# ---------------------------------------------------------------------------
# Routes — static routes come before /{id}
# ---------------------------------------------------------------------------
@router.get("")
async def list_responses(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    search: str | None = Query(None),
    category: str | None = Query(None),
):
    query = select(ApprovedResponse).where(ApprovedResponse.org_id == org_id)
    if search:
        like = f"%{search}%"
        query = query.where(
            or_(
                ApprovedResponse.question.ilike(like),
                ApprovedResponse.answer.ilike(like),
            )
        )
    if category:
        query = query.where(ApprovedResponse.category == category)
    query = query.order_by(
        ApprovedResponse.use_count.desc(), ApprovedResponse.created_at.desc()
    )
    result = await db.execute(query)
    items = list(result.scalars().all())
    return {
        "total": len(items),
        "items": [_serialize(item) for item in items],
    }


@router.post("", status_code=201)
async def create_response(
    org_id: VerifiedOrgId,
    data: ApprovedResponseCreate,
    db: DB,
    current_user: ComplianceUser,
):
    response = ApprovedResponse(
        org_id=org_id,
        question=data.question,
        answer=data.answer,
        category=data.category,
        tags=list(data.tags),
        approved_by=current_user.id,
        approved_at=datetime.now(timezone.utc),
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return {"id": str(response.id), "message": "Response added to library"}


@router.post("/seed")
async def seed_response_library(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser
):
    """Load the 15 canonical seed responses into the org's library."""
    count = 0
    for data in SEED_RESPONSES:
        response = ApprovedResponse(
            org_id=org_id,
            question=data["question"],
            answer=data["answer"],
            category=data["category"],
            tags=list(data["tags"]),
            approved_by=current_user.id,
            approved_at=datetime.now(timezone.utc),
        )
        db.add(response)
        count += 1
    await db.commit()
    return {"seeded": count, "message": f"Seeded {count} approved responses"}


@router.patch("/{response_id}")
async def update_response(
    org_id: VerifiedOrgId,
    response_id: UUID,
    data: ApprovedResponseUpdate,
    db: DB,
    current_user: ComplianceUser,
):
    result = await db.execute(
        select(ApprovedResponse).where(
            ApprovedResponse.id == response_id,
            ApprovedResponse.org_id == org_id,
        )
    )
    response = result.scalar_one_or_none()
    if not response:
        raise NotFoundError("Response not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(response, field, value)

    await db.commit()
    return {"message": "Response updated"}


@router.delete("/{response_id}", status_code=204)
async def delete_response(
    org_id: VerifiedOrgId,
    response_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    result = await db.execute(
        select(ApprovedResponse).where(
            ApprovedResponse.id == response_id,
            ApprovedResponse.org_id == org_id,
        )
    )
    response = result.scalar_one_or_none()
    if not response:
        raise NotFoundError("Response not found")
    await db.delete(response)
    await db.commit()
