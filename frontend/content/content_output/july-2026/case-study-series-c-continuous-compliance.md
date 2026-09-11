---
meta_description: "Case study: How Vaultstream, a Series C data platform, fixed 11 SOC 2 audit findings and built a continuous compliance program across 4 engineering teams — recovering $6.2M in stalled pipeline in 90 days."
target_keyword: "continuous compliance, compliance program, soc 2 renewal"
secondary_keywords: "compliance at scale, multi-team compliance, soc 2 findings remediation, enterprise compliance"
word_count_target: 3500
published: true
author: QuickTrust Editorial
last_updated: 2026-02-28
---

# Case Study: How a Series C SaaS Company Built a Continuous Compliance Program Across 4 Teams — and Recovered $6.2M in Stalled Pipeline

**Company:** Vaultstream
**Stage:** Series C ($45M raised)
**Product:** Cloud data platform for financial services — data lake, analytics, and reporting for banks and asset managers
**Employees:** 280
**Engineering Teams:** 4 (Alpha, Beta, Gamma, Delta)
**Headquarters:** New York, NY
**QuickTrust Package:** Package 2 — Continuous Compliance Program

---

## The Situation: From Clean Audit to Compliance Debt in 18 Months

Vaultstream's compliance story started the way most startups' compliance stories start — clean, simple, and manageable. In their early days, when the company was 30 people operating out of a single office in Lower Manhattan, their first SOC 2 Type II audit was almost effortless. The founding team understood every system, every access point, every policy. Their original CISO, who had been employee number eight, knew where every piece of evidence lived because he had created most of it himself. The audit came back clean. No findings, no exceptions, no drama. The SOC 2 report went into the sales deck, enterprise prospects started converting, and Vaultstream's trajectory steepened.

Then the company grew. Series B brought headcount from 60 to 150. Series C pushed it past 280. The cloud data platform expanded from a single product to a suite — data lake ingestion, real-time analytics, regulatory reporting modules, and a customer-facing dashboard layer. The engineering organization split from one team into four: Team Alpha (core platform), Team Beta (analytics engine), Team Gamma (integrations and APIs), and Team Delta (customer-facing applications). Each team had its own tech lead, its own deployment pipeline, its own way of doing things.

The original CISO left at 120 employees. He wasn't replaced. His responsibilities were distributed — which in practice meant they were abandoned. Compliance ownership became "everyone and no one." There was no single person who could answer the question: "Are we compliant right now?" Nobody even knew whom to ask.

Evidence collection, once centralized, fragmented across four different systems. Team Alpha stored policies and procedures in Notion. Team Beta used Confluence for their documentation. Team Gamma relied on Slack threads and pinned messages for compliance-related discussions and approvals. Team Delta had a shared Google Drive folder that hadn't been reorganized since the company was 80 people. If an auditor asked for evidence of a specific control, the answer depended on which team owned that control — and sometimes, nobody was sure which team that was.

The SOC 2 renewal audit in Q1 landed like a grenade. The auditor, who had given Vaultstream clean reports for two consecutive years, surfaced 11 findings — formally, 11 exceptions in the examination report. The details were damning:

- **Access reviews** had not been conducted in eight months. The last documented review was from the previous May, covering fewer than half of the company's applications.
- **Three policies** — the Acceptable Use Policy, the Data Classification Policy, and the Incident Response Plan — referenced systems that had been decommissioned six to twelve months earlier. The policies described controls for infrastructure that no longer existed.
- **Encryption key rotation** was configured correctly in AWS KMS. The rotation schedule was set. The Lambda function that triggered the rotation was deployed. But a misconfigured cron job — a CloudWatch Events rule with an incorrect schedule expression — meant the rotation had not actually executed in six months. The configuration looked right. The reality was wrong.
- **Logging was enabled** across all production environments. CloudTrail, VPC Flow Logs, application-level logging — all active, all collecting data, all shipping to a centralized S3 bucket. But nobody was monitoring the logs. There were no alerting rules, no dashboards, no escalation paths. The logs existed in the same way a fire alarm exists when no one has connected it to the monitoring station — technically present, functionally useless.

Eleven findings total. For a company selling a data platform to banks and asset managers — institutions that take security posture seriously enough to make it a contract requirement — 11 findings was not a minor issue. It was an existential threat to the sales pipeline.

And that threat materialized the same quarter. VP of Sales Rachel Torres escalated to the CEO: three enterprise deals, representing $6.2 million in combined annual contract value, had stalled. The reason was not price, not product fit, not competition. It was security questionnaire responses. Different Vaultstream employees from different teams had given contradictory answers to the same security questions. One prospect — a $2.8 million deal with a mid-tier regional bank — had received two different answers about data retention policies from two different Vaultstream employees, submitted three weeks apart. The bank's security team flagged the inconsistency. The deal froze.

CEO Amir Hassan brought the situation to the board. The board's response was unambiguous: "Compliance isn't a project — it's a program. Fix this systematically or we'll find someone who will." The message was clear. Another point-in-time remediation sprint would not be accepted. The board wanted a program — something durable, something that would scale, something that would prevent the same conversation from happening again in twelve months.

---

## The Challenge: Seven Problems, Not One

When Vaultstream reached out to QuickTrust, the initial ask was straightforward: "Help us remediate 11 SOC 2 findings." Within the first discovery call, it became clear that the 11 findings were symptoms, not the disease. The actual challenges were structural:

**No single owner for compliance across four teams.** Each team had informal compliance responsibilities, but no one had formal accountability. When Team Gamma's integration with a third-party logging provider changed, nobody updated the relevant policy. When Team Alpha decommissioned a legacy authentication service, nobody removed it from the Incident Response Plan. Ownership gaps meant control gaps.

**Evidence scattered across four different systems.** Notion, Confluence, Slack, Google Drive. An auditor requesting evidence for a single control might need to look in three different places — assuming someone remembered where the evidence was stored. In several cases, evidence existed but could not be located during the audit window, which functionally meant it did not exist.

**Eleven SOC 2 findings requiring remediation before re-audit.** Each finding needed root cause analysis, remediation, evidence of remediation, and validation. Some were quick fixes. Others — like the log monitoring gap — required new tooling, new processes, and new ownership assignments.

**Questionnaire responses inconsistent across teams.** With no single source of truth for security posture, every questionnaire was answered from memory by whoever happened to receive it. Four teams meant four different versions of the truth.

**ISO 27001 needed for European banking customers.** Vaultstream's expansion into European financial services markets introduced a new requirement. Several prospects required ISO 27001 certification as a contractual prerequisite. This was not on anyone's roadmap.

**Board demanding an ongoing program, not another point-in-time engagement.** The board had explicitly rejected the "hire a consultant, fix the findings, move on" approach. They wanted evidence of a sustainable compliance function.

**Engineering teams resistant to compliance work.** The previous audit had been disruptive — two weeks of engineers pulling screenshots, answering auditor questions, and searching Slack history for approval evidence. The engineering teams associated "compliance" with "everything stops." Team leads were openly skeptical that this time would be different.

---

## Why QuickTrust's Continuous Compliance Program

This is the key distinction: Vaultstream did not need QuickTrust's Package 1 (Certification Sprint). Package 1 is designed for companies pursuing their first certification — a focused, time-bound engagement that gets you from zero to SOC 2 or ISO 27001. Vaultstream already had SOC 2. What they had lost was the ability to maintain it.

**Vaultstream needed Package 2 — the Continuous Compliance Program.** This is QuickTrust's only offering designed for companies that need a system, not a sprint. The scope is fundamentally different:

QuickTrust proposed a four-phase engagement:

1. **Immediate remediation** of all 11 SOC 2 findings, triaged by severity, with root cause analysis to prevent recurrence.
2. **Build a unified compliance program** across all four engineering teams — with control ownership, centralized evidence collection, automated monitoring, and a single source of truth for security posture.
3. **ISO 27001 certification** built on the SOC 2 foundation, leveraging control overlap to minimize incremental effort.
4. **Ongoing continuous compliance** with quarterly reviews, automated evidence collection, board-level reporting, and renewal audit coordination — not as a project with an end date, but as a managed program.

To coordinate the engagement, QuickTrust brought in Marcus Bell from its virtual CISO bench as interim CISO. Bell would serve as the single point of accountability that Vaultstream had been missing since their original CISO departed — the person who could answer "are we compliant right now?" at any moment, for any framework, across all four teams.

The proposal was approved by the board within a week.

---

## Implementation

### Phase 1: Emergency Remediation (Weeks 1-6)

The first priority was stopping the bleeding. Marcus Bell and the QuickTrust team triaged all 11 SOC 2 findings by severity, factoring in both audit impact and business risk (specifically, the $6.2M in stalled pipeline).

**Access Reviews**

The access review gap was the highest-priority finding. Vaultstream had 280 employees and contractors across 47 applications managed through Okta. The last documented access review was eight months old and had only covered 19 of those 47 applications.

QuickTrust implemented automated quarterly access reviews via Okta's API. The first comprehensive review — covering all 280 users across all 47 applications — uncovered significant issues:

- **23 orphaned accounts** — former employees and contractors whose Okta accounts had been deactivated but whose access to downstream applications had not been fully revoked. In 6 cases, direct application credentials (not federated through Okta) remained active.
- **8 privilege escalations** — current employees with access levels beyond their job function. Three were engineers who had been granted temporary admin access during an incident and never had it revoked. Five were role changes where the new role required different (not additional) access, but the old access was never removed.

All 23 orphaned accounts were remediated within the first week. All 8 privilege escalations were corrected within two weeks, after validation with each employee's manager.

**Policy Refresh**

QuickTrust conducted a full review of all 14 compliance-relevant policies. Findings:

- 4 decommissioned systems were referenced across 7 policies. References were removed and replaced with documentation of current systems.
- 3 new systems added in the previous 18 months — a new CI/CD pipeline (GitHub Actions, replacing Jenkins), a new secrets management solution (HashiCorp Vault), and a new customer data warehouse (Snowflake) — were not covered by any existing policy. Policies were updated to include these systems.
- All 14 policies were versioned, assigned owners, and placed on an annual review cadence.

**Encryption Key Rotation**

The root cause was precise and instructive. The AWS Lambda function responsible for triggering KMS key rotation was correctly implemented. The CloudWatch Events rule that invoked the Lambda was configured with a cron expression that contained a syntax error — a missing field that caused the rule to never trigger. The configuration had passed a visual review during the previous audit because it looked correct at a glance. It had never been tested end-to-end.

QuickTrust fixed the cron expression, tested rotation across all 3 KMS keys in production, and implemented a CloudWatch alarm that fires if any KMS key has not been rotated within the expected window. The alarm routes to PagerDuty, ensuring that a rotation failure is treated as an operational incident, not a compliance observation discovered months later.

**Log Monitoring**

Logging without monitoring is security theater. Vaultstream had invested in comprehensive log collection — CloudTrail, VPC Flow Logs, application logs, database audit logs — but had never built the monitoring layer on top of it.

QuickTrust deployed Datadog as a SIEM solution with 47 detection rules covering:

- Unauthorized access attempts (brute force, credential stuffing patterns)
- Privilege escalation events
- Configuration changes to security-relevant resources (IAM policies, security groups, KMS keys, S3 bucket policies)
- Data exfiltration indicators (unusual data transfer volumes, access to sensitive S3 buckets from new IP ranges)
- Compliance-specific events (access review completions, policy acknowledgments, key rotation events)

All detection rules were configured with escalation paths through PagerDuty, with severity-based routing to the appropriate on-call engineer or security contact.

**Change Management**

Vaultstream had an informal change management process — pull requests required at least one approval — but it was not standardized across teams and was not documented in a way that satisfied SOC 2 requirements.

QuickTrust formalized a Change Advisory Board (CAB) process integrated directly with the existing GitHub PR workflow. Changes were categorized as standard, normal, or emergency. Standard changes (pre-approved types) could proceed with standard PR approval. Normal changes required CAB review, implemented as a required GitHub review from a designated CAB reviewer. Emergency changes had a defined break-glass process with mandatory post-incident documentation. The process was identical across all four engineering teams — the first compliance process at Vaultstream that operated consistently across team boundaries.

**Vendor Management**

QuickTrust re-assessed all 62 of Vaultstream's vendors against a standardized risk framework. Results:

- 14 vendors had expired or missing SOC 2 reports. QuickTrust requested updated reports from all 14; 11 provided current reports, 2 provided alternative evidence (ISO 27001 certificates), and 1 was flagged for replacement.
- 3 vendors required updated Business Associate Agreements (BAAs) reflecting changes in data handling practices.
- All vendor assessments were documented in the centralized evidence repository with annual reassessment dates.

**Re-Audit Result**

Six weeks after engagement start, Vaultstream underwent a SOC 2 Type II re-examination. The result: **clean report — unqualified opinion, zero findings.** Every one of the 11 original exceptions was remediated with documented evidence of both the fix and the systemic controls to prevent recurrence.

---

### Phase 2: Compliance Program Build (Weeks 4-12, Overlapping with Phase 1)

Remediating findings was necessary but insufficient. The board had been explicit: build a program, not a patch. Phase 2 started in Week 4, running parallel to the final stages of Phase 1, and focused on building the infrastructure for continuous compliance.

**Control Ownership Matrix**

This was the foundational deliverable. QuickTrust mapped all 47 SOC 2 controls to individual owners — not teams, individuals. Twelve people across the four engineering teams were assigned as control owners. Each owner received:

- A documented description of their controls and the evidence required
- A defined evidence collection cadence (daily automated, weekly manual, quarterly review)
- An escalation path for control failures or evidence gaps
- A quarterly review meeting with Marcus Bell to validate control health

The principle was simple and non-negotiable: **every control has exactly one owner.** Not a team. Not "engineering." A person with a name, a Slack handle, and a calendar reminder.

**Centralized Evidence Library**

The migration from four ad-hoc systems to a single evidence repository was the most operationally disruptive change — and the most impactful. All compliance evidence was consolidated into a structured repository with consistent tagging:

- **Control ID** (mapped to SOC 2 and ISO 27001 control numbers)
- **Evidence type** (configuration screenshot, log export, policy document, access review report, vendor assessment)
- **Collection date** (automated timestamp)
- **Owner** (linked to control ownership matrix)
- **Status** (current, under review, expired, archived)

The repository eliminated the fundamental problem: when an auditor asks for evidence of Control CC6.1, there is exactly one place to look, and the evidence is either there or it is not. No more searching four systems. No more "I think Team Beta has that in Confluence somewhere."

**Automated Evidence Collection**

Manual evidence collection is the reason engineering teams dread audit season. QuickTrust automated evidence collection for every control where automation was feasible:

- **AWS Config:** 24 custom rules monitoring infrastructure compliance — encryption at rest, encryption in transit, public access restrictions, logging configuration, IAM policy compliance. Evidence collected continuously and stored automatically.
- **GitHub Webhooks:** Every pull request, every approval, every merge, every deployment — captured automatically as change management evidence. No engineer action required.
- **Okta API Integration:** Access review reports generated automatically on a quarterly cadence. User provisioning and deprovisioning events captured in real time.
- **Datadog API:** Monitoring and alerting evidence — alert configurations, incident response times, resolution documentation — pulled automatically.
- **Automated Screenshot Collection:** For controls that required visual evidence of manual processes (such as physical security configurations or third-party dashboard states), QuickTrust implemented automated screenshot collection on defined schedules.

The result: roughly 80% of evidence collection required zero engineering effort. The remaining 20% (manual controls, vendor assessments, policy reviews) was assigned to specific owners with calendar-based reminders and escalation if deadlines were missed.

**Policy Lifecycle Management**

Policies were moved into version control with a defined lifecycle:

- Annual review cadence for all policies (with 30-day advance notification to policy owners)
- Defined approval workflow (policy owner drafts, security reviews, legal reviews where applicable, executive sign-off)
- Version history with change tracking
- Automated distribution and acknowledgment tracking for policies requiring employee sign-off

**Questionnaire Response System**

QuickTrust built a single source of truth for security questionnaire answers. Every question Vaultstream had ever received — from prospects, from customers, from auditors — was cataloged, answered authoritatively, and maintained in a searchable system.

When a new questionnaire arrived, the sales team could pull pre-approved answers instead of forwarding questions to whichever engineer was available. If a question had no pre-approved answer, it was routed to the appropriate control owner for a definitive response, which then became the canonical answer for all future questionnaires.

This system directly addressed the contradiction problem that had stalled $6.2M in pipeline. There was now exactly one answer to every security question — not four.

**Compliance Dashboard**

Marcus Bell built a board-level compliance dashboard that provided real-time visibility into:

- **Compliance posture score** — an aggregate metric reflecting the percentage of controls with current, validated evidence
- **Open items** — any control gaps, overdue evidence, or unresolved findings
- **Upcoming audit dates** — SOC 2 renewal, ISO 27001 surveillance audit, any customer-required assessments
- **Risk register status** — all identified risks, their treatment plans, and current residual risk levels

The dashboard transformed compliance reporting from "we think we're fine" to "here are the numbers, updated daily."

---

### Phase 3: ISO 27001 (Months 3-5, Parallel with Ongoing SOC 2)

With the SOC 2 program stabilized and the continuous compliance infrastructure in place, QuickTrust initiated ISO 27001 certification — a new requirement driven by Vaultstream's expansion into European banking markets.

The advantage of building ISO 27001 on a mature SOC 2 foundation was substantial. QuickTrust's gap analysis showed that **72% of existing SOC 2 controls mapped directly to ISO 27001 Annex A controls.** The incremental effort was focused on:

- **Information Security Management System (ISMS) documentation** — the management framework ISO 27001 requires but SOC 2 does not
- **Risk assessment methodology** — ISO 27001's risk-based approach required a formal risk assessment. QuickTrust identified and treated 56 risks across the organization, categorized by likelihood and impact, with documented treatment plans.
- **Additional Annex A controls** — controls not covered by SOC 2, primarily in areas like physical security, supplier relationships, and business continuity
- **Internal audit and management review** — ISO 27001's required governance processes

QuickTrust coordinated the entire certification process: internal audit, management review, Stage 1 (documentation review), and Stage 2 (implementation audit). Marcus Bell served as the management representative throughout.

**Vaultstream achieved ISO 27001 certification by Month 5.** The certification body noted the maturity of the ISMS relative to a first-time certification — a direct result of building on the compliance program infrastructure rather than treating ISO 27001 as a standalone project.

---

### Phase 4: Continuous Operations (Ongoing)

Phase 4 is not a phase in the traditional sense — it is the steady state. This is what makes Package 2 fundamentally different from a certification sprint. The compliance program continues to operate with the following cadence:

- **Quarterly access reviews** — fully automated via Okta, with exceptions flagged for manual review
- **Monthly evidence collection validation** — automated checks that all expected evidence has been collected, with alerts for gaps
- **Quarterly compliance program review** — Marcus Bell presents compliance posture, open items, risk register updates, and upcoming audit preparation to the board
- **Annual risk assessment update** — full reassessment of the risk register, incorporating new systems, new vendors, new markets, and evolving threat landscape
- **SOC 2 and ISO 27001 renewal audit coordination** — QuickTrust manages the auditor relationship, evidence preparation, and audit logistics
- **New vendor assessment and onboarding compliance checks** — every new vendor is assessed against the risk framework before contract execution
- **Incident response tabletop exercises** — semi-annual exercises testing the incident response plan with realistic scenarios, involving all four engineering teams

The program runs. It does not require a crisis to trigger activity. It does not depend on any single person remembering to do something. It is a system.

---

## The Results

The numbers tell the story:

| Metric | Before | After |
|---|---|---|
| SOC 2 findings | 11 | 0 |
| ISO 27001 | Not certified | Certified (Month 5) |
| Questionnaire response time | 3 weeks | 2 days |
| Orphaned accounts | 23 discovered | All remediated |
| Vendors assessed | Ad hoc | 62 (100%) |
| Control ownership | Undefined | 47 controls, 12 owners, zero unowned |
| Stalled pipeline | $6.2M frozen | All 3 deals closed within 90 days |
| Board compliance questions | Recurring concern | "No further questions" at first program review |
| Next renewal audit | N/A | Zero findings (clean report) |

The $6.2M in recovered pipeline is the headline number, but the structural outcomes matter more. Vaultstream now has a compliance program that operates continuously, scales with hiring, and survives personnel changes. The next CISO — whenever Vaultstream hires a permanent one — will inherit a functioning system, not a pile of Notion pages and Slack threads.

---

## What They Said

> "Vaultstream didn't have a compliance problem. They had a compliance program absence. The controls mostly existed — they just weren't owned, monitored, or maintained. We didn't rebuild their security. We built the system that keeps it running."
>
> — **Marcus Bell, Interim CISO (QuickTrust vCISO)**

---

> "I stood in front of the board and said 'we have a compliance program now' — and for the first time, I actually meant it. Not a spreadsheet, not a dashboard, not a PDF. A program with owners, automation, and continuous evidence. The board hasn't asked me about compliance risk since."
>
> — **Amir Hassan, CEO, Vaultstream**

---

> "My teams used to dread audit season. It was two weeks of dropping everything to find screenshots and answer auditor questions. Now evidence collection is automated, each team has a compliance owner, and our last audit required exactly zero engineering disruption."
>
> — **Kira Nakamura, VP Engineering, Vaultstream**

---

> "The three deals that were stalled? Closed within 90 days. But the bigger win is what happened after — our questionnaire response time went from three weeks to two days. We're winning deals faster because prospects can't find gaps in our security posture."
>
> — **Rachel Torres, VP Sales, Vaultstream**

---

## Key Lessons

**Compliance doesn't scale automatically.** A program that works at 30 people will break at 200. The controls that felt intuitive when everyone sat in the same room become invisible when the company spans four teams, four documentation systems, and four different ways of doing things. Growth without compliance program investment creates compliance debt — and compliance debt compounds.

**Control ownership is the single most important compliance investment.** Unowned controls are unmonitored controls. Unmonitored controls are failing controls. The difference between Vaultstream's 11-finding audit and their zero-finding re-audit was not new technology or new policies. It was assigning 47 controls to 12 named individuals who were accountable for keeping those controls operational. Ownership is not glamorous. It is the foundation.

**Evidence scattered across four systems is worse than no evidence.** When evidence does not exist, you know you have a problem. When evidence exists in four different places, you think you are covered — until an auditor asks for it and you cannot produce it within the audit window, or worse, two people produce contradictory evidence from two different systems. Centralization is not optional at scale.

**Continuous compliance costs less than point-in-time remediation fire drills.** Vaultstream's emergency remediation in Phase 1 consumed six weeks of concentrated effort across multiple teams. The ongoing continuous compliance program requires a fraction of that effort, distributed evenly across the year. The total cost of continuous compliance is lower than the cost of annual remediation sprints — and the risk exposure between sprints drops to near zero.

**Board-level reporting transforms compliance from a cost center to a risk management function.** When the board sees a compliance posture score updated daily, a risk register with treatment plans, and quarterly trend data, compliance becomes a managed risk — not an unknown one. The conversation shifts from "are we compliant?" to "here is our compliance posture, here are the risks, here is what we are doing about them." That shift changes how the board, the CEO, and the entire organization think about compliance investment.

---

## What's Next for Vaultstream

Vaultstream's compliance program continues to expand in line with business growth:

- **PCI DSS certification** is now on the roadmap. Several banking customers have indicated that PCI DSS will become a contractual requirement as Vaultstream's platform begins handling payment-adjacent data. QuickTrust is conducting a scoping assessment to determine the applicable PCI DSS requirements and the incremental controls needed beyond the existing SOC 2 and ISO 27001 foundation.

- **DORA (Digital Operational Resilience Act) compliance** is under evaluation for Vaultstream's EU financial services expansion. DORA introduces specific requirements around ICT risk management, incident reporting, digital operational resilience testing, and third-party risk management that go beyond ISO 27001. QuickTrust is mapping Vaultstream's current controls against DORA requirements to identify gaps.

The compliance program that QuickTrust built is designed to absorb new frameworks without starting from scratch. The control ownership matrix, the centralized evidence library, the automated collection infrastructure — all of it extends. That is the difference between a program and a project.

---

> **Build a compliance program that scales with your company.**
>
> QuickTrust's Continuous Compliance Program gives you control ownership, automated evidence collection, and ongoing audit readiness — so compliance works as well at 500 people as it did at 50.
>
> **[Talk to a Program Lead](https://quicktrustapp.com)**
