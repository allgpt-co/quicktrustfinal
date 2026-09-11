---
meta_description: "Master compliance audit evidence checklist mapping 86 evidence items across SOC 2, ISO 27001, HIPAA, and PCI DSS."
target_keyword: "audit evidence checklist, compliance evidence checklist"
secondary_keywords: "soc 2 evidence checklist, iso 27001 evidence list, hipaa audit evidence, compliance audit preparation"
word_count_target: "2000"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# Compliance Audit Evidence Checklist
## SOC 2, ISO 27001, HIPAA, and PCI DSS

**Prepared by QuickTrust | trust.quickintell.com**
*AI-Powered GRC Platform + Expert Engineering Implementation*

---

## How to Use This Checklist

This master evidence checklist maps 86 evidence items across 10 categories to the four most common compliance frameworks — SOC 2 Type II, ISO 27001, HIPAA Security Rule, and PCI DSS v4.0.

**Use this checklist to:**
- Identify what evidence you need to collect before an audit
- Assign ownership of each evidence item to a responsible team member
- Track collection status and identify gaps
- Understand which framework requires each item (so you can prioritize based on your target certification)
- Build your evidence repository in a format auditors expect

**Legend:**
- **SOC 2** = SOC 2 Type I or Type II (AICPA Trust Services Criteria)
- **ISO** = ISO/IEC 27001:2013 Annex A
- **HIPAA** = HIPAA Security Rule (45 CFR Part 164 Subpart C)
- **PCI** = PCI DSS v4.0

**Status codes for tracking:**
- `Collected` — Evidence is gathered, current, and stored in your evidence repository
- `In Progress` — Evidence exists but needs to be organized, updated, or formatted
- `Gap` — Evidence does not exist; must be created or implemented
- `N/A` — Not applicable to your environment (document justification)

**Pro tip:** For SOC 2 Type II audits, evidence must cover the full audit period (typically 6–12 months). Start collecting evidence from day one of your observation period — retroactive evidence collection is the #1 cause of audit delays.

---

## Evidence Category 1: Policies and Procedures

*The policy library is the foundation of every compliance audit. Auditors look for documented, approved, distributed, and annually reviewed policies that match what you actually do.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 1.1 | **Information Security Policy** | Signed, dated policy document; management approval evidence; version history; employee distribution records | Policy management system, email records, HR platform | ✓ | ✓ A.5.1.1 | ✓ §164.308(a)(1) | ✓ 12.1 | | |
| 1.2 | **Acceptable Use Policy** | Signed policy; employee acknowledgment records (dated); version history | Policy management system, HRIS, DocuSign | ✓ | ✓ A.6.2.1 | ✓ §164.308(a)(3) | ✓ 12.1 | | |
| 1.3 | **Access Control Policy** | Signed policy; management approval; review date history; distribution evidence | Policy repository | ✓ CC6.1 | ✓ A.9.1.1 | ✓ §164.312(a) | ✓ 7.1 | | |
| 1.4 | **Incident Response Policy and Plan** | Policy document; IRP document with roles, escalation, notification timelines; test records | Policy system, incident management platform | ✓ CC7.3 | ✓ A.16.1.1 | ✓ §164.308(a)(6) | ✓ 12.10 | | |
| 1.5 | **Change Management Policy** | Policy; documented approval process; change request templates | Policy system, ITSM platform | ✓ CC8.1 | ✓ A.12.1.2 | ✓ §164.308(a)(7) | ✓ 6.5 | | |
| 1.6 | **Data Classification Policy** | Policy; classification tier definitions; employee training on data handling | Policy repository | ✓ | ✓ A.8.2.1 | ✓ §164.308(a)(1) | ✓ 9.1 | | |
| 1.7 | **Encryption Policy** | Policy; approved algorithm standards; key management procedures | Policy system | ✓ CC6.7 | ✓ A.10.1.1 | ✓ §164.312(a)(2)(iv) | ✓ 4.2.1 | | |
| 1.8 | **Vendor Management Policy** | Policy; vendor assessment procedures; BAA/DPA templates; vendor register | Policy system, contract management platform | ✓ CC9.2 | ✓ A.15.1.1 | ✓ §164.308(b) | ✓ 12.8 | | |
| 1.9 | **Password Policy** | Policy; technical controls documentation showing enforcement; password manager deployment | Policy repository, IAM system screenshots | ✓ CC6.1 | ✓ A.9.3.1 | ✓ §164.312(d) | ✓ 8.3 | | |
| 1.10 | **Vulnerability Management Policy** | Policy; scanning schedule; remediation SLA definitions; patch management procedures | Policy system | ✓ CC7.1 | ✓ A.12.6.1 | ✓ §164.308(a)(1) | ✓ 6.3 | | |
| 1.11 | **Business Continuity / Disaster Recovery Policy** | Policy; BCP/DRP documents; RTO/RPO definitions; test results | Policy system, DR documentation | ✓ A1.2 | ✓ A.17.1.1 | ✓ §164.308(a)(7) | ✓ 12.10 | | |
| 1.12 | **Remote Work / BYOD Policy** | Policy; MDM enrollment requirements; VPN usage requirements; employee sign-offs | Policy system, MDM platform | ✓ | ✓ A.6.2.2 | ✓ §164.310(b) | ✓ 12.3 | | |
| 1.13 | **Secure Development (SDLC) Policy** | Policy; secure coding standards; code review requirements; security testing requirements | Policy system | ✓ CC8.1 | ✓ A.14.2.1 | | ✓ 6.2 | | |
| 1.14 | **Physical Security Policy** | Policy; facility security procedures; clean desk policy; visitor management | Policy system | ✓ CC6.4 | ✓ A.11.1.1 | ✓ §164.310 | ✓ 9.1 | | |
| 1.15 | **Logging and Monitoring Policy** | Policy; logging requirements; retention periods; alert procedures | Policy system | ✓ CC7.2 | ✓ A.12.4.1 | ✓ §164.312(b) | ✓ 10.1 | | |

**Category 1 Total:** \_\_\_ / 15 collected

---

## Evidence Category 2: Access Control Evidence

*Auditors verify that access rights are appropriate, approved, regularly reviewed, and promptly revoked. This is the most scrutinized category in SOC 2 and PCI audits.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 2.1 | **User Access List — All Production Systems** | Complete list of all users with access to production systems; role/permission level; date access was granted; last login date | IAM system (AWS IAM, Okta, Azure AD), exported reports | ✓ CC6.2 | ✓ A.9.2.1 | ✓ §164.312(a)(2)(i) | ✓ 7.2 | | |
| 2.2 | **Access Request and Approval Records** | Tickets or records showing access requests were reviewed and approved before provisioning; approver name and date | ITSM (Jira, ServiceNow), email approvals, access management platform | ✓ CC6.2 | ✓ A.9.2.2 | ✓ §164.308(a)(4) | ✓ 7.3 | | |
| 2.3 | **Privileged Account Inventory and Review** | List of all admin/privileged accounts; quarterly review records showing access was verified and unnecessary accounts removed | IAM system; quarterly review sign-off documents | ✓ CC6.3 | ✓ A.9.2.3 | ✓ §164.308(a)(1) | ✓ 8.2 | | |
| 2.4 | **MFA Configuration Evidence** | Screenshots or configuration exports showing MFA is enforced for privileged accounts, remote access, and cloud consoles; MFA enforcement policy | IAM system (Okta, AWS IAM), SSO platform configuration | ✓ CC6.1 | ✓ A.9.4.2 | ✓ §164.312(d) | ✓ 8.4 | | |
| 2.5 | **Access Review Records (Semi-Annual / Quarterly)** | Completed access review sign-offs; evidence of removals or modifications based on review; reviewer name and date | Access review tickets, spreadsheets, GRC platform | ✓ CC6.3 | ✓ A.9.2.5 | ✓ §164.308(a)(3) | ✓ 7.2.5 | | |
| 2.6 | **Offboarding / Termination Access Revocation Records** | List of employee terminations during the audit period; corresponding access revocation evidence with timestamps showing revocation within required timeframe | HR system (BambooHR, Workday), IAM deprovisioning logs, offboarding tickets | ✓ CC6.2 | ✓ A.9.2.6 | ✓ §164.308(a)(3)(ii)(C) | ✓ 8.2.6 | | |
| 2.7 | **Least-Privilege Configuration Evidence** | IAM role definitions showing scope-limited permissions; evidence that broad permissions (AdministratorAccess, FullAccess) are restricted to authorized accounts | AWS IAM or equivalent role configuration exports | ✓ CC6.3 | ✓ A.9.1.2 | ✓ §164.308(a)(4) | ✓ 7.1.2 | | |
| 2.8 | **Shared / Service Account Register** | Inventory of shared accounts and service accounts; documented approval; enhanced logging configuration for shared accounts | IAM system, service account documentation | ✓ CC6.2 | ✓ A.9.2.3 | ✓ §164.312(a)(2)(i) | ✓ 8.2.2 | | |
| 2.9 | **SSO / Identity Provider Configuration** | Evidence of centralized identity management; IDP configuration screenshots; list of systems integrated with SSO | Okta, Azure AD, Google Workspace IDP configuration | ✓ CC6.1 | ✓ A.9.4.1 | ✓ §164.312(d) | ✓ 8.2 | | |
| 2.10 | **Physical Access Control Records** | Badge access logs for server rooms / sensitive areas; access control system configuration; physical access review records | Physical access control system (HID, Avigilon), building management system | ✓ CC6.4 | ✓ A.11.1.2 | ✓ §164.310(a) | ✓ 9.2 | | |

**Category 2 Total:** \_\_\_ / 10 collected

---

## Evidence Category 3: Encryption Evidence

*Auditors verify that ePHI, cardholder data, and other sensitive data is encrypted both at rest and in transit, and that key management practices are sound.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 3.1 | **Encryption-at-Rest Configuration** | Database encryption settings (RDS, MongoDB, etc.); S3 bucket encryption policy; EBS volume encryption; storage encryption screenshots | AWS Console, GCP Console, Azure Portal configuration | ✓ CC6.7 | ✓ A.10.1.1 | ✓ §164.312(a)(2)(iv) | ✓ 3.5 | | |
| 3.2 | **TLS / HTTPS Configuration Evidence** | SSL/TLS configuration for all public-facing endpoints; SSL Labs or equivalent scan showing TLS 1.2+ and strong cipher suites; HSTS header evidence | SSL Labs scan report, load balancer configuration, NGINX/Apache TLS config | ✓ CC6.7 | ✓ A.13.2.3 | ✓ §164.312(e)(2)(ii) | ✓ 4.2.1 | | |
| 3.3 | **TLS Certificate Inventory and Renewal Records** | Inventory of all TLS certificates; expiry dates; renewal process evidence; no expired certificates in production | Certificate management tool (AWS Certificate Manager, Let's Encrypt records), certificate monitoring alerts | ✓ CC6.7 | ✓ A.10.1.2 | | ✓ 4.2.1 | | |
| 3.4 | **Key Management System (KMS) Configuration** | KMS configuration showing encryption keys; access policies restricting key usage; key rotation configuration | AWS KMS, GCP Cloud KMS, or HashiCorp Vault configuration exports | ✓ CC6.7 | ✓ A.10.1.2 | ✓ §164.312(a)(2)(iv) | ✓ 3.7 | | |
| 3.5 | **Key Rotation Evidence** | Records showing encryption keys are rotated per policy; automatic key rotation enabled or manual rotation logs | KMS rotation configuration, key version history | ✓ CC6.7 | ✓ A.10.1.2 | | ✓ 3.7.4 | | |
| 3.6 | **Endpoint Encryption Configuration** | Full-disk encryption status report for all company laptops (BitLocker for Windows, FileVault for macOS); MDM compliance reports | MDM platform (Jamf, InTune, Kandji) encryption compliance report | ✓ CC6.6 | ✓ A.10.1.1 | ✓ §164.310(d)(1) | ✓ 3.5 | | |
| 3.7 | **Secrets Management Configuration** | Evidence that secrets (API keys, DB credentials) are stored in secrets manager, not in code; secrets manager access policies | AWS Secrets Manager, HashiCorp Vault, Doppler configuration; code scanning evidence showing no hardcoded secrets | ✓ CC6.7 | ✓ A.10.1.1 | ✓ §164.312(a)(2)(iv) | ✓ 3.5 | | |
| 3.8 | **Backup Encryption Evidence** | Backup encryption configuration; evidence that backups are encrypted at rest and in transit | Backup solution configuration (AWS Backup, Veeam, Snapshots) | ✓ CC9.1 | ✓ A.12.3.1 | ✓ §164.308(a)(7) | ✓ 3.5 | | |

**Category 3 Total:** \_\_\_ / 8 collected

---

## Evidence Category 4: Monitoring and Logging Evidence

*Auditors look for centralized, tamper-resistant logs with sufficient detail to detect and investigate security incidents, covering the full audit observation period.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 4.1 | **SIEM / Log Aggregation Configuration** | Evidence of centralized log collection; sources configured; retention settings; sample dashboard | Splunk, Datadog, AWS CloudWatch, ELK Stack configuration and dashboards | ✓ CC7.2 | ✓ A.12.4.1 | ✓ §164.312(b) | ✓ 10.3 | | |
| 4.2 | **Log Retention Configuration** | Log retention policy settings confirming minimum 12-month retention; evidence logs are not deletable by application users | SIEM retention settings, S3 lifecycle policies for log archives | ✓ CC7.2 | ✓ A.12.4.1 | ✓ §164.312(b) | ✓ 10.5 | | |
| 4.3 | **Authentication Event Logs** | Sample authentication logs showing successful logins, failed logins, MFA events; evidence logs are being collected and are complete | SIEM, IDP logs (Okta, Azure AD), SSH/VPN logs | ✓ CC7.2 | ✓ A.12.4.1 | ✓ §164.312(b) | ✓ 10.2 | | |
| 4.4 | **Privileged Activity Audit Logs** | Logs of administrative actions on production systems; evidence privilege use is logged; sample of admin activity logs | AWS CloudTrail, GCP Admin Activity logs, database audit logs | ✓ CC6.3 | ✓ A.12.4.3 | ✓ §164.312(b) | ✓ 10.2.1 | | |
| 4.5 | **Security Alert Configuration and Evidence** | Alert rules configured in SIEM/monitoring platform; evidence alerts fire correctly; sample alert notifications | SIEM alert configuration, PagerDuty or alerting platform records | ✓ CC7.2 | ✓ A.12.4.1 | ✓ §164.308(a)(1) | ✓ 10.7 | | |
| 4.6 | **Log Review Records** | Evidence of regular log reviews (weekly/monthly); log review checklist or tickets; dates and reviewer names | Ticketing system, GRC platform, log review sign-offs | ✓ CC7.2 | ✓ A.12.4.1 | ✓ §164.308(a)(1) | ✓ 10.7 | | |
| 4.7 | **File Integrity Monitoring (FIM)** | FIM tool configuration; alerts for unauthorized file changes; coverage of critical system files and configurations | Tripwire, AIDE, AWS Config, cloud-native FIM configuration | ✓ CC7.2 | ✓ A.12.4.2 | | ✓ 10.3.4 | | |
| 4.8 | **Clock Synchronization (NTP) Configuration** | NTP server configuration across all production systems; evidence clocks are synchronized | System NTP configuration, CloudWatch clock sync monitoring | ✓ CC7.1 | ✓ A.12.4.4 | | ✓ 10.6 | | |
| 4.9 | **Network Flow / Traffic Monitoring** | Evidence of network traffic monitoring; VPC flow logs or equivalent; alerts for anomalous traffic | AWS VPC Flow Logs, network monitoring platform | ✓ CC7.1 | ✓ A.12.4.1 | | ✓ 10.3 | | |
| 4.10 | **Uptime / Availability Monitoring** | Monitoring tool configuration; availability SLA reports; incident tickets triggered by downtime | StatusPage, PagerDuty, Datadog, CloudWatch dashboards | ✓ A1.1 | ✓ A.12.1.3 | ✓ §164.308(a)(7) | ✓ 12.4 | | |

**Category 4 Total:** \_\_\_ / 10 collected

---

## Evidence Category 5: Incident Response Evidence

*Auditors verify that your incident response program is active and tested, not just documented on paper. Evidence of real or simulated incident handling is required.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 5.1 | **Incident Response Plan Document** | Current, approved IRP document with roles, escalation paths, classification criteria, and notification timelines | Policy management system | ✓ CC7.3 | ✓ A.16.1.1 | ✓ §164.308(a)(6) | ✓ 12.10 | | |
| 5.2 | **Incident Tabletop Exercise Records** | Documentation of tabletop exercise conducted within the past 12 months; scenario used; participants; outcomes; follow-up actions | GRC platform, meeting notes, exercise report | ✓ CC7.3 | ✓ A.17.1.3 | ✓ §164.308(a)(7)(ii)(D) | ✓ 12.10.6 | | |
| 5.3 | **Incident Log / Incident Register** | Log of all security events and incidents during the audit period; severity, classification, actions taken, resolution date | Ticketing system (Jira, ServiceNow), SIEM incident queue | ✓ CC7.4 | ✓ A.16.1.4 | ✓ §164.308(a)(6)(ii) | ✓ 12.10.2 | | |
| 5.4 | **Post-Incident Review Records** | Post-mortem documents for any significant incidents; root cause analysis; lessons learned; corrective actions implemented | Confluence, Notion, GRC platform, incident tickets | ✓ CC7.5 | ✓ A.16.1.6 | ✓ §164.308(a)(1) | ✓ 12.10.5 | | |
| 5.5 | **Security Event Reporting Channel** | Evidence of published security reporting mechanism (security@company.com or equivalent); records of reports received and triaged | Email logs, ticketing system, security reporting records | ✓ CC7.3 | ✓ A.16.1.2 | ✓ §164.308(a)(6)(i) | ✓ 12.10.1 | | |
| 5.6 | **Breach Notification Procedures** | Documented notification procedures including regulatory timelines (HIPAA 60-day, GDPR 72-hour, state laws); customer notification templates | Policy management system, legal documentation | ✓ CC7.4 | ✓ A.16.1.7 | ✓ §164.410 | ✓ 12.10.4 | | |
| 5.7 | **Incident Response Contact List** | Current contact list for IR team, legal, PR, executives, law enforcement, regulatory bodies; evidence it is maintained and accessible | IRP appendix, GRC platform, secure communication platform | ✓ CC7.3 | ✓ A.16.1.1 | ✓ §164.308(a)(6) | ✓ 12.10.1 | | |
| 5.8 | **Security Incident Escalation Records** | Evidence of incidents escalated to appropriate leadership; approval records for material incident responses | Incident tickets, executive communication records | ✓ CC7.4 | ✓ A.16.1.5 | ✓ §164.308(a)(1) | ✓ 12.10.2 | | |

**Category 5 Total:** \_\_\_ / 8 collected

---

## Evidence Category 6: Vendor Management Evidence

*Third-party risk management is heavily scrutinized, especially in HIPAA (BAA requirements) and SOC 2 (CC9.2). Auditors want to see active oversight, not just a one-time checklist.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 6.1 | **Vendor / Subprocessor Register** | Complete list of all vendors with access to systems or data; tier classification; data types shared; review dates | GRC platform, spreadsheet, vendor management system | ✓ CC9.2 | ✓ A.15.1.1 | ✓ §164.308(b) | ✓ 12.8.1 | | |
| 6.2 | **Business Associate Agreement (BAA) Repository** | Executed BAAs with all vendors who access ePHI; signed and dated; current (not expired) | Contract management platform, legal file storage | | | ✓ §164.308(b) | | | |
| 6.3 | **Data Processing Agreements (DPAs)** | Executed DPAs with all vendors processing personal data of EU residents; current; includes required GDPR clauses | Contract management platform | ✓ CC9.2 | ✓ A.15.1.2 | | | | |
| 6.4 | **Vendor Security Assessments / Questionnaires** | Completed security questionnaires (SIG Lite, CAIQ) or SOC 2 reports reviewed for critical vendors; assessment dates | GRC platform, vendor assessment files | ✓ CC9.2 | ✓ A.15.2.1 | ✓ §164.308(b) | ✓ 12.8.2 | | |
| 6.5 | **Annual Vendor Review Records** | Evidence of annual reassessment of critical vendors; updated assessment dates; action items from reviews | GRC platform, vendor review meeting notes, updated questionnaires | ✓ CC9.2 | ✓ A.15.2.1 | ✓ §164.308(b) | ✓ 12.8.4 | | |
| 6.6 | **Vendor Access Review Records** | Evidence that vendor access is reviewed and limited to what is necessary; termination records for departed vendor personnel | IAM system, vendor access tickets, vendor offboarding records | ✓ CC9.2 | ✓ A.15.2.2 | ✓ §164.308(a)(4) | ✓ 8.2.6 | | |
| 6.7 | **Vendor Offboarding Records** | Evidence of access revocation and data return/destruction for terminated vendor relationships; signed confirmation letters | Offboarding tickets, signed data destruction certificates | ✓ CC9.2 | ✓ A.15.2.2 | ✓ §164.308(b) | ✓ 12.8.5 | | |
| 6.8 | **Critical Vendor SOC 2 Reports / Security Certifications** | Current SOC 2 Type II reports or equivalent (ISO 27001 certificate) for critical vendors; within 12 months | Vendor trust portals, directly requested reports | ✓ CC9.2 | ✓ A.15.2.1 | ✓ §164.308(b) | ✓ 12.8.2 | | |

**Category 6 Total:** \_\_\_ / 8 collected

---

## Evidence Category 7: Training and Awareness Evidence

*Auditors expect to see that security training is ongoing, tracked, and relevant — not just a one-time checkbox at hiring.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 7.1 | **Security Awareness Training Completion Records** | List of all employees; training completion status; completion dates; training platform records; % completion | LMS (KnowBe4, Proofpoint, Curricula), HRIS platform | ✓ CC2.2 | ✓ A.7.2.2 | ✓ §164.308(a)(5) | ✓ 12.6 | | |
| 7.2 | **Security Training Content / Curriculum** | Training modules used; topics covered (phishing, password hygiene, data handling, incident reporting); dates of most recent update | LMS platform; training vendor curriculum | ✓ CC2.2 | ✓ A.7.2.2 | ✓ §164.308(a)(5) | ✓ 12.6.3 | | |
| 7.3 | **Phishing Simulation Results** | Phishing simulation campaign results during audit period; click rates; reporting rates; follow-up training for clickers | KnowBe4, Proofpoint, GoPhish campaign reports | ✓ CC2.2 | ✓ A.7.2.2 | ✓ §164.308(a)(5) | ✓ 12.6 | | |
| 7.4 | **New Employee Security Onboarding Records** | Evidence that security training is completed during onboarding; checklist completion; training acknowledgment dates | HRIS, onboarding checklists, LMS records filtered to new hires | ✓ CC2.2 | ✓ A.7.1.2 | ✓ §164.308(a)(5) | ✓ 12.6.2 | | |
| 7.5 | **Role-Specific Training Records** | Evidence that developers receive secure coding training; IT receives advanced security training; executives receive leadership security briefings | LMS, training certificates, conference attendance records | ✓ CC2.2 | ✓ A.7.2.2 | | ✓ 12.6 | | |
| 7.6 | **Policy Acknowledgment Records** | Signed or e-signed acknowledgment that employees have read and understood key policies (AUP, IRP, Data Classification, Password Policy) | DocuSign, HRIS acknowledgment module, GRC platform | ✓ CC1.4 | ✓ A.7.2.2 | ✓ §164.308(a)(5) | ✓ 12.6.3 | | |

**Category 7 Total:** \_\_\_ / 6 collected

---

## Evidence Category 8: Change Management Evidence

*SOC 2 CC8 and PCI DSS 6.5 require evidence that changes to production systems are authorized, tested, and documented. This is heavily sampled during audits.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 8.1 | **Change Request Tickets (Sample)** | Sample of change tickets during the audit period showing: description, requester, approver, deployment date, test evidence, rollback plan | Jira, ServiceNow, Linear, GitHub Issues | ✓ CC8.1 | ✓ A.12.1.2 | ✓ §164.308(a)(7) | ✓ 6.5 | | |
| 8.2 | **Pull Request / Code Review Records** | Evidence that all code changes went through peer review before merge; PR history in version control; reviewer names | GitHub, GitLab, Bitbucket PR history | ✓ CC8.1 | ✓ A.14.2.2 | | ✓ 6.4 | | |
| 8.3 | **CI/CD Pipeline Configuration** | Evidence of automated testing gates in CI/CD; SAST scan results; deployment automation configuration; branch protection rules | GitHub Actions, CircleCI, Jenkins configuration | ✓ CC8.1 | ✓ A.14.2.8 | | ✓ 6.3 | | |
| 8.4 | **Environment Separation Evidence** | Architecture diagram or configuration evidence showing separate dev/staging/production environments; evidence production access is restricted | Cloud console configuration, IAM environment policies, architecture diagram | ✓ CC8.1 | ✓ A.12.1.4 | ✓ §164.308(a)(7) | ✓ 6.4.1 | | |
| 8.5 | **Emergency Change Records** | Documentation of any emergency changes during the audit period; retrospective approval records; post-change review evidence | Ticketing system emergency change tickets | ✓ CC8.1 | ✓ A.12.1.2 | | ✓ 6.5.2 | | |
| 8.6 | **Change Advisory Board (CAB) Records** | CAB meeting minutes or documented change approval process; evidence changes were reviewed before deployment | Meeting notes, approval records in ticketing system | ✓ CC8.1 | ✓ A.12.1.2 | | ✓ 6.5.1 | | |
| 8.7 | **Deployment Logs / Change Log** | System or deployment logs showing what was deployed, by whom, and when; correlated with approved change tickets | Deployment platform logs (Heroku, AWS CodeDeploy, ArgoCD), release notes | ✓ CC8.1 | ✓ A.12.1.2 | | ✓ 6.5.6 | | |
| 8.8 | **Security Testing in SDLC Evidence** | SAST scan results from audit period; SCA/dependency scanning results; secret scanning evidence; penetration test results | CI/CD pipeline reports, security tool dashboards (Snyk, Semgrep, GitHub Advanced Security) | ✓ CC8.1 | ✓ A.14.2.8 | | ✓ 6.3.2 | | |

**Category 8 Total:** \_\_\_ / 8 collected

---

## Evidence Category 9: Business Continuity Evidence

*Auditors want proof that your BCDR plan actually works — not just that it's documented. Backup restoration tests and DR test records are the most commonly cited gaps.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 9.1 | **Business Continuity Plan (BCP)** | Current, approved BCP document; RTO/RPO definitions; recovery priorities; communication plan; executive approval | Policy management system, GRC platform | ✓ A1.2 | ✓ A.17.1.1 | ✓ §164.308(a)(7) | ✓ 12.10 | | |
| 9.2 | **Disaster Recovery Plan (DRP)** | Current DRP with step-by-step recovery procedures; system architecture for DR; failover procedures | Engineering documentation, GRC platform | ✓ A1.2 | ✓ A.17.1.2 | ✓ §164.308(a)(7)(ii)(B) | ✓ 12.10 | | |
| 9.3 | **Backup Configuration Evidence** | Backup schedule configuration; geographic redundancy settings; retention policy settings; backup monitoring alerts | AWS Backup, backup platform configuration, snapshots schedule | ✓ A1.2 | ✓ A.12.3.1 | ✓ §164.308(a)(7)(ii)(A) | ✓ 12.10.1 | | |
| 9.4 | **Backup Restoration Test Results** | Evidence that backup restoration was tested and successful; restoration dates; tested data volumes; tester name and sign-off | Backup test records, restoration tickets, evidence of successfully restored data | ✓ A1.2 | ✓ A.12.3.1 | ✓ §164.308(a)(7)(ii)(D) | ✓ 12.10.6 | | |
| 9.5 | **DR / Failover Test Results** | Evidence that a DR failover was tested; test date; systems tested; RTO achieved; RPO achieved; gaps identified and remediated | DR test report, failover test tickets, post-test sign-off | ✓ A1.2 | ✓ A.17.1.3 | ✓ §164.308(a)(7)(ii)(D) | ✓ 12.10.6 | | |
| 9.6 | **BCP Tabletop Exercise Records** | BCP tabletop exercise documentation; scenario; participants; outcomes; follow-up actions | Meeting notes, GRC platform, exercise report | ✓ A1.2 | ✓ A.17.1.3 | ✓ §164.308(a)(7)(ii)(D) | ✓ 12.10.6 | | |
| 9.7 | **High-Availability / Redundancy Architecture** | Architecture diagram showing HA configuration; multi-AZ or multi-region setup; load balancer configuration; uptime monitoring evidence | Cloud architecture diagram, AWS/GCP/Azure configuration, monitoring dashboards | ✓ A1.1 | ✓ A.17.2.1 | ✓ §164.308(a)(7) | ✓ 12.4 | | |

**Category 9 Total:** \_\_\_ / 7 collected

---

## Evidence Category 10: Physical Security Evidence

*While cloud-native companies have limited on-premises infrastructure, auditors still verify device security, clean desk compliance, and reliance on cloud provider physical security controls.*

| # | Evidence Item | What to Collect | Where to Find It | SOC 2 | ISO | HIPAA | PCI | Owner | Status |
|---|--------------|----------------|-----------------|-------|-----|-------|-----|-------|--------|
| 10.1 | **Cloud Provider Physical Security Reports** | AWS / GCP / Azure SOC 2 Type II reports or ISO 27001 certificates (verify physical security controls in scope); downloaded from cloud provider trust portals | AWS Artifact, Google Cloud Compliance Reports, Azure Compliance Portal | ✓ CC6.4 | ✓ A.11.1.1 | ✓ §164.310 | ✓ 9.1 | | |
| 10.2 | **Office Physical Access Control Logs** | Badge or keycard access logs for office; evidence of access control system in operation; visitor log records | Access control system (HID, Verkada, Brivo), visitor log platform | ✓ CC6.4 | ✓ A.11.1.2 | ✓ §164.310(a) | ✓ 9.3 | | |
| 10.3 | **Device Inventory and Asset Register** | Complete inventory of company-issued devices (laptops, tablets, phones); serial numbers; assignment to user; encryption status; last audit date | MDM platform asset report, IT asset management system | ✓ CC6.6 | ✓ A.8.1.1 | ✓ §164.310(d) | ✓ 9.7 | | |
| 10.4 | **Device Disposal / Decommission Records** | Records of devices decommissioned during the audit period; secure wipe certificates or certificates of destruction; vendor invoices for secure disposal | IT decommission tickets, NIST 800-88 wipe certificates, vendor destruction certificates | ✓ CC6.5 | ✓ A.11.2.7 | ✓ §164.310(d)(2)(i) | ✓ 9.8 | | |
| 10.5 | **MDM Compliance Report** | MDM platform report showing all enrolled devices, encryption status, OS patch compliance, screen lock configuration | Jamf, InTune, Kandji, Mosyle compliance dashboard | ✓ CC6.6 | ✓ A.11.2.6 | ✓ §164.310(b) | ✓ 9.7 | | |
| 10.6 | **Clean Desk Policy Compliance Evidence** | Spot check records or audit results confirming clean desk compliance; employee acknowledgment of clean desk policy | Physical audit records, HR acknowledgment records, photos (if appropriate) | ✓ CC6.4 | ✓ A.11.2.9 | ✓ §164.310(b) | ✓ 9.4 | | |

**Category 10 Total:** \_\_\_ / 6 collected

---

## Master Evidence Summary

| Category | Total Items | Collected | In Progress | Gap | N/A |
|----------|------------|-----------|-------------|-----|-----|
| 1. Policies and Procedures | 15 | | | | |
| 2. Access Control Evidence | 10 | | | | |
| 3. Encryption Evidence | 8 | | | | |
| 4. Monitoring and Logging Evidence | 10 | | | | |
| 5. Incident Response Evidence | 8 | | | | |
| 6. Vendor Management Evidence | 8 | | | | |
| 7. Training and Awareness Evidence | 6 | | | | |
| 8. Change Management Evidence | 8 | | | | |
| 9. Business Continuity Evidence | 7 | | | | |
| 10. Physical Security Evidence | 6 | | | | |
| **TOTAL** | **86** | | | | |

### Evidence Readiness Score

**(Total Collected + 0.5 × In Progress) / 86 × 100 = \_\_\_\_%**

| Score | Interpretation |
|-------|---------------|
| 90–100% | Audit-ready. Organize your evidence repository and confirm with your auditor. |
| 75–89% | Nearly ready. Close remaining gaps within 2–4 weeks. Prioritize items your target framework requires. |
| 50–74% | In progress. 4–8 weeks of focused evidence collection needed. Assign owners to each gap. |
| < 50% | Significant gaps. Begin evidence collection program immediately. Consider an evidence collection sprint before scheduling your audit. |

---

## Evidence Repository Best Practices

**Organize your evidence using this folder structure:**

```
/Audit-Evidence/
  /01-Policies/
  /02-Access-Control/
  /03-Encryption/
  /04-Monitoring-Logging/
  /05-Incident-Response/
  /06-Vendor-Management/
  /07-Training/
  /08-Change-Management/
  /09-Business-Continuity/
  /10-Physical-Security/
```

**Naming convention for evidence files:**
`[Category]-[Item#]-[Description]-[Date].pdf`

Example: `02-Access-Control-2.3-Privileged-Account-Review-Q1-2026.pdf`

**Key audit-time reminders:**
- Evidence must be current — most auditors require evidence from the past 12 months
- Screenshots must show the date and system name
- Policy documents must show approval date, version, and approver name
- Access review records must show who reviewed, when, and what actions were taken
- Test records must show what was tested, the outcome, and who signed off

---

## Ready to Never Scramble for Evidence Again?

Collecting evidence manually before every audit is exhausting and error-prone. The companies that sail through audits are the ones who collect evidence continuously throughout the year — automatically.

QuickTrust automates evidence collection from your cloud infrastructure, IAM systems, CI/CD pipelines, and security tools — so your audit evidence portal is always current. When your auditor sends their request list, your team clicks export, not scramble.

**What QuickTrust delivers:**
- Automated evidence collection from AWS, GCP, Azure, GitHub, Okta, and more
- Pre-organized evidence repository mapped to SOC 2, ISO 27001, HIPAA, and PCI DSS
- Gap alerts when evidence is missing or expiring
- Auditor-ready evidence packages in days, not weeks
- Engineering team to close the gaps — not just flag them

**100% audit pass rate. Across 100+ audits. For companies just like yours.**

**Book your free evidence gap review:**
[trust.quickintell.com](https://trust.quickintell.com)

---

*QuickTrust is an open-source, AI-powered GRC platform operated by GPT Innovations, Inc. This checklist is provided for informational purposes and does not constitute a formal audit or legal compliance assessment. Framework mappings are provided as general guidance; confirm specific requirements with your auditor.*

---

## Related Reading

- [SOC 2 Report Explained: What It Contains and How to Read It](/blog/soc2-report-explained)
- [The Complete Guide to SOC 2 Compliance](/blog/pillar-soc2-complete-guide)

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Compliance Audit Evidence Checklist: SOC 2, ISO 27001, HIPAA, and PCI DSS",
  "description": "Master compliance audit evidence checklist mapping 86 evidence items across SOC 2, ISO 27001, HIPAA, and PCI DSS. Track collection status, assign ownership, and identify gaps before your audit.",
  "author": {
    "@type": "Organization",
    "name": "QuickTrust",
    "url": "https://trust.quickintell.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "QuickTrust",
    "url": "https://trust.quickintell.com"
  },
  "datePublished": "2026-02-28",
  "dateModified": "2026-02-28"
}
</script>
