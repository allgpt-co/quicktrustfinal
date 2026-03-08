"""Phase 10 — GDPR data retention and deletion request tables.

Revision ID: 0009
Revises: 0008
"""

from alembic import op
import sqlalchemy as sa

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # data_retention_policies
    op.create_table(
        "data_retention_policies",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("retention_days", sa.Integer, nullable=False),
        sa.Column("description", sa.String(500)),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36)),
        sa.Column("updated_by", sa.String(36)),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_data_retention_policies_org_id", "data_retention_policies", ["org_id"])

    # deletion_requests
    op.create_table(
        "deletion_requests",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("requested_by", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("reason", sa.String(1000)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36)),
        sa.Column("updated_by", sa.String(36)),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_deletion_requests_org_id", "deletion_requests", ["org_id"])
    op.create_index("ix_deletion_requests_target_user", "deletion_requests", ["target_user_id"])


def downgrade() -> None:
    op.drop_table("deletion_requests")
    op.drop_table("data_retention_policies")
