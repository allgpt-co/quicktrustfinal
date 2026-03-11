from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.enums import UserRole


class InvitationCreate(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.EMPLOYEE


class InvitationResponse(BaseModel):
    id: UUID
    org_id: UUID
    invited_by: UUID
    email: str
    role: str
    token: str
    status: str
    expires_at: datetime
    accepted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    # Flattened from relationships
    org_name: str | None = None
    inviter_name: str | None = None

    model_config = {"from_attributes": True}


class InvitationPublicResponse(BaseModel):
    """Public info shown on the invite accept page (no auth required)."""
    org_name: str
    inviter_name: str
    role: str
    email: str
    status: str
    expires_at: datetime
    is_expired: bool


class InvitationAcceptResponse(BaseModel):
    message: str
    org_id: UUID
    role: str
