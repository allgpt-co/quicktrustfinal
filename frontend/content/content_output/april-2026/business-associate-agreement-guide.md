---
meta_description: "HIPAA Business Associate Agreement (BAA) guide for SaaS companies: required elements, common negotiation points, red flags in vendor BAAs."
target_keyword: "business associate agreement"
secondary_keywords: "business associate agreement hipaa, baa hipaa, hipaa baa template, hipaa business associate"
word_count_target: 2000
publish_date: April 2026
published: true
lead_magnet: "BAA template download"
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# HIPAA Business Associate Agreement (BAA): What to Include, What to Reject, and Red Flags

Healthcare enterprise deals have a specific kill switch: the Business Associate Agreement.

You have passed the security questionnaire. The deal is progressing. Then legal on the buyer's side sends over a BAA. Or they ask for yours. And suddenly the deal stalls because your company has never negotiated a BAA before, your template is a two-page document found on a compliance blog in 2019, or your vendor's standard BAA contains provisions that create unacceptable liability.

This guide cuts through the legalese. It explains what a BAA is, what HIPAA requires it to contain, what is commonly negotiated, what constitutes a genuine red flag, and how to structure your own BAA template for deals where you are the Business Associate being asked to sign.

---

## What Is a Business Associate Agreement?

A Business Associate Agreement (BAA) is a legally binding contract required by HIPAA between a Covered Entity and a Business Associate, or between a Business Associate and its subcontractors, whenever the Business Associate will create, receive, maintain, or transmit Protected Health Information (PHI) on behalf of the covered entity.

HIPAA mandates BAAs under 45 CFR § 164.504(e) (Privacy Rule) and 45 CFR § 164.314(a) (Security Rule). Both sets of regulations specify required contract provisions.

**Who signs a BAA:**

- Hospital system (Covered Entity) ↔ EHR integration platform (Business Associate) — requires BAA
- Business Associate ↔ Cloud provider hosting ePHI (Subcontractor Business Associate) — requires BAA
- Business Associate ↔ Monitoring platform that processes log data containing ePHI — requires BAA

**Critical:** You cannot lawfully receive PHI from a covered entity without a BAA in place. A signed BAA is a prerequisite to going live with any healthcare customer, not a formality to handle later.

---

## Required Elements Under HIPAA

Under 45 CFR § 164.504(e)(2), a compliant BAA must contain the following provisions:

### 1. Permitted Uses and Disclosures

The BAA must specify the permitted and required uses and disclosures of PHI by the Business Associate. This should be specific to the services you provide — not a generic "any use reasonably necessary" clause.

**Good language:** "Business Associate may use and disclose PHI only as necessary to perform the services described in the Master Services Agreement, specifically [describe service functions], and as required by applicable law."

**Red flag:** Overly broad permitted use language that allows the Business Associate to use PHI for their own product improvement, training AI/ML models, or internal analytics beyond what is needed to provide the contracted service.

### 2. Prohibition on Non-Permitted Uses

The Business Associate must agree not to use or disclose PHI other than as permitted or required by the BAA or required by law.

### 3. Appropriate Safeguards

The Business Associate must agree to use appropriate safeguards to prevent use or disclosure of PHI not provided for by the BAA — and specifically to implement the administrative, physical, and technical safeguards required by the HIPAA Security Rule (45 CFR Part 164, Subpart C).

**What this means practically:** Your BAA obligates you to maintain an actual HIPAA compliance program. Signing a BAA without having implemented Security Rule safeguards is not just non-compliant — if OCR investigates, a signed BAA creates documented evidence that you accepted obligations you did not fulfill.

### 4. Subcontractor Requirements

The Business Associate must agree to obtain satisfactory assurances from subcontractors who will have access to PHI — i.e., require subcontractors to sign BAAs providing equivalent protections.

### 5. Individual Rights (When Applicable)

The BAA must require the Business Associate to:
- Make PHI available for access by individuals upon covered entity's direction (§ 164.524)
- Make PHI available for amendment (§ 164.526)
- Provide an accounting of disclosures (§ 164.528)
- Make internal practices, books, and records available to HHS

### 6. Breach and Security Incident Reporting

The Business Associate must report to the covered entity:
- Any Security Incident it becomes aware of (§ 164.314(a)(2)(i)(C))
- Any Breach of Unsecured PHI (§ 164.410)

HIPAA requires breach notification to the covered entity without unreasonable delay and no later than 60 days after discovery. However, most BAAs add contractual notification timeframes that are much shorter — commonly 24 hours, 48 hours, or 5 business days. These contractual timeframes can be shorter than the regulatory floor.

### 7. Termination Provisions

The covered entity must be permitted to terminate the BAA if the Business Associate materially breaches a provision. Upon termination, the Business Associate must return or destroy all PHI received from or created on behalf of the covered entity.

### 8. HITECH and Omnibus Compliance

Modern BAAs should reference HITECH Act requirements and confirm that direct liability under the HITECH Omnibus Rule (effective September 2013) applies to the Business Associate.

---

## Section-by-Section BAA Template Breakdown

A well-structured BAA contains these sections:

### Section 1: Definitions

Define all key terms: PHI, ePHI, Breach, Security Incident, Unsecured PHI, Covered Entity, Business Associate, Subcontractor. Reference the regulatory definitions at 45 CFR Part 164 rather than re-defining them — this ensures alignment with current regulatory requirements even as regulations are updated.

**Tip:** Avoid defining Breach more broadly than HIPAA requires. A BAA that requires notification for any "potential" or "suspected" breach — not just confirmed breaches meeting the regulatory definition — creates notification obligations for every security event, including false positives.

### Section 2: Permitted Uses and Disclosures

This is the commercial heart of the BAA. It must be specific to your service engagement.

**Permitted uses to include:**
- Uses necessary to perform the services under the MSA (cross-reference the service description)
- Required disclosures to comply with law
- Disclosures for the proper management and administration of the Business Associate (must be required by law, or the covered entity provides written consent)
- De-identification of PHI, if applicable to your service model

**Uses to exclude:**
- Using PHI to market services to patients
- Selling PHI
- Using PHI for the Business Associate's own research or product development beyond the contracted service

### Section 3: Safeguards Obligations

Reference specific Security Rule sections. The BAA should require the Business Associate to:

- Implement all required administrative, physical, and technical safeguards (45 CFR §§ 164.308, 164.310, 164.312)
- Conduct regular risk analyses (45 CFR § 164.308(a)(1))
- Maintain security incident procedures (45 CFR § 164.308(a)(6))
- Implement a contingency plan (45 CFR § 164.308(a)(7))

**Negotiate for:** Reasonable specificity rather than a blanket obligation. "All safeguards necessary to protect PHI" is vague. "Implement the technical safeguards required under 45 CFR § 164.312" is specific and auditable.

### Section 4: Breach Notification

Define the notification window carefully. The regulatory floor is 60 days. Most enterprise covered entities push for 24–72 hours for initial notification of a suspected breach (confirmed or not), with a follow-up written report within 5–10 business days of confirmation.

**Include:**
- Discovery date definition (Business Associate is "aware" when it has a reasonable belief a breach has occurred — not just confirmed knowledge)
- Required notification content: nature of the breach, types of PHI involved, steps taken to investigate, steps taken to mitigate, steps taken to prevent recurrence
- Cooperation with covered entity's own notification obligations to HHS and individuals

**Negotiate against:** Provisions that require notification of every security "event" (firewall hit, failed login attempt). The regulatory definition of Security Incident is "the attempted or successful unauthorized access, use, disclosure, modification, or destruction of information or interference with system operations." Not every anomaly is a Security Incident requiring breach notification procedures.

### Section 5: Subcontractors

List which subcontractors will have access to PHI, or commit to maintaining a list and ensuring each has a signed BAA. Covered entities increasingly request the right to approve subcontractors or to receive notice before adding new subcontractors that will access PHI.

**Reasonable provision:** "Business Associate shall enter into a written agreement with each Subcontractor that creates, receives, maintains, or transmits PHI on Business Associate's behalf, which agreement shall impose terms no less restrictive than those in this BAA."

### Section 6: Individual Rights

For most SaaS companies providing a technical service (not a direct patient-facing application), the individual rights provisions are met by deferring to the covered entity: "Business Associate shall, upon covered entity's written request, provide access to PHI in a designated record set."

If your application is the system of record for PHI (e.g., a patient data platform), you need more detailed individual rights provisions including timelines for responding to access requests.

### Section 7: Term and Termination

The BAA term should match or exceed the term of the underlying service agreement. Termination provisions must allow the covered entity to terminate "immediately" or "upon written notice" if the Business Associate has materially breached the BAA and failed to cure within a defined cure period (10–30 days is standard).

**Upon termination:** Business Associate must return or destroy PHI within 30–60 days of termination. If return or destruction is infeasible, the Business Associate must document why and continue safeguards for as long as PHI is retained.

---

## Common BAA Negotiation Points

| Issue | Covered Entity's Position | Business Associate's Position | Resolution |
|---|---|---|---|
| Notification timeframe | 24 hours from discovery | 60 days per regulation | 72 hours for initial notice; 10 business days for written report |
| Subcontractor approval | Right to approve all subcontractors | No prior approval, just notification | Prior notice for material subcontractors, list maintained |
| Liability cap | Unlimited liability for PHI breaches | Cap at 12 months of fees | Tiered cap: standard cap for inadvertent, higher cap for willful neglect |
| Audit rights | Right to audit Business Associate's controls annually | On-request review with reasonable notice | Annual report or questionnaire; on-site audit only upon cause |
| Specific safeguards | Enumerate 20+ specific technical controls | Reference regulatory standards | Reference Security Rule requirements + key specifics (encryption, MFA) |

---

## Red Flags in Vendor BAAs

When you are reviewing a BAA from a cloud provider, SaaS tool, or other vendor you want to use with PHI, watch for these red flags:

**Red Flag 1: "We are a conduit, not a Business Associate"**
Some vendors claim they are exempt from HIPAA as mere data conduits. The conduit exception is extremely narrow — limited to postal carriers and couriers who transmit but do not access PHI. Any vendor whose systems store PHI even temporarily, or who can access PHI to provide their service, is a Business Associate. A vendor who refuses to sign a BAA citing conduit status cannot legally handle your PHI.

**Red Flag 2: Broad permitted uses for the vendor's own benefit**
Language permitting the vendor to use PHI for "improving our services," "training our algorithms," or "aggregated analytics" is problematic unless specifically and narrowly defined. Under HIPAA, the Business Associate's permitted uses must be in service of the covered entity — not the Business Associate's own commercial interests.

**Red Flag 3: No encryption requirement**
A BAA that does not specify encryption requirements for ePHI at rest and in transit — or that provides for "appropriate security measures" without specificity — gives you limited contractual protection if the vendor has a breach involving unencrypted data.

**Red Flag 4: Unilateral modification of the BAA**
Vendor BAAs that allow the vendor to modify the terms upon notice (without your consent) can be problematic. Material changes to PHI handling terms should require mutual agreement.

**Red Flag 5: Short-form BAA with no actual substance**
A two-paragraph "HIPAA Business Associate Agreement" that says "we comply with HIPAA" and lists five bullet points does not meet the regulatory requirements of 45 CFR § 164.504(e)(2). Courts and OCR have found that inadequate BAAs do not satisfy the requirement to have a BAA in place.

**Red Flag 6: No mention of HITECH or Omnibus Rule**
Pre-2013 BAAs are often missing the Business Associate's direct liability under HITECH. A modern BAA should reference the Omnibus Rule and confirm the Business Associate's direct compliance obligations.

---

## Mid-Article CTA

**Need a HIPAA BAA template you can actually use?**

Download QuickTrust's free BAA template — reviewed by HIPAA counsel, covering all required regulatory elements, with negotiation guidance for common disputed provisions.

**[Download our BAA template →](https://trust.quickintell.com)**

---

## Major Cloud Provider BAAs: Key Points

**AWS BAA:** Available to all AWS customers, signed through the AWS Management Console. Covers a defined list of HIPAA-eligible services. AWS agrees to use ePHI only to provide and improve its services. Customer is responsible for configuring AWS services in a HIPAA-compliant manner.

**Google Cloud BAA:** Available to Google Cloud customers. Covers core GCP services. Google processes PHI only as instructed and in accordance with its Privacy Policy. Google's Cloud Healthcare API includes specialized HIPAA-compliant PHI storage.

**Microsoft Azure BAA:** Included in Microsoft's Online Services Terms (OST) for eligible services. Among the broadest coverage of any major cloud provider. Azure's BAA also covers Microsoft 365 and Microsoft Teams for eligible plans.

---

## Conclusion

A BAA is not a formality — it is the legal foundation of your HIPAA compliance relationship with every covered entity customer. A poorly drafted BAA creates liability exposure. A BAA with red flag provisions can create obligations you cannot fulfill. A BAA with a vendor who handles your PHI without signing one creates OCR enforcement risk.

Getting your BAA template right is one of the highest-leverage compliance investments a healthcare SaaS company can make. It accelerates deals (procurement teams have fewer comments to a well-drafted template), reduces legal fees (less negotiation on the fundamentals), and reduces liability exposure.

[→ See our complete HIPAA compliance guide for healthcare SaaS founders]
[→ Understand the difference between HIPAA certified and HIPAA compliant]

---

## Download Our BAA Template

QuickTrust's free BAA template includes all required HIPAA elements, standard negotiation positions with annotations, and guidance on cloud provider BAA integration.

**[Download our BAA template →](https://trust.quickintell.com)**

Open-source platform: [github.com/rahuliitk/quicktrust](https://github.com/rahuliitk/quicktrust)

---

## Related Reading

- [ISO 27001 Certification: The Complete Implementation Guide](/blog/pillar-iso27001-complete-guide)
- [HIPAA Compliance Guide for Healthcare SaaS](/blog/hipaa-compliance-healthcare-saas-guide)
- [What Is a Business Associate Agreement?](/blog/what-is-a-business-associate-agreement)

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "HIPAA Business Associate Agreement (BAA): What to Include, What to Reject, and Red Flags",
  "description": "HIPAA Business Associate Agreement (BAA) guide for SaaS companies: required elements, common negotiation points, red flags in vendor BAAs, section-by-section template breakdown, and when to accept or reject BAA terms.",
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
  "datePublished": "2026-04-01",
  "dateModified": "2026-02-28"
}
</script>
