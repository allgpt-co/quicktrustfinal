from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = UserRole.EMPLOYEE
    department: str | None = Field(None, max_length=100)


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=255)
    role: UserRole | None = None
    department: str | None = Field(None, max_length=100)
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: UUID
    org_id: UUID
    keycloak_id: str
    email: str
    full_name: str
    role: str
    department: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
