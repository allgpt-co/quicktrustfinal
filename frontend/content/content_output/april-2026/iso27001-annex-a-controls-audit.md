---
meta_description: "Which ISO 27001 Annex A controls actually get tested during audits? A practical guide from audit veterans covering the controls auditors focus on most."
target_keyword: "iso 27001 annex a controls, iso 27001 certification, iso audit"
secondary_keywords: "iso 27001 2022, annex a controls, iso 27001 implementation"
word_count_target: "2500"
last_updated: "2026-02-28"
---

# ISO 27001 Annex A Controls: Which Ones Actually Get Tested in Audits

There are 93 controls in ISO 27001:2022 Annex A. Your auditor is not going to test all 93 with equal depth. That is not how ISO audits work, and if you prepare as though every control will receive identical scrutiny, you will waste engineering time on low-risk controls while leaving gaps in the ones that actually generate nonconformities.

This is a problem because most ISO 27001 implementation guides treat all controls as equally important. They list all 93, provide generic descriptions, and leave you to figure out where to focus your limited engineering capacity. That approach works for passing a knowledge exam. It does not work for passing a certification audit.

This guide is built from direct experience across 100+ ISO 27001 audits. It explains exactly which Annex A controls auditors focus on during Stage 2 certification audits, what evidence they expect to see, and where companies actually fail. If you are a CTO or CISO at a SaaS company preparing for ISO 27001 certification, this is the prioritization framework you need.

For a complete overview of the ISO 27001 standard, mandatory clauses, and implementation roadmap, see our [ISO 27001 Complete Implementation Guide](/iso-27001-certification-guide).

---

## How ISO Auditors Decide What to Test

Before we get into specific controls, you need to understand the auditor's methodology. ISO 27001 certification auditors do not follow a fixed checklist. Their audit plan is shaped by three factors:

**1. Your Statement of Applicability (SoA).** The SoA is the primary reference document. Every control you declare as "applicable and implemented" in your SoA is a candidate for testing. Controls you exclude with proper justification generally are not tested — but the justification itself is scrutinized.

**2. Risk-based sampling.** Auditors use risk-based sampling to select which controls receive deep-dive testing. They focus on controls relevant to your organization's risk profile, scope, and industry. A cloud-native SaaS company processing financial data will receive different emphasis than a manufacturing firm with on-premises infrastructure.

**3. Audit trail and evidence patterns.** Experienced auditors develop intuition about where gaps exist. If your documentation is strong but your technical evidence is thin, they will dig harder into technical controls. If your policies look template-generated, they will verify whether the policies describe controls that actually exist in your environment.

The practical implication: auditors typically perform deep-dive testing on 20-30 controls, conduct surface-level verification on another 20-30, and review the remaining controls through documentation and interview only. The controls that receive deep-dive testing are not random.

---

## The 15 Annex A Controls That Auditors Test Most Aggressively

Based on patterns across hundreds of certification audits, these are the controls that receive the highest scrutiny during Stage 2. If you only have capacity to prepare bulletproof evidence for a subset of controls, start here.

### 1. A.5.15 — Access Control

**Why auditors focus here:** Access control failures represent some of the highest-impact security risks. Auditors know this. They will request your access control policy, but more importantly, they will ask to see your actual IAM configuration.

**What auditors actually ask for:**
- Access control policy with defined roles and access levels
- Evidence that access is granted based on least privilege and business need
- IAM configuration screenshots or exports from your cloud provider (AWS IAM, GCP IAM, Azure AD)
- Evidence of periodic access reviews (quarterly is the standard expectation)
- Process for revoking access when employees leave or change roles

**Where companies fail:** Having a policy that describes role-based access control while the actual AWS environment has 14 IAM users with AdministratorAccess. Auditors will ask to see the IAM console. The delta between your policy and reality is a major nonconformity.

### 2. A.8.2 — Privileged Access Rights

**Why auditors focus here:** This is the specific control for privileged and administrative access. Auditors treat it as distinct from general access control because privileged access misuse is the single largest vector for data breaches.

**What auditors actually ask for:**
- Inventory of privileged accounts and what systems they access
- Justification for each privileged access grant
- MFA enforcement on all privileged accounts (this is non-negotiable)
- Logging of all privileged access activity
- Time-limited or just-in-time privileged access where possible

**Where companies fail:** Shared root credentials for cloud accounts. Developers with production database admin access that was granted 18 months ago for a one-time migration and never revoked. Break-glass accounts with no monitoring.

### 3. A.8.15 — Logging

**Why auditors focus here:** Without logging, you cannot demonstrate that any other control is operating effectively. Auditors use logging evidence as a meta-verification of your entire control environment.

**What auditors actually ask for:**
- Centralized log aggregation from all in-scope systems
- Log retention periods that meet your documented policy (typically 12 months minimum)
- Evidence that logs are tamper-protected (immutable storage, write-once configuration)
- Demonstrated ability to search and retrieve logs for specific events
- CloudTrail, Cloud Audit Logs, or equivalent enabled across all accounts and regions

**Where companies fail:** Logging is "enabled" but not centralized — meaning logs exist in 12 different systems with no single pane of glass. Log retention is set to 30 days in CloudWatch, which is insufficient. No one has ever actually queried the logs to investigate an event.

### 4. A.8.16 — Monitoring Activities

**Why auditors focus here:** This control was new in ISO 27001:2022, and auditors give new controls extra attention. Monitoring goes beyond logging — it requires active alerting on security-relevant events.

**What auditors actually ask for:**
- Security monitoring and alerting configuration (SIEM, AWS Security Hub, GCP Security Command Center, Datadog Security Monitoring)
- Alert rules for critical events: unauthorized access attempts, privilege escalation, configuration changes to security controls
- Evidence that alerts are reviewed and actioned (not just generated)
- On-call or response procedures for security alerts

**Where companies fail:** Having a SIEM that collects logs but has no alert rules configured. Or having 500 alert rules that generate so much noise that no one reviews them. Auditors ask: "Show me the last 5 security alerts your team responded to." If no one can answer that question, you have a nonconformity.

### 5. A.5.1 — Policies for Information Security

**Why auditors focus here:** This is the root control. Your entire ISMS is built on your information security policy, and the auditor uses it as a map for the rest of the audit.

**What auditors actually ask for:**
- Approved information security policy signed by top management
- Evidence the policy was communicated to all employees
- Evidence the policy was reviewed at planned intervals (at least annually)
- Alignment between what the policy says and what the rest of the ISMS actually does

**Where companies fail:** The policy was written 8 months ago, never reviewed, and describes controls that have since changed. Or the policy is a 40-page document that no employee has ever read — and the auditor asks three random employees what the information security policy says and gets blank stares.

### 6. A.6.3 — Information Security Awareness, Education and Training

**Why auditors focus here:** This is an easy control to verify and a frequent source of nonconformities. Auditors love testing it because the evidence is binary: either you trained your people or you did not.

**What auditors actually ask for:**
- Security awareness training program with documented content
- Training completion records for all employees in scope
- Evidence that training is conducted upon onboarding and at regular intervals (annually minimum)
- Phishing simulation results (not strictly required but increasingly expected)
- Role-specific training for developers, administrators, and security personnel

**Where companies fail:** "We plan to start training next quarter." That is not evidence. Or training records showing 62% completion — meaning 38% of your staff received no security training. Auditors expect 100% completion for all in-scope employees.

### 7. A.8.8 — Management of Technical Vulnerabilities

**Why auditors focus here:** Vulnerability management is directly observable. Auditors can ask to see your vulnerability scan results and immediately assess your risk posture.

**What auditors actually ask for:**
- Vulnerability scanning tool and scan schedule (weekly minimum for production environments)
- Recent scan results showing identified vulnerabilities
- Remediation SLAs: critical vulnerabilities within 72 hours, high within 30 days
- Evidence that vulnerabilities are actually being remediated (not just scanned and ignored)
- Patch management process for operating systems, libraries, and dependencies

**Where companies fail:** Running a vulnerability scan that shows 200+ high-severity findings with no remediation timeline. Or having a documented patching policy that says "critical patches within 72 hours" while the scan results show critical CVEs that have been open for 6 months.

### 8. A.8.24 — Use of Cryptography

**Why auditors focus here:** Encryption is a fundamental technical control, and the evidence is concrete and verifiable.

**What auditors actually ask for:**
- Encryption of data at rest (AES-256 or equivalent) with key management procedures
- Encryption of data in transit (TLS 1.2 minimum, TLS 1.3 preferred)
- Certificate management process (who manages certificates, how renewals are tracked)
- Key management: who has access to encryption keys, rotation schedule, key storage
- Cryptographic policy defining approved algorithms and key lengths

**Where companies fail:** Data is encrypted in transit and at rest, but no one can explain the key management process. Encryption keys stored in plaintext in environment variables. TLS certificates that expired last month because no one owns the renewal process.

### 9. A.5.24 — Information Security Incident Management Planning and Preparation

**Why auditors focus here:** Incident response is a test of your ISMS maturity. Every auditor asks about it because a company that has no incident response plan has not thought seriously about what happens when controls fail.

**What auditors actually ask for:**
- Documented incident response plan with clear roles, escalation paths, and communication procedures
- Incident classification criteria (what constitutes a security event vs. a security incident)
- Evidence that the plan has been tested (tabletop exercise, simulation, or actual incident response)
- Incident log or register showing past incidents and how they were handled

**Where companies fail:** Having an incident response plan that no one has ever rehearsed. The auditor asks "When was the last time this plan was tested?" and the answer is never. Also: having experienced actual incidents but not documenting them — which means you cannot demonstrate learning from incidents (A.5.27).

### 10. A.5.9 — Inventory of Information and Other Associated Assets

**Why auditors focus here:** Your asset inventory drives your risk assessment. Without a complete inventory, your risk register is incomplete, and your control implementation cannot be comprehensive.

**What auditors actually ask for:**
- Asset inventory covering information assets, hardware, software, cloud services, and data stores
- Asset ownership assigned for every asset
- Classification of assets based on sensitivity
- Regular review and update process for the inventory

**Where companies fail:** An asset inventory created during implementation that has not been updated since. Missing cloud services that were provisioned after the inventory was created. No assigned owners for 30% of listed assets.

---

## The Next 10: Controls That Get Moderate Scrutiny

These controls receive solid attention during most audits but rarely receive the same deep-dive treatment as the top 15 — unless your organization's risk profile makes them particularly relevant.

### 11. A.8.25 — Secure Development Life Cycle

Auditors verify that security is integrated into your development process. They ask for SDLC documentation, evidence of security testing in CI/CD pipelines, code review processes, and separation of development/test/production environments. For SaaS companies, this is often elevated to the "heavily tested" category.

### 12. A.5.19 and A.5.20 — Supplier Relationships and Supplier Agreements

Auditors review your third-party risk management program. They expect a supplier register, security assessment procedures for critical vendors, contractual security requirements, and ongoing monitoring. If you rely heavily on third-party services (which most SaaS companies do), expect thorough testing here.

### 13. A.8.9 — Configuration Management (New in 2022)

As a new control in the 2022 revision, auditors test this to ensure organizations have addressed it. They look for documented configuration baselines, change management procedures, and evidence that production configurations are controlled and reviewed.

### 14. A.5.29 — Information Security During Disruption

Auditors verify your business continuity planning. They expect documented BCP/DR procedures, defined RTOs and RPOs, and evidence that recovery procedures have been tested. Asking "when did you last test your backup restoration?" is a standard audit question.

### 15. A.8.32 — Change Management

Change management is foundational to operational stability. Auditors look for a documented change management process, change approval records, and evidence that changes to production systems follow the process. This is where informal "deploy from laptop" practices create audit problems.

### 16. A.5.3 — Segregation of Duties

Auditors test whether critical functions are separated — for example, whether the same person can write code, approve it, and deploy it to production. This is especially relevant for small teams where one person may wear multiple hats.

### 17. A.8.13 — Information Backup

Auditors verify that backup procedures exist, are automated, and — critically — that restore procedures have been tested. Having backups is not sufficient. You must demonstrate that you can restore from them within your stated RTO.

### 18. A.5.34 — Privacy and Protection of PII

If you process personal data, auditors will test your PII protection controls thoroughly. Expect questions about data classification, data processing agreements, retention periods, and data subject rights procedures.

### 19. A.5.17 — Authentication Information

This covers password policies, credential management, and multi-factor authentication. Auditors test whether your password policy is enforced technically (not just documented) and whether MFA is deployed across all critical systems.

### 20. A.8.7 — Protection Against Malware

Auditors expect endpoint protection on all user devices in scope. For cloud-native companies, this extends to container security scanning and runtime protection in production environments.

---

## Controls That Auditors Rarely Deep-Dive (But You Still Must Address)

The following controls are typically verified through documentation review and brief interview only. They are part of your SoA and your auditor will confirm they are addressed, but they are unlikely to be the subject of extensive evidence sampling.

**Physical controls (7.1 through 7.14):** For cloud-native SaaS companies, most physical controls are scoped to your cloud provider's responsibility under the shared responsibility model. Your auditor will verify that you have documented this correctly and have evidence of your cloud provider's ISO 27001 certification. If you operate in a co-working space, expect a brief review of office security — but it will not be the focus of your audit.

**A.5.5 — Contact with authorities:** You document which authorities to contact in different scenarios (data breach to ICO/DPA, law enforcement, etc.). Auditors verify the documentation exists and is current. That is usually sufficient.

**A.5.6 — Contact with special interest groups:** Membership in relevant security communities or information sharing groups. A brief check.

**A.5.32 — Intellectual property rights:** Auditors verify you have a process for ensuring software licensing compliance and IP protection. For SaaS companies, this usually involves license management and open-source license compliance.

**A.7.7 — Clear desk and clear screen:** If applicable to your environment, auditors may do a brief walk-through. For remote-first companies, this is often addressed through policy and endpoint management.

This does not mean you can ignore these controls. Your SoA must address every applicable control with evidence of implementation. But your preparation effort should be proportional to audit risk — and these controls carry lower audit risk than the ones listed above.

---

## The 5 Most Common Nonconformities We See in ISO Audits

After supporting over 100 ISO 27001 audits with a 100% pass rate, we have documented the failure patterns that trip up organizations. These are the nonconformities we see repeatedly during Stage 2 audits — the ones QuickTrust specifically engineers controls to prevent.

### 1. Policy-Reality Gap

The number one audit killer. Your policies describe controls that do not match your actual implementation. Your access control policy says "least privilege is enforced and access is reviewed quarterly," but you have never conducted an access review. Your incident response plan says "the Security Operations Center monitors all critical systems," but you do not have an SOC.

**How to prevent it:** Every policy must describe what you actually do — not what you aspire to do. At QuickTrust, our engineers implement the control first, then document the policy to match the implementation. Not the other way around.

### 2. Missing or Incomplete Risk Assessment

The risk assessment is a mandatory clause requirement (Clause 6), and it is the foundation of your control selection. Auditors who find a superficial risk assessment will question the entire basis of your ISMS.

**What "superficial" looks like:** A risk register with 15 generic risks copied from a template (e.g., "unauthorized access," "data breach," "natural disaster") with no connection to your actual assets, systems, or threat landscape. No risk owner assigned. No residual risk calculation after controls are applied.

**What auditors expect:** A risk register with specific risks tied to specific assets, realistic likelihood and impact assessments, documented treatment decisions (mitigate, accept, transfer, avoid), and control mappings for each treated risk.

### 3. No Evidence of Management Review

Clause 9.3 requires management reviews at planned intervals. The auditor asks for meeting minutes or records from your last management review. You produce nothing — because the review never happened, or it happened informally without documentation.

**What a proper management review includes:** Review of ISMS performance metrics, internal audit results, nonconformity trends, risk assessment updates, and improvement opportunities. Documented decisions and actions from management. This does not need to be a formal board meeting — it can be a structured 60-minute review with your leadership team. But it must be documented.

### 4. Internal Audit Not Conducted or Not Independent

Clause 9.2 requires internal audits. The auditor asks for your internal audit report. If it does not exist, that is a major nonconformity. If the "internal auditor" is the same person who built the ISMS, the auditor will question independence.

**How to handle this:** The internal auditor must not audit their own work. For small companies, this means either engaging a qualified external party for the internal audit or having a trained employee from a different department conduct it. QuickTrust includes an independent internal audit as part of every certification program.

### 5. Logging and Monitoring Without Review

You have CloudTrail enabled. You have centralized logging. But when the auditor asks "Can you show me a security event that was detected through your monitoring system and how your team responded?", nobody can produce an example. Logging without review is a control that exists on paper but provides no security value — and auditors recognize the pattern immediately.

---

## Building an Audit-Ready Evidence Package

Preparing for an ISO audit is fundamentally an evidence management exercise. Auditors evaluate your ISMS based on the evidence you can produce — not the controls you claim to have. Here is the evidence framework we use across every QuickTrust ISO 27001 engagement.

### Evidence Categories

**Policy evidence:** Approved, version-controlled documents with review history. Every policy should show who approved it, when it was last reviewed, and when the next review is scheduled.

**Process evidence:** Records demonstrating that processes operate as documented. Access review records, change management tickets, incident logs, training completion records, vulnerability remediation records.

**Technical evidence:** Configuration screenshots, system exports, scan reports, log samples. These should be timestamped and tied to the specific control they support.

**Management evidence:** Management review minutes, internal audit reports, corrective action records, resource allocation decisions.

### Evidence Organization Best Practice

Organize evidence by Annex A control number. Each control should have a folder (physical or virtual) containing:

1. The applicable policy or procedure
2. Records demonstrating the process operates
3. Technical evidence from the system(s) implementing the control
4. Most recent review or verification date

When your auditor asks for evidence of control A.8.15 (Logging), you should be able to produce the logging policy, CloudTrail configuration evidence, log retention configuration, and an example of a log review — within minutes, not hours.

QuickTrust's open-source GRC platform provides this evidence structure out of the box, with automated evidence collection from AWS, GCP, and Azure that maps directly to Annex A controls. This eliminates the manual screenshot-and-folder approach that consumes hundreds of engineering hours.

---

## Mid-Article CTA

**Want to know exactly which Annex A controls apply to your environment and where your gaps are?**

Download our ISO 27001 audit readiness checklist — a control-by-control assessment tool built from the evidence requirements we see auditors request most frequently. It covers all 93 Annex A controls with specific evidence expectations for cloud-native SaaS companies.

**[Download our ISO 27001 audit readiness checklist -->](https://trust.quickintell.com/iso27001-audit-readiness-checklist)**

---

## How QuickTrust Gets You Audit-Ready in 6-10 Weeks

The controls and evidence requirements described in this guide represent significant implementation work. The traditional approach — hiring a consultant who advises your engineering team on what to implement — takes 6-12 months because the bottleneck is your engineering team's availability, not the complexity of the work.

QuickTrust eliminates this bottleneck. Our model is fundamentally different from traditional ISO consulting:

**Engineers implement controls — not just advise.** When your audit requires evidence of centralized logging with 12-month retention, our engineers configure CloudTrail, set up log aggregation, implement immutable storage, and verify the configuration. Your engineering team stays focused on product development.

**90% reduction in engineering time.** Instead of your team spending 400-500 hours implementing compliance controls, they spend 40-50 hours on context-specific reviews and approvals. The implementation work is done by engineers who have built these controls across dozens of environments.

**100% audit pass rate across 100+ audits.** The evidence frameworks, implementation patterns, and audit preparation processes described in this guide are not theoretical. They are the same frameworks our team uses on every engagement — and they have produced a zero-failure record across more than 100 certification audits.

**Open-source GRC platform included.** Evidence management, control tracking, and audit preparation are handled through QuickTrust's open-source platform — eliminating the $15K-$60K annual GRC platform cost that most companies pay for tools like Vanta, Drata, or Secureframe. For more on how QuickTrust compares to these platforms, see our [compliance automation platform comparison](/compliance-automation-platforms-comparison).

---

## The Stage 2 Audit: What Actually Happens

Understanding the audit day itself helps you prepare effectively. Here is the typical structure of a Stage 2 certification audit for a cloud-native SaaS company with 20-100 employees:

**Day 1: Opening and Management System Review**
- Opening meeting with leadership
- Review of ISMS scope, context, and interested parties
- Information security policy review
- Risk assessment and risk treatment plan review
- Statement of Applicability walkthrough
- Management review records
- Internal audit results

**Day 2: Control Testing**
- Deep-dive into selected Annex A controls (typically 15-25 controls)
- Technical evidence review (screen sharing for cloud configurations)
- Interviews with control owners (engineering, HR, operations)
- Access control and privileged access verification
- Logging and monitoring demonstration
- Vulnerability management evidence review

**Day 3: Operational Controls and Closing**
- Incident management procedures and records
- Supplier management review
- Business continuity and backup testing evidence
- Remaining control sampling
- Auditor's findings summary
- Closing meeting with preliminary results

The auditor will issue findings in three categories:
- **Major nonconformities:** Systemic failure or absence of a required control. One major nonconformity prevents certification.
- **Minor nonconformities:** Isolated control weakness. Must be addressed within an agreed timeframe, but does not prevent certification.
- **Opportunities for improvement:** Suggestions, not requirements.

---

## Your Prioritized ISO Audit Preparation Checklist

If you are preparing for an ISO 27001 certification audit, here is the prioritized action list based on everything in this guide:

**Priority 1 (Weeks 1-2): Foundation**
- Complete risk assessment with asset-specific risks and treatment decisions
- Finalize Statement of Applicability with accurate implementation status
- Ensure information security policy is approved, communicated, and current
- Verify management review has been conducted and documented

**Priority 2 (Weeks 3-4): High-Scrutiny Controls**
- Implement and verify access control (A.5.15) with least privilege evidence
- Audit and document privileged access (A.8.2) with MFA verification
- Configure centralized logging (A.8.15) with 12-month retention
- Set up security monitoring and alerting (A.8.16) with response evidence
- Run vulnerability scans (A.8.8) and demonstrate remediation activity

**Priority 3 (Weeks 5-6): Operational Controls**
- Complete security awareness training for 100% of in-scope employees (A.6.3)
- Document and test incident response procedures (A.5.24)
- Verify encryption configuration and key management (A.8.24)
- Complete supplier security assessments (A.5.19, A.5.20)
- Conduct internal audit with qualified, independent auditor

**Priority 4 (Weeks 7-8): Evidence Assembly and Rehearsal**
- Organize evidence by Annex A control number
- Conduct a mock audit walkthrough with control owners
- Verify all policies match actual implementation (close the policy-reality gap)
- Prepare control owners for auditor interviews

This is the same preparation timeline our team follows for every QuickTrust ISO 27001 engagement. It is designed to get you audit-ready in 6-10 weeks with confidence that your controls will withstand Stage 2 scrutiny.

For a detailed breakdown of what this process costs, see our [ISO 27001 Certification Cost Guide](/iso-27001-certification-cost). For help deciding whether ISO 27001 or SOC 2 should be your first certification, see our [ISO 27001 vs SOC 2 comparison](/iso-27001-vs-soc2).

---

## Conclusion

ISO 27001 Annex A contains 93 controls. Your auditor will not test all 93 with equal depth. The controls that drive audit outcomes — the ones that generate major nonconformities and block certification — are concentrated in access control, logging, monitoring, vulnerability management, encryption, and incident response. These are the controls where your evidence must be bulletproof.

The organizations that fail ISO audits do not fail because they missed obscure controls. They fail because their policies describe a security program that does not match their actual environment. They fail because logging is enabled but never reviewed. They fail because their risk assessment was copied from a template instead of built from their actual asset inventory.

The organizations that pass — 100% of QuickTrust clients across 100+ audits — prepare differently. They implement controls before documenting them. They build evidence collection into daily operations instead of scrambling before audit day. They focus their preparation time on the 15-20 controls that auditors test most aggressively and ensure those controls have complete, current, and demonstrable evidence.

If you are preparing for ISO 27001 certification and want to know exactly where your gaps are, **[download our ISO 27001 audit readiness checklist](https://trust.quickintell.com/iso27001-audit-readiness-checklist)** or **[talk to our team about getting audit-ready in 6-10 weeks](https://trust.quickintell.com)**.

---

*Related reading:*
- [ISO 27001 Certification: The Complete Implementation Guide](/iso-27001-certification-guide)
- [ISO 27001 Certification Cost in 2026](/iso-27001-certification-cost)
- [ISO 27001 vs SOC 2: Which Certification Unlocks More Enterprise Deals?](/iso-27001-vs-soc2)
- [ISO 27001 Gap Assessment Checklist](/iso27001-gap-assessment-checklist)
- [What Is ISO 27001?](/glossary/what-is-iso-27001)
