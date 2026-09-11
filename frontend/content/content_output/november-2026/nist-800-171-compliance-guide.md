---
meta_description: "Complete NIST 800-171 compliance guide for defense contractors. Learn all 14 control families, 110 security requirements, how 800-171 maps to CMMC 2.0, and step-by-step implementation."
target_keyword: "nist 800-171"
secondary_keywords: "NIST SP 800-171, NIST 800-171 requirements, NIST 800-171 compliance, CUI protection, NIST 800-171 vs CMMC, DFARS compliance"
word_count_target: 4500+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-21
---

# NIST 800-171: The Complete Guide to Protecting CUI and Achieving DFARS Compliance

In 2017, the Department of Defense told every company in its supply chain to implement 110 cybersecurity requirements from a document called NIST Special Publication 800-171. The deadline was December 31 of that year. Almost nobody complied.

A 2019 audit by the DoD Inspector General revealed that the overwhelming majority of defense contractors had failed to implement even basic controls -- despite contractually certifying that they had. The consequences of that failure are now measured in the hundreds of billions of dollars: stolen weapons designs, exfiltrated technical data, compromised intelligence, and a strategic advantage handed to adversaries who never had to invest in their own research and development because they could simply steal ours.

NIST 800-171 is no longer optional, no longer aspirational, and no longer something contractors can self-attest without scrutiny. With the rollout of CMMC 2.0 -- which uses NIST 800-171 as the technical baseline for Level 2 certification -- the era of unchecked self-assessment is over. Third-party assessors now verify what contractors claim. The False Claims Act applies to inaccurate SPRS score submissions. And contracts are being awarded to companies that can demonstrate compliance, not just assert it.

This guide covers everything you need to understand about NIST 800-171: what the standard requires, who must comply, how the 14 control families and 110 security requirements work, what changed in Revision 3, how 800-171 relates to CMMC 2.0 and NIST 800-53, how to score your self-assessment, a step-by-step implementation roadmap, realistic cost and timeline estimates, and the most common compliance gaps that trip up defense contractors.

---

## What Is NIST SP 800-171?

NIST Special Publication 800-171, formally titled *Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations*, is a cybersecurity standard published by the National Institute of Standards and Technology (NIST). It specifies 110 security requirements that nonfederal organizations must implement when they store, process, or transmit Controlled Unclassified Information (CUI) on behalf of the United States government.

The "nonfederal" distinction is critical. Federal agencies protect their own systems using the much larger [NIST SP 800-53](/blog/nist-800-53-controls) control catalog, which contains over 1,000 controls and control enhancements. NIST 800-171 is a derived subset -- it takes the Moderate baseline controls from 800-53 that are not typically provided by the federal government itself and translates them into requirements appropriate for private-sector organizations. The result is a focused set of 110 requirements across 14 control families that represent the minimum security posture the government expects from any contractor handling CUI.

### The DFARS Connection

NIST 800-171 compliance became a contractual requirement for defense contractors through **DFARS clause 252.204-7012**, "Safeguarding Covered Defense Information and Cyber Incident Reporting." This clause, which has been included in nearly all DoD contracts since late 2017, requires contractors to:

1. **Implement NIST SP 800-171** to provide "adequate security" on any covered contractor information systems
2. **Report cyber incidents** to the DoD within 72 hours of discovery
3. **Submit malicious software** discovered during incident analysis to the DoD Cyber Crime Center
4. **Preserve and protect images** of known affected information systems and all relevant monitoring/packet capture data for at least 90 days following a cyber incident
5. **Flow down the requirement** to subcontractors at all tiers that will handle covered defense information

The practical implication: if you are a defense contractor or subcontractor and your contract includes DFARS 252.204-7012, you are contractually obligated to implement all 110 NIST 800-171 requirements. This is not guidance. It is a binding obligation, and failure to comply creates exposure under the False Claims Act.

### A Brief History of NIST 800-171

- **June 2015:** NIST publishes the original SP 800-171, establishing the baseline requirements for protecting CUI in nonfederal systems.
- **December 2016:** NIST releases Revision 1, incorporating feedback from federal agencies and industry and refining control descriptions.
- **February 2020:** NIST publishes Revision 2, which aligned the publication with updated CUI guidance and made minor adjustments to requirements. Revision 2 contains the 110 requirements across 14 families that most contractors are currently assessed against.
- **May 2023:** NIST releases the initial public draft of Revision 3, signaling a major restructuring.
- **May 2024:** NIST publishes the final version of Revision 3, which significantly restructures the requirements and aligns them more closely with NIST SP 800-53 Revision 5.

---

## Who Must Comply with NIST 800-171?

The short answer: any organization that handles Controlled Unclassified Information on behalf of the federal government and operates nonfederal information systems. In practice, this covers a large and growing population of companies.

### Defense Contractors and Subcontractors

The primary audience for NIST 800-171 is the defense industrial base. If your company holds a DoD contract that includes DFARS clause 252.204-7012, you must implement all applicable NIST 800-171 requirements. This includes:

- **Prime contractors** who contract directly with the DoD
- **Subcontractors at all tiers** who receive CUI from prime contractors or other subcontractors
- **Small businesses** -- there is no size exemption. A five-person machine shop that receives a technical drawing marked as CUI has the same compliance obligations as a prime contractor with 50,000 employees

The flow-down requirement in DFARS 252.204-7012 is explicit: primes must include equivalent requirements in their subcontracts. This means compliance pressure flows down the entire supply chain.

### Federal Civilian Agencies and Their Contractors

While DFARS is specific to the Department of Defense, the underlying CUI protection requirement is not. Executive Order 13556 and the subsequent 32 CFR Part 2002 (the CUI rule) established a government-wide framework for protecting CUI. Federal civilian agencies -- including the Department of Homeland Security, the Department of Energy, NASA, and others -- increasingly reference NIST 800-171 in their contracts and grant agreements.

### Universities and Research Institutions

Universities and research organizations that receive federal grants involving CUI must also comply with NIST 800-171. This is particularly relevant for institutions performing defense-related or classified-adjacent research under programs like the Department of Defense's fundamental research programs.

### Companies Seeking CMMC Certification

Because [CMMC Level 2](/blog/cmmc-compliance) requires implementation of all 110 NIST 800-171 Revision 2 requirements, any company pursuing CMMC Level 2 certification is by definition implementing NIST 800-171. The two standards are not alternatives -- CMMC Level 2 *is* NIST 800-171, plus a verification mechanism.

---

## What Is Controlled Unclassified Information (CUI)?

Controlled Unclassified Information is government-created or government-possessed information that requires safeguarding or dissemination controls consistent with applicable laws, regulations, and government-wide policies, but that is not classified under Executive Order 13526 or the Atomic Energy Act.

CUI replaced a patchwork of agency-specific designations -- For Official Use Only (FOUO), Sensitive But Unclassified (SBU), Law Enforcement Sensitive (LES), and dozens of others -- with a single, standardized system. The National Archives and Records Administration (NARA) maintains the CUI Registry, which catalogs all approved CUI categories and subcategories.

### Common CUI Categories in the Defense Supply Chain

Defense contractors most frequently encounter CUI in these categories:

- **Controlled Technical Information (CTI):** Technical data or computer software with military or space application that is subject to controls on access, use, reproduction, modification, performance, display, release, disclosure, or dissemination. This is the most common CUI category in defense contracting.
- **Export Controlled:** Information subject to export control regulations under ITAR (International Traffic in Arms Regulations) or EAR (Export Administration Regulations).
- **Naval Nuclear Propulsion Information (NNPI):** Information concerning the design, arrangement, development, manufacture, testing, operation, administration, training, maintenance, and repair of naval nuclear propulsion plants.
- **Operations Security (OPSEC):** Information that could be compiled by adversaries to derive critical information about military operations.
- **Proprietary Business Information:** Contractor-submitted financial, trade secret, or proprietary data that requires protection under government agreements.

### How CUI Is Marked

CUI markings follow a standardized format defined in 32 CFR Part 2002 and the CUI Marking Handbook. Documents containing CUI must include:

- The designation indicator **"CUI"** or **"CONTROLLED"** in the banner (top of the document)
- The specific CUI category or subcategory (e.g., "CUI//SP-CTI" for Controlled Technical Information with specified dissemination controls)
- The designating agency
- A footer on each page indicating CUI status

In practice, many defense contractors receive CUI without proper markings. This creates a significant compliance challenge: you cannot protect information you do not know you have. NIST 800-171 requirement 3.8.1 (Media Protection family) and related controls address this by requiring organizations to establish procedures for identifying and marking CUI, but the responsibility often falls on the originating agency. Contractors should establish processes to identify potentially unmarked CUI and seek clarification from the government contracting officer when markings are absent or ambiguous.

---

## The 14 Control Families and 110 Requirements

NIST 800-171 Revision 2 organizes its 110 security requirements into 14 control families. Each family addresses a specific domain of cybersecurity. The number of requirements per family varies significantly -- Access Control alone accounts for 22 of the 110 requirements, while Personnel Security has only two.

Understanding what each family requires is essential for scoping your implementation effort and identifying gaps in your current security posture.

### 1. Access Control (AC) -- 22 Requirements

Access Control is the largest family and addresses who can access what, under what conditions, and through what mechanisms. Requirements cover:

- Limiting system access to authorized users and transactions
- Restricting access to the types of transactions and functions that authorized users are permitted to execute
- Controlling the flow of CUI in accordance with approved authorizations
- Separating duties of individuals to reduce risk of malicious activity
- Employing the principle of least privilege
- Limiting unsuccessful logon attempts
- Providing privacy and security notices consistent with CUI rules
- Terminating user sessions after defined conditions
- Controlling remote access, wireless access, and mobile device connections
- Controlling information posted or processed on publicly accessible systems

This family is where most organizations have the largest number of gaps. Implementing least privilege across an enterprise environment -- particularly one that mixes CUI and non-CUI systems -- requires careful architectural planning.

### 2. Awareness and Training (AT) -- 3 Requirements

Requires organizations to ensure that managers, systems administrators, and users are made aware of the security risks associated with their activities, and that personnel are adequately trained to carry out their information security responsibilities. Includes requirements for role-based training for users with security-relevant roles.

### 3. Audit and Accountability (AU) -- 9 Requirements

Requires organizations to create, protect, and retain system audit logs sufficient to enable the monitoring, analysis, investigation, and reporting of unauthorized system activity. Key requirements include:

- Creating and retaining audit logs that track system events
- Ensuring individual accountability by tracing actions to specific users
- Reviewing and updating audit events
- Alerting on audit process failures
- Correlating audit information from multiple sources
- Protecting audit information and audit tools from unauthorized access and modification

### 4. Configuration Management (CM) -- 9 Requirements

Requires organizations to establish and maintain baseline configurations and inventories of systems, and to enforce security configuration settings. Covers:

- Establishing and maintaining baseline configurations
- Establishing and enforcing security configuration settings
- Tracking, reviewing, and approving or disapproving changes
- Analyzing the security impact of changes prior to implementation
- Restricting, disabling, or preventing the use of nonessential programs, functions, ports, protocols, and services
- Applying deny-by-exception (blacklisting) or permit-by-exception (whitelisting) policies

### 5. Identification and Authentication (IA) -- 11 Requirements

Requires organizations to identify and authenticate users, processes, and devices before granting access. Key requirements include:

- Identifying and authenticating system users, processes acting on behalf of users, and devices
- Enforcing multifactor authentication for local and remote access
- Using replay-resistant authentication mechanisms
- Preventing reuse of identifiers and passwords
- Enforcing minimum password complexity and change requirements
- Storing and transmitting only cryptographically protected passwords
- Obscuring feedback of authentication information during the authentication process

### 6. Incident Response (IR) -- 3 Requirements

Requires organizations to establish an operational incident-handling capability including preparation, detection, analysis, containment, recovery, and user response activities. Includes tracking, documenting, and reporting incidents to designated officials and authorities. Note that DFARS 252.204-7012 adds a 72-hour reporting requirement to the DoD that goes beyond what NIST 800-171 specifies.

### 7. Maintenance (MA) -- 6 Requirements

Requires organizations to perform maintenance on systems in a timely manner, control the tools and personnel used for maintenance, and ensure that equipment removed for off-site maintenance is sanitized of any CUI. Covers:

- Performing maintenance on organizational systems
- Providing controls on tools, techniques, mechanisms, and personnel used for maintenance
- Requiring multifactor authentication for remote maintenance
- Supervising maintenance activities performed by personnel without required access authorization

### 8. Media Protection (MP) -- 9 Requirements

Requires organizations to protect CUI stored on digital and non-digital media, limit access to CUI on media to authorized users, and sanitize or destroy media before disposal or reuse. Key requirements:

- Protecting and controlling media containing CUI during transport
- Implementing cryptographic mechanisms to protect confidentiality of CUI stored on digital media during transport
- Controlling the use of removable media
- Marking media with required CUI markings and distribution limitations
- Sanitizing media before disposal or release for reuse using NIST SP 800-88 guidelines

### 9. Personnel Security (PS) -- 2 Requirements

Requires organizations to screen individuals prior to authorizing access to systems containing CUI and to ensure that CUI and systems containing CUI are protected during and after personnel actions such as terminations and transfers. This is the smallest family but frequently overlooked -- particularly the requirement to revoke access promptly when personnel are terminated.

### 10. Physical Protection (PE) -- 6 Requirements

Requires organizations to limit physical access to systems, equipment, and operating environments to authorized individuals, and to protect and monitor the physical facility. Covers:

- Limiting physical access to authorized individuals
- Protecting and monitoring the physical facility and support infrastructure
- Escorting visitors and monitoring visitor activity
- Maintaining audit logs of physical access
- Controlling and managing physical access devices (keys, badges, combinations)
- Enforcing safeguarding measures for CUI at alternate work sites (including telework locations)

### 11. Risk Assessment (RA) -- 3 Requirements

Requires organizations to periodically assess the risk to organizational operations, assets, and individuals resulting from the operation of systems and the processing, storage, or transmission of CUI. Includes vulnerability scanning requirements:

- Periodically assessing risk to organizational operations, assets, and individuals
- Scanning for vulnerabilities in systems and applications periodically and when new vulnerabilities are identified
- Remediating vulnerabilities in accordance with risk assessments

### 12. Security Assessment (CA) -- 4 Requirements

Requires organizations to periodically assess their security controls to determine if they are effective, develop and implement plans of action to address deficiencies, and monitor security controls on an ongoing basis. This family creates the foundation for continuous compliance:

- Periodically assessing security controls to determine effectiveness
- Developing and implementing plans of action to correct deficiencies and reduce vulnerabilities
- Monitoring security controls on an ongoing basis
- Developing, documenting, and periodically updating system security plans

### 13. System and Communications Protection (SC) -- 16 Requirements

Requires organizations to monitor, control, and protect communications at external and key internal boundaries, and to employ architectural designs, software development techniques, and systems engineering principles that promote effective information security. Key requirements include:

- Monitoring, controlling, and protecting communications at system boundaries
- Employing architectural designs and hardware/software that promote effective security
- Separating user functionality from system management functionality
- Preventing unauthorized and unintended information transfer via shared system resources
- Implementing subnetworks for publicly accessible system components
- Implementing cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission (FIPS-validated cryptography)
- Terminating network connections associated with communications sessions at the end of sessions or after a defined period of inactivity
- Establishing and managing cryptographic keys
- Implementing FIPS-validated cryptography for protecting the confidentiality of CUI

The FIPS-validated cryptography requirements in this family are among the most technically challenging to implement. Standard TLS configurations may use FIPS-approved algorithms but are not necessarily running on FIPS-validated cryptographic modules. The distinction matters.

### 14. System and Information Integrity (SI) -- 7 Requirements

Requires organizations to identify, report, and correct system flaws in a timely manner, protect against malicious code, and monitor system security alerts and advisories. Covers:

- Identifying, reporting, and correcting information and system flaws in a timely manner
- Providing protection from malicious code at appropriate locations
- Monitoring system security alerts and advisories and taking appropriate action
- Updating malicious code protection mechanisms when new releases are available
- Performing periodic and real-time scans of systems
- Monitoring systems to detect unauthorized use and attacks
- Identifying unauthorized use of organizational systems

---

## NIST 800-171 Rev. 3: What Changed

NIST published the final version of SP 800-171 Revision 3 in May 2024, and it represents the most significant restructuring since the original publication. Organizations currently assessed against Revision 2 need to understand these changes, because CMMC and DFARS requirements will eventually transition to Rev. 3.

### Structural Overhaul

Revision 3 fundamentally changes how requirements are organized and expressed. The 110 "security requirements" of Revision 2 have been replaced with a new structure that more closely mirrors NIST SP 800-53 Revision 5. Instead of deriving requirements and paraphrasing them, Rev. 3 directly references 800-53 Rev. 5 controls and maps each NIST 800-171 requirement to its parent 800-53 control with greater precision.

The number of requirements changed. Some Revision 2 requirements were consolidated, others were split into more granular requirements, and new requirements were added to address emerging threats. The total requirement count differs from the familiar 110 of Revision 2.

### Key Changes

**Closer alignment with NIST 800-53 Rev. 5.** Revision 3 adopts the language, structure, and organization principles of [NIST SP 800-53](/blog/nist-800-53-controls) Rev. 5 rather than paraphrasing them. This makes it easier to trace each 800-171 requirement back to its parent 800-53 control and understand the intent behind it.

**New and enhanced requirements.** Revision 3 adds requirements that address:

- Supply chain risk management -- reflecting the growing threat of supply chain compromise
- Threat intelligence integration -- formalizing the use of threat feeds and threat hunting
- Enhanced logging and monitoring -- driven by lessons learned from nation-state intrusions where adversaries operated undetected for months
- System resilience -- requirements for ensuring system availability and recovery in the face of advanced persistent threats

**Organization-defined parameters (ODPs).** Following the 800-53 Rev. 5 model, Rev. 3 introduces ODPs -- values that the implementing organization must define based on their risk assessment. For example, instead of specifying a fixed number of unsuccessful login attempts before lockout, the requirement allows the organization to define that threshold.

**Removal of NFO (Nonfederal Organization) controls.** Revision 2 included a set of NFO controls that were expected to be in place but not assessed. Revision 3 eliminates this concept, making the requirement set cleaner and more direct.

### Transition Timeline

As of early 2026, CMMC Level 2 assessments are still based on NIST 800-171 Revision 2. The DoD has not yet announced a formal transition date to Revision 3 for CMMC purposes. However, organizations building their compliance programs today should be aware of Rev. 3 and consider designing their controls to accommodate both versions. The transition, when it comes, will require reassessment against the updated requirements.

---

## NIST 800-171 vs CMMC 2.0: How They Relate

The relationship between NIST 800-171 and [CMMC](/blog/cmmc-compliance) is a source of persistent confusion in the defense contracting community. Here is the definitive explanation.

**CMMC Level 2 equals NIST 800-171.** The 110 practices required for CMMC Level 2 certification are the 110 security requirements from NIST SP 800-171 Revision 2. They are not "based on" or "aligned with" -- they are identical. If you fully implement NIST 800-171, you have met the technical requirements for CMMC Level 2.

**CMMC adds verification.** NIST 800-171 by itself is a self-assessed standard. Contractors implement the requirements, score themselves using the NIST SP 800-171A assessment methodology, submit their score to the SPRS database, and attest to its accuracy. CMMC Level 2, for most contracts involving CUI, requires independent third-party assessment by a CMMC Third-Party Assessment Organization (C3PAO). The controls are the same; the verification mechanism is different.

**CMMC adds contractual enforcement.** Under the current DFARS regime, the consequence of non-compliance with NIST 800-171 was theoretically significant (breach of contract, False Claims Act exposure) but practically limited because nobody was checking. CMMC makes certification a prerequisite for contract award. No certification, no contract. This transforms 800-171 compliance from a contractual obligation that was widely ignored into a competitive requirement that directly affects revenue.

### The Three-Level Structure

| CMMC Level | Standard | Requirements | Assessment |
|---|---|---|---|
| Level 1 (Foundational) | FAR 52.204-21 | 17 practices | Annual self-assessment |
| Level 2 (Advanced) | NIST SP 800-171 Rev. 2 | 110 requirements | C3PAO assessment (most contracts) |
| Level 3 (Expert) | NIST SP 800-172 | 110 + selected 800-172 enhancements | Government-led assessment |

**Practical implication:** If you are a defense contractor, do not think of NIST 800-171 and CMMC as separate compliance efforts. They are the same effort. Implement 800-171 thoroughly, and you are ready for CMMC Level 2 assessment. The only additional CMMC-specific work involves preparing for the assessment process itself -- organizing evidence, preparing for assessor interviews, and ensuring your System Security Plan (SSP) and Plan of Action and Milestones (POA&M) are assessment-ready.

---

## NIST 800-171 vs NIST 800-53: Key Differences

NIST 800-171 and [NIST SP 800-53](/blog/nist-800-53-controls) are related but serve different audiences, scopes, and purposes. Understanding the differences prevents a common mistake: treating 800-171 as a standalone framework when it is actually a derived subset of a much larger control catalog.

### Audience

- **NIST 800-53:** Federal agencies and organizations operating federal information systems. It is the control catalog that agencies use to comply with FISMA.
- **NIST 800-171:** Nonfederal organizations -- contractors, subcontractors, grantees -- that handle CUI on behalf of the government but operate their own (nonfederal) systems.

### Scope

- **NIST 800-53:** Over 1,000 controls and control enhancements across 20 control families. Three baselines (Low, Moderate, High) that agencies select based on system categorization. Comprehensive coverage of every aspect of information security and privacy.
- **NIST 800-171:** 110 security requirements across 14 control families. A single baseline derived from the 800-53 Moderate baseline, minus controls that are either uniquely federal in nature (e.g., security authorization processes that assume a federal agency structure) or expected to be met without specification (e.g., basic physical security that any organization would reasonably have).

### Derivation

NIST 800-171's requirements were derived from 800-53 through a specific process:

1. Start with the NIST 800-53 Moderate baseline controls
2. Remove controls that are primarily the responsibility of the federal government (e.g., government-specific security planning requirements)
3. Remove controls that are not directly related to protecting the confidentiality of CUI
4. Tailor the remaining controls for nonfederal organizations

The result is a streamlined set of requirements that provides an equivalent level of CUI protection to what a federal agency would provide using the full 800-53 Moderate baseline, but without requiring nonfederal organizations to implement the full federal apparatus.

### Practical Comparison

| Dimension | NIST 800-53 | NIST 800-171 |
|---|---|---|
| Total controls | 1,000+ | 110 |
| Control families | 20 | 14 |
| Baselines | Low, Moderate, High | Single (derived from Moderate) |
| Primary audience | Federal agencies | Nonfederal organizations |
| Required by | FISMA, FedRAMP | DFARS, CMMC |
| Privacy controls | Integrated | Not included (focused on confidentiality) |
| Assessment methodology | NIST SP 800-53A | NIST SP 800-171A |

Organizations pursuing [FedRAMP](/blog/case-study-govtech-fedramp) authorization must implement the full 800-53 Moderate or High baseline. Organizations pursuing CMMC Level 2 implement 800-171. If your compliance roadmap includes both federal civilian and defense work, understanding how 800-171 maps back to 800-53 allows you to build a unified control environment that satisfies both requirements.

---

## The Self-Assessment Process: SPRS Scoring

Until CMMC assessments become universally required across all DoD contracts, most defense contractors demonstrate NIST 800-171 compliance through self-assessment and submission of their score to the **Supplier Performance Risk System (SPRS)**.

### How SPRS Scoring Works

The SPRS scoring methodology is defined in NIST SP 800-171 DoD Assessment Methodology. It works as follows:

1. **Start with a perfect score of 110.** Each of the 110 NIST 800-171 requirements is assigned a point value. The total possible score is 110.
2. **Subtract points for unmet requirements.** Each requirement that is not fully implemented results in a deduction. The deduction values are weighted -- some requirements are worth 1 point, others are worth 3 or 5 points, depending on their criticality to CUI protection.
3. **The minimum passing score varies.** There is no officially mandated minimum SPRS score for all contracts, but contracting officers increasingly set score thresholds in solicitations. A score of 110 means full implementation. Scores above 0 indicate partial implementation with identified gaps. Negative scores are possible if many weighted requirements are unmet.
4. **POA&Ms must accompany gaps.** For any requirement that is not fully met, the contractor must document a Plan of Action and Milestones (POA&M) that describes the deficiency, the planned remediation, the resources allocated, and the expected completion date.

### Weighted Scoring Values

Not all 110 requirements carry equal weight. The DoD assessment methodology assigns each requirement a value of 1, 3, or 5 points:

- **5-point requirements** are foundational controls whose absence creates critical risk. Examples include multifactor authentication (IA), FIPS-validated encryption (SC), and audit logging (AU).
- **3-point requirements** represent important but somewhat less critical controls.
- **1-point requirements** are supporting controls that contribute to overall security but whose absence has a more limited individual impact.

A contractor that is missing three 5-point controls will have a much lower score than one missing five 1-point controls, even though the latter has more total gaps. This weighting reflects the DoD's assessment of which controls matter most for CUI protection.

### Common Scoring Mistakes

**Overclaiming implementation.** Contractors frequently mark requirements as "met" when they have partial implementations. If you have a password policy that requires complexity but does not enforce it technically, that requirement is not met. Assessors will test -- not just review documentation.

**Ignoring inherited controls.** If you use a cloud service provider that handles certain controls (e.g., physical security for infrastructure hosted in AWS GovCloud), you can claim those controls as met through inheritance. But you must document the inheritance relationship and verify that the CSP actually meets the control requirements.

**Failing to update.** SPRS scores must be current. If your security posture changes -- new systems, staff turnover, configuration drift -- your score should be reassessed and updated.

---

## Step-by-Step Implementation Guide

Implementing NIST 800-171 is a structured process. Rushing into technical controls without proper scoping and planning leads to wasted effort, missed requirements, and failed assessments. The following ten-step approach provides a proven roadmap.

### Step 1: Define Your CUI Boundary

Before implementing any controls, you must know exactly where CUI exists in your environment. This means identifying:

- Every system that stores, processes, or transmits CUI
- Every network segment that carries CUI
- Every person who accesses CUI
- Every physical location where CUI is present (including paper records)

The goal is to define a clear **CUI boundary** -- the set of systems, networks, and people that fall within the scope of your NIST 800-171 implementation. Everything inside the boundary must comply. Everything outside the boundary does not -- but the boundary controls that separate CUI systems from non-CUI systems are themselves in scope.

**Key principle:** The smaller your CUI boundary, the lower your compliance cost. Many organizations reduce scope by isolating CUI processing into a dedicated enclave -- separate systems, separate network segments, separate user accounts -- rather than applying 800-171 controls across their entire enterprise IT environment.

### Step 2: Categorize Your CUI

Identify the specific CUI categories present in your environment using the NARA CUI Registry. Different categories may have different handling requirements. Controlled Technical Information has specific dissemination controls. Export-controlled information carries ITAR or EAR obligations in addition to NIST 800-171 requirements.

Document every CUI category you handle, where it comes from (which government agency or prime contractor), and what specific handling requirements apply.

### Step 3: Conduct a Gap Assessment

Perform a systematic, requirement-by-requirement assessment of your current security posture against all 110 NIST 800-171 requirements. For each requirement, determine:

- **Met:** The requirement is fully implemented, operational, and supported by evidence
- **Partially met:** Some elements are in place but gaps remain
- **Not met:** The requirement is not addressed

Use the assessment procedures in **NIST SP 800-171A** as your methodology. This publication provides specific assessment objectives and examination, interview, and testing methods for each requirement.

Be honest. An inflated gap assessment wastes money (you will not fix what you think is already fixed) and creates legal risk (your SPRS score will be inaccurate).

### Step 4: Calculate Your SPRS Score

Based on your gap assessment, calculate your SPRS score using the DoD's weighted methodology. This gives you a quantitative baseline and helps you prioritize remediation -- closing 5-point gaps first will yield the largest score improvement per effort.

### Step 5: Develop Your System Security Plan (SSP)

The SSP is the foundational compliance document. It describes:

- Your system and its boundaries
- The operational environment
- How each of the 110 requirements is implemented (or planned for implementation)
- The roles and responsibilities for security
- The connections to other systems

NIST provides an SSP template that aligns with 800-171, but your SSP must be tailored to accurately describe your specific environment. A generic, template-only SSP will not survive assessment scrutiny.

### Step 6: Create Your Plan of Action and Milestones (POA&M)

For every requirement that is not fully met, create a POA&M entry that documents:

- The specific deficiency
- The planned remediation action
- The resources required (budget, personnel, technology)
- The milestone dates for completion
- The risk accepted in the interim

POA&Ms are living documents. They demonstrate to assessors and contracting officers that you have identified your gaps and have a concrete plan to close them.

### Step 7: Implement Technical Controls

With your gaps identified and prioritized, begin implementing the technical controls. Common high-priority implementations include:

- **FIPS-validated encryption** for data at rest and in transit (SC family)
- **Multifactor authentication** for all remote access and privileged accounts (IA family)
- **Audit logging** with centralized collection, review, and alerting (AU family)
- **Endpoint protection** with real-time scanning and automatic updates (SI family)
- **Network segmentation** to isolate CUI systems (SC family)
- **Vulnerability scanning** on a regular schedule with documented remediation (RA family)
- **Configuration baselines** using CIS Benchmarks or DISA STIGs (CM family)

### Step 8: Develop Policies and Procedures

Each control family requires supporting policies and procedures. These are not optional -- they are themselves requirements (see the Security Assessment family, requirement 3.12.4: develop, document, and periodically update system security plans). At minimum, you need:

- An Information Security Policy that covers all 14 control families
- An Incident Response Plan
- A Configuration Management Plan
- An Access Control Policy
- A Media Protection and Handling Procedure
- A Risk Assessment Procedure
- A Security Awareness and Training Program

### Step 9: Train Your Workforce

Awareness and Training (AT) requirements mandate that all users understand their security responsibilities and that personnel with security roles receive specialized training. Implement:

- General security awareness training for all employees with CUI access
- Role-based training for system administrators, security personnel, and incident responders
- Training on CUI identification, marking, and handling
- Annual refresher training with documented completion records

### Step 10: Establish Continuous Monitoring

NIST 800-171 compliance is not a one-time achievement. Requirement 3.12.3 explicitly requires ongoing monitoring of security controls. Build a continuous monitoring program that includes:

- Regular vulnerability scanning (at least monthly)
- Continuous audit log review and alerting
- Periodic reassessment of security controls (at least annually)
- Configuration drift detection and remediation
- Incident response testing and tabletop exercises
- POA&M tracking and closure
- SSP updates as the environment changes

---

## NIST 800-171 Compliance Cost and Timeline

Honest estimates matter. Too many organizations begin their compliance journey with unrealistic budgets and timelines, leading to abandoned projects, inflated self-assessments, or compliance programs that exist only on paper.

### Cost Ranges

The total cost of NIST 800-171 compliance depends on the size of your organization, the maturity of your existing security program, the scope of your CUI environment, and whether you use internal resources or external consultants.

| Organization Size | Starting Maturity | Estimated Cost Range | Primary Cost Drivers |
|---|---|---|---|
| Small (< 50 employees) | Low | $50,000 - $150,000 | Technology (MFA, SIEM, encryption), consulting, policy development |
| Small (< 50 employees) | Moderate (existing SOC 2 or ISO 27001) | $25,000 - $75,000 | Gap remediation, CUI-specific controls, documentation |
| Mid-size (50-500 employees) | Low | $150,000 - $500,000 | Technology infrastructure, consulting, dedicated staff time |
| Mid-size (50-500 employees) | Moderate | $75,000 - $250,000 | Gap remediation, FIPS encryption, enclave architecture |
| Large (500+ employees) | Low | $500,000 - $2,000,000+ | Enterprise-wide deployment, multiple enclaves, staffing |
| Large (500+ employees) | Moderate | $200,000 - $750,000 | Gap remediation, FIPS migration, continuous monitoring |

**The biggest cost variable is scope.** A company that processes CUI on three dedicated workstations in an isolated network will spend a fraction of what a company that allows CUI across its entire enterprise environment will spend. Scope reduction is the single most effective cost control strategy.

### Timeline Ranges

| Starting Point | Typical Timeline to Assessment-Ready |
|---|---|
| Greenfield (no existing security program) | 12 - 18 months |
| Existing SOC 2 or ISO 27001 | 6 - 9 months |
| Existing partial 800-171 implementation | 3 - 6 months |
| Existing strong implementation with minor gaps | 1 - 3 months |

**Critical path items** that typically determine the timeline:

- FIPS-validated encryption deployment (can require application changes, vendor coordination, and testing)
- SIEM/log management deployment and tuning
- Network architecture changes for CUI enclave isolation
- Policy and procedure development and approval
- Security awareness training rollout
- Vulnerability remediation backlog

### The Hidden Costs

Do not overlook ongoing costs. NIST 800-171 compliance requires continuous investment:

- Annual security assessments
- Continuous vulnerability scanning (tool licensing)
- Security awareness training (annual renewal)
- SIEM/log management platform costs
- Staff time for ongoing monitoring and POA&M management
- Periodic policy reviews and updates
- Incident response readiness (tabletop exercises, on-call coverage)

A compliance automation platform like [QuickTrust](/) can significantly reduce both initial implementation cost and ongoing maintenance burden by automating evidence collection, policy management, control monitoring, and assessment preparation.

---

## Common NIST 800-171 Compliance Gaps

After working with defense contractors at every stage of their compliance journey, these are the gaps we see most frequently. Every one of them is avoidable.

### 1. FIPS-Validated Encryption

This is the single most common compliance gap. NIST 800-171 requirements 3.13.8 and 3.13.11 require FIPS-validated cryptography to protect CUI confidentiality. Many organizations use encryption that employs FIPS-approved algorithms (AES-256, SHA-256) but runs on cryptographic modules that have not been independently validated through the NIST Cryptographic Module Validation Program (CMVP). "Uses AES-256" is not the same as "uses a FIPS 140-2/140-3 validated module." Check the NIST CMVP validated modules list for every cryptographic implementation in your CUI boundary.

### 2. Incomplete Audit Logging

Organizations frequently deploy audit logging but fail to meet the full scope of requirements: logs must cover all CUI-relevant events, logs must be correlated across systems, log integrity must be protected, logs must be reviewed regularly (not just stored), and alerting must be in place for critical events. A SIEM that collects logs but that nobody reviews does not satisfy the Audit and Accountability family.

### 3. Inadequate Multifactor Authentication

NIST 800-171 requires MFA for both remote access and privileged accounts. Common gaps include: MFA not enforced on all remote access methods (VPN but not web applications), MFA not applied to all privileged accounts (domain admin but not database admin), and use of SMS-based authentication that does not meet NIST SP 800-63B requirements for verifier assurance.

### 4. Missing or Generic System Security Plan

The SSP must accurately describe your specific environment, not just restate the 110 requirements with "implemented" next to each one. Assessors read SSPs carefully. A credible SSP describes the system architecture, data flows, boundary controls, and specific implementation details for each requirement.

### 5. CUI Scope Creep

Organizations that fail to define and enforce a clear CUI boundary end up with CUI scattered across systems, devices, email accounts, and cloud services that were never intended to be in scope. This dramatically increases the compliance surface and makes it nearly impossible to implement and verify all 110 controls consistently.

### 6. Uncontrolled Remote Access

The shift to remote and hybrid work expanded the attack surface for CUI. Requirements around remote access control (AC family), CUI at alternate work sites (PE family), and mobile device management are frequently underimplemented. Every remote access path to CUI must be inventoried, controlled, and monitored.

### 7. Stale Plans of Action and Milestones

POA&Ms must be actively managed. Organizations that create POA&Ms during their initial assessment and never update them signal to assessors that compliance is not a priority. POA&M items should have realistic milestones, assigned owners, and regular status reviews. Items that remain open indefinitely without progress raise serious questions about organizational commitment.

### 8. Personnel Security Gaps

The Personnel Security family has only two requirements, but they are frequently unmet. Background screening before granting CUI access is often inconsistent, and access revocation upon personnel departure is often delayed. Every day that a terminated employee retains CUI access is a day of unnecessary risk.

---

## Frequently Asked Questions

### What is the difference between NIST 800-171 and CMMC?

NIST 800-171 defines the 110 security requirements for protecting CUI. [CMMC Level 2](/blog/cmmc-compliance) uses those same 110 requirements as its technical baseline but adds independent third-party verification. Think of NIST 800-171 as the exam content and CMMC as the proctoring system that ensures you actually took the exam honestly.

### Is NIST 800-171 compliance mandatory?

It depends on your contracts. If you hold or pursue a DoD contract that includes DFARS clause 252.204-7012, NIST 800-171 compliance is a binding contractual requirement. Non-compliance creates exposure under the False Claims Act. For organizations not subject to DFARS, NIST 800-171 is a voluntary standard, though it is increasingly referenced in civilian agency contracts.

### How long does NIST 800-171 compliance take?

For most organizations starting from scratch, 12 to 18 months is realistic. Organizations with existing security frameworks like [SOC 2](/soc-2-compliance) or [ISO 27001](/iso-27001-certification) can typically achieve compliance in 6 to 9 months due to significant control overlap. The timeline depends primarily on the scope of your CUI environment and the maturity of your existing security program.

### What is a passing SPRS score?

There is no universally defined "passing" score. The maximum score is 110 (all requirements met). Contracting officers may set minimum score thresholds in individual solicitations. A score of 110 is obviously ideal; scores significantly below 70 suggest substantial gaps that need remediation. Any score submitted to SPRS must be accompanied by POA&Ms for all unmet requirements.

### Can I use a cloud service provider to meet NIST 800-171 requirements?

Yes, but with important caveats. You can inherit certain controls from your CSP -- for example, physical security controls if you host your CUI environment in AWS GovCloud or Microsoft Azure Government. However, you remain responsible for ensuring the CSP actually meets those controls (verify through their FedRAMP authorization or SOC 2 reports), and many requirements cannot be inherited because they relate to how *you* configure and use the cloud environment. The shared responsibility model applies.

### What happens if I am not compliant with NIST 800-171?

The consequences range from losing contract eligibility (as CMMC enforcement expands) to False Claims Act liability (if you submitted an inaccurate SPRS score) to breach of contract claims. The Department of Justice has pursued enforcement actions against defense contractors for cybersecurity misrepresentation. Beyond legal risk, non-compliance means your CUI protection is inadequate, and your systems may already be compromised by adversaries who specifically target defense supply chain companies.

### Does NIST 800-171 apply to subcontractors?

Yes. DFARS 252.204-7012 requires prime contractors to flow down equivalent requirements to subcontractors at all tiers that will handle covered defense information. If you are a subcontractor and you receive CUI from a prime, you must implement NIST 800-171. There is no size exemption and no tier exemption.

### How does NIST 800-171 relate to the NIST Cybersecurity Framework?

The [NIST Cybersecurity Framework (CSF)](/blog/nist-cybersecurity-framework) is a voluntary, high-level risk management framework that helps organizations structure their overall cybersecurity program. NIST 800-171 is a specific, prescriptive set of 110 security requirements for protecting CUI. They are complementary: CSF provides the strategic governance structure, and 800-171 provides the specific controls for CUI environments. Many organizations use CSF as their enterprise cybersecurity framework and 800-171 as the control baseline for systems that handle CUI.

---

## Achieve NIST 800-171 Compliance Faster with QuickTrust

Implementing 110 security requirements across 14 control families while maintaining documentation, tracking POA&Ms, preparing for CMMC assessments, and running continuous monitoring is a massive operational lift -- especially for defense contractors without large dedicated compliance teams.

QuickTrust automates the hardest parts of NIST 800-171 compliance:

- **Automated gap assessment** that maps your current security posture against all 110 requirements and calculates your SPRS score
- **Pre-built policy and procedure templates** tailored to each control family, ready for customization rather than creation from scratch
- **Continuous control monitoring** that detects configuration drift, policy violations, and emerging gaps before they become assessment findings
- **Evidence collection automation** that gathers and organizes the artifacts assessors need to see -- reducing the weeks of manual evidence gathering that typically precede an assessment to days
- **CMMC assessment preparation** with structured workflows that align your documentation and evidence to C3PAO expectations
- **Cross-framework mapping** that connects your NIST 800-171 controls to [NIST 800-53](/blog/nist-800-53-controls), [NIST CSF](/blog/nist-cybersecurity-framework), [SOC 2](/soc-2-compliance), and [ISO 27001](/iso-27001-certification) -- so work done for one framework accelerates compliance with others

Defense contractors that use QuickTrust reduce their time to NIST 800-171 compliance by up to 60% and cut ongoing compliance management effort by 70%.

[Start your free NIST 800-171 gap assessment with QuickTrust -->](/)
