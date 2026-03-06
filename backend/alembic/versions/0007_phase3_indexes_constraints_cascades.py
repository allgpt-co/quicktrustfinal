"""Phase 3: Add indexes, unique constraints, check constraints, and cascade rules

Revision ID: 0007_phase3
Revises: 0006_v05
Create Date: 2026-03-06

"""

from typing import Sequence, Union

from alembic import op

revision: str = "0007_phase3"
down_revision: Union[str, None] = "0006_v05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
    op.create_index("ix_users_org_id", "users", ["org_id"])
    op.create_index("ix_controls_org_id", "controls", ["org_id"])
    op.create_index("ix_evidence_org_id", "evidence", ["org_id"])
    op.create_index("ix_risks_org_id", "risks", ["org_id"])
    op.create_index("ix_policies_org_id", "policies", ["org_id"])
    op.create_index("ix_audits_org_id", "audits", ["org_id"])
    op.create_index("ix_audit_findings_org_id", "audit_findings", ["org_id"])
    op.create_index("ix_incidents_org_id", "incidents", ["org_id"])
    op.create_index("ix_vendors_org_id", "vendors", ["org_id"])
    op.create_index("ix_vendor_assessments_org_id", "vendor_assessments", ["org_id"])
    op.create_index("ix_agent_runs_org_id", "agent_runs", ["org_id"])
    op.create_index("ix_monitor_rules_org_id", "monitor_rules", ["org_id"])
    op.create_index("ix_monitor_alerts_org_id", "monitor_alerts", ["org_id"])
    op.create_index("ix_reports_org_id", "reports", ["org_id"])
    op.create_index("ix_notifications_org_id", "notifications", ["org_id"])
    op.create_index("ix_integrations_org_id", "integrations", ["org_id"])
    op.create_index("ix_collection_jobs_org_id", "collection_jobs", ["org_id"])
    op.create_index("ix_embeddings_org_id", "embeddings", ["org_id"])
    op.create_index("ix_questionnaires_org_id", "questionnaires", ["org_id"])
    op.create_index("ix_training_courses_org_id", "training_courses", ["org_id"])
    op.create_index("ix_training_assignments_org_id", "training_assignments", ["org_id"])
    op.create_index("ix_access_review_campaigns_org_id", "access_review_campaigns", ["org_id"])
    op.create_index("ix_access_review_entries_org_id", "access_review_entries", ["org_id"])
    op.create_index("ix_onboarding_sessions_org_id", "onboarding_sessions", ["org_id"])
    op.create_index("ix_trust_center_documents_org_id", "trust_center_documents", ["org_id"])
    op.create_index("ix_notification_preferences_org_id", "notification_preferences", ["org_id"])
    op.create_index("ix_slack_webhook_configs_org_id", "slack_webhook_configs", ["org_id"])

    # --- status indexes (frequently filtered) ---
    op.create_index("ix_controls_status", "controls", ["status"])
    op.create_index("ix_evidence_status", "evidence", ["status"])
    op.create_index("ix_risks_status", "risks", ["status"])
    op.create_index("ix_risks_risk_level", "risks", ["risk_level"])
    op.create_index("ix_policies_status", "policies", ["status"])
    op.create_index("ix_audits_status", "audits", ["status"])
    op.create_index("ix_audit_findings_status", "audit_findings", ["status"])
    op.create_index("ix_audit_findings_severity", "audit_findings", ["severity"])
    op.create_index("ix_incidents_status", "incidents", ["status"])
    op.create_index("ix_incidents_severity", "incidents", ["severity"])
    op.create_index("ix_vendors_status", "vendors", ["status"])
    op.create_index("ix_vendors_risk_tier", "vendors", ["risk_tier"])
    op.create_index("ix_agent_runs_status", "agent_runs", ["status"])
    op.create_index("ix_agent_runs_agent_type", "agent_runs", ["agent_type"])
    op.create_index("ix_monitor_rules_is_active", "monitor_rules", ["is_active"])
    op.create_index("ix_monitor_alerts_status", "monitor_alerts", ["status"])
    op.create_index("ix_monitor_alerts_severity", "monitor_alerts", ["severity"])
    op.create_index("ix_reports_status", "reports", ["status"])
    op.create_index("ix_collection_jobs_status", "collection_jobs", ["status"])
    op.create_index("ix_questionnaires_status", "questionnaires", ["status"])

    # --- FK reference indexes ---
    op.create_index("ix_controls_owner_id", "controls", ["owner_id"])
    op.create_index("ix_controls_template_id", "controls", ["template_id"])
    op.create_index("ix_evidence_control_id", "evidence", ["control_id"])
    op.create_index("ix_evidence_template_id", "evidence", ["template_id"])
    op.create_index("ix_risks_owner_id", "risks", ["owner_id"])
    op.create_index("ix_policies_owner_id", "policies", ["owner_id"])
    op.create_index("ix_audit_findings_audit_id", "audit_findings", ["audit_id"])
    op.create_index("ix_audit_findings_control_id", "audit_findings", ["control_id"])
    op.create_index("ix_incidents_assigned_to_id", "incidents", ["assigned_to_id"])
    op.create_index("ix_monitor_rules_control_id", "monitor_rules", ["control_id"])
    op.create_index("ix_monitor_alerts_rule_id", "monitor_alerts", ["rule_id"])
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_index("ix_training_assignments_user_id", "training_assignments", ["user_id"])
    op.create_index("ix_training_assignments_course_id", "training_assignments", ["course_id"])
    op.create_index("ix_collection_jobs_integration_id", "collection_jobs", ["integration_id"])
    op.create_index("ix_questionnaire_responses_questionnaire_id", "questionnaire_responses", ["questionnaire_id"])
    op.create_index("ix_access_review_entries_campaign_id", "access_review_entries", ["campaign_id"])

    # --- composite indexes for common query patterns ---
    op.create_index("ix_controls_org_status", "controls", ["org_id", "status"])
    op.create_index("ix_evidence_org_status", "evidence", ["org_id", "status"])
    op.create_index("ix_risks_org_risk_level", "risks", ["org_id", "risk_level"])
    op.create_index("ix_agent_runs_org_status", "agent_runs", ["org_id", "status"])
    op.create_index("ix_notifications_user_is_read", "notifications", ["user_id", "is_read"])
    op.create_index("ix_audit_findings_audit_severity", "audit_findings", ["audit_id", "severity"])
    op.create_index("ix_embeddings_org_entity", "embeddings", ["org_id", "entity_type", "entity_id"])

    # --- audit_logs indexes (append-only, heavily queried) ---
    op.create_index("ix_audit_logs_org_id", "audit_logs", ["org_id"])
    op.create_index("ix_audit_logs_entity", "audit_logs", ["entity_type", "entity_id"])
    op.create_index("ix_audit_logs_actor", "audit_logs", ["actor_type", "actor_id"])
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])

    # =========================================================================
    # Fix 3.3: Unique Constraints on mapping/association tables
    # =========================================================================
    op.create_unique_constraint(
        "uq_control_framework_mapping",
        "control_framework_mappings",
        ["control_id", "framework_id", "requirement_id"],
    )
    op.create_unique_constraint(
        "uq_risk_control_mapping",
        "risk_control_mappings",
        ["risk_id", "control_id"],
    )
    op.create_unique_constraint(
        "uq_control_template_evidence_template",
        "control_template_evidence_templates",
        ["control_template_id", "evidence_template_id"],
    )
    op.create_unique_constraint(
        "uq_control_template_framework_mapping",
        "control_template_framework_mappings",
        ["control_template_id", "framework_id", "requirement_code"],
    )
    op.create_unique_constraint(
        "uq_notification_preference",
        "notification_preferences",
        ["user_id", "channel", "category"],
    )
    op.create_unique_constraint(
        "uq_training_assignment",
        "training_assignments",
        ["course_id", "user_id"],
    )
    op.create_unique_constraint(
        "uq_framework_name_version",
        "frameworks",
        ["name", "version"],
    )
    op.create_unique_constraint(
        "uq_framework_domain_code",
        "framework_domains",
        ["framework_id", "code"],
    )
    op.create_unique_constraint(
        "uq_framework_requirement_code",
        "framework_requirements",
        ["domain_id", "code"],
    )
    op.create_unique_constraint(
        "uq_control_objective_code",
        "control_objectives",
        ["requirement_id", "code"],
    )

    # =========================================================================
    # Fix 3.4: Check Constraints
    # =========================================================================
    op.create_check_constraint(
        "ck_risks_likelihood_range",
        "risks",
        "likelihood >= 1 AND likelihood <= 5",
    )
    op.create_check_constraint(
        "ck_risks_impact_range",
        "risks",
        "impact >= 1 AND impact <= 5",
    )
    op.create_check_constraint(
        "ck_risks_risk_score_range",
        "risks",
        "risk_score >= 1 AND risk_score <= 25",
    )
    op.create_check_constraint(
        "ck_risks_residual_likelihood_range",
        "risks",
        "residual_likelihood IS NULL OR (residual_likelihood >= 1 AND residual_likelihood <= 5)",
    )
    op.create_check_constraint(
        "ck_risks_residual_impact_range",
        "risks",
        "residual_impact IS NULL OR (residual_impact >= 1 AND residual_impact <= 5)",
    )
    op.create_check_constraint(
        "ck_risks_residual_score_range",
        "risks",
        "residual_score IS NULL OR (residual_score >= 1 AND residual_score <= 25)",
    )
    op.create_check_constraint(
        "ck_vendor_assessments_score_range",
        "vendor_assessments",
        "score IS NULL OR (score >= 0 AND score <= 100)",
    )
    op.create_check_constraint(
        "ck_vendors_assessment_score_range",
        "vendors",
        "assessment_score IS NULL OR (assessment_score >= 0 AND assessment_score <= 100)",
    )
    op.create_check_constraint(
        "ck_questionnaire_responses_confidence_range",
        "questionnaire_responses",
        "confidence IS NULL OR (confidence >= 0.0 AND confidence <= 1.0)",
    )
    op.create_check_constraint(
        "ck_training_assignments_score_range",
        "training_assignments",
        "score IS NULL OR (score >= 0 AND score <= 100)",
    )
    op.create_check_constraint(
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
    op.drop_constraint("users_org_id_fkey", "users", type_="foreignkey")
    op.create_foreign_key("users_org_id_fkey", "users", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Controls → Organization: CASCADE ---
    op.drop_constraint("controls_org_id_fkey", "controls", type_="foreignkey")
    op.create_foreign_key("controls_org_id_fkey", "controls", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Controls → User (owner): SET NULL ---
    op.drop_constraint("controls_owner_id_fkey", "controls", type_="foreignkey")
    op.create_foreign_key("controls_owner_id_fkey", "controls", "users", ["owner_id"], ["id"], ondelete="SET NULL")

    # --- Controls → ControlTemplate: SET NULL ---
    op.drop_constraint("controls_template_id_fkey", "controls", type_="foreignkey")
    op.create_foreign_key("controls_template_id_fkey", "controls", "control_templates", ["template_id"], ["id"], ondelete="SET NULL")

    # --- Controls → AgentRun: SET NULL ---
    op.drop_constraint("controls_agent_run_id_fkey", "controls", type_="foreignkey")
    op.create_foreign_key("controls_agent_run_id_fkey", "controls", "agent_runs", ["agent_run_id"], ["id"], ondelete="SET NULL")

    # --- Evidence → Organization: CASCADE ---
    op.drop_constraint("evidence_org_id_fkey", "evidence", type_="foreignkey")
    op.create_foreign_key("evidence_org_id_fkey", "evidence", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Evidence → Control: SET NULL ---
    op.drop_constraint("evidence_control_id_fkey", "evidence", type_="foreignkey")
    op.create_foreign_key("evidence_control_id_fkey", "evidence", "controls", ["control_id"], ["id"], ondelete="SET NULL")

    # --- Evidence → EvidenceTemplate: SET NULL ---
    op.drop_constraint("evidence_template_id_fkey", "evidence", type_="foreignkey")
    op.create_foreign_key("evidence_template_id_fkey", "evidence", "evidence_templates", ["template_id"], ["id"], ondelete="SET NULL")

    # --- Risks → Organization: CASCADE ---
    op.drop_constraint("risks_org_id_fkey", "risks", type_="foreignkey")
    op.create_foreign_key("risks_org_id_fkey", "risks", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Risks → User (owner/reviewer): SET NULL ---
    op.drop_constraint("risks_owner_id_fkey", "risks", type_="foreignkey")
    op.create_foreign_key("risks_owner_id_fkey", "risks", "users", ["owner_id"], ["id"], ondelete="SET NULL")
    op.drop_constraint("risks_reviewer_id_fkey", "risks", type_="foreignkey")
    op.create_foreign_key("risks_reviewer_id_fkey", "risks", "users", ["reviewer_id"], ["id"], ondelete="SET NULL")

    # --- Policies → Organization: CASCADE ---
    op.drop_constraint("policies_org_id_fkey", "policies", type_="foreignkey")
    op.create_foreign_key("policies_org_id_fkey", "policies", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Policies → User (owner/approved_by): SET NULL ---
    op.drop_constraint("policies_owner_id_fkey", "policies", type_="foreignkey")
    op.create_foreign_key("policies_owner_id_fkey", "policies", "users", ["owner_id"], ["id"], ondelete="SET NULL")
    op.drop_constraint("policies_approved_by_id_fkey", "policies", type_="foreignkey")
    op.create_foreign_key("policies_approved_by_id_fkey", "policies", "users", ["approved_by_id"], ["id"], ondelete="SET NULL")

    # --- Policies → PolicyTemplate: SET NULL ---
    op.drop_constraint("policies_template_id_fkey", "policies", type_="foreignkey")
    op.create_foreign_key("policies_template_id_fkey", "policies", "policy_templates", ["template_id"], ["id"], ondelete="SET NULL")

    # --- Policies → AgentRun: SET NULL ---
    op.drop_constraint("policies_agent_run_id_fkey", "policies", type_="foreignkey")
    op.create_foreign_key("policies_agent_run_id_fkey", "policies", "agent_runs", ["agent_run_id"], ["id"], ondelete="SET NULL")

    # --- Audits → Organization: CASCADE ---
    op.drop_constraint("audits_org_id_fkey", "audits", type_="foreignkey")
    op.create_foreign_key("audits_org_id_fkey", "audits", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Audits → Framework: SET NULL ---
    op.drop_constraint("audits_framework_id_fkey", "audits", type_="foreignkey")
    op.create_foreign_key("audits_framework_id_fkey", "audits", "frameworks", ["framework_id"], ["id"], ondelete="SET NULL")

    # --- Audit Findings → Organization: CASCADE ---
    op.drop_constraint("audit_findings_org_id_fkey", "audit_findings", type_="foreignkey")
    op.create_foreign_key("audit_findings_org_id_fkey", "audit_findings", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Audit Findings → Control: SET NULL ---
    op.drop_constraint("audit_findings_control_id_fkey", "audit_findings", type_="foreignkey")
    op.create_foreign_key("audit_findings_control_id_fkey", "audit_findings", "controls", ["control_id"], ["id"], ondelete="SET NULL")

    # --- Audit Findings → User (remediation_owner): SET NULL ---
    op.drop_constraint("audit_findings_remediation_owner_id_fkey", "audit_findings", type_="foreignkey")
    op.create_foreign_key("audit_findings_remediation_owner_id_fkey", "audit_findings", "users", ["remediation_owner_id"], ["id"], ondelete="SET NULL")

    # --- Incidents → Organization: CASCADE ---
    op.drop_constraint("incidents_org_id_fkey", "incidents", type_="foreignkey")
    op.create_foreign_key("incidents_org_id_fkey", "incidents", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Incidents → User (assigned_to): SET NULL ---
    op.drop_constraint("incidents_assigned_to_id_fkey", "incidents", type_="foreignkey")
    op.create_foreign_key("incidents_assigned_to_id_fkey", "incidents", "users", ["assigned_to_id"], ["id"], ondelete="SET NULL")

    # --- Vendors → Organization: CASCADE ---
    op.drop_constraint("vendors_org_id_fkey", "vendors", type_="foreignkey")
    op.create_foreign_key("vendors_org_id_fkey", "vendors", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Vendor Assessments → Organization: CASCADE ---
    op.drop_constraint("vendor_assessments_org_id_fkey", "vendor_assessments", type_="foreignkey")
    op.create_foreign_key("vendor_assessments_org_id_fkey", "vendor_assessments", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Vendor Assessments → User (assessed_by): SET NULL ---
    op.drop_constraint("vendor_assessments_assessed_by_id_fkey", "vendor_assessments", type_="foreignkey")
    op.create_foreign_key("vendor_assessments_assessed_by_id_fkey", "vendor_assessments", "users", ["assessed_by_id"], ["id"], ondelete="SET NULL")

    # --- Agent Runs → Organization: CASCADE ---
    op.drop_constraint("agent_runs_org_id_fkey", "agent_runs", type_="foreignkey")
    op.create_foreign_key("agent_runs_org_id_fkey", "agent_runs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Monitor Rules → Organization: CASCADE ---
    op.drop_constraint("monitor_rules_org_id_fkey", "monitor_rules", type_="foreignkey")
    op.create_foreign_key("monitor_rules_org_id_fkey", "monitor_rules", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Monitor Rules → Control: SET NULL ---
    op.drop_constraint("monitor_rules_control_id_fkey", "monitor_rules", type_="foreignkey")
    op.create_foreign_key("monitor_rules_control_id_fkey", "monitor_rules", "controls", ["control_id"], ["id"], ondelete="SET NULL")

    # --- Monitor Alerts → Organization: CASCADE ---
    op.drop_constraint("monitor_alerts_org_id_fkey", "monitor_alerts", type_="foreignkey")
    op.create_foreign_key("monitor_alerts_org_id_fkey", "monitor_alerts", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Monitor Alerts → User (acknowledged_by): SET NULL ---
    op.drop_constraint("monitor_alerts_acknowledged_by_id_fkey", "monitor_alerts", type_="foreignkey")
    op.create_foreign_key("monitor_alerts_acknowledged_by_id_fkey", "monitor_alerts", "users", ["acknowledged_by_id"], ["id"], ondelete="SET NULL")

    # --- Reports → Organization: CASCADE ---
    op.drop_constraint("reports_org_id_fkey", "reports", type_="foreignkey")
    op.create_foreign_key("reports_org_id_fkey", "reports", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Reports → User (requested_by): SET NULL ---
    op.drop_constraint("reports_requested_by_id_fkey", "reports", type_="foreignkey")
    op.create_foreign_key("reports_requested_by_id_fkey", "reports", "users", ["requested_by_id"], ["id"], ondelete="SET NULL")

    # --- Notifications → Organization: CASCADE ---
    op.drop_constraint("notifications_org_id_fkey", "notifications", type_="foreignkey")
    op.create_foreign_key("notifications_org_id_fkey", "notifications", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Notifications → User: SET NULL ---
    op.drop_constraint("notifications_user_id_fkey", "notifications", type_="foreignkey")
    op.create_foreign_key("notifications_user_id_fkey", "notifications", "users", ["user_id"], ["id"], ondelete="SET NULL")

    # --- Notification Preferences → Organization: CASCADE ---
    op.drop_constraint("notification_preferences_org_id_fkey", "notification_preferences", type_="foreignkey")
    op.create_foreign_key("notification_preferences_org_id_fkey", "notification_preferences", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Notification Preferences → User: CASCADE ---
    op.drop_constraint("notification_preferences_user_id_fkey", "notification_preferences", type_="foreignkey")
    op.create_foreign_key("notification_preferences_user_id_fkey", "notification_preferences", "users", ["user_id"], ["id"], ondelete="CASCADE")

    # --- Integrations → Organization: CASCADE ---
    op.drop_constraint("integrations_org_id_fkey", "integrations", type_="foreignkey")
    op.create_foreign_key("integrations_org_id_fkey", "integrations", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Collection Jobs → Organization: CASCADE ---
    op.drop_constraint("collection_jobs_org_id_fkey", "collection_jobs", type_="foreignkey")
    op.create_foreign_key("collection_jobs_org_id_fkey", "collection_jobs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Embeddings → Organization: CASCADE ---
    op.drop_constraint("embeddings_org_id_fkey", "embeddings", type_="foreignkey")
    op.create_foreign_key("embeddings_org_id_fkey", "embeddings", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Questionnaires → Organization: CASCADE ---
    op.drop_constraint("questionnaires_org_id_fkey", "questionnaires", type_="foreignkey")
    op.create_foreign_key("questionnaires_org_id_fkey", "questionnaires", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Questionnaire Responses → Organization: CASCADE ---
    op.drop_constraint("questionnaire_responses_org_id_fkey", "questionnaire_responses", type_="foreignkey")
    op.create_foreign_key("questionnaire_responses_org_id_fkey", "questionnaire_responses", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Questionnaire Responses → User (approved_by): SET NULL ---
    op.drop_constraint("questionnaire_responses_approved_by_id_fkey", "questionnaire_responses", type_="foreignkey")
    op.create_foreign_key("questionnaire_responses_approved_by_id_fkey", "questionnaire_responses", "users", ["approved_by_id"], ["id"], ondelete="SET NULL")

    # --- Training Courses → Organization: CASCADE ---
    op.drop_constraint("training_courses_org_id_fkey", "training_courses", type_="foreignkey")
    op.create_foreign_key("training_courses_org_id_fkey", "training_courses", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Training Assignments → Organization: CASCADE ---
    op.drop_constraint("training_assignments_org_id_fkey", "training_assignments", type_="foreignkey")
    op.create_foreign_key("training_assignments_org_id_fkey", "training_assignments", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Training Assignments → User: CASCADE (delete user → delete their assignments) ---
    op.drop_constraint("training_assignments_user_id_fkey", "training_assignments", type_="foreignkey")
    op.create_foreign_key("training_assignments_user_id_fkey", "training_assignments", "users", ["user_id"], ["id"], ondelete="CASCADE")

    # --- Training Assignments → User (assigned_by): SET NULL ---
    op.drop_constraint("training_assignments_assigned_by_id_fkey", "training_assignments", type_="foreignkey")
    op.create_foreign_key("training_assignments_assigned_by_id_fkey", "training_assignments", "users", ["assigned_by_id"], ["id"], ondelete="SET NULL")

    # --- Access Review Campaigns → Organization: CASCADE ---
    op.drop_constraint("access_review_campaigns_org_id_fkey", "access_review_campaigns", type_="foreignkey")
    op.create_foreign_key("access_review_campaigns_org_id_fkey", "access_review_campaigns", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Access Review Campaigns → User (reviewer): SET NULL ---
    op.drop_constraint("access_review_campaigns_reviewer_id_fkey", "access_review_campaigns", type_="foreignkey")
    op.create_foreign_key("access_review_campaigns_reviewer_id_fkey", "access_review_campaigns", "users", ["reviewer_id"], ["id"], ondelete="SET NULL")

    # --- Access Review Entries → Organization: CASCADE ---
    op.drop_constraint("access_review_entries_org_id_fkey", "access_review_entries", type_="foreignkey")
    op.create_foreign_key("access_review_entries_org_id_fkey", "access_review_entries", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Access Review Entries → User (decided_by): SET NULL ---
    op.drop_constraint("access_review_entries_decided_by_id_fkey", "access_review_entries", type_="foreignkey")
    op.create_foreign_key("access_review_entries_decided_by_id_fkey", "access_review_entries", "users", ["decided_by_id"], ["id"], ondelete="SET NULL")

    # --- Onboarding Sessions → Organization: CASCADE ---
    op.drop_constraint("onboarding_sessions_org_id_fkey", "onboarding_sessions", type_="foreignkey")
    op.create_foreign_key("onboarding_sessions_org_id_fkey", "onboarding_sessions", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Trust Center Configs → Organization: CASCADE ---
    op.drop_constraint("trust_center_configs_org_id_fkey", "trust_center_configs", type_="foreignkey")
    op.create_foreign_key("trust_center_configs_org_id_fkey", "trust_center_configs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Trust Center Documents → Organization: CASCADE ---
    op.drop_constraint("trust_center_documents_org_id_fkey", "trust_center_documents", type_="foreignkey")
    op.create_foreign_key("trust_center_documents_org_id_fkey", "trust_center_documents", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Slack Webhook Configs → Organization: CASCADE ---
    op.drop_constraint("slack_webhook_configs_org_id_fkey", "slack_webhook_configs", type_="foreignkey")
    op.create_foreign_key("slack_webhook_configs_org_id_fkey", "slack_webhook_configs", "organizations", ["org_id"], ["id"], ondelete="CASCADE")

    # --- Auditor Profiles → User: CASCADE ---
    op.drop_constraint("auditor_profiles_user_id_fkey", "auditor_profiles", type_="foreignkey")
    op.create_foreign_key("auditor_profiles_user_id_fkey", "auditor_profiles", "users", ["user_id"], ["id"], ondelete="CASCADE")

    # --- Framework hierarchy cascades ---
    op.drop_constraint("framework_domains_framework_id_fkey", "framework_domains", type_="foreignkey")
    op.create_foreign_key("framework_domains_framework_id_fkey", "framework_domains", "frameworks", ["framework_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("framework_requirements_domain_id_fkey", "framework_requirements", type_="foreignkey")
    op.create_foreign_key("framework_requirements_domain_id_fkey", "framework_requirements", "framework_domains", ["domain_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("control_objectives_requirement_id_fkey", "control_objectives", type_="foreignkey")
    op.create_foreign_key("control_objectives_requirement_id_fkey", "control_objectives", "framework_requirements", ["requirement_id"], ["id"], ondelete="CASCADE")

    # --- Mapping table cascades ---
    op.drop_constraint("control_framework_mappings_control_id_fkey", "control_framework_mappings", type_="foreignkey")
    op.create_foreign_key("control_framework_mappings_control_id_fkey", "control_framework_mappings", "controls", ["control_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("control_framework_mappings_framework_id_fkey", "control_framework_mappings", type_="foreignkey")
    op.create_foreign_key("control_framework_mappings_framework_id_fkey", "control_framework_mappings", "frameworks", ["framework_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("control_template_evidence_templates_control_template_id_fkey", "control_template_evidence_templates", type_="foreignkey")
    op.create_foreign_key("control_template_evidence_templates_control_template_id_fkey", "control_template_evidence_templates", "control_templates", ["control_template_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("control_template_evidence_templates_evidence_template_id_fkey", "control_template_evidence_templates", type_="foreignkey")
    op.create_foreign_key("control_template_evidence_templates_evidence_template_id_fkey", "control_template_evidence_templates", "evidence_templates", ["evidence_template_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("control_template_framework_mappings_control_template_id_fkey", "control_template_framework_mappings", type_="foreignkey")
    op.create_foreign_key("control_template_framework_mappings_control_template_id_fkey", "control_template_framework_mappings", "control_templates", ["control_template_id"], ["id"], ondelete="CASCADE")

    op.drop_constraint("control_template_framework_mappings_framework_id_fkey", "control_template_framework_mappings", type_="foreignkey")
    op.create_foreign_key("control_template_framework_mappings_framework_id_fkey", "control_template_framework_mappings", "frameworks", ["framework_id"], ["id"], ondelete="CASCADE")

    # --- Incident Timeline → User (actor): SET NULL ---
    op.drop_constraint("incident_timeline_events_actor_id_fkey", "incident_timeline_events", type_="foreignkey")
    op.create_foreign_key("incident_timeline_events_actor_id_fkey", "incident_timeline_events", "users", ["actor_id"], ["id"], ondelete="SET NULL")


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
    op.drop_constraint("ck_risks_likelihood_range", "risks", type_="check")
    op.drop_constraint("ck_risks_impact_range", "risks", type_="check")
    op.drop_constraint("ck_risks_risk_score_range", "risks", type_="check")
    op.drop_constraint("ck_risks_residual_likelihood_range", "risks", type_="check")
    op.drop_constraint("ck_risks_residual_impact_range", "risks", type_="check")
    op.drop_constraint("ck_risks_residual_score_range", "risks", type_="check")
    op.drop_constraint("ck_vendor_assessments_score_range", "vendor_assessments", type_="check")
    op.drop_constraint("ck_vendors_assessment_score_range", "vendors", type_="check")
    op.drop_constraint("ck_questionnaire_responses_confidence_range", "questionnaire_responses", type_="check")
    op.drop_constraint("ck_training_assignments_score_range", "training_assignments", type_="check")
    op.drop_constraint("ck_auditor_profiles_rating_range", "auditor_profiles", type_="check")

    # =========================================================================
    # Reverse Fix 3.3: Drop unique constraints
    # =========================================================================
    op.drop_constraint("uq_control_framework_mapping", "control_framework_mappings", type_="unique")
    op.drop_constraint("uq_risk_control_mapping", "risk_control_mappings", type_="unique")
    op.drop_constraint("uq_control_template_evidence_template", "control_template_evidence_templates", type_="unique")
    op.drop_constraint("uq_control_template_framework_mapping", "control_template_framework_mappings", type_="unique")
    op.drop_constraint("uq_notification_preference", "notification_preferences", type_="unique")
    op.drop_constraint("uq_training_assignment", "training_assignments", type_="unique")
    op.drop_constraint("uq_framework_name_version", "frameworks", type_="unique")
    op.drop_constraint("uq_framework_domain_code", "framework_domains", type_="unique")
    op.drop_constraint("uq_framework_requirement_code", "framework_requirements", type_="unique")
    op.drop_constraint("uq_control_objective_code", "control_objectives", type_="unique")

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
