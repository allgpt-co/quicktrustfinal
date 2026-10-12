"""Reconcile the application schema with the models shipped at revision 0012.

Revision ID: 0013
Revises: 0012

Older migrations omitted application columns and 28 tables. The seed runner's
create_all() hid the missing tables, but cannot add columns to existing tables.
This frozen snapshot supports both an untouched 0012 database and one on which
seeding already created the missing tables. It never imports application models
or removes legacy columns/tables. Required codes without a legacy equivalent are
labelled legacy-<id>, rather than inventing a compliance requirement identifier.

Downgrade is intentionally refused: pre-existing create_all tables and their data
cannot safely be distinguished from newly migrated objects after the upgrade.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def _json_type():
    return sa.Text().with_variant(postgresql.JSONB(), "postgresql")


_ADDITIONS = {
    'audit_logs': (
        sa.Column('event_type', sa.String(50), nullable=False, server_default='GENERAL'),
        sa.Column('event_category', sa.String(30), nullable=False, server_default='system'),
        sa.Column('severity', sa.String(10), nullable=False, server_default='INFO'),
        sa.Column('actor_email', sa.String(255), nullable=True),
        sa.Column('actor_role', sa.String(50), nullable=True),
        sa.Column('actor_ip', sa.String(45), nullable=True),
        sa.Column('actor_user_agent', sa.Text(), nullable=True),
        sa.Column('outcome', sa.String(20), nullable=False, server_default='success'),
        sa.Column('request_id', sa.String(64), nullable=True),
        sa.Column('session_id', sa.String(255), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    ),
    'control_templates': (
        sa.Column('template_code', sa.String(100), nullable=False),
        sa.Column('test_procedure', sa.Text(), nullable=True),
        sa.Column('automation_level', sa.String(50), nullable=False, server_default='manual'),
        sa.Column('variables', _json_type(), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'evidence_templates': (
        sa.Column('template_code', sa.String(100), nullable=False),
        sa.Column('format', sa.String(50), nullable=True),
        sa.Column('refresh_frequency', sa.String(50), nullable=True),
        sa.Column('retention_period', sa.String(50), nullable=True),
        sa.Column('fields', _json_type(), nullable=True),
        sa.Column('pass_criteria', _json_type(), nullable=True),
        sa.Column('integrations', _json_type(), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'frameworks': (
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('previous_version_id', sa.String(36), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'policy_templates': (
        sa.Column('template_code', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sections', _json_type(), nullable=True),
        sa.Column('variables', _json_type(), nullable=True),
        sa.Column('content_template', sa.Text(), nullable=True),
        sa.Column('required_by_frameworks', _json_type(), nullable=True),
        sa.Column('review_frequency', sa.String(50), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'agent_runs': (
        sa.Column('trigger', sa.String(50), nullable=False, server_default='manual'),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('approval_status', sa.String(50), nullable=False, server_default='auto'),
        sa.Column('approved_by', sa.String(36), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('original_output', _json_type(), nullable=True),
        sa.Column('model_version', sa.String(100), nullable=True),
        sa.Column('prompt_version', sa.String(50), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('cost_usd', sa.Float(), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'audits': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'compliance_snapshots': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('framework_id', sa.String(36), nullable=False),
        sa.Column('snapshot_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('total_controls', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('implemented_controls', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('implementation_percentage', sa.Float(), nullable=False, server_default=sa.text('0.0')),
        sa.Column('evidence_coverage_percentage', sa.Float(), nullable=False, server_default=sa.text('0.0')),
        sa.Column('risk_score_avg', sa.Float(), nullable=True),
        sa.Column('details', _json_type(), nullable=True),
        sa.Column('triggered_by', sa.String(50), nullable=False, server_default='manual'),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'control_template_evidence_templates': (
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('control_template_id', sa.String(36), nullable=False),
        sa.Column('evidence_template_id', sa.String(36), nullable=False),
    ),
    'control_template_framework_mappings': (
        sa.Column('requirement_code', sa.String(50), nullable=False),
    ),
    'drift_baselines': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('resource_id', sa.String(36), nullable=False),
        sa.Column('baseline_hash', sa.String(64), nullable=False),
        sa.Column('baseline_data', _json_type(), nullable=True),
        sa.Column('finding_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'framework_domains': (
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'incident_playbooks': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity_trigger', sa.String(20), nullable=True),
        sa.Column('category_trigger', sa.String(100), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('steps', _json_type(), nullable=True),
        sa.Column('notification_channels', _json_type(), nullable=True),
        sa.Column('compliance_references', _json_type(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'integrations': (
        sa.Column('collection_schedule', sa.String(20), nullable=True),
        sa.Column('schedule_collector_type', sa.String(100), nullable=True),
        sa.Column('schedule_control_id', sa.String(36), nullable=True),
        sa.Column('schedule_enabled', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('next_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_schedule_error', sa.Text(), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'nda_signatures': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('signer_name', sa.String(255), nullable=False),
        sa.Column('signer_email', sa.String(255), nullable=False),
        sa.Column('signer_company', sa.String(255), nullable=True),
        sa.Column('signed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('document_ids_accessed', _json_type(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'onboarding_sessions': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'questionnaires': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'report_schedules': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('report_type', sa.String(100), nullable=False),
        sa.Column('frequency', sa.String(50), nullable=False),
        sa.Column('day_of_week', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('recipients', _json_type(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('last_sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'scim_tokens': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('token_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'sso_configurations': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('provider', sa.String(20), nullable=False, server_default='saml'),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('enforced', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('entity_id', sa.String(500), nullable=True),
        sa.Column('sso_url', sa.String(500), nullable=True),
        sa.Column('certificate', sa.Text(), nullable=True),
        sa.Column('oidc_client_id', sa.String(255), nullable=True),
        sa.Column('oidc_client_secret', sa.String(500), nullable=True),
        sa.Column('oidc_issuer', sa.String(500), nullable=True),
        sa.Column('email_domains', sa.Text(), nullable=True),
        sa.Column('attribute_mapping', _json_type(), nullable=True),
        sa.Column('scim_enabled', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('scim_token_hash', sa.String(255), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'training_courses': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'trust_center_configs': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'trust_center_documents': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'vendors': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'webhook_endpoints': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('url', sa.String(1000), nullable=False),
        sa.Column('secret', sa.String(255), nullable=True),
        sa.Column('events', _json_type(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('last_triggered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failure_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'access_review_campaigns': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'api_keys': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('key_hash', sa.String(128), nullable=False),
        sa.Column('key_prefix', sa.String(8), nullable=False),
        sa.Column('scopes', _json_type(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'approved_responses': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('tags', _json_type(), nullable=True),
        sa.Column('approved_by', sa.String(36), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('use_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'auditor_access_tokens': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'controls': (
        sa.Column('implementation_details', sa.Text(), nullable=True),
        sa.Column('effectiveness', sa.String(50), nullable=True),
        sa.Column('automation_level', sa.String(50), nullable=False, server_default='manual'),
        sa.Column('test_procedure', sa.Text(), nullable=True),
        sa.Column('last_test_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_test_result', sa.String(50), nullable=True),
        sa.Column('agent_run_id', sa.String(36), nullable=True),
        sa.Column('maturity_level', sa.Integer(), nullable=True),
        sa.Column('test_frequency', sa.String(20), nullable=True),
        sa.Column('next_test_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('findings', sa.Text(), nullable=True),
        sa.Column('remediation_plan', sa.Text(), nullable=True),
        sa.Column('remediation_due', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'drift_events': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('baseline_id', sa.String(36), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('resource_id', sa.String(36), nullable=False),
        sa.Column('drift_type', sa.String(30), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False, server_default='medium'),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('previous_value', _json_type(), nullable=True),
        sa.Column('current_value', _json_type(), nullable=True),
        sa.Column('status', sa.String(30), nullable=False, server_default='open'),
        sa.Column('acknowledged_by', sa.String(36), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'framework_requirements': (
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'incidents': (
        sa.Column('contained_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('root_cause', sa.Text(), nullable=True),
        sa.Column('lessons_learned', sa.Text(), nullable=True),
        sa.Column('breach_notification_required', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('breach_notification_deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('breach_notified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('affected_users_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('affected_systems', _json_type(), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'policies': (
        sa.Column('template_id', sa.String(36), nullable=True),
        sa.Column('version', sa.String(50), nullable=False, server_default='1.0'),
        sa.Column('owner_id', sa.String(36), nullable=True),
        sa.Column('next_review_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('framework_ids', _json_type(), nullable=True),
        sa.Column('control_ids', _json_type(), nullable=True),
        sa.Column('agent_run_id', sa.String(36), nullable=True),
        sa.Column('classification', sa.String(20), nullable=False, server_default='CONFIDENTIAL'),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'questionnaire_responses': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'reports': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'risks': (
        sa.Column('acceptance_status', sa.String(20), nullable=True),
        sa.Column('acceptance_requested_by', sa.String(36), nullable=True),
        sa.Column('acceptance_requested_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('acceptance_approved_by', sa.String(36), nullable=True),
        sa.Column('acceptance_approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('acceptance_justification', sa.Text(), nullable=True),
        sa.Column('acceptance_expiry', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'scan_results': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('scanner', sa.String(50), nullable=False),
        sa.Column('scan_type', sa.String(50), nullable=False),
        sa.Column('target', sa.String(500), nullable=False),
        sa.Column('status', sa.String(30), nullable=False, server_default='pending'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('total_findings', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('critical_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('high_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('medium_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('low_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('info_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('raw_output_url', sa.String(1000), nullable=True),
        sa.Column('config', _json_type(), nullable=True),
        sa.Column('triggered_by', sa.String(36), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'training_assignments': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'vendor_assessments': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'webhook_deliveries': (
        sa.Column('webhook_id', sa.String(36), nullable=False),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('payload', _json_type(), nullable=True),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('response_body', sa.Text(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'workflow_executions': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('workflow_type', sa.String(100), nullable=False),
        sa.Column('reference_id', sa.String(36), nullable=True),
        sa.Column('status', sa.String(30), nullable=False, server_default='pending'),
        sa.Column('current_step', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('total_steps', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('step_name', sa.String(255), nullable=True),
        sa.Column('input_data', _json_type(), nullable=True),
        sa.Column('output_data', _json_type(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('max_retries', sa.Integer(), nullable=False, server_default=sa.text('3')),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('triggered_by', sa.String(36), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'access_review_entries': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'approval_chains': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('policy_id', sa.String(36), nullable=False),
        sa.Column('step_order', sa.Integer(), nullable=False),
        sa.Column('approver_role', sa.String(100), nullable=False),
        sa.Column('approver_id', sa.String(36), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'audit_findings': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'collection_jobs': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'control_dependencies': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('control_id', sa.String(36), nullable=False),
        sa.Column('depends_on_id', sa.String(36), nullable=False),
        sa.Column('dependency_type', sa.String(50), nullable=False, server_default='requires'),
        sa.Column('notes', sa.String(500), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'control_exceptions': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('control_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('compensating_control', sa.Text(), nullable=True),
        sa.Column('risk_acceptance', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('requested_by_id', sa.String(36), nullable=True),
        sa.Column('approved_by_id', sa.String(36), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('denied_by_id', sa.String(36), nullable=True),
        sa.Column('denied_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('denial_reason', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'control_objectives': (
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'control_test_definitions': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('control_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('collector_type', sa.String(100), nullable=False),
        sa.Column('assertion_field', sa.String(255), nullable=False),
        sa.Column('assertion_operator', sa.String(20), nullable=False, server_default='eq'),
        sa.Column('assertion_value', sa.String(500), nullable=False),
        sa.Column('schedule', sa.String(20), nullable=False, server_default='daily'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('integration_id', sa.String(36), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'control_versions': (
        sa.Column('control_id', sa.String(36), nullable=False),
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('changed_by', sa.String(36), nullable=True),
        sa.Column('change_reason', sa.String(500), nullable=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('implementation_details', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('effectiveness', sa.String(50), nullable=True),
        sa.Column('test_procedure', sa.Text(), nullable=True),
        sa.Column('changes', _json_type(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'cross_framework_mappings': (
        sa.Column('requirement_a_id', sa.String(36), nullable=False),
        sa.Column('requirement_b_id', sa.String(36), nullable=False),
        sa.Column('mapping_type', sa.String(20), nullable=False),
        sa.Column('notes', sa.String(1000), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'evidence': (
        sa.Column('artifact_url', sa.String(1000), nullable=True),
        sa.Column('data_source', sa.String(20), nullable=False, server_default='live'),
        sa.Column('classification', sa.String(20), nullable=False, server_default='CONFIDENTIAL'),
        sa.Column('collected_by', sa.String(36), nullable=True),
        sa.Column('reviewed_by', sa.String(36), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('approved_by', sa.String(36), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('rejected_by', sa.String(36), nullable=True),
        sa.Column('rejected_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('rejection_reason', sa.String(1000), nullable=True),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'incident_timeline_events': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'monitor_rules': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'playbook_executions': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('playbook_id', sa.String(36), nullable=False),
        sa.Column('incident_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='in_progress'),
        sa.Column('current_step', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('step_statuses', _json_type(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'policy_acknowledgments': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('policy_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('policy_version', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'policy_versions': (
        sa.Column('policy_id', sa.String(36), nullable=False),
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('changed_by', sa.String(36), nullable=True),
        sa.Column('change_summary', sa.String(500), nullable=True),
        sa.Column('status_at_version', sa.String(50), nullable=True),
        sa.Column('changes', _json_type(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'scan_findings': (
        sa.Column('scan_result_id', sa.String(36), nullable=False),
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('scanner', sa.String(50), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('location', sa.String(1000), nullable=True),
        sa.Column('line_number', sa.Integer(), nullable=True),
        sa.Column('rule_id', sa.String(255), nullable=True),
        sa.Column('cve_id', sa.String(255), nullable=True),
        sa.Column('cwe_id', sa.String(500), nullable=True),
        sa.Column('remediation', sa.Text(), nullable=True),
        sa.Column('status', sa.String(30), nullable=False, server_default='open'),
        sa.Column('package_name', sa.String(255), nullable=True),
        sa.Column('package_version', sa.String(100), nullable=True),
        sa.Column('fixed_version', sa.String(100), nullable=True),
        sa.Column('confidence', sa.String(20), nullable=True),
        sa.Column('extra_data', _json_type(), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'control_test_results': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('test_definition_id', sa.String(36), nullable=False),
        sa.Column('control_id', sa.String(36), nullable=False),
        sa.Column('result', sa.String(20), nullable=False),
        sa.Column('actual_value', sa.String(500), nullable=True),
        sa.Column('expected_value', sa.String(500), nullable=False),
        sa.Column('evidence_id', sa.String(36), nullable=True),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('details', _json_type(), nullable=True),
        sa.Column('executed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'evidence_requests': (
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('audit_id', sa.String(36), nullable=True),
        sa.Column('control_id', sa.String(36), nullable=True),
        sa.Column('requested_by', sa.String(36), nullable=False),
        sa.Column('assigned_to', sa.String(36), nullable=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('evidence_id', sa.String(36), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'evidence_versions': (
        sa.Column('evidence_id', sa.String(36), nullable=False),
        sa.Column('org_id', sa.String(36), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('collection_method', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('file_url', sa.String(1000), nullable=True),
        sa.Column('file_hash', sa.String(128), nullable=True),
        sa.Column('change_reason', sa.String(500), nullable=True),
        sa.Column('changes', _json_type(), nullable=True),
        sa.Column('changed_by', sa.String(36), nullable=True),
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
    'monitor_alerts': (
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    ),
}

_NEW_TABLES = ('compliance_snapshots',
 'control_template_evidence_templates',
 'drift_baselines',
 'incident_playbooks',
 'nda_signatures',
 'report_schedules',
 'scim_tokens',
 'sso_configurations',
 'webhook_endpoints',
 'api_keys',
 'approved_responses',
 'drift_events',
 'scan_results',
 'webhook_deliveries',
 'workflow_executions',
 'approval_chains',
 'control_dependencies',
 'control_exceptions',
 'control_test_definitions',
 'control_versions',
 'cross_framework_mappings',
 'playbook_executions',
 'policy_acknowledgments',
 'policy_versions',
 'scan_findings',
 'control_test_results',
 'evidence_requests',
 'evidence_versions')

_FOREIGN_KEYS = (('frameworks', 'previous_version_id', 'frameworks.id', None),
 ('compliance_snapshots', 'org_id', 'organizations.id', None),
 ('compliance_snapshots', 'framework_id', 'frameworks.id', None),
 ('control_template_evidence_templates', 'control_template_id', 'control_templates.id', None),
 ('control_template_evidence_templates', 'evidence_template_id', 'evidence_templates.id', None),
 ('drift_baselines', 'org_id', 'organizations.id', None),
 ('incident_playbooks', 'org_id', 'organizations.id', None),
 ('nda_signatures', 'org_id', 'organizations.id', None),
 ('report_schedules', 'org_id', 'organizations.id', None),
 ('scim_tokens', 'org_id', 'organizations.id', 'CASCADE'),
 ('sso_configurations', 'org_id', 'organizations.id', 'CASCADE'),
 ('webhook_endpoints', 'org_id', 'organizations.id', None),
 ('api_keys', 'org_id', 'organizations.id', None),
 ('api_keys', 'user_id', 'users.id', None),
 ('approved_responses', 'org_id', 'organizations.id', None),
 ('approved_responses', 'approved_by', 'users.id', None),
 ('controls', 'agent_run_id', 'agent_runs.id', None),
 ('drift_events', 'org_id', 'organizations.id', None),
 ('drift_events', 'baseline_id', 'drift_baselines.id', 'CASCADE'),
 ('policies', 'template_id', 'policy_templates.id', None),
 ('policies', 'owner_id', 'users.id', None),
 ('policies', 'agent_run_id', 'agent_runs.id', None),
 ('scan_results', 'org_id', 'organizations.id', None),
 ('scan_results', 'triggered_by', 'users.id', None),
 ('webhook_deliveries', 'webhook_id', 'webhook_endpoints.id', 'CASCADE'),
 ('workflow_executions', 'org_id', 'organizations.id', None),
 ('workflow_executions', 'triggered_by', 'users.id', None),
 ('approval_chains', 'org_id', 'organizations.id', None),
 ('approval_chains', 'policy_id', 'policies.id', None),
 ('approval_chains', 'approver_id', 'users.id', None),
 ('control_dependencies', 'org_id', 'organizations.id', None),
 ('control_dependencies', 'control_id', 'controls.id', 'CASCADE'),
 ('control_dependencies', 'depends_on_id', 'controls.id', 'CASCADE'),
 ('control_exceptions', 'org_id', 'organizations.id', None),
 ('control_exceptions', 'control_id', 'controls.id', None),
 ('control_exceptions', 'requested_by_id', 'users.id', None),
 ('control_exceptions', 'approved_by_id', 'users.id', None),
 ('control_exceptions', 'denied_by_id', 'users.id', None),
 ('control_test_definitions', 'org_id', 'organizations.id', None),
 ('control_test_definitions', 'control_id', 'controls.id', 'CASCADE'),
 ('control_test_definitions', 'integration_id', 'integrations.id', None),
 ('control_versions', 'control_id', 'controls.id', 'CASCADE'),
 ('control_versions', 'org_id', 'organizations.id', None),
 ('control_versions', 'changed_by', 'users.id', None),
 ('cross_framework_mappings', 'requirement_a_id', 'framework_requirements.id', None),
 ('cross_framework_mappings', 'requirement_b_id', 'framework_requirements.id', None),
 ('evidence', 'collected_by', 'users.id', None),
 ('evidence', 'reviewed_by', 'users.id', None),
 ('evidence', 'approved_by', 'users.id', None),
 ('evidence', 'rejected_by', 'users.id', None),
 ('playbook_executions', 'org_id', 'organizations.id', None),
 ('playbook_executions', 'playbook_id', 'incident_playbooks.id', None),
 ('playbook_executions', 'incident_id', 'incidents.id', None),
 ('policy_acknowledgments', 'org_id', 'organizations.id', None),
 ('policy_acknowledgments', 'policy_id', 'policies.id', 'CASCADE'),
 ('policy_versions', 'policy_id', 'policies.id', 'CASCADE'),
 ('policy_versions', 'org_id', 'organizations.id', None),
 ('policy_versions', 'changed_by', 'users.id', None),
 ('scan_findings', 'scan_result_id', 'scan_results.id', 'CASCADE'),
 ('scan_findings', 'org_id', 'organizations.id', None),
 ('control_test_results', 'org_id', 'organizations.id', None),
 ('control_test_results', 'test_definition_id', 'control_test_definitions.id', 'CASCADE'),
 ('control_test_results', 'control_id', 'controls.id', None),
 ('control_test_results', 'evidence_id', 'evidence.id', None),
 ('evidence_requests', 'org_id', 'organizations.id', None),
 ('evidence_requests', 'audit_id', 'audits.id', None),
 ('evidence_requests', 'control_id', 'controls.id', None),
 ('evidence_requests', 'requested_by', 'users.id', None),
 ('evidence_requests', 'assigned_to', 'users.id', None),
 ('evidence_requests', 'evidence_id', 'evidence.id', None),
 ('evidence_versions', 'evidence_id', 'evidence.id', 'CASCADE'),
 ('evidence_versions', 'org_id', 'organizations.id', None),
 ('evidence_versions', 'changed_by', 'users.id', None))

_UNIQUE_COLUMNS = (('control_templates', 'template_code'),
 ('evidence_templates', 'template_code'),
 ('policy_templates', 'template_code'),
 ('scim_tokens', 'token_hash'),
 ('sso_configurations', 'org_id'),
 ('api_keys', 'key_hash'))

_JSON_COLUMNS = (('audit_logs', 'changes'),
 ('organizations', 'cloud_providers'),
 ('organizations', 'tech_stack'),
 ('agent_runs', 'input_data'),
 ('agent_runs', 'output_data'),
 ('integrations', 'config'),
 ('onboarding_sessions', 'input_data'),
 ('onboarding_sessions', 'progress'),
 ('onboarding_sessions', 'results'),
 ('onboarding_sessions', 'agent_run_ids'),
 ('questionnaires', 'questions'),
 ('training_courses', 'required_roles'),
 ('trust_center_configs', 'certifications'),
 ('trust_center_configs', 'branding'),
 ('vendors', 'tags'),
 ('auditor_access_tokens', 'permissions'),
 ('incidents', 'related_control_ids'),
 ('reports', 'parameters'),
 ('vendor_assessments', 'questionnaire_data'),
 ('collection_jobs', 'result_data'),
 ('evidence', 'data'),
 ('monitor_rules', 'config'),
 ('monitor_alerts', 'details'))


# These are the only required additions to pre-existing tables without defaults.
_CODE_COLUMNS = (
    ("control_templates", "template_code"),
    ("evidence_templates", "template_code"),
    ("policy_templates", "template_code"),
    ("framework_domains", "code"),
    ("framework_requirements", "code"),
    ("control_objectives", "code"),
    ("control_template_framework_mappings", "requirement_code"),
)

# Copy rather than rename: keep old data and old consumers intact.
_LEGACY_COPIES = (
    ("framework_domains", "domain_order", "sort_order"),
    ("framework_requirements", "ref_code", "code"),
    ("control_objectives", "ref_code", "code"),
    ("controls", "implementation_notes", "implementation_details"),
    ("policy_templates", "content", "content_template"),
    ("policies", "next_review_at", "next_review_date"),
    ("audit_logs", "created_at", "timestamp"),
    ("audit_logs", "ip_address", "actor_ip"),
)


def _columns(table):
    return {c["name"]: c for c in sa.inspect(op.get_bind()).get_columns(table)}


def _quote(identifier):
    return op.get_bind().dialect.identifier_preparer.quote(identifier)


def upgrade():
    bind = op.get_bind()
    tables = set(sa.inspect(bind).get_table_names())
    added = set()

    for table, definitions in _ADDITIONS.items():
        if table not in tables:
            if table not in _NEW_TABLES:
                raise RuntimeError(f"Expected revision 0012 table is missing: {table}")
            op.create_table(table, *(column._copy() for column in definitions))
            tables.add(table)
            added.update((table, c.name) for c in definitions)
            continue

        existing = _columns(table)
        for definition in definitions:
            if definition.name in existing:
                continue
            column = definition._copy()
            if (table, column.name) in _CODE_COLUMNS:
                column.nullable = True  # backfill before enforcing NOT NULL
            op.add_column(table, column)
            added.add((table, column.name))

    for table, old, new in _LEGACY_COPIES:
        if (table, new) not in added or old not in _columns(table):
            continue
        op.execute(sa.text(
            f"UPDATE {_quote(table)} SET {_quote(new)} = {_quote(old)} "
            f"WHERE {_quote(old)} IS NOT NULL"
        ))

    # Old mappings referenced requirement IDs; preserve their known codes.
    mapping = "control_template_framework_mappings"
    if (mapping, "requirement_code") in added and "requirement_id" in _columns(mapping):
        op.execute(sa.text(
            "UPDATE control_template_framework_mappings SET requirement_code = "
            "(SELECT code FROM framework_requirements "
            "WHERE framework_requirements.id = control_template_framework_mappings.requirement_id) "
            "WHERE requirement_code IS NULL"
        ))

    for table, name in _CODE_COLUMNS:
        if (table, name) not in added:
            continue
        op.execute(sa.text(
            f"UPDATE {_quote(table)} SET {_quote(name)} = 'legacy-' || CAST(id AS VARCHAR) "
            f"WHERE {_quote(name)} IS NULL"
        ))
        with op.batch_alter_table(table) as batch:
            batch.alter_column(name, existing_type=_columns(table)[name]["type"], nullable=False)

    # Do not label historical audit events as successful when outcome was never recorded.
    if ("audit_logs", "outcome") in added:
        op.execute(sa.text("UPDATE audit_logs SET outcome = 'unknown'"))

    # All referenced tables now exist. Add only absent FK signatures so schemas
    # created by the seed runner retain their existing constraints unchanged.
    for table, column, target, ondelete in _FOREIGN_KEYS:
        target_table, target_column = target.split(".")
        existing = sa.inspect(bind).get_foreign_keys(table)
        if any(fk["constrained_columns"] == [column]
               and fk["referred_table"] == target_table
               and fk["referred_columns"] == [target_column] for fk in existing):
            continue
        with op.batch_alter_table(table) as batch:
            batch.create_foreign_key(
                f"fk_{table}_{column}", target_table, [column], [target_column], ondelete=ondelete
            )

    for table, column in _UNIQUE_COLUMNS:
        existing = sa.inspect(bind).get_unique_constraints(table)
        if any(constraint["column_names"] == [column] for constraint in existing):
            continue
        with op.batch_alter_table(table) as batch:
            batch.create_unique_constraint(f"uq_{table}_{column}", [column])

    # Historical migrations stored JSON as TEXT. JSONType binds JSONB on
    # PostgreSQL. Cast valid existing JSON transactionally; invalid legacy JSON
    # fails the migration instead of silently replacing or discarding data.
    if bind.dialect.name == "postgresql":
        for table, name in _JSON_COLUMNS:
            current_type = _columns(table)[name]["type"]
            if isinstance(current_type, sa.Text):
                op.alter_column(
                    table, name, existing_type=current_type, type_=postgresql.JSONB(),
                    postgresql_using=f"{_quote(name)}::jsonb",
                )


def downgrade():
    raise RuntimeError(
        "0013 is a forward-only schema reconciliation. Restore a pre-upgrade "
        "backup to roll back; dropping columns or tables could destroy data "
        "that existed before this migration."
    )
