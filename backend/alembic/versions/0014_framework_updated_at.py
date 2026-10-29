"""Fix missing framework update timestamps.

Revision ID: 0014
Revises: 0013
"""
from alembic import op
import sqlalchemy as sa

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE frameworks SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP) WHERE updated_at IS NULL")
    op.alter_column("frameworks", "updated_at", existing_type=sa.DateTime(timezone=True),
                    server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False)


def downgrade():
    op.alter_column("frameworks", "updated_at", existing_type=sa.DateTime(timezone=True),
                    server_default=None, nullable=True)
