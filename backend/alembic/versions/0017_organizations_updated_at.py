"""Backfill organization update timestamps and align the column with the ORM.

Revision ID: 0017
Revises: 0016
"""
from alembic import op
import sqlalchemy as sa

revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE organizations SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP) "
        "WHERE updated_at IS NULL"
    )
    op.alter_column(
        "organizations", "updated_at", existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False,
    )


def downgrade():
    op.alter_column(
        "organizations", "updated_at", existing_type=sa.DateTime(timezone=True),
        server_default=None, nullable=True,
    )
