"""Policy versioning + diff + distribution API."""

import difflib
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from app.core.dependencies import DB, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.models.policy_version import PolicyVersion

router = APIRouter(
    prefix="/organizations/{org_id}/policies",
    tags=["policy-versions"],
)


# --- Version History ---

@router.get("/{policy_id}/versions")
async def list_policy_versions(
    org_id: VerifiedOrgId, policy_id: UUID, db: DB, current_user: AnyInternalUser,
):
    result = await db.execute(
        select(PolicyVersion)
        .where(PolicyVersion.policy_id == policy_id, PolicyVersion.org_id == org_id)
        .order_by(PolicyVersion.version_number.desc())
        .limit(50)
    )
    versions = result.scalars().all()
    return [
        {
            "id": str(v.id),
            "version_number": v.version_number,
            "change_summary": v.change_summary,
            "status_at_version": v.status_at_version,
            "changes": v.changes,
            "content_length": len(v.content) if v.content else 0,
            "created_at": v.created_at.isoformat() if v.created_at else None,
        }
        for v in versions
    ]


@router.get("/{policy_id}/versions/{version_id}")
async def get_policy_version(
    org_id: VerifiedOrgId, policy_id: UUID, version_id: UUID,
    db: DB, current_user: AnyInternalUser,
):
    result = await db.execute(
        select(PolicyVersion).where(
            PolicyVersion.id == version_id,
            PolicyVersion.policy_id == policy_id,
            PolicyVersion.org_id == org_id,
        )
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")
    return {
        "id": str(version.id),
        "version_number": version.version_number,
        "content": version.content,
        "change_summary": version.change_summary,
        "status_at_version": version.status_at_version,
        "changes": version.changes,
        "created_at": version.created_at.isoformat() if version.created_at else None,
    }


# --- Diff ---

@router.get("/{policy_id}/diff")
async def diff_policy_versions(
    org_id: VerifiedOrgId, policy_id: UUID,
    v1: int, v2: int,
    db: DB, current_user: AnyInternalUser,
):
    """Compare two policy versions and return a unified diff."""
    r1 = await db.execute(
        select(PolicyVersion).where(
            PolicyVersion.policy_id == policy_id,
            PolicyVersion.org_id == org_id,
            PolicyVersion.version_number == v1,
        )
    )
    r2 = await db.execute(
        select(PolicyVersion).where(
            PolicyVersion.policy_id == policy_id,
            PolicyVersion.org_id == org_id,
            PolicyVersion.version_number == v2,
        )
    )
    ver1 = r1.scalar_one_or_none()
    ver2 = r2.scalar_one_or_none()

    if not ver1 or not ver2:
        raise HTTPException(404, "One or both versions not found")

    lines1 = (ver1.content or "").splitlines(keepends=True)
    lines2 = (ver2.content or "").splitlines(keepends=True)

    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=f"v{v1}",
        tofile=f"v{v2}",
        lineterm="",
    ))

    # Also create a structured diff for the frontend
    additions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))

    return {
        "policy_id": str(policy_id),
        "from_version": v1,
        "to_version": v2,
        "diff_text": "\n".join(diff),
        "additions": additions,
        "deletions": deletions,
        "total_changes": additions + deletions,
    }
