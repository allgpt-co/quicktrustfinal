from uuid import UUID

from fastapi import APIRouter, Query, status

from app.core.dependencies import DB, AnyInternalUser, AdminUser
from app.schemas.framework import (
    DomainCreate,
    DomainDetailResponse,
    FrameworkCreate,
    FrameworkDetailResponse,
    FrameworkDomainResponse,
    FrameworkRequirementResponse,
    FrameworkResponse,
    FrameworkUpdate,
    RequirementCreate,
    RequirementDetailResponse,
)
from app.services import framework_service

router = APIRouter(prefix="/frameworks", tags=["frameworks"])


# ---------------------------------------------------------------------------
# READ endpoints (existing)
# ---------------------------------------------------------------------------


@router.get("", response_model=list[FrameworkResponse])
async def list_frameworks(db: DB, current_user: AnyInternalUser):
    return await framework_service.list_frameworks(db)


# /diff must be registered before /{framework_id} to avoid UUID parsing conflict
@router.get("/diff")
async def diff_frameworks_route(
    db: DB, current_user: AnyInternalUser,
    source_id: UUID = Query(..., description="Source framework ID"),
    target_id: UUID = Query(..., description="Target framework ID"),
):
    return await _diff_frameworks_impl(db, current_user, source_id, target_id)


@router.get("/{framework_id}", response_model=FrameworkDetailResponse)
async def get_framework(framework_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_framework(db, framework_id)


@router.get("/{framework_id}/domains", response_model=list[FrameworkDomainResponse])
async def get_domains(framework_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_framework_domains(db, framework_id)


@router.get("/{framework_id}/domains/{domain_id}", response_model=DomainDetailResponse)
async def get_domain(framework_id: UUID, domain_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_domain(db, domain_id)


@router.get("/{framework_id}/requirements", response_model=list[FrameworkRequirementResponse])
async def get_requirements(framework_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_requirements(db, framework_id)


@router.get(
    "/{framework_id}/requirements/{requirement_id}",
    response_model=RequirementDetailResponse,
)
async def get_requirement(framework_id: UUID, requirement_id: UUID, db: DB, current_user: AnyInternalUser):
    return await framework_service.get_requirement(db, requirement_id)


# ---------------------------------------------------------------------------
# WRITE endpoints (new – Phase 4)
# ---------------------------------------------------------------------------


@router.post("", response_model=FrameworkResponse, status_code=status.HTTP_201_CREATED)
async def create_framework(data: FrameworkCreate, db: DB, current_user: AdminUser):
    """Create a new custom compliance framework."""
    return await framework_service.create_framework(db, data)


@router.patch("/{framework_id}", response_model=FrameworkResponse)
async def update_framework(framework_id: UUID, data: FrameworkUpdate, db: DB, current_user: AdminUser):
    """Update an existing framework's metadata."""
    return await framework_service.update_framework(db, framework_id, data)


@router.delete("/{framework_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_framework(framework_id: UUID, db: DB, current_user: AdminUser):
    """Delete a custom framework. Seeded frameworks cannot be deleted."""
    await framework_service.delete_framework(db, framework_id)


@router.post(
    "/{framework_id}/domains",
    response_model=FrameworkDomainResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_domain(framework_id: UUID, data: DomainCreate, db: DB, current_user: AdminUser):
    """Add a domain to an existing framework."""
    return await framework_service.add_domain(db, framework_id, data)


@router.post(
    "/{framework_id}/domains/{domain_id}/requirements",
    response_model=FrameworkRequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_requirement(framework_id: UUID, domain_id: UUID, data: RequirementCreate, db: DB, current_user: AdminUser):
    """Add a requirement to a domain within a framework."""
    return await framework_service.add_requirement(db, framework_id, domain_id, data)


# ---------------------------------------------------------------------------
# Framework versioning & diff
# ---------------------------------------------------------------------------


@router.post(
    "/{framework_id}/new-version",
    response_model=FrameworkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_version(framework_id: UUID, db: DB, current_user: AdminUser):
    """Create a new version of an existing framework.

    Duplicates the framework (including domains and requirements) with an
    incremented version string. The new framework's ``previous_version_id``
    points back to the source.
    """
    from sqlalchemy.orm import selectinload
    from sqlalchemy import select
    from app.models.framework import Framework
    from app.models.framework_domain import FrameworkDomain
    from app.models.framework_requirement import FrameworkRequirement

    # Load source framework with domains -> requirements
    result = await db.execute(
        select(Framework)
        .options(
            selectinload(Framework.domains).selectinload(FrameworkDomain.requirements)
        )
        .where(Framework.id == framework_id)
    )
    source = result.scalar_one_or_none()
    if not source:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(f"Framework {framework_id} not found")

    # Increment version string (e.g. "1.0" -> "2.0", "v2" -> "v3")
    new_version = _increment_version(source.version)

    new_framework = Framework(
        name=source.name,
        version=new_version,
        category=source.category,
        description=source.description,
        is_active=True,
        previous_version_id=source.id,
    )
    db.add(new_framework)
    await db.flush()

    # Duplicate domains and requirements
    for domain in source.domains:
        new_domain = FrameworkDomain(
            framework_id=new_framework.id,
            code=domain.code,
            name=domain.name,
            description=domain.description,
            sort_order=domain.sort_order,
        )
        db.add(new_domain)
        await db.flush()

        for req in domain.requirements:
            new_req = FrameworkRequirement(
                domain_id=new_domain.id,
                code=req.code,
                title=req.title,
                description=req.description,
                sort_order=req.sort_order,
            )
            db.add(new_req)

    await db.commit()
    await db.refresh(new_framework)
    return new_framework


async def _diff_frameworks_impl(
    db,
    current_user,
    source_id: UUID = None,
    target_id: UUID = None,
):
    """Compare two frameworks by their requirement codes.

    Returns lists of added, removed, and modified requirements.
    """
    source = await framework_service.get_framework(db, source_id)
    target = await framework_service.get_framework(db, target_id)

    # Build code -> requirement maps
    source_reqs: dict[str, dict] = {}
    for domain in source.domains:
        for req in domain.requirements:
            source_reqs[req.code] = {
                "code": req.code,
                "title": req.title,
                "description": req.description,
                "domain": domain.code,
            }

    target_reqs: dict[str, dict] = {}
    for domain in target.domains:
        for req in domain.requirements:
            target_reqs[req.code] = {
                "code": req.code,
                "title": req.title,
                "description": req.description,
                "domain": domain.code,
            }

    source_codes = set(source_reqs.keys())
    target_codes = set(target_reqs.keys())

    added = [target_reqs[c] for c in sorted(target_codes - source_codes)]
    removed = [source_reqs[c] for c in sorted(source_codes - target_codes)]

    modified = []
    for code in sorted(source_codes & target_codes):
        s = source_reqs[code]
        t = target_reqs[code]
        if s["title"] != t["title"] or s["description"] != t["description"] or s["domain"] != t["domain"]:
            modified.append({
                "code": code,
                "source": s,
                "target": t,
            })

    return {
        "source_framework": {
            "id": str(source.id),
            "name": source.name,
            "version": source.version,
        },
        "target_framework": {
            "id": str(target.id),
            "name": target.name,
            "version": target.version,
        },
        "added": added,
        "removed": removed,
        "modified": modified,
        "summary": {
            "added_count": len(added),
            "removed_count": len(removed),
            "modified_count": len(modified),
        },
    }


def _increment_version(version: str) -> str:
    """Increment a version string. Handles formats like '1.0', 'v2', '3'."""
    import re

    # Try "X.Y" format
    match = re.match(r"^(\d+)\.(\d+)$", version)
    if match:
        major = int(match.group(1)) + 1
        return f"{major}.0"

    # Try "vX" format
    match = re.match(r"^v(\d+)$", version, re.IGNORECASE)
    if match:
        num = int(match.group(1)) + 1
        prefix = "V" if version[0] == "V" else "v"
        return f"{prefix}{num}"

    # Try plain number
    match = re.match(r"^(\d+)$", version)
    if match:
        return str(int(match.group(1)) + 1)

    # Fallback: append " v2" or increment trailing number
    match = re.search(r"(\d+)$", version)
    if match:
        num = int(match.group(1))
        return version[: match.start()] + str(num + 1)

    return version + " v2"
