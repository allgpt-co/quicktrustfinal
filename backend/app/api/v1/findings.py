"""Normalized findings API — unified view of all scanner findings."""

from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DB, AnyInternalUser, VerifiedOrgId
from app.models.scan import ScanFinding
from app.services.finding_normalizer import normalize_finding

router = APIRouter(
    prefix="/organizations/{org_id}/findings",
    tags=["findings"],
)


@router.get("/normalized")
async def list_normalized_findings(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    severity: str | None = Query(None, description="Filter by severity"),
    scanner: str | None = Query(None, description="Filter by scanner"),
    category: str | None = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
):
    """Return all scan findings in a unified, normalized format."""
    query = select(ScanFinding).where(ScanFinding.org_id == org_id)

    if severity:
        query = query.where(ScanFinding.severity == severity)
    if scanner:
        query = query.where(ScanFinding.scanner == scanner)

    query = query.order_by(ScanFinding.created_at.desc())

    # Count total
    from sqlalchemy import func

    count_q = select(func.count()).select_from(ScanFinding).where(
        ScanFinding.org_id == org_id
    )
    if severity:
        count_q = count_q.where(ScanFinding.severity == severity)
    if scanner:
        count_q = count_q.where(ScanFinding.scanner == scanner)

    total_result = await db.execute(count_q)
    total = total_result.scalar() or 0

    # Paginate
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    findings = list(result.scalars().all())

    # Normalize each finding
    normalized = []
    for f in findings:
        raw_data = {
            "title": f.title,
            "severity": f.severity,
            "description": f.description,
            "location": f.location,
            "line_number": f.line_number,
            "rule_id": f.rule_id,
            "cve_id": f.cve_id,
            "cwe_id": f.cwe_id,
            "remediation": f.remediation,
            "package_name": f.package_name,
            "package_version": f.package_version,
            "fixed_version": f.fixed_version,
            "confidence": f.confidence,
            **(f.extra_data or {}),
        }
        norm = normalize_finding(f.scanner, raw_data)

        # Apply category filter after normalization
        if category and norm.get("category") != category:
            continue

        norm["id"] = str(f.id)
        norm["status"] = f.status
        norm["scan_result_id"] = str(f.scan_result_id)
        norm["created_at"] = f.created_at.isoformat() if f.created_at else None
        normalized.append(norm)

    return {
        "items": normalized,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }
