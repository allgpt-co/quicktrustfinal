---
meta_description: "Everything SaaS companies need to know about Data Processing Agreements (DPAs) for GDPR compliance. Includes required clauses, templates, negotiation tips, and common mistakes to avoid."
target_keyword: "data processing agreement"
secondary_keywords: "DPA GDPR, data processing agreement template, data processing agreement requirements, what is a data processing agreement, GDPR data processor"
word_count_target: 4000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-19
---

# Data Processing Agreement (DPA): What Every SaaS Company Must Include for GDPR and Global Privacy Compliance

You are three weeks from closing a six-figure European enterprise deal. The technical evaluation is done. The champion on the buyer's side has signed off. Procurement has approved the pricing. Then the buyer's Data Protection Officer sends a single email: "Please provide your Data Processing Agreement for review."

Your company does not have one. Or you have a two-page document your co-founder copied from a competitor's website in 2022 that references "Privacy Shield" -- a transfer mechanism the Court of Justice of the European Union invalidated in July 2020. Or your DPA exists but omits half the clauses required by GDPR Article 28(3), and the buyer's legal team sends back a redline with 47 comments.

The deal stalls. It stalls for weeks, sometimes months, sometimes permanently. And the frustrating part is that the DPA requirement is not ambiguous -- it is one of the most clearly defined obligations in the entire regulation. GDPR Article 28 spells out, clause by clause, what a Data Processing Agreement must contain. The companies that lose deals over DPAs are not facing an unreasonable demand. They are facing a standard, well-documented legal requirement they failed to prepare for.

This guide covers everything a SaaS company needs to know about Data Processing Agreements: what they are, when you need one, exactly what clauses GDPR requires, how to negotiate common sticking points, and how to build a DPA that accelerates enterprise deals instead of blocking them.

---

## What Is a Data Processing Agreement?

A Data Processing Agreement (DPA) is a legally binding contract between a data controller and a data processor that governs the processing of personal data. Under GDPR, a DPA is not optional -- it is a statutory requirement. Article 28(3) of the GDPR mandates that "processing by a processor shall be governed by a contract or other legal act under Union or Member State law, that is binding on the processor with regard to the controller."

In plain language: any time one organization processes personal data on behalf of another organization, there must be a written contract defining how that data will be handled, protected, and eventually returned or deleted.

**The legal basis is GDPR Article 28.** This article does not merely suggest that controllers and processors enter into agreements -- it requires it. And it does not leave the contents to negotiation. Article 28(3) lists specific provisions that the contract "shall stipulate." A DPA that omits required provisions does not satisfy the legal obligation, even if both parties signed it willingly.

**Why this matters commercially:** European enterprise buyers know the DPA requirement exists. Their procurement teams, legal departments, and Data Protection Officers evaluate vendor DPAs as part of standard due diligence. A well-drafted DPA signals that your company understands its obligations and can be trusted with personal data. A missing or inadequate DPA signals the opposite -- and in competitive sales cycles, that signal loses deals.

**Key distinction:** A DPA is not a privacy policy. A privacy policy is a public-facing document that tells individuals how you handle their personal data. A DPA is a B2B contract between two organizations that governs data processing activities performed by one party on behalf of the other. Most SaaS companies need both.

---

## Controller vs Processor vs Sub-Processor: Understanding Your Role

Before you can draft or negotiate a DPA, you need to understand which role you occupy. GDPR defines three distinct roles in data processing, and your obligations differ depending on which role applies.

### Data Controller

The data controller determines the purposes and means of processing personal data. The controller decides why data is collected and how it will be used. In B2B SaaS, your customer is typically the controller -- they decide to use your software to process their employees', customers', or users' personal data.

**Example:** A European e-commerce company uses your CRM platform to manage customer relationships. The e-commerce company is the controller -- they decided to collect customer data, they determined the purpose (managing customer relationships), and they chose the means (your CRM platform).

### Data Processor

The data processor processes personal data on behalf of and under the instructions of the controller. The processor does not decide why data is collected -- they execute the controller's instructions. Most B2B SaaS companies operate as data processors.

**Example:** Your CRM platform stores, organizes, and enables your customer to interact with their customer data. You are processing that data on behalf of and under the instructions of your customer. You are the data processor.

### Sub-Processor

A sub-processor is a third party engaged by the data processor to carry out specific processing activities on behalf of the controller. If your SaaS platform uses third-party services that access or process your customers' personal data, those third parties are sub-processors.

**Example:** Your CRM platform uses AWS for cloud hosting, Twilio for sending transactional emails, and Segment for analytics. Each of these services processes personal data that originated from your customer (the controller), routed through you (the processor). AWS, Twilio, and Segment are sub-processors. Under GDPR Article 28(2) and 28(4), you need DPAs with each of them, and those DPAs must impose data protection obligations no less stringent than the ones in your DPA with the controller.

### Why Role Classification Matters

Your role determines your obligations:

| | Controller | Processor | Sub-Processor |
|---|---|---|---|
| **Determines purposes of processing** | Yes | No | No |
| **Determines means of processing** | Yes | Partially (technical means) | No |
| **Requires DPA with the other party** | Must ensure DPA is in place | Must have DPA with controller | Must have DPA with processor |
| **Responds to data subject requests** | Primary obligation | Assists controller | Assists processor |
| **Reports breaches to DPA (authority)** | Yes (within 72 hours) | Reports to controller | Reports to processor |
| **Maintains Records of Processing** | Yes (Article 30(1)) | Yes (Article 30(2)) | Yes (Article 30(2)) |

**Common misclassification:** Some SaaS companies assume they are controllers because they "control" the software. This is incorrect. Controller status is about controlling the purposes of data processing -- not the software platform. If your customer decides what data to input, why to input it, and how to use the outputs, they are the controller and you are the processor, regardless of who owns the software.

**Joint controllership:** In some cases, two parties jointly determine the purposes and means of processing. GDPR Article 26 requires joint controllers to enter into an arrangement defining their respective responsibilities. This is less common in standard B2B SaaS but can arise in data sharing partnerships, co-marketing arrangements, or platform integrations where both parties independently benefit from the processing.

---

## When Do You Need a DPA?

The short answer: whenever personal data is processed by one party on behalf of another. The practical triggers for SaaS companies fall into three categories.

### 1. Selling to EU Customers

If your customers are established in the EU or EEA, they are subject to GDPR and are required to have DPAs with their data processors. They will ask for your DPA during procurement. Not having one is a deal-breaker -- not because the buyer is being difficult, but because they would be violating GDPR Article 28 if they engaged you without one.

### 2. Processing EU Resident Data

Even if your customer is a US company, if their users, employees, or customers include EU residents whose personal data flows through your platform, GDPR applies. The regulation follows the data subject, not the company. A US-based customer with a European sales team using your HR platform triggers GDPR obligations for the personal data of those European employees.

### 3. Using EU-Based Vendors or Sub-Processors

If you use vendors established in the EU to process personal data, the GDPR framework applies to that relationship. You need DPAs with your EU-based sub-processors, and those sub-processors need to comply with the processing instructions you pass through from your controllers.

### 4. Non-GDPR Jurisdictions Adopting Similar Requirements

The DPA requirement is not unique to GDPR. The UK GDPR (post-Brexit) requires equivalent agreements. Brazil's LGPD, South Africa's POPIA, and Thailand's PDPA all include processor agreement requirements. Even within the United States, the CCPA/CPRA requires "service provider" agreements that function similarly to DPAs for California resident data. Building a strong DPA now covers you across multiple jurisdictions.

**Practical rule:** If you are a B2B SaaS company with customers in any regulated market, you need a DPA. The cost of having one and not needing it in a specific deal is zero. The cost of needing one and not having it is a lost deal plus the time to create one under deadline pressure.

---

## The 12 Required Clauses in a GDPR-Compliant DPA

GDPR Article 28(3) is unusually prescriptive. It lists specific provisions that the processing contract must include. This is not a framework to interpret -- it is a checklist. A DPA that omits any of these elements does not satisfy the legal requirement.

### Clause 1: Subject Matter and Duration of Processing

The DPA must define what the processing arrangement covers and how long it lasts. This is typically tied to the underlying service agreement.

**What to include:** A clear statement that the DPA governs the processing of personal data by the processor in connection with the services described in the Master Services Agreement (or equivalent). The duration should match the term of the services agreement, plus any post-termination period required for data return or deletion.

**Example language:** "This DPA governs Processor's processing of Personal Data in connection with the Services provided under the Master Services Agreement dated [date] between Controller and Processor. The duration of processing shall be the term of the Services Agreement plus [30/60/90] days for data return and deletion."

### Clause 2: Nature and Purpose of Processing

Specify what processing activities the processor will perform and why.

**What to include:** A description of the processing operations -- storage, retrieval, organization, analysis, transmission -- and the business purpose. For a SaaS platform, this is typically "providing the contracted SaaS service as described in the Services Agreement."

**Avoid:** Vague language like "any processing reasonably necessary." Auditors and Data Protection Authorities expect specificity. If your platform stores data, processes analytics, sends notifications, and generates reports, say so.

### Clause 3: Types of Personal Data

Enumerate the categories of personal data that will be processed.

**What to include:** A list of the data types your platform handles. Common categories for B2B SaaS include: contact information (name, email, phone), account credentials, usage data, IP addresses, device identifiers, and any customer-specific data types the platform stores.

**Why this matters:** The categories of personal data determine the risk profile of the processing. A DPA covering only contact information has a different risk profile than one covering financial data or health information. Data Protection Authorities evaluate whether the security measures in the DPA are proportionate to the data types being processed.

### Clause 4: Categories of Data Subjects

Identify whose personal data is being processed.

**What to include:** Typically "employees, contractors, customers, and end users of the Controller" for B2B SaaS. Be specific enough to accurately describe the data subjects but broad enough to cover legitimate use cases.

### Clause 5: Controller's Obligations and Rights

Define what the controller is responsible for and what rights they retain.

**What to include:** The controller's obligation to ensure a lawful basis for processing, the controller's right to issue documented processing instructions, the controller's responsibility for responding to data subject requests (with processor assistance), and the controller's right to audit the processor's compliance.

### Clause 6: Processor Must Act Only on Documented Instructions

This is a core GDPR requirement. Article 28(3)(a) requires that the processor "processes the personal data only on documented instructions from the controller, including with regard to transfers of personal data to a third country."

**What to include:** A clear commitment that the processor will process personal data only in accordance with the controller's documented instructions. The DPA itself and the services agreement constitute the primary instructions. Any processing outside the scope of documented instructions requires prior written authorization from the controller.

**Exception:** The processor must inform the controller if, in its opinion, an instruction infringes GDPR or other data protection law. The processor is not required to blindly follow unlawful instructions.

### Clause 7: Confidentiality Obligations

Article 28(3)(b) requires the processor to ensure that persons authorized to process personal data "have committed themselves to confidentiality or are under an appropriate statutory obligation of confidentiality."

**What to include:** A commitment that all personnel with access to personal data are bound by confidentiality obligations -- either through employment contracts, NDAs, or statutory obligations. This extends to sub-processor personnel.

### Clause 8: Security Measures

Article 28(3)(c) cross-references Article 32, which requires "appropriate technical and organisational measures to ensure a level of security appropriate to the risk."

**What to include:** Specific security measures the processor implements: encryption at rest and in transit, access controls, multi-factor authentication, logging and monitoring, vulnerability management, penetration testing, and incident response procedures. Many DPAs include a Security Annex that details these measures.

**Best practice:** Reference your SOC 2 report or ISO 27001 certification as evidence of your security posture. European enterprise buyers increasingly accept SOC 2 Type II reports and ISO 27001 certificates as evidence of Article 32 compliance, which reduces the back-and-forth during DPA negotiation.

### Clause 9: Sub-Processor Requirements

Article 28(2) and 28(4) govern sub-processors. The processor must not engage another processor without prior authorization from the controller. Two authorization models are permitted:

**Specific prior authorization:** The processor must obtain the controller's written consent before engaging each sub-processor. This gives the controller maximum oversight but is operationally burdensome for SaaS companies that regularly add or change infrastructure providers.

**General written authorization:** The processor maintains a list of authorized sub-processors and notifies the controller of any changes. The controller has a defined objection period (typically 30 days) during which they can object to a new sub-processor. If the objection cannot be resolved, the controller can terminate the DPA. This is the model most SaaS companies use.

**What to include:** The authorization model you are using, a current sub-processor list (typically as an annex or at a URL), the notification mechanism for changes, the objection procedure, and a commitment that sub-processor agreements impose data protection obligations no less protective than those in the DPA.

### Clause 10: Data Breach Notification

Article 28(3)(f) requires the processor to assist the controller in complying with its breach notification obligations under Articles 33 and 34.

**What to include:** A commitment to notify the controller of a personal data breach without undue delay after becoming aware of it. GDPR does not specify a timeframe for processor-to-controller notification, but most DPAs set one contractually -- commonly 24 to 72 hours. The notification should include: the nature of the breach, categories and approximate number of data subjects affected, categories and approximate number of personal data records affected, likely consequences, and measures taken or proposed to address the breach.

**Why the timeframe matters:** Controllers must notify their Data Protection Authority within 72 hours of becoming aware of a breach (Article 33). The controller's clock starts when they learn of the breach -- which means your notification to them must be fast enough to allow them to investigate and file their own notification within the 72-hour window.

### Clause 11: Data Deletion or Return

Article 28(3)(g) requires the processor to "delete or return all the personal data to the controller after the end of the provision of services relating to processing, and delete existing copies unless Union or Member State law requires storage of the personal data."

**What to include:** The controller's choice between data return (in a standard, machine-readable format) and data deletion. A defined timeframe for completing return or deletion after contract termination. Certification of deletion upon completion. Any exceptions where retention is required by law (e.g., financial records for tax purposes).

### Clause 12: Audit Rights

Article 28(3)(h) requires the processor to "make available to the controller all information necessary to demonstrate compliance with the obligations laid down in this Article and allow for and contribute to audits, including inspections, conducted by the controller or another auditor mandated by the controller."

**What to include:** The controller's right to audit the processor's compliance with the DPA. Practical limitations are acceptable -- most DPAs limit audits to once per year, require reasonable advance notice (30 days), limit audits to business hours, and allow the processor to use third-party audit reports (SOC 2, ISO 27001) to satisfy audit requests.

**Negotiation note:** Most SaaS companies resist unlimited on-site audit rights because of operational disruption and the risk of exposing other customers' confidential information. A reasonable middle ground: the processor provides its most recent SOC 2 Type II report or ISO 27001 certificate. If the report does not address the controller's concerns, the controller may request an on-site audit with reasonable notice and scope limitations.

---

## Standard Contractual Clauses (SCCs): When You Need Them for International Transfers

A DPA governs the relationship between controller and processor. Standard Contractual Clauses (SCCs) address a different problem: the lawful transfer of personal data from the EU/EEA to a country without an adequate level of data protection -- which includes the United States.

### When SCCs Are Required

If personal data originating from EU/EEA data subjects is transferred to a country that does not have an EU adequacy decision, you need a lawful transfer mechanism. For most US SaaS companies, this means SCCs.

The European Commission published updated SCCs in June 2021 (Commission Implementing Decision 2021/914), replacing the older 2001/2010 versions. The new SCCs are modular and cover four transfer scenarios:

| Module | Transfer Scenario | Typical SaaS Application |
|---|---|---|
| **Module 1** | Controller to Controller | Rare in SaaS; used in data sharing partnerships |
| **Module 2** | Controller to Processor | Most common for SaaS -- EU customer (controller) transfers data to US SaaS vendor (processor) |
| **Module 3** | Processor to Processor | Used when a US SaaS vendor transfers data to a US sub-processor on behalf of an EU controller |
| **Module 4** | Processor to Controller | Rare; used when a processor returns data to a controller in a non-adequate country |

### The EU-US Data Privacy Framework

In July 2023, the European Commission adopted an adequacy decision for the EU-US Data Privacy Framework (DPF), providing a lawful basis for transfers to US organizations that have self-certified under the DPF. If your company has certified under the DPF, you can rely on it for EU-US transfers without SCCs.

However, many European enterprise buyers still require SCCs as a belt-and-suspenders approach, given the history of invalidated transfer mechanisms (Safe Harbor in 2015, Privacy Shield in 2020). Including SCCs in your DPA -- even if you also rely on the DPF -- demonstrates thoroughness and future-proofs the arrangement.

### Transfer Impact Assessments

Since the Schrems II decision (CJEU Case C-311/18, July 2020), SCCs alone are not automatically sufficient. Both parties must assess whether the laws and practices of the data-importing country provide adequate protection. For US transfers, this assessment should address US surveillance laws (FISA Section 702, Executive Order 12333) and the protections provided by Executive Order 14086 (October 2022), which established the Data Protection Review Court. Document this assessment as an annex to your DPA.

---

## Sub-Processor Management: Obligations and Notification Requirements

Sub-processor management is one of the most operationally demanding aspects of DPA compliance. GDPR Article 28(2) requires the processor to obtain authorization before engaging sub-processors, and Article 28(4) requires that sub-processor contracts impose the same data protection obligations.

### Building Your Sub-Processor List

Maintain a comprehensive, current list of all sub-processors that process personal data on behalf of your controllers. For each sub-processor, document:

- Company name and registered address
- Country where processing occurs
- Description of the processing activity
- Categories of personal data processed
- Whether SCCs or another transfer mechanism are in place (for non-adequate countries)

**Common sub-processors for SaaS companies:** Cloud infrastructure (AWS, GCP, Azure), email delivery (SendGrid, Mailgun, Twilio), analytics (Segment, Mixpanel, Amplitude), customer support (Zendesk, Intercom), payment processing (Stripe, Adyen), error monitoring (Sentry, Datadog).

### Notification Process

Most DPAs use the general authorization model with a notification and objection mechanism:

1. Processor publishes a sub-processor list on a publicly accessible URL
2. Processor notifies the controller (typically by email) at least 30 days before engaging a new sub-processor
3. Controller has a defined objection period (usually 30 days) to raise concerns
4. If the controller objects, the processor must work to address the concern -- this may involve not using the sub-processor for that controller's data, implementing additional safeguards, or offering the controller the option to terminate
5. If the objection cannot be resolved, the controller may terminate the DPA and the associated services agreement

### Due Diligence on Sub-Processors

You are not absolved of responsibility by flowing down contractual obligations to sub-processors. GDPR Article 28(4) states that if a sub-processor fails to fulfill its data protection obligations, the initial processor "shall remain fully liable to the controller for the performance of that other processor's obligations." Conduct due diligence: review sub-processor security certifications, DPA terms, breach history, and data handling practices.

---

## DPA Negotiation: Common Sticking Points and How to Resolve Them

DPA negotiations between SaaS vendors and enterprise buyers follow predictable patterns. Understanding the common sticking points -- and having reasonable positions prepared -- accelerates deals.

### 1. Data Breach Notification Timeframe

**Buyer's position:** Notify within 24 hours of discovery.
**Vendor's position:** Notify "without undue delay" per GDPR language.
**Resolution:** 48-72 hours for initial notification of a confirmed personal data breach affecting the controller's data, with a follow-up detailed report within 5 business days. Distinguish between a "security incident" (broad) and a "personal data breach" (specific) -- notification obligations should attach to the latter.

### 2. Audit Rights Scope

**Buyer's position:** On-site audit rights with full access, at any time.
**Vendor's position:** No on-site audits; SOC 2 report suffices.
**Resolution:** Processor provides its most recent SOC 2 Type II report or ISO 27001 certificate. If the report does not address specific concerns, the controller may conduct one audit per year with 30 days' advance notice, during business hours, limited in scope to DPA compliance, and subject to confidentiality obligations. The controller bears the cost of the audit unless it reveals material non-compliance.

### 3. Sub-Processor Approval

**Buyer's position:** Specific prior written approval for each sub-processor.
**Vendor's position:** General authorization with notification.
**Resolution:** General authorization with the controller receiving at least 30 days' advance notice of new sub-processors and a meaningful objection right. Provide the current sub-processor list as part of the DPA so the controller has approved the existing set at the time of signing.

### 4. Liability and Indemnification

**Buyer's position:** Unlimited liability for data breaches; processor indemnifies controller for all regulatory fines.
**Vendor's position:** Liability capped at 12 months of fees.
**Resolution:** Tiered liability structure. Standard commercial liability cap for general DPA obligations. A higher cap (24 months of fees, or a defined multiple) for data breaches caused by processor's willful misconduct or material non-compliance. Indemnification for regulatory fines that directly result from processor's breach of the DPA, subject to the higher cap. Note: indemnification for GDPR fines is contentious -- many jurisdictions do not permit insuring against or indemnifying regulatory penalties.

### 5. Data Localization

**Buyer's position:** All data must remain within the EU/EEA.
**Vendor's position:** Data stored in the US or multiple regions.
**Resolution:** Offer EU-region hosting as an option (many cloud providers support EU-only data residency). If US processing is unavoidable, ensure SCCs and a Transfer Impact Assessment are in place. Some vendors offer a price premium for EU-only processing, which is a commercially reasonable approach.

### 6. Return Format and Deletion Certification

**Buyer's position:** Data returned in specific format with certified deletion of all copies within 7 days.
**Vendor's position:** Data available for self-service export; deletion within 90 days.
**Resolution:** Data return in a standard, machine-readable format (JSON, CSV, or via API) within 30 days of request. Deletion of all copies (including backups) within 90 days. Written certification of deletion upon completion. Exception for data retained under legal obligation, with those retention requirements documented.

---

## DPA vs BAA: Key Differences for Companies Subject to Both GDPR and HIPAA

SaaS companies selling into healthcare face a dual obligation: GDPR DPAs for European data and HIPAA Business Associate Agreements (BAAs) for protected health information. While both are processor-controller agreements, they differ in important ways.

| Dimension | GDPR DPA | HIPAA BAA |
|---|---|---|
| **Legal basis** | GDPR Article 28 | 45 CFR 164.504(e), 164.314(a) |
| **Scope** | All personal data of EU/EEA residents | Protected Health Information (PHI) only |
| **Breach notification (to partner)** | "Without undue delay" (typically 48-72 hours contractually) | Within 60 days (regulatory), often 24-72 hours (contractual) |
| **Breach notification (to authority)** | Controller notifies DPA within 72 hours | Covered Entity notifies HHS within 60 days |
| **Sub-processor obligations** | Prior authorization required (specific or general) | BAA required with each subcontractor handling PHI |
| **Data subject rights** | Eight rights (access, erasure, portability, etc.) | Access and amendment rights under HIPAA Privacy Rule |
| **International transfers** | Requires transfer mechanism (SCCs, adequacy, DPF) | No specific international transfer mechanism |
| **Audit rights** | Explicit requirement in Article 28(3)(h) | Implied; covered entity may audit |
| **Regulatory enforcement** | Data Protection Authorities; fines up to 4% global turnover | HHS Office for Civil Rights; fines up to $2.13M per violation category |

**For companies subject to both:** You can create a unified agreement that addresses both GDPR and HIPAA requirements, or maintain separate DPA and BAA documents. The unified approach is simpler but requires careful drafting to avoid conflicts -- for example, GDPR's "right to erasure" may conflict with HIPAA's retention requirements for PHI. The separate-document approach is cleaner legally but creates a heavier contract package.

[See our complete [Business Associate Agreement (BAA) guide](/blog/business-associate-agreement-guide) for a section-by-section breakdown of HIPAA requirements.]

---

## Data Processing Agreement Template: Section-by-Section Guide

A well-structured DPA typically contains the following sections. This is not legal advice -- it is an operational guide to help you understand what belongs in each section and why.

### Section 1: Definitions

Define all key terms: Personal Data, Processing, Controller, Processor, Sub-Processor, Data Subject, Personal Data Breach, Data Protection Authority, GDPR, Applicable Data Protection Law. Reference the GDPR definitions (Article 4) rather than creating your own -- this ensures consistency and avoids ambiguity.

### Section 2: Scope and Applicability

State that the DPA applies to the processing of personal data by the processor in connection with the services agreement. Specify which services involve personal data processing. Confirm that in the event of a conflict between the DPA and the services agreement, the DPA prevails for data protection matters.

### Section 3: Roles and Responsibilities

Confirm the controller-processor relationship. State that the controller determines the purposes and means of processing, and the processor processes personal data only on the controller's documented instructions.

### Section 4: Processing Instructions

Define the scope of documented processing instructions. The DPA and services agreement constitute the primary instructions. Additional instructions must be provided in writing. The processor must inform the controller if an instruction infringes data protection law.

### Section 5: Confidentiality

Require all processor personnel with access to personal data to be bound by confidentiality obligations. This extends to sub-processor personnel.

### Section 6: Security Measures

Reference Article 32 of the GDPR. Include a Security Annex detailing specific technical and organizational measures: encryption standards, access control mechanisms, monitoring and logging, vulnerability management, incident response, physical security, personnel security.

### Section 7: Sub-Processor Management

Specify the authorization model (specific or general). Include the current sub-processor list. Define the notification and objection procedure for new sub-processors. Require flow-down of equivalent data protection obligations.

### Section 8: International Transfers

Address the lawful basis for any transfers outside the EU/EEA. Attach SCCs as an annex if applicable. Reference the EU-US Data Privacy Framework if the processor is certified. Include a Transfer Impact Assessment or reference to one.

### Section 9: Data Subject Rights

Commit the processor to assist the controller in fulfilling data subject rights requests. Define the mechanism for cooperation (e.g., the processor provides a self-service data export tool, or responds to controller requests within a defined timeframe).

### Section 10: Breach Notification

Define the notification timeframe, required content, and cooperation obligations. Distinguish between security incidents and personal data breaches.

### Section 11: Audits and Compliance Demonstrations

Establish the controller's audit rights. Define practical limitations (frequency, notice, scope, cost allocation). Specify what compliance evidence the processor will make available (SOC 2 reports, ISO 27001 certificates, penetration test summaries).

### Section 12: Data Return and Deletion

Define the controller's options upon termination: data return in a specified format, data deletion with certification, and the timeframe for each. Note any exceptions for legally required retention.

### Section 13: Liability

Define the liability framework for data protection breaches. Address indemnification for regulatory fines if applicable. Cross-reference the liability provisions of the main services agreement.

### Annex A: Details of Processing

A table or structured description covering: subject matter and duration of processing, nature and purpose, types of personal data, categories of data subjects.

### Annex B: Technical and Organizational Measures

Detailed description of security measures implemented by the processor.

### Annex C: Sub-Processor List

Current list of sub-processors with entity name, location, processing activity, and transfer mechanism.

### Annex D: Standard Contractual Clauses (if applicable)

The applicable SCC modules, fully executed.

---

## Beyond GDPR: DPA Requirements Under CCPA, UK GDPR, and Other Privacy Laws

GDPR established the template, but data processing agreements are now required -- or strongly advisable -- under privacy laws worldwide.

### UK GDPR

After Brexit, the UK adopted the UK GDPR (Data Protection Act 2018, as amended), which mirrors EU GDPR requirements for processing agreements. If you process personal data of UK residents, you need a DPA that complies with UK GDPR Article 28 -- which is substantively identical to EU GDPR Article 28. Most companies address this by extending the scope of their GDPR DPA to cover UK data, with a reference to the UK International Data Transfer Agreement (IDTA) or the UK Addendum to the EU SCCs for international transfers.

### California Consumer Privacy Act / California Privacy Rights Act (CCPA/CPRA)

The CCPA/CPRA does not use the term "Data Processing Agreement," but it requires equivalent contracts. When a business shares personal information with a "service provider" or "contractor," the CCPA requires a written contract that:

- Specifies the business purpose for which personal information is disclosed
- Prohibits the service provider from retaining, using, or disclosing the information for any purpose other than performing the specified services
- Prohibits selling or sharing the personal information
- Requires the service provider to comply with applicable CCPA obligations
- Grants the business the right to take reasonable steps to ensure compliance

**Practical approach:** Include a CCPA/CPRA addendum in your DPA or draft your DPA to cover both GDPR and CCPA requirements simultaneously. The obligations are largely compatible -- GDPR's requirements are generally more stringent, so a GDPR-compliant DPA typically satisfies CCPA requirements with minor additions.

### Brazil's LGPD

Brazil's Lei Geral de Protecao de Dados (LGPD) requires contracts between controllers and processors (called "operators" under LGPD) that define processing activities and security measures. The LGPD's processor agreement requirements are less prescriptive than GDPR Article 28 but follow the same pattern.

### Other Jurisdictions

South Africa's POPIA, Thailand's PDPA, Singapore's PDPA, Japan's APPI, and South Korea's PIPA all include some form of processor agreement requirement. The trend is clear: data processing agreements are becoming a global standard, not a European anomaly.

**Strategic implication:** Building a comprehensive GDPR DPA now -- rather than a minimum-viable document -- creates a template that can be adapted for multiple jurisdictions. The marginal cost of adding a CCPA addendum or UK GDPR references to a well-drafted GDPR DPA is minimal compared to building separate agreements for each jurisdiction.

[For a detailed breakdown of GDPR compliance requirements for US SaaS companies, see our [GDPR Compliance Guide](/blog/gdpr-compliance-us-saas-guide).]

---

## Common DPA Mistakes That Stall Enterprise Deals

After reviewing hundreds of DPAs across SaaS vendor procurement processes, these are the mistakes that most frequently delay or kill deals.

### Mistake 1: Not Having a DPA at All

Surprisingly common, especially among US SaaS companies expanding into Europe for the first time. When a European buyer asks for your DPA and you do not have one, it signals that your company has not thought about data protection -- which makes the buyer question everything else about your security posture.

**Fix:** Have a DPA ready before your first European sales conversation. It should be a standard document available on your website or provided immediately upon request.

### Mistake 2: Using a Pre-2021 Template

DPAs that reference Privacy Shield (invalidated July 2020), the old SCCs (replaced June 2021), or pre-Schrems II transfer mechanisms are immediately flagged by competent legal teams. They signal that your data protection program has not been maintained.

**Fix:** Ensure your DPA references the 2021 SCCs, the EU-US Data Privacy Framework (if you are certified), and current legal authorities.

### Mistake 3: Omitting Required Article 28(3) Clauses

Some DPAs read like abbreviated privacy policies rather than Article 28-compliant contracts. Missing sub-processor provisions, audit rights, or breach notification obligations means the DPA does not satisfy the legal requirement -- even if both parties sign it.

**Fix:** Use Article 28(3) as a literal checklist. Every sub-clause should have a corresponding provision in your DPA.

### Mistake 4: Vague Security Measures

"We implement industry-standard security measures" is not sufficient. European enterprise buyers and their DPOs want to see specific measures: encryption algorithms, access control mechanisms, monitoring practices, incident response timelines.

**Fix:** Include a detailed Security Annex. Reference your SOC 2 Type II report or ISO 27001 certificate. Specificity builds confidence.

### Mistake 5: No Sub-Processor List

Enterprise buyers need to know who else will process their data. A DPA that says "Processor may engage sub-processors" without providing a list or a notification mechanism does not comply with Article 28(2).

**Fix:** Maintain a current sub-processor list as an annex to your DPA or at a public URL. Include a notification and objection mechanism for changes.

### Mistake 6: Unreasonable Positions That Invite Negotiation

DPAs with clearly one-sided terms -- unlimited audit rights, 1-hour breach notification, unlimited liability -- invite redline battles. Conversely, DPAs that disclaim all processor obligations invite the buyer's legal team to insert them.

**Fix:** Start with reasonable, market-standard positions. A well-balanced DPA reduces negotiation cycles from weeks to days.

### Mistake 7: Not Addressing International Transfers

If you are a US company processing EU data, your DPA must address the legal basis for the international transfer. A DPA that ignores this topic entirely raises a fundamental compliance question that will stall procurement.

**Fix:** Include SCCs (typically Module 2 for controller-to-processor transfers) as an annex to your DPA, or reference your EU-US Data Privacy Framework certification.

### Mistake 8: Treating the DPA as a One-Time Document

Data protection laws evolve. Sub-processor lists change. Security measures improve. A DPA drafted in 2023 and never updated will contain outdated references and potentially non-compliant provisions by 2026.

**Fix:** Review and update your DPA template annually. Track regulatory changes that affect DPA requirements. Update your sub-processor list whenever you add or remove a vendor that processes customer personal data.

---

## Frequently Asked Questions

**Q: Is a DPA the same as a privacy policy?**

No. A privacy policy is a public-facing document that informs individuals (data subjects) about how their personal data is collected and used. A DPA is a business-to-business contract between a data controller and a data processor that governs data processing activities. Most organizations need both, but they serve different audiences and different legal purposes.

**Q: Can we use the European Commission's Standard Contractual Clauses as our DPA?**

The SCCs address international data transfers, not the full scope of Article 28 requirements. However, Module 2 of the 2021 SCCs (controller to processor) includes provisions that overlap with DPA requirements. Some companies use the SCCs as the core of their DPA and supplement them with additional clauses for areas the SCCs do not fully cover (such as detailed security measures, sub-processor lists, and liability provisions). This approach is legally sound but can be harder to navigate during negotiation because the SCC text cannot be modified.

**Q: Our SaaS product does not store customer data -- we just process it in real time. Do we still need a DPA?**

If you process personal data in any form -- including real-time processing without persistent storage -- you are a data processor and a DPA is required. "Processing" under GDPR Article 4(2) includes "collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination or otherwise making available, alignment or combination, restriction, erasure or destruction." Real-time processing without storage still constitutes processing.

**Q: How long does it typically take to negotiate a DPA with an enterprise buyer?**

With a well-drafted, market-standard DPA, negotiation typically takes 1-3 weeks. With a poorly drafted or missing DPA, it can take 2-3 months, because the buyer's legal team must essentially draft the DPA for you through redlines. The most efficient approach: have your DPA reviewed by privacy counsel before you enter sales conversations, and provide it proactively during procurement.

**Q: What happens if we process personal data without a DPA in place?**

Both the controller and processor are in violation of GDPR Article 28. The controller has failed to ensure a lawful processing arrangement; the processor is processing without a contractual basis. Both can face enforcement action and fines. In practice, the controller is more likely to face scrutiny (since ensuring DPAs are in place is their obligation), but processors are not immune -- Data Protection Authorities have issued fines to processors for non-compliance.

**Q: Do we need a separate DPA for each customer, or can we use a standard template?**

You can -- and should -- use a standard DPA template. Most SaaS companies publish a standard DPA that all customers execute. The template contains fixed terms (security measures, breach notification, audit rights), with customer-specific details (services description, data types, sub-processor list) either in the annexes or incorporated by reference from the services agreement. Enterprise customers may negotiate modifications, but starting from a strong standard template significantly reduces negotiation overhead.

**Q: Our customer wants to be listed as both controller and processor in the DPA. Is that correct?**

It depends on the processing activities. In some arrangements, the customer is the controller for certain data (e.g., their end users' data processed through your platform) and a processor for other data (e.g., data they process on behalf of their own customers). In these cases, the DPA should clearly delineate which processing activities fall under each role. This is common in platform and marketplace businesses where data flows through multiple layers.

**Q: How does a DPA interact with our Terms of Service?**

The DPA supplements your Terms of Service (or Master Services Agreement) with data-protection-specific obligations. Typically, the DPA includes a clause stating that in the event of a conflict between the DPA and the services agreement, the DPA prevails for data protection matters. This ensures that data protection obligations are not inadvertently weakened by general commercial terms.

---

## Manage Your DPAs as Part of a Complete Compliance Program

A Data Processing Agreement is one piece of a larger compliance infrastructure. The DPA documents your data protection obligations, but fulfilling those obligations requires technical controls, organizational processes, and ongoing monitoring.

QuickTrust helps SaaS companies build and maintain the compliance programs that make DPA commitments real:

- **DPA template development:** Attorney-reviewed, GDPR Article 28-compliant DPA templates tailored to your SaaS business model, with SCCs pre-integrated for international transfers
- **Sub-processor management:** Automated tracking of your vendor ecosystem, DPA status with each sub-processor, and notification workflows for sub-processor changes
- **Security controls implementation:** The technical and organizational measures referenced in your DPA Security Annex -- encryption, access controls, monitoring, incident response -- implemented and evidenced in your infrastructure
- **Audit readiness:** SOC 2 Type II and ISO 27001 certification programs that satisfy the audit clauses in your DPA, reducing negotiation friction with enterprise buyers
- **Privacy program management:** ROPA, data mapping, data subject rights workflows, consent management, and breach notification procedures -- the operational backbone of GDPR compliance
- **Multi-framework mapping:** Controls implemented once, mapped to GDPR, SOC 2, ISO 27001, HIPAA, and CCPA simultaneously -- because the security measures in your DPA are the same controls your auditors evaluate

The companies that close European enterprise deals fastest are not the ones with the best lawyers. They are the ones with DPAs backed by real compliance programs -- programs where every commitment in the contract has a corresponding control, evidence artifact, and monitoring process behind it.

**[Start your compliance assessment at trust.quickintell.com](https://trust.quickintell.com)**

---

*Related reading:*
- *[GDPR Compliance for US SaaS Companies: The Non-Lawyer's Implementation Guide](/blog/gdpr-compliance-us-saas-guide)*
- *[HIPAA Business Associate Agreement (BAA): What to Include, What to Reject, and Red Flags](/blog/business-associate-agreement-guide)*
- *[What Is GDPR? The EU Data Protection Regulation Explained for Tech Companies](/blog/what-is-gdpr)*
- *[Regulatory Compliance for SaaS in 2026: A Framework Decision Matrix](/blog/regulatory-compliance-framework-matrix)*

Open-source platform: [github.com/rahuliitk/quicktrust](https://github.com/rahuliitk/quicktrust)
