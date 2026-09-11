---
meta_description: "What is a SOC 1 report? Learn everything about SOC 1 audits — who needs them, what they cover, Type 1 vs Type 2, costs, and how SOC 1 differs from SOC 2. Plain-English guide for tech companies."
target_keyword: "what is soc 1"
secondary_keywords: "soc 1 report, soc 1 audit, soc 1 type 1, soc 1 type 2, what is a soc 1 report, soc 1 meaning"
word_count_target: 3000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-19
---

# What Is SOC 1? The Complete Guide to SOC 1 Reports for Service Organizations

A SOC 1 report (System and Organization Controls 1) is an independent audit report that evaluates a service organization's internal controls relevant to its clients' financial reporting. Issued by a licensed CPA firm under the SSAE 18 attestation standard, a SOC 1 report gives your clients — and their auditors — assurance that your organization will not introduce errors, misstatements, or fraud risks into their financial statements.

If you have heard of SOC 2 but are unclear on where SOC 1 fits, you are not alone. SOC 1 and SOC 2 are both part of the AICPA's System and Organization Controls framework, but they serve fundamentally different purposes. SOC 2 evaluates how you protect customer data across five Trust Service Criteria (Security, Availability, Processing Integrity, Confidentiality, and Privacy). SOC 1 evaluates how your service affects your clients' financial reporting — their general ledger, their revenue recognition, their payroll records, their transaction processing accuracy.

The distinction matters because choosing the wrong report wastes time and money — and fails to satisfy the auditors who actually requested it.

---

## TL;DR — Key Takeaways

- A SOC 1 report examines your **internal controls over financial reporting (ICFR)** — not your security posture or data protection practices
- SOC 1 is governed by the **SSAE 18** standard in the United States and **ISAE 3402** internationally
- There are two types: **SOC 1 Type 1** (point-in-time design assessment) and **SOC 1 Type 2** (period-of-time operating effectiveness evaluation)
- Companies that process transactions, handle payroll, manage funds, or perform accounting functions on behalf of clients almost always need a SOC 1
- SOC 1 is **not** interchangeable with SOC 2 — enterprise procurement teams, financial auditors, and regulators know the difference
- A SOC 1 audit typically costs between **$20,000 and $100,000+**, depending on scope, organization size, and report type

---

## What Is a SOC 1 Report?

A SOC 1 report is a formal attestation report issued by an independent CPA firm that evaluates the design and, in the case of a Type 2 report, the operating effectiveness of a service organization's controls that are relevant to user entities' internal control over financial reporting (ICFR).

In plain English: if your company provides a service that touches your clients' financial data — processing their payments, running their payroll, reconciling their accounts, managing their benefits — your clients' auditors need assurance that your systems and processes will not introduce errors into their financial statements. A SOC 1 report is how you provide that assurance.

### The Standards Behind SOC 1

In the United States, SOC 1 reports are governed by **SSAE 18** (Statement on Standards for Attestation Engagements No. 18), issued by the AICPA. SSAE 18 replaced SSAE 16 in May 2017 and introduced strengthened requirements around risk assessment, complementary subservice organization controls (CSOCs), and monitoring.

Internationally, the equivalent standard is **ISAE 3402** (International Standard on Assurance Engagements 3402), published by the International Auditing and Assurance Standards Board (IAASB). If your clients operate internationally or their auditors follow international standards, they may request an ISAE 3402 report. Many CPA firms issue dual-standard reports that satisfy both SSAE 18 and ISAE 3402 simultaneously.

### Who Receives a SOC 1 Report?

SOC 1 reports are restricted-use documents. Unlike a SOC 3 report (which is a general-use summary), a SOC 1 report is intended for:

- **User entities** — your clients whose financial reporting depends on your service
- **User entity auditors** — the CPA firms auditing your clients' financial statements
- **Management of the service organization** — your own leadership team

SOC 1 reports are not designed for public distribution. Clients typically receive them under NDA, and their auditors use them as part of their own audit procedures.

---

## What Does SOC 1 Stand For?

SOC stands for **System and Organization Controls**. This is the current terminology adopted by the AICPA in 2017. Prior to that, SOC stood for "Service Organization Controls."

The "1" designates this as the first of three SOC report types:

- **SOC 1** — Controls relevant to user entities' financial reporting
- **SOC 2** — Controls relevant to security, availability, processing integrity, confidentiality, and privacy ([learn more about SOC 2](/glossary/what-is-soc2))
- **SOC 3** — A general-use summary of a SOC 2 report, designed for public distribution

### The SAS 70 Connection

Before the SOC framework existed, service organizations that needed to demonstrate controls over financial reporting obtained a **SAS 70** report (Statement on Auditing Standards No. 70). SAS 70 was the industry standard from 1992 until 2011, when the AICPA introduced the SOC framework and replaced SAS 70 with SSAE 16 (later superseded by SSAE 18).

If you encounter references to SAS 70 in vendor questionnaires or legacy procurement documents, the modern equivalent is a SOC 1 report. SAS 70 is no longer issued by CPA firms.

---

## What Does a SOC 1 Report Cover?

A SOC 1 report covers **internal controls over financial reporting (ICFR)** — specifically, the controls within a service organization that could affect the accuracy, completeness, and validity of financial transactions processed on behalf of client organizations.

### Control Objectives in a SOC 1

Unlike SOC 2, which uses the AICPA's predefined Trust Service Criteria, SOC 1 control objectives are **custom-defined** by the service organization and its auditor based on the specific services provided. This means two SOC 1 reports from different companies will have different control objectives.

Common categories of SOC 1 control objectives include:

**Transaction Processing Controls**
- Transactions are authorized, complete, accurate, and processed in a timely manner
- Input data is validated before processing
- Output reports are accurate and distributed to authorized recipients only
- Error handling and exception processing procedures are documented and followed

**Access Controls**
- Logical access to systems and applications that process financial data is restricted to authorized personnel
- User access is provisioned, modified, and terminated following documented procedures
- Privileged access is limited and monitored

**Change Management Controls**
- Changes to applications and systems that process financial data are authorized, tested, and approved before deployment
- Emergency changes follow documented exception procedures

**Data Integrity and Reconciliation Controls**
- Data transmissions between systems are complete and accurate
- Reconciliations are performed to verify data integrity between source and target systems
- Discrepancies are investigated and resolved in a timely manner

**Operational Controls**
- Backup and recovery procedures are in place and tested regularly
- Job scheduling and batch processing controls ensure complete and timely execution
- Physical and environmental controls protect computing infrastructure

**Segregation of Duties**
- Incompatible functions are separated (e.g., the person who initiates a transaction cannot also approve it)
- Compensating controls exist where perfect segregation is not feasible

The specific control objectives in your SOC 1 report will depend entirely on what your service does. A payroll processor will have control objectives around payroll calculation accuracy, tax withholding, and pay distribution. A payment gateway will have control objectives around transaction authorization, settlement accuracy, and funds transfer completeness.

---

## SOC 1 Type 1 vs SOC 1 Type 2

Like SOC 2, SOC 1 reports come in two types. The distinction is identical in concept: **time**.

| | SOC 1 Type 1 | SOC 1 Type 2 |
|--|-------------|-------------|
| **What it evaluates** | Design of controls at a specific point in time | Design and operating effectiveness of controls over a period of time |
| **Observation period** | A single date (e.g., "as of March 31, 2026") | A defined period (e.g., "January 1, 2026 through December 31, 2026") |
| **What it proves** | "Controls are suitably designed" | "Controls are suitably designed and operated effectively" |
| **Evidence requirements** | Description of controls and auditor walkthrough | Full evidence of controls operating: logs, samples, reconciliations |
| **Typical duration** | 4-8 weeks of audit fieldwork | 6-12 month observation period + audit fieldwork |
| **Cost** | $20,000-$60,000 | $40,000-$100,000+ |
| **What client auditors prefer** | Acceptable for initial engagements | Required by most user entity auditors for ongoing reliance |

### When to Use SOC 1 Type 1

A Type 1 report is appropriate when:

- Your organization is undergoing a SOC 1 audit for the first time and needs an initial report
- A new client's auditor needs assurance before the next full audit cycle
- You are establishing a baseline before transitioning to a Type 2 report
- You recently implemented significant changes to your control environment and want to demonstrate the redesigned controls

### When to Use SOC 1 Type 2

A Type 2 report is the standard expectation for mature service organizations. Most user entity auditors will require a Type 2 report to:

- Place reliance on your controls when auditing their client's financial statements
- Reduce the amount of substantive testing they must perform on transactions processed through your service
- Satisfy regulatory requirements (e.g., banking regulators often expect Type 2 reports from critical service providers)

**Bottom line:** Type 1 is a stepping stone. If your clients' auditors are asking for a SOC 1, they will ultimately want a Type 2.

---

## Who Needs a SOC 1 Report?

A SOC 1 report is necessary for any service organization whose services or systems affect the financial reporting of its client organizations. The test is straightforward: **if a misstatement or error in your service could cause a material misstatement in your client's financial statements, you likely need a SOC 1.**

### Industries and Roles That Commonly Require SOC 1

**Payroll Service Providers**
Companies like ADP, Paychex, or any third-party payroll processor. If you calculate wages, withhold taxes, distribute paychecks, or file payroll tax returns on behalf of clients, errors in your processing directly affect your clients' financial statements. Their auditors will request a SOC 1.

**Payment Processors and Gateways**
If you authorize, settle, or reconcile payment transactions for merchants or businesses, the accuracy and completeness of those transactions flow directly into your clients' revenue recognition, accounts receivable, and cash balances.

**Benefits Administrators and Third-Party Administrators (TPAs)**
Companies that administer health insurance, retirement plans (401(k)), flexible spending accounts, or other employee benefit programs. Errors in contribution calculations, eligibility determinations, or benefit distributions affect plan sponsors' financial reporting.

**Loan Servicers and Mortgage Processors**
Organizations that service loans — collecting payments, managing escrow accounts, calculating interest, and reporting to borrowers and investors. The accuracy of loan accounting directly affects the financial statements of the institutions that own those loans.

**Trust Companies and Custodians**
Entities that hold assets in custody, process trust transactions, or manage fiduciary accounts. Asset valuations, income allocations, and distribution calculations must be accurate for the trust or fund's financial reporting.

**Financial SaaS and Accounting Platforms**
If your software processes, calculates, or stores financial transactions that your clients use for their financial reporting — general ledger systems, accounts payable/receivable platforms, billing systems, revenue recognition tools — your clients' auditors may request a SOC 1.

**Data Centers and Cloud Infrastructure Providers (When Financial Processing Is Involved)**
If you host or manage infrastructure specifically for financial processing applications — not general-purpose cloud hosting — a SOC 1 may be appropriate for those specific services.

**Claims Processors**
Insurance claims administrators, healthcare claims processors, and similar organizations whose processing accuracy affects the financial reporting of insurers or self-insured employers.

### How to Know If You Need SOC 1, SOC 2, or Both

A simple framework:

- **Your service affects clients' financial reporting** → SOC 1
- **Your service stores, processes, or transmits client data and clients care about your security posture** → [SOC 2](/glossary/what-is-soc2)
- **Both apply** → Both reports (this is common for financial services technology companies)

Many payment processors, financial SaaS providers, and benefits administrators need both SOC 1 (for their clients' auditors) and SOC 2 (for their clients' security teams). The two reports address different audiences and different risk domains.

---

## The SOC 1 Audit Process: What to Expect

A SOC 1 audit follows a structured process. Understanding it upfront helps you plan resources, set expectations, and avoid surprises.

### Phase 1: Scoping and Planning (2-4 Weeks)

Work with your CPA firm to define the scope of the engagement:

- **Services in scope** — Which services affect client financial reporting?
- **Control objectives** — What should the controls achieve? (These are custom, not predefined.)
- **System boundaries** — Which applications, databases, infrastructure, and processes are included?
- **Subservice organizations** — Do you rely on third parties (e.g., cloud hosting, payment networks) that are part of the service delivery? You must decide whether to use the **inclusive method** (include their controls in your report) or the **carve-out method** (exclude them and note the dependency).
- **Report type** — Type 1 or Type 2?
- **Observation period** (for Type 2) — Typically aligned with a calendar year or a client's fiscal year.

### Phase 2: System Description Preparation (2-4 Weeks)

You prepare a detailed description of your system, including:

- The nature of services provided
- The components of the system (infrastructure, software, people, data, procedures)
- The boundaries of the system
- Control objectives and related controls
- Complementary User Entity Controls (CUECs) — controls that your clients must have in place for the overall control environment to work
- Complementary Subservice Organization Controls (CSOCs) — controls that your subservice organizations must have in place

This system description becomes Section III of your SOC 1 report.

### Phase 3: Evidence Collection (Ongoing for Type 2)

For a Type 2 report, you collect evidence throughout the observation period demonstrating that controls operated effectively:

- Access provisioning and termination tickets
- User access review documentation
- Change management tickets with approvals and testing evidence
- Reconciliation reports
- Batch processing logs and exception reports
- Incident reports and resolution documentation
- Backup and recovery test results

For a Type 1 report, evidence requirements are lighter — auditors focus on walkthroughs and documentation of control design rather than operational evidence.

### Phase 4: Auditor Fieldwork (2-6 Weeks)

The CPA firm performs testing:

- **For Type 1:** Walkthroughs of controls to confirm they are suitably designed. The auditor traces a transaction or process through the control to verify the design.
- **For Type 2:** Testing of operating effectiveness through sampling. Auditors select samples of transactions, access changes, reconciliations, and other events to verify that controls operated as described throughout the observation period. Sample sizes are typically 25-50 items per control, depending on the frequency of the control activity.

Auditors will also interview control owners, review documentation, and inspect system configurations.

### Phase 5: Report Drafting and Issuance (2-4 Weeks)

The CPA firm drafts the report, including:

- Their independent opinion
- A description of tests performed and results
- Any exceptions identified

You review the draft for factual accuracy (especially the system description), and the final report is issued.

**Total timeline:** A Type 1 engagement typically takes 8-16 weeks from kickoff to report issuance. A Type 2 engagement requires the observation period (6-12 months) plus approximately 6-10 weeks for fieldwork and reporting.

---

## SOC 1 Report Contents: What's Inside

A SOC 1 report is a formal document, typically 50 to 200+ pages, with five distinct sections. Understanding the structure helps you prepare effectively and helps your clients' auditors navigate the report.

### Section I: Independent Service Auditor's Report (The Opinion)

This is the most important section. Written entirely by the CPA firm, it contains:

- The scope of the engagement
- The auditor's responsibilities
- Management's responsibilities
- **The auditor's opinion** — either unqualified (clean) or qualified (exceptions noted that affect the opinion)

An **unqualified opinion** means the auditor concluded that, in all material respects, the controls were suitably designed (Type 1) or suitably designed and operating effectively (Type 2). This is what you want.

A **qualified opinion** means the auditor identified material exceptions. This is a serious outcome that your clients' auditors will scrutinize closely.

### Section II: Management's Assertion

A formal statement from your management asserting that:

- The system description is fairly presented
- Controls are suitably designed (Type 1) or suitably designed and operated effectively throughout the observation period (Type 2)
- The criteria used for the assertion are clearly identified (SSAE 18)

### Section III: Description of the Service Organization's System

The most detailed section — often 30-100+ pages. It describes:

- The services provided and the service commitments
- The components of the system (infrastructure, software, people, procedures, data)
- The control environment, including organizational structure, governance, and risk management
- Control objectives and the specific controls in place
- Complementary User Entity Controls (CUECs)
- Complementary Subservice Organization Controls (CSOCs) and whether subservice organizations are treated using the inclusive or carve-out method

### Section IV: Control Objectives, Related Controls, Tests of Controls, and Results

This is the section user entity auditors spend the most time reading. For each control objective, it lists:

- The stated control objective
- The specific controls designed to achieve that objective
- The tests the auditor performed
- The results of those tests, **including any exceptions identified**

Exceptions do not automatically mean a qualified opinion. A few isolated exceptions in a large sample may be noted without affecting the overall opinion. However, pervasive or systemic exceptions — such as an access review that was never performed during the observation period — can lead to a qualification.

### Section V: Other Information Provided by the Service Organization (Optional)

Some organizations include supplementary information — typically management's response to exceptions, future remediation plans, or additional context about the control environment. This section is **not covered by the auditor's opinion**.

---

## SOC 1 vs SOC 2: The Key Differences

This is the most common point of confusion in compliance conversations. SOC 1 and SOC 2 are both SOC reports issued by CPA firms, but they serve entirely different purposes.

| Dimension | SOC 1 | SOC 2 |
|-----------|-------|-------|
| **Purpose** | Evaluate controls relevant to client financial reporting (ICFR) | Evaluate controls relevant to security, availability, processing integrity, confidentiality, and privacy |
| **Standard** | SSAE 18 / ISAE 3402 | SSAE 18 (AT-C Section 205) / Trust Service Criteria |
| **Control criteria** | Custom control objectives defined by the organization | AICPA Trust Service Criteria (predefined) |
| **Primary audience** | User entity auditors (financial statement auditors) | Customers, prospects, security teams, procurement |
| **Typical requestor** | Your client's external auditor | Your client's security or procurement team |
| **Industry focus** | Financial services, payroll, payment processing, benefits administration | Technology, SaaS, cloud services, data-handling companies |
| **Report types** | Type 1 and Type 2 | Type 1 and Type 2 |
| **Public version** | No (SOC 1 has no public equivalent) | SOC 3 (general-use summary) |

### The Critical Decision Point

If a client's **auditor** is asking for a report to rely on during a **financial statement audit**, they need a SOC 1.

If a client's **security team or procurement department** is asking for a report to evaluate your **data protection and security controls**, they need a SOC 2.

If both are asking, you need both. For a detailed comparison, see our [SOC 1 vs SOC 2 comparison guide](/comparisons/soc1-vs-soc2).

---

## SOC 1 Cost: How Much Does a SOC 1 Audit Cost?

SOC 1 audit costs vary significantly based on the complexity of your service, the size of your organization, the number of control objectives, and whether you are pursuing a Type 1 or Type 2 report.

### Typical Cost Ranges

| Component | Type 1 | Type 2 |
|-----------|--------|--------|
| **CPA firm audit fees** | $20,000-$60,000 | $40,000-$100,000+ |
| **Internal preparation costs** (staff time, documentation) | $10,000-$30,000 | $20,000-$60,000 |
| **Remediation costs** (fixing control gaps) | $5,000-$50,000 | $5,000-$50,000 |
| **Total estimated range** | $35,000-$140,000 | $65,000-$210,000+ |

### Factors That Increase Cost

- **Number of control objectives** — More control objectives means more testing, which increases audit hours
- **Number of locations or systems** — Multi-site or multi-application environments require broader testing
- **Subservice organizations** — Using the inclusive method (including subservice organizations in your report) significantly increases scope and cost
- **Organization size** — Larger organizations with more employees, more transactions, and more complex processes require larger audit samples
- **First-time audit** — The initial SOC 1 engagement requires more effort from both the auditor and your team to establish the system description and control framework
- **Exceptions from prior year** — If the previous year's report had exceptions, auditors will likely increase sample sizes, which increases cost
- **CPA firm tier** — Big 4 firms (Deloitte, PwC, EY, KPMG) charge significantly more than regional or mid-tier firms. The choice of firm should match your clients' expectations and industry norms.

### How to Reduce SOC 1 Costs

- **Narrow the scope** — Only include services and systems that actually affect client financial reporting
- **Use the carve-out method** for subservice organizations when appropriate
- **Maintain clean controls year-over-year** — Fewer exceptions mean smaller audit samples in subsequent years
- **Prepare thoroughly** — Organized evidence and responsive control owners reduce audit fieldwork hours
- **Align your SOC 1 and SOC 2 audits** if you need both — some CPA firms offer efficiencies when performing both engagements concurrently

---

## How to Prepare for a SOC 1 Audit

Whether this is your first SOC 1 audit or you are improving on a prior year's report, following a structured preparation process reduces cost, minimizes surprises, and increases your likelihood of a clean opinion.

### Step 1: Identify the Services in Scope

Document every service you provide that could affect your clients' financial reporting. Map each service to the specific financial statement line items or processes it touches. This defines the boundary of your SOC 1 engagement.

### Step 2: Define Control Objectives

Work with your CPA firm (or an experienced compliance advisor) to draft control objectives that are specific, testable, and aligned with the risks inherent in your service. Avoid vague objectives — auditors need to be able to design tests that definitively determine whether the objective has been met.

### Step 3: Map Controls to Objectives

For each control objective, identify the specific controls that address it. A single control objective may have multiple controls. Each control should be:

- **Clearly documented** — A written description of what the control does, who performs it, how often, and what evidence it produces
- **Assigned to a control owner** — A specific person responsible for execution
- **Testable** — An auditor should be able to verify its operation through inspection, observation, inquiry, or re-performance

### Step 4: Identify and Document CUECs and CSOCs

Complementary User Entity Controls (CUECs) are controls your clients must implement for the overall system of controls to function. For example, if your payroll system requires clients to submit payroll data by a specific deadline for accurate processing, that is a CUEC.

Complementary Subservice Organization Controls (CSOCs) are controls at your third-party providers (cloud hosting, payment networks, etc.) that your control environment depends on.

Document these clearly — they appear in your SOC 1 report and set appropriate expectations.

### Step 5: Perform a Readiness Assessment

Before your auditor begins fieldwork, conduct an internal assessment:

- Are all controls documented?
- Are control owners identified and trained?
- Is evidence being generated and retained?
- Are there any known gaps that would result in exceptions?

Fix issues before the audit starts — it is far less expensive and disruptive to remediate proactively than to have exceptions in your report.

### Step 6: Establish Evidence Collection Processes

For a Type 2 report, evidence must be collected **throughout the observation period**, not assembled after the fact. Set up processes and systems to:

- Retain access provisioning and termination records
- Document all change management approvals and testing
- Archive reconciliation reports
- Log exception processing and resolution
- Record backup test results
- Maintain incident response documentation

### Step 7: Conduct a Pre-Audit Walkthrough

Before auditors arrive for fieldwork, walk through each control with the control owner. Verify that:

- The control is operating as documented
- Evidence is available and organized
- The control owner can explain the control clearly to an auditor

### Step 8: Prepare Your Team

Auditors will interview control owners and process managers. Prepare your team by:

- Explaining the audit process and what to expect
- Clarifying what auditors are looking for (consistency and documentation, not perfection)
- Identifying who will be the primary point of contact for auditor requests
- Setting up a shared repository for evidence delivery to minimize back-and-forth

---

## Common SOC 1 Audit Findings

Understanding the most frequent findings helps you prevent them. These are the issues CPA firms identify most often during SOC 1 audits:

### 1. Access Reviews Not Performed on Schedule

Control: User access to financial processing systems is reviewed quarterly (or annually).
Finding: The review was not performed during one or more quarters, or the review was performed but no evidence of remediation actions was retained when inappropriate access was identified.

**How to prevent it:** Set calendar reminders, assign a specific owner, use a standardized template, and document both the review and any resulting access changes.

### 2. Segregation of Duties Violations

Control: Incompatible duties are segregated (e.g., transaction initiation and approval are performed by different individuals).
Finding: A single individual performed both functions, or system configurations allowed it even if it was not supposed to happen.

**How to prevent it:** Configure system-level role restrictions. Where perfect segregation is not feasible (common in smaller organizations), implement and document compensating controls such as supervisory review of all transactions.

### 3. Incomplete Change Management Documentation

Control: All changes to financial processing applications are authorized, tested, and approved before deployment.
Finding: Changes were deployed without documented approval, testing evidence was not retained, or emergency changes were not retroactively documented.

**How to prevent it:** Enforce a change management workflow that requires approval tickets before deployment. Retain all testing and approval artifacts. Establish a formal exception process for emergency changes with mandatory post-deployment review.

### 4. Reconciliation Exceptions Not Resolved Timely

Control: Reconciliations between systems are performed and discrepancies are investigated and resolved.
Finding: Reconciliations were performed, but identified discrepancies were not investigated or resolved within the specified timeframe.

**How to prevent it:** Define clear SLAs for discrepancy resolution. Track open items and escalate unresolved discrepancies. Retain evidence of the investigation and resolution.

### 5. Insufficient Documentation of CUECs

Control: Complementary User Entity Controls are clearly communicated to clients.
Finding: CUECs were mentioned in the report but not communicated to clients in a way that enables them to implement the controls.

**How to prevent it:** Include CUECs in client-facing documentation — service agreements, implementation guides, or a dedicated controls communication.

### 6. Terminated Employee Access Not Revoked Promptly

Control: System access is revoked within a defined timeframe (e.g., 24 hours) of employment termination.
Finding: Access remained active for days or weeks after termination.

**How to prevent it:** Integrate your HR termination process with your IT access management process. Automate deprovisioning where possible. Audit for orphaned accounts monthly.

### 7. Backup and Recovery Testing Gaps

Control: Backup restoration is tested periodically to verify recoverability.
Finding: Backups were performed, but restoration testing was not conducted or documented during the observation period.

**How to prevent it:** Schedule restoration tests at least annually (quarterly is better). Document the test, including what was restored, the recovery time, and whether the restored data was validated for completeness and accuracy.

---

## SOC 1 Frequently Asked Questions

### Is SOC 1 the same as SOC 2?

No. SOC 1 and SOC 2 are fundamentally different reports that serve different audiences and evaluate different control domains. SOC 1 evaluates controls relevant to your clients' financial reporting. [SOC 2](/glossary/what-is-soc2) evaluates controls related to security, availability, processing integrity, confidentiality, and privacy. A company may need one or both, depending on the services it provides.

### What is the difference between SOC 1 and SAS 70?

SOC 1 is the modern replacement for SAS 70. The AICPA retired SAS 70 in 2011 and introduced the SOC framework (SOC 1, SOC 2, SOC 3). The underlying purpose is similar — evaluating a service organization's controls relevant to financial reporting — but SOC 1 operates under updated attestation standards (SSAE 18 vs. the older SAS 70 standard) and includes stricter requirements around risk assessment, subservice organizations, and management assertions.

### How long does a SOC 1 audit take?

For a Type 1 report, expect 8-16 weeks from engagement kickoff to report issuance. For a Type 2 report, the observation period is typically 6-12 months, followed by 6-10 weeks of fieldwork and reporting. Total elapsed time for a first-time Type 2 engagement is approximately 9-15 months.

### Who performs a SOC 1 audit?

Only a licensed **CPA firm** can issue a SOC 1 report. The engagement must be conducted by CPAs following SSAE 18 (or ISAE 3402) attestation standards. Internal auditors and non-CPA consulting firms can help you prepare for the audit, but they cannot issue the report.

### Can a SOC 1 report replace a SOC 2 report?

No. They evaluate entirely different control domains. A SOC 1 report does not evaluate your security posture, data protection practices, or privacy controls — which is what SOC 2 covers. If a client's security team asks for a SOC 2, giving them a SOC 1 will not satisfy their requirements (and may raise questions about your organization's compliance maturity).

### How often do I need a SOC 1 audit?

SOC 1 reports are typically issued annually. For a Type 2 report, the observation period usually covers a 12-month period (often aligned with a calendar year). User entity auditors expect a current SOC 1 report each year — a report that is more than 12 months old is generally considered stale.

### What happens if my SOC 1 report has exceptions?

Exceptions do not necessarily mean a qualified opinion. Isolated exceptions (e.g., one missed access review out of four quarterly reviews) may be noted in the report without affecting the overall opinion. However, pervasive or systemic exceptions can lead to a qualified opinion, which may cause your clients' auditors to perform additional testing or, in some cases, decline to rely on your controls entirely.

### Do startups need a SOC 1?

It depends on what the startup does. If your startup processes financial transactions, runs payroll, manages payments, or performs any service that touches your clients' financial reporting, you may need a SOC 1 report even at an early stage — especially if your clients are publicly traded companies or financial institutions whose auditors require it. For startups that are primarily SaaS or technology companies focused on data handling, [SOC 2](/glossary/what-is-soc2) is typically the first priority.

---

## Ready to Prepare for a SOC 1 Audit?

Whether you need a SOC 1 report, a SOC 2 report, or both, the preparation process follows the same principle: define your controls, implement them systematically, collect evidence continuously, and engage with an auditor when you are ready — not when you are scrambling.

QuickTrust helps service organizations prepare for SOC 1 and SOC 2 audits with hands-on engineering and compliance expertise. Our team of Big 4-experienced security professionals and DevOps engineers do not just tell you what to fix — they implement the controls, configure the systems, build the evidence collection processes, and coordinate with your auditor so your team can stay focused on running the business.

- **Gap assessment** — Identify control gaps and remediation priorities before your audit engagement begins
- **Control implementation** — Engineers configure access management, change management workflows, monitoring, and reconciliation processes
- **Evidence management** — Automated collection and organization of audit evidence tied to your actual systems
- **Auditor coordination** — Manage the engagement, respond to auditor requests, and prepare your team for interviews
- **Multi-framework efficiency** — If you need both SOC 1 and [SOC 2](/glossary/what-is-soc2), QuickTrust maps overlapping controls to reduce duplicate effort and cost

**Get your compliance gap assessment at [trust.quickintell.com](https://trust.quickintell.com)**

100% audit pass rate. Audit-ready in weeks, not months. Engineers included.
