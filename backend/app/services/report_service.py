from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.report import Report
from app.schemas.report import ReportCreate


async def list_reports(
    db: AsyncSession,
    org_id: UUID,
    report_type: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Report], int]:
    base_q = select(Report).where(Report.org_id == org_id)
    count_q = select(func.count()).select_from(Report).where(Report.org_id == org_id)

    if report_type:
        base_q = base_q.where(Report.report_type == report_type)
        count_q = count_q.where(Report.report_type == report_type)
    if status:
        base_q = base_q.where(Report.status == status)
        count_q = count_q.where(Report.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Report.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_report(
    db: AsyncSession, org_id: UUID, data: ReportCreate, requested_by_id: UUID | None = None
) -> Report:
    report = Report(
        org_id=org_id,
        requested_by_id=requested_by_id,
        **data.model_dump(),
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def get_report(db: AsyncSession, org_id: UUID, report_id: UUID) -> Report:
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.org_id == org_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError(f"Report {report_id} not found")
    return report


async def delete_report(db: AsyncSession, org_id: UUID, report_id: UUID) -> None:
    report = await get_report(db, org_id, report_id)
    await db.delete(report)
    await db.commit()


async def generate_report_data(db: AsyncSession, org_id: UUID, report_id: UUID) -> dict:
    """Generate report data by aggregating from existing services."""
    report = await get_report(db, org_id, report_id)
    report.status = "generating"
    await db.commit()

    try:
        from app.services import control_service, risk_service
        from app.models.policy import Policy
        from app.models.evidence import Evidence
        from app.models.training import TrainingAssignment

        data: dict = {"report_type": report.report_type, "generated_at": datetime.now(timezone.utc).isoformat()}

        if report.report_type in ("compliance_summary", "evidence_audit"):
            from app.models.control import Control
            control_stats = await control_service.get_control_stats(db, org_id)
            data["control_stats"] = {
                "total": control_stats.total,
                "draft": control_stats.draft,
                "implemented": control_stats.implemented,
                "partially_implemented": control_stats.partially_implemented,
                "not_implemented": control_stats.not_implemented,
                "not_applicable": control_stats.not_applicable,
            }
            # Include actual controls list
            controls_result = await db.execute(
                select(Control).where(Control.org_id == org_id).order_by(Control.status, Control.title).limit(100)
            )
            data["controls"] = [
                {"title": c.title, "status": c.status, "automation_level": c.automation_level or "manual"}
                for c in controls_result.scalars().all()
            ]

        if report.report_type in ("compliance_summary", "risk_report"):
            from app.models.risk import Risk
            risk_stats = await risk_service.get_risk_stats(db, org_id)
            data["risk_stats"] = risk_stats
            risks_result = await db.execute(
                select(Risk).where(Risk.org_id == org_id).limit(50)
            )
            data["risks"] = [
                {"title": r.title, "risk_level": r.risk_level or "unknown", "status": r.status or "open", "score": r.risk_score}
                for r in risks_result.scalars().all()
            ]

        if report.report_type in ("compliance_summary",):
            policy_count = (await db.execute(
                select(func.count()).select_from(Policy).where(Policy.org_id == org_id)
            )).scalar() or 0
            published_count = (await db.execute(
                select(func.count()).select_from(Policy).where(
                    Policy.org_id == org_id, Policy.status == "published"
                )
            )).scalar() or 0
            data["policy_stats"] = {"total": policy_count, "published": published_count}
            policies_result = await db.execute(
                select(Policy).where(Policy.org_id == org_id).order_by(Policy.status, Policy.title).limit(50)
            )
            data["policies"] = [
                {"title": p.title, "status": p.status}
                for p in policies_result.scalars().all()
            ]

            # Include frameworks
            from app.models.framework import Framework
            fw_result = await db.execute(select(Framework).where(Framework.is_active.is_(True)).limit(20))
            data["frameworks"] = [{"name": f.name, "version": f.version} for f in fw_result.scalars().all()]

        if report.report_type in ("compliance_summary", "evidence_audit"):
            evidence_count = (await db.execute(
                select(func.count()).select_from(Evidence).where(Evidence.org_id == org_id)
            )).scalar() or 0
            data["evidence_stats"] = {"total": evidence_count}
            evidence_result = await db.execute(
                select(Evidence).where(Evidence.org_id == org_id).order_by(Evidence.status, Evidence.title).limit(100)
            )
            data["evidence_items"] = [
                {"title": e.title, "status": e.status, "collection_method": e.collection_method or "manual"}
                for e in evidence_result.scalars().all()
            ]

        if report.report_type == "training_completion":
            from app.models.training import TrainingCourse
            total_assignments = (await db.execute(
                select(func.count()).select_from(TrainingAssignment).where(TrainingAssignment.org_id == org_id)
            )).scalar() or 0
            completed = (await db.execute(
                select(func.count()).select_from(TrainingAssignment).where(
                    TrainingAssignment.org_id == org_id, TrainingAssignment.status == "completed"
                )
            )).scalar() or 0
            data["training_stats"] = {
                "total_assignments": total_assignments,
                "completed": completed,
                "completion_rate": round((completed / total_assignments * 100), 1) if total_assignments else 0.0,
            }
            courses_result = await db.execute(
                select(TrainingCourse).where(TrainingCourse.org_id == org_id).limit(20)
            )
            data["courses"] = [
                {"title": c.title, "status": c.status or "active"}
                for c in courses_result.scalars().all()
            ]

        if report.report_type == "vendor_risk":
            from app.models.vendor import Vendor
            vendors_result = await db.execute(
                select(Vendor).where(Vendor.org_id == org_id).limit(50)
            )
            vendor_list = list(vendors_result.scalars().all())
            tier_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            vendors_data = []
            for v in vendor_list:
                tier = (v.risk_tier or "unknown").lower()
                if tier in tier_counts:
                    tier_counts[tier] += 1
                vendors_data.append({
                    "name": v.name,
                    "risk_tier": v.risk_tier or "unknown",
                    "status": v.status or "active",
                    "last_assessment_date": v.updated_at.strftime("%Y-%m-%d") if v.updated_at else "N/A",
                })
            data["vendor_stats"] = {"total": len(vendor_list), **tier_counts}
            data["vendors"] = vendors_data

        # Render to the requested format and upload to MinIO
        if report.format in ("pdf", "csv", "pptx"):
            from app.services.report_renderer import render_pdf, render_csv, render_pptx
            from app.core.storage import upload_file

            if report.format == "pdf":
                file_bytes = render_pdf(data, report.report_type)
                content_type = "application/pdf"
                extension = "pdf"
            elif report.format == "pptx":
                file_bytes = render_pptx(report.report_type, data)
                content_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                extension = "pptx"
            else:
                file_bytes = render_csv(data, report.report_type)
                content_type = "text/csv"
                extension = "csv"

            object_name = (
                f"reports/{org_id}/{report_id}.{extension}"
            )
            file_url = upload_file(
                bucket="quicktrust-reports",
                object_name=object_name,
                data=file_bytes,
                content_type=content_type,
            )
            report.file_url = file_url if file_url else None

        report.status = "completed"
        report.generated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(report)
        return data

    except Exception as e:
        report.status = "failed"
        report.error_message = str(e)
        await db.commit()
        return {"error": str(e)}


async def get_report_stats(db: AsyncSession, org_id: UUID) -> dict:
    result = await db.execute(select(Report).where(Report.org_id == org_id))
    reports = list(result.scalars().all())

    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for r in reports:
        by_type[r.report_type] = by_type.get(r.report_type, 0) + 1
        by_status[r.status] = by_status.get(r.status, 0) + 1

    return {
        "total": len(reports),
        "by_type": by_type,
        "by_status": by_status,
    }
