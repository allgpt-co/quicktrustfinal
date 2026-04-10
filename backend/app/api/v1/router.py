from fastapi import APIRouter

from app.api.v1 import (
    auth,
    organizations,
    users,
    frameworks,
    control_templates,
    evidence_templates,
    controls,
    evidence,
    agent_runs,
    policies,
    policy_templates,
    risks,
    integrations,
    audits,
    auditor_portal,
    onboarding,
    incidents,
    vendors,
    training,
    access_reviews,
    monitoring,
    questionnaires,
    trust_center,
    reports,
    files,
    notifications,
    audit_logs,
    auditor_marketplace,
    gap_analysis,
    tenants,
    embeddings,
    prowler,
    cross_framework_mappings,
    compliance_snapshots,
    privacy,
    invitations,
    profile,
    scanners,
    control_exceptions,
    playbooks,
    policy_acknowledgments,
    dashboards,
    drift,
    control_tests,
    workflows,
    sso,
    scim,
    backups,
    control_versions,
    policy_versions,
    scan_orchestration,
    webhooks,
    api_keys,
    sse,
    agent_memory,
    findings,
    credential_rotation,
    evidence_requests,
    response_library,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(users.router)
api_router.include_router(frameworks.router)
api_router.include_router(control_templates.router)
api_router.include_router(evidence_templates.router)
api_router.include_router(controls.router)
api_router.include_router(evidence.router)
api_router.include_router(agent_runs.router)
api_router.include_router(policies.router)
api_router.include_router(policy_templates.router)
api_router.include_router(risks.router)
api_router.include_router(integrations.router)
api_router.include_router(audits.router)
api_router.include_router(audits.utility_router)
api_router.include_router(auditor_portal.router)
api_router.include_router(onboarding.router)
api_router.include_router(incidents.router)
api_router.include_router(vendors.router)
api_router.include_router(training.router)
api_router.include_router(access_reviews.router)
api_router.include_router(monitoring.router)
api_router.include_router(questionnaires.router)
api_router.include_router(trust_center.router)
api_router.include_router(reports.router)
api_router.include_router(files.router)
api_router.include_router(trust_center.public_router)
# v0.5 additions
api_router.include_router(notifications.router)
api_router.include_router(audit_logs.router)
api_router.include_router(auditor_marketplace.router)
api_router.include_router(gap_analysis.router)
api_router.include_router(tenants.router)
api_router.include_router(embeddings.router)
api_router.include_router(prowler.router)
api_router.include_router(cross_framework_mappings.router)
api_router.include_router(compliance_snapshots.router)
api_router.include_router(privacy.router)
api_router.include_router(invitations.router)
api_router.include_router(profile.router)
api_router.include_router(scanners.router)
# Phase 4 additions
api_router.include_router(control_exceptions.router)
api_router.include_router(playbooks.router)
api_router.include_router(policy_acknowledgments.router)
# Phase 5 additions
api_router.include_router(dashboards.router)
# P0 Group 1: Workflow & Automation
api_router.include_router(drift.router)
api_router.include_router(control_tests.router)
api_router.include_router(workflows.router)
# Phase 4: Enterprise SSO & SCIM
api_router.include_router(sso.router)
api_router.include_router(scim.router)
# Phase 7: Infrastructure & DR
api_router.include_router(backups.router)
# Priority 2: Versioning, Dependencies, Bulk Ops, Scanner Orchestration
api_router.include_router(control_versions.router)
api_router.include_router(policy_versions.router)
api_router.include_router(scan_orchestration.router)
# Webhooks, API Keys, SSE, Agent Memory, Findings, Credential Rotation
api_router.include_router(webhooks.router)
api_router.include_router(api_keys.router)
api_router.include_router(sse.router)
api_router.include_router(agent_memory.router)
api_router.include_router(findings.router)
api_router.include_router(credential_rotation.router)
# Priority 3: Evidence Request System
api_router.include_router(evidence_requests.router)
# Priority 3: Approved Response Library
api_router.include_router(response_library.router)
