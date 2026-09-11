---
meta_description: "ISO 27001 Annex A controls explained: all 93 controls across 4 categories, which ones auditors test most, common failures, and implementation guidance."
target_keyword: "iso 27001 annex a controls"
secondary_keywords: "annex a controls, iso 27001 2022 controls, iso 27001 audit controls, annex a categories"
word_count_target: "1800"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# ISO 27001 Annex A Controls: Which Ones Actually Get Tested in Audits

If you have started preparing for ISO 27001 certification, you have probably opened the standard's Annex A and been confronted with 93 individual controls spread across four categories. The immediate question most teams ask: do we really need to implement all of these?

The short answer is no -- not all 93 controls will apply to every organization. Your Statement of Applicability (SoA) determines which controls are in scope, and your auditor will test every single one you include. Excluding a control without a defensible justification is one of the fastest ways to fail a Stage 2 audit.

This guide covers the full Annex A control set, identifies the ones auditors focus on most, documents common failure patterns, and provides implementation guidance for each critical area.

---

## Understanding the ISO 27001:2022 Annex A Structure

The 2022 revision reorganized Annex A from 14 categories (114 controls) into 4 streamlined categories with 93 controls total, eliminating redundancy and aligning with how modern organizations implement security.

### The 4 Categories

**1. Organizational Controls (37 controls, A.5.1 through A.5.37)**
Governance, policy, roles, and management-level security activities -- including information security policies, segregation of duties, threat intelligence, asset management, access control policy, supplier relationships, and information security reviews.

**2. People Controls (8 controls, A.6.1 through A.6.8)**
The human element: screening, terms of employment, security awareness and training, disciplinary processes, responsibilities after termination, and remote working security.

**3. Physical Controls (14 controls, A.7.1 through A.7.14)**
Physical perimeters, entry controls, facility security, environmental threats, clear desk and screen policies, equipment siting, storage media handling, and cabling security.

**4. Technological Controls (34 controls, A.8.1 through A.8.34)**
Technical implementations: endpoint devices, privileged access, source code security, authentication, malware protection, vulnerability management, configuration management, data deletion, data masking, data leakage prevention, monitoring, secure coding, and cryptography.

---

## Which Controls Auditors Focus on Most

Not all 93 controls receive equal attention. Certain controls consistently attract deeper scrutiny because they represent high-impact areas where failures are most common. Based on patterns across hundreds of audits, these controls receive the most intensive testing.

### Access Control and Identity Management (A.5.15 through A.5.18, A.8.2 through A.8.5)

Auditors examine your access control policy, user provisioning and deprovisioning, privileged access management, and access review frequency. They request evidence of user access reviews, look for orphaned accounts, and verify least privilege enforcement.

**Common failures:**
- No formal access review process or reviews conducted inconsistently
- Shared service accounts without individual accountability
- Privileged access granted without documented justification
- Delayed deprovisioning when employees leave (anything over 24 hours draws attention)
- No MFA on administrative or privileged accounts

**Implementation guidance:**
Implement automated provisioning and deprovisioning tied to your HR system or identity provider. Enforce MFA on all accounts with elevated privileges. Conduct quarterly access reviews with documented sign-off from system owners. Maintain an access control policy that specifies who can approve access to each system category.

### Risk Assessment and Treatment (Clause 6.1, supported by A.5.7)

Auditors treat risk management as the backbone of the entire ISMS. They will examine your risk assessment methodology, your risk register, how you determined risk treatment options, and whether your Statement of Applicability links back to identified risks.

**Common failures:**
- Risk assessments conducted as a one-time exercise rather than a living process
- Risks identified at too high a level (e.g., "cyber attack") without specificity
- No clear link between identified risks and selected Annex A controls
- Risk treatment plans without owners or deadlines
- Failure to reassess risks after significant changes

**Implementation guidance:**
Adopt a risk assessment methodology that specifies criteria for likelihood and impact. Maintain a risk register that ties each risk to specific controls and treatment actions. Assign risk owners. Schedule formal risk reassessments at least annually and trigger ad-hoc reassessments when significant changes occur -- new systems, new business lines, incidents, or infrastructure changes.

### Incident Management (A.5.24 through A.5.28)

Auditors want to see that you have a defined incident response process, that it has been tested, that incidents are classified and recorded, and that you can demonstrate learning from past incidents. They will ask to see your incident log, response procedures, communication templates, and evidence of post-incident reviews.

**Common failures:**
- Incident response plan exists but has never been tested
- No classification scheme for severity levels
- Incidents recorded informally (Slack messages, emails) rather than in a structured log
- No evidence of lessons learned or corrective actions from past incidents
- Notification timelines not defined or not aligned with contractual or regulatory requirements

**Implementation guidance:**
Create an incident response plan with clear phases, roles, escalation paths, and communication templates. Classify incidents by severity with defined response timelines for each level. Conduct at least one tabletop exercise per year and document the results. Maintain a formal incident log with timestamps, actions taken, and post-incident review outcomes.

### Supplier and Third-Party Management (A.5.19 through A.5.23)

Third-party risk is one of the fastest-growing areas of audit focus. Auditors will examine how you assess vendor security posture, what contractual requirements you impose, how you monitor ongoing compliance, and whether you maintain an inventory of suppliers with access to your data or systems.

**Common failures:**
- No formal vendor risk assessment process
- Contracts that lack information security clauses
- No ongoing monitoring of critical vendors after initial assessment
- Inability to produce a complete list of vendors with data access
- Over-reliance on vendor self-attestation without verification

**Implementation guidance:**
Classify vendors by criticality based on the data and systems they access. Require SOC 2 reports or equivalent evidence from critical vendors. Include information security clauses in all vendor contracts. Conduct annual reassessments of critical vendors and maintain a vendor register that tracks assessment dates, findings, and risk ratings.

### Change Management and Secure Development (A.8.25 through A.8.28, A.8.32, A.8.33)

For technology companies, auditors pay close attention to how code changes move through development, testing, and production environments. They examine change management procedures, environment separation, secure coding practices, and testing requirements.

**Common failures:**
- Developers deploying directly to production without peer review
- No separation between development, staging, and production environments
- Security testing (SAST/DAST) not integrated into the CI/CD pipeline
- Change records missing or incomplete
- No rollback procedures documented

**Implementation guidance:**
Implement a CI/CD pipeline that enforces code review, runs automated security scans (SAST at minimum), and requires approval before production deployment. Maintain separate environments with restricted production access. Log all changes with timestamps, approvers, and descriptions. Define and document rollback procedures.

### Business Continuity and Backup (A.5.29, A.5.30, A.8.13, A.8.14)

Auditors verify that you have tested backup and recovery procedures, not just that backups exist. They will check backup schedules, retention policies, encryption of backup data, and evidence that restores have been tested successfully.

**Common failures:**
- Backups configured but never tested for successful restoration
- No documented recovery time objectives (RTO) or recovery point objectives (RPO)
- Backup data stored in the same region or availability zone as production
- Business continuity plan that exists on paper but has never been exercised
- Backup encryption keys not managed separately from the backup data

**Implementation guidance:**
Define RTOs and RPOs for each critical system. Configure automated backups with cross-region or cross-provider storage. Test restore procedures at least quarterly and document the results. Encrypt backup data and manage encryption keys separately. Conduct an annual business continuity exercise.

---

## Controls That Often Get Overlooked

Beyond the high-focus areas, several controls consistently catch organizations off guard because they seem minor but carry audit weight.

**A.5.9 -- Inventory of information and other associated assets.** You need a current, accurate asset inventory. This includes cloud resources, SaaS applications, data repositories, and endpoints. Many companies maintain a partial inventory that omits SaaS tools or data stores.

**A.5.10 -- Acceptable use of information and other associated assets.** An acceptable use policy is required, and it must be communicated to all employees with evidence of acknowledgment.

**A.6.3 -- Information security awareness, education, and training.** Annual security awareness training is the minimum. Auditors want to see completion records for all employees, not just a policy stating training is required.

**A.7.7 -- Clear desk and clear screen.** Even for fully remote organizations, this control applies. Auditors may ask how you enforce screen lock policies on company-managed devices.

**A.8.10 -- Information deletion.** You must demonstrate that data is deleted when it is no longer needed, in accordance with your retention schedule. This is increasingly tested given privacy regulation overlap.

---

## Building Your Statement of Applicability

The Statement of Applicability (SoA) is the single most important document in your ISMS. It lists every Annex A control, states whether it is applicable or not, provides justification for any exclusions, and references the implementation status and evidence location for applicable controls.

**Rules for a defensible SoA:**

1. Every control must be addressed. You cannot simply ignore a control -- you must explicitly state it is not applicable and explain why.
2. Exclusions must be justified based on your risk assessment. "We do not think this is important" is not a valid justification. A valid justification is: "We do not operate physical facilities; all infrastructure is cloud-hosted, therefore physical perimeter controls (A.7.1) are managed by our cloud provider per our shared responsibility model."
3. For applicable controls, reference the specific policy, procedure, or technical implementation that addresses the control.
4. Keep the SoA current. It should be updated whenever controls change, new risks are identified, or the scope of the ISMS shifts.

---

## How QuickTrust Engineers Implement Annex A Controls

Most organizations struggle with Annex A implementation because the standard tells you what to achieve but not how to achieve it in your specific environment. That gap between requirement and implementation is where QuickTrust operates.

QuickTrust's approach to Annex A implementation follows a defined sequence:

**1. Automated gap assessment against all 93 controls.** The QuickTrust platform maps your existing policies, configurations, and evidence against each Annex A control and produces a scored gap report. Controls are rated as fully implemented, partially implemented, or missing.

**2. Risk-based prioritization.** Gaps are prioritized based on audit risk and business impact. High-focus controls (access management, incident response, change management) are addressed first.

**3. Engineering implementation.** QuickTrust's security and DevOps engineers implement controls directly in your environment. This includes configuring IAM policies, deploying monitoring and logging, setting up backup automation, integrating SAST/DAST into CI/CD pipelines, and building evidence collection workflows. Your engineering team's involvement is typically limited to two hours per week for reviews and approvals.

**4. Evidence mapping.** Every implemented control is linked to its evidence source -- whether that is a cloud configuration, a policy document, a training completion record, or a monitoring dashboard. This evidence map becomes the foundation of your audit package.

**5. SoA generation.** QuickTrust generates your Statement of Applicability with control-level references to implementation evidence, exclusion justifications based on your risk assessment, and status tracking for any controls still in progress.

Organizations working with QuickTrust typically move from gap assessment to audit-ready status in 6 to 10 weeks, with a 100% audit pass rate across more than 100 completed audits.

---

## Key Takeaways

ISO 27001 Annex A contains 93 controls, but not all are created equal from an audit perspective. Focus on access control, risk assessment, incident management, supplier risk, change management, and business continuity. Build a defensible SoA with justified exclusions. Ensure every control you claim to implement has current, verifiable evidence.

The organizations that fail audits are rarely the ones with the worst security. They are the ones with the worst documentation. Getting the implementation right is only half the job -- proving it is the other half.
