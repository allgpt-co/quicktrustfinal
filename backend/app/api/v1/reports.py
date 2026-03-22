from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse, Response

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import BadRequestError
from app.schemas.common import PaginatedResponse
from app.schemas.report import ReportCreate, ReportResponse, ReportStatsResponse
from app.services import report_service

router = APIRouter(
    prefix="/organizations/{org_id}/reports",
    tags=["reports"],
)


@router.get("", response_model=PaginatedResponse)
async def list_reports(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    report_type: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await report_service.list_reports(
        db, org_id, report_type=report_type, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[ReportResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=ReportResponse, status_code=201)
async def create_report(org_id: VerifiedOrgId, data: ReportCreate, db: DB, current_user: ComplianceUser):
    report = await report_service.create_report(db, org_id, data, requested_by_id=current_user.id)
    # Immediately generate the report data and render the file
    try:
        await report_service.generate_report_data(db, org_id, report.id)
        await db.refresh(report)
    except Exception:
        pass  # Report stays as pending if generation fails — can be retried
    return report


@router.get("/stats", response_model=ReportStatsResponse)
async def get_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await report_service.get_report_stats(db, org_id)


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(org_id: VerifiedOrgId, report_id: UUID, db: DB, current_user: AnyInternalUser):
    return await report_service.get_report(db, org_id, report_id)


@router.delete("/{report_id}", status_code=204)
async def delete_report(org_id: VerifiedOrgId, report_id: UUID, db: DB, current_user: ComplianceUser):
    await report_service.delete_report(db, org_id, report_id)


@router.get("/{report_id}/download")
async def download_report(org_id: VerifiedOrgId, report_id: UUID, db: DB, current_user: AnyInternalUser):
    """Download a rendered report file (PDF/CSV) directly."""
    from app.core.storage import _get_client

    report = await report_service.get_report(db, org_id, report_id)

    if not report.file_url:
        raise BadRequestError(
            "No file available for this report. "
            "Generate the report in PDF or CSV format first."
        )

    # file_url is stored as "bucket/object_name"
    parts = report.file_url.split("/", 1)
    if len(parts) != 2:
        raise BadRequestError("Invalid file reference on this report.")

    bucket, object_name = parts

    client = _get_client()
    if not client:
        raise BadRequestError("File storage is currently unavailable.")

    try:
        response = client.get_object(bucket, object_name)
        file_bytes = response.read()
        response.close()
        response.release_conn()

        content_type = "application/pdf" if report.format == "pdf" else "text/csv"
        import re
        safe_title = re.sub(r'[^\w\s\-.]', '', report.title or 'report').replace(' ', '_')
        filename = f"{safe_title}.{report.format or 'pdf'}"

        return Response(
            content=file_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
            },
        )
    except Exception as e:
        raise BadRequestError(f"Failed to download report: {str(e)[:200]}")


@router.get("/{report_id}/data")
async def get_report_data(org_id: VerifiedOrgId, report_id: UUID, db: DB, current_user: AnyInternalUser):
    return await report_service.generate_report_data(db, org_id, report_id)
