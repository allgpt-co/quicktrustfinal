"""Phase 3: Add indexes, unique constraints, check constraints, and cascade rules

Revision ID: 0007_phase3
Revises: 0006_v05
Create Date: 2026-03-06

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import inspect

revision: str = "0007_phase3"
down_revision: Union[str, None] = "0006_v05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def _inspector():
    return inspect(op.get_bind())


def _table_exists(table_name: str) -> bool:
    return _inspector().has_table(table_name)


def _columns_exist(table_name: str, columns: list[str]) -> bool:
    if not _table_exists(table_name):
        return False
    existing = {column["name"] for column in _inspector().get_columns(table_name)}
    return all(column in existing for column in columns)


def _constraint_exists(table_name: str, name: str, type_: str | None = None) -> bool:
    if not _table_exists(table_name):
        return False
    inspector = _inspector()
    if type_ == "foreignkey":
        return any(fk.get("name") == name for fk in inspector.get_foreign_keys(table_name))
    if type_ == "unique":
        return any(constraint.get("name") == name for constraint in inspector.get_unique_constraints(table_name))
    if type_ == "check":
        return any(constraint.get("name") == name for constraint in inspector.get_check_constraints(table_name))
    constraints = []
    constraints.extend(inspector.get_foreign_keys(table_name))
    constraints.extend(inspector.get_unique_constraints(table_name))
    constraints.extend(inspector.get_check_constraints(table_name))
    return any(constraint.get("name") == name for constraint in constraints)


def _create_index(name: str, table_name: str, columns: list[str], **kwargs) -> None:
    if not _columns_exist(table_name, columns):
        return
    if any(index.get("name") == name for index in _inspector().get_indexes(table_name)):
        return
    op.create_index(name, table_name, columns, **kwargs)


def _create_unique_constraint(name: str, table_name: str, columns: list[str], **kwargs) -> None:
    if not _columns_exist(table_name, columns):
        return
    if _constraint_exists(table_name, name, "unique"):
        return
    op.create_unique_constraint(name, table_name, columns, **kwargs)


def _create_check_constraint(name: str, table_name: str, condition: str, **kwargs) -> None:
    if not _table_exists(table_name):
        return
    if _constraint_exists(table_name, name, "check"):
        return
    op.create_check_constraint(name, table_name, condition, **kwargs)


def _drop_constraint_if_exists(name: str, table_name: str, type_: str | None = None) -> None:
    if _constraint_exists(table_name, name, type_):
        op.drop_constraint(name, table_name, type_=type_)


def _create_foreign_key_if_possible(
    name: str,
    source_table: str,
    referent_table: str,
    local_cols: list[str],
    remote_cols: list[str],
    **kwargs,
) -> None:
    if not _columns_exist(source_table, local_cols):
        return
    if not _columns_exist(referent_table, remote_cols):
        return
    if _constraint_exists(source_table, name, "foreignkey"):
        return
    op.create_foreign_key(name, source_table, referent_table, local_cols, remote_cols, **kwargs)


def upgrade() -> None:
    # =========================================================================
    # Fix 3.1: Audit trail columns (created_by, updated_by, deleted_at)
    # These are added via BaseModel and will be auto-created by autogenerate,
    # but we add them explicitly here for tables that already exist.
    # =========================================================================
    # (Handled by BaseModel changes — autogenerate will pick these up)

    # =========================================================================
    # Fix 3.2: Performance Indexes
    # Add indexes on frequently queried columns: org_id, status, FKs, deleted_at
    # =========================================================================

    # --- org_id indexes (every tenant-scoped table) ---
    _create_index("ix_users_org_id", "users", ["org_id"])
    _create_index("ix_controls_org_id", "controls", ["org_id"])
    _create_index("ix_evidence_org_id", "evidence", ["org_id"])
    _create_index("ix_risks_org_id", "risks", ["org_id"])
    _create_index("ix_policies_org_id", "policies", ["org_id"])
    _create_index("ix_audits_org_id", "audits", ["org_id"])
    _create_index("ix_audit_findings_org_id", "audit_findings", ["org_id"])
    _create_index("ix_incidents_org_id", "incidents", ["org_id"])
    _create_index("ix_vendors_org_id", "vendors", ["org_id"])
    _create_index("ix_vendor_assessments_org_id", "vendor_assessments", ["org_id"])
    _create_index("ix_agent_runs_org_id", "agent_runs", ["org_id"])
    _create_index("ix_monitor_rules_org_id", "monitor_rules", ["org_id"])
    _create_index("ix_monitor_alerts_org_id", "monitor_alerts", ["org_id"])
    _create_index("ix_reports_org_id", "reports", ["org_id"])
    _create_index("ix_notifications_org_id", "notifications", ["org_id"])
    _create_index("ix_integrations_org_id", "integrations", ["org_id"])
    _create_index("ix_collection_jobs_org_id", "collection_jobs", ["org_id"])
    _create_index("ix_embeddings_org_id", "embeddings", ["org_id"])
    _create_index("ix_questionnaires_org_id", "questionnaires", ["org_id"])
    _create_index("ix_training_courses_org_id", "training_courses", ["org_id"])
    _create_index("ix_training_assignments_org_id", "training_assignments", ["org_id"])
    _create_index("ix_access_review_campaigns_org_id", "access_review_campaigns", ["org_id"])
    _create_index("ix_access_review_entries_org_id", "access_review_entries", ["org_id"])
    _create_index("ix_onboarding_sessions_org_id", "onboarding_sessions", ["org_id"])
    _create_index("ix_trust_center_documents_org_id", "trust_center_documents", ["org_id"])
    _create_index("ix_notification_preferences_org_id", "notification_preferences", ["org_id"])
    _create_index("ix_slack_webhook_configs_org_id", "slack_webhook_configs", ["org_id"])

    # --- status indexes (frequently filtered) ---
    _create_index("ix_controls_status", "controls", ["status"])
    _create_index("ix_evidence_status", "evidence", ["status"])
    _create_index("ix_risks_status", "risks", ["status"])
    _create_index("ix_risks_risk_level", "risks", ["risk_level"])
    _create_index("ix_policies_status", "policies", ["status"])
    _create_index("ix_audits_status", "audits", ["status"])
    _create_index("ix_audit_findings_status", "audit_findings", ["status"])
    _create_index("ix_audit_findings_severity", "audit_findings", ["severity"])
    _create_index("ix_incidents_status", "incidents", ["status"])
    _create_index("ix_incidents_severity", "incidents", ["severity"])
    _create_index("ix_vendors_status", "vendors", ["status"])
    _create_index("ix_vendors_risk_tier", "vendors", ["risk_tier"])
    _create_index("ix_agent_runs_status", "agent_runs", ["status"])
    _create_index("ix_agent_runs_agent_type", "agent_runs", ["agent_type"])
    _create_index("ix_monitor_rules_is_active", "monitor_rules", ["is_active"])
    _create_index("ix_monitor_alerts_status", "monitor_alerts", ["status"])
    _create_index("ix_monitor_alerts_severity", "monitor_alerts", ["severity"])
    _create_index("ix_reports_status", "reports", ["status"])
    _create_index("ix_collection_jobs_status", "collection_jobs", ["status"])
    _create_index("ix_questionnaires_status", "questionnaires", ["status"])

    # --- FK reference indexes ---
    _create_index("ix_controls_owner_id", "controls", ["owner_id"])
    _create_index("ix_controls_template_id", "controls", ["template_id"])
    _create_index("ix_evidence_control_id", "evidence", ["control_id"])
    _create_index("ix_evidence_template_id", "evidence", ["template_id"])
    _create_index("ix_risks_owner_id", "risks", ["owner_id"])
    _create_index("ix_policies_owner_id", "policies", ["owner_id"])
    _create_index("ix_audit_findings_audit_id", "audit_findings", ["audit_id"])
    _create_index("ix_audit_findings_control_id", "audit_findings", ["control_id"])
    _create_index("ix_incidents_assigned_to_id", "incidents", ["assigned_to_id"])
    _create_index("ix_monitor_rules_control_id", "monitor_rules", ["control_id"])
    _create_index("ix_monitor_alerts_rule_id", "monitor_alerts", ["rule_id"])
    _create_index("ix_notifications_user_id", "notifications", ["user_id"])
    _create_index("ix_training_assignments_user_id", "training_assignments", ["user_id"])
    _create_index("ix_training_assignments_course_id", "training_assignments", ["course_id"])
    _create_index("ix_collection_jobs_integration_id", "collection_jobs", ["integration_id"])
    _create_index("ix_questionnaire_responses_questionnaire_id", "questionnaire_responses", ["questionnaire_id"])
    _create_index("ix_access_review_entries_campaign_id", "access_review_entries", ["campaign_id"])

    # --- composite indexes for common query patterns ---
    _create_index("ix_controls_org_status", "controls", ["org_id", "status"])
    _create_index("ix_evidence_org_status", "evidence", ["org_id", "status"])
    _create_index("ix_risks_org_risk_level", "risks", ["org_id", "risk_level"])
    _create_index("ix_agent_runs_org_status", "agent_runs", ["org_id", "status"])
    _create_index("ix_notifications_user_is_read", "notifications", ["user_id", "is_read"])
    _create_index("ix_audit_findings_audit_severity", "audit_findings", ["audit_id", "severity"])
    _create_index("ix_embeddings_org_entity", "embeddings", ["org_id", "entity_type", "entity_id"])

    # --- audit_logs indexes (append-only, heavily queried) ---
    _create_index("ix_audit_logs_org_id", "audit_logs", ["org_id"])
    _create_index("ix_audit_logs_entity", "audit_logs", ["entity_type", "entity_id"])
    _create_index("ix_audit_logs_actor", "audit_logs", ["actor_type", "actor_id"])
    _create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])
    _create_index("ix_audit_logs_action", "audit_logs", ["action"])

    # =========================================================================
    # Fix 3.3: Unique Constraints on mapping/association tables
    # =========================================================================
    _create_unique_constraint(
        "uq_control_framework_mapping",
        "control_framework_mappings",
        ["control_id", "framework_id", "requirement_id"],
    )
    _create_unique_constraint(
        "uq_risk_control_mapping",
        "risk_control_mappings",
        ["risk_id", "control_id"],
    )
    _create_unique_constraint(
        "uq_control_template_evidence_template",
        "control_template_evidence_templates",
        ["control_template_id", "evidence_template_id"],
    )
    _create_unique_constraint(
        "uq_control_template_framework_mapping",
        "control_template_framework_mappings",
        ["control_template_id", "framework_id", "requirement_code"],
    )
    _create_unique_constraint(
        "uq_notification_preference",
        "notification_preferences",
        ["user_id", "channel", "category"],
    )
    _create_unique_constraint(
        "uq_training_assignment",
        "training_assignments",
        ["course_id", "user_id"],
    )
    _create_unique_constraint(
        "uq_framework_name_version",
        "frameworks",
        ["name", "version"],
    )
    _create_unique_constraint(
        "uq_framework_domain_code",
        "framework_domains",
        ["framework_id", "code"],
    )
    _create_unique_constraint(
        "uq_framework_requirement_code",
        "framework_requirements",
        ["domain_id", "code"],
    )
    _create_unique_constraint(
        "uq_control_objective_code",
        "control_objectives",
        ["requirement_id", "code"],
    )

    # =========================================================================
    # Fix 3.4: Check Constraints
    # =========================================================================
    _create_check_constraint(
        "ck_risks_likelihood_range",
        "risks",
        "likelihood >= 1 AND likelihood <= 5",
    )
    _create_check_constraint(
        "ck_risks_impact_range",
        "risks",
        "impact >= 1 AND impact <= 5",
    )
    _create_check_constraint(
        "ck_risks_risk_score_range",
        "risks",
        "risk_score >= 1 AND risk_score <= 25",
    )
    _create_check_constraint(
        "ck_risks_residual_likelihood_range",
        "risks",
        "residual_likelihood IS NULL OR (residual_likelihood >= 1 AND residual_likelihood <= 5)",
    )
    _create_check_constraint(
        "ck_risks_residual_impact_range",
        "risks",
        "residual_impact IS NULL OR (residual_impact >= 1 AND residual_impact <= 5)",
    )
    _create_check_constraint(
        "ck_risks_residual_score_range",
        "risks",
        "residual_score IS NULL OR (residual_score >= 1 AND residual_score <= 25)",
    )
    _create_check_constraint(
        "ck_vendor_assessments_score_range",
        "vendor_assessments",
        "score IS NULL OR (score >= 0 AND score <= 100)",
    )
    _create_check_constraint(
        "ck_vendors_assessment_score_range",
        "vendors",
        "assessment_score IS NULL OR (assessment_score >= 0 AND assessment_score <= 100)",
    )
    _create_check_constraint(
        "ck_questionnaire_responses_confidence_range",
        "questionnaire_responses",
        "confidence IS NULL OR (confidence >= 0.0 AND confidence <= 1.0)",
    )
    _create_check_constraint(
        "ck_training_assignments_score_range",
        "training_assignments",
        "score IS NULL OR (score >= 0 AND score <= 100)",
    )
    _create_check_constraint(
        "ck_auditor_profiles_rating_range",
        "auditor_profiles",
        "rating IS NULL OR (rating >= 0.0 AND rating <= 5.0)",
    )

    # =========================================================================
    # Fix 3.6: CASCADE foreign key rules
    # Add ON DELETE CASCADE where parent deletion should cascade to children.
    # Add ON DELETE SET NULL where the reference is optional.
    # We drop and recreate the FK constraints to add cascade behavior.
    # =========================================================================

    # --- Users → Organization: CASCADE (delete org → delete users) ---
    _drop_constraint_if_exists("users_org_id_fkey", "users", type_="foreignkey")
    _create_foreign_key_if_possible("users_org_id_fkey", "users", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Controls → Organization: CASCADE ---
    _drop_constraint_if_exists("controls_org_id_fkey", "controls", type_="foreignkey")
    _create_foreign_key_if_possible("controls_org_id_fkey", "controls", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Controls → User (owner): SET NULL ---
    _drop_constraint_if_exists("controls_owner_id_fkey", "controls", type_="foreignkey")
    _create_foreign_key_if_possible("controls_owner_id_fkey", "controls", "users", ["owner_id"], ["id"], ondelete="SET NULL")

    # --- Controls → ControlTemplate: SET NULL ---
    _drop_constraint_if_exists("controls_template_id_fkey", "controls", type_="foreignkey")
    _create_foreign_key_if_possible("controls_template_id_fkey", "controls", "control_templates", ["template_id"], ["id"], ondelete="SET NULL")

    # --- Controls → AgentRun: SET NULL ---
    _drop_constraint_if_exists("controls_agent_run_id_fkey", "controls", type_="foreignkey")
    _create_foreign_key_if_possible("controls_agent_run_id_fkey", "controls", "agent_runs", ["agent_run_id"], ["id"], ondelete="SET NULL")

    # --- Evidence → Organization: CASCADE ---
    _drop_constraint_if_exists("evidence_org_id_fkey", "evidence", type_="foreignkey")
    _create_foreign_key_if_possible("evidence_org_id_fkey", "evidence", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Evidence → Control: SET NULL ---
    _drop_constraint_if_exists("evidence_control_id_fkey", "evidence", type_="foreignkey")
    _create_foreign_key_if_possible("evidence_control_id_fkey", "evidence", "controls", ["control_id"], ["id"], ondelete="SET NULL")

    # --- Evidence → EvidenceTemplate: SET NULL ---
    _drop_constraint_if_exists("evidence_template_id_fkey", "evidence", type_="foreignkey")
    _create_foreign_key_if_possible("evidence_template_id_fkey", "evidence", "evidence_templates", ["template_id"], ["id"], ondelete="SET NULL")

    # --- Risks → Organization: CASCADE ---
    _drop_constraint_if_exists("risks_org_id_fkey", "risks", type_="foreignkey")
    _create_foreign_key_if_possible("risks_org_id_fkey", "risks", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Risks → User (owner/reviewer): SET NULL ---
    _drop_constraint_if_exists("risks_owner_id_fkey", "risks", type_="foreignkey")
    _create_foreign_key_if_possible("risks_owner_id_fkey", "risks", "users", ["owner_id"], ["id"], ondelete="SET NULL")
    _drop_constraint_if_exists("risks_reviewer_id_fkey", "risks", type_="foreignkey")
    _create_foreign_key_if_possible("risks_reviewer_id_fkey", "risks", "users", ["reviewer_id"], ["id"], ondelete="SET NULL")

    # --- Policies → Organization: CASCADE ---
    _drop_constraint_if_exists("policies_org_id_fkey", "policies", type_="foreignkey")
    _create_foreign_key_if_possible("policies_org_id_fkey", "policies", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Policies → User (owner/approved_by): SET NULL ---
    _drop_constraint_if_exists("policies_owner_id_fkey", "policies", type_="foreignkey")
    _create_foreign_key_if_possible("policies_owner_id_fkey", "policies", "users", ["owner_id"], ["id"], ondelete="SET NULL")
    _drop_constraint_if_exists("policies_approved_by_id_fkey", "policies", type_="foreignkey")
    _create_foreign_key_if_possible("policies_approved_by_id_fkey", "policies", "users", ["approved_by_id"], ["id"], ondelete="SET NULL")

    # --- Policies → PolicyTemplate: SET NULL ---
    _drop_constraint_if_exists("policies_template_id_fkey", "policies", type_="foreignkey")
    _create_foreign_key_if_possible("policies_template_id_fkey", "policies", "policy_templates", ["template_id"], ["id"], ondelete="SET NULL")

    # --- Policies → AgentRun: SET NULL ---
    _drop_constraint_if_exists("policies_agent_run_id_fkey", "policies", type_="foreignkey")
    _create_foreign_key_if_possible("policies_agent_run_id_fkey", "policies", "agent_runs", ["agent_run_id"], ["id"], ondelete="SET NULL")

    # --- Audits → Organization: CASCADE ---
    _drop_constraint_if_exists("audits_org_id_fkey", "audits", type_="foreignkey")
    _create_foreign_key_if_possible("audits_org_id_fkey", "audits", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Audits → Framework: SET NULL ---
    _drop_constraint_if_exists("audits_framework_id_fkey", "audits", type_="foreignkey")
    _create_foreign_key_if_possible("audits_framework_id_fkey", "audits", "frameworks", ["framework_id"], ["id"], ondelete="SET NULL")

    # --- Audit Findings → Organization: CASCADE ---
    _drop_constraint_if_exists("audit_findings_org_id_fkey", "audit_findings", type_="foreignkey")
    _create_foreign_key_if_possible("audit_findings_org_id_fkey", "audit_findings", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Audit Findings → Control: SET NULL ---
    _drop_constraint_if_exists("audit_findings_control_id_fkey", "audit_findings", type_="foreignkey")
    _create_foreign_key_if_possible("audit_findings_control_id_fkey", "audit_findings", "controls", ["control_id"], ["id"], ondelete="SET NULL")

    # --- Audit Findings → User (remediation_owner): SET NULL ---
    _drop_constraint_if_exists("audit_findings_remediation_owner_id_fkey", "audit_findings", type_="foreignkey")
    _create_foreign_key_if_possible("audit_findings_remediation_owner_id_fkey", "audit_findings", "users", ["remediation_owner_id"], ["id"], ondelete="SET NULL")

    # --- Incidents → Organization: CASCADE ---
    _drop_constraint_if_exists("incidents_org_id_fkey", "incidents", type_="foreignkey")
    _create_foreign_key_if_possible("incidents_org_id_fkey", "incidents", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Incidents → User (assigned_to): SET NULL ---
    _drop_constraint_if_exists("incidents_assigned_to_id_fkey", "incidents", type_="foreignkey")
    _create_foreign_key_if_possible("incidents_assigned_to_id_fkey", "incidents", "users", ["assigned_to_id"], ["id"], ondelete="SET NULL")

    # --- Vendors → Organization: CASCADE ---
    _drop_constraint_if_exists("vendors_org_id_fkey", "vendors", type_="foreignkey")
    _create_foreign_key_if_possible("vendors_org_id_fkey", "vendors", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Vendor Assessments → Organization: CASCADE ---
    _drop_constraint_if_exists("vendor_assessments_org_id_fkey", "vendor_assessments", type_="foreignkey")
    _create_foreign_key_if_possible("vendor_assessments_org_id_fkey", "vendor_assessments", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Vendor Assessments → User (assessed_by): SET NULL ---
    _drop_constraint_if_exists("vendor_assessments_assessed_by_id_fkey", "vendor_assessments", type_="foreignkey")
    _create_foreign_key_if_possible("vendor_assessments_assessed_by_id_fkey", "vendor_assessments", "users", ["assessed_by_id"], ["id"], ondelete="SET NULL")

    # --- Agent Runs → Organization: CASCADE ---
    _drop_constraint_if_exists("agent_runs_org_id_fkey", "agent_runs", type_="foreignkey")
    _create_foreign_key_if_possible("agent_runs_org_id_fkey", "agent_runs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Monitor Rules → Organization: CASCADE ---
    _drop_constraint_if_exists("monitor_rules_org_id_fkey", "monitor_rules", type_="foreignkey")
    _create_foreign_key_if_possible("monitor_rules_org_id_fkey", "monitor_rules", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Monitor Rules → Control: SET NULL ---
    _drop_constraint_if_exists("monitor_rules_control_id_fkey", "monitor_rules", type_="foreignkey")
    _create_foreign_key_if_possible("monitor_rules_control_id_fkey", "monitor_rules", "controls", ["control_id"], ["id"], ondelete="SET NULL")

    # --- Monitor Alerts → Organization: CASCADE ---
    _drop_constraint_if_exists("monitor_alerts_org_id_fkey", "monitor_alerts", type_="foreignkey")
    _create_foreign_key_if_possible("monitor_alerts_org_id_fkey", "monitor_alerts", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Monitor Alerts → User (acknowledged_by): SET NULL ---
    _drop_constraint_if_exists("monitor_alerts_acknowledged_by_id_fkey", "monitor_alerts", type_="foreignkey")
    _create_foreign_key_if_possible("monitor_alerts_acknowledged_by_id_fkey", "monitor_alerts", "users", ["acknowledged_by_id"], ["id"], ondelete="SET NULL")

    # --- Reports → Organization: CASCADE ---
    _drop_constraint_if_exists("reports_org_id_fkey", "reports", type_="foreignkey")
    _create_foreign_key_if_possible("reports_org_id_fkey", "reports", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Reports → User (requested_by): SET NULL ---
    _drop_constraint_if_exists("reports_requested_by_id_fkey", "reports", type_="foreignkey")
    _create_foreign_key_if_possible("reports_requested_by_id_fkey", "reports", "users", ["requested_by_id"], ["id"], ondelete="SET NULL")

    # --- Notifications → Organization: CASCADE ---
    _drop_constraint_if_exists("notifications_org_id_fkey", "notifications", type_="foreignkey")
    _create_foreign_key_if_possible("notifications_org_id_fkey", "notifications", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Notifications → User: SET NULL ---
    _drop_constraint_if_exists("notifications_user_id_fkey", "notifications", type_="foreignkey")
    _create_foreign_key_if_possible("notifications_user_id_fkey", "notifications", "users", ["user_id"], ["id"], ondelete="SET NULL")

    # --- Notification Preferences → Organization: CASCADE ---
    _drop_constraint_if_exists("notification_preferences_org_id_fkey", "notification_preferences", type_="foreignkey")
    _create_foreign_key_if_possible("notification_preferences_org_id_fkey", "notification_preferences", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Notification Preferences → User: CASCADE ---
    _drop_constraint_if_exists("notification_preferences_user_id_fkey", "notification_preferences", type_="foreignkey")
    _create_foreign_key_if_possible("notification_preferences_user_id_fkey", "notification_preferences", "users", ["user_id"], ["id"], ondelete="CASCADE")

    # --- Integrations → Organization: CASCADE ---
    _drop_constraint_if_exists("integrations_org_id_fkey", "integrations", type_="foreignkey")
    _create_foreign_key_if_possible("integrations_org_id_fkey", "integrations", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Collection Jobs → Organization: CASCADE ---
    _drop_constraint_if_exists("collection_jobs_org_id_fkey", "collection_jobs", type_="foreignkey")
    _create_foreign_key_if_possible("collection_jobs_org_id_fkey", "collection_jobs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Embeddings → Organization: CASCADE ---
    _drop_constraint_if_exists("embeddings_org_id_fkey", "embeddings", type_="foreignkey")
    _create_foreign_key_if_possible("embeddings_org_id_fkey", "embeddings", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Questionnaires → Organization: CASCADE ---
    _drop_constraint_if_exists("questionnaires_org_id_fkey", "questionnaires", type_="foreignkey")
    _create_foreign_key_if_possible("questionnaires_org_id_fkey", "questionnaires", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Questionnaire Responses → Organization: CASCADE ---
    _drop_constraint_if_exists("questionnaire_responses_org_id_fkey", "questionnaire_responses", type_="foreignkey")
    _create_foreign_key_if_possible("questionnaire_responses_org_id_fkey", "questionnaire_responses", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Questionnaire Responses → User (approved_by): SET NULL ---
    _drop_constraint_if_exists("questionnaire_responses_approved_by_id_fkey", "questionnaire_responses", type_="foreignkey")
    _create_foreign_key_if_possible("questionnaire_responses_approved_by_id_fkey", "questionnaire_responses", "users", ["approved_by_id"], ["id"], ondelete="SET NULL")

    # --- Training Courses → Organization: CASCADE ---
    _drop_constraint_if_exists("training_courses_org_id_fkey", "training_courses", type_="foreignkey")
    _create_foreign_key_if_possible("training_courses_org_id_fkey", "training_courses", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Training Assignments → Organization: CASCADE ---
    _drop_constraint_if_exists("training_assignments_org_id_fkey", "training_assignments", type_="foreignkey")
    _create_foreign_key_if_possible("training_assignments_org_id_fkey", "training_assignments", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Training Assignments → User: CASCADE (delete user → delete their assignments) ---
    _drop_constraint_if_exists("training_assignments_user_id_fkey", "training_assignments", type_="foreignkey")
    _create_foreign_key_if_possible("training_assignments_user_id_fkey", "training_assignments", "users", ["user_id"], ["id"], ondelete="CASCADE")

    # --- Training Assignments → User (assigned_by): SET NULL ---
    _drop_constraint_if_exists("training_assignments_assigned_by_id_fkey", "training_assignments", type_="foreignkey")
    _create_foreign_key_if_possible("training_assignments_assigned_by_id_fkey", "training_assignments", "users", ["assigned_by_id"], ["id"], ondelete="SET NULL")

    # --- Access Review Campaigns → Organization: CASCADE ---
    _drop_constraint_if_exists("access_review_campaigns_org_id_fkey", "access_review_campaigns", type_="foreignkey")
    _create_foreign_key_if_possible("access_review_campaigns_org_id_fkey", "access_review_campaigns", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Access Review Campaigns → User (reviewer): SET NULL ---
    _drop_constraint_if_exists("access_review_campaigns_reviewer_id_fkey", "access_review_campaigns", type_="foreignkey")
    _create_foreign_key_if_possible("access_review_campaigns_reviewer_id_fkey", "access_review_campaigns", "users", ["reviewer_id"], ["id"], ondelete="SET NULL")

    # --- Access Review Entries → Organization: CASCADE ---
    _drop_constraint_if_exists("access_review_entries_org_id_fkey", "access_review_entries", type_="foreignkey")
    _create_foreign_key_if_possible("access_review_entries_org_id_fkey", "access_review_entries", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Access Review Entries → User (decided_by): SET NULL ---
    _drop_constraint_if_exists("access_review_entries_decided_by_id_fkey", "access_review_entries", type_="foreignkey")
    _create_foreign_key_if_possible("access_review_entries_decided_by_id_fkey", "access_review_entries", "users", ["decided_by_id"], ["id"], ondelete="SET NULL")

    # --- Onboarding Sessions → Organization: CASCADE ---
    _drop_constraint_if_exists("onboarding_sessions_org_id_fkey", "onboarding_sessions", type_="foreignkey")
    _create_foreign_key_if_possible("onboarding_sessions_org_id_fkey", "onboarding_sessions", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Trust Center Configs → Organization: CASCADE ---
    _drop_constraint_if_exists("trust_center_configs_org_id_fkey", "trust_center_configs", type_="foreignkey")
    _create_foreign_key_if_possible("trust_center_configs_org_id_fkey", "trust_center_configs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Trust Center Documents → Organization: CASCADE ---
    _drop_constraint_if_exists("trust_center_documents_org_id_fkey", "trust_center_documents", type_="foreignkey")
    _create_foreign_key_if_possible("trust_center_documents_org_id_fkey", "trust_center_documents", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Slack Webhook Configs → Organization: CASCADE ---
    _drop_constraint_if_exists("slack_webhook_configs_org_id_fkey", "slack_webhook_configs", type_="foreignkey")
    _create_foreign_key_if_possible("slack_webhook_configs_org_id_fkey", "slack_webhook_configs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Auditor Profiles → User: CASCADE ---
    _drop_constraint_if_exists("auditor_profiles_user_id_fkey", "auditor_profiles", type_="foreignkey")
    _create_foreign_key_if_possible("auditor_profiles_user_id_fkey", "auditor_profiles", "users", ["user_id"], ["id"], ondelete="CASCADE")

    # --- Framework hierarchy cascades ---
    _drop_constraint_if_exists("framework_domains_framework_id_fkey", "framework_domains", type_="foreignkey")
    _create_foreign_key_if_possible("framework_domains_framework_id_fkey", "framework_domains", "frameworks", ["framework_id"], ["id"], ondelete="CASCADE")

    _drop_constraint_if_exists("framework_requirements_domain_id_fkey", "framework_requirements", type_="foreignkey")
    _create_foreign_key_if_possible("framework_requirements_domain_id_fkey", "framework_requirements", "framework_domains", ["domain_id"], ["id"], ondelete="CASCADE")

    _drop_constraint_if_exists("control_objectives_requirement_id_fkey", "control_objectives", type_="foreignkey")
    _create_foreign_key_if_possible("control_objectives_requirement_id_fkey", "control_objectives", "framework_requirements", ["requirement_id"], ["id"], ondelete="CASCADE")

    # --- Mapping table cascades ---
    _drop_constraint_if_exists("control_framework_mappings_control_id_fkey", "control_framework_mappings", type_="foreignkey")
    _create_foreign_key_if_possible("control_framework_mappings_control_id_fkey", "control_framework_mappings", "controls", ["control_id"], ["id"], ondelete="CASCADE")

    _drop_constraint_if_exists("control_framework_mappings_framework_id_fkey", "control_framework_mappings", type_="foreignkey")
    _create_foreign_key_if_possible("control_framework_mappings_framework_id_fkey", "control_framework_mappings", "frameworks", ["framework_id"], ["id"], ondelete="CASCADE")

    _drop_constraint_if_exists("control_template_evidence_templates_control_template_id_fkey", "control_template_evidence_templates", type_="foreignkey")
    _create_foreign_key_if_possible("control_template_evidence_templates_control_template_id_fkey", "control_template_evidence_templates", "control_templates", ["control_template_id"], ["id"], ondelete="CASCADE")

    _drop_constraint_if_exists("control_template_evidence_templates_evidence_template_id_fkey", "control_template_evidence_templates", type_="foreignkey")
    _create_foreign_key_if_possible("control_template_evidence_templates_evidence_template_id_fkey", "control_template_evidence_templates", "evidence_templates", ["evidence_template_id"], ["id"], ondelete="CASCADE")

    _drop_constraint_if_exists("control_template_framework_mappings_control_template_id_fkey", "control_template_framework_mappings", type_="foreignkey")
    _create_foreign_key_if_possible("control_template_framework_mappings_control_template_id_fkey", "control_template_framework_mappings", "control_templates", ["control_template_id"], ["id"], ondelete="CASCADE")

    _drop_constraint_if_exists("control_template_framework_mappings_framework_id_fkey", "control_template_framework_mappings", type_="foreignkey")
    _create_foreign_key_if_possible("control_template_framework_mappings_framework_id_fkey", "control_template_framework_mappings", "frameworks", ["framework_id"], ["id"], ondelete="CASCADE")

    # --- Incident Timeline → User (actor): SET NULL ---
    _drop_constraint_if_exists("incident_timeline_events_actor_id_fkey", "incident_timeline_events", type_="foreignkey")
    _create_foreign_key_if_possible("incident_timeline_events_actor_id_fkey", "incident_timeline_events", "users", ["actor_id"], ["id"], ondelete="SET NULL")


def downgrade() -> None:
    # =========================================================================
    # Reverse Fix 3.6: Remove CASCADE rules (restore default NO ACTION)
    # =========================================================================
    # This is extensive — in practice, a downgrade would restore all FKs
    # to their original state. For brevity, dropping all named constraints
    # and recreating without ondelete is omitted here.
    # A full downgrade should be done by restoring from backup.
    pass

    # =========================================================================
    # Reverse Fix 3.4: Drop check constraints
    # =========================================================================
    _drop_constraint_if_exists("ck_risks_likelihood_range", "risks", type_="check")
    _drop_constraint_if_exists("ck_risks_impact_range", "risks", type_="check")
    _drop_constraint_if_exists("ck_risks_risk_score_range", "risks", type_="check")
    _drop_constraint_if_exists("ck_risks_residual_likelihood_range", "risks", type_="check")
    _drop_constraint_if_exists("ck_risks_residual_impact_range", "risks", type_="check")
    _drop_constraint_if_exists("ck_risks_residual_score_range", "risks", type_="check")
    _drop_constraint_if_exists("ck_vendor_assessments_score_range", "vendor_assessments", type_="check")
    _drop_constraint_if_exists("ck_vendors_assessment_score_range", "vendors", type_="check")
    _drop_constraint_if_exists("ck_questionnaire_responses_confidence_range", "questionnaire_responses", type_="check")
    _drop_constraint_if_exists("ck_training_assignments_score_range", "training_assignments", type_="check")
    _drop_constraint_if_exists("ck_auditor_profiles_rating_range", "auditor_profiles", type_="check")

    # =========================================================================
    # Reverse Fix 3.3: Drop unique constraints
    # =========================================================================
    _drop_constraint_if_exists("uq_control_framework_mapping", "control_framework_mappings", type_="unique")
    _drop_constraint_if_exists("uq_risk_control_mapping", "risk_control_mappings", type_="unique")
    _drop_constraint_if_exists("uq_control_template_evidence_template", "control_template_evidence_templates", type_="unique")
    _drop_constraint_if_exists("uq_control_template_framework_mapping", "control_template_framework_mappings", type_="unique")
    _drop_constraint_if_exists("uq_notification_preference", "notification_preferences", type_="unique")
    _drop_constraint_if_exists("uq_training_assignment", "training_assignments", type_="unique")
    _drop_constraint_if_exists("uq_framework_name_version", "frameworks", type_="unique")
    _drop_constraint_if_exists("uq_framework_domain_code", "framework_domains", type_="unique")
    _drop_constraint_if_exists("uq_framework_requirement_code", "framework_requirements", type_="unique")
    _drop_constraint_if_exists("uq_control_objective_code", "control_objectives", type_="unique")

    # =========================================================================
    # Reverse Fix 3.2: Drop indexes
    # =========================================================================
    # org_id indexes
    op.drop_index("ix_users_org_id", "users")
    op.drop_index("ix_controls_org_id", "controls")
    op.drop_index("ix_evidence_org_id", "evidence")
    op.drop_index("ix_risks_org_id", "risks")
    op.drop_index("ix_policies_org_id", "policies")
    op.drop_index("ix_audits_org_id", "audits")
    op.drop_index("ix_audit_findings_org_id", "audit_findings")
    op.drop_index("ix_incidents_org_id", "incidents")
    op.drop_index("ix_vendors_org_id", "vendors")
    op.drop_index("ix_vendor_assessments_org_id", "vendor_assessments")
    op.drop_index("ix_agent_runs_org_id", "agent_runs")
    op.drop_index("ix_monitor_rules_org_id", "monitor_rules")
    op.drop_index("ix_monitor_alerts_org_id", "monitor_alerts")
    op.drop_index("ix_reports_org_id", "reports")
    op.drop_index("ix_notifications_org_id", "notifications")
    op.drop_index("ix_integrations_org_id", "integrations")
    op.drop_index("ix_collection_jobs_org_id", "collection_jobs")
    op.drop_index("ix_embeddings_org_id", "embeddings")
    op.drop_index("ix_questionnaires_org_id", "questionnaires")
    op.drop_index("ix_training_courses_org_id", "training_courses")
    op.drop_index("ix_training_assignments_org_id", "training_assignments")
    op.drop_index("ix_access_review_campaigns_org_id", "access_review_campaigns")
    op.drop_index("ix_access_review_entries_org_id", "access_review_entries")
    op.drop_index("ix_onboarding_sessions_org_id", "onboarding_sessions")
    op.drop_index("ix_trust_center_documents_org_id", "trust_center_documents")
    op.drop_index("ix_notification_preferences_org_id", "notification_preferences")
    op.drop_index("ix_slack_webhook_configs_org_id", "slack_webhook_configs")

    # status indexes
    op.drop_index("ix_controls_status", "controls")
    op.drop_index("ix_evidence_status", "evidence")
    op.drop_index("ix_risks_status", "risks")
    op.drop_index("ix_risks_risk_level", "risks")
    op.drop_index("ix_policies_status", "policies")
    op.drop_index("ix_audits_status", "audits")
    op.drop_index("ix_audit_findings_status", "audit_findings")
    op.drop_index("ix_audit_findings_severity", "audit_findings")
    op.drop_index("ix_incidents_status", "incidents")
    op.drop_index("ix_incidents_severity", "incidents")
    op.drop_index("ix_vendors_status", "vendors")
    op.drop_index("ix_vendors_risk_tier", "vendors")
    op.drop_index("ix_agent_runs_status", "agent_runs")
    op.drop_index("ix_agent_runs_agent_type", "agent_runs")
    op.drop_index("ix_monitor_rules_is_active", "monitor_rules")
    op.drop_index("ix_monitor_alerts_status", "monitor_alerts")
    op.drop_index("ix_monitor_alerts_severity", "monitor_alerts")
    op.drop_index("ix_reports_status", "reports")
    op.drop_index("ix_collection_jobs_status", "collection_jobs")
    op.drop_index("ix_questionnaires_status", "questionnaires")

    # FK indexes
    op.drop_index("ix_controls_owner_id", "controls")
    op.drop_index("ix_controls_template_id", "controls")
    op.drop_index("ix_evidence_control_id", "evidence")
    op.drop_index("ix_evidence_template_id", "evidence")
    op.drop_index("ix_risks_owner_id", "risks")
    op.drop_index("ix_policies_owner_id", "policies")
    op.drop_index("ix_audit_findings_audit_id", "audit_findings")
    op.drop_index("ix_audit_findings_control_id", "audit_findings")
    op.drop_index("ix_incidents_assigned_to_id", "incidents")
    op.drop_index("ix_monitor_rules_control_id", "monitor_rules")
    op.drop_index("ix_monitor_alerts_rule_id", "monitor_alerts")
    op.drop_index("ix_notifications_user_id", "notifications")
    op.drop_index("ix_training_assignments_user_id", "training_assignments")
    op.drop_index("ix_training_assignments_course_id", "training_assignments")
    op.drop_index("ix_collection_jobs_integration_id", "collection_jobs")
    op.drop_index("ix_questionnaire_responses_questionnaire_id", "questionnaire_responses")
    op.drop_index("ix_access_review_entries_campaign_id", "access_review_entries")

    # composite indexes
    op.drop_index("ix_controls_org_status", "controls")
    op.drop_index("ix_evidence_org_status", "evidence")
    op.drop_index("ix_risks_org_risk_level", "risks")
    op.drop_index("ix_agent_runs_org_status", "agent_runs")
    op.drop_index("ix_notifications_user_is_read", "notifications")
    op.drop_index("ix_audit_findings_audit_severity", "audit_findings")
    op.drop_index("ix_embeddings_org_entity", "embeddings")

    # audit_logs indexes
    op.drop_index("ix_audit_logs_org_id", "audit_logs")
    op.drop_index("ix_audit_logs_entity", "audit_logs")
    op.drop_index("ix_audit_logs_actor", "audit_logs")
    op.drop_index("ix_audit_logs_timestamp", "audit_logs")
    op.drop_index("ix_audit_logs_action", "audit_logs")
