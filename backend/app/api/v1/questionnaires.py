from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.questionnaire import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireDetailResponse,
    QuestionResponseCreate,
    QuestionResponseUpdate,
    QuestionResponseRead,
    QuestionnaireStatsResponse,
)
from app.services import questionnaire_service

router = APIRouter(
    prefix="/organizations/{org_id}/questionnaires",
    tags=["questionnaires"],
)


# ---------------------------------------------------------------------------
# Built-in industry questionnaire templates
# ---------------------------------------------------------------------------
SIG_LITE_QUESTIONS: tuple[str, ...] = (
    "Does your organization have a documented information security policy reviewed at least annually?",
    "Is multi-factor authentication (MFA) required for remote access to production systems?",
    "Do you perform annual penetration testing by a qualified third party?",
    "Is sensitive data encrypted at rest using AES-256 or equivalent?",
    "Do you have a documented incident response plan?",
    "Are backups tested for successful restoration at least quarterly?",
    "Is there a formal change management process for production changes?",
    "Do you conduct background checks on all employees with access to sensitive data?",
    "Are all endpoints protected with anti-malware software?",
    "Do you have a vendor risk management program?",
)

CAIQ_QUESTIONS: tuple[str, ...] = (
    "Are cryptographic controls used to protect data in transit (TLS 1.2+)?",
    "Is there a formal change management process with approval workflows?",
    "Do you segment cloud environments (production, staging, development)?",
    "Is access to cloud consoles restricted via MFA and IP whitelisting?",
    "Do you monitor cloud resources with CSPM tools?",
    "Is there a documented process for credential rotation?",
    "Are audit logs from cloud providers retained for at least 1 year?",
    "Do you have a disaster recovery plan tested annually?",
)

HECVAT_QUESTIONS: tuple[str, ...] = (
    "Is sensitive data encrypted at rest using AES-256 or equivalent?",
    "Do you have a documented disaster recovery plan with defined RPO/RTO?",
    "Is there a formal vulnerability management program?",
    "Do you conduct regular security awareness training for all employees?",
    "Are third-party security assessments (SOC 2, ISO 27001) current?",
    "Is there a documented data retention and destruction policy?",
    "Do you have a business continuity plan tested annually?",
    "Are production systems monitored 24/7 for security events?",
)

TEMPLATE_DEFINITIONS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("SIG Lite", "Standardized Information Gathering — Lite version", SIG_LITE_QUESTIONS),
    ("CAIQ", "Consensus Assessments Initiative Questionnaire (CSA)", CAIQ_QUESTIONS),
    ("HECVAT", "Higher Education Community Vendor Assessment Tool", HECVAT_QUESTIONS),
)


@router.post("/seed-templates")
async def seed_questionnaire_templates(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser
):
    """Seed industry-standard questionnaire templates (SIG Lite, CAIQ, HECVAT)."""
    from app.models.questionnaire import Questionnaire

    created: list[dict] = []
    for name, description, questions in TEMPLATE_DEFINITIONS:
        question_payload = [
            {
                "question_id": f"q{i + 1}",
                "question_text": text,
                "question_type": "text",
                "category": "general",
                "description": description,
            }
            for i, text in enumerate(questions)
        ]
        questionnaire = Questionnaire(
            org_id=org_id,
            title=name,
            source=description,
            status="draft",
            questions=question_payload,
            total_questions=len(question_payload),
        )
        db.add(questionnaire)
        created.append({"name": name, "question_count": len(question_payload)})

    await db.commit()
    return {"seeded": len(created), "templates": created}


@router.get("", response_model=PaginatedResponse)
async def list_questionnaires(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await questionnaire_service.list_questionnaires(
        db, org_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[QuestionnaireDetailResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=QuestionnaireDetailResponse, status_code=201)
async def create_questionnaire(org_id: VerifiedOrgId, data: QuestionnaireCreate, db: DB, current_user: ComplianceUser):
    return await questionnaire_service.create_questionnaire(db, org_id, data)


@router.get("/stats", response_model=QuestionnaireStatsResponse)
async def get_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await questionnaire_service.get_questionnaire_stats(db, org_id)


@router.get("/{questionnaire_id}", response_model=QuestionnaireDetailResponse)
async def get_questionnaire(org_id: VerifiedOrgId, questionnaire_id: UUID, db: DB, current_user: AnyInternalUser):
    return await questionnaire_service.get_questionnaire(db, org_id, questionnaire_id)


@router.patch("/{questionnaire_id}", response_model=QuestionnaireDetailResponse)
async def update_questionnaire(
    org_id: VerifiedOrgId, questionnaire_id: UUID, data: QuestionnaireUpdate, db: DB, current_user: ComplianceUser
):
    return await questionnaire_service.update_questionnaire(db, org_id, questionnaire_id, data)


@router.delete("/{questionnaire_id}", status_code=204)
async def delete_questionnaire(org_id: VerifiedOrgId, questionnaire_id: UUID, db: DB, current_user: ComplianceUser):
    await questionnaire_service.delete_questionnaire(db, org_id, questionnaire_id)


@router.post("/{questionnaire_id}/auto-fill", response_model=MessageResponse)
async def auto_fill(org_id: VerifiedOrgId, questionnaire_id: UUID, db: DB, current_user: ComplianceUser):
    count = await questionnaire_service.auto_fill(db, org_id, questionnaire_id)
    return MessageResponse(message=f"Auto-filled {count} responses")


@router.get("/{questionnaire_id}/responses/{question_id}", response_model=QuestionResponseRead)
async def get_response(
    org_id: VerifiedOrgId, questionnaire_id: UUID, question_id: str, db: DB, current_user: AnyInternalUser
):
    return await questionnaire_service.get_response(db, org_id, questionnaire_id, question_id)


@router.put("/{questionnaire_id}/responses/{question_id}", response_model=QuestionResponseRead)
async def upsert_response(
    org_id: VerifiedOrgId, questionnaire_id: UUID, question_id: str,
    data: QuestionResponseCreate, db: DB, current_user: ComplianceUser,
):
    data.question_id = question_id
    return await questionnaire_service.upsert_response(db, org_id, questionnaire_id, data)


@router.patch("/{questionnaire_id}/responses/{question_id}/approve", response_model=QuestionResponseRead)
async def approve_response(
    org_id: VerifiedOrgId, questionnaire_id: UUID, question_id: str, db: DB, current_user: ComplianceUser
):
    data = QuestionResponseUpdate(is_approved=True)
    return await questionnaire_service.update_response(
        db, org_id, questionnaire_id, question_id, data, approved_by_id=current_user.id
    )
