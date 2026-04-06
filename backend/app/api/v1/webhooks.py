"""Webhook management endpoints — register, list, delete, and test outbound webhooks."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel as PydanticBaseModel

from app.core.dependencies import DB, AdminUser, AnyInternalUser, VerifiedOrgId
from app.services import webhook_service

router = APIRouter(
    prefix="/organizations/{org_id}/webhooks",
    tags=["webhooks"],
)


# ---------- Schemas ----------

class WebhookCreate(PydanticBaseModel):
    url: str
    secret: str | None = None
    events: list[str] = []


class WebhookResponse(PydanticBaseModel):
    id: UUID
    org_id: UUID
    url: str
    events: list | None = None
    is_active: bool = True
    failure_count: int = 0
    last_triggered_at: datetime | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class WebhookDeliveryResponse(PydanticBaseModel):
    id: UUID
    webhook_id: UUID
    event_type: str
    payload: dict | None
    status_code: int | None
    response_body: str | None
    success: bool
    created_at: str | None = None

    model_config = {"from_attributes": True}


# ---------- Endpoints ----------

@router.get("", response_model=list[WebhookResponse])
async def list_webhooks(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
):
    """List all webhook endpoints for the organization."""
    items = await webhook_service.list_webhooks(db, org_id)
    return [WebhookResponse.model_validate(w) for w in items]


@router.post("", response_model=WebhookResponse, status_code=201)
async def create_webhook(
    org_id: VerifiedOrgId, data: WebhookCreate, db: DB, current_user: AdminUser,
):
    """Create a new webhook endpoint."""
    webhook = await webhook_service.create_webhook(
        db, org_id, data.url, data.secret, data.events,
    )
    return WebhookResponse.model_validate(webhook)


@router.delete("/{webhook_id}", status_code=204)
async def delete_webhook(
    org_id: VerifiedOrgId, webhook_id: UUID, db: DB, current_user: AdminUser,
):
    """Delete a webhook endpoint."""
    await webhook_service.delete_webhook(db, org_id, webhook_id)


@router.get("/{webhook_id}/deliveries", response_model=list[WebhookDeliveryResponse])
async def list_deliveries(
    org_id: VerifiedOrgId, webhook_id: UUID, db: DB, current_user: AnyInternalUser,
):
    """List recent deliveries for a webhook."""
    items = await webhook_service.list_deliveries(db, org_id, webhook_id)
    return [WebhookDeliveryResponse.model_validate(d) for d in items]


@router.post("/{webhook_id}/test")
async def test_webhook(
    org_id: VerifiedOrgId, webhook_id: UUID, db: DB, current_user: AdminUser,
):
    """Send a test event to the webhook endpoint."""
    return await webhook_service.send_test_event(db, org_id, webhook_id)
