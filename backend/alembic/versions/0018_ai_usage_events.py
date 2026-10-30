"""Persist questionnaire AI-call usage independently of generated answers.

Revision ID: 0018
Revises: 0017
"""
from alembic import op
import sqlalchemy as sa

revision = "0018"
down_revision = "0017"
branch_labels = None
depends_on = None


def upgrade():
    # Local seed tooling may have already created the new ORM table.
    inspector = sa.inspect(op.get_bind())
    if inspector.has_table("ai_usage_events"):
        required = {"id", "org_id", "user_id", "questionnaire_id", "job_id", "batch_index",
                    "model", "status", "prompt_tokens", "completion_tokens", "cost_micros",
                    "input_rate_per_million", "output_rate_per_million", "created_at", "recorded_at"}
        present = {column["name"] for column in inspector.get_columns("ai_usage_events")}
        if not required.issubset(present):
            raise RuntimeError("Existing ai_usage_events table is incomplete; reconcile before migrating")
        if "ix_ai_usage_org_created" not in {index["name"] for index in inspector.get_indexes("ai_usage_events")}:
            op.create_index("ix_ai_usage_org_created", "ai_usage_events", ["org_id", "created_at"])
        return
    op.create_table(
        "ai_usage_events",
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("org_id", sa.CHAR(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("user_id", sa.CHAR(36)),
        sa.Column("questionnaire_id", sa.CHAR(36), nullable=False),
        sa.Column("job_id", sa.CHAR(36)),
        sa.Column("batch_index", sa.Integer(), nullable=False),
        sa.Column("model", sa.String(255)),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("prompt_tokens", sa.BigInteger()),
        sa.Column("completion_tokens", sa.BigInteger()),
        sa.Column("cost_micros", sa.BigInteger()),
        sa.Column("input_rate_per_million", sa.Numeric(20, 8)),
        sa.Column("output_rate_per_million", sa.Numeric(20, 8)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_ai_usage_org_created", "ai_usage_events", ["org_id", "created_at"])


def downgrade():
    # Usage records are financial evidence; never drop them as a rollback side effect.
    raise RuntimeError("Forward-only migration: archive usage records before any schema removal")
