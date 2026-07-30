"""Align the database objects required by application authentication.

Revision ID: 0012
Revises: 0011
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def _settings_type() -> sa.types.TypeEngine:
    """Match JSONType: JSONB on PostgreSQL and TEXT on SQLite."""
    if op.get_bind().dialect.name == "postgresql":
        return postgresql.JSONB()
    return sa.Text()


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("created_by", sa.String(36), nullable=True))
        batch_op.add_column(sa.Column("updated_by", sa.String(36), nullable=True))
        batch_op.add_column(
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
        )
        batch_op.create_unique_constraint("uq_users_email", ["email"])

    with op.batch_alter_table("organizations") as batch_op:
        batch_op.add_column(sa.Column("slug", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("settings", _settings_type(), nullable=True))
        batch_op.add_column(sa.Column("created_by", sa.String(36), nullable=True))
        batch_op.add_column(sa.Column("updated_by", sa.String(36), nullable=True))
        batch_op.add_column(
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
        )

    # Existing organizations predate the required slug. IDs are unique, so this
    # produces stable, collision-free values without changing organization data.
    op.execute(
        sa.text(
            """
            UPDATE organizations
            SET slug = 'org-' || replace(lower(CAST(id AS VARCHAR)), '-', '')
            WHERE slug IS NULL
            """
        )
    )

    with op.batch_alter_table("organizations") as batch_op:
        batch_op.alter_column(
            "slug",
            existing_type=sa.String(255),
            nullable=False,
        )
        batch_op.create_unique_constraint("uq_organizations_slug", ["slug"])

    op.create_table(
        "invitations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "invited_by",
            sa.String(36),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("token", sa.String(64), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_invitations_email", "invitations", ["email"])
    op.create_index(
        "ix_invitations_token",
        "invitations",
        ["token"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_table("invitations")

    with op.batch_alter_table("organizations") as batch_op:
        batch_op.drop_constraint("uq_organizations_slug", type_="unique")
        batch_op.drop_column("deleted_at")
        batch_op.drop_column("updated_by")
        batch_op.drop_column("created_by")
        batch_op.drop_column("settings")
        batch_op.drop_column("slug")

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_email", type_="unique")
        batch_op.drop_column("deleted_at")
        batch_op.drop_column("updated_by")
        batch_op.drop_column("created_by")
