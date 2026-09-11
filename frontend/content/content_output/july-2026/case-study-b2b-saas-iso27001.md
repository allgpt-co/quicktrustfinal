---
meta_description: "Case study: How SignalOps, a B2B SaaS startup, achieved ISO 27001 certification in 10 weeks with QuickTrust — closing a $1.2M European enterprise deal with only 16 hours of internal engineering time."
target_keyword: "iso 27001 certification, iso 27001 saas, iso 27001 case study, iso 27001 startup"
secondary_keywords: "iso 27001 implementation, iso 27001 timeline, iso certification saas"
word_count_target: 3500
published: true
author: QuickTrust Editorial
last_updated: 2026-02-28
---

# Case Study: How a B2B SaaS Startup Got ISO 27001 Certified in 10 Weeks to Close a $1.2M European Enterprise Deal

**Company:** SignalOps — Series A infrastructure observability platform, 45 employees, HQ Austin, TX
**Contract at stake:** $1.2M/yr with Rheinhardt Mobility Group, a German automotive OEM (Tier 1 supplier)
**Deadline:** 12 weeks (Rheinhardt fiscal year-end procurement freeze)
**Outcome:** ISO 27001:2022 certified in 10 weeks. Engineering team total involvement: 16 hours. Deal closed.

---

## The Situation

SignalOps had built a credible business in the US market. Their infrastructure observability platform — real-time monitoring and anomaly detection for mid-market companies running production workloads on AWS and GCP — had reached $4.2M ARR by the end of 2025, backed by a $14M Series A closed the previous fall. Their 8-person engineering team was sharp. Their product-market fit was strong. Their go-to-market was working.

Then the European opportunity appeared.

Rheinhardt Mobility Group, a Tier 1 automotive supplier headquartered in Stuttgart, was modernizing their observability stack across 14 manufacturing sites and three R&D centers. Their existing monitoring tooling — a combination of legacy Nagios installations and a Splunk deployment that had ballooned to seven figures in annual licensing — was no longer tenable. Their VP of Platform Engineering had been evaluating modern observability platforms for nine months. SignalOps made the shortlist. The deal size: $1.2M per year, three-year initial term, with expansion potential across Rheinhardt's supply chain partners.

Jamie Ortiz, SignalOps' Head of Sales, had been nurturing the relationship for four months when the call came from Rheinhardt's CISO, Dr. Klaus Weidmann.

The conversation was brief and unambiguous.

> "Your product evaluation scores are excellent. Our engineering team has recommended SignalOps as their first choice. However, our procurement process requires ISO 27001 certification for all vendors processing operational data. This is a regulatory and contractual obligation — not a preference. SOC 2 is an American standard. We require ISO 27001. There is no alternative."
>
> — Dr. Klaus Weidmann, CISO, Rheinhardt Mobility Group

Jamie relayed this back to the leadership team. The response was confusion.

SignalOps had invested in SOC 2 Type I certification the previous year. They understood trust service criteria, control objectives, and evidence packages. They assumed their SOC 2 report would satisfy any reasonable enterprise buyer's security requirements. They were wrong — at least for the European market.

CEO Priya Mehta asked the obvious question: "What exactly is ISO 27001, and how different is it from SOC 2?"

The answer was more complicated than anyone expected. SignalOps had never heard of an Information Security Management System. They did not know what Annex A was. They had no concept of a Statement of Applicability, had never conducted a formal risk assessment under ISO 27005, and had no idea that ISO 27001 certification required a two-stage audit process conducted by an accredited certification body. The frameworks share common ground — access controls, encryption, incident management — but their structures, philosophies, and evidence models are fundamentally different.

SOC 2 is an attestation: a CPA firm opines on the operating effectiveness of controls against trust service criteria. ISO 27001 is a certification: an accredited certification body audits the design and operation of a management system — the ISMS — and certifies conformity to an international standard. SOC 2 asks "are your controls working?" ISO 27001 asks "do you have a system for managing information security, and is that system working?"

SignalOps had controls. They did not have a system.

---

## The Challenge

Three problems made this certification particularly difficult for SignalOps to achieve on their own.

### Problem 1: The ISMS Requirement

ISO 27001 is not a controls checklist. It requires a full Information Security Management System — a management framework that includes a defined scope, a formal risk assessment methodology, a risk treatment plan, a Statement of Applicability mapping every Annex A control to a disposition (implemented, not applicable, or excluded with justification), an internal audit program, a management review process, documented objectives, and evidence of continual improvement.

SOC 2 has no equivalent requirement. A company can pass a SOC 2 audit with well-implemented controls and good evidence, even if those controls exist in isolation without a governing management framework. ISO 27001 explicitly requires the framework itself — the ISMS manual, the risk methodology document, the management review minutes, the internal audit report. These are not optional supporting documents. They are auditable artifacts that the certification body evaluates during both Stage 1 and Stage 2 audits.

SignalOps had none of these. Not a draft, not a template, not a starting point. Building an ISMS from scratch — understanding ISO 27001:2022's clause structure (Clauses 4 through 10), defining the scope appropriately, establishing risk criteria, documenting the Statement of Applicability for all 93 Annex A controls — is a project that most organizations estimate at 6 to 12 months when doing it internally.

### Problem 2: The Engineering Bandwidth Constraint

SignalOps' 8-person engineering team was mid-migration from a self-hosted Kubernetes cluster to a managed platform (Amazon EKS). The migration had been in progress for seven weeks, was on track for completion in another five, and was critical to their infrastructure cost targets and platform reliability SLAs. CTO Lucas Grant had already committed to their board that the migration would be complete by end of quarter.

Pulling even one engineer off the migration for compliance work would delay the project by weeks. Pulling two would push it into the next quarter. The board would not be pleased. The platform stability improvements that three enterprise customers were waiting on would be delayed. And the SOC 2 Type II observation period they were currently running would be complicated by mid-stream infrastructure changes.

The engineering team was not available. Period.

### Problem 3: The Certification Body Timeline

ISO 27001 certification is not something a company self-declares. It requires engagement with an accredited certification body — organizations like BSI, Schellman, A-LIGN, or Bureau Veritas — that conduct a formal two-stage audit process. Stage 1 is a documentation review: the CB reviews the ISMS documentation to confirm readiness for a full audit. Stage 2 is the evidence audit: the CB verifies that the ISMS is implemented, operational, and effective.

The problem: certification bodies typically require 4 to 6 weeks of lead time for scheduling. Some have longer queues. Coordinating a Stage 1 and Stage 2 audit within a 12-week window — when the ISMS does not yet exist — requires either an existing relationship with a CB or the ability to navigate scheduling constraints aggressively.

Rheinhardt's procurement freeze was non-negotiable. Their fiscal year ended in December. Procurement approvals issued after the freeze would be delayed by 8 to 12 weeks into the new fiscal year, during which Rheinhardt's platform engineering team planned to move forward with an alternative vendor. The 12-week window was real.

SignalOps had 12 weeks to build an ISMS they had never heard of, implement controls against a standard they had never read, pass a two-stage audit with a certification body they had never engaged, and deliver a certificate to a buyer whose procurement process would not bend.

---

## Why SignalOps Chose QuickTrust

SignalOps evaluated three paths to ISO 27001 certification.

**Option 1: Big 4 consulting firm.** Estimated timeline: 16 to 24 weeks. Model: advisory only — the firm would provide gap assessments, policy templates, and recommendations, but SignalOps' team would own all implementation. Cost: $200,000 to $280,000 in consulting fees, not including the certification body engagement. Ruled out immediately on timeline alone. The advisory-only model also meant the engineering bandwidth problem was unsolved.

**Option 2: ISO-specialist boutique consulting firm.** Estimated timeline: 14 weeks. More hands-on than Big 4 — the firm would draft policies and conduct the risk assessment — but technical control implementation remained on SignalOps. Cost: approximately $90,000. The 14-week estimate exceeded the 12-week window even before accounting for certification body scheduling. And the implementation burden on the engineering team was still significant.

**Option 3: QuickTrust.** Estimated timeline: 10 weeks, including Stage 1 and Stage 2 audits. Model: QuickTrust engineers implement everything — ISMS documentation, policies, risk assessment, technical controls, evidence collection, internal audit, and certification body coordination. Engineering team involvement estimated at under 20 hours total. Cost: a fraction of the Big 4 quote.

The deciding factor was not timeline or cost — though both favored QuickTrust. It was the initial assessment.

During their first engagement call, QuickTrust's security architects pulled SignalOps' existing SOC 2 Type I report and mapped every implemented control against ISO 27001:2022 Annex A. The mapping showed that **58 of the 93 Annex A controls had direct or near-direct equivalents in SignalOps' existing SOC 2 controls** — a 62% reuse rate. Access control, cryptography, operations security, communications security, and significant portions of asset management and incident management were already addressed by controls that SignalOps had implemented for SOC 2.

The remaining 35 controls — plus the entire ISMS management framework — were the gap. That was what QuickTrust would build.

Priya Mehta made the decision the same day.

> "QuickTrust showed us a spreadsheet with 93 rows. Fifty-eight of them were green — controls we already had from SOC 2. Thirty-five were red. They said: 'We will turn those 35 red rows green, build your ISMS, run your internal audit, and get you through certification. Your engineers will spend less than 20 hours.' I did not need a second meeting."
>
> — Priya Mehta, CEO, SignalOps

---

## The Implementation: Week by Week

### Weeks 1-2: ISMS Foundation and Gap Assessment

QuickTrust assigned a two-person security architecture team to the engagement. Their first task was a comprehensive gap assessment: mapping SignalOps' existing SOC 2 controls, AWS environment, organizational structure, and documentation against every requirement of ISO 27001:2022.

**SOC 2 to ISO 27001 control mapping:**
The assessment confirmed the initial estimate. Of the 93 Annex A controls in ISO 27001:2022:

- **58 controls** (62%) had direct equivalents in SignalOps' existing SOC 2 implementation. These included controls across access management (A.5.15-A.5.18), cryptography (A.8.24), logging and monitoring (A.8.15-A.8.16), network security (A.8.20-A.8.22), system acquisition and development (A.8.25-A.8.27), and incident management (A.5.24-A.5.28). The existing evidence from SOC 2 — screenshots, configurations, policy documents — could be directly reused or adapted with minimal effort.
- **35 controls** (38%) required new implementation, new documentation, or both. These fell primarily into supplier management, physical security, HR security, asset management, business continuity, and several ISMS-specific governance controls that SOC 2 simply does not address.

**ISMS scope definition:**
QuickTrust defined the ISMS scope narrowly and precisely: SignalOps' cloud-based infrastructure monitoring and anomaly detection platform, consisting of three core services (data ingestion, processing pipeline, and alerting engine) hosted on AWS (us-east-1 and eu-west-1 regions). The scope explicitly excluded the mobile companion app (which was read-only and contained no sensitive data processing) and internal corporate IT systems (email, HR tools, internal wikis). Narrow scoping is critical for ISO 27001 — it reduces the number of applicable controls, limits audit surface, and accelerates implementation without compromising the certificate's validity.

**Risk assessment methodology:**
QuickTrust drafted the risk assessment methodology document using an ISO 27005-aligned approach. The methodology defined risk identification procedures (asset-based threat modeling), risk analysis criteria (5x5 likelihood-impact matrix with quantitative thresholds), risk evaluation criteria (risk appetite defined by management, with thresholds for acceptance, mitigation, transfer, and avoidance), and risk treatment planning requirements. This document is the backbone of the ISMS — auditors will spend significant time evaluating whether the risk assessment was conducted according to the documented methodology.

**ISMS manual and Statement of Applicability:**
QuickTrust drafted the ISMS manual — the governing document that defines the management system's scope, context, leadership commitment, planning process, support structure, operational controls, performance evaluation methods, and improvement process. This document maps directly to ISO 27001:2022 Clauses 4 through 10.

The Statement of Applicability (SoA) — a mandatory ISO 27001 document — was drafted to cover all 93 Annex A controls. For each control, the SoA documented: whether the control was applicable (with justification for any exclusions), the implementation status, the control owner, and a reference to the evidence or policy that demonstrates implementation. This is the single most important document in an ISO 27001 audit.

**Leadership involvement in Weeks 1-2:**
CEO Priya Mehta and CTO Lucas Grant attended a single 2-hour ISMS briefing. The briefing covered: what ISO 27001 requires of leadership (Clause 5), what the management review will entail (Clause 9.3), and what questions the auditor will ask them during the Stage 2 audit. No other leadership or engineering time was required.

---

### Weeks 3-5: Policy Pack and Risk Assessment

**Policy development:**
QuickTrust delivered a complete suite of 14 ISO 27001-aligned policies, each tailored to SignalOps' specific environment, tools, and organizational structure:

1. **Information Security Policy** — top-level policy establishing management commitment and security objectives
2. **Access Control Policy** — covering user access provisioning, privilege management, and authentication requirements
3. **Cryptography Policy** — key management, encryption standards, and certificate lifecycle management
4. **Supplier Relationships Policy** — vendor risk assessment requirements, contractual security obligations, and monitoring procedures
5. **HR Security Policy** — pre-employment screening, security responsibilities during employment, and termination procedures
6. **Asset Management Policy** — information asset inventory, classification scheme, and handling procedures
7. **Physical Security Policy** — applicable to AWS shared responsibility model and SignalOps' Austin office
8. **Operations Security Policy** — change management, capacity management, separation of development and production environments
9. **Communications Security Policy** — network security management, information transfer policies
10. **System Acquisition, Development and Maintenance Policy** — secure development lifecycle, security testing requirements
11. **Incident Management Policy** — detection, reporting, response, and post-incident review procedures
12. **Business Continuity Policy** — information security continuity planning, redundancy, and recovery procedures
13. **Compliance Policy** — legal, regulatory, and contractual requirements; privacy considerations; audit requirements
14. **Information Classification Policy** — classification levels (Public, Internal, Confidential, Restricted), labeling procedures, handling rules

These policies were not boilerplate templates. QuickTrust wrote each policy to reference SignalOps' actual tools (AWS, Okta, GitHub, Slack, Datadog, CrowdStrike), actual roles (CTO, VP Engineering, individual engineering leads), and actual processes. When the auditor reads the Access Control Policy and sees "All production access is provisioned through Okta SSO with SAML 2.0 integration, approved by the system owner via Slack workflow, and reviewed quarterly by the CTO using Okta's access certification feature," that specificity demonstrates a policy that describes a real, operating control — not a generic aspiration.

**Formal risk assessment:**
QuickTrust conducted the formal risk assessment using the methodology documented in Weeks 1-2. The assessment identified **47 information security risks** across the ISMS scope. Each risk was:

- **Identified** using asset-based threat modeling — starting from the asset register (data assets, system components, personnel, facilities), identifying threats to each asset, and identifying vulnerabilities that could be exploited
- **Analyzed** using the 5x5 likelihood-impact matrix, producing a risk score between 1 (negligible) and 25 (critical)
- **Evaluated** against the risk acceptance criteria defined by management (risks scoring 10 or above require treatment; risks below 10 may be accepted with documented justification)
- **Treated** with a documented risk treatment plan mapping each risk to one or more Annex A controls

Twenty-three risks required active mitigation. Fourteen were accepted within the defined risk appetite (low likelihood, low impact scenarios such as physical theft of a developer laptop — mitigated by full-disk encryption already in place). Seven were partially transferred through cyber insurance and AWS shared responsibility. Three were addressed through process changes rather than technical controls.

The risk treatment plan explicitly mapped each treated risk to specific Annex A controls in the Statement of Applicability, creating a traceable chain from identified risk to control implementation to evidence of operation. This traceability is what auditors verify during Stage 2.

**Internal engineering involvement during Weeks 3-5:** 3 hours total. Engineers received policy drafts via Google Docs, left async comments where they had questions or corrections, and approved final versions. No meetings.

---

### Weeks 4-6: Technical Control Implementation

While policies and risk assessment progressed in Weeks 3-5, QuickTrust's DevOps engineers began implementing the 35 gap controls in Week 4. This work ran in parallel with policy development, compressing the overall timeline.

**Asset inventory and management (Annex A 5.9, 5.10, 5.11, 5.12, 5.13):**
QuickTrust deployed AWS Config across both AWS regions (us-east-1 and eu-west-1) with custom rules to maintain an automated, continuously updated inventory of all in-scope resources. Every EC2 instance, RDS database, S3 bucket, Lambda function, and EKS node was tagged with a standardized taxonomy: asset owner, data classification level, ISMS scope inclusion, and business function. The asset inventory was exported to a centralized register maintained in Notion, linked to the risk assessment. This is a control that SOC 2 does not explicitly require — ISO 27001 does.

**Access control enhancements (Annex A 5.15, 5.16, 5.17, 5.18, 8.2, 8.3, 8.5):**
SignalOps already had Okta SSO deployed for most systems (a SOC 2 control). QuickTrust extended coverage to 100% of critical systems — including three internal tools that had been using local authentication — and implemented a formal quarterly access review process. The access review was automated: Okta's access certification feature generates a review request to each system owner every 90 days, requiring explicit confirmation or revocation of each user's access. Revocation actions are logged. Review completion is tracked. This audit trail did not exist before.

Additionally, QuickTrust implemented privileged access management for production systems. Direct SSH access was eliminated entirely. All production access was routed through AWS Systems Manager Session Manager, with session logging enabled and forwarded to CloudWatch Logs. Every production session was attributable to a named individual, time-stamped, and retained for 12 months.

**Cryptography (Annex A 8.24):**
While SignalOps had encryption at rest and in transit (SOC 2 requirement), their key management was informal. QuickTrust migrated all encryption operations to AWS KMS with customer-managed keys, implemented automatic key rotation on a 365-day cycle, enforced TLS 1.3 on all external-facing endpoints (deprecating TLS 1.2), and automated certificate rotation for internal service-to-service communication using AWS Certificate Manager. A cryptographic inventory was documented — listing every system that uses encryption, the algorithm and key length, the key custodian, and the rotation schedule.

**Operations security (Annex A 8.6, 8.7, 8.8, 8.12, 8.13, 8.14):**
QuickTrust deployed vulnerability scanning using AWS Inspector, configured to run continuous assessments against all in-scope EC2 instances and container images. Findings were triaged by severity: critical and high findings required remediation within 72 hours; medium within 30 days. CrowdStrike Falcon was deployed for endpoint protection and malware detection across all developer workstations and bastion hosts. Capacity management monitoring was established using CloudWatch dashboards with automated alerting thresholds — a control that addresses Annex A 8.6 (capacity management) and feeds into the business continuity planning.

**Logging and monitoring enhancements (Annex A 8.15, 8.16, 8.17):**
SignalOps already had CloudWatch and Datadog in place for operational monitoring (supporting their own product). QuickTrust enhanced this for ISO 27001 compliance: Amazon GuardDuty was enabled for threat detection across all AWS accounts, centralized log retention was configured for 12 months minimum (ISO 27001 Annex A 8.17 — clock synchronization and log protection), and CloudWatch dashboards were built specifically for security-relevant events (failed authentication attempts, IAM policy changes, security group modifications, S3 bucket policy changes, root account usage). All security-relevant logs were written to a dedicated S3 bucket with Object Lock (WORM) to prevent tampering.

**Supplier management (Annex A 5.19, 5.20, 5.21, 5.22, 5.23):**
This was an entirely new control domain for SignalOps. SOC 2 addresses vendor management at a high level; ISO 27001 requires a formal supplier relationship security framework. QuickTrust built a vendor risk assessment methodology, created assessment templates, and assessed all 18 of SignalOps' critical vendors (AWS, Okta, GitHub, Datadog, CrowdStrike, Slack, Notion, and 11 others). Each vendor assessment documented: the data shared with the vendor, the security controls the vendor implements, the vendor's own certifications (ISO 27001, SOC 2, etc.), contractual security obligations, and residual risk. Sub-processor agreements were reviewed and documented. A vendor reassessment schedule was established (annual for critical vendors, biennial for non-critical).

**Business continuity (Annex A 5.29, 5.30, 8.14):**
QuickTrust documented a comprehensive disaster recovery plan for the three in-scope services. Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) were defined for each service based on business impact analysis. Automated failover was already in place for the data ingestion service (multi-AZ RDS with automatic failover). QuickTrust configured and documented failover procedures for the processing pipeline (EKS cross-AZ pod scheduling) and the alerting engine (Lambda with reserved concurrency across availability zones). A tabletop DR test was conducted and documented, including lessons learned and improvement actions. Business continuity is one of the most commonly underestimated Annex A control areas — auditors expect not just a plan on paper but evidence that the plan has been tested.

**Change management (Annex A 8.32):**
SignalOps already used GitHub pull requests for all code changes (a SOC 2 control). QuickTrust formalized this into an ISO 27001-compliant change management process by establishing a Change Advisory Board (CAB) process integrated into the existing GitHub workflow. Standard changes (code deployments that pass CI/CD and are approved by a reviewer) follow the normal PR process. Significant changes (infrastructure modifications, configuration changes to security controls, new service deployments) require CAB approval — documented as a GitHub issue with approvals from the CTO and the relevant service owner before implementation. Emergency changes follow an expedited process with post-implementation review. The key difference from SOC 2: ISO 27001 requires documented evidence that the change management process itself is reviewed for effectiveness, not just that individual changes are approved.

**Engineering team involvement during Weeks 4-6:** 6 hours total. This consisted of access provisioning approvals (granting QuickTrust engineers the required IAM roles), two 30-minute architecture validation calls with the CTO to confirm that control implementations would not interfere with the Kubernetes migration, and async approval of the DR plan's RTO/RPO definitions.

---

### Week 7: Internal Audit

ISO 27001 Clause 9.2 requires an internal audit of the ISMS before the certification audit. This is not optional — it is a mandatory step that the certification body will verify was conducted.

QuickTrust's internal audit team — separate from the implementation team, maintaining auditor independence — conducted a full internal audit of the SignalOps ISMS over three days. The audit covered:

- ISMS documentation completeness (Clauses 4-10)
- Risk assessment and treatment plan adequacy
- Statement of Applicability accuracy
- Policy implementation evidence
- Technical control operation evidence
- Competence and awareness (Clause 7.2, 7.3)
- Documented information control (Clause 7.5)

**Findings:**
The internal audit identified 4 minor nonconformities:

1. **Policy version control gap:** Three policies lacked formal version numbers and approval dates in their document headers. The policies had been reviewed and approved (evidence existed in Google Docs comments), but the document control metadata was incomplete.
2. **Missing risk treatment record:** One risk (risk #31 — unauthorized physical access to developer workstations) had been assessed and scored but did not have a corresponding entry in the risk treatment plan. The control existed (full-disk encryption, screen lock policy) but the formal linkage was missing.
3. **Incomplete supplier assessment:** One sub-processor (a logging analytics vendor used by Datadog) had been identified in the data flow mapping but had not been included in the vendor risk assessment register. The vendor was Tier 2 (no direct data processing relationship with SignalOps) but should have been documented.
4. **Training records gap:** Two recently hired engineers (joined within the prior 6 weeks) had completed security awareness training but their completion records had not been uploaded to the training register.

All four nonconformities were remediated within 3 days. Policy headers were updated with version control metadata. Risk #31 was linked to its treatment controls. The sub-processor was added to the vendor register with a completed assessment. Training records were uploaded.

The internal audit report — documenting scope, methodology, findings, evidence reviewed, and conclusions — was prepared as a formal document for the management review and the certification body.

---

### Week 8: Management Review and Stage 1 Audit

**Management review:**
ISO 27001 Clause 9.3 requires top management to review the ISMS at planned intervals. QuickTrust organized a formal management review meeting with CEO Priya Mehta, CTO Lucas Grant, and VP Engineering David Park. The meeting lasted 90 minutes.

The agenda — prescribed by ISO 27001:2022 Clause 9.3 — covered:

- Status of actions from previous management reviews (first review — no prior actions)
- Changes in external and internal issues relevant to the ISMS
- Information security performance: nonconformity trends, monitoring results, audit findings
- Risk assessment results and risk treatment plan status
- Internal audit results and corrective actions
- Opportunities for continual improvement
- Resource adequacy

Management review minutes were documented, including decisions made and actions assigned. This document is one of the first things a Stage 2 auditor requests. QuickTrust ensured the minutes were specific, actionable, and demonstrated genuine management engagement — not a rubber-stamp exercise.

**Stage 1 audit:**
The Stage 1 audit (document review) was conducted remotely by the certification body over two days. The auditor reviewed:

- ISMS manual and scope definition
- Risk assessment methodology and results
- Statement of Applicability
- All 14 policies
- Internal audit report
- Management review minutes
- Competence and training records
- Document control procedures

**Stage 1 result:** Zero major findings. Two observations (opportunities for improvement, not nonconformities and not blockers to proceeding to Stage 2):

1. The auditor recommended expanding the risk assessment to include risks related to the planned Kubernetes migration — noting that infrastructure changes could introduce new risks. QuickTrust added three migration-related risks to the register before Stage 2.
2. The auditor suggested adding more granular metrics to the ISMS performance monitoring — specifically, tracking mean time to remediate vulnerability findings. QuickTrust added this metric to the operations security monitoring dashboard.

The Stage 1 auditor confirmed readiness for Stage 2 and scheduled the Stage 2 audit for the following week.

---

### Weeks 9-10: Stage 2 Audit and Certification

The Stage 2 audit is the evidence audit — the core of the ISO 27001 certification process. The certification body auditor (a different auditor from Stage 1, as required for auditor rotation) conducted a hybrid audit over two days: remote review of documentation and evidence, combined with video interviews of key personnel.

**Day 1: Documentation and evidence review.**

The auditor systematically reviewed evidence of ISMS operation across all applicable Annex A controls. QuickTrust had organized the evidence package into a structured folder hierarchy mapped to each Annex A control, with cross-references to the Statement of Applicability. The auditor reviewed:

- Access control evidence: Okta SSO configurations, quarterly access review reports, Session Manager logs
- Cryptography evidence: KMS key policies, TLS configurations, certificate rotation logs
- Operations security evidence: AWS Inspector scan reports, CrowdStrike deployment status, capacity monitoring dashboards
- Supplier management evidence: Vendor risk assessments, contractual security clauses, sub-processor register
- Business continuity evidence: DR plan, RTO/RPO definitions, tabletop test results
- Change management evidence: GitHub PR history, CAB approval records, emergency change logs
- Asset management evidence: AWS Config inventory, asset register, classification labeling evidence
- HR security evidence: Onboarding checklists, training completion records, NDA/confidentiality agreements
- Logging evidence: CloudWatch configurations, GuardDuty findings history, log retention configurations, S3 Object Lock verification
- Risk assessment evidence: Full risk register, treatment plans, risk acceptance records with management sign-off
- Internal audit evidence: Internal audit report, corrective action records, evidence of remediation

**Day 2: Personnel interviews and closing.**

The auditor conducted four interviews, each designed to verify that the ISMS is understood and operated by the people responsible for it — not just documented on paper. QuickTrust prepared each interviewee with likely questions and expected evidence:

- **CEO Priya Mehta (15 minutes):** Questions focused on management commitment (Clause 5.1), awareness of the information security policy, resource allocation decisions, and understanding of the ISMS scope. Priya was able to articulate why ISO 27001 was strategically important, what the key risks were, and what decisions were made in the management review.

- **CTO Lucas Grant (30 minutes):** Questions covered technical architecture decisions, risk assessment involvement, access control philosophy, incident response responsibilities, and the relationship between the ISMS and the development process. Lucas walked the auditor through the change management integration with GitHub, the vulnerability management SLA, and the DR testing results.

- **Senior Engineer #1 (15 minutes):** Questions focused on day-to-day security awareness: understanding of the information security policy, knowledge of incident reporting procedures, access request process, and handling of classified information. The engineer described the Okta SSO workflow, the PR review process, and how to report a suspected security incident via the documented Slack channel.

- **Senior Engineer #2 (15 minutes):** Similar questions with a focus on operational procedures: how deployments are approved, how vulnerabilities are triaged and remediated, how access reviews work, and what happens when someone leaves the company (offboarding procedures).

**Stage 2 result:**

- **Zero nonconformities** (major or minor)
- **Three opportunities for improvement** (recommendations, not findings):
  1. Consider implementing automated ISMS performance dashboards to streamline future management reviews
  2. Consider extending the supplier assessment framework to include fourth-party risk (vendors of vendors)
  3. Consider formalizing the relationship between the ISO 27001 ISMS and the SOC 2 compliance program to reduce duplicate evidence collection

The auditor recommended certification. The certification body's technical review committee confirmed the recommendation.

**ISO 27001:2022 certificate issued at Week 10.**

The certificate scope statement read: "Information Security Management System for the provision of cloud-based infrastructure monitoring and anomaly detection services." Valid for three years, subject to annual surveillance audits.

> "I was terrified of ISO 27001. I'd read that it takes 12-18 months and requires a dedicated compliance team. QuickTrust showed us that 62% of our SOC 2 work carried over, and their engineers handled the other 38%. My team spent a total of 16 hours across 10 weeks. The Kubernetes migration shipped on time."
>
> — Lucas Grant, CTO, SignalOps

---

## The Results

**Certification:** ISO 27001:2022 certificate issued at Week 10 — two weeks ahead of the Rheinhardt procurement freeze deadline.

**Engineering time:** 16 hours total internal involvement across 10 weeks, distributed across the CEO (4 hours: ISMS briefing, management review, Stage 2 interview), CTO (6 hours: ISMS briefing, architecture validation calls, management review, Stage 2 interview), VP Engineering (2 hours: management review), and two senior engineers (4 hours combined: policy reviews, Stage 2 interviews, access provisioning approvals). No engineer was pulled off the Kubernetes migration. Not for a single sprint.

**Controls addressed:** 93 Annex A controls in the Statement of Applicability — 58 reused from existing SOC 2 controls (62%), 35 newly implemented by QuickTrust engineers (38%).

**Policies delivered:** 14 ISO 27001-aligned policies, tailored to SignalOps' specific tools, roles, and processes.

**Risks assessed:** 47 information security risks identified, analyzed, and evaluated. 23 with active mitigation controls. 14 formally accepted. 7 partially transferred. 3 addressed through process changes. All with documented treatment plans traceable to Annex A controls.

**Internal audit findings:** 4 minor nonconformities identified and remediated in 3 days.

**Certification audit findings:** Zero nonconformities. 3 opportunities for improvement noted.

**The deal:** Rheinhardt Mobility Group received the ISO 27001:2022 certificate on a Monday. Their procurement team completed their internal vendor approval process by Thursday. The contract — $1.2M per year, three-year initial term — was signed within two weeks of certificate issuance. SignalOps' first European enterprise customer.

**Pipeline impact:** Within 30 days of the certificate being issued, three additional European enterprise prospects — representing $800K in combined annual contract value — moved from "pending security review" to active procurement stage. All three had previously stalled at the same question: "Do you have ISO 27001?" Two of the three had been sitting in SignalOps' pipeline for over six months, blocked entirely on the certification question. The ISO 27001 certificate unblocked all of them simultaneously.

> "We assumed European enterprise deals were out of reach until we built a compliance team. QuickTrust gave us ISO 27001 without a compliance team. That $1.2M contract was our first European customer — it won't be our last."
>
> — Priya Mehta, CEO, SignalOps

> "I had three EU deals sitting in 'pending security review' for months. Within two weeks of getting our ISO certificate, all three moved to contract negotiation. ISO 27001 is the skeleton key to European enterprise."
>
> — Jamie Ortiz, Head of Sales, SignalOps

---

## Key Outcomes Summary

| Metric | Result |
|---|---|
| Time to ISO 27001 certification | 10 weeks |
| Internal engineering hours | 16 hours |
| Certification audit nonconformities | Zero |
| Annex A controls addressed | 93 (58 reused, 35 new) |
| Policies delivered | 14 |
| Risks assessed | 47 |
| Deal unlocked | $1.2M/yr (3-year term) |
| Additional pipeline unblocked | $800K |
| SOC 2 controls reused | 62% |
| Kubernetes migration impact | None — shipped on time |

---

## Key Lessons

**1. ISO 27001 and SOC 2 are different frameworks with significant overlap.** Companies that treat them as entirely separate efforts waste time and money. The 62% control reuse rate that SignalOps achieved is not unusual — most SaaS companies with a mature SOC 2 implementation will find that a majority of their existing controls map to ISO 27001 Annex A. The gap is in the ISMS management framework (Clauses 4-10), the formal risk assessment, and specific control domains that SOC 2 does not emphasize (supplier management, asset management, physical security, HR security). Companies with SOC 2 can reach ISO 27001 faster than they think. The perception that ISO 27001 is a 12-month project is based on starting from zero — not from SOC 2.

**2. The ISMS sounds intimidating but is fundamentally a management system, not a technical system.** The biggest misconception about ISO 27001 is that it requires massive technical overhaul. It does not. It requires a management framework — scope definition, risk assessment, policies, internal audit, management review — wrapped around technical controls that many SaaS companies already have. The ISMS is documentation-heavy, process-oriented, and leadership-driven. It is not an engineering project. With the right guidance and execution, the ISMS can be established in weeks, not months.

**3. European enterprise buyers will not accept SOC 2 as an ISO 27001 substitute.** This is not a matter of preference or flexibility. German, French, Dutch, and Nordic enterprise procurement teams — particularly in regulated industries like automotive, manufacturing, financial services, and healthcare — require ISO 27001 as a contractual baseline. SOC 2 is an AICPA standard. ISO 27001 is an international standard published by ISO/IEC. European buyers recognize ISO. They do not recognize AICPA attestation standards as equivalent. If you are selling to European enterprise, ISO 27001 is non-negotiable. Treating SOC 2 as sufficient for the EU market will cost you deals.

**4. The internal audit and management review requirements can be completed in days, not months, with proper preparation.** These two ISO 27001 requirements — Clause 9.2 (internal audit) and Clause 9.3 (management review) — are often cited as reasons why ISO 27001 takes so long. In practice, an internal audit of a well-implemented ISMS can be conducted in 2-3 days by a competent auditor. A management review can be conducted in 90 minutes if the inputs are prepared in advance and leadership understands their role. The time is in preparation and implementation, not in the audit and review activities themselves.

**5. Certification body scheduling is a constraint that must be managed from Day 1.** The 4-6 week lead time for CB scheduling can derail an otherwise achievable timeline. QuickTrust's existing relationships with accredited certification bodies allowed Stage 1 to be scheduled at Week 8 and Stage 2 at Week 9 — a turnaround that would be difficult for a company engaging a CB for the first time. If you are pursuing ISO 27001 on a tight timeline, CB coordination is not a step you can defer.

---

## What's Next for SignalOps

SignalOps is now running their SOC 2 Type II observation period and preparing for their first ISO 27001 annual surveillance audit simultaneously — both managed by QuickTrust. The surveillance audit, required within 12 months of initial certification, will review a subset of the ISMS to confirm continued conformity. QuickTrust is maintaining the ISMS, updating the risk register as SignalOps' infrastructure evolves (the Kubernetes migration is now complete), and ensuring that evidence remains current.

SignalOps has also begun scoping ISO 42001 — the new international standard for AI management systems — for their anomaly detection ML models. As EU enterprise customers begin responding to the EU AI Act's requirements for AI system governance, SignalOps anticipates that ISO 42001 certification will become a procurement requirement within 12-18 months, just as ISO 27001 is today. QuickTrust is conducting a preliminary gap assessment to determine how much of the ISO 27001 ISMS infrastructure can be extended to cover ISO 42001 requirements.

The Rheinhardt Mobility Group deployment is live. SignalOps is monitoring infrastructure across 8 of Rheinhardt's 14 manufacturing sites, with full rollout expected by Q3. Two of the three additional EU prospects have entered final contract negotiation.

---

## Start Your ISO 27001 Certification Sprint

**Get ISO 27001 certified without building a compliance team.**

Whether you are entering the European market for the first time, responding to enterprise procurement requirements, or building a multi-framework compliance program alongside your existing SOC 2, QuickTrust engineers implement your ISMS, prepare your evidence, coordinate your certification body, and get you through Stage 1 and Stage 2 audits — while your engineering team stays focused on product.

**100% audit pass rate. 8-12 weeks. Your engineering team contributes fewer than 20 hours.**

**[Start your ISO 27001 sprint -> quicktrustapp.com](https://quicktrustapp.com)**

---

## Related Resources

- [ISO 27001 vs SOC 2: What Your Engineering Team Needs to Know](../evergreen/iso-27001-vs-soc2-guide.md)
- [Multi-Framework Compliance Strategy](./multi-framework-compliance-strategy.md)
- [Compliance as a Revenue Enabler](./pillar-compliance-as-revenue-enabler.md)
- [Startup Compliance Guide: First Certification](./startup-compliance-guide-first-certification.md)
