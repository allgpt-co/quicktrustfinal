---
title: "NIST 800-171: The Complete Guide to Protecting CUI and Achieving DFARS Compliance"
meta_description: "Complete guide to NIST 800-171 compliance. Covers CUI protection, 14 control families, CMMC relationship, self-assessment, and SOC 2 mapping."
target_keyword: "NIST 800-171"
secondary_keywords: "NIST 800-171 compliance, controlled unclassified information, CUI protection, DFARS compliance, CMMC requirements, NIST 800-171 controls"
word_count_target: "1500"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# NIST 800-171: The Complete Guide to Protecting CUI and Achieving DFARS Compliance

If your organization handles Controlled Unclassified Information (CUI) for the U.S. federal government -- or if you are part of a defense supply chain -- NIST Special Publication 800-171 is not optional. It defines the minimum security requirements for protecting CUI in nonfederal systems, and compliance is a contractual obligation embedded in Department of Defense (DoD) contracts through the Defense Federal Acquisition Regulation Supplement (DFARS) clause 252.204-7012.

With the Cybersecurity Maturity Model Certification (CMMC) program now codifying these requirements into a mandatory certification framework, organizations can no longer treat NIST 800-171 as a paperwork exercise. This guide covers what CUI is, who needs to comply, the 14 control families, how NIST 800-171 relates to CMMC, and a practical implementation approach.

## What Is Controlled Unclassified Information (CUI)?

CUI is information that the government creates or possesses -- or that an entity creates or possesses on behalf of the government -- that requires safeguarding but is not classified under Executive Order 13526 or the Atomic Energy Act.

CUI includes categories such as:

- **Export-controlled technical data** (ITAR, EAR)
- **Proprietary business information** shared under contract
- **Law enforcement sensitive information**
- **Critical infrastructure information**
- **Federal tax information**
- **Personally identifiable information (PII)** held for government purposes

The National Archives and Records Administration (NARA) maintains the CUI Registry, which lists all approved CUI categories and subcategories. If your contract specifies that you will handle CUI, the contract itself typically identifies the applicable CUI categories.

The critical point: if you are a contractor, subcontractor, or supplier in the defense industrial base and your work involves any form of sensitive but unclassified government information, NIST 800-171 likely applies to you.

## Who Needs NIST 800-171 Compliance?

**Direct DoD Contractors.** Any organization with a DoD contract that includes DFARS 252.204-7012 must implement NIST 800-171 controls. This applies to contracts involving CUI.

**Subcontractors in the Defense Supply Chain.** The DFARS clause flows down to subcontractors. If a prime contractor shares CUI with your organization as part of contract performance, you are obligated to protect that CUI in accordance with NIST 800-171.

**Other Federal Agencies.** While NIST 800-171 originated in the DoD context, other federal agencies increasingly reference it in their contracts and grant requirements. NASA, the Department of Energy, and the General Services Administration have all incorporated NIST 800-171 requirements.

**Higher Education and Research Institutions.** Universities and research organizations that receive federal grants involving CUI must also comply, which has created significant implementation challenges for institutions with decentralized IT environments.

## The 14 Control Families

NIST 800-171 Revision 2 contains 110 security requirements organized into 14 families. (Note: Revision 3 has been published and aligns controls more directly with NIST 800-53 Revision 5, but CMMC currently references Revision 2.)

**1. Access Control (AC) -- 22 requirements.** Limit system access to authorized users, processes, and devices. Covers account management, least privilege, remote access, and wireless access controls.

**2. Awareness and Training (AT) -- 3 requirements.** Ensure personnel are aware of security risks and trained on policies and procedures applicable to their roles.

**3. Audit and Accountability (AU) -- 9 requirements.** Create, protect, and retain system audit logs. Ensure individual actions can be traced to specific users.

**4. Configuration Management (CM) -- 9 requirements.** Establish and maintain baseline configurations. Control changes to systems. Restrict nonessential programs, functions, and services.

**5. Identification and Authentication (IA) -- 11 requirements.** Identify and authenticate users, processes, and devices before granting access. Enforce multi-factor authentication for network and privileged access.

**6. Incident Response (IR) -- 3 requirements.** Establish incident response capabilities including preparation, detection, analysis, containment, recovery, and reporting.

**7. Maintenance (MA) -- 6 requirements.** Perform timely maintenance. Control maintenance tools and personnel, especially for remote maintenance activities.

**8. Media Protection (MP) -- 9 requirements.** Protect, sanitize, and destroy media containing CUI. Control the transport of media outside controlled areas.

**9. Personnel Security (PS) -- 2 requirements.** Screen individuals before granting access to CUI. Protect CUI during personnel actions such as terminations and transfers.

**10. Physical Protection (PE) -- 6 requirements.** Limit physical access to systems, equipment, and operating environments. Protect and monitor the physical facility.

**11. Risk Assessment (RA) -- 3 requirements.** Periodically assess risk to operations, assets, and individuals. Scan for vulnerabilities and remediate them.

**12. Security Assessment (CA) -- 4 requirements.** Periodically assess security controls. Develop and implement plans of action to correct deficiencies. Monitor controls on an ongoing basis.

**13. System and Communications Protection (SC) -- 16 requirements.** Monitor, control, and protect communications at system boundaries. Implement cryptographic mechanisms to protect CUI in transit and at rest.

**14. System and Information Integrity (SI) -- 7 requirements.** Identify, report, and correct system flaws in a timely manner. Monitor systems for unauthorized access and anomalous activity.

## The Relationship Between NIST 800-171 and CMMC

The Cybersecurity Maturity Model Certification (CMMC) program was created to verify that defense contractors actually implement the security requirements they claim. Before CMMC, compliance was entirely self-attested, and DoD investigations found widespread gaps between self-reported compliance and actual security posture.

**CMMC Level 1** covers 15 basic safeguarding requirements from FAR 52.204-21 (Federal Contract Information, not CUI). Self-assessment is permitted.

**CMMC Level 2** maps directly to the 110 requirements of NIST 800-171 Revision 2. This level requires a third-party assessment by a CMMC Third-Party Assessor Organization (C3PAO) for contracts involving prioritized CUI. Some contracts will allow self-assessment at this level.

**CMMC Level 3** includes NIST 800-171 plus additional requirements from NIST 800-172 (enhanced security). Government-led assessments are required.

The practical takeaway: if you are pursuing CMMC Level 2, your implementation path is NIST 800-171. The framework is the same; CMMC adds a verification mechanism.

## Self-Assessment vs. Third-Party Assessment

**Self-Assessment.** Organizations can (and should) conduct self-assessments against NIST 800-171 using the DoD Assessment Methodology. Scores range from -203 (no controls implemented) to 110 (full implementation). Scores must be submitted to the Supplier Performance Risk System (SPRS). False reporting carries significant liability under the False Claims Act.

**Third-Party Assessment (CMMC).** For contracts requiring CMMC Level 2 certification with third-party assessment, a C3PAO will conduct the evaluation. Assessors examine evidence of implementation -- documentation, configurations, logs, and interviews -- for each of the 110 requirements.

Organizations should treat self-assessment as preparation for third-party certification, not as an alternative to it. Conducting an honest self-assessment identifies gaps early and prevents costly failures during formal assessments.

## Common Implementation Gaps

After working with defense contractors across the supply chain, these are the most frequent gaps we observe:

**Multi-Factor Authentication.** Requirement 3.5.3 mandates MFA for local and network access to privileged accounts and for network access to non-privileged accounts. Many organizations have implemented MFA for some systems but not all, or have not addressed service accounts and API access.

**Audit Log Management.** Requirements in the AU family demand comprehensive logging, protection of audit information, and the ability to correlate audit records. Organizations often log selectively rather than comprehensively, and many lack centralized log management.

**CUI Boundary Definition.** Organizations struggle to define the boundary of their CUI environment. Every system, network segment, and device that processes, stores, or transmits CUI is in scope. Failure to properly scope the CUI environment leads to either underprotection or unnecessarily broad (and expensive) implementation.

**Encryption.** SC requirements mandate FIPS-validated cryptographic mechanisms. Using encryption is not sufficient -- the encryption must use FIPS 140-2 (or 140-3) validated modules. Many commercial encryption implementations do not meet this standard.

**Plans of Action and Milestones (POA&M).** Security Assessment requirements allow organizations to document and track gaps through POA&Ms, but many organizations create them and never close them. Under CMMC, certain requirements cannot have open POA&Ms -- they must be fully implemented.

## How NIST 800-171 Maps to SOC 2

Organizations that already maintain SOC 2 compliance have a significant head start on NIST 800-171. There is substantial overlap between SOC 2 Trust Services Criteria and NIST 800-171 control families:

| NIST 800-171 Family | SOC 2 Trust Services Criteria |
|---------------------|-------------------------------|
| Access Control | CC6.1, CC6.2, CC6.3 |
| Audit and Accountability | CC7.1, CC7.2 |
| Configuration Management | CC8.1 |
| Identification and Authentication | CC6.1 |
| Incident Response | CC7.3, CC7.4, CC7.5 |
| Risk Assessment | CC3.1, CC3.2, CC3.3 |
| System and Communications Protection | CC6.1, CC6.6, CC6.7 |

However, SOC 2 does not cover several NIST 800-171 areas in sufficient depth, including media protection, physical security, personnel security, and maintenance. FIPS-validated encryption requirements also exceed typical SOC 2 implementations.

## Getting Started with Implementation

1. **Scope your CUI environment.** Identify every system, application, and network that touches CUI. Consider segmenting your network to minimize the CUI boundary.
2. **Conduct a gap assessment.** Evaluate your current controls against all 110 requirements. Score yourself honestly using the DoD Assessment Methodology.
3. **Prioritize remediation.** Address the highest-weighted gaps first. Focus on areas that CMMC does not allow POA&Ms.
4. **Implement and document.** Deploy technical controls, update policies, and generate evidence. Every requirement needs documented evidence of implementation.
5. **Submit your SPRS score.** Report your self-assessment score to SPRS as required.
6. **Prepare for third-party assessment.** If your contracts require CMMC Level 2 C3PAO assessment, engage with an assessor early to understand their expectations.

## How QuickTrust Supports NIST 800-171 Compliance

QuickTrust's platform maps NIST 800-171 requirements alongside your existing SOC 2, ISO 27001, or HIPAA controls, identifying where existing work satisfies requirements and where gaps remain. Our implementation engineers handle the technical remediation -- deploying FIPS-validated encryption, configuring centralized logging, implementing MFA across your CUI environment, and establishing the network segmentation that reduces your compliance scope.

For defense contractors navigating CMMC, we provide end-to-end support from gap assessment through C3PAO engagement, with 100% audit pass rate across our client engagements.

[Schedule a NIST 800-171 gap assessment](https://trust.quickintell.com) to understand your current posture and build a practical path to compliance.
