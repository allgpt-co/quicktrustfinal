---
meta_description: "PCI DSS 4.0 is now fully enforced. Learn what the 64 new mandatory requirements mean for your engineering team, what changed from 3.2."
target_keyword: "pci 4.0"
secondary_keywords:
  - "pci dss requirements"
  - "pci dss 4.0 changes"
  - "pci dss 4.0 requirements"
word_count_target: 2,200+
last_updated: "2026-03-22"
published: true
author: QuickTrust Editorial
---

# PCI DSS 4.0 Requirements: What Changed and What Your Engineering Team Must Implement Now

The grace period is over.

PCI DSS 4.0 was released in March 2022. Version 3.2.1 was retired on March 31, 2024. But the headline most engineering teams missed: **64 additional requirements** within version 4.0 carried a "future-dated" status with a compliance deadline of March 31, 2025. That deadline has passed. All 64 requirements are now mandatory.

If your last assessment was completed against 3.2.1, or if you assessed against 4.0 before March 2025 and treated those future-dated requirements as optional, your current posture has gaps. This is not a hypothetical risk — QSAs are now assessing against the full set of requirements, and findings from these previously optional controls are appearing in ROCs and SAQs across the industry.

This article breaks down the most impactful changes in PCI DSS 4.0, with specific engineering actions for each.

---

## Why PCI DSS 4.0 Is a Genuine Architectural Change

PCI DSS 3.2.1 was largely prescriptive: do this exact thing. 4.0 is outcome-focused: achieve this security objective, and you can choose your implementation path. That sounds like more flexibility — and it is — but it also requires more documentation, risk analysis, and QSA collaboration.

The other shift: 4.0 explicitly targets the threat landscape of the 2020s, particularly:

- **E-skimming (Magecart-style attacks)** on payment pages
- **Phishing and social engineering** against payment operations staff
- **Identity-based attacks** against privileged accounts
- **Supply chain risks** from third-party scripts and payment libraries

If your previous compliance program treated these as edge cases, PCI DSS 4.0 treats them as primary controls.

---

## The Customized Approach: Flexibility with a Documentation Price

The most architecturally significant change in 4.0 is the introduction of the **Customized Approach**. Under the old standard, each requirement had a defined control implementation. Under the Customized Approach, you can meet the stated security objective through a different technical control — as long as:

1. You document the control fully in a **Controls Matrix**
2. You perform and document a **Targeted Risk Analysis** justifying the control
3. The control is tested and validated by a QSA
4. The QSA formally assesses your custom control against the stated objective

**Who this is for:** Organizations with mature, innovative security architectures that already exceed PCI prescriptive requirements through different means. For example, if you use a behavioral analytics platform instead of traditional FIM, the Customized Approach lets you formalize that.

**Engineering action required:** If you want to use the Customized Approach for any requirement, prepare documentation before your assessment. QSAs cannot approve a custom control they haven't reviewed. Build the Controls Matrix early.

---

## Requirement-by-Requirement Changes Your Engineering Team Must Address

### Requirement 1: Network Security Controls

**What changed:** The language shifted from "firewall and router rules" to "network security controls" — recognizing that modern environments use cloud-native controls, not just physical appliances.

**New 4.0 requirements now mandatory:**
- Network security control rulesets must be reviewed at least every six months, with documented review results retained
- All services, protocols, and ports allowed must have documented business justification
- Bi-annual review of all connected components and their necessity

**Engineering action:** Automate the six-month review process. Use AWS Config Rules or GCP Organization Policy to flag any security group or firewall rule without a documented business justification tag. Build a reconciliation process between your infrastructure-as-code (Terraform/CloudFormation) and your network documentation.

---

### Requirement 3: Protect Stored Account Data

**What changed (previously future-dated, now mandatory):**
- Organizations must perform a targeted risk analysis to determine the frequency of reviewing cryptographic key management procedures — at minimum annually
- Disk-level encryption (such as BitLocker or OS-level full-disk encryption) is now explicitly insufficient to satisfy the requirement for rendering PAN unreadable — you must use database-level or field-level encryption
- Hashing algorithms used for one-way hashes of PAN must be keyed — unkeyed hashes are no longer acceptable

**Engineering action:** If you are using full-disk encryption or AES-256 at the volume level and storing PAN fields in your database, this is a gap. Migrate to field-level encryption using a proper key management solution (AWS KMS, GCP Cloud KMS, Azure Key Vault). Ensure hashing implementations use HMAC, not plain SHA-256.

---

### Requirement 6: Develop and Maintain Secure Systems and Software

This requirement has the most significant changes for software engineering teams.

**6.2.4 — Prevent Common Software Attacks (Now mandatory)**

All custom and bespoke software must be protected against:
- Injection attacks (SQL injection, command injection, LDAP injection)
- Attacks on data and data structures (buffer overflows, XML attacks)
- Attacks on cryptography
- Business logic attacks

This must be achieved through automated technical controls integrated in the software development pipeline — not just code review.

**Engineering action:** Integrate SAST (Static Application Security Testing) into your CI/CD pipeline. Tools include Semgrep, Checkmarx, Snyk Code, Veracode. Findings from SAST scans must be triaged and tracked. Critical and high findings must be remediated before deployment to production.

**6.3.3 — All Software in the CDE Must Be Protected Against Known Vulnerabilities**

All software components (including third-party libraries and open-source dependencies) must be protected against known vulnerabilities at the time of deployment. This directly targets supply chain attacks.

**Engineering action:** Implement SCA (Software Composition Analysis) scanning. Tools include Snyk Open Source, OWASP Dependency Check, or GitHub Dependabot with a policy requiring remediation before merge. Maintain a software inventory (SBOM — Software Bill of Materials) for all in-scope systems.

**6.4.1 and 6.4.2 — E-Commerce Payment Page Protection (Now fully mandatory)**

These requirements directly target Magecart/e-skimming attacks:

- **6.4.1:** All payment pages delivered to end-users must have a mechanism to detect and alert on unauthorized modification of HTTP headers and script contents
- **6.4.2:** A content security policy (CSP) or equivalent mechanism must prevent unauthorized script execution on payment pages

**Engineering action:** This is one of the most commonly missed new requirements. Implement:
1. A Content Security Policy header on all payment pages with a strict script-src directive
2. Subresource Integrity (SRI) hashes on all externally loaded scripts
3. A monitoring mechanism (e.g., real-user monitoring or synthetic monitoring) to alert on CSP violations
4. An explicit inventory of all authorized scripts on payment pages, reviewed at least every six months (6.4.3)

---

### Requirement 7: Restrict Access by Business Need to Know

**What changed:**
- Access control systems must be reviewed for all accounts at least every six months — previously this was an annual requirement for some account types
- Privileged access must be reviewed at least every six months, with documentation of the review

**Engineering action:** Automate access reviews using your IdP (Okta, Azure AD, Google Workspace). Export user-to-role mappings quarterly and build an approval workflow. This can be partially automated with tools like Vanta, Drata, or the QuickTrust platform for continuous evidence collection.

---

### Requirement 8: Identify Users and Authenticate Access

The most operationally impactful changes in 4.0 live in Requirement 8.

**8.3.6 — Minimum Password Length Increased to 12 Characters**

PCI DSS 3.2.1 required seven characters. 4.0 requires 12. This sounds simple but it affects:
- Your IdP password policies
- Any internal applications with local authentication
- Service account password rotation policies
- Any documentation or user-facing content about password requirements

**8.3.9 — Password History Requirement**

Passwords must not match the previous four passwords (increased from the implicit guidance in 3.2.1).

**8.4.2 — MFA Required for All CDE Access**

Previously, MFA was required for remote access to the CDE. Now it is required for all access to the CDE, including:
- Local network access by administrators
- Jump host / bastion host sessions
- Direct console access
- Database client access to CDE databases

**Engineering action:** Audit every access path into the CDE. If any path does not enforce MFA, it is a finding. This includes developer access via VPN, database administration tools (DBeaver, TablePlus, pgAdmin), and internal admin dashboards.

**8.6.1 — Service Accounts Must Have MFA or Equivalent Controls**

Interactive service accounts — service accounts that can be logged into by a human — must have MFA. Non-interactive service accounts must have their passwords rotated at least every 12 months or upon personnel changes.

**Engineering action:** Audit your service account inventory. Identify any service account credentials that have not been rotated in over 12 months. Implement an automated rotation process using AWS Secrets Manager, GCP Secret Manager, or HashiCorp Vault.

> **Free Download:** Audit Evidence Checklist — Map every PCI DSS 4.0 requirement to the exact evidence artifacts your QSA will request. [Download now →](/resources/audit-evidence-checklist)

---

### Requirement 10: Log and Monitor All Access

**10.7.2 and 10.7.3 — Failures of Critical Security Controls Must Be Detected and Responded To**

Failures in security controls — such as intrusion detection going offline, logging failures, or FIM deactivation — must be detected promptly and documented. This must include a defined response process.

**Engineering action:** Build alerting for security control failures, not just security events. If your CloudTrail logging stops, if your SIEM loses connectivity, or if your antimalware signatures are not updating — those failures must trigger alerts that go to the security team, not just to operations.

---

### Requirement 11: Test Security

**11.6.1 — Payment Page Change Detection Mechanism**

A mechanism must be deployed to detect unauthorized changes to HTTP headers and content on payment pages. This must alert personnel to investigate within 48 hours of detection.

**Engineering action:** Implement a page integrity monitoring solution. Options include commercial tools (Featurespace, Jscrambler, Source Defense) or a custom implementation using CloudFront Functions or Lambda@Edge to inject and validate script hashes on every page response.

---

### Requirement 12: Organizational Policies and Programs

**12.3.2 — Targeted Risk Analysis for Customized Approach**

Any requirement where you use the Customized Approach requires a documented targeted risk analysis. This must be reviewed annually by personnel with appropriate risk management expertise.

**12.6.3.1 and 12.6.3.2 — Phishing Training Now Explicit**

Security awareness training must now explicitly address phishing and related social engineering attacks. Training content must be reviewed annually and updated to reflect current threat techniques.

**Engineering action:** Implement a phishing simulation program with quarterly simulations. Track click rates, reporting rates, and training completion. This data becomes part of your PCI compliance evidence.

---

## The 64 Previously Future-Dated Requirements: Summary by Category

Rather than listing all 64, here are the categories where the highest concentration of new mandatory requirements now live:

| Category | Number of New Mandatory Requirements | Engineering Impact |
|----------|-------------------------------------|-------------------|
| E-commerce payment page protection (Req 6.4) | 3 | High — CSP, SRI, script monitoring |
| Authentication and MFA (Req 8.4, 8.6) | 7 | High — MFA everywhere in CDE |
| Cryptography and key management (Req 3) | 4 | Medium — field-level encryption, keyed hashes |
| Software security / SAST / SBOM (Req 6.2, 6.3) | 6 | High — pipeline changes required |
| Logging and control failure detection (Req 10.7) | 3 | Medium — alerting configuration |
| Risk analysis for frequency (multiple Req) | 14 | Low-Medium — documentation work |
| Physical security and access review (Req 9, 7) | 5 | Low for cloud-native |
| Phishing awareness (Req 12.6) | 3 | Low — training program update |
| Vendor and third-party management (Req 12.8) | 5 | Medium — attestation collection |
| Penetration testing methodology (Req 11.4) | 4 | Medium — scope and reporting updates |

---

## Mid-Article CTA

**Not sure which of the 64 new requirements your environment is missing?** QuickTrust's engineers conduct a full PCI DSS 4.0 gap assessment and implement the controls directly in your cloud environment. [Have our engineers audit your PCI DSS 4.0 readiness](https://trust.quickintell.com).

---

## What to Do If Your Last Assessment Was Against 3.2.1

1. **Map your current controls to PCI DSS 4.0 requirements.** Use the PCI SSC's Summary of Changes document (available free at pcisecuritystandards.org) as your crosswalk.

2. **Identify the future-dated requirements that now apply.** Focus first on Requirement 8 (MFA changes), Requirement 6.4 (payment page protection), and Requirement 3 (cryptography).

3. **Engage your QSA early.** Alert your QSA to your intent to remediate before your next scheduled assessment. QSAs can provide pre-assessment guidance.

4. **Prioritize by risk and engineering complexity.** MFA enforcement and password policy changes are typically low-effort, high-impact. Payment page script monitoring may require architectural work.

5. **Document everything.** PCI DSS 4.0 requires more documented risk analyses and justifications than 3.2.1. Start building documentation alongside your technical controls.

---

## Related Resources

- [PCI DSS Compliance: The Complete Guide](./pillar-pci-dss-complete-guide.md)
- [PCI DSS Scope Reduction: Cut Your Audit Surface by 70%](./pci-dss-scope-reduction-guide.md)
- [PCI DSS Audit Cost in 2026](./pci-dss-audit-cost-guide.md)
- [Cybersecurity Policy Templates: 15 Policies Before Your First Audit](./cybersecurity-policy-templates-guide.md)

---

## Related Reading

- [PCI DSS Compliance: The Complete Guide](/blog/pillar-pci-dss-complete-guide)
- [PCI DSS Audit Cost Guide](/blog/pci-dss-audit-cost-guide)
- [PCI DSS Scope Reduction Guide](/blog/pci-dss-scope-reduction-guide)

---

## Have Our Engineers Audit Your PCI DSS 4.0 Readiness

QuickTrust's security engineers conduct a complete PCI DSS 4.0 gap assessment against your current environment and deliver a prioritized remediation roadmap within seven days — with the option to have our engineers implement every finding directly.

100% audit pass rate. Audit-ready in 6–10 weeks. Your engineering team spends fewer than 20 hours total.

[Schedule your PCI DSS 4.0 readiness audit at trust.quickintell.com](https://trust.quickintell.com)

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "PCI DSS 4.0 Requirements: What Changed and What Your Engineering Team Must Implement Now",
  "description": "PCI DSS 4.0 is now fully enforced. Learn what the 64 new mandatory requirements mean for your engineering team, what changed from 3.2.1, and how to close the gaps before your next assessment.",
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
  "datePublished": "2026-05-01",
  "dateModified": "2026-02-28"
}
</script>
