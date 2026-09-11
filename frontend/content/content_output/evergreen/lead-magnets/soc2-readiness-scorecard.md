---
meta_description: "SOC 2 readiness scorecard with 40 questions across 8 security domains mapped to Trust Services Criteria."
target_keyword: "soc 2 readiness scorecard, soc 2 readiness assessment"
secondary_keywords: "soc 2 readiness checklist, soc 2 self assessment, soc 2 audit readiness, soc 2 preparation checklist"
word_count_target: "2000"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# SOC 2 Readiness Scorecard
## Assess Your Certification Readiness in 10 Minutes

**Prepared by QuickTrust | trust.quickintell.com**
*AI-Powered GRC Platform + Expert Engineering Implementation*

---

## How to Use This Scorecard

This scorecard contains **40 questions across 8 security domains** that directly map to the SOC 2 Trust Services Criteria. For each question, assign a score based on your current implementation status:

| Score | Meaning |
|-------|---------|
| **0** | Not implemented — no evidence, no process, no documentation exists |
| **1** | Partially implemented — in progress, informal, inconsistently applied, or undocumented |
| **2** | Fully implemented — documented, enforced, consistently applied, and auditable |

**Total possible score: 80 points**

Record your score for each question, sum the domain totals, then add them for your overall score. Your results and recommended next steps appear at the end.

> **Time required:** 10–15 minutes
> **Who should complete this:** CISO, CTO, VP Engineering, or Security Lead
> **Save your results** — you'll need them to book your free gap assessment call with QuickTrust

---

## Domain 1: Access Control
*Maps to: CC6 — Logical and Physical Access Controls*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 1.1 | Do you maintain a formal inventory of all users with access to production systems, and is this inventory reviewed at least quarterly? | |
| 1.2 | Is multi-factor authentication (MFA) enforced for all remote access, cloud consoles, and privileged accounts — with no exceptions? | |
| 1.3 | Do you follow a documented least-privilege access model, where users are granted only the minimum permissions needed for their role? | |
| 1.4 | Is there a documented, consistently followed offboarding process that revokes all system access within 24 hours of employee termination? | |
| 1.5 | Are privileged accounts (admin, root, superuser) separated from standard user accounts, with privileged access requiring documented justification and approval? | |

**Domain 1 Total: \_\_\_\_ / 10**

---

## Domain 2: Encryption
*Maps to: CC6.7, CC9 — Encryption and Data Protection*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 2.1 | Is all sensitive data encrypted at rest using AES-256 or equivalent, across databases, object storage, and backup media? | |
| 2.2 | Is all data in transit encrypted using TLS 1.2 or higher, with weak cipher suites disabled and HTTPS enforced across all services? | |
| 2.3 | Do you have a documented key management policy that covers key generation, rotation schedules, storage, and destruction? | |
| 2.4 | Are encryption keys stored separately from the data they protect, using a dedicated key management service (e.g., AWS KMS, HashiCorp Vault)? | |
| 2.5 | Is there a documented process for encrypting data before it leaves your network boundary, including emails, file transfers, and API payloads containing sensitive data? | |

**Domain 2 Total: \_\_\_\_ / 10**

---

## Domain 3: Monitoring & Logging
*Maps to: CC7 — System Operations and Monitoring*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 3.1 | Are audit logs enabled and collected for all production systems, cloud infrastructure, and applications — including authentication events, admin actions, and data access? | |
| 3.2 | Are logs stored in a centralized, tamper-resistant system (SIEM or equivalent) with a documented retention period of at least 12 months? | |
| 3.3 | Are automated alerts configured for security-relevant events such as failed login attempts, privilege escalation, configuration changes, and anomalous data access? | |
| 3.4 | Is there a documented process for reviewing security alerts, with defined response SLAs and evidence of regular log reviews by a responsible team? | |
| 3.5 | Do you monitor third-party integrations, APIs, and vendor connections for anomalous activity, and are these logs included in your centralized logging platform? | |

**Domain 3 Total: \_\_\_\_ / 10**

---

## Domain 4: Incident Response
*Maps to: CC7.3, CC7.4, CC7.5 — Incident Management*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 4.1 | Do you have a written Incident Response Plan (IRP) that defines incident classification, escalation paths, roles and responsibilities, and communication procedures? | |
| 4.2 | Has your incident response plan been tested within the past 12 months via a tabletop exercise, simulation, or actual incident — with documented results? | |
| 4.3 | Do you maintain an incident log or ticketing system that tracks all security events with timestamps, severity, actions taken, and resolution status? | |
| 4.4 | Are breach notification procedures documented and compliant with applicable regulations (GDPR 72-hour rule, HIPAA 60-day rule, state breach laws) for customer and regulatory notification? | |
| 4.5 | Is there a documented post-incident review process (post-mortem) that generates lessons learned and feeds back into policy and control improvements? | |

**Domain 4 Total: \_\_\_\_ / 10**

---

## Domain 5: Change Management
*Maps to: CC8 — Change Management*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 5.1 | Is there a formal change management policy that requires documented approval before deploying code, infrastructure changes, or configuration modifications to production? | |
| 5.2 | Are all production deployments tracked in a change log or ticketing system with records of who approved, who deployed, when, and what changed? | |
| 5.3 | Is there a documented and enforced process for emergency/hotfix changes, including retroactive approval, documentation, and post-change review? | |
| 5.4 | Do you maintain separate development, staging/QA, and production environments, with production access restricted to authorized personnel and deployment automation? | |
| 5.5 | Are code changes reviewed via pull request or peer review by at least one other engineer before merging to main branches, with evidence retained in version control history? | |

**Domain 5 Total: \_\_\_\_ / 10**

---

## Domain 6: Vendor Management
*Maps to: CC9.2 — Vendor and Business Partner Risk*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 6.1 | Do you maintain a documented inventory of all vendors, subprocessors, and third parties that have access to your systems or customer data? | |
| 6.2 | Is there a formal vendor risk assessment process, including security questionnaires or SOC 2 / ISO 27001 review, conducted before onboarding new vendors? | |
| 6.3 | Are Data Processing Agreements (DPAs) or Business Associate Agreements (BAAs) executed with all vendors who process personal or sensitive data? | |
| 6.4 | Are vendor security postures reviewed at least annually, with evidence of reassessment documented in your vendor management system? | |
| 6.5 | Is there an offboarding process for terminated vendors that includes revoking access, retrieving or destroying data, and documenting the offboarding completion? | |

**Domain 6 Total: \_\_\_\_ / 10**

---

## Domain 7: Security Policies
*Maps to: CC1, CC2 — Control Environment and Communication*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 7.1 | Do you have a master Information Security Policy that has been approved by leadership, communicated to all employees, and reviewed within the past 12 months? | |
| 7.2 | Are role-specific security policies (e.g., Acceptable Use, Password, Remote Work) documented, distributed to all employees, and acknowledged in writing? | |
| 7.3 | Do all employees complete security awareness training at least annually, with completion records tracked and maintained as auditable evidence? | |
| 7.4 | Are all security policies version-controlled with a documented review and approval cycle, and are superseded versions archived? | |
| 7.5 | Is there a formal process for employees to report security concerns, policy violations, or suspected incidents — with defined escalation paths and non-retaliation guarantees? | |

**Domain 7 Total: \_\_\_\_ / 10**

---

## Domain 8: Business Continuity
*Maps to: A17, CC9 — Availability and Business Continuity*

| # | Question | Score (0/1/2) |
|---|----------|---------------|
| 8.1 | Do you have a documented Business Continuity Plan (BCP) and Disaster Recovery Plan (DRP) that define RTOs and RPOs for critical systems? | |
| 8.2 | Are automated backups in place for all production databases and critical data, with backups stored in a separate geographic region and tested for restoration? | |
| 8.3 | Has your disaster recovery plan been tested within the past 12 months via a failover test or simulation, with documented results showing RTO/RPO targets were met? | |
| 8.4 | Do you have documented infrastructure redundancy and high-availability configurations for systems covered by your uptime commitments or SLAs? | |
| 8.5 | Is there a documented communication plan for customer and stakeholder notification in the event of a service disruption, including defined communication timelines and templates? | |

**Domain 8 Total: \_\_\_\_ / 10**

---

## Your Scorecard Summary

| Domain | Max Score | Your Score |
|--------|-----------|------------|
| Domain 1: Access Control | 10 | |
| Domain 2: Encryption | 10 | |
| Domain 3: Monitoring & Logging | 10 | |
| Domain 4: Incident Response | 10 | |
| Domain 5: Change Management | 10 | |
| Domain 6: Vendor Management | 10 | |
| Domain 7: Security Policies | 10 | |
| Domain 8: Business Continuity | 10 | |
| **TOTAL** | **80** | |

---

## Score Interpretation

### 0–30: Early Stage
**What this means:**
You have significant gaps across multiple control domains. Your organization is not ready for a SOC 2 audit, and attempting one now would result in findings across the board — potentially delaying certification by 12+ months and damaging your auditor relationship. The good news: you're in the right place to get started.

**What happens if you do nothing:**
78% of startups lose enterprise deals specifically because they lack compliance certifications. Without SOC 2, enterprise procurement teams will block your contracts at the security review stage — regardless of how strong your product is.

**What to do next:**
1. Do not attempt an audit yet
2. Conduct a formal gap assessment to prioritize controls by risk and audit impact
3. Begin with foundational policies — access control, incident response, and encryption are typically fastest to implement
4. Assign a compliance owner internally, even if part-time
5. Consider an implementation partner who provides engineers, not just software

**How QuickTrust helps:**
At this score range, QuickTrust provides a full-scope implementation engagement. Our team of Security and DevOps engineers builds your control environment from scratch — IAM, encryption, logging, policies, vendor processes — in your actual cloud infrastructure. You don't need to hire a security team. Typical clients at this stage are audit-ready in 8–10 weeks.

---

### 31–50: In Progress
**What this means:**
You have compliance awareness and some controls in place, but you have material gaps in multiple domains. You likely have informal processes that aren't consistently documented or enforced. An auditor reviewing your environment today would identify enough exceptions to issue a qualified opinion or recommend significant remediation before issuing a report.

**What to do next:**
1. Identify your two lowest-scoring domains and prioritize those first
2. Focus on making informal processes formal — documentation and evidence collection are often the fastest wins
3. Run a pre-audit readiness assessment to identify your highest-risk gaps
4. Implement continuous monitoring if you haven't already
5. Start collecting evidence now — retroactive evidence collection is a major audit-time bottleneck

**How QuickTrust helps:**
At this score range, QuickTrust clients typically engage our Certification Fast Track program. We conduct a formal gap assessment, build a prioritized remediation roadmap, and our engineers close your gaps — cloud configurations, policy documentation, SIEM setup, vendor risk workflows — while your team focuses on product. Most clients at this stage achieve audit readiness in 6–8 weeks.

---

### 51–65: Nearly Ready
**What this means:**
You're in good shape. Your foundational controls are in place and you have documented processes across most domains. The gaps that remain are likely in evidence collection rigor, consistency of enforcement, or specific technical controls that haven't been fully implemented. An auditor would likely be able to complete a review, but you'd receive findings that could impact your report.

**What to do next:**
1. Conduct a full evidence gap review — identify what you have vs. what an auditor will request
2. Focus on the domains where you scored 0 or 1 — these are your highest risk items
3. Implement automated evidence collection where possible to reduce audit-time burden
4. Schedule a pre-audit readiness call with your target auditor
5. Assign evidence ownership per control so nothing falls through the cracks at audit time

**How QuickTrust helps:**
At this score range, QuickTrust provides targeted implementation support and audit coordination. We close your remaining gaps, build your evidence package, and coordinate directly with your auditor. Our 100% audit pass rate across 100+ audits means you're not going into the room alone. Most clients at this stage complete their audit in 4–6 weeks.

---

### 66–80: Audit Ready
**What this means:**
Excellent. Your control environment is mature and consistently implemented. You have strong foundational evidence and documented processes across all eight domains. You are likely ready to engage an auditor and begin your SOC 2 examination.

**What to do next:**
1. Engage an accredited SOC 2 auditor and schedule your examination window
2. Confirm your evidence package is complete and organized per the auditor's request list
3. Conduct a final internal readiness review against the SOC 2 criteria
4. Establish a continuous monitoring and compliance maintenance program to prevent drift post-audit
5. Plan for SOC 2 Type II (if you've achieved Type I) — 6-month observation period planning

**How QuickTrust helps:**
At this score range, QuickTrust provides audit coordination and continuous compliance maintenance. We manage auditor communications, respond to RFIs, organize your evidence portal, and implement ongoing automation to keep your controls current year-round — so your next renewal audit is a fraction of the effort.

---

## Next Steps: Book Your Free 20-Minute Readiness Call

**Your score is a starting point, not a ceiling.**

Whether you scored 12 or 72, QuickTrust has helped companies at every stage achieve SOC 2 certification — in as little as 6 weeks, with a 100% audit pass rate across 100+ audits. Our engineers don't just tell you what to fix. They fix it — in your cloud, with your infrastructure, at a fraction of the cost of hiring in-house.

**What you get on the call:**
- A review of your scorecard results by a compliance engineer
- Identification of your top 3 highest-risk gaps
- A realistic timeline and effort estimate for your certification
- A custom scope recommendation (Type I vs. Type II, which frameworks to tackle first)
- No sales pressure — just a clear picture of where you stand

**Book your free 20-minute SOC 2 readiness call:**
[trust.quickintell.com](https://trust.quickintell.com)

---

*QuickTrust is an open-source, AI-powered GRC platform operated by GPT Innovations, Inc. We provide SOC 2, ISO 27001, HIPAA, PCI DSS, and custom framework certifications with implementation engineers included.*

*This scorecard is provided for informational purposes and does not constitute a formal audit or legal compliance assessment.*

---

## Related Reading

- [The Complete Guide to SOC 2 Compliance](/blog/pillar-soc2-complete-guide)
- [How Much Does a SOC 2 Audit Cost in 2026?](/blog/soc2-audit-cost-2026)

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "SOC 2 Readiness Scorecard: Assess Your Certification Readiness in 10 Minutes",
  "description": "SOC 2 readiness scorecard with 40 questions across 8 security domains mapped to Trust Services Criteria. Assess your certification readiness in 10 minutes and get a prioritized action plan.",
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
