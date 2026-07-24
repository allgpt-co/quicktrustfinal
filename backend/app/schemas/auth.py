from pydantic import BaseModel, EmailStr, Field


class TokenRequest(BaseModel):
    # Keep "username" for compatibility with the existing API contract; it is an email.
    username: EmailStr
    password: str = Field(..., min_length=1, max_length=1024)


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=12, max_length=1024)
    invitation_token: str | None = Field(None, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None


class UserInfo(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    org_id: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=32, max_length=256)
    new_password: str = Field(..., min_length=12, max_length=1024)
