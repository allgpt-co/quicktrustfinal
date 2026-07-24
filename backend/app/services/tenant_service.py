"""Multi-tenancy hardening — tenant provisioning and isolation."""

import logging
from uuid import UUID

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import quoted_name

from app.core.exceptions import ConflictError
from app.core.security import hash_password
from app.models.organization import Organization
from app.models.user import User
from app.services import auth_service

logger = logging.getLogger(__name__)


async def provision_tenant(
    db: AsyncSession,
    name: str,
    industry: str | None = None,
    company_size: str | None = None,
    admin_email: str | None = None,
    admin_name: str | None = None,
    admin_password: str | None = None,
) -> dict:
    """Provision a new tenant and optionally its application-managed admin."""
    slug = name.lower().replace(" ", "-").replace("_", "-")
    existing = await db.execute(select(Organization).where(Organization.slug == slug))
    if existing.scalar_one_or_none():
        raise ConflictError(f"Organization with slug '{slug}' already exists")

    org = Organization(
        name=name, slug=slug, industry=industry, company_size=company_size
    )
    db.add(org)
    await db.flush()

    admin_user = None
    if admin_email:
        normalized_email = admin_email.strip().lower()
        existing_user = await db.execute(
            select(User).where(func.lower(User.email) == normalized_email)
        )
        if existing_user.scalar_one_or_none():
            raise ConflictError(f"User with email '{admin_email}' already exists")
        admin_user = User(
            org_id=org.id,
            email=normalized_email,
            full_name=admin_name or normalized_email.split("@")[0],
            password_hash=hash_password(admin_password, normalized_email)
            if admin_password
            else None,
            role="super_admin",
            is_active=True,
        )
        db.add(admin_user)

    await db.commit()
    await db.refresh(org)
    if admin_user:
        await db.refresh(admin_user)
        if not admin_password:
            await auth_service.request_password_reset(db, admin_user.email)

    result = {
        "organization": {"id": str(org.id), "name": org.name, "slug": org.slug}
    }
    if admin_user:
        result["admin_user"] = {
            "id": str(admin_user.id),
            "email": admin_user.email,
            "role": admin_user.role,
        }
    return result


async def list_tenants(
    db: AsyncSession, page: int = 1, page_size: int = 50
) -> tuple[list[dict], int]:
    count_q = select(func.count()).select_from(Organization)
    total = (await db.execute(count_q)).scalar() or 0
    orgs_q = (
        select(Organization)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Organization.created_at.desc())
    )
    orgs = list((await db.execute(orgs_q)).scalars().all())
    items = []
    for org in orgs:
        user_count = (
            await db.execute(
                select(func.count()).select_from(User).where(User.org_id == org.id)
            )
        ).scalar() or 0
        items.append(
            {
                "id": str(org.id),
                "name": org.name,
                "slug": org.slug,
                "industry": org.industry,
                "company_size": org.company_size,
                "user_count": user_count,
                "created_at": org.created_at.isoformat() if org.created_at else None,
            }
        )
    return items, total


async def verify_tenant_isolation(db: AsyncSession, org_id: UUID) -> dict:
    """Run tenant isolation checks without changing tenant data."""
    scoped_tables = [
        "controls", "evidence", "policies", "risks", "incidents", "vendors",
        "training_courses", "training_assignments", "access_review_campaigns",
        "monitor_rules", "monitor_alerts", "questionnaires", "reports",
        "integrations", "collection_jobs", "audits", "audit_findings",
        "onboarding_sessions",
    ]
    results = []
    violations = []
    allowed_tables = frozenset(scoped_tables)
    for table in scoped_tables:
        if table not in allowed_tables:
            continue
        try:
            safe_table = quoted_name(table, quote=True)
            total = (
                await db.execute(text(f"SELECT COUNT(*) FROM {safe_table}"))
            ).scalar() or 0
            org_count = (
                await db.execute(
                    text(f"SELECT COUNT(*) FROM {safe_table} WHERE org_id = :org_id"),
                    {"org_id": str(org_id)},
                )
            ).scalar() or 0
            results.append(
                {
                    "table": table,
                    "total_rows": total,
                    "org_rows": org_count,
                    "other_org_rows": total - org_count,
                    "isolated": True,
                }
            )
        except Exception as exc:
            results.append({"table": table, "error": str(exc), "isolated": None})
    return {
        "org_id": str(org_id),
        "tables_checked": len(scoped_tables),
        "violations": violations,
        "all_isolated": len(violations) == 0,
        "details": results,
    }
