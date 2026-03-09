# QuickTrust — Implementation Roadmap

> Generated: 2026-03-06
> Current Status: 103 tests passing, 22 core features built, 150+ API endpoints
> Goal: Production-ready GRC SaaS platform

---

## Phase 1: Foundation (Week 1-2) — UNBLOCKS EVERYTHING ELSE

### 1.1 Task Scheduler (APScheduler)
**Why first:** Unblocks evidence collection, monitoring, reviews, training reminders
**Effort:** 2-3 days

- [ ] Create `backend/app/core/scheduler.py` — APScheduler setup with AsyncIOScheduler
- [ ] Wire scheduler startup/shutdown into `app/main.py` lifespan
- [ ] Create `backend/app/jobs/` directory with job modules:
  - [ ] `evidence_collection_job.py` — Refresh stale evidence on schedule
  - [ ] `monitoring_job.py` — Run monitoring rules (hourly/daily/weekly)
  - [ ] `compliance_score_job.py` — Recalculate org compliance scores
  - [ ] `notification_job.py` — Send pending email/Slack notifications
  - [ ] `stale_evidence_job.py` — Flag evidence older than N days
  - [ ] `policy_review_job.py` — Alert on policies past review date
  - [ ] `training_reminder_job.py` — Remind users of overdue training
- [ ] Add API endpoints: `GET /jobs` (list), `POST /jobs/{id}/trigger` (manual run)
- [ ] Add scheduler config to `.env` (cron expressions)
- [ ] Tests for each job

### 1.2 MinIO Client Integration
**Why:** Evidence files need actual S3-compatible storage, not just URL references
**Effort:** 1 day

- [ ] Create `backend/app/core/storage.py` — MinIO client (aioboto3 or miniopy-async)
- [ ] Wire into evidence upload/download endpoints
- [ ] Wire into report file storage
- [ ] Wire into trust center document storage
- [ ] Update evidence service to store/retrieve from MinIO
- [ ] Tests for upload, download, delete

### 1.3 Questionnaire Agent (Agent #10)
**Why:** Requirements specify 10 agents, only 9 exist
**Effort:** 1-2 days

- [ ] Create `backend/app/agents/questionnaire_agent/`
  - [ ] `state.py` — QuestionnaireState (questions, org context, matched responses)
  - [ ] `nodes.py` — parse_questions, match_knowledge_base, llm_generate_answers, score_confidence
  - [ ] `prompts.py` — LLM prompts for answer generation
  - [ ] `graph.py` — LangGraph workflow
- [ ] Wire into agent runs API
- [ ] Add frontend agent page at `/agents/questionnaire`
- [ ] Tests

---

## Phase 2: Core Security Scanners (Week 3-4) — BIGGEST GAP

### 2.1 Scanner Framework
**Why:** Need a common pattern before adding 10+ tools
**Effort:** 1 day

- [ ] Create `backend/app/scanners/base.py` — BaseScannerCollector abstract class
  - Methods: `install_check()`, `scan()`, `parse_results()`, `map_to_controls()`
- [ ] Create `backend/app/scanners/registry.py` — Scanner registry (like collector registry)
- [ ] Create scanner results normalization schema (tool, findings, severity, control_mapping)
- [ ] Add `POST /api/v1/scanners/run` and `GET /api/v1/scanners/results` endpoints

### 2.2 Trivy (Container Vulnerability Scanning)
**Priority:** HIGH — Required for SOC 2, ISO 27001
**Effort:** 1-2 days

- [ ] Create `backend/app/scanners/trivy.py`
- [ ] Install Trivy in Docker image
- [ ] Parse JSON output → normalize to finding schema
- [ ] Map CVEs to compliance controls (CC7.1 Vulnerability Management)
- [ ] Create evidence records from scan results
- [ ] Frontend page: `/security-scanner/trivy`
- [ ] Tests with mock output

### 2.3 Semgrep (SAST — Static Code Analysis)
**Priority:** HIGH — Required for secure development controls
**Effort:** 1-2 days

- [ ] Create `backend/app/scanners/semgrep.py`
- [ ] Install Semgrep in Docker image
- [ ] Run with OWASP Top 10 ruleset
- [ ] Parse SARIF output → normalize findings
- [ ] Map to controls (CC8.1 Change Management, secure coding)
- [ ] Frontend page: `/security-scanner/semgrep`
- [ ] Tests

### 2.4 Gitleaks (Secret Detection)
**Priority:** HIGH — Critical for preventing credential leaks
**Effort:** 1 day

- [ ] Create `backend/app/scanners/gitleaks.py`
- [ ] Install Gitleaks in Docker image
- [ ] Scan configured repositories
- [ ] Parse JSON output → normalize findings
- [ ] Map to controls (CC6.1 Access Control — no hardcoded secrets)
- [ ] Create alerts for found secrets
- [ ] Tests

### 2.5 Checkov (Infrastructure as Code Scanning)
**Priority:** HIGH — Required for cloud configuration controls
**Effort:** 1-2 days

- [ ] Create `backend/app/scanners/checkov.py`
- [ ] Install Checkov in Docker image
- [ ] Scan Terraform/CloudFormation files
- [ ] Parse JSON output → normalize findings
- [ ] Map to CIS Benchmark controls
- [ ] Tests

### 2.6 OWASP ZAP (DAST — Dynamic App Scanning)
**Priority:** MEDIUM — Required for web app security controls
**Effort:** 2 days

- [ ] Create `backend/app/scanners/owasp_zap.py`
- [ ] Add ZAP as Docker service or CLI tool
- [ ] Implement baseline scan (passive) and full scan (active)
- [ ] Parse XML/JSON output → normalize findings
- [ ] Map to OWASP Top 10 controls
- [ ] Add scope-lock safety (only scan whitelisted URLs)
- [ ] Tests

### 2.7 Nuclei (Template-based Vulnerability Scanner)
**Priority:** MEDIUM
**Effort:** 1-2 days

- [ ] Create `backend/app/scanners/nuclei.py`
- [ ] Install Nuclei + community templates
- [ ] Parse JSON output → normalize findings
- [ ] Map to pen test controls
- [ ] Tests

---

## Phase 3: Integration Hub Expansion (Week 5-6)

### 3.1 Integration Connector Framework Upgrade
**Effort:** 1 day

- [ ] Upgrade `backend/app/collectors/base.py` with:
  - `authenticate()` — Test connection
  - `list_resources()` — Discover available data
  - `collect_evidence()` — Pull specific evidence
  - `test_control()` — Verify a control passes
- [ ] Add credential vault abstraction (env vars → Infisical → Vault)
- [ ] Add integration health check endpoint

### 3.2 Slack Integration (Full)
**Effort:** 1-2 days
- [ ] Create `backend/app/collectors/slack_collector.py`
- [ ] OAuth2 app installation flow
- [ ] Send notifications to channels
- [ ] Collect evidence: channel list, retention settings, DLP config
- [ ] Interactive approvals via Slack (approve/reject controls, policies)

### 3.3 Google Cloud (GCP) Connector
**Effort:** 2 days
- [ ] Create `backend/app/collectors/gcp_collector.py`
- [ ] IAM audit (service accounts, key rotation)
- [ ] Cloud Audit Logs collection
- [ ] Storage encryption verification
- [ ] VPC firewall rules check

### 3.4 Azure Connector
**Effort:** 2 days
- [ ] Create `backend/app/collectors/azure_collector.py`
- [ ] Azure AD users/groups/MFA status
- [ ] Azure Policy compliance
- [ ] Key Vault configuration
- [ ] NSG rules verification

### 3.5 Jira Integration
**Effort:** 1 day
- [ ] Create `backend/app/collectors/jira_collector.py`
- [ ] Sync incidents as Jira tickets
- [ ] Track remediation tasks
- [ ] Collect evidence: change management tickets, approval workflows

### 3.6 PagerDuty/OpsGenie Integration
**Effort:** 1 day
- [ ] Create `backend/app/collectors/pagerduty_collector.py`
- [ ] Alert forwarding for critical findings
- [ ] Incident response integration
- [ ] On-call schedule evidence

### 3.7 Additional Connectors (5 more)
**Effort:** 1 day each
- [ ] GitLab connector (branch protection, pipeline evidence)
- [ ] Microsoft Teams connector (notifications)
- [ ] CrowdStrike connector (endpoint protection evidence)
- [ ] Snyk connector (dependency vulnerability evidence)
- [ ] Datadog/Grafana connector (monitoring evidence)

---

## Phase 4: Feature Completeness (Week 7-9)

### 4.1 Evidence Engine Enhancements
**Effort:** 3 days
- [ ] Evidence versioning (keep history of all collected artifacts)
- [ ] Freshness tracking (alert when evidence > N days old)
- [ ] Evidence packaging by domain (bundle for auditor download)
- [ ] Auto-collection scheduling (per evidence template, configurable cron)
- [ ] Retention management (auto-archive after expiry)

### 4.2 Control Exceptions & Versioning
**Effort:** 2 days
- [ ] Add ControlException model (reason, approved_by, expiry_date, compensating_control)
- [ ] Exception approval workflow (request → review → approve/deny)
- [ ] Control version history (track changes over time)
- [ ] Control dependency graph (which controls depend on others)
- [ ] Exception expiry notifications

### 4.3 Incident Response Playbooks
**Effort:** 2 days
- [ ] Add IncidentPlaybook model (name, steps, severity_trigger, auto_actions)
- [ ] Seed 5 default playbooks (data breach, DDoS, unauthorized access, malware, insider threat)
- [ ] Auto-trigger playbook when incident created
- [ ] MTTD/MTTR metric calculation and trending
- [ ] Breach notification tracker (GDPR 72h clock, HIPAA requirements)

### 4.4 Access Review Automation
**Effort:** 2 days
- [ ] User aggregation from integrated systems (pull users from Okta/Azure AD/GitHub)
- [ ] Over-provisioned access detection (flag accounts with 90+ days no activity)
- [ ] Orphan account detection (accounts in systems but not in HR)
- [ ] Segregation of duties engine (define conflicting role pairs, detect violations)
- [ ] Auto-deprovisioning API (revoke access via integration connectors)

### 4.5 Advanced Audit Management
**Effort:** 2 days
- [ ] Sampling calculator (statistical sampling for auditor)
- [ ] Workpaper templates (per framework, pre-populated by Audit Prep agent)
- [ ] Evidence request system (auditor requests → control owner gets notified)
- [ ] Audit timeline/Gantt visualization
- [ ] In-app messaging between auditor and org

### 4.6 Training Module Content
**Effort:** 2 days
- [ ] Seed 5 built-in courses (Security Awareness, Phishing, Data Handling, Incident Reporting, Password Security)
- [ ] Auto-assignment engine (assign by role on user creation)
- [ ] Overdue training notifications
- [ ] Training evidence generation (completion certificates)
- [ ] Annual recertification scheduling

### 4.7 Policy Enhancements
**Effort:** 1-2 days
- [ ] Version diff view (side-by-side comparison)
- [ ] Multi-level approval chains (owner → legal → CISO)
- [ ] Employee policy portal (browse all published policies, acknowledge)
- [ ] Annual review automation (notify owner when review_date approaches)

---

## Phase 5: Dashboards & Reporting (Week 10)

### 5.1 Specialized Dashboards
**Effort:** 3 days
- [ ] Executive Dashboard (board-level: top risks, compliance score trend, open incidents)
- [ ] Compliance Manager Dashboard (framework progress, evidence gaps, policy status)
- [ ] Control Owner Dashboard (my controls, pending evidence, overdue items)
- [ ] Security Posture Dashboard (scanner results, vulnerability trends, threat map)
- [ ] Audit Readiness Dashboard (weighted score: controls 40% + evidence 30% + policies 20% + risks 10%)

### 5.2 Advanced Reports
**Effort:** 2 days
- [ ] Board report template (executive summary, risk heatmap, compliance scores)
- [ ] Framework detail report (per-framework control status, evidence coverage)
- [ ] Risk register report (full risk inventory with treatment plans)
- [ ] Audit readiness report (readiness score breakdown)
- [ ] Vendor summary report (vendor inventory, risk tiers, assessment results)
- [ ] Compliance trending report (score changes over time)
- [ ] Scheduled report delivery (email weekly/monthly reports)

### 5.3 Visualization Components
**Effort:** 2 days
- [ ] Risk heatmap (interactive 5x5 matrix)
- [ ] Compliance score trending chart (line chart over months)
- [ ] Control status sunburst chart (by framework → domain → status)
- [ ] Evidence freshness timeline
- [ ] Vulnerability trend chart (from scanner results)

---

## Phase 6: SaaS & Production (Week 11-13)

### 6.1 SaaS Billing (Stripe)
**Effort:** 3 days
- [ ] Add pricing tier field to Organization model (free/pro/enterprise)
- [ ] Stripe integration (checkout, webhooks, subscription management)
- [ ] Feature gating by tier (free: 1 framework, pro: 5, enterprise: unlimited)
- [ ] Usage tracking (agents run, integrations, users)
- [ ] Billing portal page in frontend

### 6.2 Webhook System
**Effort:** 2 days
- [ ] Create WebhookEndpoint model (url, events, secret, active)
- [ ] Event emitter service (emit events on key actions)
- [ ] Webhook delivery with retry (3 attempts, exponential backoff)
- [ ] Webhook management UI
- [ ] HMAC signature verification

### 6.3 Real-time Updates (SSE)
**Effort:** 1-2 days
- [ ] Server-Sent Events endpoint for live dashboard updates
- [ ] Push notifications for: agent completion, scan results, alert triggers
- [ ] Frontend EventSource client with auto-reconnect

### 6.4 API Rate Limiting
**Effort:** 1 day
- [ ] Add slowapi/redis-based rate limiting middleware
- [ ] Tier-based limits (free: 100 req/min, pro: 1000, enterprise: unlimited)
- [ ] Rate limit headers in responses

### 6.5 Kubernetes Deployment
**Effort:** 3 days
- [ ] Helm chart with values.yaml for all services
- [ ] Horizontal pod autoscaler configs
- [ ] Persistent volume claims for PostgreSQL/MinIO
- [ ] Ingress configuration (nginx/traefik)
- [ ] Health check probes (liveness, readiness)
- [ ] Secret management (sealed-secrets or external-secrets)

### 6.6 Production Hardening
**Effort:** 2 days
- [ ] Database backup/restore procedures
- [ ] Data export API (GDPR compliance)
- [ ] Account deletion workflow (GDPR right to be forgotten)
- [ ] Audit log retention management
- [ ] Error tracking (Sentry integration)
- [ ] Prometheus metrics for all services
- [ ] Grafana dashboards for monitoring

---

## Phase 7: Advanced Integrations (Week 14-16)

### 7.1 Remaining Security Scanners
- [ ] CloudSploit (cloud config)
- [ ] ScoutSuite (multi-cloud audit)
- [ ] tfsec (Terraform security)
- [ ] KICS (IaC scanning)
- [ ] Grype (SCA)
- [ ] Nikto (web server scanning)
- [ ] Nmap (network scanning — for pen test agent)
- [ ] SQLMap (SQL injection testing — for pen test agent)

### 7.2 Remaining Integrations
- [ ] Google Workspace (user evidence)
- [ ] Okta enhancements (full API coverage)
- [ ] BambooHR/Gusto (HR evidence — onboarding/offboarding)
- [ ] Jamf/Intune (endpoint management evidence)
- [ ] Jenkins/CircleCI (CI/CD pipeline evidence)

### 7.3 Advanced AI Features
- [ ] Redis Pub/Sub for inter-agent messaging
- [ ] Agent collaboration (risk agent triggers remediation agent)
- [ ] Agent memory refresh (pgvector context updates)
- [ ] Custom agent builder (let users define agent workflows)

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| **Phase 1** | Week 1-2 | Task scheduler + MinIO + Agent #10 |
| **Phase 2** | Week 3-4 | 6 security scanners (Trivy, Semgrep, Gitleaks, Checkov, ZAP, Nuclei) |
| **Phase 3** | Week 5-6 | 12 integration connectors (Slack, GCP, Azure, Jira, etc.) |
| **Phase 4** | Week 7-9 | Feature completeness (evidence, incidents, access reviews, training) |
| **Phase 5** | Week 10 | 5 dashboards + advanced reports + visualizations |
| **Phase 6** | Week 11-13 | SaaS billing + webhooks + SSE + K8s + production hardening |
| **Phase 7** | Week 14-16 | Remaining scanners + integrations + advanced AI |

**Total: ~16 weeks (4 months) to full requirements coverage**

---

## Priority Order (If Limited Time)

If you can only do a few things, do them in this order:

1. Task Scheduler (Phase 1.1) — Unblocks 80% of automation
2. Trivy + Semgrep + Gitleaks (Phase 2.2-2.4) — Covers the most common compliance evidence needs
3. Evidence automation (Phase 4.1) — Scheduled collection + freshness tracking
4. Executive Dashboard (Phase 5.1) — Most visible feature for demos/investors
5. Slack integration (Phase 3.2) — Most requested integration for notifications
