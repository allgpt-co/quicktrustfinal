"""Add idempotent usage receipts, atomic counters and AI period snapshots.

Revision ID: 0020
Revises: 0019
"""
from alembic import op
import sqlalchemy as sa

revision = "0020"
down_revision = "0019"
branch_labels = None
depends_on = None

KINDS = "('LLM_COMPLETION','EMBEDDING','VECTOR_QUERY','VECTOR_UPSERT','STORAGE_BYTES','EMAIL','QUESTION_ANSWERED','QUESTION_MATCHED','QUESTIONNAIRE_PROCESSED')"
SOURCES = "('subscription','calendar_month','legacy_calendar_month')"


def _period_columns():
    return [sa.Column("org_id", sa.CHAR(36), sa.ForeignKey("organizations.id"), nullable=False),
            sa.Column("kind", sa.String(40), nullable=False),
            sa.Column("period_start", sa.DateTime(timezone=True), nullable=False),
            sa.Column("period_end", sa.DateTime(timezone=True), nullable=False),
            sa.Column("period_source", sa.String(30), nullable=False)]


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {c["name"] for c in inspector.get_columns("ai_usage_events")}
    for column in (sa.Column("usage_period_start", sa.DateTime(timezone=True)),
                   sa.Column("usage_period_end", sa.DateTime(timezone=True)),
                   sa.Column("usage_period_source", sa.String(30))):
        if column.name not in columns:
            op.add_column("ai_usage_events", column)
    # Historical calls are projected by the bounded backfill command, not guessed
    # into today's subscription or processed in one unbounded migration transaction.
    metadata = sa.MetaData()
    sa.Table("organizations", metadata, sa.Column("id", sa.CHAR(36), primary_key=True))
    events = sa.Table("usage_events", metadata,
        sa.Column("id", sa.CHAR(36), primary_key=True), *_period_columns(),
        sa.Column("idempotency_key", sa.String(200), nullable=False),
        sa.Column("user_id", sa.CHAR(36)),
        sa.Column("source_type", sa.String(40), nullable=False),
        sa.Column("source_id", sa.String(200), nullable=False),
        sa.Column("quantity", sa.BigInteger(), nullable=False),
        sa.Column("prompt_tokens", sa.BigInteger()),
        sa.Column("completion_tokens", sa.BigInteger()),
        sa.Column("cost_micros", sa.BigInteger()),
        sa.Column("is_mock", sa.Boolean(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("org_id", "kind", "idempotency_key", name="uq_usage_event_key"),
        sa.CheckConstraint("period_end > period_start", name="ck_usage_event_period"),
        sa.CheckConstraint("quantity >= 0 OR kind = 'STORAGE_BYTES'", name="ck_usage_event_quantity"),
        sa.CheckConstraint("cost_micros IS NULL OR cost_micros >= 0", name="ck_usage_event_cost"),
        sa.CheckConstraint("prompt_tokens IS NULL OR prompt_tokens >= 0", name="ck_usage_event_prompt"),
        sa.CheckConstraint("completion_tokens IS NULL OR completion_tokens >= 0", name="ck_usage_event_completion"),
        sa.CheckConstraint(f"kind IN {KINDS}", name="ck_usage_event_kind"),
        sa.CheckConstraint(f"period_source IN {SOURCES}", name="ck_usage_event_period_source"),
        sa.Index("ix_usage_events_org_occurred", "org_id", "occurred_at"),
    )
    counters = sa.Table("usage_counters", metadata,
        sa.Column("id", sa.CHAR(36), primary_key=True), *_period_columns(),
        *[sa.Column(name, sa.BigInteger(), nullable=False) for name in (
            "event_count", "quantity", "known_prompt_tokens", "known_completion_tokens",
            "known_cost_micros", "unknown_token_events", "unpriced_events")],
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("org_id", "kind", "period_start", "period_end", "period_source", name="uq_usage_counter_period"),
        sa.CheckConstraint("period_end > period_start", name="ck_usage_counter_period"),
        sa.CheckConstraint("quantity >= 0 OR kind = 'STORAGE_BYTES'", name="ck_usage_counter_quantity"),
        sa.CheckConstraint("event_count >= 0 AND known_prompt_tokens >= 0 AND known_completion_tokens >= 0 AND known_cost_micros >= 0 AND unknown_token_events >= 0 AND unpriced_events >= 0", name="ck_usage_counter_totals"),
        sa.CheckConstraint(f"kind IN {KINDS}", name="ck_usage_counter_kind"),
        sa.CheckConstraint(f"period_source IN {SOURCES}", name="ck_usage_counter_period_source"),
        sa.Index("ix_usage_counters_org_period", "org_id", "period_start"),
    )
    for table in (events, counters):
        if not inspector.has_table(table.name):
            table.create(bind)
            continue
        actual = {c["name"]: c for c in inspector.get_columns(table.name)}
        if any(c.name not in actual or (not c.nullable and actual[c.name]["nullable"]) for c in table.columns):
            raise RuntimeError(f"Existing {table.name} is incomplete; reconcile before migrating")
        unique = {tuple(c["column_names"]) for c in inspector.get_unique_constraints(table.name)}
        checks = {c["name"] for c in inspector.get_check_constraints(table.name)}
        required_unique = {tuple(c.columns.keys()) for c in table.constraints if isinstance(c, sa.UniqueConstraint)}
        required_checks = {c.name for c in table.constraints if isinstance(c, sa.CheckConstraint)}
        fks = {(tuple(c["constrained_columns"]), c["referred_table"]) for c in inspector.get_foreign_keys(table.name)}
        if not required_unique.issubset(unique) or not required_checks.issubset(checks) or (("org_id",), "organizations") not in fks:
            raise RuntimeError(f"Existing {table.name} lacks accounting constraints")
        indexes = {index["name"] for index in inspector.get_indexes(table.name)}
        for index in table.indexes:
            if index.name not in indexes:
                index.create(bind)


def downgrade():
    raise RuntimeError("Forward-only migration: preserve usage receipts and financial totals")
