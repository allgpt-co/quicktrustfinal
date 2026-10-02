---
meta_description: "A working SOC 2 compliance checklist covering system boundary, Type I or Type II, Trust Services Criteria, policies, controls, evidence and audit steps."
target_keyword: "soc 2 compliance checklist"
secondary_keywords: "soc 2 checklist, soc 2 requirements checklist, soc 2 audit checklist, soc 2 readiness checklist"
published: true
author: QuickTrust Editorial
publish_date: 2026-10-02
last_updated: 2026-10-02
---
# SOC 2 Compliance Checklist: Scope, Controls, Evidence and Audit Steps

A SOC 2 report is an attestation issued by a licensed CPA firm. The auditor examines whether your controls are suitably designed and, for a Type II report, whether they operated effectively over a review period, measured against the AICPA Trust Services Criteria. The work that leads up to the report is mostly ordinary security engineering and documentation, but it has to be scoped, evidenced and sequenced correctly or the audit stalls.

This checklist follows the order in which the work actually happens. Copy it into your project tracker, assign a named owner to every line, and do not move to fieldwork until the readiness section is clean.

## Step 1: Define the service and system boundary

Everything else depends on this decision. The system description in your report defines what the auditor tests, what customers can rely on, and what you can leave out.

- [ ] Name the service or services the report covers. If you run several products, decide whether all of them are in scope or only one.
- [ ] List the infrastructure that delivers the service: cloud accounts, regions, clusters, databases and managed services.
- [ ] List the software components, including internal tools that touch customer data.
- [ ] Identify the people in scope: engineering, operations, support, and anyone with production access.
- [ ] Identify the data in scope and classify it. Customer data, authentication secrets, logs and backups all count.
- [ ] Document subservice organizations, such as your cloud provider, and agree the carve-out or inclusive method with your auditor.
- [ ] Write a draft system description. The auditor will refine it, but you need a working version to scope everything below.

## Step 2: Choose Type I or Type II with the auditor

- [ ] Decide whether a Type I report (controls designed and in place at a point in time) or a Type II report (controls operating over a review period) fits your commercial need.
- [ ] If you choose Type II, agree the review period start date with the auditor before you begin collecting evidence. Evidence from before the period does not count.
- [ ] Confirm whether a Type I first and a Type II later is the right path, or whether you go straight to Type II.
- [ ] Record the decision and the date in writing.

The two report types differ in timing, effort and what customers accept. See [SOC 2 Type I vs Type II](/blog/soc2-type1-vs-type2) for a fuller treatment.

## Step 3: Select the Trust Services Criteria

There are five Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality and Privacy. Security is the required one and is often called the Common Criteria. The other four are optional and belong in scope only when a customer contract or your own service commitments call for them.

- [ ] Confirm Security is in scope. It always is.
- [ ] Decide on Availability based on whether you make uptime commitments.
- [ ] Decide on Confidentiality based on whether you handle confidential customer information under contract.
- [ ] Decide on Processing Integrity based on whether customers rely on the accuracy and completeness of your processing.
- [ ] Decide on Privacy based on whether you collect personal information directly from individuals and make privacy commitments.
- [ ] Map each selected criterion to the controls that will satisfy it.

## Step 4: Build the policy set

Policies are the written commitments your controls enforce. Auditors expect them to be approved, versioned, communicated and reviewed on a schedule.

- [ ] Information security policy
- [ ] Access control policy
- [ ] Change management policy
- [ ] Incident response policy and plan
- [ ] Business continuity and disaster recovery policy
- [ ] Risk assessment and risk management policy
- [ ] Vendor and third-party risk management policy
- [ ] Data classification and handling policy
- [ ] Acceptable use policy
- [ ] Logging and monitoring policy
- [ ] Encryption and key management policy
- [ ] Human resources security policy covering onboarding, offboarding and background checks
- [ ] Every policy has an owner, an approval record, a version number and a review date
- [ ] Every policy has been acknowledged by the staff it applies to, with a record

If you are not sure where your current documentation falls short, a [policy gap analysis](/solutions/policy-gap-analysis) against the criteria is the quickest way to find out.

## Step 5: Implement controls by area

The policy says what you commit to. The control is the mechanism that makes it true. Work through each area and confirm the control exists, is enforced technically where possible, and produces evidence on its own.

### Access control

- [ ] Single sign-on or a central identity provider for production and business systems
- [ ] Multi-factor authentication enforced for all staff and for privileged access
- [ ] Role-based access with least privilege, documented per system
- [ ] Access request and approval workflow with records
- [ ] Periodic access reviews with sign-off and remediation of findings
- [ ] Offboarding procedure that removes access on departure, with evidence of timing

### Change management

- [ ] Version control for all production code and infrastructure configuration
- [ ] Peer review required before merge, enforced by branch protection
- [ ] Automated testing in the pipeline
- [ ] Separation between who writes a change and who approves deployment to production
- [ ] Emergency change procedure with retrospective approval

### Logging and monitoring

- [ ] Centralized logging for production systems, authentication events and administrative actions
- [ ] Log retention period defined in policy and enforced
- [ ] Alerting for security-relevant events with an on-call owner
- [ ] Vulnerability scanning of infrastructure and dependencies with tracked remediation
- [ ] Logs protected from tampering and limited to authorized viewers

### Vendor management

- [ ] Inventory of vendors with access to customer data or production systems
- [ ] Risk rating per vendor
- [ ] Security review before onboarding critical vendors, with records
- [ ] Collection of vendor SOC 2 reports or equivalent assurance, and review of any exceptions
- [ ] Re-review of critical vendors on a defined cadence

### Incident response

- [ ] Documented incident response plan with roles, severity levels and escalation paths
- [ ] Customer and regulator notification procedures
- [ ] Incident log with root cause and corrective actions
- [ ] At least one tabletop exercise or real incident review, with a record

### Business continuity and disaster recovery

- [ ] Backups configured, encrypted and tested by restoration, with results recorded
- [ ] Recovery time and recovery point objectives defined per system
- [ ] Disaster recovery plan tested, with a record of the test and follow-up actions

### Risk assessment

- [ ] Formal risk assessment performed and documented, with a stated methodology
- [ ] Risk register with owners, likelihood, impact and treatment decisions
- [ ] Risks tied to the controls that mitigate them
- [ ] Reassessment on a defined cadence and after significant changes

### Security awareness

- [ ] Security awareness training at onboarding and on a recurring schedule
- [ ] Completion records per employee
- [ ] Background checks performed in line with policy and local law, with records

## Step 6: Evidence per control, with owner and period

Auditors do not test policies. They test evidence. Every control above needs to produce something a stranger can inspect, and for a Type II report that something must come from inside the review period.

Build an evidence matrix with one row per control and these columns:

| Column | What goes in it |
| --- | --- |
| Control ID and description | Links back to the criterion it satisfies |
| Evidence type | Screenshot, export, log sample, signed document, ticket, configuration file |
| Source system | Where the evidence comes from: identity provider, cloud console, ticketing, HR system |
| Owner | One named person accountable for producing it |
| Frequency | Once, monthly, quarterly, per event, or continuous |
| Period covered | The dates the evidence must span |
| Status | Not started, collected, reviewed, accepted |

- [ ] Every control has at least one evidence row
- [ ] Every evidence row has a named owner, not a team
- [ ] Recurring evidence has a schedule and a reminder
- [ ] Evidence is stored in one place with access control and version history
- [ ] Sampled evidence, such as access reviews or change tickets, covers the whole review period rather than just the end of it

The [audit evidence checklist](/blog/audit-evidence-checklist) lists what auditors commonly request for each control area.

## Step 7: Readiness review

A readiness review is a dry run of the audit, done by someone who did not build the controls. Its purpose is to find gaps before the auditor does.

- [ ] Walk every control with its owner and inspect the evidence as an auditor would
- [ ] Confirm policies are approved, current and acknowledged
- [ ] Confirm the system description matches reality, including recent architecture changes
- [ ] Identify controls with no evidence, stale evidence or evidence outside the period
- [ ] Record each gap with an owner and a target date
- [ ] Close gaps before fieldwork, or agree with the auditor how to treat them
- [ ] Repeat the review once gaps are closed

If you have not done this before, the [SOC 2 readiness assessment](/tools/soc-2-readiness-assessment) is a structured starting point.

## Step 8: Auditor selection and fieldwork

- [ ] Shortlist licensed CPA firms with SOC 2 experience in your industry and technology stack
- [ ] Ask each firm about sampling approach, schedule, fee structure and who will actually perform the work
- [ ] Confirm independence: the firm that issues the opinion cannot have designed your controls
- [ ] Sign the engagement letter and agree the fieldwork schedule
- [ ] Provide the system description, policies and evidence matrix before fieldwork begins
- [ ] Assign a single internal point of contact for auditor requests, and track every request in one list
- [ ] Review draft findings and provide management responses where exceptions are noted

Fee structures vary widely between firms. [SOC 2 audit costs](/blog/soc2-audit-cost-2026) explains the factors that shape quotes so you can compare proposals sensibly.

## Step 9: After the report

The report covers a point in time or a period of time. The controls have to keep operating the moment it is issued, because the next review period starts immediately.

- [ ] Read the report in full, including any exceptions and the auditor's description of tests performed
- [ ] Prepare a remediation plan for every exception, with owners
- [ ] Decide how the report is shared: under NDA, through a trust portal, or on request
- [ ] Update the system description for any changes planned in the coming period
- [ ] Keep the evidence calendar running without a gap
- [ ] Schedule the next readiness review and the next audit

## Where QuickTrust fits

QuickTrust is a compliance platform combined with scoped implementation engineering. The platform tracks controls, policies and evidence. Security and DevOps engineers do the implementation work described above, such as configuring identity, logging, change controls and evidence pipelines, within a scope agreed per engagement. Pricing is quote-based. QuickTrust does not issue the audit opinion; a licensed CPA firm that you select does that. Details are on the [SOC 2 compliance page](/soc-2-compliance).

## Frequently asked questions

### Do I need all five Trust Services Criteria?

No. Security is required in every SOC 2 report. Availability, Processing Integrity, Confidentiality and Privacy are optional and should be included only when your service commitments or customer contracts call for them.

### Can I start collecting evidence before I pick an auditor?

You can and should start building controls and the evidence matrix early. For a Type II report, however, the review period start date is agreed with the auditor, and only evidence from within that period counts, so engage the auditor before you assume a period has begun.

### What is the difference between a policy and a control?

A policy is a written statement of what the organization commits to do. A control is the mechanism that enforces it, such as branch protection that blocks unreviewed merges. Auditors test whether controls operate, and they read policies to understand what the controls are meant to achieve.

### What happens if the auditor finds an exception?

The exception is described in the report along with management's response. A report with exceptions is still a valid report. What matters to customers is the nature of the exception and the credibility of the remediation plan.
