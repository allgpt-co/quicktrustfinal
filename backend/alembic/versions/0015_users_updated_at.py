"""Backfill user update timestamps and align the column with the ORM.

Revision ID: 0015
Revises: 0014
"""
from alembic import op
import sqlalchemy as sa

revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE users SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP) "
        "WHERE updated_at IS NULL"
    )
    op.alter_column(
        "users", "updated_at", existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False,
    )


def downgrade():
    op.alter_column(
        "users", "updated_at", existing_type=sa.DateTime(timezone=True),
        server_default=None, nullable=True,
    )
