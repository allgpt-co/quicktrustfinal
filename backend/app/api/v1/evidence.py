from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from fastapi.responses import RedirectResponse

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import BadRequestError
from app.schemas.common import PaginatedResponse
from app.schemas.evidence import EvidenceCreate, EvidenceReject, EvidenceResponse
from app.services import evidence_service

EVIDENCE_ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/csv",
    "application/json",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}
EVIDENCE_MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

router = APIRouter(prefix="/organizations/{org_id}/evidence", tags=["evidence"])


@router.get("", response_model=PaginatedResponse)
async def list_evidence(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    control_id: UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await evidence_service.list_evidence(
        db, org_id, control_id=control_id, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[EvidenceResponse.model_validate(e) for e in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=EvidenceResponse, status_code=201)
async def create_evidence(org_id: VerifiedOrgId, data: EvidenceCreate, db: DB, current_user: ComplianceUser):
    item = await evidence_service.create_evidence(db, org_id, data)
    await log_audit(db, current_user, "create", "evidence", str(item.id), org_id)
    return item


@router.get("/{evidence_id}", response_model=EvidenceResponse)
async def get_evidence(org_id: VerifiedOrgId, evidence_id: UUID, db: DB, current_user: AnyInternalUser):
    return await evidence_service.get_evidence(db, org_id, evidence_id)


@router.post("/{evidence_id}/upload", response_model=EvidenceResponse)
async def upload_evidence_file(
    org_id: VerifiedOrgId,
    evidence_id: UUID,
    db: DB,
    current_user: ComplianceUser,
    file: UploadFile = File(...),
):
    """Upload an evidence file to object storage and associate it with the evidence record."""
    from app.core.hashing import compute_sha256
    from app.core.storage import upload_file

    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)

    # Validate content type
    if file.content_type not in EVIDENCE_ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' is not allowed for evidence upload.",
        )

    # Read with size limit (chunked to avoid loading huge files into memory)
    contents = bytearray()
    while True:
        chunk = await file.read(8192)
        if not chunk:
            break
        contents.extend(chunk)
        if len(contents) > EVIDENCE_MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum size of {EVIDENCE_MAX_FILE_SIZE // (1024 * 1024)}MB.",
            )
    contents = bytes(contents)

    # Compute SHA-256 hash of the uploaded file for integrity tracking
    file_hash = compute_sha256(contents)

    # Determine content type
    content_type = file.content_type or "application/octet-stream"
    original_name = file.filename or "upload"

    object_name = f"evidence/{org_id}/{evidence_id}/{original_name}"
    file_url = upload_file(
        bucket="quicktrust-evidence",
        object_name=object_name,
        data=contents,
        content_type=content_type,
    )

    if not file_url:
        raise BadRequestError("File storage is currently unavailable. Upload failed.")

    evidence.file_url = file_url
    evidence.file_name = original_name
    evidence.artifact_hash = file_hash
    await db.commit()
    await db.refresh(evidence)

    await log_audit(db, current_user, "upload_file", "evidence", str(evidence_id), org_id)
    return evidence


@router.get("/{evidence_id}/download")
async def download_evidence_file(
    org_id: VerifiedOrgId, evidence_id: UUID, db: DB, current_user: AnyInternalUser
):
    """Download an evidence file via presigned URL redirect."""
    from app.core.storage import get_presigned_url

    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)

    if not evidence.file_url:
        raise BadRequestError("No file has been uploaded for this evidence item.")

    # file_url is stored as "bucket/object_name"
    parts = evidence.file_url.split("/", 1)
    if len(parts) != 2:
        raise BadRequestError("Invalid file reference on this evidence item.")

    bucket, object_name = parts
    presigned_url = get_presigned_url(bucket=bucket, object_name=object_name)

    if not presigned_url:
        raise BadRequestError("File storage is currently unavailable.")

    return RedirectResponse(url=presigned_url, status_code=307)


@router.post("/{evidence_id}/approve", response_model=EvidenceResponse)
async def approve_evidence(
    org_id: VerifiedOrgId,
    evidence_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    """Approve evidence, marking it as reviewed and approved in the chain of custody."""
    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)
    if evidence.status != "collected":
        raise HTTPException(400, "Evidence must be in 'collected' status to approve")
    evidence.status = "approved"
    evidence.approved_by = current_user.id
    evidence.approved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(evidence)
    await log_audit(db, current_user, "approve", "evidence", str(evidence_id), org_id)
    return evidence


@router.post("/{evidence_id}/reject", response_model=EvidenceResponse)
async def reject_evidence(
    org_id: VerifiedOrgId,
    evidence_id: UUID,
    body: EvidenceReject,
    db: DB,
    current_user: ComplianceUser,
):
    """Reject evidence with a reason, recording who rejected and when."""
    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)
    if evidence.status not in ("collected", "approved"):
        raise HTTPException(400, "Evidence must be in 'collected' or 'approved' status to reject")
    evidence.status = "rejected"
    evidence.rejected_by = current_user.id
    evidence.rejected_at = datetime.now(timezone.utc)
    evidence.rejection_reason = body.reason
    await db.commit()
    await db.refresh(evidence)
    await log_audit(db, current_user, "reject", "evidence", str(evidence_id), org_id)
    return evidence
