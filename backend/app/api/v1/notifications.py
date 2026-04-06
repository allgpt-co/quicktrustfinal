from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel as PydanticBaseModel

from app.core.dependencies import DB, AnyInternalUser, AdminUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationStatsResponse,
    SlackWebhookCreate,
    SlackWebhookResponse,
)
from app.services import notification_service

router = APIRouter(
    prefix="/organizations/{org_id}/notifications",
    tags=["notifications"],
)


@router.get("", response_model=PaginatedResponse)
async def list_notifications(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    is_read: bool | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await notification_service.list_notifications(
        db, org_id, user_id=current_user.id, is_read=is_read,
        category=category, page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[NotificationResponse.model_validate(n) for n in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=NotificationResponse, status_code=201)
async def create_notification(
    org_id: VerifiedOrgId, data: NotificationCreate, db: DB, current_user: AdminUser,
):
    return await notification_service.create_notification(db, org_id, data)


@router.get("/stats", response_model=NotificationStatsResponse)
async def get_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await notification_service.get_notification_stats(
        db, org_id, user_id=current_user.id
    )


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_read(
    org_id: VerifiedOrgId, notification_id: UUID, db: DB, current_user: AnyInternalUser,
):
    return await notification_service.mark_read(db, org_id, notification_id)


@router.post("/read-all", response_model=MessageResponse)
async def mark_all_read(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    count = await notification_service.mark_all_read(db, org_id, user_id=current_user.id)
    return MessageResponse(message=f"Marked {count} notifications as read")


# --- Slack webhook configuration ---

@router.post("/slack", response_model=SlackWebhookResponse, status_code=201)
async def configure_slack(
    org_id: VerifiedOrgId, data: SlackWebhookCreate, db: DB, current_user: AdminUser,
):
    return await notification_service.configure_slack(
        db, org_id, data.webhook_url, data.channel_name, data.categories
    )


@router.get("/slack", response_model=SlackWebhookResponse | None)
async def get_slack_config(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    return await notification_service.get_slack_config(db, org_id)


@router.delete("/slack")
async def delete_slack_config(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    config = await notification_service.get_slack_config(db, org_id)
    if config:
        config.is_active = False
        await db.commit()
    return {"message": "Slack webhook disabled"}


@router.post("/test-slack")
async def test_slack(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    """Send a test message to the configured Slack webhook."""
    config = await notification_service.get_slack_config(db, org_id)
    if not config:
        from app.core.exceptions import BadRequestError
        raise BadRequestError("No Slack webhook configured")

    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(config.webhook_url, json={
                "text": ":white_check_mark: *QuickTrust Test Alert*\nSlack integration is working! Alerts will appear here."
            })
            if resp.status_code == 200:
                return {"message": "Test message sent to Slack successfully"}
            return {"message": f"Slack returned status {resp.status_code}"}
    except Exception as e:
        from app.core.exceptions import BadRequestError
        raise BadRequestError(f"Failed to send test message: {str(e)[:200]}")


@router.post("/run-alerts")
async def trigger_alert_engine(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    """Manually trigger the alert engine (evidence freshness + compliance regression)."""
    from app.services import alert_engine

    freshness = await alert_engine.check_evidence_freshness(db)
    regression = await alert_engine.check_compliance_regression(db)

    return {
        "message": "Alert engine completed",
        "freshness_alerts": freshness,
        "regression_alerts": regression,
    }


# --- PagerDuty configuration ---


class PagerDutyConfigCreate(PydanticBaseModel):
    routing_key: str


class PagerDutyConfigResponse(PydanticBaseModel):
    routing_key: str  # masked
    is_active: bool


@router.post("/pagerduty", response_model=PagerDutyConfigResponse, status_code=201)
async def configure_pagerduty(
    org_id: VerifiedOrgId, data: PagerDutyConfigCreate, db: DB, current_user: AdminUser,
):
    """Save PagerDuty routing key for this organization."""
    result = await notification_service.save_pagerduty_config(
        db, org_id, data.routing_key
    )
    return result


@router.get("/pagerduty")
async def get_pagerduty_config(org_id: VerifiedOrgId, db: DB, current_user: AdminUser):
    """Get PagerDuty configuration status for this organization."""
    config = await notification_service.get_pagerduty_config(db, org_id)
    if config:
        return {
            "routing_key": notification_service._mask_key(config.get("routing_key", "")),
            "is_active": config.get("is_active", False),
        }
    return {"routing_key": None, "is_active": False}
