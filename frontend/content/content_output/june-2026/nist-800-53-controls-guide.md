---
title: "NIST 800-53 Controls: The Complete Guide to All 20 Control Families (Rev. 5)"
meta_description: "Complete guide to all 20 NIST 800-53 Rev. 5 control families with SaaS priorities, SOC 2 and ISO 27001 mappings, and common audit findings."
target_keyword: "NIST 800-53 controls"
secondary_keywords: "NIST 800-53 Rev 5, NIST 800-53 control families, NIST security controls, NIST 800-53 SOC 2 mapping, NIST 800-53 ISO 27001, NIST compliance"
word_count_target: "1500"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# NIST 800-53 Controls: The Complete Guide to All 20 Control Families (Rev. 5)

NIST Special Publication 800-53 Revision 5 is the most comprehensive catalog of security and privacy controls available. With over 1,000 individual controls organized into 20 families, it serves as the foundation for federal information security programs and, increasingly, as the baseline that commercial organizations use to structure their own security programs.

Understanding NIST 800-53 matters for SaaS companies for a practical reason: the controls in this catalog are the source material for virtually every other compliance framework. SOC 2 trust services criteria, ISO 27001 Annex A controls, HIPAA security requirements, PCI DSS requirements, and CMMC controls all trace back to concepts defined in NIST 800-53. If you understand this catalog, you understand the building blocks of every major compliance framework.

This guide covers all 20 control families, identifies which are most relevant for SaaS companies, maps key controls to SOC 2 and ISO 27001, and highlights the implementation priorities and common audit findings that organizations encounter.

## Overview of the 20 Control Families

NIST 800-53 Rev. 5 organizes controls into 20 families. Each family addresses a distinct area of security or privacy. Here is a concise overview of every family, what it covers, and why it matters.

### 1. Access Control (AC)

**Controls:** 25 base controls with numerous enhancements

**Covers:** Account management, access enforcement, information flow enforcement, separation of duties, least privilege, unsuccessful logon attempts, system use notification, session controls, remote access, and wireless access.

**Why it matters for SaaS:** Access control is the single most scrutinized area in any compliance audit. Every framework requires documented access management processes, role-based access, MFA, and regular access reviews.

### 2. Awareness and Training (AT)

**Controls:** 6 base controls

**Covers:** Security awareness training, role-based security training, training records, and insider threat awareness.

**Why it matters for SaaS:** Every framework requires security awareness training for all personnel and specialized training for individuals with security responsibilities. Training completion records are standard audit evidence.

### 3. Audit and Accountability (AU)

**Controls:** 16 base controls

**Covers:** Audit event logging, content of audit records, audit storage capacity, audit log review and reporting, time stamps, protection of audit information, audit record generation, and cross-organizational auditing.

**Why it matters for SaaS:** Centralized logging and log review are foundational requirements. Auditors verify that critical events are logged, logs are protected from tampering, and someone reviews them.

### 4. Assessment, Authorization, and Monitoring (CA)

**Controls:** 9 base controls

**Covers:** Security and privacy assessments, system interconnections, plans of action and milestones, continuous monitoring, and penetration testing.

**Why it matters for SaaS:** This family governs how you evaluate and monitor the effectiveness of your own controls -- the meta-process that ensures your security program is working.

### 5. Configuration Management (CM)

**Controls:** 14 base controls

**Covers:** Baseline configurations, configuration change control, impact analysis, access restrictions for change, configuration settings, least functionality, information system component inventory, and software usage restrictions.

**Why it matters for SaaS:** Configuration management controls prevent unauthorized changes to production environments. In cloud-native SaaS environments, infrastructure-as-code practices map directly to these controls.

### 6. Contingency Planning (CP)

**Controls:** 13 base controls

**Covers:** Contingency planning, contingency training, contingency plan testing, system backup, system recovery and reconstitution, and alternate processing and storage sites.

**Why it matters for SaaS:** Business continuity and disaster recovery are audit requirements across all frameworks. Auditors verify that you have documented plans, test them regularly, and maintain backup and recovery capabilities.

### 7. Identification and Authentication (IA)

**Controls:** 12 base controls

**Covers:** User identification and authentication, device identification and authentication, authenticator management, authenticator feedback, cryptographic module authentication, and re-authentication.

**Why it matters for SaaS:** Identity is the new perimeter. MFA, SSO, strong password policies, and service account management are universally required controls.

### 8. Incident Response (IR)

**Controls:** 10 base controls

**Covers:** Incident response planning, training, testing, handling, monitoring, reporting, and information sharing.

**Why it matters for SaaS:** Every framework requires a documented incident response plan, regular testing (tabletop exercises at minimum), and defined communication procedures.

### 9. Maintenance (MA)

**Controls:** 7 base controls

**Covers:** System maintenance, maintenance tools, nonlocal maintenance, and maintenance personnel.

**Why it matters for SaaS:** More relevant for organizations with physical infrastructure. For cloud-native SaaS companies, these controls map to patch management and system update procedures.

### 10. Media Protection (MP)

**Controls:** 8 base controls

**Covers:** Media access, marking, storage, transport, sanitization, and use of removable media.

**Why it matters for SaaS:** While physical media controls are less relevant for cloud-native companies, data disposal and sanitization requirements remain important, especially for HIPAA and PCI DSS compliance.

### 11. Physical and Environmental Protection (PE)

**Controls:** 23 base controls. Covers physical access authorizations, visitor management, monitoring, fire protection, and environmental controls. Cloud-native SaaS companies inherit most physical controls from their cloud provider, but office environments still require visitor management and access control.

### 12. Planning (PL)

**Controls:** 11 base controls. Covers system security plans, rules of behavior, and information security architecture. The system security plan is the master document auditors review to understand your control environment.

### 13. Program Management (PM)

**Controls:** 32 base controls. Covers information security program governance, risk management strategy, enterprise architecture, and insider threat programs. These controls define the governance structure required by SOC 2 and ISO 27001.

### 14. Personnel Security (PS)

**Controls:** 9 base controls

**Covers:** Position risk designation, personnel screening, termination, transfer, access agreements, third-party personnel security, and sanctions.

**Why it matters for SaaS:** Background checks, onboarding security procedures, and termination access revocation are universally required controls.

### 15. Personally Identifiable Information Processing and Transparency (PT)

**Controls:** 8 base controls

**Covers:** Authority to process PII, privacy notice, consent, privacy impact assessment, data minimization, and PII quality management.

**Why it matters for SaaS:** Added in Rev. 5, this family addresses privacy requirements that map to GDPR, CCPA, and other privacy regulations.

### 16. Risk Assessment (RA)

**Controls:** 10 base controls

**Covers:** Risk assessment, vulnerability monitoring and scanning, risk response, and threat awareness.

**Why it matters for SaaS:** Regular risk assessments and vulnerability scanning are foundational requirements. Auditors verify that you maintain a risk register, assess risks regularly, and have a defined vulnerability management program.

### 17. System and Services Acquisition (SA)

**Controls:** 23 base controls

**Covers:** System development life cycle, acquisition process, system documentation, software usage restrictions, security and privacy engineering, developer security testing, supply chain risk management, and tamper resistance.

**Why it matters for SaaS:** Secure SDLC controls (code review, testing, change management) are core audit requirements. This family also covers supply chain risk management for software dependencies.

### 18. System and Communications Protection (SC)

**Controls:** 51 base controls

**Covers:** Application partitioning, information in shared resources, denial-of-service protection, boundary protection, transmission confidentiality and integrity, network disconnect, cryptographic key management, mobile code, VoIP, secure name resolution, and session authenticity.

**Why it matters for SaaS:** Encryption in transit and at rest, network segmentation, TLS configuration, and API security all map to controls in this family.

### 19. System and Information Integrity (SI)

**Controls:** 23 base controls

**Covers:** Flaw remediation, malicious code protection, security alerts and advisories, information management and retention, security function verification, software and information integrity, spam protection, and information input validation.

**Why it matters for SaaS:** Patch management, antimalware, vulnerability remediation SLAs, and input validation are common audit focus areas.

### 20. Supply Chain Risk Management (SR)

**Controls:** 12 base controls

**Covers:** Supply chain risk management plan, acquisition strategies, supply chain controls, supply chain assessments, component authenticity, and supplier reviews.

**Why it matters for SaaS:** Added in Rev. 5 as a standalone family. Reflects the growing importance of vendor and software supply chain risk management across all compliance frameworks.

## Which Families Matter Most for SaaS Companies

Not all 20 families carry equal weight for a typical SaaS company. Priority should go to:

**Tier 1 (Implement first):** Access Control (AC), Audit and Accountability (AU), Configuration Management (CM), Identification and Authentication (IA), System and Communications Protection (SC), System and Information Integrity (SI)

**Tier 2 (Implement next):** Risk Assessment (RA), Incident Response (IR), Awareness and Training (AT), Personnel Security (PS), System and Services Acquisition (SA)

**Tier 3 (Address based on requirements):** Contingency Planning (CP), Supply Chain Risk Management (SR), Planning (PL), Personally Identifiable Information Processing (PT)

**Often inherited from cloud providers:** Physical and Environmental Protection (PE), Media Protection (MP), Maintenance (MA)

## Mapping NIST 800-53 to SOC 2 and ISO 27001

NIST 800-53 is the Rosetta Stone of compliance frameworks. Understanding the mappings saves significant effort for organizations pursuing multiple certifications.

**SOC 2 mapping.** The AICPA Trust Services Criteria (TSC) map to NIST 800-53 controls. For example: CC6.1 (Logical and Physical Access Controls) maps to AC-1 through AC-25, IA-1 through IA-12, and PE-1 through PE-23. CC7.1 (System Monitoring) maps to AU-1 through AU-16 and SI-1 through SI-23.

**ISO 27001 mapping.** ISO 27001:2022 Annex A controls have documented mappings to NIST 800-53. For example: A.8.3 (Access Restriction) maps to AC-3 and AC-6. A.8.15 (Logging) maps to AU-2, AU-3, and AU-12.

The practical implication: if you implement controls using NIST 800-53 as your baseline, you will satisfy a substantial portion of SOC 2 and ISO 27001 requirements with minimal additional work.

## Common Audit Findings

Across frameworks that draw from NIST 800-53, these findings appear repeatedly:

- **Incomplete access reviews.** Access reviews are required but not conducted for all systems or not documented.
- **Weak password policies.** Password requirements do not meet minimum standards or MFA is not enforced for all critical systems.
- **Insufficient logging.** Critical events are not logged, logs are not retained for the required period, or nobody reviews them.
- **Missing vulnerability scanning.** Scanning is conducted but not for all assets, or remediation SLAs are not defined or followed.
- **Stale risk assessments.** The risk register has not been updated in over a year.
- **Undocumented change management.** Changes are deployed to production without documented approval or testing.

## How QuickTrust Uses NIST 800-53 as a Baseline

QuickTrust's platform uses NIST 800-53 as its foundational control catalog. When you select a target framework -- SOC 2, ISO 27001, HIPAA, PCI DSS, or CMMC -- the platform maps your controls to the relevant NIST 800-53 families, identifies gaps, and generates implementation tasks.

This approach means that when you pursue a second or third framework, the platform immediately identifies which controls are already satisfied. You implement once and certify across multiple frameworks, reducing duplicated effort by 40-60% for dual-framework programs.

QuickTrust's security engineers implement the technical controls in your environment -- access management, logging infrastructure, encryption, vulnerability scanning, and change management pipelines -- using NIST 800-53 as the reference standard. The result is a security program built on the most rigorous and comprehensive control catalog available, mapped to whichever frameworks your business requires.

QuickTrust makes that foundation accessible to companies of every size, with the engineering support to turn a control catalog into a certified security program.
