from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import Response
from pydantic import BaseModel as PydanticBaseModel

from app.core.dependencies import DB, AnyInternalUser, ComplianceUser, VerifiedOrgId
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
    from app.core.storage import download_file

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

    response = download_file(bucket=bucket, object_name=object_name)
    if response is None:
        raise BadRequestError("File storage is currently unavailable.")

    try:
        file_bytes = response.read()
        response.close()
        response.release_conn()

        format_content_types = {
            "pdf": "application/pdf",
            "csv": "text/csv",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        }
        content_type = format_content_types.get(report.format, "application/octet-stream")
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


# ---------------------------------------------------------------------------
# Report Schedule endpoints
# ---------------------------------------------------------------------------


class ReportScheduleCreate(PydanticBaseModel):
    report_type: str
    frequency: str  # daily, weekly, monthly
    day_of_week: int = 0  # 0=Monday, only used for weekly
    recipients: list[str] | None = None


class ReportScheduleResponse(PydanticBaseModel):
    id: UUID
    org_id: UUID
    report_type: str
    frequency: str
    day_of_week: int
    recipients: list[str] | None = None
    is_active: bool
    last_sent_at: datetime | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


@router.get("/schedules", response_model=list[ReportScheduleResponse])
async def list_schedules(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: ComplianceUser,
):
    """List all report schedules for this organization."""
    from sqlalchemy import select
    from app.models.report_schedule import ReportSchedule

    result = await db.execute(
        select(ReportSchedule).where(ReportSchedule.org_id == org_id).order_by(
            ReportSchedule.created_at.desc()
        )
    )
    return list(result.scalars().all())


@router.post("/schedules", response_model=ReportScheduleResponse, status_code=201)
async def create_schedule(
    org_id: VerifiedOrgId,
    data: ReportScheduleCreate,
    db: DB,
    current_user: ComplianceUser,
):
    """Create a new report delivery schedule."""
    from app.models.report_schedule import ReportSchedule

    valid_frequencies = {"daily", "weekly", "monthly"}
    if data.frequency not in valid_frequencies:
        raise BadRequestError(f"Frequency must be one of: {', '.join(valid_frequencies)}")

    schedule = ReportSchedule(
        org_id=org_id,
        report_type=data.report_type,
        frequency=data.frequency,
        day_of_week=data.day_of_week,
        recipients=data.recipients or [],
        is_active=True,
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


@router.delete("/schedules/{schedule_id}", status_code=204)
async def delete_schedule(
    org_id: VerifiedOrgId,
    schedule_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    """Delete a report delivery schedule."""
    from sqlalchemy import select
    from app.models.report_schedule import ReportSchedule

    result = await db.execute(
        select(ReportSchedule).where(
            ReportSchedule.id == schedule_id, ReportSchedule.org_id == org_id
        )
    )
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise BadRequestError(f"Schedule {schedule_id} not found")
    await db.delete(schedule)
    await db.commit()
