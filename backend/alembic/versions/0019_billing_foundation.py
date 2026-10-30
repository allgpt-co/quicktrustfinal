"""Add manual plan/subscription configuration without changing existing access.

Revision ID: 0019
Revises: 0018
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0019"
down_revision = "0018"
branch_labels = None
depends_on = None


def upgrade():
    # Static definitions keep this revision independent of future application models.
    json_type = sa.JSON().with_variant(JSONB(), "postgresql")
    metadata = sa.MetaData()
    sa.Table("organizations", metadata, sa.Column("id", sa.CHAR(36), primary_key=True))
    plans = sa.Table("billing_plans", metadata,
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("code", sa.String(80), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("limits", json_type, nullable=False),
        sa.Column("features", json_type, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    subscriptions = sa.Table("billing_subscriptions", metadata,
        sa.Column("id", sa.CHAR(36), primary_key=True),
        sa.Column("org_id", sa.CHAR(36), sa.ForeignKey("organizations.id"), unique=True, nullable=False),
        sa.Column("plan_id", sa.CHAR(36), sa.ForeignKey("billing_plans.id"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("source", sa.String(20), nullable=False),
        sa.Column("billing_interval", sa.String(10), nullable=False),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("trial_ends_at", sa.DateTime(timezone=True)),
        sa.Column("canceled_at", sa.DateTime(timezone=True)),
        sa.Column("contract_ref", sa.String(255)),
        sa.Column("limit_overrides", json_type, nullable=False),
        sa.Column("feature_overrides", json_type, nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("status IN ('trialing','active','past_due','suspended','canceled')", name="ck_subscription_status"),
        sa.CheckConstraint("source = 'manual'", name="ck_subscription_source"),
        sa.CheckConstraint("billing_interval IN ('month','year')", name="ck_subscription_interval"),
        sa.CheckConstraint("current_period_end > current_period_start", name="ck_subscription_period"),
        sa.CheckConstraint("status != 'trialing' OR trial_ends_at IS NOT NULL", name="ck_subscription_trial"),
        sa.CheckConstraint("version >= 1", name="ck_subscription_version"),
    )
    bind = op.get_bind()
    # Seed tooling can create ORM tables before migration. Validate rather than drop data.
    inspector = sa.inspect(bind)
    for table in (plans, subscriptions):
        if not inspector.has_table(table.name):
            table.create(bind)
            continue
        columns = {c["name"]: c for c in inspector.get_columns(table.name)}
        if any(c.name not in columns or (not c.nullable and columns[c.name]["nullable"])
               for c in table.columns):
            raise RuntimeError(f"Existing {table.name} schema is incomplete; reconcile before migrating")
        unique = {tuple(c["column_names"]) for c in inspector.get_unique_constraints(table.name)}
        expected_unique = ("code",) if table is plans else ("org_id",)
        if expected_unique not in unique:
            raise RuntimeError(f"Existing {table.name} lacks required uniqueness")
        if table is subscriptions:
            checks = {c["name"] for c in inspector.get_check_constraints(table.name)}
            expected = {c.name for c in table.constraints if isinstance(c, sa.CheckConstraint)}
            foreign_keys = {(tuple(c["constrained_columns"]), c["referred_table"]) for c in inspector.get_foreign_keys(table.name)}
            if not expected.issubset(checks) or not {(("org_id",), "organizations"), (("plan_id",), "billing_plans")}.issubset(foreign_keys):
                raise RuntimeError("Existing billing_subscriptions lacks required constraints")


def downgrade():
    raise RuntimeError("Forward-only migration: preserve customer subscription history")
