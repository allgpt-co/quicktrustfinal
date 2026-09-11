---
meta_description: "Step-by-step HIPAA security risk assessment template for healthcare SaaS companies. Covers the legally required assessment per 45 CFR 164."
target_keyword: "hipaa risk assessment template, hipaa security risk assessment"
secondary_keywords: "hipaa risk analysis template, hipaa risk assessment checklist, healthcare risk assessment, phi risk assessment"
word_count_target: "2000"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# HIPAA Security Risk Assessment Template
## Step-by-Step for Healthcare SaaS Companies

**Prepared by QuickTrust | trust.quickintell.com**
*AI-Powered GRC Platform + Expert Engineering Implementation*

---

## Overview and Purpose

### Why This Risk Assessment Is Legally Required

The HIPAA Security Rule — specifically **45 CFR §164.308(a)(1)** — mandates that every Covered Entity and Business Associate conduct an accurate and thorough assessment of the potential risks and vulnerabilities to the confidentiality, integrity, and availability of electronic Protected Health Information (ePHI) held or transmitted by the organization.

This is not optional. The Office for Civil Rights (OCR) has issued tens of millions of dollars in penalties to healthcare organizations whose HIPAA violations stemmed directly from failure to conduct or maintain a proper risk assessment. In virtually every HIPAA audit and enforcement action, absence of a documented risk assessment is the first finding.

**What the regulation requires (45 CFR §164.308(a)(1)(ii)(A)):**

> *"Conduct an accurate and thorough assessment of the potential risks and vulnerabilities to the confidentiality, integrity, and availability of electronic protected health information held by the covered entity or business associate."*

**What OCR's guidance says a compliant risk assessment must include:**
1. Scope of the analysis covering all ePHI
2. Data collection identifying where ePHI is stored, received, maintained, or transmitted
3. Threat identification
4. Vulnerability identification
5. Assessment of current security measures
6. Determination of likelihood of threat occurrence
7. Determination of potential impact
8. Risk level determination
9. Documentation of the assessment
10. Periodic review and updates

This template satisfies all ten requirements. Use it as-is or adapt it for your organization's specific environment.

**Who must complete this:**
- All HIPAA Covered Entities (healthcare providers, health plans, healthcare clearinghouses)
- All Business Associates — including healthcare SaaS vendors, EHR/EMR companies, telehealth platforms, RCM vendors, healthcare AI/ML companies, and any technology company that creates, receives, maintains, or transmits ePHI on behalf of a Covered Entity

**How often:**
- Initial risk assessment: Before handling ePHI
- Updates: Annually, and whenever there is a material change to operations, systems, environment, or relevant threats

---

## Template Information

**Organization Name:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Assessment Period:** From: \_\_\_\_\_\_\_\_\_\_ To: \_\_\_\_\_\_\_\_\_\_
**Assessment Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Date Completed:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Reviewed By:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Approved By (Executive):** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_\_\_
**Next Review Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Version:** \_\_\_\_\_\_\_\_\_\_

---

## Step 1: Define Scope — Systems, Data Flows, and PHI Inventory

### 1.1 Business Description

Provide a brief description of your organization's HIPAA-relevant operations:

**Organization Type:**
- [ ] Covered Entity — Healthcare Provider
- [ ] Covered Entity — Health Plan
- [ ] Covered Entity — Healthcare Clearinghouse
- [ ] Business Associate
- [ ] Subcontractor Business Associate

**Primary HIPAA-Relevant Business Activities:**
(Describe what ePHI your organization creates, receives, maintains, or transmits)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 1.2 ePHI Inventory

For each system or location where ePHI is stored, received, maintained, or transmitted, complete the following:

| # | System / Application | ePHI Data Elements Present | Storage Location (Cloud/On-Prem) | Approximate Volume | Owner / Custodian |
|---|---------------------|---------------------------|----------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |

**Common ePHI data elements to consider:**
Names, addresses, dates (birth, admission, discharge, death), phone numbers, fax numbers, email addresses, Social Security Numbers, medical record numbers, health plan beneficiary numbers, account numbers, certificate/license numbers, VINs, device identifiers, web URLs, IP addresses, biometric identifiers, full-face photographs, any other unique identifying number or code.

### 1.3 Data Flow Diagram

*Attach or describe below the flow of ePHI into, within, and out of your organization:*

**ePHI Entry Points** (how ePHI enters your environment):
- [ ] Direct patient/member data entry via web portal
- [ ] HL7 / FHIR API integration with Covered Entities
- [ ] File/batch uploads from healthcare partners
- [ ] EHR/EMR system integrations
- [ ] Claims data feeds
- [ ] Other: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**ePHI Processing and Storage:**
(List internal systems that process or store ePHI)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**ePHI Exit Points** (how ePHI leaves your environment):
- [ ] API responses to Covered Entity clients
- [ ] Reports and dashboards
- [ ] Third-party analytics platforms
- [ ] Cloud backups
- [ ] Subcontractors / Business Associate subprocessors
- [ ] Other: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 1.4 Business Associate Agreements (BAA) Inventory

| # | Vendor / Subcontractor | Service Provided | BAA Executed? | BAA Date | BAA Expiry |
|---|----------------------|-----------------|--------------|---------|-----------|
| 1 | | | Yes / No | | |
| 2 | | | Yes / No | | |
| 3 | | | Yes / No | | |
| 4 | | | Yes / No | | |
| 5 | | | Yes / No | | |

---

## Step 2: Identify Threats and Vulnerabilities

### 2.1 Threat Catalogue

For each threat below, indicate whether it is applicable to your environment and record any organization-specific notes:

**Category A: Environmental and Physical Threats**

| # | Threat | Applicable? | Notes |
|---|--------|-------------|-------|
| T-01 | Natural disaster (earthquake, flood, tornado, hurricane) affecting data center or office | Yes / No / Partial | |
| T-02 | Fire or smoke damage to physical infrastructure | Yes / No / Partial | |
| T-03 | Power failure or extended power outage | Yes / No / Partial | |
| T-04 | Hardware failure (server, storage, network equipment) | Yes / No / Partial | |
| T-05 | HVAC failure leading to equipment overheating | Yes / No / Partial | |
| T-06 | Theft of physical devices containing ePHI (laptops, USB drives, servers) | Yes / No / Partial | |

**Category B: Human Threats — Unintentional**

| # | Threat | Applicable? | Notes |
|---|--------|-------------|-------|
| T-07 | Accidental deletion or modification of ePHI by authorized user | Yes / No / Partial | |
| T-08 | Misconfigured cloud storage bucket or database exposing ePHI publicly | Yes / No / Partial | |
| T-09 | ePHI sent to wrong recipient via email or fax | Yes / No / Partial | |
| T-10 | Unauthorized access resulting from shared credentials | Yes / No / Partial | |
| T-11 | Loss of laptop or mobile device containing ePHI | Yes / No / Partial | |
| T-12 | Failure to properly dispose of ePHI (paper records, decommissioned devices) | Yes / No / Partial | |
| T-13 | Employee accessing more ePHI than necessary (excess privilege) | Yes / No / Partial | |

**Category C: Human Threats — Intentional (Insider)**

| # | Threat | Applicable? | Notes |
|---|--------|-------------|-------|
| T-14 | Insider data theft — current employee exfiltrating ePHI for personal gain | Yes / No / Partial | |
| T-15 | Insider sabotage — disgruntled employee deleting or corrupting ePHI | Yes / No / Partial | |
| T-16 | Unauthorized access to ePHI by employee outside their role (snooping) | Yes / No / Partial | |
| T-17 | Contractor or vendor misusing access to ePHI | Yes / No / Partial | |

**Category D: External Threat Actors**

| # | Threat | Applicable? | Notes |
|---|--------|-------------|-------|
| T-18 | Ransomware attack encrypting ePHI and demanding payment | Yes / No / Partial | |
| T-19 | Phishing attack resulting in credential theft and unauthorized ePHI access | Yes / No / Partial | |
| T-20 | SQL injection or API attack exploiting application vulnerability to access ePHI | Yes / No / Partial | |
| T-21 | External brute-force attack against authentication systems | Yes / No / Partial | |
| T-22 | Supply chain attack via compromised vendor or software dependency | Yes / No / Partial | |
| T-23 | Distributed Denial of Service (DDoS) attack affecting ePHI system availability | Yes / No / Partial | |
| T-24 | Social engineering attack targeting employees to gain ePHI access | Yes / No / Partial | |
| T-25 | Exploitation of unpatched vulnerability in internet-facing systems | Yes / No / Partial | |
| T-26 | Man-in-the-middle attack intercepting ePHI in transit | Yes / No / Partial | |
| T-27 | Account takeover via credential stuffing or password spraying | Yes / No / Partial | |

**Category E: Technology and Process Threats**

| # | Threat | Applicable? | Notes |
|---|--------|-------------|-------|
| T-28 | Software bug or defect resulting in unauthorized ePHI exposure | Yes / No / Partial | |
| T-29 | Inadequate audit logging preventing detection of unauthorized access | Yes / No / Partial | |
| T-30 | Third-party subprocessor breach affecting ePHI entrusted to them | Yes / No / Partial | |

---

## Step 3: Assess Current Controls

For each HIPAA Security Rule safeguard category, assess your current control implementation:

### 3.1 Administrative Safeguards Assessment

| Safeguard | Regulation Reference | Implementation Status | Evidence Available | Gaps Identified |
|-----------|---------------------|----------------------|-------------------|----------------|
| Security Management Process — Risk Analysis | §164.308(a)(1)(ii)(A) | ☐ Implemented ☐ Partial ☐ None | | |
| Security Management Process — Risk Management | §164.308(a)(1)(ii)(B) | ☐ Implemented ☐ Partial ☐ None | | |
| Security Management Process — Sanction Policy | §164.308(a)(1)(ii)(C) | ☐ Implemented ☐ Partial ☐ None | | |
| Security Management Process — Information System Activity Review | §164.308(a)(1)(ii)(D) | ☐ Implemented ☐ Partial ☐ None | | |
| Assigned Security Responsibility | §164.308(a)(2) | ☐ Implemented ☐ Partial ☐ None | | |
| Workforce Security — Authorization and Supervision | §164.308(a)(3)(ii)(A) | ☐ Implemented ☐ Partial ☐ None | | |
| Workforce Security — Workforce Clearance Procedures | §164.308(a)(3)(ii)(B) | ☐ Implemented ☐ Partial ☐ None | | |
| Workforce Security — Termination Procedures | §164.308(a)(3)(ii)(C) | ☐ Implemented ☐ Partial ☐ None | | |
| Information Access Management — Access Authorization | §164.308(a)(4)(ii)(B) | ☐ Implemented ☐ Partial ☐ None | | |
| Information Access Management — Access Establishment and Modification | §164.308(a)(4)(ii)(C) | ☐ Implemented ☐ Partial ☐ None | | |
| Security Awareness and Training | §164.308(a)(5) | ☐ Implemented ☐ Partial ☐ None | | |
| Security Incident Procedures — Response and Reporting | §164.308(a)(6)(ii) | ☐ Implemented ☐ Partial ☐ None | | |
| Contingency Plan — Data Backup Plan | §164.308(a)(7)(ii)(A) | ☐ Implemented ☐ Partial ☐ None | | |
| Contingency Plan — Disaster Recovery Plan | §164.308(a)(7)(ii)(B) | ☐ Implemented ☐ Partial ☐ None | | |
| Contingency Plan — Emergency Mode Operation Plan | §164.308(a)(7)(ii)(C) | ☐ Implemented ☐ Partial ☐ None | | |
| Contingency Plan — Testing and Revision | §164.308(a)(7)(ii)(D) | ☐ Implemented ☐ Partial ☐ None | | |
| Business Associate Contracts and Other Arrangements | §164.308(b) | ☐ Implemented ☐ Partial ☐ None | | |

### 3.2 Physical Safeguards Assessment

| Safeguard | Regulation Reference | Implementation Status | Evidence Available | Gaps Identified |
|-----------|---------------------|----------------------|-------------------|----------------|
| Facility Access Controls — Contingency Operations | §164.310(a)(2)(i) | ☐ Implemented ☐ Partial ☐ None | | |
| Facility Access Controls — Facility Security Plan | §164.310(a)(2)(ii) | ☐ Implemented ☐ Partial ☐ None | | |
| Facility Access Controls — Access Control and Validation | §164.310(a)(2)(iii) | ☐ Implemented ☐ Partial ☐ None | | |
| Facility Access Controls — Maintenance Records | §164.310(a)(2)(iv) | ☐ Implemented ☐ Partial ☐ None | | |
| Workstation Use Policy | §164.310(b) | ☐ Implemented ☐ Partial ☐ None | | |
| Workstation Security (Physical) | §164.310(c) | ☐ Implemented ☐ Partial ☐ None | | |
| Device and Media Controls — Disposal | §164.310(d)(2)(i) | ☐ Implemented ☐ Partial ☐ None | | |
| Device and Media Controls — Media Re-use | §164.310(d)(2)(ii) | ☐ Implemented ☐ Partial ☐ None | | |
| Device and Media Controls — Accountability | §164.310(d)(2)(iii) | ☐ Implemented ☐ Partial ☐ None | | |
| Device and Media Controls — Data Backup and Storage | §164.310(d)(2)(iv) | ☐ Implemented ☐ Partial ☐ None | | |

### 3.3 Technical Safeguards Assessment

| Safeguard | Regulation Reference | Implementation Status | Evidence Available | Gaps Identified |
|-----------|---------------------|----------------------|-------------------|----------------|
| Access Control — Unique User Identification | §164.312(a)(2)(i) | ☐ Implemented ☐ Partial ☐ None | | |
| Access Control — Emergency Access Procedure | §164.312(a)(2)(ii) | ☐ Implemented ☐ Partial ☐ None | | |
| Access Control — Automatic Logoff | §164.312(a)(2)(iii) | ☐ Implemented ☐ Partial ☐ None | | |
| Access Control — Encryption and Decryption | §164.312(a)(2)(iv) | ☐ Implemented ☐ Partial ☐ None | | |
| Audit Controls | §164.312(b) | ☐ Implemented ☐ Partial ☐ None | | |
| Integrity — Authentication Mechanisms (ePHI) | §164.312(c)(2) | ☐ Implemented ☐ Partial ☐ None | | |
| Person or Entity Authentication | §164.312(d) | ☐ Implemented ☐ Partial ☐ None | | |
| Transmission Security — Encryption | §164.312(e)(2)(ii) | ☐ Implemented ☐ Partial ☐ None | | |
| Transmission Security — Integrity Controls | §164.312(e)(2)(i) | ☐ Implemented ☐ Partial ☐ None | | |

---

## Step 4: Determine Likelihood and Impact

### 4.1 Risk Rating Definitions

**Likelihood Rating (Probability of Threat Exploiting Vulnerability):**

| Score | Label | Definition |
|-------|-------|-----------|
| 5 | Very High | Threat is almost certain to occur; active exploitation known or ongoing; control gaps are significant |
| 4 | High | Threat is likely; this type of attack is common in your industry; minor controls exist but insufficient |
| 3 | Medium | Threat could occur; some controls exist; not actively observed but plausible |
| 2 | Low | Threat is unlikely; strong controls in place; would require determined attacker |
| 1 | Very Low | Threat is very unlikely; robust controls; attack would be highly sophisticated and unlikely |

**Impact Rating (Severity of Harm if Threat Occurs):**

| Score | Label | Definition |
|-------|-------|-----------|
| 5 | Catastrophic | Mass ePHI exposure (10,000+ records); business-threatening penalties; irreparable reputational damage; criminal liability |
| 4 | Severe | Significant ePHI exposure (500–10,000 records); major regulatory penalties; serious reputational harm; potential litigation |
| 3 | Moderate | Moderate ePHI exposure (< 500 records); regulatory investigation likely; notable financial and reputational impact |
| 2 | Minor | Limited ePHI exposure; isolated incident; manageable regulatory and financial impact |
| 1 | Negligible | Minimal or no ePHI exposed; no regulatory notification required; minimal business impact |

### 4.2 Risk Score Matrix

**Risk Score = Likelihood × Impact**

|  | Impact 1 (Negligible) | Impact 2 (Minor) | Impact 3 (Moderate) | Impact 4 (Severe) | Impact 5 (Catastrophic) |
|--|----------------------|-----------------|--------------------|-----------------|-----------------------|
| **Likelihood 5 (Very High)** | 5 — Low | 10 — Medium | 15 — High | 20 — Critical | 25 — Critical |
| **Likelihood 4 (High)** | 4 — Low | 8 — Medium | 12 — High | 16 — Critical | 20 — Critical |
| **Likelihood 3 (Medium)** | 3 — Low | 6 — Medium | 9 — Medium | 12 — High | 15 — High |
| **Likelihood 2 (Low)** | 2 — Low | 4 — Low | 6 — Medium | 8 — Medium | 10 — Medium |
| **Likelihood 1 (Very Low)** | 1 — Low | 2 — Low | 3 — Low | 4 — Low | 5 — Low |

**Risk Level Definitions:**
- **Critical (17–25):** Immediate action required. Implement controls or accept risk with executive approval. Report to leadership.
- **High (10–16):** Remediation required within 30 days. Assign owner and track to completion.
- **Medium (5–9):** Remediation required within 90 days. Document in risk register.
- **Low (1–4):** Monitor. Address in next planning cycle or accept with documentation.

---

## Step 5: Risk Register

Use this table to document each identified risk. Complete one row per threat-vulnerability pairing.

### Risk Register Template

| Risk ID | System / Asset | Threat | Vulnerability | Current Control | Likelihood (1–5) | Impact (1–5) | Risk Score | Risk Level | Residual Risk | Remediation Plan | Owner | Due Date | Status |
|---------|---------------|--------|--------------|----------------|-----------------|-------------|-----------|-----------|--------------|-----------------|-------|---------|--------|
| R-001 | | | | | | | | | | | | | |
| R-002 | | | | | | | | | | | | | |
| R-003 | | | | | | | | | | | | | |
| R-004 | | | | | | | | | | | | | |
| R-005 | | | | | | | | | | | | | |
| R-006 | | | | | | | | | | | | | |
| R-007 | | | | | | | | | | | | | |
| R-008 | | | | | | | | | | | | | |
| R-009 | | | | | | | | | | | | | |
| R-010 | | | | | | | | | | | | | |
| R-011 | | | | | | | | | | | | | |
| R-012 | | | | | | | | | | | | | |
| R-013 | | | | | | | | | | | | | |
| R-014 | | | | | | | | | | | | | |
| R-015 | | | | | | | | | | | | | |
| R-016 | | | | | | | | | | | | | |
| R-017 | | | | | | | | | | | | | |
| R-018 | | | | | | | | | | | | | |
| R-019 | | | | | | | | | | | | | |
| R-020 | | | | | | | | | | | | | |

**Column Definitions:**
- **Risk ID:** Sequential identifier (R-001, R-002, etc.)
- **System / Asset:** The system, application, or data asset exposed to this risk
- **Threat:** The threat from the catalogue in Step 2 (reference T-## codes)
- **Vulnerability:** The weakness or gap being exploited by this threat
- **Current Control:** What controls currently exist to mitigate this risk (if any)
- **Likelihood:** Score 1–5 using the rating in Step 4
- **Impact:** Score 1–5 using the rating in Step 4
- **Risk Score:** Likelihood × Impact
- **Risk Level:** Critical / High / Medium / Low per the matrix
- **Residual Risk:** Expected risk level after remediation controls are implemented
- **Remediation Plan:** Specific action(s) to be taken, including technical and process controls
- **Owner:** Named individual responsible for remediation
- **Due Date:** Target completion date
- **Status:** Open / In Progress / Remediated / Accepted

---

## Step 6: Risk Treatment Plan

For each risk identified in the register, select and document one of four treatment strategies:

### 6.1 Risk Treatment Options

| Strategy | Definition | When to Use | HIPAA Acceptability |
|----------|-----------|-------------|-------------------|
| **Mitigate** | Implement controls to reduce the likelihood or impact of the risk | Where controls are technically and financially feasible | Primary approach; most risks should be mitigated |
| **Transfer** | Shift risk to a third party (insurance, vendor contractual liability) | For risks that cannot be fully mitigated internally | Acceptable as supplementary; does not eliminate the underlying compliance obligation |
| **Accept** | Formally accept the risk without additional controls | For Low risks, or where cost of mitigation exceeds benefit | Must be documented with executive approval; not appropriate for Critical risks |
| **Avoid** | Eliminate the activity or system that generates the risk | When a business activity creates unacceptable risk | Appropriate when a function is not essential to operations |

### 6.2 Risk Treatment Decision Log

| Risk ID | Risk Level | Treatment Decision | Rationale | Compensating Controls (if Accepted) | Approved By | Approval Date |
|---------|-----------|-------------------|-----------|-------------------------------------|------------|--------------|
| R-001 | | | | | | |
| R-002 | | | | | | |
| R-003 | | | | | | |
| R-004 | | | | | | |
| R-005 | | | | | | |
| R-006 | | | | | | |
| R-007 | | | | | | |
| R-008 | | | | | | |
| R-009 | | | | | | |
| R-010 | | | | | | |

**Important:** Under HIPAA, formal risk acceptance for High or Critical risks requires documented executive approval and should include compensating controls. OCR has penalized organizations for accepting risks without documentation.

### 6.3 Remediation Prioritization Summary

| Priority | Risk IDs | Control/Remediation Action | Timeline | Budget Estimate | Owner |
|---------|---------|--------------------------|---------|----------------|-------|
| Immediate (Critical) | | | Within 30 days | | |
| Short-Term (High) | | | Within 60 days | | |
| Medium-Term (Medium) | | | Within 90 days | | |
| Long-Term (Low) | | | Within 180 days | | |

---

## Step 7: Executive Summary Template

*Complete this section for leadership review and sign-off. This is the document that demonstrates HIPAA-required risk management to OCR.*

---

**HIPAA SECURITY RISK ASSESSMENT — EXECUTIVE SUMMARY**

**Organization:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Assessment Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Assessment Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Scope of Assessment:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**Assessment Scope Summary**

This risk assessment covered \[NUMBER\] systems and applications that create, receive, maintain, or transmit ePHI. The assessment identified \[NUMBER\] potential threats, assessed \[NUMBER\] vulnerabilities, and evaluated \[NUMBER\] current controls across administrative, physical, and technical safeguard categories.

**ePHI Volume Assessed:** Approximately \[NUMBER\] records across \[NUMBER\] systems.

---

**Risk Summary**

| Risk Level | Number of Risks Identified | Number Remediated | Number In Progress | Number Accepted |
|-----------|--------------------------|------------------|-------------------|----------------|
| Critical | | | | |
| High | | | | |
| Medium | | | | |
| Low | | | | |
| **Total** | | | | |

---

**Key Findings**

*List the top 5 highest-risk findings from the risk register:*

1. **\[Risk ID — Risk Description\]** — Risk Level: \_\_\_\_ | Remediation Timeline: \_\_\_\_ | Owner: \_\_\_\_
2. **\[Risk ID — Risk Description\]** — Risk Level: \_\_\_\_ | Remediation Timeline: \_\_\_\_ | Owner: \_\_\_\_
3. **\[Risk ID — Risk Description\]** — Risk Level: \_\_\_\_ | Remediation Timeline: \_\_\_\_ | Owner: \_\_\_\_
4. **\[Risk ID — Risk Description\]** — Risk Level: \_\_\_\_ | Remediation Timeline: \_\_\_\_ | Owner: \_\_\_\_
5. **\[Risk ID — Risk Description\]** — Risk Level: \_\_\_\_ | Remediation Timeline: \_\_\_\_ | Owner: \_\_\_\_

---

**Overall Risk Posture**

- [ ] **High Risk** — Critical gaps exist; immediate remediation required before handling additional ePHI
- [ ] **Moderate Risk** — Material gaps identified; remediation underway; ongoing monitoring required
- [ ] **Low Risk** — Controls are substantially implemented; ongoing maintenance and annual review required

---

**Recommended Immediate Actions**

1. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
2. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
3. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**Next Assessment Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Executive Approval:**

Signature: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_\_\_
Name / Title: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Scoring and Assessment Interpretation

### Calculating Your Overall HIPAA Security Posture Score

Count your responses from Step 3 (Current Controls Assessment):

| Safeguard Category | Total Controls | Implemented | Partial (×0.5) | Not Implemented |
|-------------------|---------------|-------------|----------------|----------------|
| Administrative Safeguards | 17 | | | |
| Physical Safeguards | 10 | | | |
| Technical Safeguards | 9 | | | |
| **Total** | **36** | | | |

**Adjusted Score:** (Number Implemented × 1) + (Number Partial × 0.5) = \_\_\_\_ / 36

---

### Score Interpretation

**28–36 (Strong Posture):**
Your HIPAA controls are substantially implemented. Focus on maintaining and documenting existing controls, closing remaining gaps, and ensuring annual reviews are conducted. You are likely ready for a HIPAA audit or HITRUST assessment engagement.

**18–27 (Developing Posture):**
You have implemented foundational controls but have material gaps that OCR would likely identify in an investigation. Prioritize your highest-risk items (Critical and High from the risk register) and document a remediation roadmap with executive sign-off.

**9–17 (Early Stage):**
Significant gaps exist across multiple safeguard categories. You should not expand ePHI handling until foundational controls are in place. Engage a HIPAA compliance specialist to build your control environment.

**0–8 (Pre-Compliance):**
Your organization is at significant legal and financial risk. OCR penalties range from $100 to $50,000 per violation category (up to $1.9 million per violation type per year). Immediate engagement with a HIPAA compliance team is strongly recommended.

---

## Ready to Close Your HIPAA Gaps?

Completing this risk assessment is the legally required first step. Closing the gaps — implementing the controls, documenting the evidence, and maintaining your HIPAA compliance program — is where healthcare SaaS companies most often fall short.

QuickTrust has helped healthcare SaaS companies, EHR platforms, telehealth vendors, and RCM companies achieve HIPAA compliance with:

- **HIPAA-compliant cloud architecture** — implemented in AWS, GCP, or Azure by our Security and DevOps engineers
- **Administrative safeguard documentation** — policies, procedures, training programs, BAA management
- **Technical control implementation** — encryption, access controls, audit logging, MFA, data segmentation
- **HITRUST CSF certification** — for clients requiring third-party validated HIPAA compliance
- **OCR audit preparation** — evidence organization, documentation review, investigation support

Our engineers implement the controls. Your team stays focused on your product.

**100% audit pass rate. Audit-ready in 6–10 weeks.**

**Book your free HIPAA readiness call:**
[trust.quickintell.com](https://trust.quickintell.com)

---

*This template is based on the HIPAA Security Rule (45 CFR Part 164, Subpart C) and HHS OCR guidance on conducting risk assessments. It is provided for informational and educational purposes. It does not constitute legal advice and should be reviewed by qualified HIPAA compliance counsel before use in a compliance program. QuickTrust is operated by GPT Innovations, Inc.*

---

## Related Reading

- [HIPAA Compliance for Healthcare SaaS: The Complete Guide](/blog/hipaa-compliance-healthcare-saas-guide)
- [HIPAA Security Rule Technical Safeguards: Implementation Guide](/blog/hipaa-security-rule-technical-safeguards)

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "HIPAA Security Risk Assessment Template: Step-by-Step for Healthcare SaaS Companies",
  "description": "Step-by-step HIPAA security risk assessment template for healthcare SaaS companies. Covers the legally required assessment per 45 CFR 164.308(a)(1) with threat identification, vulnerability analysis, and risk scoring.",
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
