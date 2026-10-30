"""Separate platform administration from customer organization roles.

All existing accounts retain their organization role but lose implicit global
access. Legitimate platform staff must be explicitly provisioned after upgrade.

Revision ID: 0016
Revises: 0015
"""
from alembic import op
import sqlalchemy as sa

revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column(
        "is_platform_admin", sa.Boolean(), nullable=False, server_default=sa.false(),
    ))


def downgrade():
    raise RuntimeError("Forward-only security migration: removing platform scope restores unsafe authorization")
