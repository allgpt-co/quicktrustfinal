---
meta_description: "Create an acceptable use policy that satisfies SOC 2, ISO 27001, and HIPAA auditors. Includes template sections, enforcement guidelines, and real-world examples for tech companies."
target_keyword: "acceptable use policy"
secondary_keywords: "acceptable use policy template, AUP policy, acceptable use policy examples, IT acceptable use policy, computer acceptable use policy"
word_count_target: 4000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-19
---

# Acceptable Use Policy: The Complete Guide and Template for Compliance-Ready Tech Companies

Every compliance framework has a control that most companies underestimate until it produces an audit finding: the acceptable use policy.

It sounds straightforward. Write down the rules for how employees use company technology. Get everyone to sign it. Move on to the more technically interesting parts of your security program.

But the acceptable use policy is where auditors test whether your organization actually governs human behavior around information assets — or whether it just governs infrastructure. Your firewalls, encryption, and access controls protect systems from external threats. Your acceptable use policy protects those same systems from the people who have legitimate access to them: your own employees, contractors, and third-party collaborators.

And that is where most breaches originate. According to the 2025 Verizon Data Breach Investigations Report, 68% of breaches involved a non-malicious human element — people clicking phishing links, misconfiguring cloud storage, using unauthorized SaaS tools, or sharing credentials in ways that seemed convenient at the time. An acceptable use policy exists to set the boundaries that prevent these behaviors before they become incidents.

This guide covers how to write an acceptable use policy that satisfies auditors across SOC 2, ISO 27001, HIPAA, and PCI DSS simultaneously — the 12 essential sections it must contain, template language for each, the specific framework requirements it must address, enforcement mechanisms that actually work, and the mistakes that consistently produce audit findings.

**[Generate your audit-ready acceptable use policy with QuickTrust](https://trust.quickintell.com)**

---

## What Is an Acceptable Use Policy (AUP)?

An acceptable use policy is a formal document that defines how employees, contractors, and authorized third parties are permitted to use an organization's information systems, devices, networks, data, and technology resources. It establishes the boundaries between permitted and prohibited behavior when interacting with company technology — and it documents the consequences for crossing those boundaries.

More specifically, the AUP is the **behavioral governance layer** of your security program. Your [information security policy](/blog/information-security-policy-guide) defines what your organization commits to protecting and why. Your technical standards define the specific controls that enforce those commitments. Your acceptable use policy defines what the humans inside your organization must do, may do, and must never do when using the systems those controls protect.

### Purpose

An acceptable use policy serves four distinct purposes:

1. **Behavioral boundaries.** It tells every person with access to your systems exactly what is permitted and what is prohibited — from installing software to using personal email for work communications to connecting personal devices to the corporate network. Without these documented boundaries, employees operate on assumptions, and assumptions produce security incidents.

2. **Legal protection.** An AUP provides the legal basis for monitoring employee activity on company systems and for taking disciplinary action when policy violations occur. Without a signed AUP, an employer's ability to enforce security rules, terminate for violations, or pursue legal action after an insider incident is significantly weakened.

3. **Audit evidence.** Every major compliance framework requires documented controls governing user behavior. The AUP is the primary artifact that satisfies these requirements. Auditors check not only that the policy exists but that it covers specific topics and that every employee has acknowledged it.

4. **Security awareness reinforcement.** The AUP is one of the few security documents that every employee must read and acknowledge. It serves as a recurring touchpoint for security awareness — particularly when re-signed annually — reminding employees of their specific obligations.

### Legal Basis

The enforceability of an acceptable use policy rests on three legal principles:

- **Employment relationship.** Employers have broad rights to establish rules governing how company-owned resources are used. The AUP documents those rules.
- **Consent through acknowledgment.** When an employee signs or electronically acknowledges the AUP, they consent to its terms, including monitoring provisions. This consent is critical in jurisdictions with strong employee privacy protections.
- **Notice.** Many states and countries require employers to notify employees before monitoring their electronic communications or computer usage. The AUP's monitoring disclosure satisfies this legal requirement.

In the United States, the Electronic Communications Privacy Act (ECPA) provides exceptions for employer monitoring when employees have consented — and a signed AUP constitutes that consent. In the EU, GDPR Article 6(1)(f) permits monitoring as a "legitimate interest" when employees have been informed, which the AUP provides. Without a documented, acknowledged AUP, monitoring activities that are routine in most tech companies may lack legal standing.

---

## Why Compliance Frameworks Require an AUP

An acceptable use policy is not a nice-to-have that security teams write when they run out of more important things to document. It is an explicitly required control across every major compliance framework. Here is exactly where each framework sets this requirement and what auditors look for:

### SOC 2 — CC1.4 and CC6.1

SOC 2's Common Criteria address acceptable use in two primary areas:

**CC1.4 (Commitment to Competence)** requires that the organization demonstrates that employees understand their security responsibilities. Auditors use the AUP as evidence that the organization has communicated specific behavioral expectations and that employees have acknowledged them.

**CC6.1 (Logical and Physical Access Controls)** requires that the organization "implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events." In practice, auditors interpret this to include user-level behavioral controls — rules governing what users do with the access they have been granted, not just how that access is authenticated. The AUP provides this documentation.

During a SOC 2 audit, expect the auditor to:
- Request the current AUP
- Check that it was reviewed within the last 12 months
- Verify that acknowledgment records exist for all in-scope personnel
- Confirm that it addresses internet use, email, personal devices, and prohibited activities
- Cross-reference monitoring statements in the AUP against actual monitoring controls

### ISO 27001 — Annex A Control 5.10

ISO 27001:2022 addresses acceptable use directly in **Annex A Control 5.10 ("Acceptable use of information and other associated assets")**. This control requires the organization to:

- Identify and document rules for the acceptable use of information and associated assets
- Ensure that personnel and other interested parties are made aware of the acceptable use requirements for information assets
- Establish procedures for the return of assets upon termination or change of role

The ISO 27001 certification audit will check that Control 5.10 is implemented, that the AUP is referenced in your Statement of Applicability, and that you can demonstrate the policy is communicated and acknowledged. A missing or outdated AUP is a nonconformity that must be resolved before certification.

### HIPAA — 45 CFR 164.310(b) and 164.312(a)

The HIPAA Security Rule does not use the term "acceptable use policy," but its requirements map directly to one:

- **164.310(b) (Workstation Use)** requires covered entities to implement policies and procedures that specify the proper functions to be performed, the manner in which those functions are to be performed, and the physical attributes of the surroundings of workstations that can access ePHI.
- **164.312(a) (Access Control)** requires policies governing who can access ePHI and under what conditions.

In practice, HHS OCR auditors expect to see an acceptable use policy that specifically addresses how systems containing protected health information may be used, prohibits personal use that could compromise PHI security, and defines workstation security requirements.

### PCI DSS — Requirement 12.3

PCI DSS is the most explicit about acceptable use. **Requirement 12.3** states that usage policies for critical technologies must be developed, and these policies must require:

- Explicit management approval for use of technologies
- Authentication for use of the technology
- A list of all such devices and personnel with access
- Labeling of devices with owner, contact information, and purpose
- Acceptable uses of the technology
- Acceptable network locations for the technologies
- Automatic disconnect of sessions after a specific period of inactivity

For organizations handling payment card data, the AUP must address each of these sub-requirements or the QSA will issue a finding.

> **Related:** [The Complete SOC 2 Compliance Guide for SaaS Startups](/blog/soc2-complete-guide) | [ISO 27001 Certification: The Complete Implementation Guide](/blog/iso27001-complete-guide)

---

## The 12 Essential Sections of an Acceptable Use Policy

A compliance-ready acceptable use policy must address 12 distinct domains of user behavior. Each maps to specific control requirements across SOC 2, ISO 27001, HIPAA, and PCI DSS. Omitting any of these sections will leave gaps that auditors will identify.

### 1. General Use and Ownership

This section establishes the foundational principle: company systems and the data on them belong to the company. Users have no expectation of privacy when using company-owned resources.

**Must cover:**
- All company-provided technology (laptops, phones, accounts, licenses) remains company property
- Data created on or transmitted through company systems belongs to the company
- Personal use of company systems, if permitted, is limited and subject to the same monitoring and policy requirements as business use
- Users must protect company assets from unauthorized access, theft, damage, and misuse

### 2. Email and Electronic Communications

Email remains one of the most common vectors for data exfiltration and social engineering. This section governs all electronic communications: email, instant messaging, video conferencing, and collaboration platforms.

**Must cover:**
- Business email must be used for business communications; personal email must not be used for work-related communications
- Prohibition against forwarding confidential or restricted data to personal email accounts
- Rules for email attachments containing sensitive data (encryption requirements)
- Social engineering awareness — instructions not to click unsolicited links, open unexpected attachments, or respond to requests for credentials
- Retention and archival expectations aligned with legal hold and compliance requirements
- Prohibition against impersonation, harassment, and distribution of inappropriate content

### 3. Internet and Web Use

Internet access creates both productivity and security risks. This section defines what is acceptable browsing behavior on company networks and devices.

**Must cover:**
- Permitted use of the internet for business purposes
- Prohibition against accessing illegal, obscene, or malicious websites
- Prohibition against downloading software, browser extensions, or files from untrusted sources
- Prohibition against using company internet access to bypass security controls (VPN tunneling, proxy services)
- Streaming and bandwidth-intensive personal use policies
- Web-based personal storage services (personal Google Drive, Dropbox) — typically prohibited for work data

### 4. Social Media

Social media creates reputational and data leakage risks that require explicit governance.

**Must cover:**
- Prohibition against disclosing confidential company information on social media platforms
- Requirement to use personal accounts (not company accounts) for personal opinions
- Prohibition against claiming to represent the company without authorization
- Security hygiene for social media accounts (no credential reuse with corporate accounts)
- Rules about discussing customers, partners, or vendors on public platforms

### 5. Mobile Devices

Company-issued mobile devices require specific governance because they leave the controlled network perimeter every day.

**Must cover:**
- Device passcode and biometric authentication requirements
- Encryption requirements
- Automatic lock timeout settings
- Approved application installation policies
- Remote wipe capability and consent
- Physical security (not leaving devices unattended in public locations)
- Reporting requirements for lost or stolen devices (immediate reporting, typically within 1-4 hours)
- Restrictions on connecting to untrusted networks

### 6. Bring Your Own Device (BYOD)

BYOD policies are consistently the most audited section of the AUP in 2026, because the boundary between personal and corporate data has become almost impossible to enforce without explicit written rules.

**Must cover:**
- Which personal device types are permitted (laptops, phones, tablets)
- Minimum security requirements for personal devices (OS version, encryption, passcode, antivirus)
- Requirement to enroll in mobile device management (MDM) or endpoint management
- Separation of personal and corporate data (containerization or sandboxing)
- Right to remote wipe corporate data from personal devices upon termination or device loss
- Prohibition against storing corporate data on personal devices outside managed containers
- Privacy expectations — what the company can and cannot see on personal devices

### 7. Cloud Services and SaaS Tools

Shadow IT — employees using unauthorized cloud services — is one of the most common audit findings. This section directly addresses it.

**Must cover:**
- Only approved, vetted cloud services and SaaS tools may be used for business purposes
- Process for requesting approval of new tools (who approves, what security review is required)
- Prohibition against creating accounts on unapproved services using corporate email addresses
- Data storage restrictions (where corporate data may and may not be stored)
- AI tools policy — which generative AI services are approved, what data may and may not be entered into them
- Single sign-on (SSO) and MFA requirements for all approved SaaS tools

### 8. Data Handling and Classification

This section connects the AUP to the organization's data classification scheme and defines how users must handle different categories of data in their daily work.

**Must cover:**
- Reference to the organization's data classification policy (Public, Internal, Confidential, Restricted — or equivalent)
- Handling requirements for each classification level (encryption, sharing, storage, transmission, disposal)
- Prohibition against sharing confidential or restricted data through unapproved channels
- Clean desk and clean screen requirements
- Secure disposal of physical and digital media
- Customer data handling requirements specific to your compliance obligations (PHI for HIPAA, cardholder data for PCI DSS)

### 9. Software Installation and Licensing

Unauthorized software is both a security risk and a legal liability.

**Must cover:**
- Prohibition against installing software on company devices without IT approval
- Prohibition against using pirated, unlicensed, or cracked software
- Approved software list or approved software request process
- Restriction on browser extensions and plugins
- Prohibition against disabling or circumventing endpoint security software (EDR, antivirus, DLP agents)
- Open source software usage policy for engineering teams

### 10. Remote Work

With remote and hybrid work now permanent at most tech companies, this section addresses the security requirements specific to working outside the office.

**Must cover:**
- VPN requirements for accessing internal resources
- Home network security recommendations (WPA3, router firmware updates, no shared or public networks for sensitive work)
- Physical security of work devices and documents in home environments
- Screen lock and privacy screen requirements when working in shared or public spaces
- Prohibition against using public WiFi for accessing company systems without VPN
- Coworking space and shared office security requirements
- Video conferencing security (screen sharing awareness, meeting room locks)
- Prohibition against allowing family members or other unauthorized individuals to use work devices

### 11. Monitoring Notice

This is the most legally important section of the AUP. It discloses that the organization monitors system usage and provides the legal basis for that monitoring.

**Must cover:**
- Clear, unambiguous statement that the company monitors use of its systems, networks, devices, and communications
- Types of monitoring conducted (network traffic, email content, web browsing, endpoint activity, file access)
- Purpose of monitoring (security, compliance, performance, investigation)
- Statement that users have no expectation of privacy when using company systems
- Reference to applicable law (ECPA in the US, relevant national law elsewhere)
- Statement that monitoring may occur without additional notice
- Consent mechanism (acknowledgment signature)

**Example language:**
"[Company Name] reserves the right to monitor, intercept, review, and disclose all activity on company-owned systems, devices, and networks, including but not limited to email, instant messaging, web browsing, file transfers, and application usage. Users should have no expectation of privacy when using company resources. By signing this policy, you consent to such monitoring."

### 12. Enforcement and Consequences

A policy without consequences is a suggestion. This section must make clear that violations produce real outcomes.

**Must cover:**
- Statement that violations will result in disciplinary action
- Range of possible consequences (verbal warning, written warning, suspension, termination, legal action)
- Factors considered in determining consequences (severity, intent, prior violations, impact)
- Right to investigate suspected violations
- Obligation to report observed violations (and how to report)
- Statement that criminal violations will be reported to law enforcement

---

## Acceptable Use Policy Template: Section-by-Section Guide

Below is a section-by-section template with example language that meets auditor expectations across all major frameworks. Adapt the specific requirements to your organization's risk profile, industry, and technical environment.

### Policy Header

```
ACCEPTABLE USE POLICY

Version: [X.X]
Effective Date: [Date]
Last Reviewed: [Date]
Policy Owner: [CISO / IT Director / VP of Engineering]
Approved By: [CEO / CTO / Board]
Next Review Date: [Date + 12 months]
Classification: Internal
```

Every auditor checks the header first. A policy without a version number, approval signature, or review date generates an immediate finding.

### Section 1: Purpose

"This Acceptable Use Policy establishes the rules and guidelines governing the use of [Company Name]'s information systems, technology resources, and data by all authorized users. The purpose of this policy is to protect [Company Name]'s information assets, ensure compliance with applicable legal and regulatory requirements (including SOC 2, ISO 27001, HIPAA, and PCI DSS), reduce organizational risk, and ensure that technology resources are used in a manner consistent with the company's business objectives and security posture."

### Section 2: Scope

"This policy applies to all employees, contractors, temporary staff, interns, consultants, and third-party users who are granted access to [Company Name]'s information systems, technology resources, networks, data, or facilities. It applies to all company-owned devices (laptops, mobile phones, tablets, servers), all company-managed accounts and services, all personal devices used to access company resources, and all locations from which company resources are accessed, including corporate offices, home offices, coworking spaces, and public locations."

### Section 3: General Use and Ownership

"All technology resources provided by [Company Name] — including but not limited to hardware, software, network access, email accounts, cloud service accounts, and data storage — remain the property of [Company Name]. Users are granted access to these resources solely for the purpose of performing their assigned job functions. Limited personal use of company resources is permitted provided it does not interfere with job performance, does not consume significant resources, does not violate any section of this policy, and does not create security, legal, or compliance risks."

### Section 4: Prohibited Activities

This section is where the AUP must be explicit. Vague language produces vague enforcement. Include at minimum:

"The following activities are strictly prohibited:

- Sharing, lending, or disclosing user credentials (passwords, MFA tokens, API keys) to any other person
- Accessing systems, data, or resources outside the scope of assigned job responsibilities
- Installing software, browser extensions, or applications not approved by IT
- Connecting unauthorized devices to the corporate network
- Storing company data on personal cloud storage accounts (personal Google Drive, Dropbox, iCloud) outside approved channels
- Disabling, bypassing, or interfering with security controls, including endpoint protection, firewalls, and DLP tools
- Using company resources for illegal activities of any kind
- Attempting to gain unauthorized access to any system, account, or data (even as a test, unless formally authorized by the security team)
- Sending, forwarding, or storing material that is harassing, discriminatory, threatening, or obscene
- Using company email or accounts to sign up for personal services unrelated to work
- Connecting to company resources over unsecured public WiFi without using the company VPN
- Entering confidential, restricted, or customer data into unapproved AI tools or generative AI platforms"

### Section 5: Data Handling

"Users must handle company data in accordance with the [Company Name] Data Classification Policy. At minimum:

- **Restricted data** (e.g., PHI, cardholder data, encryption keys, customer authentication credentials) must be encrypted at rest and in transit, accessed only on approved systems, never stored locally on endpoints, and never transmitted through email without encryption.
- **Confidential data** (e.g., customer data, financial records, source code, internal communications) must be accessed only by authorized personnel, stored only on approved company systems and services, and shared externally only with written approval from the data owner.
- **Internal data** (e.g., internal procedures, project documentation, meeting notes) must not be shared externally without approval.
- **Public data** (e.g., published marketing materials, open-source documentation) may be shared freely."

### Section 6: Remote Work and BYOD

"Employees working remotely must:

- Use the company-provided VPN when accessing internal company resources
- Ensure their home network uses WPA3 (or WPA2 minimum) encryption with a strong, unique password
- Lock their screen whenever stepping away from their workstation
- Use a privacy screen in shared or public spaces
- Never allow unauthorized individuals (including family members) to access company devices
- Report any suspected compromise of their home network or work device immediately

Employees using personal devices (BYOD) for work must:

- Enroll their device in the company's mobile device management (MDM) system
- Maintain a minimum OS version as specified by IT
- Enable full-disk encryption and device passcode/biometric authentication
- Accept that [Company Name] may remote-wipe corporate data from the device upon termination, device loss, or suspected compromise
- Understand that corporate data on personal devices is subject to the same classification and handling requirements as data on company-owned devices"

### Section 7: Cloud Services and AI Tools

"Only cloud services and SaaS applications that have been approved by the IT/Security team and added to the company's approved tools list may be used for business purposes. To request approval for a new tool, submit a request through [ticketing system]. The security team will conduct a vendor risk assessment before approval is granted.

The use of generative AI tools (including but not limited to ChatGPT, Claude, Gemini, Copilot, and similar services) is governed by the following rules:

- Only AI tools on the approved tools list may be used for work purposes
- Confidential, restricted, or customer data must never be entered into any AI tool unless that tool has been specifically approved for such data by the security team
- AI-generated code must be reviewed for security vulnerabilities before deployment to production
- Users must not rely on AI outputs for compliance, legal, or financial decisions without human review"

### Section 8: Monitoring and Privacy

"[Company Name] monitors the use of its technology resources, including but not limited to email, web browsing, file transfers, instant messaging, application usage, and endpoint activity. This monitoring is conducted for purposes of security, compliance, performance management, and investigation of suspected policy violations.

Users should have no expectation of privacy when using company-owned or company-managed systems, even if personal use is incidentally permitted. By acknowledging this policy, you consent to such monitoring.

Monitoring activities are conducted in compliance with applicable federal, state, and local laws."

### Section 9: Enforcement

"Violations of this policy may result in disciplinary action up to and including termination of employment or contract. In determining the appropriate response, [Company Name] will consider the severity of the violation, whether it was intentional or negligent, the user's history of compliance, and the impact on the organization and its customers.

Violations that involve illegal activity may be referred to law enforcement authorities.

All employees have an obligation to report suspected policy violations to their manager or the security team at [security email address]. Reports may also be submitted anonymously through [reporting channel]. Retaliation against individuals who report policy violations in good faith is strictly prohibited."

### Section 10: Acknowledgment

"I have read the [Company Name] Acceptable Use Policy in its entirety. I understand its contents and agree to comply with its terms. I understand that violation of this policy may result in disciplinary action, up to and including termination of employment or contract, and potential legal action.

Signature: _______________
Printed Name: _______________
Date: _______________"

> **Related:** [Cybersecurity Policy Templates: The 15 Policies Every SaaS Company Needs](/blog/cybersecurity-policy-templates-guide) | [Information Security Policy: The Complete Guide](/blog/information-security-policy-guide)

---

## AUP for Remote and Hybrid Workforces

The shift to remote and hybrid work has fundamentally changed what an acceptable use policy must address. An AUP written for an office-only workforce is no longer sufficient for audit, and auditors in 2026 specifically look for remote work provisions.

### The Expanded Attack Surface

When employees work from home, the security perimeter extends to every home network, personal device, shared apartment, coffee shop, and airport lounge where work happens. The acceptable use policy must address this expanded attack surface explicitly.

**Home network security.** Most home networks were not designed with enterprise security in mind. An AUP for remote workers should require:
- WPA3 or WPA2-minimum encryption on home WiFi
- A unique, strong WiFi password (not the ISP default)
- Router firmware kept up to date
- Separation from IoT devices when possible (using a guest network for smart home devices)

Auditors will not inspect employees' home routers, but they will check that your AUP documents these requirements. The documented requirement is what satisfies the control.

**Public WiFi.** The AUP should contain an unambiguous prohibition: do not connect to company resources over public WiFi without using the company VPN. No exceptions. No "if the VPN is unavailable, use your judgment." Public WiFi is an untrusted network. Period.

**Physical security at home.** This is often overlooked, but auditors check for it, particularly in HIPAA and PCI DSS contexts. The AUP should require:
- A lockable workspace or the ability to secure work devices when not in use
- Screens not visible to unauthorized household members during calls or work sessions
- Company documents (if printed) stored and disposed of securely
- Awareness that smart home devices (Alexa, Google Home) with always-on microphones may capture sensitive conversations

### BYOD Challenges in Remote Work

Remote workers are far more likely to use personal devices for work tasks — checking email on a personal phone, joining a meeting from a personal tablet, transferring a file to a personal laptop "just this once." The AUP must anticipate these behaviors and set clear rules:

- If personal devices are permitted, they must meet minimum security requirements and enroll in MDM
- If personal devices are not permitted for specific activities (e.g., accessing production systems, handling PHI), the prohibition must be explicit
- The right to remote-wipe corporate data must be documented and acknowledged before the personal device is used for work

The most common audit finding in this area is a BYOD policy that exists on paper but has no MDM enrollment records to back it up. If your AUP says personal devices must enroll in MDM, the auditor will ask for enrollment records. If those records do not match your employee list, you have a finding.

---

## AUP for Cloud Services and SaaS Tools

Shadow IT is one of the fastest-growing compliance risks in tech companies. Research consistently shows that the average mid-market company has 3-4 times more SaaS applications in active use than IT is aware of. Employees sign up for project management tools, design platforms, file-sharing services, and AI assistants using their corporate email — and each one becomes an unvetted data repository outside the organization's security controls.

### The Shadow IT Problem

The acceptable use policy is the primary governance document for preventing shadow IT. Without it, employees operate under the reasonable assumption that any tool that helps them do their job is acceptable to use. The AUP must correct that assumption explicitly:

- Only tools on the approved software list may be used for business purposes
- Creating accounts on unapproved services using a corporate email address is prohibited
- Storing company data on unapproved platforms (personal cloud storage, unapproved SaaS tools, personal messaging apps) is prohibited
- Requesting approval for new tools is expected and encouraged — the goal is not to block innovation but to ensure security review

### Maintaining an Approved Tools List

The AUP should reference (not contain) an approved tools list. This list is a living document maintained by IT or the security team. It includes:

- Tool name and purpose
- Data classification level approved for the tool (e.g., "approved for Internal data only" vs. "approved for Confidential data")
- Authentication requirements (SSO, MFA)
- Vendor risk assessment status
- Data processing agreement status

The approved tools list changes frequently. Embedding it in the AUP would require constant policy updates. Instead, the AUP states that users must consult the current approved tools list and references where to find it.

### AI Tools: The 2026 AUP Challenge

Generative AI tools are the single biggest addition to acceptable use policies in 2026. Most organizations have employees using AI tools daily, and most AUPs written before 2024 do not address them at all.

The AUP must cover:
- Which AI tools are approved for business use
- What data may be entered into approved AI tools (typically, nothing above Internal classification unless the tool has been specifically vetted for higher sensitivity)
- Prohibition against entering customer data, PHI, PII, source code, financial data, or other confidential/restricted information into AI tools that have not been approved for that data category
- Requirements for human review of AI-generated outputs before they are used in production, shared with customers, or used for decision-making
- Intellectual property considerations — AI-generated content may have unclear IP ownership depending on the tool's terms of service

Auditors are increasingly asking about AI governance during SOC 2 and ISO 27001 audits. An AUP that does not mention AI tools signals that the organization has not addressed a significant and rapidly evolving risk vector.

---

## Enforcement: Violations, Consequences, and Due Process

An acceptable use policy without an enforcement mechanism is not a policy. It is a document that employees sign and forget. Enforcement is what transforms the AUP from a formality into a functional security control — and auditors specifically evaluate whether the organization enforces its AUP, not just whether one exists.

### Building a Proportional Consequences Framework

Not all violations are equal. An employee who accidentally visits a blocked website is not in the same category as one who intentionally exfiltrates customer data. Your enforcement framework must account for this range:

**Tier 1 — Minor, Unintentional Violations:**
Examples: Forgetting to lock a screen, accidentally visiting a blocked site, failing to use VPN once.
Consequences: Verbal reminder, additional training, documented warning in HR file.

**Tier 2 — Moderate Violations:**
Examples: Installing unauthorized software, using personal cloud storage for work files, sharing a password with a colleague, repeated Tier 1 violations.
Consequences: Written warning, mandatory security awareness re-training, restricted system access pending review, formal documentation in personnel file.

**Tier 3 — Severe Violations:**
Examples: Intentionally accessing data outside job function, disabling security controls, sharing credentials externally, entering customer data into unauthorized AI tools.
Consequences: Suspension, termination, removal of all system access, potential legal action.

**Tier 4 — Criminal Violations:**
Examples: Data theft, sabotage, unauthorized sale of data, hacking.
Consequences: Immediate termination, referral to law enforcement, civil litigation.

### Due Process Requirements

Enforcement must follow a documented process. This is not just good practice — auditors check for it, and employment law requires it in many jurisdictions:

1. **Investigation.** Suspected violations are investigated by the security team in coordination with HR before any action is taken.
2. **Documentation.** The violation, the evidence, and the outcome are documented.
3. **Consistency.** Similar violations receive similar consequences. Inconsistent enforcement undermines the policy's credibility and creates legal exposure.
4. **Escalation path.** Employees have the right to contest findings and appeal disciplinary actions through a defined process.
5. **No retaliation.** Individuals who report violations in good faith are protected from retaliation.

### Audit Evidence for Enforcement

Auditors do not just check that the enforcement section exists. They may ask for evidence that the process has been followed. Be prepared to show:
- Records of policy violation investigations (anonymized)
- Evidence that violations resulted in documented consequences
- Training completion records after violations
- Consistency in enforcement outcomes

If your AUP describes a tiered consequences framework but you have never documented a single violation or consequence, the auditor may question whether the policy is actually enforced.

---

## Getting Employee Acknowledgment

An acceptable use policy that has not been acknowledged by every in-scope person is an incomplete control. This is one of the most straightforward audit checks — and one of the most common audit findings.

### What Auditors Expect

Every major framework requires evidence that policies have been communicated and acknowledged:

- **SOC 2 (CC1.4):** Employees are aware of and understand their security responsibilities.
- **ISO 27001 (Clause 7.3):** Persons doing work under the organization's control must be aware of the information security policy and their contribution to the ISMS.
- **HIPAA (164.308(a)(5)):** Security awareness and training, including periodic security reminders.
- **PCI DSS (Requirement 12.6):** All personnel must be aware of the importance of cardholder data security.

The auditor will request your acknowledgment records and compare them against your current employee and contractor roster. Every name on the roster must have a corresponding acknowledgment. Missing acknowledgments are immediate findings.

### Onboarding Acknowledgment

The AUP acknowledgment should be part of the Day 1 onboarding process, before system access is provisioned:

1. New hire receives the AUP as part of their onboarding package (either physical or electronic)
2. New hire reads the policy in full
3. New hire signs or electronically acknowledges the policy
4. Acknowledgment is recorded in the HR system or compliance platform with a timestamp
5. System access is provisioned after acknowledgment is confirmed

This sequence is critical. If an employee has system access before acknowledging the AUP, there is a gap in your control. Best practice: make AUP acknowledgment a prerequisite for account provisioning.

### Annual Re-Acknowledgment

A one-time acknowledgment during onboarding is not sufficient for most frameworks. Best practice — and what auditors expect — is annual re-acknowledgment:

- Push the AUP to all employees and contractors annually (typically aligned with the security awareness training cycle)
- Require electronic acknowledgment within a defined timeframe (14-30 days)
- Track completions and send reminders for non-responses
- Escalate persistent non-acknowledgments to management
- Maintain records of each acknowledgment cycle with timestamps

Annual re-acknowledgment serves a dual purpose: it ensures ongoing compliance, and it prompts employees to re-read the policy — which may have been updated with new provisions (e.g., AI tools, new remote work requirements).

### Tracking Acknowledgments at Scale

For companies with more than 50 employees, manual tracking (spreadsheets, paper forms) becomes unreliable. Compliance automation platforms like [QuickTrust](https://trust.quickintell.com) automate policy distribution, track acknowledgments in real time, send automated reminders, and generate audit-ready reports showing 100% acknowledgment coverage across the organization.

---

## AUP vs. Other Security Policies: How They Work Together

The acceptable use policy does not exist in isolation. It is one component of a layered security governance framework. Understanding how the AUP relates to other policies prevents overlap, gaps, and contradictions that auditors will flag.

### The Policy Hierarchy

| Policy | What It Governs | Relationship to AUP |
|--------|----------------|---------------------|
| **[Information Security Policy](/blog/information-security-policy-guide)** | Overall security program governance, management commitment, policy framework | The AUP derives its authority from the information security policy. The ISP should reference the AUP as a subordinate policy. |
| **Access Control Policy** | How access is granted, managed, reviewed, and revoked | The AUP defines what users may do with the access they have been granted. The access control policy defines who gets access and how. |
| **Data Classification Policy** | How data is categorized and what protections each category requires | The AUP references the classification scheme and defines user-level handling requirements for each category. |
| **[Incident Response Plan](/blog/incident-response-plan-compliance-guide)** | How security incidents are detected, reported, and resolved | The AUP defines what constitutes a user-caused incident and the obligation to report. The IRP defines what happens after reporting. |
| **Remote Work Policy** | Detailed requirements for working outside the office | The AUP covers remote work at the behavioral level. A separate remote work policy may provide more detailed technical requirements. |
| **Password Policy** | Password complexity, rotation, and management requirements | The AUP prohibits sharing credentials. The password policy defines what a compliant password looks like. |
| **[Vendor Risk Management Policy](/blog/vendor-risk-management-complete-guide)** | How third-party vendors are assessed and monitored | The AUP's cloud services section prevents shadow IT. The vendor risk management policy governs the formal vendor assessment process. |

### Avoiding Contradictions

The most common problem with multiple overlapping policies is contradiction. If your password policy requires 90-day rotation but your AUP does not mention rotation, an auditor may note the inconsistency. If your remote work policy permits personal device use but your AUP prohibits it, you have a conflict that undermines both documents.

To prevent contradictions:
- Designate a single policy owner responsible for cross-policy consistency
- Review all security policies simultaneously during the annual review cycle
- Use cross-references ("as defined in the Data Classification Policy") rather than restating requirements from other policies in the AUP
- Maintain a policy matrix mapping each control requirement to its governing policy

---

## Common AUP Mistakes That Fail Audits

After reviewing hundreds of acceptable use policies across SOC 2, ISO 27001, and HIPAA audits, the same mistakes appear consistently. Avoiding these is the difference between a clean audit and a findings report that delays your certification.

### Mistake 1: The Policy Has Not Been Updated in Over 12 Months

Every framework requires annual policy review at minimum. An AUP with a "Last Reviewed" date more than 12 months old is an automatic finding. Set a calendar reminder. Review the policy. Update the date. Even if no substantive changes are needed, the review itself must be documented.

### Mistake 2: No Coverage for Remote Work

An AUP that reads as though all employees work in a single office, circa 2019, will not satisfy auditors in 2026. If your organization has remote workers — and virtually all tech companies do — the AUP must address home network security, VPN requirements, physical security at home, and public WiFi restrictions.

### Mistake 3: No Coverage for AI Tools

This is the fastest-growing gap in 2026. Employees are using AI tools daily. If your AUP does not address which AI tools are approved and what data may be entered into them, you have an uncontrolled risk that auditors are now trained to identify.

### Mistake 4: Generic Language Copied from a Template

Auditors recognize templated language. When the AUP says "authorized tools" but there is no approved tools list, or references "the IT department" when the company has no IT department (the CTO handles everything), the policy loses credibility. Customize every section to reflect your actual organization.

### Mistake 5: No Acknowledgment Tracking

The policy exists. It is well-written. But there are no acknowledgment records. For half the workforce, there is no evidence they have ever read or agreed to the policy. This is one of the most common and most easily preventable findings.

### Mistake 6: Missing Monitoring Disclosure

The AUP does not include a clear statement that the company monitors system usage. Without this disclosure, the company's monitoring activities may lack legal standing, and the auditor cannot confirm that employees have been notified of monitoring.

### Mistake 7: No Enforcement Section or No Evidence of Enforcement

The AUP lists no consequences for violations. Or it lists consequences but the organization has never documented a single enforcement action, raising auditor questions about whether the policy is decorative rather than operational.

### Mistake 8: No BYOD Policy When BYOD Is Occurring

The AUP states that only company-issued devices may be used for work, but employees are clearly using personal phones to check email and access Slack. The policy does not match reality. Auditors test for this disconnect by comparing the AUP's device provisions against MDM enrollment records and access logs.

### Mistake 9: Scope Excludes Contractors

The AUP applies to "all employees" and does not mention contractors, temporary staff, or third parties. Yet contractors have system access. This scope gap means the AUP does not govern all users with access — which is exactly what auditors check.

### Mistake 10: No Version Control

The AUP has no version number, no change history, and no clear indication of when it was approved or by whom. Auditors need to verify that the policy is current, approved, and controlled. Without version metadata, they cannot.

---

## Frequently Asked Questions

### What is an acceptable use policy?

An acceptable use policy (AUP) is a formal document that defines the rules and guidelines for how employees, contractors, and other authorized users may use an organization's technology resources, including computers, networks, email, internet access, mobile devices, cloud services, and data. It establishes what behavior is permitted, what is prohibited, and what the consequences are for violations.

### Is an acceptable use policy legally binding?

An AUP is generally enforceable as a condition of employment or engagement when the user has acknowledged it in writing. It provides the legal basis for monitoring employee activity on company systems and for taking disciplinary action for violations. Its enforceability depends on jurisdiction, the clarity of its terms, and whether the employee was given adequate notice and opportunity to review it before acknowledgment.

### How often should an acceptable use policy be reviewed?

At minimum, the AUP should be reviewed annually. This is the standard expected by SOC 2, ISO 27001, HIPAA, and PCI DSS auditors. In practice, it should also be reviewed whenever there is a significant change in the technology environment (e.g., adoption of new AI tools, shift to remote work, introduction of BYOD), a change in regulatory requirements, or a security incident that reveals a gap in the current policy.

### What is the difference between an acceptable use policy and an information security policy?

The [information security policy](/blog/information-security-policy-guide) is the top-level governance document that defines the organization's overall commitment to information security, assigns security responsibilities, and establishes the framework under which all other security policies operate. The acceptable use policy is a subordinate document that focuses specifically on how users interact with technology resources. The information security policy governs the program. The AUP governs the people.

### Do contractors and third parties need to sign the AUP?

Yes. Every person with access to your organization's systems or data must acknowledge the acceptable use policy. This includes full-time employees, part-time employees, contractors, temporary staff, interns, consultants, and any third party with system access. Auditors compare your AUP acknowledgment records against your full access roster — not just your employee roster.

### What should an AUP say about generative AI tools?

The AUP should identify which AI tools are approved for business use, define what categories of data may be entered into those tools (typically nothing above Internal classification unless specifically approved), prohibit the use of unapproved AI platforms, require human review of AI-generated outputs, and address intellectual property considerations. This has become a standard audit check point in 2026.

### What happens if an employee violates the acceptable use policy?

The specific consequences depend on the severity, intent, and impact of the violation. A well-structured AUP defines a tiered consequences framework ranging from verbal warnings for minor, unintentional violations to termination and legal action for severe or criminal violations. The enforcement process should include investigation, documentation, consistency, and an appeal mechanism. Auditors expect to see evidence that the enforcement process is followed, not just that it exists on paper.

### Can a company monitor employees without an AUP?

Technically, in many US jurisdictions, employers have broad rights to monitor activity on company-owned systems. However, without an AUP that discloses monitoring and obtains consent, the organization faces increased legal risk, particularly in states with stricter privacy laws and in international jurisdictions subject to GDPR or similar regulations. From a compliance perspective, auditors expect the monitoring disclosure in the AUP. From a legal perspective, the AUP provides the cleanest basis for monitoring and for acting on what monitoring reveals.

---

## Build Your Acceptable Use Policy in Minutes, Not Weeks

Writing an acceptable use policy from scratch takes time. Making it audit-ready — with the right framework mappings, the right section coverage, proper version control, and automated acknowledgment tracking — takes even more.

QuickTrust generates a fully customized, audit-ready acceptable use policy tailored to your organization's size, industry, compliance requirements, and technology stack. It maps every section to the specific SOC 2, ISO 27001, HIPAA, and PCI DSS controls you need to satisfy. It distributes the policy to your team, tracks acknowledgments automatically, and alerts you when annual reviews are due.

No templates. No guesswork. No audit findings on Day 1.

**[Start building your AUP with QuickTrust](https://trust.quickintell.com)**
