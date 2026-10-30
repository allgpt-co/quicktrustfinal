"""Customer billing reads and explicitly platform-only commercial configuration."""
from fastapi import APIRouter, Query

from app.core.dependencies import DB, AdminUser, AnyInternalUser, PlatformAdminUser, VerifiedOrgId
from app.schemas.billing import BillingResponse, EntitlementResponse, PlanCreate, PlanResponse, SubscriptionPut, SubscriptionResponse
from app.services import billing_service, usage_service
from app.schemas.usage import UsageResponse

router = APIRouter(tags=["billing"])


@router.post("/admin/billing/plans", response_model=PlanResponse, status_code=201)
async def create_plan(data: PlanCreate, db: DB, current_user: PlatformAdminUser):
    return await billing_service.create_plan(db, data, current_user)


@router.get("/admin/billing/plans", response_model=list[PlanResponse])
async def list_plans(db: DB, current_user: PlatformAdminUser,
                     offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    return await billing_service.list_plans(db, offset, limit)


@router.put("/admin/organizations/{org_id}/subscription", response_model=SubscriptionResponse)
async def put_subscription(org_id: VerifiedOrgId, data: SubscriptionPut, db: DB, current_user: PlatformAdminUser):
    return await billing_service.put_subscription(db, org_id, data, current_user)


@router.get("/organizations/{org_id}/billing/subscription", response_model=BillingResponse)
async def get_subscription(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    return await billing_service.get_billing(db, org_id)


@router.get("/organizations/{org_id}/entitlements", response_model=EntitlementResponse)
async def get_entitlements(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await billing_service.get_entitlements(db, org_id)


# Consumption records are server-written only; customers cannot submit billable events.
@router.get("/organizations/{org_id}/billing/usage", response_model=UsageResponse)
async def get_usage(org_id: VerifiedOrgId, db: DB, current_user: AdminUser,
                    offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    return await usage_service.get_usage(db, org_id, offset=offset, limit=limit)
