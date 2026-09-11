---
title: "What Is PCI DSS? Everything SaaS and Fintech Companies Need to Know"
meta_description: "PCI DSS (Payment Card Industry Data Security Standard) is a global security standard that any company storing, processing."
target_keyword: "pci dss, what is pci dss"
secondary_keywords: "pci dss definition, payment card industry data security standard, pci compliance meaning, pci dss requirements"
word_count_target: "1500"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# What Is PCI DSS? Everything SaaS and Fintech Companies Need to Know

PCI DSS — the Payment Card Industry Data Security Standard — is a global information security standard established by the PCI Security Standards Council (PCI SSC) that governs how organizations must protect cardholder data when storing, processing, or transmitting credit and debit card information. Any company that touches payment card data — from enterprise e-commerce platforms to SaaS tools that integrate with payment processors — must comply with PCI DSS or risk significant fines, card brand penalties, and the loss of the ability to accept card payments altogether.

---

## TL;DR — Key Takeaways

- PCI DSS applies to **any organization that stores, processes, or transmits payment cardholder data** — including SaaS companies with payment integrations
- The current version is **PCI DSS 4.0**, which became mandatory in March 2025 (replacing v3.2.1)
- There are **12 high-level requirements** organized into 6 control objectives covering network security, data protection, access control, monitoring, and more
- Compliance level is determined by **transaction volume** — from Level 1 (6 million+ transactions/year, requires QSA audit) to Level 4 (under 20,000 transactions/year, self-assessment eligible)
- **SAQs (Self-Assessment Questionnaires)** allow smaller merchants to self-certify compliance depending on how they handle card data
- Non-compliance can result in fines of $5,000–$100,000 per month and the loss of your ability to process card payments

---

## What Is the PCI Security Standards Council?

The PCI SSC is a consortium founded in 2006 by the five major card brands: **Visa, Mastercard, American Express, Discover, and JCB**. The Council maintains PCI DSS and related standards. Enforcement is handled by the individual card brands and your acquiring bank — not the PCI SSC directly.

This is an important distinction: **PCI DSS is a contractual requirement**, not a law. When you sign a merchant agreement with your payment processor, you contractually commit to PCI DSS compliance. Failure to comply is a breach of contract — and the financial consequences are severe.

---

## Who Needs PCI DSS Compliance?

If your organization **stores, processes, or transmits** cardholder data (CHD) or sensitive authentication data (SAD), PCI DSS applies:

| Entity Type | Examples |
|-------------|---------|
| **Merchants** | E-commerce sites, SaaS platforms with direct billing, retail |
| **Service providers** | Payment gateways, cloud hosting companies, managed security providers that store or process CHD on behalf of merchants |
| **Fintech companies** | Payment processors, wallet providers, BNPL platforms |
| **SaaS companies** | Any SaaS product that handles its own billing or processes customer payments directly |

**Important note for SaaS companies:** If you use a payment processor like Stripe, Braintree, or Adyen and redirect customers to their hosted payment page (never handling raw card numbers yourself), your PCI scope is dramatically reduced. However, you still have PCI compliance obligations — just under a simpler SAQ type.

---

## What Is Cardholder Data?

PCI DSS protects two categories of payment data:

**Cardholder Data (CHD) — can be stored (with protections):**
- Primary Account Number (PAN) — the 16-digit card number (must be rendered unreadable if stored)
- Cardholder name
- Expiration date
- Service code

**Sensitive Authentication Data (SAD) — can NEVER be stored after authorization:**
- Full magnetic stripe data
- CAV2/CVC2/CVV2/CID codes (the 3-4 digit security codes)
- PINs and PIN blocks

---

## The 12 PCI DSS Requirements

PCI DSS is organized around 6 control objectives and 12 high-level requirements:

### Build and Maintain a Secure Network and Systems
1. **Install and maintain network security controls** — Firewalls and equivalent technology protecting the cardholder data environment (CDE)
2. **Apply secure configurations** — No vendor-supplied defaults; document all system components

### Protect Account Data
3. **Protect stored account data** — Encryption, truncation, masking, or hashing of PANs; never store SAD post-authorization
4. **Protect cardholder data with strong cryptography during transmission** — TLS 1.2+ for all transmissions over open/public networks

### Maintain a Vulnerability Management Program
5. **Protect all systems against malware** — Anti-malware on all systems; regular updates
6. **Develop and maintain secure systems and software** — Vulnerability management, secure development practices, patch management

### Implement Strong Access Control Measures
7. **Restrict access to system components and cardholder data by business need** — Role-based access; least privilege principle
8. **Identify users and authenticate access** — Unique user IDs, MFA for all non-console administrative access and remote access
9. **Restrict physical access to cardholder data** — Physical access controls, visitor logs, media destruction

### Regularly Monitor and Test Networks
10. **Log and monitor all access to network resources and cardholder data** — Audit logs, log review, time synchronization
11. **Test security of systems and networks regularly** — Vulnerability scans (quarterly), penetration testing (annually), intrusion detection

### Maintain an Information Security Policy
12. **Support information security with organizational policies and programs** — Security policy, risk assessments, incident response plan, security awareness training

---

## PCI DSS Merchant Levels

Your PCI compliance obligations depend on your annual transaction volume with each card brand:

| Level | Transaction Volume | Compliance Requirements |
|-------|--------------------|------------------------|
| **Level 1** | 6 million+ Visa/Mastercard transactions/year | Annual on-site audit by Qualified Security Assessor (QSA); quarterly network scans by Approved Scanning Vendor (ASV) |
| **Level 2** | 1–6 million transactions/year | Annual Self-Assessment Questionnaire (SAQ); quarterly ASV scans |
| **Level 3** | 20,000–1 million e-commerce transactions/year | Annual SAQ; quarterly ASV scans |
| **Level 4** | Under 20,000 e-commerce transactions/year | Annual SAQ; quarterly ASV scans (recommended) |

**Service providers** have their own leveling system: Level 1 service providers (storing, processing, or transmitting 300,000+ transactions/year) require an annual QSA audit and a Report on Compliance (ROC). Level 2 service providers can use an SAQ.

---

## Self-Assessment Questionnaires (SAQs): Which One Do You Need?

SAQs allow eligible merchants and service providers to self-certify their PCI compliance. The right SAQ depends on how you handle cardholder data:

| SAQ Type | Who Uses It | Cardholder Data Environment |
|----------|-------------|----------------------------|
| **SAQ A** | E-commerce merchants; all cardholder data functions outsourced to PCI-compliant third parties | No electronic storage, processing, or transmission of CHD on merchant systems |
| **SAQ A-EP** | E-commerce merchants with partially outsourced payment pages | No electronic storage, but third-party payment page is not fully controlled by the processor |
| **SAQ B** | Merchants using imprint machines or standalone dial-out terminals | No electronic storage; limited connectivity |
| **SAQ B-IP** | Merchants with standalone IP-connected payment terminals | Terminals are isolated from other networks |
| **SAQ C** | Merchants with payment applications connected to the internet | No electronic storage of CHD |
| **SAQ C-VT** | Merchants using virtual terminals on isolated computers | Only web-based virtual terminal; no other cardholder data systems |
| **SAQ D** | All other merchants and service providers | Electronic storage of cardholder data or more complex environments |
| **SAQ P2PE** | Merchants using validated point-to-point encryption solutions | Card data never entered electronically; hardware payment terminal only |

Most SaaS companies using Stripe or similar processors with hosted checkout fall under **SAQ A** — the simplest form with the fewest requirements.

---

## PCI DSS 4.0: What Changed?

PCI DSS 4.0 became the mandatory standard in March 2025. Key changes from v3.2.1:

- **Expanded multi-factor authentication (MFA):** MFA is now required for all access into the cardholder data environment — not just administrator access and remote access
- **Customized approach:** Organizations can now implement alternative controls that meet the intent of a requirement rather than the specific control listed — subject to thorough documentation and validation
- **E-commerce security:** New targeted requirements for protecting payment pages from skimming attacks (client-side script management, integrity checking)
- **Phishing controls:** Anti-phishing controls are now a formal requirement
- **Password/authentication requirements updated:** Minimum password length increased to 12 characters; password change policies updated
- **Expanded cloud and shared responsibility guidance:** Clearer requirements for cloud environments and service provider relationships

Organizations that were compliant with v3.2.1 should conduct a gap assessment against v4.0 requirements — there are over 60 new or evolved requirements.

> **Free Download:** [Audit Evidence Checklist](/resources/audit-evidence-checklist) — The complete list of evidence artifacts your QSA or assessor will request, organized by PCI DSS requirement. [Download now →](/resources/audit-evidence-checklist)

---

## Common Misconceptions About PCI DSS

**Misconception 1: "We use Stripe, so we don't need PCI DSS compliance."**
Using Stripe reduces your scope — but does not eliminate your PCI obligations. You still need to complete an SAQ (typically SAQ A), scan your environment, and maintain applicable security controls.

**Misconception 2: "PCI compliance means we can't be breached."**
Compliance reduces risk but is not a guarantee. Organizations that were PCI compliant at the time of a breach have still faced card brand fines because they were not compliant at the exact time of the incident.

**Misconception 3: "PCI DSS is only for large companies."**
Small merchants are the most common targets for payment card theft precisely because their security is often weaker. Level 4 merchants face real consequences for non-compliance.

**Misconception 4: "Once we're compliant, we're done."**
PCI DSS requires continuous compliance — quarterly scans, annual assessments, and ongoing security operations.

---

## How QuickTrust Helps With PCI DSS Compliance

QuickTrust's security and DevOps engineers implement the technical controls that PCI DSS requires — from network segmentation to logging pipelines to secure CI/CD practices.

**What QuickTrust delivers for PCI DSS:**
- **Scope reduction strategy** — Identify the fastest path to minimal CDE scope through tokenization, hosted payment fields, and network segmentation
- **Network security implementation** — Configure firewall rules, network segments, and security controls isolating the CDE from other systems
- **Encryption and key management** — Implement TLS enforcement, database encryption, and key management procedures
- **Access control and MFA** — Configure IAM policies, role-based access, MFA enforcement meeting PCI DSS 4.0 requirements
- **Logging and monitoring** — Deploy centralized log management covering all CDE systems, with alerting for suspicious activity
- **Vulnerability management** — Quarterly ASV scans, annual penetration testing, patch management process
- **SAQ completion and QSA coordination** — Navigate your applicable SAQ type or coordinate QSA audit engagement
- **PCI DSS 4.0 gap assessment** — Map your current controls against all 12 requirements under the new standard

**Result:** 100% audit pass rate. Audit-ready in 6–10 weeks. 90% reduction in engineering time.

---

## PCI DSS FAQ

### What happens if we're not PCI DSS compliant and have a breach?

If a breach occurs and you are found non-compliant, the card brands and your acquiring bank can impose: fines of $5,000–$100,000 per month of non-compliance, forensic investigation costs (often $20,000–$100,000+), card reissuance costs charged back to you, and potential termination of your ability to accept card payments. Non-compliant merchants also lose most of the liability protection that compliance provides.

### Do we need PCI DSS if we outsource all payment processing?

Outsourcing reduces your scope but does not eliminate your obligations. You still need to ensure your service provider is PCI compliant (verify via the Visa/Mastercard service provider lists), execute appropriate agreements, and complete the applicable SAQ for your environment.

### How long does PCI DSS compliance take to achieve?

For most SaaS companies with limited scope (SAQ A or SAQ A-EP), achieving compliance can take 4–8 weeks with dedicated resources. For companies with more complex environments requiring full QSA audits, the timeline is typically 3–6 months. QuickTrust's engineering-included model accelerates this significantly.

### What is a QSA?

A Qualified Security Assessor (QSA) is a company approved by the PCI SSC to conduct Level 1 PCI DSS audits and issue Reports on Compliance (ROC). Not all compliance consultants are QSAs. Level 1 merchants and service providers must use a PCI SSC-certified QSA for their annual assessments.

### Is PCI DSS required by law?

PCI DSS is not a law — it is a contractual requirement between merchants and their acquiring banks, enforced through card brand rules. However, several US states have incorporated PCI DSS compliance requirements into state law, and non-compliance can trigger state consumer protection actions following a breach.

---

## Ready to Achieve PCI DSS Compliance?

Whether you're scoping your first SAQ or preparing for a Level 1 QSA audit, QuickTrust's engineers implement the controls — not just the documentation.

**Get your PCI DSS gap assessment at [trust.quickintell.com](https://trust.quickintell.com)**

Engineering-included. Audit-ready in 6–10 weeks. 100% audit pass rate.

---

## Related Reading

- [The Complete Guide to PCI DSS Compliance](/blog/pillar-pci-dss-complete-guide)
- [PCI DSS 4.0: What Changed and What You Need to Do](/blog/pci-dss-4-requirements-changes)
- [How Much Does a PCI DSS Audit Cost?](/blog/pci-dss-audit-cost-guide)

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "What Is PCI DSS? Everything SaaS and Fintech Companies Need to Know",
  "description": "PCI DSS (Payment Card Industry Data Security Standard) is a global security standard that any company storing, processing, or transmitting cardholder data must follow. Learn the 12 requirements, merchant levels, SAQ types, and what PCI DSS 4.0 changes.",
  "author": {
    "@type": "Organization",
    "name": "QuickTrust",
    "url": "https://trust.quickintell.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "QuickTrust",
    "url": "https://trust.quickintell.com"
  },
  "datePublished": "2026-02-28",
  "dateModified": "2026-02-28"
}
</script>
