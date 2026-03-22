import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class SSOConfiguration(BaseModel):
    """SSO (SAML/OIDC) configuration per organization."""

    __tablename__ = "sso_configurations"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    provider: Mapped[str] = mapped_column(String(20), nullable=False, default="saml")
    # "saml" or "oidc"
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    enforced: Mapped[bool] = mapped_column(Boolean, default=False)
    # If enforced=True, users MUST use SSO (password login disabled)

    # SAML fields
    entity_id: Mapped[str | None] = mapped_column(String(500))
    sso_url: Mapped[str | None] = mapped_column(String(500))
    certificate: Mapped[str | None] = mapped_column(Text)

    # OIDC fields
    oidc_client_id: Mapped[str | None] = mapped_column(String(255))
    oidc_client_secret: Mapped[str | None] = mapped_column(String(500))
    oidc_issuer: Mapped[str | None] = mapped_column(String(500))

    # Domain mapping — which email domains use this SSO
    email_domains: Mapped[str | None] = mapped_column(Text)
    # Comma-separated: "company.com,subsidiary.com"

    # Attribute mapping (IdP attribute → QuickTrust field)
    attribute_mapping: Mapped[dict | None] = mapped_column(JSONType())

    # SCIM provisioning
    scim_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    scim_token_hash: Mapped[str | None] = mapped_column(String(255))
    # Hashed bearer token for SCIM API auth

    organization = relationship("Organization", back_populates="sso_config", lazy="selectin")


class SCIMToken(BaseModel):
    """SCIM bearer tokens for automated user provisioning."""

    __tablename__ = "scim_tokens"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
