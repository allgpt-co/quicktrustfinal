---
meta_description: "Complete DPA guide for SaaS companies. Covers GDPR Article 28, Standard Contractual Clauses, sub-processor lists, breach notification, audit rights."
target_keyword: data processing agreement
secondary_keywords: DPA, gdpr article 28, data processor agreement, standard contractual clauses, sub-processor management, data processing addendum
word_count_target: "1500"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# Data Processing Agreement (DPA): What Every SaaS Company Must Include for GDPR and Global Privacy Compliance

A SaaS company closes its first European enterprise deal. The procurement team sends over a 28-page Data Processing Agreement referencing GDPR articles the company has never read, requiring commitments it has never made, and demanding a sub-processor list it has never compiled. The deal stalls for six weeks. The competitor with a DPA already on their website closes the deal instead.

For B2B SaaS companies selling to European customers, a well-drafted DPA is not a legal formality -- it is a sales enablement tool. This guide covers what a DPA must contain under GDPR, how it differs from a BAA, when Standard Contractual Clauses are needed, and how to structure a DPA that satisfies procurement teams.

---

## What a DPA Is and Why It Matters

A Data Processing Agreement is a legally binding contract between a data controller (the entity that determines the purposes and means of processing personal data) and a data processor (the entity that processes personal data on behalf of the controller). Under GDPR Article 28, whenever a controller engages a processor to handle personal data on its behalf, a DPA is mandatory.

In the B2B SaaS context:

- **Your customer is typically the controller.** They determine why and how personal data is processed -- their employees' data, their end users' data, their customers' data.
- **You, the SaaS provider, are typically the processor.** You process personal data on behalf of your customer, according to their instructions, using your platform.

The DPA governs this relationship. It defines what data you process, what you can do with it, how you must protect it, and what happens when things go wrong.

### DPA vs. BAA

A Business Associate Agreement (BAA) serves a similar function under HIPAA. Both are contracts governing how a service provider handles regulated data on behalf of a client. The key differences:

| Aspect | DPA (GDPR) | BAA (HIPAA) |
|--------|-----------|-------------|
| Regulatory basis | GDPR Article 28 | HIPAA Privacy Rule, 45 CFR 164.502(e) |
| Data covered | Personal data of EU data subjects | Protected Health Information (PHI) |
| Parties | Controller and Processor | Covered Entity and Business Associate |
| Scope | All processing on behalf of controller | Use and disclosure of PHI |
| Sub-contractor provisions | Sub-processor requirements | Subcontractor BAA requirements |
| Breach notification | Without undue delay (typically 72 hours to DPA) | Within 60 days to covered entity |
| Audit rights | Must be provided | Must be provided |
| Data transfer | Requires transfer mechanism (SCCs, adequacy) | No equivalent concept |

Companies subject to both GDPR and HIPAA -- common in healthcare SaaS -- need both a DPA and a BAA. These can be separate documents or combined into a single agreement that addresses both frameworks.

---

## GDPR Article 28: Mandatory DPA Requirements

Article 28 specifies the minimum content that must appear in every DPA. These are not optional provisions -- they are legal requirements. A DPA that omits any of these elements does not satisfy GDPR.

### Required Provisions

**1. Subject matter and duration.** Describe the processing, its duration, nature and purpose, data types, and data subject categories.

**2. Controller's instructions.** The processor may only process data on documented instructions. The processor must flag instructions that may infringe GDPR.

**3. Confidentiality.** Authorized personnel must be bound by confidentiality obligations.

**4. Security measures.** Implement appropriate technical and organizational security measures per Article 32, described specifically or in a security annex.

**5. Sub-processor requirements.** No sub-processor engagement without prior written authorization. Controllers must be informed of changes and given the opportunity to object.

**6. Data subject rights assistance.** The processor must assist with access, rectification, erasure, portability, restriction, and objection requests.

**7. Compliance assistance.** Support the controller on security, breach notification, DPIAs, and prior consultation (Articles 32-36).

**8. Data deletion or return.** At relationship end, delete or return all personal data at the controller's choice.

**9. Audit rights.** Make compliance information available and allow audits and inspections by the controller or their mandated auditor.

---

## Standard Contractual Clauses (SCCs)

When personal data is transferred from the EU/EEA to a country that does not have an adequacy decision from the European Commission, a valid transfer mechanism must be in place. The most commonly used mechanism is Standard Contractual Clauses.

### What SCCs Are

SCCs are pre-approved contractual terms adopted by the European Commission that provide appropriate safeguards for international data transfers. The current SCCs (Commission Implementing Decision 2021/914) were adopted on June 4, 2021, and replaced the previous versions.

### When SCCs Are Needed

SCCs are needed when your SaaS company is located outside the EU/EEA in a country without an adequacy decision and processes personal data of EU/EEA data subjects. The most relevant scenarios for SaaS companies:

- **US-based SaaS company processing EU customer data.** The EU-US Data Privacy Framework provides an adequacy mechanism for US companies that are certified under the framework. If your company is certified, SCCs may not be strictly necessary for US transfers, but many European customers still require them as a belt-and-suspenders approach.
- **Data processed in other non-adequate countries.** If your infrastructure, sub-processors, or support teams are located in countries without adequacy decisions (e.g., India, Philippines, most of Latin America), SCCs are required.

### SCC Modules

The current SCCs are modular. You select the module that matches your transfer scenario:

| Module | Transfer Scenario |
|--------|-------------------|
| Module 1 | Controller to Controller |
| Module 2 | Controller to Processor |
| Module 3 | Processor to Sub-Processor |
| Module 4 | Processor to Controller |

For most B2B SaaS companies, Module 2 (Controller to Processor) applies: your European customer (controller) transfers data to you (processor) outside the EEA. If you use sub-processors outside the EEA, Module 3 also applies.

### Transfer Impact Assessment

Post-Schrems II, SCCs alone may not be sufficient. You must also conduct a Transfer Impact Assessment (TIA) evaluating whether the laws and practices of the destination country provide a level of protection essentially equivalent to that in the EU. If they do not, supplementary measures (additional encryption, pseudonymization, contractual commitments) must be implemented.

---

## Sub-Processor Management

Sub-processor management is one of the most operationally challenging aspects of DPA compliance. GDPR requires transparency about who processes data and gives controllers the right to object to sub-processor changes.

### Building a Sub-Processor List

Your sub-processor list should include every third-party service that processes personal data on behalf of your customers -- cloud infrastructure (AWS, GCP, Azure), email delivery, customer support platforms, analytics services, payment processors, monitoring tools, and CDN providers. For each, document the company name, processing location, nature of processing, and categories of personal data.

### Notification and Objection Handling

Under general authorization, you must notify controllers of sub-processor changes before they take effect and provide an objection period (typically 30 days). The most scalable approach is publishing your sub-processor list on a public URL with an email subscription mechanism for change notifications.

If a controller objects, the DPA should define a resolution process: discuss the concern, offer alternatives, and -- if no resolution is possible -- allow either party to terminate the affected processing.

---

## Data Breach Notification Clauses

GDPR Article 33 requires controllers to notify their supervisory authority of a personal data breach within 72 hours of becoming aware of it. Controllers depend on processors to detect and report breaches promptly.

Your DPA's breach notification clause should specify:

**Notification timeline.** Most enterprise customers require a specific timeframe -- typically 24 to 72 hours -- rather than the GDPR standard of "without undue delay."

**Notification content.** The initial notification should cover the nature of the breach, approximate number of data subjects affected, DPO contact details, likely consequences, and measures taken to address the breach.

**Cooperation and scope.** Commit to providing ongoing updates and cooperating with investigations. Define exclusions for unsuccessful security incidents (failed logins, port scans, denial-of-service attacks without data access).

---

## Audit Rights

Article 28 requires that processors allow controllers to conduct audits. This is non-negotiable under GDPR, but the practical implementation varies significantly:

In practice, most customers accept SOC 2 Type II reports, ISO 27001 certificates, and penetration test summaries in lieu of on-site audits, with on-site audits available upon reasonable request. Standard cost allocation: the processor provides third-party audit reports at no cost; on-site audits are conducted at the controller's expense with reasonable advance notice.

---

## DPA Template Structure

A well-structured DPA for a SaaS company includes:

1. **Main body.** Definitions, roles (controller/processor), scope, duration, general obligations, governing law, and jurisdiction.
2. **Annex 1: Processing details.** Subject matter, nature and purpose, data categories, data subject categories, processing duration, and retention.
3. **Annex 2: Technical and organizational measures.** Security controls, encryption standards, access controls, incident response, business continuity. Reference your SOC 2 report or ISO 27001 certificate.
4. **Annex 3: Sub-processor list.** Current sub-processors with entity names, locations, and processing descriptions.
5. **Annex 4: Standard Contractual Clauses.** If applicable, the relevant SCC modules with completed appendices.

Publish a template DPA on your website's legal or trust page. Make it downloadable without requiring a sales conversation. European procurement teams expect self-service access to DPAs, and having one ready signals compliance maturity.

---

## Where QuickTrust Fits

QuickTrust helps SaaS companies build DPA programs that accelerate European enterprise sales rather than stall them. The platform provides GDPR-compliant DPA templates mapped to Article 28 requirements, SCC module selection guidance, sub-processor list management, and breach notification workflow automation.

Our team of Big 4-trained compliance experts and security engineers implement the technical and organizational measures your DPA commits you to -- so your contractual commitments are backed by actual controls, not aspirational statements. With a 100% audit pass rate across 100+ engagements, QuickTrust ensures your DPA is a sales accelerator, not a legal liability.

Schedule a 20-minute readiness call to review your current DPA, identify gaps against GDPR Article 28, and build a trust page that closes European deals faster.
