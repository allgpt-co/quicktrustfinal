"""Control versioning + dependencies + bulk operations API."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DB, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.models.control import Control
from app.models.control_version import ControlVersion
from app.models.control_dependency import ControlDependency
from app.schemas.common import PaginatedResponse

router = APIRouter(
    prefix="/organizations/{org_id}/controls",
    tags=["control-versions"],
)


# --- Schemas ---

class ControlVersionResponse(BaseModel):
    id: UUID
    control_id: UUID
    version_number: int
    title: str
    status: str
    description: str | None
    implementation_details: str | None
    effectiveness: str | None
    change_reason: str | None
    changes: dict | None
    created_at: str

    model_config = {"from_attributes": True}


class DependencyCreate(BaseModel):
    depends_on_id: UUID
    dependency_type: str = "requires"
    notes: str | None = None


class DependencyResponse(BaseModel):
    id: UUID
    control_id: UUID
    depends_on_id: UUID
    dependency_type: str
    notes: str | None
    depends_on_title: str | None = None

    model_config = {"from_attributes": True}


class BulkStatusUpdate(BaseModel):
    control_ids: list[UUID]
    status: str


class BulkOwnerUpdate(BaseModel):
    control_ids: list[UUID]
    owner_id: UUID


class BulkDeleteRequest(BaseModel):
    control_ids: list[UUID]


# --- Version History ---

@router.get("/{control_id}/versions")
async def list_control_versions(
    org_id: VerifiedOrgId, control_id: UUID, db: DB, current_user: AnyInternalUser,
):
    result = await db.execute(
        select(ControlVersion)
        .where(ControlVersion.control_id == control_id, ControlVersion.org_id == org_id)
        .order_by(ControlVersion.version_number.desc())
        .limit(50)
    )
    versions = result.scalars().all()
    return [
        {
            "id": str(v.id),
            "version_number": v.version_number,
            "title": v.title,
            "status": v.status,
            "description": v.description,
            "implementation_details": v.implementation_details,
            "effectiveness": v.effectiveness,
            "change_reason": v.change_reason,
            "changes": v.changes,
            "created_at": v.created_at.isoformat() if v.created_at else None,
        }
        for v in versions
    ]


@router.get("/{control_id}/versions/{version_id}")
async def get_control_version(
    org_id: VerifiedOrgId, control_id: UUID, version_id: UUID,
    db: DB, current_user: AnyInternalUser,
):
    result = await db.execute(
        select(ControlVersion).where(
            ControlVersion.id == version_id,
            ControlVersion.control_id == control_id,
            ControlVersion.org_id == org_id,
        )
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")
    return version


# --- Dependencies ---

@router.get("/{control_id}/dependencies")
async def list_dependencies(
    org_id: VerifiedOrgId, control_id: UUID, db: DB, current_user: AnyInternalUser,
):
    result = await db.execute(
        select(ControlDependency)
        .where(ControlDependency.control_id == control_id, ControlDependency.org_id == org_id)
    )
    deps = result.scalars().all()
    items = []
    for d in deps:
        dep_control = await db.get(Control, d.depends_on_id)
        items.append({
            "id": str(d.id),
            "control_id": str(d.control_id),
            "depends_on_id": str(d.depends_on_id),
            "dependency_type": d.dependency_type,
            "notes": d.notes,
            "depends_on_title": dep_control.title if dep_control else None,
        })
    return items


@router.post("/{control_id}/dependencies")
async def add_dependency(
    org_id: VerifiedOrgId, control_id: UUID, data: DependencyCreate,
    db: DB, current_user: ComplianceUser,
):
    # Verify both controls exist
    ctrl = await db.get(Control, control_id)
    dep = await db.get(Control, data.depends_on_id)
    if not ctrl or not dep:
        raise HTTPException(404, "Control not found")
    if str(ctrl.org_id) != str(org_id) or str(dep.org_id) != str(org_id):
        raise HTTPException(403, "Controls must belong to the same organization")
    if control_id == data.depends_on_id:
        raise HTTPException(400, "A control cannot depend on itself")

    dependency = ControlDependency(
        org_id=org_id,
        control_id=control_id,
        depends_on_id=data.depends_on_id,
        dependency_type=data.dependency_type,
        notes=data.notes,
    )
    db.add(dependency)
    await db.commit()
    return {"id": str(dependency.id), "message": "Dependency added"}


@router.delete("/{control_id}/dependencies/{dep_id}")
async def remove_dependency(
    org_id: VerifiedOrgId, control_id: UUID, dep_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    result = await db.execute(
        select(ControlDependency).where(
            ControlDependency.id == dep_id,
            ControlDependency.control_id == control_id,
            ControlDependency.org_id == org_id,
        )
    )
    dep = result.scalar_one_or_none()
    if not dep:
        raise HTTPException(404, "Dependency not found")
    await db.delete(dep)
    await db.commit()
    return {"message": "Dependency removed"}


# --- Bulk Operations ---

@router.post("/bulk/status")
async def bulk_update_status(
    org_id: VerifiedOrgId, data: BulkStatusUpdate,
    db: DB, current_user: ComplianceUser,
):
    from app.core.cache import cache_delete

    updated = 0
    for cid in data.control_ids:
        result = await db.execute(
            select(Control).where(Control.id == cid, Control.org_id == org_id)
        )
        ctrl = result.scalar_one_or_none()
        if ctrl:
            ctrl.status = data.status
            updated += 1
    await db.commit()
    await cache_delete(f"org:{org_id}:control_stats")
    return {"message": f"Updated {updated} controls to status '{data.status}'"}


@router.post("/bulk/owner")
async def bulk_update_owner(
    org_id: VerifiedOrgId, data: BulkOwnerUpdate,
    db: DB, current_user: ComplianceUser,
):
    updated = 0
    for cid in data.control_ids:
        result = await db.execute(
            select(Control).where(Control.id == cid, Control.org_id == org_id)
        )
        ctrl = result.scalar_one_or_none()
        if ctrl:
            ctrl.owner_id = data.owner_id
            updated += 1
    await db.commit()
    return {"message": f"Assigned {updated} controls to new owner"}


@router.post("/bulk/delete")
async def bulk_delete(
    org_id: VerifiedOrgId, data: BulkDeleteRequest,
    db: DB, current_user: ComplianceUser,
):
    from app.core.cache import cache_delete

    deleted = 0
    for cid in data.control_ids:
        result = await db.execute(
            select(Control).where(Control.id == cid, Control.org_id == org_id)
        )
        ctrl = result.scalar_one_or_none()
        if ctrl:
            await db.delete(ctrl)
            deleted += 1
    await db.commit()
    await cache_delete(f"org:{org_id}:control_stats")
    return {"message": f"Deleted {deleted} controls"}
