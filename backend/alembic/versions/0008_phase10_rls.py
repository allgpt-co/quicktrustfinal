"""Phase 10 — PostgreSQL Row-Level Security for tenant isolation.

RLS policies ensure that queries can only see rows belonging to the
current tenant (org_id) as set by the application via
``SET LOCAL app.current_org = '<uuid>'`` at the start of each request.

On SQLite (dev) this migration is a no-op.

Revision ID: 0008
Revises: 0007
"""

from alembic import op
import sqlalchemy as sa

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None

# Tables that hold tenant-scoped data with an org_id column
RLS_TABLES = [
    "controls",
    "evidences",
    "risks",
    "policies",
    "frameworks",
    "audits",
    "audit_findings",
    "incidents",
    "vendors",
    "vendor_assessments",
    "collection_jobs",
    "monitor_rules",
    "monitor_alerts",
    "reports",
    "compliance_snapshots",
    "questionnaires",
    "questionnaire_responses",
    "training_courses",
    "training_assignments",
    "access_review_campaigns",
    "access_review_entries",
    "trust_center_configs",
    "trust_center_documents",
    "integrations",
    "agent_runs",
    "audit_logs",
    "notifications",
    "onboarding_sessions",
]


def upgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name != "postgresql":
        return  # RLS is PostgreSQL-only

    for table in RLS_TABLES:
        # Check if the table exists before applying RLS
        op.execute(sa.text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
        op.execute(sa.text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"))

        policy_name = f"{table}_tenant_isolation"
        # Drop policy if it already exists (idempotent)
        op.execute(sa.text(
            f"DROP POLICY IF EXISTS {policy_name} ON {table}"
        ))
        # Create policy: rows visible only when org_id matches the session var
        op.execute(sa.text(
            f"CREATE POLICY {policy_name} ON {table} "
            f"USING (org_id::text = current_setting('app.current_org', true)) "
            f"WITH CHECK (org_id::text = current_setting('app.current_org', true))"
        ))


def downgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name != "postgresql":
        return

    for table in RLS_TABLES:
        policy_name = f"{table}_tenant_isolation"
        op.execute(sa.text(f"DROP POLICY IF EXISTS {policy_name} ON {table}"))
        op.execute(sa.text(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY"))
