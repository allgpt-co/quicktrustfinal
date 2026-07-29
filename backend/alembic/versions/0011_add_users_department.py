"""Add the nullable department column to users.

Revision ID: 0011
Revises: 0010
"""

from alembic import op
import sqlalchemy as sa


revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("department", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "department")
