---
meta_description: "The definitive guide to security metrics and KPIs for compliance reporting. 50+ metrics organized by category with formulas, benchmarks, and board-ready dashboard templates."
target_keyword: "security metrics"
secondary_keywords: "security KPIs, cybersecurity metrics, security metrics dashboard, security metrics for board reporting, compliance metrics"
word_count_target: 4500+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-21
---

# Security Metrics and KPIs: The Complete Guide to Measuring and Reporting Your Security Posture

"How secure are we?" It is the most important question a board of directors can ask, and the most difficult question a security leader can answer honestly. Not because the answer is unknowable, but because most security programs lack the measurement framework to answer it with anything beyond anecdotes, tool outputs, and gut feel.

The problem is not a shortage of data. Modern security programs generate enormous volumes of telemetry -- vulnerability scans, endpoint alerts, access logs, phishing simulation results, patch deployment records, incident tickets. The problem is that very little of this data is organized into metrics that are meaningful, comparable, actionable, and aligned with what auditors, executives, and regulators actually need to see.

The consequence is predictable. Security teams report activity instead of outcomes. Boards receive dashboards full of numbers that look impressive but communicate nothing about actual risk posture. Auditors ask for metrics that the team has never tracked. And when something goes wrong, there is no baseline to measure the response against.

This guide provides a complete framework for security metrics and KPIs: what to measure, how to calculate it, what benchmarks to target, and how to report it to the three audiences that matter most -- your operations team, your compliance auditors, and your board of directors. It includes more than 50 specific metrics organized by security domain, calculation formulas, industry benchmarks, dashboard design principles, and framework-specific requirements for SOC 2, ISO 27001, and HIPAA.

If you have ever been asked to present security metrics to a board and did not know where to start, or if your auditor has flagged insufficient monitoring metrics as a finding, this is the guide you need.

---

## Why Security Metrics Matter

The adage "what gets measured gets managed" is overused in business writing, but in security it carries specific, consequential weight. Without defined metrics and consistent measurement, three things happen that directly undermine your security program and your compliance posture.

### You cannot demonstrate control effectiveness to auditors

Every major compliance framework requires not just that controls exist, but that they are operating effectively over time. SOC 2 auditors examining a Type II report need evidence of consistent control operation over the observation period. ISO 27001 certification auditors require documented performance evaluation under Clause 9. HIPAA requires ongoing evaluation of security measures. None of these requirements can be satisfied without metrics.

A vulnerability management program without mean-time-to-remediate data cannot prove it is working. An access control program without orphaned account metrics cannot demonstrate completeness. An incident response program without detection and response time data cannot evidence its effectiveness. Metrics are not a reporting luxury -- they are audit evidence.

For a detailed breakdown of compliance monitoring requirements across frameworks, see our [compliance monitoring guide](/compliance-monitoring-guide).

### You cannot prioritize investments rationally

Security budgets are finite, and every dollar spent on one control is a dollar not spent on another. Without metrics, investment decisions are driven by vendor marketing, recent headlines, the loudest voice in the room, or whatever the last auditor mentioned. With metrics, you can identify which areas of your program are performing below target, quantify the gap, estimate the cost of closing it, and compare that cost against alternatives. This is the difference between a security program that improves and one that merely changes.

### You cannot communicate risk to leadership

The SEC's cybersecurity disclosure rules (effective December 2023) require public companies to describe their processes for assessing, identifying, and managing material cybersecurity risks, including board oversight of those processes. Private companies face similar expectations from investors, customers, and cyber insurance underwriters. These stakeholders do not want to see a list of tools deployed or a count of vulnerabilities scanned. They want to understand the organization's security posture in terms that map to business risk. Security metrics, structured correctly, provide the translation layer between technical operations and business risk communication.

---

## The Security Metrics Framework: Operational, Tactical, and Strategic

Not all metrics serve the same audience or the same purpose. Treating a vulnerability count and a board-level risk score as equivalent metrics is a category error that leads to dashboards that satisfy nobody. Effective security measurement programs organize metrics into three tiers, each with a different audience, cadence, and level of abstraction.

### Tier 1: Operational Metrics

**Audience:** Security analysts, IT operations, SOC engineers
**Cadence:** Real-time or daily
**Purpose:** Drive day-to-day security operations and identify issues requiring immediate action

Operational metrics are the raw performance indicators that security teams use to manage their daily work. They are granular, technical, and high-frequency. Examples include the number of unpatched critical vulnerabilities, current EDR deployment coverage, phishing emails blocked in the last 24 hours, and the number of open incident tickets by severity.

These metrics are consumed by the people doing the work. They belong on a SOC dashboard, not in a board presentation.

### Tier 2: Tactical Metrics

**Audience:** Security managers, compliance leads, IT directors
**Cadence:** Weekly or monthly
**Purpose:** Measure program effectiveness, track trends, identify areas requiring resource allocation

Tactical metrics aggregate operational data into performance indicators that reveal whether programs are meeting their objectives. Mean time to remediate vulnerabilities, incident response SLA compliance rate, percentage of endpoints with current patches, and phishing simulation failure rate trends are tactical metrics. They are the primary indicators used to manage programs, allocate resources, and prepare for audits.

Tactical metrics should be trended over time. A single data point is informational. A six-month trend is actionable.

### Tier 3: Strategic Metrics

**Audience:** CISO, CEO, board of directors, investors, cyber insurers
**Cadence:** Monthly or quarterly
**Purpose:** Communicate overall security posture and risk exposure in business terms

Strategic metrics translate security program performance into language that non-technical stakeholders can evaluate: overall risk score, compliance posture across frameworks, residual risk by business unit, security program maturity level, and security investment as a percentage of IT spend. They should be few in number (no more than ten), stable in methodology, and linked to business outcomes.

The most common mistake in security reporting is presenting operational metrics to a strategic audience. A board does not need to know how many vulnerabilities were scanned last quarter. It needs to know whether the vulnerability management program is reducing risk at a rate that is consistent with the organization's risk appetite.

---

## 50+ Security Metrics Organized by Category

The following sections catalog the most important security metrics by domain. For each metric, we provide a definition, the calculation method, the recommended measurement cadence, and the compliance relevance. Formulas are provided in the dedicated section that follows.

### Vulnerability Management Metrics

Vulnerability management is one of the most metric-rich security domains, and auditors across every framework expect quantitative evidence that your program is working. For a complete guide to building a vulnerability management program, see our [vulnerability management program guide](/vulnerability-management-program-guide).

| # | Metric | What It Measures | Cadence |
|---|--------|-----------------|---------|
| 1 | **Mean Time to Remediate (MTTR) by Severity** | Average elapsed time from vulnerability discovery to confirmed remediation, segmented by critical, high, medium, and low severity | Monthly |
| 2 | **Vulnerability Scan Coverage** | Percentage of in-scope assets scanned within the defined scanning cadence | Weekly |
| 3 | **Aging Vulnerabilities** | Count and percentage of vulnerabilities that have exceeded their SLA-defined remediation window | Weekly |
| 4 | **Remediation SLA Compliance Rate** | Percentage of vulnerabilities remediated within the defined SLA for their severity level | Monthly |
| 5 | **Vulnerability Density** | Number of open vulnerabilities per asset (or per 1,000 lines of code for application security) | Monthly |
| 6 | **Recurrence Rate** | Percentage of remediated vulnerabilities that reappear in subsequent scans | Monthly |
| 7 | **Risk-Accepted Vulnerability Ratio** | Percentage of total open vulnerabilities that have been formally risk-accepted rather than remediated | Quarterly |
| 8 | **Patch Cycle Time** | Average time from vendor patch release to deployment in your environment | Monthly |

### Incident Response Metrics

Incident response metrics demonstrate that your organization can detect, contain, and recover from security incidents within defined timelines. These are among the first metrics auditors request. For guidance on building an incident response plan, see our [incident response plan guide](/incident-response-plan-compliance-guide).

| # | Metric | What It Measures | Cadence |
|---|--------|-----------------|---------|
| 9 | **Mean Time to Detect (MTTD)** | Average elapsed time from when an incident occurs to when it is detected | Monthly |
| 10 | **Mean Time to Respond (MTTR)** | Average elapsed time from incident detection to initial containment action | Monthly |
| 11 | **Mean Time to Contain (MTTC)** | Average elapsed time from detection to full containment of the incident | Monthly |
| 12 | **Mean Time to Recover (MTTRec)** | Average elapsed time from containment to full restoration of normal operations | Monthly |
| 13 | **Incidents by Severity** | Count of incidents classified by severity level (P1/P2/P3/P4) over the reporting period | Monthly |
| 14 | **False Positive Rate** | Percentage of alerts investigated that were determined to be non-incidents | Monthly |
| 15 | **Escalation Accuracy** | Percentage of incidents correctly classified at initial triage (not reclassified during investigation) | Quarterly |
| 16 | **Post-Incident Review Completion Rate** | Percentage of P1/P2 incidents that received a documented post-incident review within the defined timeframe | Monthly |
| 17 | **Recurring Incident Rate** | Percentage of incidents with root causes that match a previously identified and remediated root cause | Quarterly |

### Access Control Metrics

Access control metrics are critical for SOC 2 (CC6.1-CC6.3), ISO 27001 (A.5.15-A.5.18, A.8.2-A.8.5), and HIPAA (164.312(a), 164.312(d)). They measure whether the principle of least privilege is being maintained and whether identity lifecycle management is functioning.

| # | Metric | What It Measures | Cadence |
|---|--------|-----------------|---------|
| 18 | **Orphaned Account Count** | Number of active accounts belonging to terminated employees or contractors | Weekly |
| 19 | **MFA Adoption Rate** | Percentage of user accounts with multi-factor authentication enabled | Weekly |
| 20 | **Privileged Access Ratio** | Percentage of total user accounts with administrative or elevated privileges | Monthly |
| 21 | **Access Review Completion Rate** | Percentage of required access reviews completed on schedule | Quarterly |
| 22 | **Access Provisioning Time** | Average time from access request approval to account provisioning | Monthly |
| 23 | **Access Deprovisioning Time** | Average time from employee termination to full access revocation across all systems | Weekly |
| 24 | **Shared Account Count** | Number of active shared or generic accounts in the environment | Monthly |
| 25 | **Dormant Account Rate** | Percentage of accounts with no login activity in the last 90 days | Monthly |

### Compliance Metrics

These metrics measure the health of your compliance program itself -- not individual security controls, but the operational machinery that keeps you audit-ready. For a comprehensive guide to continuous compliance monitoring, see our [compliance monitoring guide](/compliance-monitoring-guide).

| # | Metric | What It Measures | Cadence |
|---|--------|-----------------|---------|
| 26 | **Control Health Score** | Percentage of controls in a passing state at the time of measurement | Daily |
| 27 | **Evidence Freshness** | Percentage of required evidence items that are current (collected within their defined validity period) | Weekly |
| 28 | **Audit Findings Closure Rate** | Percentage of audit findings remediated within the agreed-upon timeline | Monthly |
| 29 | **Policy Acknowledgment Rate** | Percentage of employees who have acknowledged the current version of all required policies | Monthly |
| 30 | **Policy Review Completion** | Percentage of security policies reviewed and updated within their defined review cycle | Quarterly |
| 31 | **Control Exception Count** | Number of active control exceptions or compensating controls in effect | Monthly |
| 32 | **Compliance Posture by Framework** | Overall compliance percentage for each framework the organization is certified against | Monthly |
| 33 | **Days to Audit Readiness** | Estimated number of days of preparation work needed if an audit started today | Monthly |

### Endpoint Security Metrics

Endpoint security metrics measure the health and coverage of your endpoint protection program. With the shift to remote and hybrid workforces, endpoint visibility has become one of the most scrutinized areas during compliance audits.

| # | Metric | What It Measures | Cadence |
|---|--------|-----------------|---------|
| 34 | **EDR/XDR Coverage Rate** | Percentage of endpoints (workstations, servers, mobile devices in scope) with active endpoint detection and response agents | Weekly |
| 35 | **Patch Compliance Rate** | Percentage of endpoints running the latest approved OS and application patches | Weekly |
| 36 | **Unmanaged Device Count** | Number of devices accessing corporate resources that are not enrolled in endpoint management | Weekly |
| 37 | **Encryption Compliance Rate** | Percentage of endpoints with full-disk encryption enabled and verified | Monthly |
| 38 | **OS Currency Rate** | Percentage of endpoints running a supported (non-EOL) operating system version | Monthly |
| 39 | **Endpoint Isolation Response Time** | Average time to isolate a compromised endpoint from the network after detection | Monthly |

### Vendor Risk Metrics

Third-party risk is one of the fastest-growing areas of regulatory focus. These metrics demonstrate that your vendor risk management program is operating effectively. For a complete guide, see our [vendor risk management guide](/vendor-risk-management-complete-guide).

| # | Metric | What It Measures | Cadence |
|---|--------|-----------------|---------|
| 40 | **Vendor Assessment Completion Rate** | Percentage of vendors assessed within the required assessment cycle | Quarterly |
| 41 | **Critical Vendor Coverage** | Percentage of critical and high-risk vendors with current risk assessments and valid compliance certifications | Monthly |
| 42 | **Overdue Vendor Assessments** | Count of vendor assessments that have exceeded their scheduled due date | Monthly |
| 43 | **Vendor Compliance Certificate Currency** | Percentage of vendor SOC 2 reports, ISO 27001 certificates, and other compliance documentation that is current (not expired) | Monthly |
| 44 | **Fourth-Party Risk Visibility** | Percentage of critical vendors for which you have documented and assessed subprocessor/fourth-party risk | Quarterly |
| 45 | **Vendor Incident Rate** | Number of security incidents originating from or involving third-party vendors | Quarterly |

For detailed guidance on conducting individual vendor assessments, see our [third-party risk assessment guide](/third-party-risk-assessment-guide).

### Security Awareness and Training Metrics

Training metrics are required by every major compliance framework and are among the easiest to measure and improve. They also serve as a proxy for organizational security culture.

| # | Metric | What It Measures | Cadence |
|---|--------|-----------------|---------|
| 46 | **Training Completion Rate** | Percentage of employees who have completed required security awareness training within the defined period | Monthly |
| 47 | **Phishing Simulation Click Rate** | Percentage of employees who clicked a link or opened an attachment in a simulated phishing exercise | Per campaign |
| 48 | **Phishing Report Rate** | Percentage of employees who correctly reported the simulated phishing email through the designated reporting mechanism | Per campaign |
| 49 | **Time to Report** | Average elapsed time from simulated phishing email delivery to employee report | Per campaign |
| 50 | **Repeat Offender Rate** | Percentage of employees who failed multiple consecutive phishing simulations | Quarterly |
| 51 | **Training Assessment Pass Rate** | Percentage of employees scoring above the minimum threshold on post-training assessments | Per training cycle |
| 52 | **New Hire Training SLA Compliance** | Percentage of new hires who complete security awareness training within the defined onboarding window (typically 30 days) | Monthly |

For more on building a security awareness training program, see our [security awareness training guide](/security-awareness-training-guide).

---

## Security Metrics for SOC 2, ISO 27001, and HIPAA Compliance

Each compliance framework has specific expectations around metrics and measurement. Understanding these expectations is essential for building a metrics program that simultaneously satisfies operational needs and audit requirements.

### SOC 2 Trust Services Criteria

SOC 2 does not prescribe specific metrics, but the Trust Services Criteria create clear measurement obligations:

**CC4.1 -- COSO Principle 16:** The organization selects, develops, and performs ongoing and/or separate evaluations to ascertain whether the components of internal control are present and functioning. This directly requires that you measure whether your controls are working -- which is, by definition, a metrics requirement.

**CC4.2 -- COSO Principle 17:** The organization evaluates and communicates internal control deficiencies in a timely manner to those parties responsible for taking corrective action. This requires that you have thresholds for control performance and that you escalate when performance falls below those thresholds.

**CC7.1 -- Monitoring:** Requires ongoing monitoring of system components. Auditors expect to see metrics demonstrating that monitoring is continuous, not periodic.

In practice, SOC 2 Type II auditors commonly request: vulnerability MTTR data, access review completion evidence, incident response time data, system availability metrics, change management success rates, and evidence of management review of security performance data. For a complete SOC 2 overview, see our [SOC 2 Compliance Guide](/soc-2-compliance).

### ISO 27001 Performance Evaluation (Clause 9)

ISO 27001 is the most explicit of the major frameworks in its measurement requirements:

**Clause 9.1 -- Monitoring, measurement, analysis, and evaluation:** The organization shall determine what needs to be monitored and measured (including information security processes and controls), the methods for monitoring, measurement, analysis, and evaluation, when the monitoring and measuring shall be performed, who shall monitor and measure, when the results shall be analyzed and evaluated, and who shall analyze and evaluate these results.

This clause requires a documented metrics program. Certification auditors will ask to see: a list of defined metrics, evidence that metrics are being collected at the defined cadence, evidence that metrics are reviewed by management (typically in the management review meeting per Clause 9.3), and evidence that metric results drive corrective actions.

**Clause 9.3 -- Management Review:** Top management must review the ISMS at planned intervals. The review must consider the results of monitoring and measurement -- meaning management must see and discuss security metrics. Minutes from management review meetings must document which metrics were reviewed and what decisions were made based on those metrics.

For a complete ISO 27001 implementation guide, including all mandatory clauses, see our [ISO 27001 Certification Guide](/iso-27001-certification).

### HIPAA Security Rule

HIPAA's requirements are less prescriptive about specific metrics but create clear measurement obligations through:

**164.308(a)(1)(ii)(D) -- Information System Activity Review:** Covered entities must regularly review records of information system activity, such as audit logs, access reports, and security incident tracking reports. This requires metrics derived from system activity monitoring.

**164.308(a)(8) -- Evaluation:** Covered entities must perform periodic technical and nontechnical evaluations that establish the extent to which security policies and procedures meet the requirements of the Security Rule. This evaluation cannot be performed without defined metrics and measurement criteria.

**164.316(b)(2)(iii) -- Updates:** Covered entities must review documentation periodically and update it as needed. Metrics on policy currency, evidence freshness, and control effectiveness support this requirement.

HIPAA auditors (OCR investigators) commonly examine: access audit log review evidence, workforce training completion data, incident response metrics, risk assessment completion, and device and media control metrics (particularly encryption rates). For comprehensive HIPAA guidance, see our [HIPAA Compliance Guide](/hipaa-compliance).

---

## Building a Security Metrics Dashboard

A metrics program without effective visualization is a collection of numbers in a spreadsheet that nobody looks at. The dashboard is the delivery mechanism that transforms raw data into decisions.

### Dashboard Architecture

Build three dashboards aligned to the three-tier framework:

**Operational Dashboard (SOC/Security Team)**
- Real-time or near-real-time refresh
- Granular, technical metrics
- Alert-driven: highlight items requiring immediate action
- Tools: SIEM dashboards (Splunk, Elastic, Sentinel), EDR console, vulnerability scanner UI, ticketing system dashboards
- Focus: what needs attention right now

**Tactical Dashboard (Security Leadership/Compliance)**
- Weekly refresh with monthly trend analysis
- Program-level metrics with trend lines
- SLA compliance indicators with red/amber/green status
- Tools: Business intelligence platforms (Tableau, Power BI, Looker), compliance automation platforms, custom dashboards
- Focus: are programs meeting their objectives

**Strategic Dashboard (Board/Executive)**
- Monthly or quarterly refresh
- Maximum 8-10 metrics
- Business-contextualized: risk scores, compliance posture, program maturity
- No technical jargon, no acronyms without definition
- Tools: Board presentation format (typically slides, not interactive dashboards), compliance automation platform executive views
- Focus: what is the organization's risk posture and is it improving

### Dashboard Design Principles

**Show trends, not snapshots.** A metric at a single point in time is almost meaningless. A six-month trend tells a story. Every metric on a tactical or strategic dashboard should include historical trend data -- ideally 6-12 months of history.

**Define thresholds visually.** Every metric should have a defined target, and the dashboard should visually indicate whether the metric is meeting, approaching, or missing that target. Red/amber/green indicators are effective. A metric without a threshold is a number without meaning.

**Aggregate for executives, decompose for operators.** The board sees a single vulnerability management score. The security team sees the same score decomposed into MTTR by severity, scan coverage by asset category, SLA compliance by team, and aging vulnerability trends. Same underlying data, different level of abstraction.

**Update cadence must match the audience.** A board that meets quarterly does not need a real-time dashboard. A SOC analyst dealing with active incidents does not need monthly reports. Mismatched cadence leads to dashboards that are either stale or overwhelming.

### Integration Approach

The most common mistake organizations make when building security metrics dashboards is attempting to build a single, centralized dashboard from scratch by pulling data from every security tool via API. This approach is expensive, fragile, and requires ongoing engineering investment.

A more effective approach:

1. **Use native tool dashboards for operational metrics.** Your SIEM, EDR, vulnerability scanner, and identity provider all have built-in dashboards. Use them for operational data.
2. **Use your compliance automation platform for tactical metrics.** Platforms like QuickTrust aggregate control status, evidence freshness, and compliance posture data across frameworks and present it in dashboard form without custom engineering work.
3. **Build a lightweight executive layer for strategic metrics.** Extract the 8-10 strategic metrics from your compliance platform and operational tools, and present them in a board-friendly format. This can be as simple as a slide template updated monthly.

---

## Board-Ready Security Reporting: What Executives Need to See

Presenting security metrics to a board of directors is fundamentally different from presenting them to a security team. The failure mode is not lack of data -- it is presenting the wrong data, at the wrong level of abstraction, without the business context that makes it actionable.

### SEC Cybersecurity Disclosure Rules

For public companies, the SEC's cybersecurity disclosure rules (adopted July 2023, effective December 2023) create specific governance expectations. Companies must describe the board's oversight of risks from cybersecurity threats, including whether the board or a committee is responsible for oversight, how the board is informed about cybersecurity risks, and how frequently the board considers cybersecurity matters.

This means the board must receive regular, documented security briefings that include metrics. The board minutes must reflect that security posture was discussed. And the information presented must be substantive enough to demonstrate genuine oversight, not a perfunctory checkbox exercise.

Even for private companies, investors, acquirers, and cyber insurance underwriters increasingly expect evidence of board-level security governance.

### The Board Reporting Framework

Structure board security reports around five questions that directors care about:

**1. What is our current risk posture?**
Present an overall risk score or maturity level (NIST CSF maturity is increasingly the standard), mapped to the organization's defined risk appetite. Show the trend over the last four quarters. Identify the top three risks by residual risk score.

**2. Are we compliant with our obligations?**
Present compliance posture by framework (SOC 2, ISO 27001, HIPAA, PCI DSS, or whichever frameworks the organization operates against). Show the percentage of controls in a passing state. Highlight any audit findings or certification risks.

**3. What incidents occurred, and how did we respond?**
Summarize significant security incidents (P1/P2) with a one-sentence description, the impact, the response timeline, and the status. Board members do not need technical details. They need to know what happened, whether the response was effective, and whether the root cause has been addressed.

**4. Are we improving?**
Show quarter-over-quarter trends for the core metrics: MTTR for vulnerabilities, incident detection and response times, compliance posture, phishing simulation results, and training completion. An improving trend demonstrates that the security investment is producing results.

**5. What do we need?**
If additional resources, budget, or executive decisions are required, present the request with supporting data. "We need to reduce our MTTR for critical vulnerabilities from 12 days to 7 days. This requires adding two engineers to the vulnerability management team at a cost of $X. Current MTTR is trending in the wrong direction due to increased vulnerability volume from our cloud migration."

### Metrics Executives Should See

The following metrics are appropriate for board-level reporting:

- **Overall Security Maturity Score** (mapped to NIST CSF or equivalent framework)
- **Compliance Posture by Framework** (percentage of controls passing)
- **Significant Incident Count and Trend** (P1/P2 incidents per quarter)
- **Mean Time to Remediate Critical Vulnerabilities** (trended over 4+ quarters)
- **Phishing Simulation Failure Rate** (trended -- a proxy for security culture)
- **Third-Party/Vendor Risk Summary** (percentage of critical vendors with current assessments)
- **Security Investment as Percentage of IT Spend** (benchmarked against industry)
- **Open Audit Findings** (count and aging)

Do not present more than ten metrics. Do not present operational detail. Do not use acronyms without defining them. Include a one-paragraph narrative summary at the top of the report that a director can read in 30 seconds and understand the overall state.

---

## Metric Formulas and Calculation Methods

Precise, consistent calculation methodology is essential. A metric that is calculated differently each month is not a metric -- it is a guess. The following formulas define the standard calculations for the most critical security metrics.

### Vulnerability Management Formulas

**Mean Time to Remediate (MTTR)**

```
MTTR = Sum of (Remediation Date - Discovery Date) for all remediated vulnerabilities / Count of remediated vulnerabilities
```

Segment by severity (critical, high, medium, low). Calculate monthly. Use calendar days, not business days, because attackers do not observe weekends.

**Vulnerability Scan Coverage**

```
Scan Coverage (%) = (Assets scanned within defined cadence / Total in-scope assets) x 100
```

Define "cadence" by asset type: weekly for internet-facing assets, monthly for internal infrastructure, per-build for application code.

**Remediation SLA Compliance Rate**

```
SLA Compliance (%) = (Vulnerabilities remediated within SLA / Total vulnerabilities remediated) x 100
```

SLA targets by severity (example): Critical = 7 days, High = 30 days, Medium = 90 days, Low = 180 days. Adjust these targets based on your organization's risk appetite and operational capacity.

**Vulnerability Density**

```
Vulnerability Density = Open vulnerabilities / Count of in-scope assets
```

For application security: Open vulnerabilities / Thousands of lines of code (KLOC).

### Incident Response Formulas

**Mean Time to Detect (MTTD)**

```
MTTD = Sum of (Detection Timestamp - Incident Occurrence Timestamp) for all incidents / Count of incidents
```

The "occurrence timestamp" is often estimated based on forensic analysis. Document your methodology for determining this timestamp.

**Mean Time to Respond (MTTR)**

```
MTTR = Sum of (First Response Action Timestamp - Detection Timestamp) for all incidents / Count of incidents
```

"First response action" means the first containment or investigation action, not the first acknowledgment of an alert.

**Mean Time to Contain (MTTC)**

```
MTTC = Sum of (Containment Confirmed Timestamp - Detection Timestamp) for all incidents / Count of incidents
```

**False Positive Rate**

```
False Positive Rate (%) = (Alerts investigated and closed as non-incidents / Total alerts investigated) x 100
```

A high false positive rate (above 50%) indicates tuning issues that waste analyst time and increase the risk of genuine incidents being overlooked.

### Access Control Formulas

**MFA Adoption Rate**

```
MFA Adoption (%) = (User accounts with MFA enabled / Total active user accounts) x 100
```

Target: 100% for all accounts, with no exceptions for service accounts that support MFA. Track separately for privileged and non-privileged accounts.

**Access Deprovisioning Time**

```
Average Deprovisioning Time = Sum of (Full Revocation Timestamp - Termination Date) for all terminations / Count of terminations
```

"Full revocation" means all systems, not just the identity provider. Measure from the HR termination date, not from when IT received the notification.

**Privileged Access Ratio**

```
Privileged Access Ratio (%) = (Accounts with admin/elevated privileges / Total active accounts) x 100
```

### Compliance Formulas

**Control Health Score**

```
Control Health (%) = (Controls in passing state / Total controls in scope) x 100
```

A control is "passing" if its most recent evidence is current, the automated check (if applicable) is passing, and no open exceptions or findings affect it.

**Evidence Freshness**

```
Evidence Freshness (%) = (Evidence items collected within their validity period / Total required evidence items) x 100
```

Validity periods vary by evidence type: automated configuration checks may be valid for 24 hours; quarterly access review evidence is valid for 90 days; annual policy review evidence is valid for 365 days.

**Audit Findings Closure Rate**

```
Closure Rate (%) = (Findings closed within agreed timeline / Total findings requiring closure) x 100
```

---

## Benchmarks: What "Good" Looks Like

Benchmarks provide context. A 15-day MTTR for critical vulnerabilities means nothing without knowing what comparable organizations achieve. The following benchmarks are derived from industry reports (Verizon DBIR, IBM Cost of a Data Breach, SANS Institute surveys, Ponemon Institute research) and represent target ranges for mature security programs in mid-market technology companies.

| Metric | Below Average | Average | Above Average | Best in Class |
|--------|--------------|---------|---------------|---------------|
| **MTTR -- Critical Vulnerabilities** | > 30 days | 15-30 days | 7-15 days | < 7 days |
| **MTTR -- High Vulnerabilities** | > 60 days | 30-60 days | 15-30 days | < 15 days |
| **Vulnerability Scan Coverage** | < 80% | 80-90% | 90-95% | > 95% |
| **Remediation SLA Compliance** | < 70% | 70-85% | 85-95% | > 95% |
| **MTTD (Incident Detection)** | > 200 days | 100-200 days | 24-100 hours | < 24 hours |
| **MTTR (Incident Response)** | > 72 hours | 24-72 hours | 4-24 hours | < 4 hours |
| **False Positive Rate** | > 70% | 50-70% | 30-50% | < 30% |
| **MFA Adoption** | < 80% | 80-95% | 95-99% | 100% |
| **Orphaned Accounts** | > 10 | 5-10 | 1-4 | 0 |
| **Access Deprovisioning Time** | > 72 hours | 24-72 hours | 4-24 hours | < 4 hours |
| **Patch Compliance (Endpoints)** | < 80% | 80-90% | 90-95% | > 95% |
| **EDR Coverage** | < 85% | 85-95% | 95-99% | 100% |
| **Phishing Click Rate** | > 15% | 8-15% | 3-8% | < 3% |
| **Training Completion** | < 85% | 85-95% | 95-99% | 100% |
| **Control Health Score** | < 80% | 80-90% | 90-95% | > 95% |
| **Evidence Freshness** | < 80% | 80-90% | 90-95% | 100% |
| **Vendor Assessment Completion** | < 70% | 70-85% | 85-95% | > 95% |

These benchmarks should be used directionally, not as absolute standards. A healthcare organization handling PHI should target best-in-class for access control metrics. A pre-revenue startup pursuing its first SOC 2 should target "above average" as an initial milestone and improve from there.

The most important comparison is not against industry benchmarks but against your own historical performance. A company that reduces its critical vulnerability MTTR from 45 days to 20 days in six months is making meaningful progress, even if the absolute number is still above the industry benchmark.

---

## Common Security Metrics Mistakes

After working with hundreds of organizations on their compliance and security measurement programs, the following mistakes appear with striking regularity.

### Measuring activity instead of outcomes

Counting the number of vulnerability scans run is an activity metric. Measuring the percentage of vulnerabilities remediated within SLA is an outcome metric. Activity metrics tell you that the team is busy. Outcome metrics tell you that the program is working. Every metric on your dashboard should answer the question "is this program achieving its objective?" -- not "is this team doing work?"

### Tracking too many metrics

A dashboard with 50 metrics is not a dashboard -- it is a data dump. Nobody will look at it. The operational team should track 15-25 metrics across all domains. The tactical dashboard should present 10-15. The board should see no more than 10. If a metric is not driving a decision or satisfying an audit requirement, remove it.

### No defined thresholds or targets

A metric without a target is a number. It provides no information about whether performance is acceptable. Every metric must have a defined target (green), a warning threshold (amber), and a critical threshold (red). These thresholds should be documented, approved by management, and reviewed annually. Without thresholds, nobody knows whether a 12-day critical vulnerability MTTR is a success or a failure.

### Inconsistent calculation methodology

If the MTTR calculation changes quarter to quarter -- sometimes including weekends, sometimes not; sometimes counting from scan date, sometimes from CVE publication date -- the trend data is meaningless. Document the formula, the data sources, and the inclusion/exclusion criteria for every metric. Lock the methodology and do not change it without documenting the change and restating historical data.

### Reporting without context

"Our phishing click rate is 8%." Is that good? Bad? Improving? Worsening? How does it compare to last quarter? To the industry? To our target? Every metric presented to any audience should include: the current value, the trend (improving/stable/worsening), the target, and, for executive audiences, the industry benchmark.

### Ignoring manual controls

Automated security controls are easy to measure because tools generate the data. Manual controls -- access reviews, policy reviews, vendor assessments, security training -- are harder to measure but equally important to auditors. A metrics program that only tracks automated controls will have blind spots exactly where auditors look most carefully.

### Gaming the metrics

When metrics are tied to team performance evaluations without proper context, teams optimize for the metric rather than the outcome. A vulnerability management team that closes vulnerability tickets without verifying remediation will show excellent MTTR numbers and terrible actual security. A security awareness team that sends only easy phishing simulations will show improving click rates while the workforce remains vulnerable to real attacks. Metrics must be validated, and the validation process must be independent of the team being measured.

---

## Frequently Asked Questions

### What are the most important security metrics for a startup pursuing its first SOC 2 audit?

Focus on five metrics initially: vulnerability MTTR by severity (demonstrates your vulnerability management program is operational), MFA adoption rate (demonstrates access control enforcement), training completion rate (demonstrates security awareness program operation), control health score (demonstrates ongoing monitoring), and evidence freshness (demonstrates continuous evidence collection). These five metrics cover the areas most commonly flagged by SOC 2 auditors and can be tracked with minimal tooling. Expand your metrics program as the security function matures.

### How often should security metrics be reviewed?

Operational metrics should be reviewed daily by the security team. Tactical metrics should be reviewed weekly by security leadership and monthly for trend analysis and reporting. Strategic metrics should be reviewed monthly by the CISO and presented quarterly to the board of directors. ISO 27001 Clause 9.3 requires management review at planned intervals -- most organizations conduct this quarterly, using the management review meeting to formally review security metrics and document resulting decisions.

### What is a good security metrics dashboard tool?

The best tool is the one your team will actually use. For operational dashboards, use the native interfaces of your security tools (SIEM, EDR, vulnerability scanner). For tactical and compliance dashboards, a compliance automation platform like QuickTrust provides out-of-the-box metrics dashboards mapped to framework requirements. For executive reporting, a slide deck updated monthly from compliance platform data is often more effective than an interactive dashboard that executives will never log into. Avoid building custom dashboards from scratch unless you have a dedicated data engineering team to maintain them.

### How do security metrics differ from security KPIs?

A metric is any quantitative measurement of a security-related activity or outcome. A KPI (Key Performance Indicator) is a metric that has been designated as a key indicator of program performance and has a defined target. All KPIs are metrics, but not all metrics are KPIs. Your vulnerability management program might track 15 metrics, but only MTTR by severity and SLA compliance rate might be designated as KPIs -- the two numbers that, if they are on target, indicate the program is healthy.

### How do I calculate security ROI for executive reporting?

Security ROI is inherently difficult because it requires quantifying the cost of events that did not happen. The most credible approach is risk reduction measurement: calculate the annualized loss expectancy (ALE) for key risk scenarios before and after security investments, and present the delta as the return. For compliance-specific ROI, calculate the cost of audit preparation time before and after implementing a compliance automation platform, the cost of delayed deals due to missing compliance certifications, and the cost of audit findings remediation. Our [compliance as a revenue enabler guide](/compliance-roi-enterprise-deals) provides a detailed framework for this calculation.

### What metrics should I present to cyber insurance underwriters?

Cyber insurance underwriters increasingly request quantitative security data during the application and renewal process. The metrics most commonly requested are: MFA adoption rate (especially for privileged accounts and remote access), endpoint detection and response coverage, patch compliance rate (especially for critical and internet-facing systems), mean time to detect and respond to incidents, backup testing frequency and success rate, phishing simulation results, vulnerability scan cadence and MTTR, and security awareness training completion rate. Present these with 12-month trend data to demonstrate program maturity and improvement.

### How do I handle months with zero incidents in my incident response metrics?

Zero-incident months are normal for smaller organizations and do not invalidate your incident response metrics program. Report zero-incident months as zero -- do not omit them from dashboards or trend data. For MTTD and MTTR calculations, use only months where incidents occurred. Supplement incident metrics with incident response preparedness metrics during low-incident periods: tabletop exercise completion, playbook review dates, on-call rotation coverage, and tool integration testing results. This demonstrates that the incident response capability is maintained even when incidents are infrequent.

### What is the relationship between security metrics and risk management?

Security metrics are the quantitative foundation of your risk management program. Risk assessments identify threats and vulnerabilities. Security metrics measure how effectively your controls mitigate those risks over time. A risk register might identify "delayed vulnerability remediation" as a risk with a likelihood of 3/5 and impact of 4/5. The vulnerability MTTR metric provides ongoing, quantitative evidence of whether that risk is being adequately controlled. When MTTR exceeds the target threshold, the risk level increases. When MTTR meets the target, the risk is controlled within tolerance. For a complete guide to risk management frameworks, see our [risk management framework guide](/risk-management-framework-guide).

---

## Measure What Matters with QuickTrust

Security metrics are not a reporting exercise -- they are the mechanism by which security programs demonstrate their value, satisfy auditors, communicate risk to leadership, and continuously improve. Without metrics, you are operating on intuition. With the right metrics, measured consistently and reported to the right audiences, you have a security program that is transparent, accountable, and defensible.

QuickTrust was built to make security measurement automatic. The platform connects to your cloud infrastructure, identity provider, endpoint management, vulnerability scanner, HR system, and development tools. It calculates control health scores, evidence freshness, compliance posture, and program metrics in real time -- mapped to every framework you operate against. When it is time to report to the board, the data is already assembled: current, accurate, and presented at the right level of abstraction.

No more pulling data from six different tools into a spreadsheet. No more inconsistent calculations. No more audit-season scrambles to reconstruct metrics that should have been tracked continuously.

**[Start your free QuickTrust trial](https://quicktrustapp.com)** and see what a metrics-driven security program looks like when measurement is built into the platform, not bolted on afterward.

---

### Related Resources

- [Compliance Monitoring: How to Build a Continuous Monitoring Program](/compliance-monitoring-guide)
- [How to Build a Vulnerability Management Program That Passes Compliance Audits](/vulnerability-management-program-guide)
- [How to Build an Incident Response Plan That Passes Every Compliance Audit](/incident-response-plan-compliance-guide)
- [Vendor Risk Management: The Complete Program Guide](/vendor-risk-management-complete-guide)
- [Third-Party Risk Assessment: The Complete Guide](/third-party-risk-assessment-guide)
- [The Complete SOC 2 Compliance Guide for SaaS Startups](/soc-2-compliance)
- [ISO 27001 Certification: The Complete Implementation Guide](/iso-27001-certification)
- [HIPAA Compliance for Healthcare SaaS Companies](/hipaa-compliance)
- [Security Awareness Training: The Complete Guide](/security-awareness-training-guide)
- [Risk Management Framework: The Complete Guide](/risk-management-framework-guide)
- [Information Security Policy: The Complete Guide](/information-security-policy-guide)
- [Compliance as a Revenue Enabler](/compliance-roi-enterprise-deals)
