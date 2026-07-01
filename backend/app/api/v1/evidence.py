from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse

from app.config import get_settings
from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import BadRequestError
from app.schemas.common import PaginatedResponse
from app.schemas.evidence import EvidenceCreate, EvidenceReject, EvidenceResponse
from app.services import evidence_service


# ---------------------------------------------------------------------------
# Evidence version snapshot helper
# ---------------------------------------------------------------------------

async def _create_evidence_version(db, evidence, change_reason: str, changed_by_id=None, changes: dict | None = None):
    """Create an EvidenceVersion snapshot for the current state of an evidence item."""
    from sqlalchemy import select, func
    from app.models.evidence_version import EvidenceVersion

    # Determine next version number
    max_version = (await db.execute(
        select(func.coalesce(func.max(EvidenceVersion.version_number), 0)).where(
            EvidenceVersion.evidence_id == evidence.id
        )
    )).scalar() or 0

    version = EvidenceVersion(
        evidence_id=evidence.id,
        org_id=evidence.org_id,
        version_number=max_version + 1,
        title=evidence.title,
        status=evidence.status,
        collection_method=evidence.collection_method,
        description=None,
        file_url=evidence.file_url,
        file_hash=evidence.artifact_hash,
        change_reason=change_reason,
        changes=changes,
        changed_by=changed_by_id,
    )
    db.add(version)
    await db.flush()
    return version

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


# ---------------------------------------------------------------------------
# Static-path routes — registered before /{evidence_id} to prevent FastAPI
# from interpreting "package" / "freshness" / "screenshot" as a UUID.
# The actual handler bodies live further down in the file; we use thin
# forwarders here so the path registration order is correct.
# ---------------------------------------------------------------------------

@router.get("/package")
async def download_evidence_package_fwd(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    domain: str | None = Query(None, description="Filter by control template domain"),
    control_id: UUID | None = Query(None, description="Filter by specific control ID"),
):
    return await _download_evidence_package(org_id, db, current_user, domain, control_id)


@router.get("/freshness/report")
async def evidence_freshness_report_fwd(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    max_age_days: int = Query(30, ge=1, le=365),
):
    return await _evidence_freshness_report(org_id, db, current_user, max_age_days)


@router.post("/screenshot", response_model=EvidenceResponse)
async def capture_screenshot_fwd(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser,
    url: str = Query(..., description="URL to capture"),
    control_id: UUID | None = Query(None),
    title: str | None = Query(None),
):
    return await _capture_screenshot(org_id, db, current_user, url, control_id, title)


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
        bucket=get_settings().S3_BUCKET,
        object_name=object_name,
        data=contents,
        content_type=content_type,
    )

    if not file_url:
        raise BadRequestError("File storage is currently unavailable. Upload failed.")

    old_file_url = evidence.file_url
    old_file_hash = evidence.artifact_hash

    evidence.file_url = file_url
    evidence.file_name = original_name
    evidence.artifact_hash = file_hash

    # Create version snapshot for file upload
    await _create_evidence_version(
        db, evidence,
        change_reason=f"File uploaded: {original_name}",
        changed_by_id=current_user.id,
        changes={
            "file_url": {"old": old_file_url, "new": file_url},
            "artifact_hash": {"old": old_file_hash, "new": file_hash},
            "file_name": {"old": evidence.file_name, "new": original_name},
        },
    )

    await db.commit()
    await db.refresh(evidence)

    await log_audit(db, current_user, "upload_file", "evidence", str(evidence_id), org_id)
    return evidence


@router.get("/{evidence_id}/download")
async def download_evidence_file(
    org_id: VerifiedOrgId, evidence_id: UUID, db: DB, current_user: AnyInternalUser
):
    """Download an evidence file by streaming it from object storage."""
    from app.core.storage import download_file

    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)

    if not evidence.file_url:
        raise BadRequestError("No file has been uploaded for this evidence item.")

    # file_url is stored as "bucket/object_name"
    parts = evidence.file_url.split("/", 1)
    if len(parts) != 2:
        raise BadRequestError("Invalid file reference on this evidence item.")

    bucket, object_name = parts
    response = download_file(bucket=bucket, object_name=object_name)

    if response is None:
        raise BadRequestError("File storage is currently unavailable.")

    filename = evidence.file_name or "download"

    return StreamingResponse(
        response.stream(32 * 1024),
        media_type=response.headers.get("content-type", "application/octet-stream"),
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


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
    old_status = evidence.status
    evidence.status = "approved"
    evidence.approved_by = current_user.id
    evidence.approved_at = datetime.now(timezone.utc)

    # Create version snapshot for approval
    await _create_evidence_version(
        db, evidence,
        change_reason="Evidence approved",
        changed_by_id=current_user.id,
        changes={"status": {"old": old_status, "new": "approved"}},
    )

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
    old_status = evidence.status
    evidence.status = "rejected"
    evidence.rejected_by = current_user.id
    evidence.rejected_at = datetime.now(timezone.utc)
    evidence.rejection_reason = body.reason

    # Create version snapshot for rejection
    await _create_evidence_version(
        db, evidence,
        change_reason=f"Evidence rejected: {body.reason}",
        changed_by_id=current_user.id,
        changes={"status": {"old": old_status, "new": "rejected"}},
    )

    await db.commit()
    await db.refresh(evidence)
    await log_audit(db, current_user, "reject", "evidence", str(evidence_id), org_id)
    return evidence


async def _download_evidence_package(
    org_id,
    db,
    current_user,
    domain: str | None = None,
    control_id: UUID | None = None,
):
    """Download a ZIP package of all evidence files with a manifest.json."""
    import io
    import json
    import zipfile
    from sqlalchemy import select
    from app.models.evidence import Evidence
    from app.models.control import Control
    from app.models.control_template import ControlTemplate
    from app.core.storage import download_file

    # Build query for evidence items
    query = select(Evidence).where(Evidence.org_id == org_id)

    if control_id:
        query = query.where(Evidence.control_id == control_id)
    elif domain:
        # Join through Control -> ControlTemplate to filter by domain
        query = (
            query
            .join(Control, Evidence.control_id == Control.id)
            .join(ControlTemplate, Control.template_id == ControlTemplate.id)
            .where(ControlTemplate.domain == domain)
        )

    result = await db.execute(query)
    evidence_items = list(result.scalars().all())

    if not evidence_items:
        raise BadRequestError("No evidence items found matching the specified filters.")

    # Build ZIP in memory
    zip_buffer = io.BytesIO()
    manifest_entries = []

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for ev in evidence_items:
            entry = {
                "id": str(ev.id),
                "title": ev.title,
                "status": ev.status,
                "collection_method": ev.collection_method,
                "collector": ev.collector,
                "collected_at": ev.collected_at.isoformat() if ev.collected_at else None,
                "file_url": ev.file_url,
                "file_name": ev.file_name,
                "artifact_hash": ev.artifact_hash,
                "control_id": str(ev.control_id) if ev.control_id else None,
                "classification": ev.classification,
                "created_at": ev.created_at.isoformat() if ev.created_at else None,
            }
            manifest_entries.append(entry)

            # Download the file from object storage and add to ZIP
            if ev.file_url:
                parts = ev.file_url.split("/", 1)
                if len(parts) == 2:
                    bucket, object_name = parts
                    try:
                        response = download_file(bucket=bucket, object_name=object_name)
                        if response is not None:
                            file_data = response.read()
                            response.close()
                            response.release_conn()
                            # Use a safe filename in the ZIP
                            safe_name = ev.file_name or f"{ev.id}"
                            zip_path = f"evidence/{ev.id}/{safe_name}"
                            zf.writestr(zip_path, file_data)
                            entry["zip_path"] = zip_path
                    except Exception:
                        entry["zip_path"] = None
                        entry["download_error"] = "Failed to retrieve file from storage"

        # Add manifest
        manifest = {
            "org_id": str(org_id),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_items": len(manifest_entries),
            "filters": {
                "domain": domain,
                "control_id": str(control_id) if control_id else None,
            },
            "evidence": manifest_entries,
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))

    zip_buffer.seek(0)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"evidence_package_{timestamp}.zip"

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{evidence_id}/versions")
async def list_evidence_versions(
    org_id: VerifiedOrgId,
    evidence_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
):
    """List all version snapshots for a specific evidence item."""
    from sqlalchemy import select
    from app.models.evidence_version import EvidenceVersion

    # Verify evidence exists and belongs to org
    await evidence_service.get_evidence(db, org_id, evidence_id)

    result = await db.execute(
        select(EvidenceVersion)
        .where(
            EvidenceVersion.evidence_id == evidence_id,
            EvidenceVersion.org_id == org_id,
        )
        .order_by(EvidenceVersion.version_number.desc())
    )
    versions = list(result.scalars().all())

    return {
        "evidence_id": str(evidence_id),
        "total_versions": len(versions),
        "versions": [
            {
                "id": str(v.id),
                "version_number": v.version_number,
                "title": v.title,
                "status": v.status,
                "collection_method": v.collection_method,
                "file_url": v.file_url,
                "file_hash": v.file_hash,
                "change_reason": v.change_reason,
                "changes": v.changes,
                "changed_by": str(v.changed_by) if v.changed_by else None,
                "created_at": v.created_at.isoformat() if v.created_at else None,
            }
            for v in versions
        ],
    }


async def _evidence_freshness_report(
    org_id, db, current_user,
    max_age_days: int = 30,
):
    """Get evidence freshness report — flags stale evidence older than max_age_days."""
    from sqlalchemy import select
    from app.models.evidence import Evidence

    result = await db.execute(
        select(Evidence).where(
            Evidence.org_id == org_id,
            Evidence.status.in_(["collected", "approved"]),
        )
    )
    all_evidence = list(result.scalars().all())

    now = datetime.now(timezone.utc)
    fresh = []
    stale = []
    expired = []

    for e in all_evidence:
        collected = e.collected_at or e.created_at
        age_days = (now - collected).days

        item = {
            "id": str(e.id),
            "title": e.title,
            "status": e.status,
            "collector": e.collector,
            "collected_at": collected.isoformat(),
            "age_days": age_days,
        }

        if e.expires_at and now > e.expires_at:
            expired.append(item)
        elif age_days > max_age_days:
            stale.append(item)
        else:
            fresh.append(item)

    return {
        "total": len(all_evidence),
        "fresh": len(fresh),
        "stale": len(stale),
        "expired": len(expired),
        "max_age_days": max_age_days,
        "freshness_rate": round(len(fresh) / max(len(all_evidence), 1) * 100, 1),
        "stale_evidence": stale[:20],
        "expired_evidence": expired[:20],
    }


async def _capture_screenshot(
    org_id,
    db,
    current_user,
    url: str = "",
    control_id: UUID | None = None,
    title: str | None = None,
):
    """Capture a screenshot of a URL and store it as evidence.

    Uses Playwright for headless screenshot capture. Falls back to an HTTP
    501 error when Playwright is not installed.
    """
    import uuid as _uuid

    from app.core.storage import upload_file
    from app.models.evidence import Evidence

    evidence_title = title or f"Screenshot of {url}"

    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            screenshot_bytes = await page.screenshot(full_page=True)
            await browser.close()
    except Exception:
        raise HTTPException(
            501,
            "Screenshot capture requires Playwright. "
            "Install with: pip install playwright && playwright install chromium",
        )

    # Upload to object storage
    evidence_id = _uuid.uuid4()
    object_name = f"evidence/{org_id}/{evidence_id}/screenshot.png"
    file_url = upload_file(
        bucket=get_settings().S3_BUCKET,
        object_name=object_name,
        data=screenshot_bytes,
        content_type="image/png",
    )

    if not file_url:
        raise HTTPException(503, "File storage is currently unavailable.")

    # Compute hash
    import hashlib

    file_hash = hashlib.sha256(screenshot_bytes).hexdigest()

    # Create the Evidence record
    evidence = Evidence(
        id=evidence_id,
        org_id=org_id,
        control_id=control_id,
        title=evidence_title,
        status="collected",
        collection_method="screenshot",
        collector=f"playwright:{url}",
        collected_at=datetime.now(timezone.utc),
        file_url=file_url,
        file_name="screenshot.png",
        artifact_hash=file_hash,
        collected_by=current_user.id,
    )
    db.add(evidence)
    await db.commit()
    await db.refresh(evidence)

    await log_audit(db, current_user, "screenshot", "evidence", str(evidence.id), org_id)
    return evidence
