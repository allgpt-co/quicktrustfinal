---
meta_description: "Build an incident response plan that satisfies SOC 2, ISO 27001, HIPAA, and PCI DSS auditors. Step-by-step template with roles, phases, and real-world examples."
target_keyword: "incident response plan"
secondary_keywords: "incident response plan template, incident response procedure, security incident response, incident response framework, cyber incident response plan"
word_count_target: 4500+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-19
---

# How to Build an Incident Response Plan That Passes Every Compliance Audit (SOC 2, ISO 27001, HIPAA, PCI DSS)

The average cost of a data breach in 2025 reached $4.88 million globally, according to IBM's annual Cost of a Data Breach Report. But buried in that same report is a statistic that should change how every security team allocates its time: organizations with a tested incident response plan saved an average of $1.49 million per breach compared to those without one.

That is not a marginal improvement. It is the difference between a breach that threatens the business and one that the business can absorb. And yet, when auditors arrive to assess SOC 2, ISO 27001, HIPAA, or PCI DSS compliance, the incident response plan is one of the most common areas where companies fall short. Not because they lack one entirely, but because what they have does not meet the bar. The plan is a five-page document that no one has tested, with outdated contact information, no severity classification scheme, and no documented connection to regulatory notification requirements.

This guide walks through how to build an incident response plan that does two things simultaneously: it actually works during a real security incident, and it passes the scrutiny of every major compliance framework audit. Those two objectives are not in conflict. An IRP that satisfies auditors but fails during an actual incident is worthless. An IRP that works in practice but lacks the documentation auditors need will generate findings. The goal is to build one plan that does both.

---

## What Is an Incident Response Plan?

An incident response plan is a documented, structured approach for detecting, responding to, containing, and recovering from security incidents. It defines who does what, when, and how when something goes wrong — whether that is a ransomware attack, an unauthorized data exposure, a misconfigured cloud resource leaking customer data, or an employee clicking a phishing link that compromises credentials.

The IRP is not a single document sitting on a shelf. At maturity, it is a system: a master plan supported by playbooks for specific incident types, a communication plan, a severity classification matrix, escalation procedures, and evidence collection templates. It names real people, references real tools, and has been tested under conditions that approximate real incidents.

### Why an IRP matters beyond compliance

An incident response plan reduces breach costs, but it does more than that:

- **Speed of containment.** The average time to identify and contain a breach is 258 days. Organizations with a tested IRP cut that timeline substantially, and every day of containment delay increases cost.
- **Legal exposure.** A documented, followed IRP demonstrates reasonable care — a critical legal standard in breach litigation and regulatory enforcement actions. A company that can show it had a plan, followed the plan, and notified affected parties within required timelines is in a fundamentally different legal position than one that improvised.
- **Customer retention.** How a company handles an incident matters more to customers than whether the incident occurred. A coordinated, transparent response preserves trust. A chaotic, delayed response destroys it.
- **Insurance coverage.** Cyber insurance underwriters increasingly require evidence of a tested IRP as a condition of coverage. Claims may be denied if the insured cannot demonstrate that an IRP existed and was followed.

---

## Why Every Compliance Framework Requires an IRP

Every major compliance framework includes specific requirements for incident response. This is not coincidental — incident response is one of the few controls that auditors universally treat as non-negotiable. A company can have minor gaps in access control documentation or incomplete asset inventories and still pass an audit. A company without an incident response plan will not.

Here is where each framework sets its requirements:

### SOC 2 (Trust Services Criteria)

SOC 2 addresses incident response across several Common Criteria:

- **CC7.2 — Monitoring for anomalies and indicators of compromise.** The organization monitors system components and the operation of those components for anomalies that are indicative of malicious acts, natural disasters, and errors affecting the entity's ability to meet its objectives.
- **CC7.3 — Evaluation of events to determine whether they are incidents.** The organization evaluates events to determine whether they constitute security incidents.
- **CC7.4 — Response to identified security incidents.** The organization responds to identified security incidents by executing a defined incident response program to understand, contain, remediate, and communicate security incidents, as appropriate.
- **CC7.5 — Recovery from identified security incidents.** The organization identifies, develops, and implements activities to recover from identified security incidents.

What auditors specifically examine: documented IRP with defined roles, evidence of IRP testing (tabletop exercises), evidence of actual incident handling (if incidents occurred during the audit period), and post-incident review documentation.

### ISO 27001 (Annex A Controls)

ISO 27001:2022 dedicates five controls to incident management:

- **A.5.24 — Information security incident management planning and preparation.** Requires a documented approach for managing information security incidents, including defined responsibilities and procedures.
- **A.5.25 — Assessment and decision on information security events.** Requires evaluation of information security events to classify them as incidents.
- **A.5.26 — Response to information security incidents.** Requires response according to documented procedures.
- **A.5.27 — Learning from information security incidents.** Requires that knowledge from incidents is used to strengthen controls and reduce future incidents.
- **A.5.28 — Collection of evidence.** Requires procedures for identification, collection, acquisition, and preservation of evidence related to information security events.

Certification auditors will ask to see the documented plan, evidence of management review, training records, and post-incident analysis reports.

### HIPAA (Security Rule)

HIPAA is direct and non-negotiable:

- **Section 164.308(a)(6)(i) — Security Incident Procedures.** Covered entities and business associates must implement policies and procedures to address security incidents.
- **Section 164.308(a)(6)(ii) — Response and Reporting.** Requires identifying and responding to suspected or known security incidents, mitigating harmful effects, and documenting incidents and their outcomes.

For breaches involving unsecured Protected Health Information (PHI), HIPAA's Breach Notification Rule (Section 164.400-414) imposes strict notification timelines: individual notification within 60 days of discovery, HHS notification within 60 days (or annually for breaches affecting fewer than 500 individuals), and media notification for breaches affecting 500+ individuals in a state or jurisdiction.

### PCI DSS (Requirement 12.10)

PCI DSS v4.0 Requirement 12.10 is among the most prescriptive incident response requirements of any framework:

- **12.10.1 — Establish an incident response plan.** The plan must be ready to activate immediately upon breach detection. PCI DSS specifies the plan must include roles, responsibilities, communication strategies, notification requirements, specific incident response procedures, business recovery and continuity procedures, data backup processes, legal requirements for reporting compromises, and coverage for all critical system components.
- **12.10.2 — Review and test the plan at least annually.**
- **12.10.3 — Designate specific personnel to be available on a 24/7 basis to respond to alerts.**
- **12.10.4 — Provide appropriate training to staff with security breach response responsibilities.**
- **12.10.4.1 — Perform periodic training for incident response personnel.** (New in v4.0)
- **12.10.5 — Include alerts from security monitoring systems in the incident response plan.**
- **12.10.6 — Develop a process to modify and evolve the incident response plan per lessons learned and industry developments.**
- **12.10.7 — Have incident response procedures in place for detection of stored PAN anywhere it is not expected.** (New in v4.0)

PCI DSS assessors (QSAs) will request documentation of the plan, evidence of annual testing, 24/7 coverage assignments, and training records.

---

## The 6 Phases of Incident Response

The industry-standard incident response framework comes from NIST Special Publication 800-61 Revision 2, "Computer Security Incident Handling Guide." It defines six phases that form a cycle — because lessons learned from one incident feed directly into preparation for the next.

### Phase 1: Preparation

Preparation is everything that happens before an incident occurs. It is, by a significant margin, the phase where the highest-leverage work happens.

**What preparation includes:**

- Establishing and training the incident response team (IRT)
- Documenting the IRP, playbooks, and communication procedures
- Deploying detection and monitoring tools (SIEM, EDR, IDS/IPS, cloud security monitoring)
- Creating evidence preservation procedures and chain-of-custody templates
- Establishing communication channels that remain available during an incident (out-of-band communication — do not rely solely on corporate email if email may be compromised)
- Conducting tabletop exercises and simulations at least annually
- Maintaining a current contact list for internal responders, external counsel, forensics vendors, law enforcement contacts, and regulatory notification contacts
- Securing forensic tools, network diagrams, and system architecture documentation where the response team can access them during an incident

**Audit evidence produced:** Documented IRP, training records, tabletop exercise reports, tool inventory, contact lists.

### Phase 2: Identification (Detection and Analysis)

Identification is the process of detecting that a security event has occurred and determining whether it qualifies as an incident requiring formal response.

**What identification includes:**

- Monitoring alerts from SIEM, EDR, intrusion detection systems, cloud security posture management (CSPM), and application-level logging
- Correlating events from multiple sources to identify attack patterns
- Triaging alerts to distinguish actual incidents from false positives
- Classifying the incident by severity (see Severity Classification section below)
- Documenting the initial indicators of compromise (IOCs), affected systems, and timeline
- Formally declaring an incident and activating the IRP

**Key considerations:** The identification phase is where most organizations lose time. Alert fatigue — the overwhelming volume of false positives — causes teams to miss genuine incidents or respond too slowly. Your IRP should define specific thresholds and criteria for when an event becomes an incident and who has the authority to declare one.

**Audit evidence produced:** Alert logs, triage documentation, incident declaration record with timestamp, initial severity classification.

### Phase 3: Containment

Containment prevents the incident from spreading further while preserving evidence for investigation. NIST distinguishes between short-term containment (immediate actions to stop the bleeding) and long-term containment (sustained measures while you prepare for eradication).

**Short-term containment examples:**

- Isolating affected systems from the network
- Blocking malicious IP addresses or domains at the firewall
- Disabling compromised user accounts
- Revoking compromised API keys or access tokens
- Activating break-glass procedures for critical systems

**Long-term containment examples:**

- Standing up clean systems to replace compromised ones
- Applying temporary firewall rules or network segmentation
- Implementing enhanced monitoring on systems adjacent to the compromise
- Redirecting traffic away from affected systems

**Critical rule:** Before taking containment actions, capture forensic images and volatile data (memory dumps, running processes, network connections) from affected systems. Containment actions alter or destroy evidence. An IRP that prescribes immediate system wipes without evidence preservation will create problems for forensic investigation, legal proceedings, and regulatory reporting.

**Audit evidence produced:** Containment action log with timestamps and responsible parties, forensic image hash values, network isolation records.

### Phase 4: Eradication

Eradication removes the root cause of the incident from the environment.

**What eradication includes:**

- Removing malware, backdoors, and unauthorized access mechanisms
- Patching the vulnerability that was exploited
- Resetting all compromised credentials (not just the ones you know about — assume lateral movement occurred)
- Reviewing all systems that had connectivity to compromised assets for additional indicators
- Verifying that the attacker's access has been fully removed through threat hunting

**Common mistake:** Declaring eradication complete too early. If the attacker established persistence mechanisms (scheduled tasks, cron jobs, additional user accounts, modified system binaries) that were not found, they will regain access. Thorough eradication requires systematic verification.

**Audit evidence produced:** Root cause analysis, remediation action log, vulnerability patch records, credential reset confirmation.

### Phase 5: Recovery

Recovery restores affected systems and services to normal operation, with enhanced monitoring to confirm the incident has been fully resolved.

**What recovery includes:**

- Restoring systems from clean backups (verified clean — not from a backup taken after the compromise began)
- Gradually bringing systems back online in a controlled sequence
- Implementing enhanced monitoring and alerting for indicators of the same attack pattern
- Validating system integrity before returning to production
- Confirming that business operations have resumed and customers are unaffected (or have been appropriately notified)

**Key principle:** Recovery should be gradual and monitored. Do not restore all systems simultaneously. Bring them back in order of business priority, monitor each for signs of re-infection, and validate functionality before proceeding to the next.

**Audit evidence produced:** System restoration logs, backup verification records, enhanced monitoring configuration, business resumption confirmation.

### Phase 6: Lessons Learned (Post-Incident Review)

The lessons learned phase — sometimes called the post-incident review or retrospective — is the phase that auditors care about most after the plan itself. It is also the phase that organizations most frequently skip.

**What the post-incident review must cover:**

- Complete incident timeline from initial detection to full recovery
- What happened, how it happened, and why existing controls did not prevent it
- What the team did well
- What the team could improve
- Specific, assigned, deadline-bound action items for improvements
- Whether the IRP itself needs to be updated based on the incident
- Metrics: time to detect, time to contain, time to eradicate, time to recover, total cost

**When to conduct it:** Within 5-10 business days of incident closure, while details are still fresh. Do not let it slip to "when things calm down" — it will never happen.

**Audit evidence produced:** Post-incident review report, updated IRP (if changes were made), action item tracking with completion status.

---

## Building Your Incident Response Team: Roles and Responsibilities

An incident response plan without named roles is a document, not a plan. Every IRP must define who fills each role, who their backup is, and what authority each role carries.

### Incident Commander (IC)

The Incident Commander owns the overall response. They make decisions about containment strategy, resource allocation, escalation, and communication timing. During an active incident, the IC has authority to make operational decisions without waiting for normal approval chains.

**Typical assignment:** Director of Security, VP of Engineering, or CISO. For smaller companies without these roles, a senior engineer or CTO may serve as IC.

**Key responsibilities:**
- Declare and classify the incident
- Assemble the response team
- Make containment and escalation decisions
- Coordinate across all workstreams (technical, communication, legal)
- Ensure documentation is maintained throughout the incident
- Authorize public communication
- Close the incident and initiate post-incident review

### Security Lead / Technical Lead

The Security Lead directs the technical investigation and remediation. They determine the attack vector, scope of compromise, and technical containment and eradication strategy.

**Typical assignment:** Senior security engineer, security architect, or lead infrastructure engineer.

**Key responsibilities:**
- Lead the technical investigation
- Identify the attack vector and indicators of compromise
- Direct containment actions
- Oversee evidence preservation and forensic analysis
- Coordinate with external forensics vendors if engaged
- Provide technical status updates to the Incident Commander

### Communications Lead

The Communications Lead manages all internal and external communications related to the incident. They draft customer notifications, coordinate with marketing and PR, and manage regulatory notification content.

**Typical assignment:** Head of Communications, VP of Marketing, or Chief of Staff. In smaller companies, this may fall to the CEO or a designated executive.

**Key responsibilities:**
- Draft internal communications (employee notifications, leadership updates)
- Draft external communications (customer notifications, press statements)
- Coordinate with Legal on regulatory notification content and timing
- Manage incoming inquiries from customers, press, and partners
- Maintain a communication log

### Legal Counsel

Legal Counsel advises on regulatory notification obligations, liability exposure, law enforcement engagement, and communications review.

**Typical assignment:** General Counsel or outside counsel with cybersecurity and data privacy expertise.

**Key responsibilities:**
- Determine regulatory notification obligations (which laws apply, which regulators must be notified, on what timeline)
- Review all external communications for legal risk
- Advise on law enforcement engagement
- Manage attorney-client privilege considerations for the investigation
- Coordinate with cyber insurance carrier

### Engineering / Operations

The engineering team executes the technical containment, eradication, and recovery actions under the direction of the Security Lead.

**Typical assignment:** DevOps engineers, site reliability engineers, system administrators, and application developers as needed.

**Key responsibilities:**
- Execute containment actions (network isolation, credential revocation, system shutdown)
- Perform evidence collection (log exports, forensic imaging)
- Execute eradication steps (patching, malware removal, credential resets)
- Restore systems from clean backups
- Implement enhanced monitoring during recovery

### On-Call and Escalation

Your IRP must define 24/7 on-call coverage with clear escalation timelines. A security incident at 2 AM on a Saturday should not wait until Monday morning because no one knew who to call.

**Minimum requirements:**
- Primary and secondary on-call for each role
- Contact information for all team members (phone numbers — not just Slack or email)
- Maximum response time for each severity level (e.g., Sev 1: 15 minutes, Sev 2: 1 hour)
- Automatic escalation if the primary does not respond within the defined window

---

## What Your IRP Must Include to Pass Audits

Each framework has specific expectations. This checklist consolidates the requirements across SOC 2, ISO 27001, HIPAA, and PCI DSS. If your IRP addresses every item on this list, it will satisfy the incident response requirements of all four frameworks.

### Universal IRP Checklist

| Requirement | SOC 2 | ISO 27001 | HIPAA | PCI DSS |
|---|---|---|---|---|
| Documented incident response plan | CC7.4 | A.5.24 | 164.308(a)(6) | 12.10.1 |
| Defined roles and responsibilities | CC7.4 | A.5.24 | 164.308(a)(6) | 12.10.1 |
| Incident classification/severity scheme | CC7.3 | A.5.25 | Required | 12.10.1 |
| Containment procedures | CC7.4 | A.5.26 | 164.308(a)(6)(ii) | 12.10.1 |
| Evidence collection procedures | CC7.4 | A.5.28 | Required | 12.10.5 |
| Regulatory notification procedures | CC7.4 | A.5.24 | 164.400-414 | 12.10.1 |
| Customer notification procedures | CC7.4 | A.5.24 | 164.404 | 12.10.1 |
| Business recovery procedures | CC7.5 | A.5.26 | 164.308(a)(7) | 12.10.1 |
| Post-incident review process | CC7.5 | A.5.27 | Required | 12.10.6 |
| Annual plan testing | CC7.4 | A.5.24 | Recommended | 12.10.2 |
| 24/7 response capability | CC7.4 | A.5.24 | Required | 12.10.3 |
| Personnel training records | CC1.4 | A.6.3 | 164.308(a)(5) | 12.10.4 |
| Integration with monitoring/alerting | CC7.2 | A.8.16 | 164.312(b) | 12.10.5 |
| Plan update/evolution process | CC7.5 | A.5.27 | Required | 12.10.6 |

### Framework-Specific Requirements

**HIPAA-specific:** Your IRP must explicitly address breaches involving Protected Health Information (PHI), including the breach risk assessment methodology (the four-factor test from 45 CFR 164.402), individual notification requirements, HHS notification procedures, and media notification triggers. If you process PHI, your IRP must have a PHI-specific playbook. For more on HIPAA requirements, see our [HIPAA Compliance Guide](/hipaa-compliance).

**PCI DSS-specific:** Your IRP must cover detection of stored primary account numbers (PAN) in unauthorized locations (Requirement 12.10.7 — new in PCI DSS v4.0), and must include alerts from security monitoring systems as trigger events. Annual testing is explicitly required, not just recommended.

**ISO 27001-specific:** The IRP must be integrated into the broader Information Security Management System (ISMS). Auditors will check that the IRP references the risk assessment, that incident classifications align with the risk register, and that lessons learned feed back into the risk treatment plan. Read our [ISO 27001 Certification Guide](/iso-27001-certification) for context on how incident response fits into ISMS implementation.

**SOC 2-specific:** Auditors will examine not just the plan but evidence of its operation. If security events occurred during the audit period, the auditor will request documentation showing how those events were handled, even if they were ultimately classified as non-incidents. The [SOC 2 Compliance Guide](/soc-2-compliance) covers the full Common Criteria context.

---

## Incident Severity Classification: How to Categorize Incidents

A severity classification scheme is essential for two reasons: it determines the speed and scale of the response, and it provides auditors with evidence that your organization systematically prioritizes incidents rather than treating all events identically.

### Severity 1 (Critical)

**Definition:** Active, confirmed compromise with material impact to customers, data, or business operations. Immediate threat to confidentiality, integrity, or availability of production systems or sensitive data.

**Examples:**
- Active ransomware spreading across production infrastructure
- Confirmed exfiltration of customer PII, PHI, or cardholder data
- Complete loss of production system availability
- Unauthorized access to production databases containing sensitive data
- Compromise of the CI/CD pipeline or code signing infrastructure

**Response requirements:**
- All hands on deck — full IRT activation within 15 minutes
- Incident Commander and Security Lead engaged immediately
- Legal Counsel notified within 1 hour
- Executive leadership briefed within 2 hours
- Status updates every 30 minutes until containment
- External forensics firm engaged if internal capacity is insufficient

### Severity 2 (High)

**Definition:** Confirmed security incident with potential for significant impact, but the blast radius is currently limited or the incident is contained to non-production systems.

**Examples:**
- Compromised employee credentials with access to sensitive systems (contained before lateral movement confirmed)
- Successful phishing attack compromising a single user account
- Unauthorized access to staging or development environments containing copies of production data
- Vulnerability actively exploited in the wild that affects your exposed systems, but no confirmed compromise yet
- Security misconfiguration exposing non-sensitive data

**Response requirements:**
- Core IRT activation within 1 hour
- Incident Commander and Security Lead engaged within 1 hour
- Legal Counsel notified within 4 hours
- Status updates every 2 hours until containment
- Post-incident review required

### Severity 3 (Medium)

**Definition:** Security event that requires investigation and response but does not pose an immediate threat to sensitive data or production availability.

**Examples:**
- Malware detected and quarantined on a single endpoint (no lateral movement)
- Failed brute-force attack against an externally facing service
- Unauthorized software installed on a corporate device
- Policy violation detected (e.g., data transferred to an unauthorized personal device)
- Anomalous but unexplained activity in logs that requires investigation

**Response requirements:**
- Investigation initiated within 4 hours during business hours
- Security Lead assesses and directs investigation
- Resolution within 48 hours
- Documented in the incident tracking system
- Post-incident review at team discretion

### Severity 4 (Low / Informational)

**Definition:** Security event that is notable and should be documented but does not require immediate response.

**Examples:**
- Automated vulnerability scan detecting known, low-risk vulnerabilities
- Blocked phishing email that was not opened or interacted with by any user
- Minor policy deviation that was self-corrected
- Security awareness training test failure (simulated phishing click)

**Response requirements:**
- Logged in the incident tracking system
- Addressed during normal business operations
- No IRT activation required
- Tracked for trend analysis

---

## Communication and Escalation Procedures

Communication failures during an incident cause more organizational damage than technical failures. Your IRP must define exactly who communicates what, to whom, and when.

### Internal Communication

**During the incident:**

- **IRT communication channel:** Establish a dedicated, out-of-band communication channel before an incident occurs. A dedicated Slack channel or Microsoft Teams channel is acceptable for most incidents, but for Sev 1 incidents, have a phone bridge or conferencing line as a backup. If the incident involves compromise of your primary communication platform, you need a fallback (e.g., Signal group, dedicated Zoom bridge, or a phone tree).
- **Leadership updates:** Sev 1 incidents require executive briefings within 2 hours and regular updates. Sev 2 incidents require leadership notification within 4 hours. Define who gives the briefing (typically the Incident Commander) and what format it follows.
- **Company-wide communication:** Employees need to know what is happening — not necessarily the technical details, but what they should and should not do. Should they change their passwords? Avoid accessing certain systems? Refrain from discussing the incident externally? The Communications Lead drafts this, the IC approves it.

### Customer Notification

When an incident affects customer data or service availability, customer notification is both a legal obligation and a trust obligation. Your IRP must define:

- **Threshold for customer notification:** What criteria trigger a customer notification? Any incident involving customer data? Only confirmed breaches? Only incidents affecting specific data types?
- **Notification timeline:** Within 72 hours of confirmation is a common best practice (and a legal requirement under GDPR). HIPAA requires notification within 60 days of discovery. Your contracts may have tighter SLAs.
- **Notification content:** What happened, what data was affected, what you are doing about it, and what customers should do (e.g., monitor accounts, rotate credentials). Have a template drafted and approved by Legal before an incident occurs.
- **Notification channel:** Email, in-app notification, status page, or dedicated incident communication page.

### Regulatory Notification Timelines

This is where organizations most frequently make errors — either missing deadlines or notifying the wrong regulator. Your IRP must include a reference table:

| Regulation | Notification Deadline | Who to Notify | Threshold |
|---|---|---|---|
| HIPAA Breach Notification Rule | 60 days from discovery | HHS (OCR), affected individuals, media (if 500+ in a state) | Breach of unsecured PHI |
| GDPR (Article 33/34) | 72 hours from awareness | Supervisory authority; data subjects if high risk | Personal data breach |
| PCI DSS / Card Brand Rules | Immediately | Acquiring bank, card brands (Visa, Mastercard incident response teams) | Compromise of cardholder data |
| SEC Cybersecurity Rules | 4 business days from materiality determination | SEC (Form 8-K) | Material cybersecurity incident (public companies) |
| State Breach Notification Laws | Varies (30-90 days, depending on state) | State Attorney General, affected residents | Breach of personal information as defined by state law |
| CCPA/CPRA | Without unreasonable delay | California AG, affected consumers | Breach of personal information |

**Important:** Multiple regulations may apply to the same incident. A healthcare SaaS company that processes payments may need to notify HHS under HIPAA, the acquiring bank under PCI DSS, and the state AG under state breach notification laws — all with different timelines and content requirements. Your IRP should include a decision tree for determining which notifications apply.

---

## Incident Response Plan Template: Section-by-Section Breakdown

This section provides a practical walkthrough of every section your IRP should contain. Use this as a template skeleton and customize it for your organization.

### Section 1: Purpose and Scope

Define what the plan covers, what systems are in scope, and what types of events it applies to. Be specific. A vague scope ("this plan covers all security incidents") is less useful than a defined scope ("this plan covers security incidents affecting the production environment, corporate IT systems, and employee devices used to access company data").

**Must include:**
- Purpose statement
- Systems and environments in scope
- Types of incidents covered (security, privacy, availability)
- Applicable regulatory frameworks
- Relationship to other plans (Business Continuity Plan, Disaster Recovery Plan)

### Section 2: Definitions

Define key terms to eliminate ambiguity during a high-stress incident. At minimum:

- **Security Event:** An observable occurrence in a system or network.
- **Security Incident:** A security event that violates security policy or poses an actual threat to the confidentiality, integrity, or availability of information assets.
- **Breach:** A confirmed incident resulting in unauthorized access to or disclosure of protected data.
- **Indicators of Compromise (IOC):** Artifacts or evidence that suggest a system has been compromised.

### Section 3: Roles, Responsibilities, and Contact Information

List every IRT role (as defined in the Roles section above), including:
- Primary assignee (name, title, phone, email)
- Backup assignee
- Escalation path if neither responds within the defined window
- Authority level for each role

Include external contacts: outside legal counsel, forensic investigation firm (have a retainer in place before you need them), cyber insurance carrier claims line, law enforcement contacts (FBI field office, local CISA contact), and regulatory notification contacts.

### Section 4: Severity Classification Matrix

Include the full severity classification scheme (Sev 1 through Sev 4) with definitions, examples, response time requirements, and escalation rules for each level.

### Section 5: Detection and Analysis Procedures

Document how incidents are detected, how events are triaged, and who has the authority to declare an incident. Include:
- Monitoring tools and alert sources
- Triage workflow (who reviews alerts, what criteria they use)
- Incident declaration criteria and authority
- Initial documentation requirements

### Section 6: Containment, Eradication, and Recovery Procedures

Document procedures for each phase, including:
- Evidence preservation requirements (before containment actions)
- Short-term and long-term containment strategies
- Eradication verification procedures
- Recovery sequencing and validation
- Enhanced monitoring during recovery

### Section 7: Communication Plan

Include templates for:
- Internal status update (format, frequency, distribution)
- Executive briefing (format, content, frequency)
- Customer notification (draft template reviewed by Legal)
- Regulatory notification (specific forms and portals for each applicable regulation)
- Media statement (if applicable)

### Section 8: Evidence Collection and Preservation

Document chain-of-custody procedures, forensic imaging protocols, log retention requirements, and how evidence is stored and secured. This section directly supports ISO 27001 A.5.28 and is critical for legal proceedings.

### Section 9: Post-Incident Review Process

Define when the review occurs, who participates, what the review covers, and how action items are tracked to completion. Include a post-incident review template.

### Section 10: Plan Maintenance

Define review and update frequency (at least annually, and after every significant incident), version control, approval requirements, and distribution.

---

## Testing Your IRP: Tabletop Exercises and Simulations

An untested incident response plan is a hypothesis. You do not know whether it works until people have walked through it under conditions that approximate the stress, ambiguity, and time pressure of a real incident.

Auditors across every framework view testing as essential. PCI DSS explicitly requires annual testing (12.10.2). SOC 2 auditors routinely ask for evidence of testing. ISO 27001 auditors assess whether the plan has been validated through exercises.

### Tabletop Exercises

A tabletop exercise is a discussion-based walkthrough of an incident scenario. The IRT gathers (in person or virtually) and works through a realistic scenario step by step, making decisions as they would in a real incident without executing technical actions.

**How to run a tabletop exercise:**

1. **Select a scenario.** Choose a realistic, relevant incident type. Ransomware attack, compromised employee credentials, third-party data breach, insider threat, or cloud misconfiguration exposing data are all strong choices. Rotate scenarios each year.
2. **Prepare injects.** An inject is a new piece of information introduced during the exercise that changes the situation. For example: "The attacker has now moved laterally to the database server." Injects force the team to adapt their response in real time.
3. **Assign a facilitator.** Someone who is not on the IRT runs the exercise, introduces injects, takes notes on decisions, and manages the timeline.
4. **Walk through the scenario.** The facilitator presents the initial scenario. The team discusses and decides on actions. The facilitator introduces injects at planned intervals. Decisions, rationale, and timeline are documented throughout.
5. **Debrief immediately.** After the exercise, conduct a 30-minute debrief: What went well? Where did the team get stuck? Were roles and responsibilities clear? Were there gaps in the plan? Did the communication procedures work?
6. **Document and remediate.** Write an exercise report documenting the scenario, participants, decisions, findings, and remediation items. Track remediation items to completion.

**Tabletop exercise frequency:** At minimum, annually. Best practice is quarterly, with different scenarios each time. New IRT members should participate in an exercise within 90 days of joining.

### Simulated Incidents (Technical Exercises)

For organizations with mature incident response programs, simulated incidents go beyond tabletop discussions. These involve actually executing response procedures: deploying forensic tools, isolating a test system, collecting evidence, restoring from backup. Purple team exercises — where the red team (or a penetration testing firm) executes an attack while the blue team responds — are the most realistic form of IRP testing.

### What to Document for Auditors

After any exercise, create a formal report containing:
- Date, time, duration
- Participants (name, role)
- Scenario description
- Key decisions made and rationale
- Findings (what worked, what did not)
- Action items with owners and deadlines
- Sign-off from the Incident Commander or CISO

This report is your primary audit evidence for IRP testing.

---

## How to Document Incidents for Audit Evidence

When an actual incident occurs, the documentation you produce during the response becomes audit evidence for your next SOC 2, ISO 27001, HIPAA, or PCI DSS assessment. Auditors will request this documentation during the audit period review. Poor documentation during an incident creates audit findings even if the response itself was excellent.

### What to Document During an Incident

Maintain an incident log from the moment the incident is declared until closure. The log should include:

- **Incident ID and declaration timestamp** — assigned as soon as the incident is declared
- **Severity classification** — initial classification and any reclassifications during the incident, with rationale
- **Timeline of events** — every significant event, discovery, decision, and action with timestamps
- **Actions taken** — containment, eradication, and recovery actions with who performed them and when
- **Evidence collected** — list of forensic images, log files, screenshots, and other evidence, with hash values and storage locations
- **Communications sent** — internal updates, executive briefings, customer notifications, regulatory notifications, with timestamps and content
- **Root cause** — what vulnerability or gap was exploited, and why existing controls did not prevent it
- **Impact assessment** — what data was affected, how many records, which customers, what systems
- **Resolution and recovery** — how the incident was resolved, when systems were restored, when the incident was closed

### Incident Documentation Template

Use a structured template so that documentation is consistent across incidents. At minimum:

```
INCIDENT REPORT
===============
Incident ID:            [INC-YYYY-NNN]
Severity:               [Sev 1 / 2 / 3 / 4]
Date Detected:          [Date and time, timezone]
Date Declared:          [Date and time, timezone]
Date Contained:         [Date and time, timezone]
Date Resolved:          [Date and time, timezone]
Incident Commander:     [Name]
Security Lead:          [Name]

SUMMARY
-------
[2-3 sentence summary of the incident]

TIMELINE
--------
[Chronological list of events with timestamps]

ROOT CAUSE ANALYSIS
-------------------
[What happened and why]

IMPACT ASSESSMENT
-----------------
Systems affected:       [List]
Data affected:          [Type, volume, sensitivity]
Customers affected:     [Number, names if applicable]
Regulatory implications: [Which regulations triggered, notifications required]

CONTAINMENT ACTIONS
-------------------
[Numbered list of actions taken with timestamps and responsible parties]

ERADICATION ACTIONS
-------------------
[Numbered list of actions taken]

RECOVERY ACTIONS
----------------
[Numbered list of actions taken]

NOTIFICATIONS SENT
------------------
[Internal, customer, regulatory — with dates and content summaries]

LESSONS LEARNED
---------------
What went well:         [List]
What needs improvement: [List]
Action items:           [List with owners and deadlines]

POST-INCIDENT REVIEW
---------------------
Review date:            [Date]
Participants:           [List]
IRP updates required:   [Yes/No — if yes, describe]
```

### Evidence Retention

Retain incident documentation and evidence for a minimum of:
- **SOC 2:** Duration of the audit period plus the retention period defined in your data retention policy (typically 1-3 years)
- **ISO 27001:** The certification cycle (3 years) at minimum
- **HIPAA:** 6 years from the date of creation or last effective date
- **PCI DSS:** At least 1 year, with 3 months of logs immediately available

Store incident documentation in a secured, access-controlled repository with audit trail logging on who accessed the records.

---

## Common IRP Mistakes That Fail Audits

After reviewing thousands of incident response plans, these are the mistakes that most frequently result in audit findings, exceptions, or failed assessments.

### 1. The Plan Exists But Has Never Been Tested

This is the single most common finding. The IRP was written, approved, and filed. It has never been tested. When the auditor asks for evidence of annual testing, there is none. PCI DSS assessors will issue a finding for Requirement 12.10.2. SOC 2 auditors will note it as a control deficiency. ISO 27001 auditors will cite a nonconformity.

**Fix:** Schedule your first tabletop exercise within 30 days. Put recurring annual exercises on the calendar.

### 2. Outdated Contact Information

The IRP names an Incident Commander who left the company 18 months ago. The phone numbers for outside counsel are wrong. The forensic investigation firm referenced in the plan was never actually retained.

**Fix:** Review and update all contact information quarterly. Include this in your IRP maintenance procedure.

### 3. No Severity Classification Scheme

The plan describes what to do during an incident, but all incidents are treated the same. There is no severity classification, no differentiated response timelines, and no escalation rules based on impact.

**Fix:** Implement the Sev 1-4 classification scheme outlined in this guide. Map response timelines and escalation rules to each level.

### 4. Missing Regulatory Notification Procedures

The plan addresses technical response but does not document when, how, and to whom regulatory notifications must be made. For HIPAA-covered entities, this is a critical gap — the Breach Notification Rule has specific timelines and procedures that must be documented in the IRP.

**Fix:** Build the regulatory notification reference table into your IRP. Assign the Legal Counsel role explicit responsibility for determining notification obligations.

### 5. No Evidence Collection Procedures

The plan directs the team to "collect evidence" but does not specify what evidence to collect, how to preserve chain of custody, where to store forensic images, or what tools to use. When an incident occurs, evidence is overwritten by containment actions before it can be preserved.

**Fix:** Document specific evidence collection procedures, including forensic imaging tools, hash value generation, chain-of-custody forms, and evidence storage requirements.

### 6. No Post-Incident Review Process

Incidents are responded to and resolved, but no formal retrospective occurs. There is no documentation of lessons learned, no analysis of what went wrong, and no updates to the IRP based on the incident experience.

**Fix:** Make post-incident reviews mandatory for all Sev 1 and Sev 2 incidents. Define a template, assign responsibility, and track action items.

### 7. The Plan Does Not Address the Frameworks You Are Audited Against

The IRP is a generic cybersecurity incident response plan that does not reference the specific frameworks the organization is audited against. It does not mention SOC 2 Common Criteria, ISO 27001 Annex A controls, HIPAA breach notification requirements, or PCI DSS reporting obligations.

**Fix:** Map your IRP sections to the specific control requirements of each framework you are subject to. Include an appendix that cross-references IRP sections to framework requirements.

### 8. Roles and Responsibilities Are Vague

The plan says "the security team will handle containment" without naming specific individuals, defining authority, or establishing an escalation chain. When an incident occurs, three people think someone else is in charge.

**Fix:** Name specific people in each role. Define authority levels. Designate backups. Include a RACI matrix if the team is large.

### 9. No Integration with Monitoring and Alerting

The IRP exists as a standalone document, disconnected from the technical monitoring and alerting infrastructure. There is no documentation of which alerts trigger incident response, what thresholds activate the plan, or how monitoring data feeds into the identification phase.

**Fix:** Document the specific alerts and alert sources that feed into incident identification. Map monitoring tools to IRP phases.

### 10. Annual Review Has Not Occurred

The IRP has a stated annual review cycle, but the last review date was two years ago. Auditors check the version history and review date on every policy document. An IRP that was last reviewed outside the review cycle will generate a finding.

**Fix:** Set a calendar reminder for annual IRP review. Document the review even if no changes were made — the record of review is the evidence.

---

## FAQ: Incident Response Plan Compliance Questions

### What is the difference between an incident response plan and a disaster recovery plan?

An incident response plan addresses security incidents — events that compromise the confidentiality, integrity, or availability of information assets through malicious or unauthorized activity. A disaster recovery plan addresses the restoration of IT systems and business operations after any disruption, including natural disasters, hardware failures, and infrastructure outages. The two plans overlap in the recovery phase, but an IRP focuses on investigation, containment, and evidence preservation, while a DRP focuses on restoring systems and maintaining business continuity. Most compliance frameworks require both.

### How often should an incident response plan be tested?

At minimum, annually. PCI DSS Requirement 12.10.2 explicitly mandates annual testing. SOC 2 and ISO 27001 auditors expect at least annual testing. Best practice for organizations with mature security programs is quarterly tabletop exercises with different scenarios. New team members should participate in an exercise within 90 days of assuming their incident response role.

### Does a small startup need an incident response plan?

Yes. If you are pursuing any compliance certification — SOC 2, ISO 27001, HIPAA, or PCI DSS — an IRP is a mandatory requirement. Even without a compliance driver, any company that stores customer data needs an IRP. The plan can be proportional to the organization's size. A 20-person startup does not need the same IRP as a 5,000-person enterprise, but it needs a documented plan with named roles, a severity scheme, and communication procedures.

### What happens during an audit if we had an incident but did not follow our IRP?

This is a serious audit risk. If an incident occurred during the audit period and the organization did not follow its documented IRP, the auditor will likely issue an exception (SOC 2) or nonconformity (ISO 27001). The auditor compares what the plan says should happen against what actually happened. Gaps between documented procedures and actual practice are findings. If the plan was not followed at all, it indicates the plan is ineffective or untested — both of which undermine the control.

### Can one incident response plan cover multiple compliance frameworks?

Yes, and this is the recommended approach. Maintaining separate IRPs for SOC 2, ISO 27001, HIPAA, and PCI DSS creates unnecessary duplication and increases the risk of inconsistency. Build one comprehensive IRP that addresses the most prescriptive requirements across all applicable frameworks, then include a framework mapping appendix that shows how each section of your IRP maps to each framework's specific control requirements.

### Who should own the incident response plan?

The IRP should be owned by the CISO, VP of Security, or the most senior person responsible for information security. In companies without a dedicated security leader, the CTO or VP of Engineering typically owns the IRP. Ownership means accountability for the plan's accuracy, maintenance, testing, and effectiveness — not that the owner writes every word. The owner ensures the plan is current, tested, and approved by executive leadership.

### What tools do we need for incident response?

At minimum: a SIEM or centralized log management platform for detection and investigation, an endpoint detection and response (EDR) solution for endpoint visibility and containment, a secure communication channel for IRT coordination, an incident tracking system (can be as simple as a dedicated Jira project or as sophisticated as a SOAR platform), and forensic imaging tools. You should also have retainer agreements in place with an external forensics firm and outside legal counsel before an incident occurs — you do not want to be negotiating contracts during a breach.

### How do we handle an incident that spans multiple compliance frameworks?

Identify all applicable regulatory notification requirements immediately when the incident is declared. If you process healthcare data (HIPAA), accept payments (PCI DSS), operate in the EU (GDPR), and are a public company (SEC rules), a single breach could trigger four separate notification obligations with different timelines and requirements. Your Legal Counsel role is responsible for mapping the incident to all applicable frameworks and ensuring every notification obligation is met. This is where the regulatory notification reference table in your IRP becomes critical.

---

## Automate Your Incident Response Compliance with QuickTrust

Building an incident response plan that satisfies multiple compliance frameworks is complex. Maintaining it — keeping contact information current, tracking testing schedules, documenting incidents, mapping controls to framework requirements, and producing audit-ready evidence — is an ongoing operational burden.

QuickTrust eliminates that burden. Our platform provides:

- **Pre-built incident response policy templates** mapped to SOC 2, ISO 27001, HIPAA, and PCI DSS requirements — customizable to your organization, not generic boilerplate
- **Automated control mapping** that cross-references your IRP to every applicable framework requirement, so you never miss a control during an audit
- **Continuous compliance monitoring** that tracks whether your IRP is current, tested, and aligned with your active certifications
- **Incident documentation workflows** that guide your team through evidence collection, notification tracking, and post-incident review — producing audit-ready documentation in real time
- **Tabletop exercise management** with scenario libraries, facilitator guides, and exercise report templates

Stop treating incident response compliance as a manual, annual exercise. Start treating it as a continuously monitored, always audit-ready capability.

**[Get started with QuickTrust](https://trust.quickintell.com)** and see how companies like yours build incident response programs that pass every audit — the first time.
