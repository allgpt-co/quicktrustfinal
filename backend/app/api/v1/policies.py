import io
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import select

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import BadRequestError, NotFoundError
from app.schemas.common import PaginatedResponse
from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyStatsResponse,
)
from app.services import policy_service

router = APIRouter(prefix="/organizations/{org_id}/policies", tags=["policies"])


@router.get("", response_model=PaginatedResponse)
async def list_policies(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    policies, total = await policy_service.list_policies(
        db, org_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[PolicyResponse.model_validate(p) for p in policies],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=PolicyResponse, status_code=201)
async def create_policy(
    org_id: VerifiedOrgId, data: PolicyCreate, db: DB, current_user: ComplianceUser
):
    item = await policy_service.create_policy(db, org_id, data)
    await log_audit(db, current_user, "create", "policy", str(item.id), org_id)
    return item


@router.get("/stats", response_model=PolicyStatsResponse)
async def get_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await policy_service.get_policy_stats(db, org_id)


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: AnyInternalUser
):
    return await policy_service.get_policy(db, org_id, policy_id)


@router.patch("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    org_id: VerifiedOrgId,
    policy_id: UUID,
    data: PolicyUpdate,
    db: DB,
    current_user: ComplianceUser,
):
    item = await policy_service.update_policy(db, org_id, policy_id, data)
    await log_audit(db, current_user, "update", "policy", str(policy_id), org_id)
    return item


@router.delete("/{policy_id}", status_code=204)
async def delete_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    await policy_service.delete_policy(db, org_id, policy_id)
    await log_audit(db, current_user, "delete", "policy", str(policy_id), org_id)


# ---------------------------------------------------------------------------
# Policy workflow endpoints
# ---------------------------------------------------------------------------


@router.post("/{policy_id}/submit-for-review", response_model=PolicyResponse)
async def submit_for_review(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Submit a draft policy for review."""
    item = await policy_service.submit_for_review(db, org_id, policy_id, current_user.id)
    await log_audit(db, current_user, "submit_for_review", "policy", str(policy_id), org_id)
    return item


@router.post("/{policy_id}/approve", response_model=PolicyResponse)
async def approve_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Approve a policy that is in review."""
    item = await policy_service.approve_policy(db, org_id, policy_id, current_user.id)
    await log_audit(db, current_user, "approve", "policy", str(policy_id), org_id)
    return item


@router.post("/{policy_id}/publish", response_model=PolicyResponse)
async def publish_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Publish an approved policy."""
    item = await policy_service.publish_policy(db, org_id, policy_id, current_user.id)
    await log_audit(db, current_user, "publish", "policy", str(policy_id), org_id)
    return item


@router.post("/{policy_id}/archive", response_model=PolicyResponse)
async def archive_policy(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: ComplianceUser
):
    """Archive a policy."""
    item = await policy_service.archive_policy(db, org_id, policy_id)
    await log_audit(db, current_user, "archive", "policy", str(policy_id), org_id)
    return item


# ---------------------------------------------------------------------------
# Policy export endpoints (PDF / DOCX)
# ---------------------------------------------------------------------------


@router.get("/{policy_id}/export/pdf")
async def export_policy_pdf(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: AnyInternalUser
):
    """Export a policy as a PDF document."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors

    policy = await policy_service.get_policy(db, org_id, policy_id)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("PolicyTitle", parent=styles["Title"], fontSize=20, spaceAfter=20)
    body_style = styles["BodyText"]

    elements = []

    # Title
    elements.append(Paragraph(policy.title, title_style))
    elements.append(Spacer(1, 12))

    # Metadata table
    meta_data = [
        ["Version", str(policy.version)],
        ["Status", policy.status.replace("_", " ").title()],
        ["Classification", policy.classification or "N/A"],
        ["Created", policy.created_at.strftime("%Y-%m-%d") if policy.created_at else "N/A"],
        ["Last Updated", policy.updated_at.strftime("%Y-%m-%d") if policy.updated_at else "N/A"],
    ]
    if policy.approved_at:
        meta_data.append(["Approved", policy.approved_at.strftime("%Y-%m-%d")])
    if policy.published_at:
        meta_data.append(["Published", policy.published_at.strftime("%Y-%m-%d")])
    if policy.next_review_date:
        meta_data.append(["Next Review", policy.next_review_date.strftime("%Y-%m-%d")])

    meta_table = Table(meta_data, colWidths=[1.8 * inch, 4.5 * inch])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.Color(0.93, 0.93, 0.93)),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 24))

    # Content
    elements.append(Paragraph("Policy Content", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    content = policy.content or "No content."
    for para in content.split("\n\n"):
        para = para.strip()
        if para:
            # Escape XML-sensitive characters for ReportLab
            safe_para = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(safe_para, body_style))
            elements.append(Spacer(1, 6))

    doc.build(elements)
    buffer.seek(0)

    safe_title = policy.title.replace(" ", "_")[:50]
    filename = f"{safe_title}_v{policy.version}.pdf"

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{policy_id}/export/docx")
async def export_policy_docx(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: AnyInternalUser
):
    """Export a policy as a DOCX (Word) document."""
    from docx import Document
    from docx.shared import Inches, Pt

    policy = await policy_service.get_policy(db, org_id, policy_id)

    doc = Document()

    # Title
    doc.add_heading(policy.title, level=1)

    # Metadata table
    table = doc.add_table(rows=0, cols=2)
    table.style = "Light Grid Accent 1"

    meta_rows = [
        ("Version", str(policy.version)),
        ("Status", policy.status.replace("_", " ").title()),
        ("Classification", policy.classification or "N/A"),
        ("Owner", str(policy.owner_id) if policy.owner_id else "N/A"),
        ("Created", policy.created_at.strftime("%Y-%m-%d") if policy.created_at else "N/A"),
        ("Last Updated", policy.updated_at.strftime("%Y-%m-%d") if policy.updated_at else "N/A"),
    ]
    if policy.approved_by_id:
        meta_rows.append(("Approved By", str(policy.approved_by_id)))
    if policy.approved_at:
        meta_rows.append(("Approved", policy.approved_at.strftime("%Y-%m-%d")))
    if policy.published_at:
        meta_rows.append(("Published", policy.published_at.strftime("%Y-%m-%d")))
    if policy.next_review_date:
        meta_rows.append(("Next Review", policy.next_review_date.strftime("%Y-%m-%d")))

    for label, value in meta_rows:
        row = table.add_row()
        row.cells[0].text = label
        row.cells[1].text = value

    # Set column widths
    for row in table.rows:
        row.cells[0].width = Inches(2)
        row.cells[1].width = Inches(4.5)

    doc.add_paragraph("")  # spacer

    # Content
    doc.add_heading("Policy Content", level=2)
    content = policy.content or "No content."
    for para in content.split("\n\n"):
        para = para.strip()
        if para:
            doc.add_paragraph(para)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    safe_title = policy.title.replace(" ", "_")[:50]
    filename = f"{safe_title}_v{policy.version}.docx"

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------------------------------------------------------------------------
# Multi-level approval chain endpoints
# ---------------------------------------------------------------------------


class ApprovalStepCreate(PydanticBaseModel):
    approver_role: str
    step_order: int
    approver_id: UUID | None = None


class ApprovalStepResponse(PydanticBaseModel):
    id: UUID
    org_id: UUID
    policy_id: UUID
    step_order: int
    approver_role: str
    approver_id: UUID | None = None
    status: str
    approved_at: datetime | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApprovalActionBody(PydanticBaseModel):
    notes: str | None = None


@router.get("/{policy_id}/approval-chain", response_model=list[ApprovalStepResponse])
async def list_approval_chain(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: AnyInternalUser
):
    """List all approval chain steps for a policy, ordered by step_order."""
    from app.models.approval_chain import ApprovalChain

    # Ensure the policy exists
    await policy_service.get_policy(db, org_id, policy_id)

    result = await db.execute(
        select(ApprovalChain)
        .where(ApprovalChain.org_id == org_id, ApprovalChain.policy_id == policy_id)
        .order_by(ApprovalChain.step_order)
    )
    return list(result.scalars().all())


@router.post("/{policy_id}/approval-chain", response_model=ApprovalStepResponse, status_code=201)
async def add_approval_step(
    org_id: VerifiedOrgId,
    policy_id: UUID,
    data: ApprovalStepCreate,
    db: DB,
    current_user: ComplianceUser,
):
    """Add an approval step to a policy's approval chain."""
    from app.models.approval_chain import ApprovalChain

    # Ensure the policy exists
    await policy_service.get_policy(db, org_id, policy_id)

    step = ApprovalChain(
        org_id=org_id,
        policy_id=policy_id,
        step_order=data.step_order,
        approver_role=data.approver_role,
        approver_id=data.approver_id,
        status="pending",
    )
    db.add(step)
    await db.commit()
    await db.refresh(step)
    await log_audit(db, current_user, "add_approval_step", "policy", str(policy_id), org_id)
    return step


@router.post("/{policy_id}/approval-chain/{step_id}/approve", response_model=ApprovalStepResponse)
async def approve_chain_step(
    org_id: VerifiedOrgId,
    policy_id: UUID,
    step_id: UUID,
    body: ApprovalActionBody,
    db: DB,
    current_user: ComplianceUser,
):
    """Approve a specific step in the approval chain."""
    from app.models.approval_chain import ApprovalChain

    result = await db.execute(
        select(ApprovalChain).where(
            ApprovalChain.id == step_id,
            ApprovalChain.org_id == org_id,
            ApprovalChain.policy_id == policy_id,
        )
    )
    step = result.scalar_one_or_none()
    if not step:
        raise NotFoundError(f"Approval step {step_id} not found")
    if step.status != "pending":
        raise BadRequestError(f"Step is already '{step.status}', cannot approve.")

    step.status = "approved"
    step.approved_at = datetime.now(timezone.utc)
    step.approver_id = current_user.id
    step.notes = body.notes
    await db.commit()
    await db.refresh(step)

    # Check if ALL steps for this policy are now approved
    all_result = await db.execute(
        select(ApprovalChain).where(
            ApprovalChain.org_id == org_id, ApprovalChain.policy_id == policy_id
        )
    )
    all_steps = list(all_result.scalars().all())
    if all_steps and all(s.status == "approved" for s in all_steps):
        # Auto-approve the policy
        policy = await policy_service.get_policy(db, org_id, policy_id)
        policy.status = "approved"
        policy.approved_by_id = current_user.id
        policy.approved_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(policy)

    await log_audit(db, current_user, "approve_chain_step", "policy", str(policy_id), org_id)
    return step


@router.post("/{policy_id}/approval-chain/{step_id}/reject", response_model=ApprovalStepResponse)
async def reject_chain_step(
    org_id: VerifiedOrgId,
    policy_id: UUID,
    step_id: UUID,
    body: ApprovalActionBody,
    db: DB,
    current_user: ComplianceUser,
):
    """Reject a specific step in the approval chain."""
    from app.models.approval_chain import ApprovalChain

    result = await db.execute(
        select(ApprovalChain).where(
            ApprovalChain.id == step_id,
            ApprovalChain.org_id == org_id,
            ApprovalChain.policy_id == policy_id,
        )
    )
    step = result.scalar_one_or_none()
    if not step:
        raise NotFoundError(f"Approval step {step_id} not found")
    if step.status != "pending":
        raise BadRequestError(f"Step is already '{step.status}', cannot reject.")

    step.status = "rejected"
    step.approver_id = current_user.id
    step.notes = body.notes
    await db.commit()
    await db.refresh(step)

    await log_audit(db, current_user, "reject_chain_step", "policy", str(policy_id), org_id)
    return step
