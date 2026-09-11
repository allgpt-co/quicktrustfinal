---
meta_description: "Complete guide to data breach notification requirements across GDPR, HIPAA, state laws, PCI DSS, and SEC rules. Includes notification timelines, templates, and a 72-hour response playbook."
target_keyword: "data breach notification"
secondary_keywords: "data breach notification requirements, breach notification law, data breach notification timeline, data breach reporting, breach notification template"
word_count_target: 4500+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-21
---

# Data Breach Notification Requirements: The Complete Guide to Notification Timelines, Templates, and Compliance Across Every Major Framework

On January 12, 2023, T-Mobile disclosed a data breach affecting 37 million customer accounts. The breach had been ongoing since November 25, 2022 -- 49 days of unauthorized access before detection. On July 26, 2023, the SEC adopted new cybersecurity disclosure rules requiring public companies to report material cyber incidents within four business days. In September 2024, the Irish Data Protection Commission fined Meta 91 million euros for storing hundreds of millions of Facebook and Instagram passwords in plaintext -- a violation discovered five years earlier.

These are not isolated events. They are data points in a regulatory environment that has fundamentally shifted the consequences of getting breach notification wrong. Every major compliance framework, every US state, and an expanding list of international regulators now impose specific, enforceable notification requirements on organizations that experience a data breach. The timelines are short. The penalties for missing them are severe. And the legal landscape is fragmented enough that a single breach can trigger overlapping obligations across three, four, or five different notification regimes simultaneously.

This guide covers every major data breach notification requirement that technology companies face today: what counts as a reportable breach, who must be notified, within what timeframe, what the notification must contain, and what happens when you get it wrong. It includes a step-by-step breach notification playbook, sample notification language, and a framework-by-framework comparison that you can use as a reference during an actual incident.

If you handle personal data, health records, payment card information, or operate as a public company, this guide is your operational reference for breach notification compliance.

---

## What Is a Data Breach Notification?

A data breach notification is a formal communication, required by law or regulation, that informs affected individuals, regulatory authorities, or other designated parties that their personal data has been compromised through unauthorized access, disclosure, acquisition, or destruction.

The obligation to notify is not a courtesy. It is a legal requirement under virtually every privacy and security framework in force today. Failing to notify -- or notifying late -- is itself a violation, independent of the breach that triggered it.

### What counts as a "breach"?

The definition of a reportable breach varies by jurisdiction and framework, but the core concept is consistent: an incident involving unauthorized access to, or unauthorized disclosure of, protected data.

**GDPR (Article 4(12))** defines a personal data breach as "a breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data transmitted, stored or otherwise processed." This is deliberately broad. It covers not just hacking, but also accidental email disclosures, lost laptops, misconfigured cloud storage, and employee snooping.

**HIPAA** defines a breach as "the acquisition, access, use, or disclosure of protected health information in a manner not permitted under subpart E [the Privacy Rule] which compromises the security or privacy of the protected health information." HIPAA applies a presumption: any impermissible use or disclosure of PHI is presumed to be a breach unless the covered entity or business associate can demonstrate a low probability that the PHI was compromised, based on a four-factor risk assessment.

**State breach notification laws** typically define a breach as the unauthorized acquisition of (or in some states, unauthorized access to) computerized data that includes personal information. The definition of "personal information" varies by state, but generally includes name combined with Social Security number, driver's license number, financial account number, or -- increasingly -- medical information, biometric data, and login credentials.

**PCI DSS** does not use the word "breach" in its requirements. It uses "compromise" -- any unauthorized access to cardholder data or the cardholder data environment.

### The notification obligation versus the breach itself

This distinction matters: the breach is the underlying security incident. The notification obligation is a separate, independent legal requirement triggered by the breach. An organization can handle the technical response to a breach perfectly -- containing the threat, remediating the vulnerability, restoring systems -- and still violate the law by failing to notify within the required timeframe. Conversely, an organization that notifies promptly but fails to remediate the underlying vulnerability has satisfied one obligation while failing another.

Both matter. This guide focuses on the notification obligation.

---

## Data Breach Notification Timelines by Framework

The single most common source of compliance failure in breach response is the notification timeline. Different frameworks impose different deadlines, measured from different starting points, with different recipients. The following table is a reference you should have printed and taped to the wall of your incident response war room.

| Framework / Law | Notification Deadline | Clock Starts When | Who Must Be Notified | Threshold for Notification |
|---|---|---|---|---|
| **GDPR (Article 33)** | 72 hours | The controller becomes "aware" of the breach | Supervisory authority (DPA) | All personal data breaches, unless unlikely to result in a risk to individuals |
| **GDPR (Article 34)** | Without undue delay | The controller becomes "aware" of the breach | Affected data subjects | Only when breach is likely to result in "high risk" to individuals |
| **HIPAA Breach Notification Rule** | 60 calendar days | Discovery of the breach (or when it should have been discovered through reasonable diligence) | Affected individuals, HHS (OCR), media (if 500+ in a state/jurisdiction) | Breach of unsecured PHI (presumed unless low-probability risk assessment) |
| **PCI DSS / Card Brand Rules** | Immediately (within 24 hours in practice) | Discovery of suspected or confirmed compromise | Acquiring bank, payment brands (Visa, Mastercard, etc.) | Any suspected or confirmed compromise of cardholder data |
| **SEC Cybersecurity Rules (8-K)** | 4 business days | Determination that the incident is "material" | SEC (via Form 8-K Item 1.05) | Material cybersecurity incident (public companies only) |
| **CCPA/CPRA (California)** | In the most expedient time possible, without unreasonable delay | Discovery of the breach | Affected California residents, California AG (if 500+ residents) | Breach of personal information as defined by Cal. Civ. Code 1798.82 |
| **State Laws (general range)** | 30 to 90 days (varies by state) | Discovery of the breach | Affected residents, state AG (in most states) | Breach of personal information as defined by state statute |

**Critical note on overlapping obligations:** A single breach can trigger multiple notification requirements simultaneously. A healthcare SaaS company processing payments for a California hospital that is publicly traded could face notification obligations under HIPAA (60 days, to HHS and individuals), PCI DSS (immediate, to acquiring bank and card brands), CCPA (expedient, to California residents and AG), SEC rules (4 business days, via 8-K), and GDPR (72 hours, to the DPA) if any EU data subjects are affected. Your [incident response plan](/blog/incident-response-plan-compliance-guide) must include a decision tree for identifying all applicable notification requirements.

---

## GDPR Breach Notification Requirements

GDPR imposes two separate notification obligations with different triggers and different recipients. Understanding the distinction between Article 33 and Article 34 is essential.

### Article 33: Notification to the Supervisory Authority

**Who must notify:** The data controller. If you are a data processor and you discover a breach, your obligation under Article 33(2) is to notify the controller "without undue delay" after becoming aware of the breach. The controller then has 72 hours from the moment it becomes aware to notify the supervisory authority.

**Timeline:** Not later than 72 hours after becoming aware of the breach. If notification is made after 72 hours, it must be accompanied by reasons for the delay. The 72-hour clock is strict and has been enforced. The European Data Protection Board (EDPB) has clarified that "awareness" occurs at the point when the controller has a "reasonable degree of certainty" that a breach has occurred -- not when the investigation is complete.

**Content required by Article 33(3):**

- The nature of the personal data breach, including (where possible) the categories and approximate number of data subjects and records affected
- The name and contact details of the Data Protection Officer or other contact point
- The likely consequences of the breach
- The measures taken or proposed to address the breach, including measures to mitigate its possible adverse effects

**When notification is not required:** If the breach is "unlikely to result in a risk to the rights and freedoms of natural persons." The controller must document this determination. In practice, most breaches involving personal data should be notified -- the bar for the exception is high.

**Practical consideration:** You do not need to have complete information at the 72-hour mark. Article 33(4) allows information to be provided in phases. It is better to notify with partial information within 72 hours than to wait for a complete picture and miss the deadline.

### Article 34: Notification to Data Subjects

**Trigger:** The breach is "likely to result in a high risk to the rights and freedoms of natural persons." This is a higher bar than Article 33. Not every breach that must be reported to the supervisory authority must also be reported to affected individuals.

**Content:** Must describe, in clear and plain language, the nature of the breach and provide at minimum the DPO contact details, the likely consequences, and the measures taken to address the breach.

**Exceptions (Article 34(3)):** Notification to individuals is not required if: (a) the controller has applied appropriate technical and organizational protection measures (such as encryption) to the affected data; (b) the controller has taken subsequent measures that ensure the high risk is no longer likely to materialize; or (c) it would involve disproportionate effort, in which case a public communication or similar measure must be used instead.

For a comprehensive overview of GDPR obligations for US-based SaaS companies, see our [GDPR Compliance Guide](/blog/gdpr-compliance-us-saas-guide).

---

## HIPAA Breach Notification Rule

The HIPAA Breach Notification Rule (45 CFR Sections 164.400-414) applies to covered entities and business associates that experience a breach of unsecured Protected Health Information. The rule is prescriptive about who must be notified, when, and through what channels.

### The breach presumption

HIPAA applies a presumption: any impermissible acquisition, access, use, or disclosure of PHI is presumed to be a breach. The covered entity or business associate can rebut this presumption only by demonstrating that there is a low probability the PHI was compromised. This determination requires a documented risk assessment considering four factors:

1. The nature and extent of the PHI involved, including the types of identifiers and the likelihood of re-identification
2. The unauthorized person who used the PHI or to whom the disclosure was made
3. Whether the PHI was actually acquired or viewed
4. The extent to which the risk to the PHI has been mitigated

If this four-factor assessment does not demonstrate a low probability of compromise, the incident is a reportable breach.

### Individual notice (Section 164.404)

**Timeline:** Without unreasonable delay, and no later than 60 calendar days from the date of discovery. Discovery occurs on the date the breach is first known -- or the date it would have been known through the exercise of reasonable diligence.

**Method:** Written notification by first-class mail (or email if the individual has agreed to electronic notice). If contact information is insufficient or out of date for 10 or more individuals, substitute notice must be provided through a conspicuous posting on the entity's website for 90 days or through major print or broadcast media.

**Content required:**
- A brief description of what happened, including the date of the breach and the date of discovery
- A description of the types of unsecured PHI involved (but not the data itself)
- Steps the individual should take to protect themselves
- A brief description of what the entity is doing to investigate, mitigate harm, and prevent future breaches
- Contact procedures for questions, including a toll-free phone number

### HHS notification (Section 164.408)

- **Breaches affecting 500 or more individuals:** Notification to the HHS Secretary (via the HHS breach portal) without unreasonable delay, and no later than 60 days from discovery. HHS publishes these breaches on its public "Wall of Shame" -- the Breach Portal.
- **Breaches affecting fewer than 500 individuals:** Notification to HHS must be submitted no later than 60 days after the end of the calendar year in which the breach was discovered. These are logged annually.

### Media notification (Section 164.406)

If a breach affects 500 or more residents of a single state or jurisdiction, the covered entity must provide notice to prominent media outlets serving that state or jurisdiction. This notice must be provided without unreasonable delay and no later than 60 days from discovery.

### Business associate obligations

If you are a business associate and you discover a breach of unsecured PHI, you must notify the covered entity without unreasonable delay and no later than 60 days from discovery. The covered entity is then responsible for the individual, HHS, and media notifications. However, the 60-day clock for those notifications starts running from the date the business associate discovered (or should have discovered) the breach -- not from the date the covered entity received notice. This means delays in your notification to the covered entity compress the covered entity's available response time.

For a complete overview of HIPAA obligations for SaaS companies, see our [HIPAA Compliance Guide](/blog/hipaa-compliance-healthcare-saas-guide).

---

## U.S. State Breach Notification Laws

All 50 U.S. states, the District of Columbia, Guam, Puerto Rico, and the U.S. Virgin Islands have enacted breach notification laws. There is no federal breach notification law -- Congress has introduced dozens of bills over the past two decades, but none have been enacted. The result is a patchwork of 54 distinct state and territorial laws, each with its own definitions, timelines, notification requirements, and enforcement mechanisms.

### Key dimensions where state laws differ

**Definition of personal information.** Every state covers name plus Social Security number, driver's license number, and financial account number. But an increasing number of states have expanded their definitions to include:

- Medical information and health insurance information (California, Texas, others)
- Biometric data (Illinois, Texas, Washington, others)
- Login credentials (username plus password or security question/answer) (California, Florida, others)
- Taxpayer identification numbers
- Passport numbers
- Genetic data

**Notification timeline.** Timelines range from 30 days (Colorado, Florida) to 90 days (Connecticut, after a 2023 amendment) to no specific numerical deadline ("most expedient time possible" -- California, New York). Some states allow the timeline to be extended if law enforcement determines that notification would impede a criminal investigation.

**AG notification.** Most states require notification to the state Attorney General, but the thresholds vary. Some states require AG notification for every breach. Others set a threshold (e.g., California and Maine require AG notification when 500 or more residents are affected). A few states require notification to other agencies (e.g., New York requires notification to the AG, the Department of State, and the Division of State Police).

**Safe harbors.** Some states provide a safe harbor for encrypted data. If the breached data was encrypted and the encryption key was not compromised in the same incident, notification may not be required. The specifics of these safe harbors vary.

### Strictest states for breach notification

**California (Cal. Civ. Code 1798.29, 1798.82):** Broadest definition of personal information, including biometric data and health insurance information. No numerical notification deadline ("most expedient time possible, without unreasonable delay"). Requires specific notification content and format. AG notification for breaches affecting 500+ residents. Private right of action under the CCPA for breaches resulting from failure to implement reasonable security measures (statutory damages of $100-$750 per consumer per incident).

**New York (SHIELD Act, N.Y. Gen. Bus. Law 899-aa):** Expanded definition of personal information to include biometric data and username/email plus password. Notification to AG, Department of State, and Division of State Police. Requires "reasonable" data security safeguards. No specific numerical deadline ("in the most expedient time possible and without unreasonable delay").

**Texas (Tex. Bus. & Com. Code 521.053):** 60-day notification deadline. Notification to AG if 250 or more Texas residents are affected. Broad definition that includes biometric identifiers.

**Illinois:** While Illinois does not have the shortest breach notification timeline, the state's Biometric Information Privacy Act (BIPA) creates significant exposure for breaches involving biometric data, including a private right of action with statutory damages of $1,000 per negligent violation and $5,000 per intentional or reckless violation.

**Colorado (CPC 6-1-716):** 30-day notification deadline -- among the shortest in the country. AG notification for breaches affecting 500+ residents.

**Florida (Fla. Stat. 501.171):** 30-day notification deadline. AG notification for breaches affecting 500+ individuals. Requires the notification to include information about the entity's breach response.

### Practical implications for multi-state operations

If your company has customers or users across multiple states -- as most SaaS companies do -- you face a coordination challenge. A single breach may trigger notification obligations in every state where an affected individual resides. Because state laws differ in their definitions, timelines, and requirements, the safest approach is to: (1) use the shortest applicable timeline as your deadline for all notifications; (2) use the broadest applicable definition of personal information; and (3) include in your notification all elements required by any applicable state. In practice, this means designing your notification process to satisfy California, Colorado, and Florida requirements, which will generally cover the requirements of every other state.

---

## SEC Cyber Incident Disclosure

On July 26, 2023, the SEC adopted final rules requiring public companies to disclose material cybersecurity incidents. These rules, codified in Regulation S-K Item 106 and Form 8-K Item 1.05, represent the most significant federal cybersecurity disclosure requirements for public companies.

### Form 8-K Item 1.05 (Incident Disclosure)

**Who:** All public companies subject to SEC reporting requirements (registrants filing on domestic forms).

**Timeline:** Within four business days after the company determines that a cybersecurity incident is material. The clock does not start at discovery of the incident -- it starts at the materiality determination. However, companies cannot unreasonably delay the materiality assessment. The SEC has stated that companies should conduct materiality determinations "without unreasonable delay" after discovery.

**Content required:**
- The material aspects of the nature, scope, and timing of the incident
- The material impact or reasonably likely material impact on the company, including financial condition and results of operations

The SEC explicitly stated that companies are not required to disclose specific technical information about their cybersecurity systems, related networks and devices, or potential system vulnerabilities if disclosure would impede the company's response or remediation.

**Delayed disclosure:** The Attorney General of the United States may authorize a delay of up to 30 days (extendable to 60 days) if disclosure would pose a substantial risk to national security or public safety. This is expected to be a narrow exception.

**Materiality standard:** The SEC applies the same materiality standard used throughout securities law: information is material if there is a "substantial likelihood that a reasonable shareholder would consider it important" in making an investment decision. There is no bright-line dollar threshold. Companies must evaluate the qualitative and quantitative significance of the incident.

### Regulation S-K Item 106 (Annual Disclosure)

In addition to incident-specific 8-K filings, public companies must disclose in their annual reports (10-K):

- Their processes for assessing, identifying, and managing material risks from cybersecurity threats
- Whether cybersecurity risks have materially affected or are reasonably likely to materially affect the company
- The board of directors' oversight of cybersecurity risk
- Management's role and expertise in assessing and managing cybersecurity risk

These annual disclosures create ongoing obligations for cybersecurity governance -- not just incident response.

---

## PCI DSS Breach Response and Notification

PCI DSS does not prescribe specific notification timelines in the way that GDPR or HIPAA do. Instead, it requires organizations to have an incident response plan (Requirement 12.10) and to activate it immediately upon a suspected or confirmed compromise. The notification obligations flow primarily from the card brand operating regulations -- not from PCI DSS itself.

### Card brand notification requirements

Each major card brand (Visa, Mastercard, American Express, Discover, JCB) has its own incident response program:

**Visa:** The Visa Incident Response Procedure requires merchants and service providers to immediately notify their acquiring bank upon discovery of a suspected or confirmed compromise. The acquiring bank then notifies Visa. Visa may require a forensic investigation by a PCI Forensic Investigator (PFI).

**Mastercard:** Mastercard's Account Data Compromise (ADC) program requires notification within 24 hours of discovery. Mastercard may mandate a PFI investigation and issue operational fines for non-compliance.

**American Express:** Requires immediate notification to American Express upon discovery of a suspected breach involving American Express card data.

### PCI Forensic Investigation (PFI)

For significant breaches, the card brands will typically require an independent forensic investigation conducted by a PCI Forensic Investigator -- a firm specifically qualified and listed by the PCI Security Standards Council. The PFI will determine the scope of the compromise, identify how the breach occurred, assess whether the organization was PCI DSS compliant at the time of the breach, and recommend remediation measures.

Key point: if the PFI determines that the organization was not PCI DSS compliant at the time of the breach, the organization may face significant fines from the card brands, in addition to liability for fraudulent transactions. These fines are contractual, not regulatory -- they flow through the acquiring bank under the merchant agreement.

### Requirement 12.10: Incident Response Plan

PCI DSS v4.0 Requirement 12.10 mandates that organizations maintain an incident response plan that is ready to activate immediately. The plan must include specific incident response procedures, business recovery and continuity procedures, data backup processes, analysis of legal requirements for reporting compromises, coverage and responses for all critical system components, and reference to or inclusion of incident response procedures from the card brands.

For a comprehensive overview of PCI DSS requirements, see our [PCI DSS Complete Guide](/blog/pillar-pci-dss-complete-guide).

---

## Building a Breach Notification Playbook: Step-by-Step

A breach notification playbook is not the same as an incident response plan. Your [incident response plan](/blog/incident-response-plan-compliance-guide) covers the full lifecycle of incident detection, containment, eradication, and recovery. The breach notification playbook is the subset of that plan focused specifically on meeting your legal notification obligations. It should be a standalone, quickly accessible document that your legal and compliance team can execute under time pressure.

### Hour 0-4: Detection and Initial Assessment

**Objective:** Confirm that a security incident has occurred and perform initial triage to determine whether it involves protected data.

- Activate the incident response team. Assign an Incident Commander.
- Confirm the nature of the incident: Is there evidence of unauthorized access to, disclosure of, or acquisition of data?
- Identify the types of data potentially affected: personal information, PHI, cardholder data, financial data, login credentials.
- Document everything. Timestamps, actions taken, people involved, evidence collected. This documentation is critical for meeting the "reasonable diligence" standard under HIPAA and for demonstrating compliance with GDPR's 72-hour timeline.

### Hour 4-24: Scope Assessment and Containment

**Objective:** Determine the scope of the breach and contain the threat.

- Identify affected systems, databases, and data stores.
- Determine the number and categories of individuals affected.
- Determine which jurisdictions are implicated (where do affected individuals reside?).
- Contain the breach: isolate affected systems, revoke compromised credentials, block unauthorized access vectors.
- Begin the four-factor HIPAA risk assessment (if PHI is involved).
- Engage external legal counsel. Breach notification triggers attorney-client privilege considerations. Communications through legal counsel may be protected.
- Engage a forensic investigation firm if needed (PFI if cardholder data is involved).

### Hour 24-48: Regulatory Mapping and Notification Preparation

**Objective:** Determine all applicable notification obligations and begin drafting notifications.

- Complete the regulatory mapping: Which frameworks apply? GDPR? HIPAA? PCI DSS? SEC? Which state laws?
- Determine whether each applicable framework requires notification based on the facts of the breach.
- For GDPR: assess whether the breach is "unlikely to result in a risk" (Article 33 exception) or "likely to result in high risk" (Article 34 trigger).
- For HIPAA: complete the four-factor risk assessment. Does the assessment demonstrate a low probability of compromise?
- For SEC: begin the materiality assessment. Is the incident material or reasonably likely to become material?
- Draft notification letters for each required audience: supervisory authority, affected individuals, state AGs, HHS, card brands, SEC.
- Have legal counsel review all draft notifications.

### Hour 48-72: Notification Execution

**Objective:** Execute notifications within the earliest applicable deadline.

- File the GDPR supervisory authority notification (72-hour deadline). Remember: partial information is acceptable. You can supplement later.
- Notify the acquiring bank and card brands (if cardholder data is involved -- this should have happened as early as possible, ideally within 24 hours).
- Determine whether the SEC 8-K clock has started (materiality determination).
- Begin state AG notifications for states with 30-day deadlines (Colorado, Florida).
- Prepare and queue individual notifications (HIPAA 60-day deadline, state law deadlines).
- Update your public status page if customers are affected.

### Day 3-60: Ongoing Notification and Remediation

**Objective:** Complete all remaining notifications and remediate the underlying vulnerability.

- Send individual notification letters to affected persons (via first-class mail for HIPAA; method varies by state).
- For HIPAA breaches affecting 500+ in a state: issue media notification.
- Submit HHS breach portal notification (for breaches affecting 500+).
- File SEC Form 8-K if materiality has been determined (within 4 business days of determination).
- Complete state AG notifications (within each state's deadline).
- Document all notification activities, including dates, methods, and recipients.
- Conduct root cause analysis and implement remediation measures.
- Preserve all forensic evidence and documentation for potential regulatory inquiries or litigation.

---

## What Must Be Included in a Breach Notification

The required content of a breach notification varies by framework. Using a notification that omits required elements is a compliance failure even if the notification is timely. The following table summarizes required elements across the major frameworks.

| Element | GDPR (Art. 33) | GDPR (Art. 34) | HIPAA | State Laws (typical) | SEC (8-K) |
|---|---|---|---|---|---|
| Description of the breach | Required | Required (plain language) | Required | Required | Required (material aspects) |
| Types of data affected | Required | Not explicitly required | Required | Required (most states) | Not explicitly required |
| Number of individuals affected | Required (approximate) | Not explicitly required | Required | Varies | Not explicitly required |
| Likely consequences | Required | Required | Not explicitly required | Varies | Required (material impact) |
| Measures taken to address the breach | Required | Required | Required | Required (most states) | Not explicitly required |
| DPO / contact point details | Required | Required | Required (toll-free number) | Required (contact info) | N/A |
| Steps individuals should take | Not explicitly required | Implicit | Required | Required (most states) | N/A |
| Date of breach and discovery | Not explicitly required | Not explicitly required | Required | Required (most states) | Required (timing) |
| Identity theft protection offer | N/A | N/A | Common practice, not required | Required in some states | N/A |

---

## Breach Notification Templates: Sample Language

The following templates provide starting points for breach notification communications. They must be customized for the specific facts of each incident and reviewed by legal counsel before use. These are structural frameworks, not fill-and-send documents.

### Template 1: Notification to GDPR Supervisory Authority (Article 33)

```
PERSONAL DATA BREACH NOTIFICATION
[Supervisory Authority Name]
Date of notification: [Date]

1. CONTROLLER INFORMATION
Organization name: [Name]
DPO / Contact: [Name, email, phone]

2. NATURE OF THE BREACH
Description: [Brief description of what occurred]
Date/time of breach: [Date/time, or "under investigation"]
Date/time controller became aware: [Date/time]
Categories of data subjects affected: [e.g., customers, employees, users]
Approximate number of data subjects: [Number, or "under investigation"]
Categories of personal data records: [e.g., names, email addresses,
financial data]
Approximate number of records: [Number, or "under investigation"]

3. LIKELY CONSEQUENCES
[Description of the likely consequences for affected data subjects]

4. MEASURES TAKEN
[Description of measures taken or proposed to address the breach,
including measures to mitigate its adverse effects]

5. SUPPLEMENTARY INFORMATION
[Note if information will be provided in phases, per Article 33(4)]
```

### Template 2: Notification to Affected Individuals (HIPAA-Compliant)

```
[Organization Letterhead]
[Date]

Dear [Individual Name],

We are writing to inform you of an incident that may have involved
your protected health information.

WHAT HAPPENED
On [date of discovery], [Organization Name] discovered that
[brief description of the incident]. The incident occurred on or
about [date of breach]. We immediately began an investigation and
engaged [forensic firm / law enforcement, as applicable].

WHAT INFORMATION WAS INVOLVED
The types of information that may have been involved include:
[List specific types -- e.g., name, date of birth, medical record
number, diagnosis information, treatment information, health
insurance information]. [Explicitly state: "Your Social Security
number was / was not involved."]

WHAT WE ARE DOING
[Description of remediation steps, security improvements, and
any steps taken to prevent recurrence.]

WHAT YOU CAN DO
We recommend that you [specific protective steps -- e.g., review
explanation of benefits statements, monitor credit reports, place
fraud alerts]. [If offering credit monitoring: "We are providing
[X] months of complimentary credit monitoring and identity theft
protection through [Provider Name]. To enroll, [instructions]."]

FOR MORE INFORMATION
If you have questions, please call our dedicated response line at
[toll-free number], available [hours of operation]. You may also
write to us at [mailing address].

Sincerely,
[Name and Title]
[Organization Name]
```

### Template 3: Notification to State Attorney General

```
[Date]

[State Attorney General Name]
[Office Address]

RE: Data Breach Notification Pursuant to [State Statute Citation]

Dear [Attorney General / Office]:

[Organization Name] is providing this notification pursuant to
[specific state statute] regarding a data security incident
affecting [number] residents of [State].

DESCRIPTION OF INCIDENT
[Brief factual description]

DATE OF BREACH AND DISCOVERY
Breach occurred: [Date or approximate date range]
Breach discovered: [Date]

INFORMATION INVOLVED
[Types of personal information affected]

NUMBER OF [STATE] RESIDENTS AFFECTED
[Number]

STEPS TAKEN
[Description of response, remediation, and prevention measures]

NOTICE TO INDIVIDUALS
Individual notification letters are being sent on [date] via
[method]. A copy of the notification letter is enclosed.

CONTACT INFORMATION
[Name, title, phone, email]

Sincerely,
[Name and Title]
```

---

## The Cost of Late or Failed Notification

The consequences of failing to meet breach notification requirements extend across four categories: regulatory fines, civil litigation, contractual penalties, and reputational damage.

### Regulatory fines

**GDPR:** Failure to notify the supervisory authority within 72 hours is a violation of Article 33, punishable by fines up to 10 million euros or 2% of global annual turnover. Failure to notify affected individuals under Article 34 carries the same penalty. In practice, regulators have imposed significant fines for notification failures even when the underlying breach was relatively contained:

- **Meta (2024):** 91 million euros from the Irish DPC for the plaintext password storage incident, where inadequate breach documentation and notification practices were cited as aggravating factors.
- **British Airways (2020):** Originally fined 183 million pounds (reduced to 20 million pounds) by the UK ICO. The timeline and adequacy of breach notification were factors in the enforcement assessment.

**HIPAA:** The HHS Office for Civil Rights has imposed significant penalties for breach notification failures:

- **Presence Health (2017):** $475,000 settlement for failing to notify affected individuals within 60 days. The breach affected only 836 individuals, but the notification was 101 days late.
- **CHSPSC (2020):** $2.3 million settlement for a breach affecting 6.1 million individuals. Inadequate breach response procedures and delayed notification were contributing factors.

**State laws:** State AG enforcement actions for breach notification failures are increasing. The New York AG has pursued settlements with companies for late notification, inadequate notification content, and failure to implement reasonable security measures that would have prevented the breach.

### Civil litigation

Data breach class action lawsuits are now routine following large breaches. Late or inadequate notification strengthens plaintiffs' claims by providing evidence of negligence and by increasing the window during which affected individuals were exposed without knowledge. The T-Mobile breaches resulted in a $350 million class action settlement in 2023. Equifax paid $700 million. These settlements are driven in part by the adequacy (or inadequacy) of the company's breach response and notification practices.

### Contractual penalties

Enterprise contracts increasingly include breach notification SLAs -- typically requiring notification to the customer within 24-72 hours of discovering a breach affecting the customer's data. Failure to meet these contractual timelines can trigger indemnification obligations, service credits, and contract termination rights, independent of any regulatory penalty.

### Reputational damage

A 2024 Ponemon Institute study found that 65% of consumers reported losing trust in a company after a data breach. That number increased to 80% when the company was perceived as having been slow or evasive in its breach notification. The notification is not just a legal obligation -- it is a moment that defines the organization's relationship with its customers and the public.

---

## Breach Notification for SaaS Companies: Processor vs Controller Obligations

SaaS companies face a specific challenge in breach notification: their obligations depend on whether they are acting as a data processor or a data controller with respect to the affected data. This distinction, well established in GDPR and increasingly relevant under other frameworks, determines who must notify regulators and individuals, and on what timeline.

### When you are the data processor

Most B2B SaaS companies are data processors under GDPR -- they process personal data on behalf of their customers (the controllers). As a processor, your obligations are:

**GDPR:** Notify the controller "without undue delay" after becoming aware of a breach (Article 33(2)). You do not notify the supervisory authority or data subjects directly -- the controller does. However, you must provide the controller with sufficient information to enable them to meet their 72-hour notification obligation. Your [data processing agreement](/blog/data-processing-agreement-guide) should define the specific notification timeline and information requirements.

**HIPAA:** If you are a business associate, notify the covered entity within 60 days of discovery (or sooner if your BAA specifies a shorter timeline). The covered entity handles individual, HHS, and media notifications.

**Practical impact:** Even though the controller bears the notification obligation, your delay becomes their delay. If you take 48 hours to notify the controller, you have consumed two-thirds of their 72-hour GDPR window. Best practice is to notify your customer within 24 hours of confirming a breach, regardless of what your DPA requires.

### When you are the data controller

You are a controller for data you collect directly from individuals for your own purposes -- website visitor data, employee data, marketing contact data, free trial user data. For breaches affecting this data, you bear the full notification obligation: supervisory authority, data subjects, state AGs, and any other applicable requirements.

### The processor-controller notification chain

A breach at a SaaS company often creates a cascade:

1. The SaaS company (processor) discovers the breach.
2. The SaaS company notifies its customers (controllers) under the DPA.
3. Each customer (controller) evaluates the breach against its own notification obligations.
4. Each customer notifies its relevant supervisory authority (GDPR), affected individuals (GDPR/HIPAA/state laws), and any other required parties.

This cascade means a single breach at a SaaS company can generate dozens or hundreds of downstream notification obligations for its customers. Your breach notification playbook must include a customer communication plan: how you will notify all affected customers, what information you will provide, and how you will support their notification obligations.

For a detailed explanation of controller and processor roles and obligations, see our [Data Processing Agreement Guide](/blog/data-processing-agreement-guide).

---

## FAQ

### How quickly do I need to report a data breach?

It depends on the applicable framework. GDPR requires notification to the supervisory authority within 72 hours. HIPAA allows up to 60 calendar days for individual notification. PCI DSS and card brand rules require immediate notification (practically within 24 hours). SEC rules require an 8-K filing within four business days of a materiality determination. U.S. state laws range from 30 to 90 days. If multiple frameworks apply, you must meet the shortest applicable deadline -- which means your operational target should be 72 hours or less.

### What is the penalty for not reporting a data breach?

Penalties vary by framework. GDPR fines can reach 10 million euros or 2% of global annual turnover. HIPAA penalties range from $100 to $50,000 per violation (per affected record), with annual maximums up to $1.5 million per violation category. State laws impose penalties ranging from $500 to $750,000 per violation, depending on the state. SEC violations can result in enforcement actions, fines, and shareholder lawsuits. Beyond direct penalties, late notification increases litigation exposure and reputational damage.

### Does encryption protect me from breach notification requirements?

Partially. Under HIPAA, a breach of PHI that was encrypted using NIST-approved algorithms does not require notification -- HIPAA considers encrypted data to be "secured" PHI, and the Breach Notification Rule applies only to "unsecured" PHI. Several state laws provide similar encryption safe harbors. GDPR does not provide an automatic encryption exemption from Article 33 (DPA notification), but encryption may exempt you from Article 34 (individual notification) if the data was rendered "unintelligible" to unauthorized persons. The key must not have been compromised in the same incident.

### What is the difference between a data breach and a security incident?

A security incident is any event that potentially threatens the confidentiality, integrity, or availability of information or systems. A data breach is a specific type of security incident in which protected data is confirmed to have been accessed, disclosed, or acquired by an unauthorized party. Not every security incident is a data breach. A failed login attempt is a security incident but not a breach. A successful SQL injection that exfiltrates customer records is both. Notification requirements are triggered by breaches, not by security incidents generally (though your incident response plan should address both).

### Do I need to notify law enforcement about a data breach?

There is no general federal requirement to notify law enforcement, though it is often advisable. Some state laws specifically require or encourage law enforcement notification. GDPR does not require law enforcement notification, but data protection authorities may coordinate with law enforcement. In practice, involving law enforcement early can provide benefits: some state laws allow you to delay public notification if law enforcement determines it would impede an investigation. For breaches involving criminal activity (hacking, ransomware, insider theft), reporting to the FBI's Internet Crime Complaint Center (IC3) is recommended.

### What counts as "discovery" of a breach for purposes of the notification timeline?

Under HIPAA, a breach is "discovered" on the first day it is known to the entity -- or the date it would have been known if the entity had exercised reasonable diligence. Under GDPR, the controller is "aware" when it has a "reasonable degree of certainty" that a breach has occurred. Under most state laws, discovery occurs when the entity becomes aware of the breach or has reason to believe a breach occurred. The critical point: you cannot stop the clock by failing to investigate. If evidence of a breach was available and you failed to review it, regulators will treat the breach as discovered on the date you should have known.

### What should I do if I discover a breach at a vendor or sub-processor?

If you discover that a vendor processing data on your behalf has experienced a breach, your obligations depend on your role. If you are the data controller, you bear the notification obligations to regulators and individuals. Your vendor (processor) should have notified you under your data processing agreement, but the regulatory obligation rests with you. Immediately assess the scope of the breach, determine which of your data was affected, and execute your breach notification playbook. If you are a processor and the breach occurred at your sub-processor, you must notify your controller customers per your DPA and support their notification efforts.

### Can I delay breach notification to complete my investigation?

Under GDPR, no. The 72-hour notification to the supervisory authority cannot be delayed to complete the investigation. Article 33(4) specifically allows notification in phases -- provide what you know now and supplement later. Under HIPAA, the 60-day window is measured from discovery, not from completion of the investigation. Under SEC rules, the 4-business-day clock starts from the materiality determination, but you cannot unreasonably delay the materiality assessment. Under state laws, some jurisdictions allow a delay if law enforcement requests it. In general, the trend across all frameworks is to prohibit investigative delays from extending notification timelines.

### Do I need a breach notification plan even if I have never had a breach?

Yes. Every major compliance framework requires documented incident response and breach notification procedures as a standing requirement -- not just as a response to an actual incident. SOC 2 (CC7.3, CC7.4), ISO 27001 (A.5.24-A.5.28), HIPAA (164.308(a)(6)), and PCI DSS (Requirement 12.10) all require documented, tested incident response plans. During an audit, the absence of a breach notification playbook is a finding -- regardless of whether a breach has occurred. Building and testing the plan before you need it is what separates organizations that survive a breach from those that do not.

---

## Take Control of Breach Notification Compliance with QuickTrust

A breach notification failure is not caused by the breach itself. It is caused by the absence of a plan that was tested before the breach occurred. When a breach happens -- and for most organizations, it is a matter of when, not if -- the difference between a controlled, compliant response and a chaotic, penalty-triggering scramble comes down to preparation.

QuickTrust helps technology companies build the compliance infrastructure that breach notification readiness requires: documented incident response plans that map to every applicable framework, automated evidence collection that tracks your response in real time, regulatory notification tracking that ensures no deadline is missed, and continuous compliance monitoring that reduces the likelihood of a breach in the first place.

Your next audit will ask whether you have a breach notification playbook. Your next breach will test whether it works.

**[Start your free QuickTrust assessment](https://quicktrustapp.com)** and see where your breach notification readiness stands against GDPR, HIPAA, PCI DSS, SEC, and state law requirements -- before you need to find out the hard way.

---

*Related reading:*

- *[How to Build an Incident Response Plan That Passes Every Compliance Audit](/blog/incident-response-plan-compliance-guide)*
- *[GDPR Compliance for US SaaS Companies: The Non-Lawyer's Implementation Guide](/blog/gdpr-compliance-us-saas-guide)*
- *[HIPAA Compliance in 2026: What Every Healthcare SaaS Founder Must Know](/blog/hipaa-compliance-healthcare-saas-guide)*
- *[Data Processing Agreement (DPA): What Every SaaS Company Must Include](/blog/data-processing-agreement-guide)*
- *[PCI DSS Compliance: The Complete Guide](/blog/pillar-pci-dss-complete-guide)*
- *[Regulatory Compliance for Tech Companies: A Framework Decision Matrix](/blog/regulatory-compliance-tech-companies-guide)*
