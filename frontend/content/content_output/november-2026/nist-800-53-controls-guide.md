---
meta_description: "Complete guide to NIST 800-53 security controls (Rev. 5). Learn all 20 control families, how they map to SOC 2 and ISO 27001, and which controls apply to your organization."
target_keyword: "nist 800-53"
secondary_keywords: "nist 800-53 controls, nist 800-53 rev 5, nist sp 800-53, nist 800-53 control families, nist 800-53 compliance"
word_count_target: 5000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-19
---

# NIST 800-53 Controls: The Complete Guide to All 20 Control Families (Rev. 5)

No single publication has shaped information security practice in the United States more than NIST Special Publication 800-53. Originally written for federal agencies, this catalog of security and privacy controls has become the reference baseline for any organization that takes security seriously -- including thousands of private companies that are under no legal obligation to follow it.

The document is massive. Revision 5, published in September 2020 and updated through 2024, contains over 1,000 individual controls and control enhancements organized across 20 families. It covers everything from password policy and access control to supply chain risk management and privacy engineering. For organizations navigating federal compliance requirements -- or for private companies that simply want the most rigorous control framework available -- NIST 800-53 is the definitive source.

But the sheer scope of 800-53 creates a real problem: where do you start? Which controls actually apply to your organization? How do these controls relate to the SOC 2 audit your customers are requesting, or the ISO 27001 certification your European buyers require?

This guide answers those questions. We will walk through every control family in Revision 5, explain the baseline system (Low, Moderate, High), show exactly how NIST 800-53 maps to other frameworks you are likely pursuing, and clarify who must comply versus who voluntarily adopts this standard. Whether you are a federal contractor facing FISMA requirements, a cloud service provider pursuing FedRAMP authorization, or a private-sector security leader building a world-class control environment, this is the reference you need.

---

## What Is NIST SP 800-53?

NIST SP 800-53, formally titled *Security and Privacy Controls for Information Systems and Organizations*, is a publication from the National Institute of Standards and Technology (NIST), a non-regulatory agency within the U.S. Department of Commerce. It provides a comprehensive catalog of security and privacy controls that organizations can use to protect their information systems, the data those systems process, and the individuals whose information is at stake.

### A Brief History

The origins of NIST 800-53 trace back to the Federal Information Security Management Act (FISMA) of 2002, which mandated that federal agencies develop, document, and implement information security programs. NIST was tasked with developing the standards and guidelines that agencies would use to meet those requirements. The first edition of SP 800-53 was published in **February 2005**.

Since then, the publication has undergone five major revisions:

- **Revision 1 (2006):** Added supplemental guidance and refinements based on early adoption feedback.
- **Revision 2 (2007):** Updated control baselines and expanded guidance for specific system environments.
- **Revision 3 (2009):** Major overhaul that introduced the three-tier risk management approach and expanded the control catalog significantly.
- **Revision 4 (2013):** Added controls for mobile devices, cloud computing, insider threats, application security, and supply chain. This was the version most organizations used for over seven years.
- **Revision 5 (2020):** The most significant rewrite in the publication's history. Integrated privacy controls, added two entirely new control families (PT and SR), adopted outcome-based language, and decoupled the controls from any specific type of organization -- making the catalog usable by federal agencies, private companies, and international organizations alike.

### Purpose and Scope

NIST 800-53 serves three primary purposes:

1. **Provide a catalog of controls.** The publication contains a comprehensive, standardized set of security and privacy controls that organizations select from based on their risk profile. It is not a checklist -- it is a menu. Organizations choose the controls that are relevant to their systems, data sensitivity, and threat environment.

2. **Establish baselines for federal systems.** NIST 800-53 defines three control baselines -- Low, Moderate, and High -- that correspond to the potential impact of a security breach. Federal agencies are required to implement the controls in the baseline that matches the categorization of their information systems.

3. **Enable framework mapping.** Because 800-53 is the most granular control catalog available, it serves as the foundational layer that other frameworks map to. NIST itself publishes crosswalks between 800-53 and the NIST Cybersecurity Framework (CSF), ISO 27001, and other standards. This makes 800-53 the Rosetta Stone of security controls.

### Who Must Comply?

Compliance with NIST 800-53 is mandatory for:

- **Federal agencies** under FISMA (updated by FISMA 2014 and subsequent legislation)
- **Federal contractors and subcontractors** that process, store, or transmit federal information on behalf of agencies
- **Cloud service providers** seeking FedRAMP authorization (FedRAMP baselines are derived directly from NIST 800-53 Moderate and High baselines)
- **Defense contractors** subject to DFARS and CMMC requirements (CMMC maps extensively to NIST 800-171, which is itself derived from NIST 800-53 Moderate)

For private companies, compliance is voluntary -- but increasingly common, as we discuss later in this guide.

---

## NIST 800-53 Rev. 5: What Changed

Revision 5, released in September 2020, was not an incremental update. It was a fundamental rethinking of how the control catalog should be structured and used. If your organization is still operating against Revision 4 controls, you need to understand what changed and why.

### 1. Privacy Controls Fully Integrated

In Revision 4, privacy controls existed in a separate appendix (Appendix J). They were treated as supplementary -- bolted on rather than woven into the fabric of the catalog. Revision 5 eliminated this separation entirely. Privacy controls are now integrated throughout the catalog, and a new control family -- **PT: PII Processing and Transparency** -- was created to address privacy-specific requirements that did not fit cleanly into existing families.

This change reflects a fundamental shift in thinking: security and privacy are not separate disciplines that happen to share some overlapping concerns. They are interdependent. An access control failure is both a security incident and a privacy incident. A data retention policy is both a security control and a privacy control. Revision 5 treats them accordingly.

### 2. New Control Family: Supply Chain Risk Management (SR)

The SolarWinds attack, Kaseya breach, and a growing list of supply chain compromises made it clear that organizations needed explicit controls for managing risks introduced by third-party products, services, and components. Revision 5 added the **SR: Supply Chain Risk Management** family with controls covering:

- Supply chain risk management plans and policies
- Acquisition strategies that account for supply chain risk
- Component authenticity and provenance
- Supply chain intelligence and monitoring
- Supplier assessments and due diligence

### 3. Outcome-Based Language

Revision 4 controls were often prescriptive -- they told organizations *what to do* in specific terms. Revision 5 shifted to outcome-based language, describing the *security or privacy outcome* that a control is designed to achieve, without prescribing the specific method. This makes the controls technology-agnostic and adaptable to different organizational contexts.

For example, rather than prescribing a specific authentication mechanism, Revision 5 describes the outcome of ensuring that users and devices are authenticated before being granted access, leaving the implementation approach to the organization.

### 4. Decoupled from Federal-Only Use

Revision 4 was explicitly written for "federal information systems and organizations." Revision 5 changed the title to "Security and Privacy Controls for Information Systems and Organizations" -- dropping the word "federal." The controls are now written to be applicable to any organization, regardless of sector. This was a deliberate effort to make the catalog useful for critical infrastructure operators, private-sector companies, and international organizations.

### 5. Control Baselines Moved to a Separate Publication

In Revision 4, the control baselines (Low, Moderate, High) were embedded within the 800-53 document itself. Revision 5 moved baselines to a companion publication: **NIST SP 800-53B**. This separation allows the control catalog to be updated independently of the baselines, and vice versa, providing greater flexibility for both.

### 6. New and Consolidated Controls

Revision 5 added new controls (bringing the total to over 1,000 controls and enhancements), withdrew some that were obsolete, and consolidated others that overlapped. The result is a more coherent catalog, though the increase in total controls means that the publication is denser than ever.

---

## All 20 Control Families Explained

NIST 800-53 Rev. 5 organizes its controls into 20 families, each identified by a two-letter code. Each family contains a set of base controls and optional control enhancements that provide additional specificity. Below is a comprehensive description of each family, what it covers, and why it matters.

### AC: Access Control

**Number of base controls:** 25

Access Control is the largest and most frequently cited control family in NIST 800-53. It governs who can access your information systems, what they can do once they have access, and how that access is managed throughout its lifecycle.

Key controls include account management (AC-2), which requires organizations to define, create, enable, modify, disable, and remove accounts in accordance with policy; access enforcement (AC-3), which requires systems to enforce approved authorizations; and least privilege (AC-6), which requires that users and processes operate with only the minimum permissions necessary.

The AC family also covers remote access (AC-17), wireless access (AC-18), access control for mobile devices (AC-19), and session management controls including session lock (AC-11) and session termination (AC-12). For cloud-native organizations, the controls around information flow enforcement (AC-4) and separation of duties (AC-5) are particularly critical.

### AT: Awareness and Training

**Number of base controls:** 6

The AT family ensures that all personnel -- employees, contractors, and third parties -- understand their security and privacy responsibilities and have the knowledge and skills to fulfill them. Controls cover security awareness training (AT-2), role-based training (AT-3), and training records (AT-4).

While six controls may seem modest, the enhancements are substantial. AT-2 alone has eight enhancements covering topics like insider threat awareness, social engineering training, suspicious communications reporting, and advanced persistent threat awareness. Organizations often underestimate the implementation effort required for this family because the control count is low, but the scope of the training program can be extensive.

### AU: Audit and Accountability

**Number of base controls:** 16

Audit and Accountability controls ensure that your organization can track, record, and analyze system activity. If something goes wrong -- a breach, an unauthorized access, an operational failure -- you need an audit trail that tells you what happened, who did it, when, and from where.

Core controls include audit event definition (AU-2), content of audit records (AU-3), audit storage capacity (AU-4), response to audit logging failures (AU-5), and audit record review and reporting (AU-6). The family also covers timestamp accuracy (AU-8), protection of audit information (AU-9), and audit record generation (AU-12).

For organizations subject to FedRAMP, the AU family receives particularly intense scrutiny. Cloud environments generate massive volumes of audit data, and assessors will verify that you are capturing the right events, protecting the integrity of audit logs, and reviewing them on a defined schedule.

### CA: Assessment, Authorization, and Monitoring

**Number of base controls:** 9

The CA family governs how organizations assess their security controls, authorize systems to operate, and monitor those systems on an ongoing basis. This is the family that operationalizes risk management -- it turns the theoretical risk assessment process into concrete assessment activities.

Key controls include control assessments (CA-2), which require organizations to periodically assess their security controls; system authorization (CA-6), which requires a senior official to formally authorize a system to operate based on assessed risk; and continuous monitoring (CA-7), which requires organizations to develop and implement a strategy for ongoing monitoring of control effectiveness.

The CA family also covers penetration testing (CA-8) and internal system connections (CA-9), both of which are high-priority controls in environments where systems interconnect.

### CM: Configuration Management

**Number of base controls:** 14

Configuration Management controls ensure that your systems are configured securely and that changes to those configurations are managed, tracked, and approved. This family is foundational for operational security -- most breaches exploit misconfigurations, not zero-day vulnerabilities.

Controls cover baseline configuration (CM-2), which requires organizations to develop, document, and maintain a current baseline configuration for each system; configuration change control (CM-3), which requires a formal change management process; and least functionality (CM-7), which requires that systems be configured to provide only essential capabilities, with all unnecessary functions, ports, protocols, and services disabled.

The CM family also addresses configuration settings (CM-6), software usage restrictions (CM-10), and user-installed software (CM-11). For organizations running cloud infrastructure, CM-2 and CM-6 are typically operationalized through infrastructure-as-code and automated configuration scanning.

### CP: Contingency Planning

**Number of base controls:** 13

Contingency Planning controls ensure that your organization can continue critical operations during and after a disruption -- whether that disruption is a natural disaster, a cyberattack, an infrastructure failure, or a pandemic. This family is the backbone of business continuity and disaster recovery.

Core controls include contingency plan development (CP-2), contingency training (CP-3), contingency plan testing (CP-4), system backup (CP-9), and system recovery and reconstitution (CP-10). The family also covers alternate storage sites (CP-6), alternate processing sites (CP-7), and telecommunications services (CP-8) for organizations that require geographic redundancy.

Organizations frequently underinvest in CP controls because their value is not apparent until a disaster strikes. Auditors will look for documented plans that have been tested within the required timeframes, not just plans that exist on paper.

### IA: Identification and Authentication

**Number of base controls:** 12

The IA family ensures that users, devices, and services are properly identified and authenticated before they are granted access to systems and data. This family works in tandem with AC (Access Control) -- IA verifies who or what is requesting access, and AC determines what that entity is allowed to do.

Key controls include identification and authentication of organizational users (IA-2), device identification and authentication (IA-3), identifier management (IA-4), authenticator management (IA-5), and re-authentication (IA-11). IA-2 has a particularly rich set of enhancements covering multi-factor authentication for privileged and non-privileged accounts, network access, and local access.

With the industry-wide push toward zero trust architectures, the IA family has become even more critical. Identity is the new perimeter, and these controls define how that perimeter is secured.

### IR: Incident Response

**Number of base controls:** 10

Incident Response controls ensure that your organization can detect, analyze, contain, eradicate, and recover from security incidents. This family defines the full incident lifecycle, from preparation to post-incident activity.

Core controls include incident response training (IR-2), incident response testing (IR-3), incident handling (IR-4), incident monitoring (IR-5), and incident reporting (IR-6). The family also covers incident response assistance (IR-7) and incident response plan (IR-8), which requires organizations to develop and maintain a documented incident response plan that addresses roles, responsibilities, and communication procedures.

IR-4 (Incident Handling) and its enhancements are particularly detailed, covering automated incident handling processes, correlation of security events, and integration with the organization's contingency plan. For organizations that have experienced a breach, the IR family is often the first area where auditors identify gaps.

### MA: Maintenance

**Number of base controls:** 7

The Maintenance family covers the maintenance of information systems, including both routine and non-routine maintenance activities. While it may seem straightforward, these controls address critical security risks that arise when systems are opened up for maintenance -- particularly when that maintenance is performed remotely or by third parties.

Key controls include controlled maintenance (MA-2), maintenance tools (MA-3), nonlocal maintenance (MA-4), and maintenance personnel (MA-5). The enhancements to MA-4 are particularly important for modern organizations, as they address automated maintenance activities, session termination, and the use of cryptographic protections during remote maintenance sessions.

### MP: Media Protection

**Number of base controls:** 8

Media Protection controls govern how your organization handles system media -- any physical or digital medium that stores information. This includes hard drives, USB devices, backup tapes, optical media, and removable storage.

Controls cover media access (MP-2), media marking (MP-3), media storage (MP-4), media transport (MP-5), media sanitization (MP-6), and media use restrictions (MP-7). MP-6 (Media Sanitization) receives significant auditor attention because improper disposal of media is one of the most common causes of data breaches in the physical domain.

For cloud-native organizations with minimal physical infrastructure, many MP controls are inherited from the cloud service provider. However, you are still responsible for demonstrating that the CSP's media protection controls meet the required baseline -- and for addressing any media that your organization handles directly (employee laptops, external drives, etc.).

### PE: Physical and Environmental Protection

**Number of base controls:** 23

The PE family is one of the largest in the catalog and covers physical access to facilities, environmental protections (fire, flood, temperature, humidity), and the physical infrastructure that supports your information systems.

Key controls include physical access authorizations (PE-2), physical access control (PE-3), monitoring physical access (PE-6), visitor management (PE-8), emergency shutoff (PE-10), emergency power (PE-11), emergency lighting (PE-12), fire protection (PE-13), and temperature and humidity controls (PE-14).

For organizations that operate their own data centers, the PE family is extensive and demanding. For cloud-first organizations, the majority of PE controls are inherited from the infrastructure provider (AWS, Azure, GCP), but you must still address physical security for your offices, any on-premise equipment, and endpoint devices.

### PL: Planning

**Number of base controls:** 11

The Planning family addresses the development and maintenance of security and privacy plans for organizational information systems. These are not project plans -- they are formal documents that describe the security controls in place, the system boundaries, the data flows, and the rationale for control selection.

Key controls include system security and privacy plans (PL-2), rules of behavior (PL-4), and information security and privacy architectures (PL-8). PL-2 is foundational: it requires organizations to develop a system security plan (SSP) that describes the system boundary, operating environment, interconnections, and the security controls applied. The SSP is the single most important document in any federal compliance program, and FedRAMP assessors will use it as the roadmap for their entire assessment.

### PM: Program Management

**Number of base controls:** 32

Program Management is the organizational-level family -- it addresses the enterprise-wide information security and privacy program rather than individual systems. PM controls are not allocated to specific system baselines (Low, Moderate, High) because they apply at the organizational level.

Key controls include the information security program plan (PM-1), senior information security officer (PM-2), information security and privacy resources (PM-3), plan of action and milestones (PM-4), risk management strategy (PM-9), and insider threat program (PM-12). The family also covers enterprise architecture (PM-7), critical infrastructure plan (PM-8), and threat awareness program (PM-16).

PM controls are frequently overlooked by organizations that focus narrowly on system-level compliance. But auditors evaluating the maturity of your security program will look at PM controls as indicators of whether your organization treats security as a strategic function or a check-the-box exercise.

### PS: Personnel Security

**Number of base controls:** 9

Personnel Security controls ensure that individuals who access your information systems are trustworthy and that appropriate security measures are in place throughout the employment lifecycle -- from pre-hire screening to separation.

Key controls include position risk designation (PS-2), personnel screening (PS-3), personnel termination (PS-4), personnel transfer (PS-5), access agreements (PS-6), and external personnel security (PS-7). PS-4 (Personnel Termination) is particularly important because it requires that system access be revoked immediately upon termination and that all organizational information and assets be returned.

The PS family works in conjunction with AC (Access Control) and IA (Identification and Authentication) to ensure that identity and access lifecycle management is governed end to end.

### PT: PII Processing and Transparency (New in Rev. 5)

**Number of base controls:** 8

The PT family is one of two entirely new families introduced in Revision 5. It addresses how organizations process personally identifiable information (PII) and how they provide transparency to individuals about that processing.

Key controls include authority to process personally identifiable information (PT-2), personally identifiable information processing purposes (PT-3), consent (PT-4), privacy notice (PT-5), and system of records notice (PT-6). These controls operationalize the privacy principles that were previously scattered across Appendix J in Revision 4.

For organizations subject to GDPR, CCPA, or other privacy regulations, the PT family provides a structured way to implement privacy-by-design principles within the NIST framework. The controls are complementary to -- not duplicative of -- privacy regulations, meaning you can use PT controls as the implementation mechanism for your regulatory obligations.

### RA: Risk Assessment

**Number of base controls:** 10

The Risk Assessment family requires organizations to identify, assess, and respond to risks to their information systems and data. This is the analytical foundation of the entire NIST risk management framework -- without effective risk assessment, control selection becomes arbitrary.

Key controls include security categorization (RA-2), risk assessment (RA-3), and vulnerability monitoring and scanning (RA-5). RA-2 is the starting point for all federal compliance: it requires organizations to categorize their information systems based on the potential impact of a breach (using FIPS 199 categories), which then determines which control baseline applies.

RA-3 (Risk Assessment) requires organizations to conduct formal risk assessments that identify threats, vulnerabilities, likelihood, and impact. The results of these assessments drive the selection and tailoring of controls from the 800-53 catalog.

RA-5 (Vulnerability Monitoring and Scanning) is the most operationally intensive control in this family, requiring regular vulnerability scanning, remediation tracking, and sharing of vulnerability information across the organization.

### SA: System and Services Acquisition

**Number of base controls:** 23

The SA family covers security requirements in the acquisition lifecycle -- ensuring that security is baked into systems from design through development, testing, deployment, and maintenance. This family is critical for organizations that build software, procure commercial products, or rely on third-party services.

Key controls include system development life cycle (SA-3), acquisition process (SA-4), system documentation (SA-5), security and privacy engineering principles (SA-8), and developer security and privacy architecture and design (SA-17). SA-4 is particularly detailed, with enhancements covering functional properties of security controls, security and privacy documentation requirements, and continuous monitoring requirements for acquired systems.

For software development organizations, SA-11 (Developer Testing and Evaluation) and its enhancements covering static analysis, dynamic analysis, penetration testing, and attack surface reviews are often the controls that drive the most engineering investment.

### SC: System and Communications Protection

**Number of base controls:** 51

SC is the most technically dense control family in the entire catalog. It covers the protection mechanisms applied to systems and communications, including boundary protection, cryptographic protections, network segmentation, denial-of-service protection, and secure communication channels.

Key controls include application partitioning (SC-2), information in shared system resources (SC-4), boundary protection (SC-7), transmission confidentiality and integrity (SC-8), cryptographic key establishment and management (SC-12), cryptographic protection (SC-13), and session authenticity (SC-23).

SC-7 (Boundary Protection) is arguably the most scrutinized control in FedRAMP assessments. It requires organizations to monitor and control communications at the external managed interfaces and at key internal boundaries. The enhancements to SC-7 address denial of service protection, fail-secure operation, boundary protection for telecommunications, and restricting inbound and outbound communications traffic.

For organizations building modern, microservices-based architectures, SC controls around network segmentation, API protection, and encryption in transit and at rest define the technical security requirements for the entire platform.

### SI: System and Information Integrity

**Number of base controls:** 23

System and Information Integrity controls ensure that your systems operate correctly, that flaws are identified and corrected, and that your organization can detect and respond to integrity violations. This family is where patching, malware protection, and security monitoring requirements live.

Key controls include flaw remediation (SI-2), malicious code protection (SI-3), security alerts and advisories (SI-5), software and firmware integrity verification (SI-7), information input validation (SI-10), and error handling (SI-11). SI-4 (System Monitoring) is one of the most extensive controls in the catalog, with enhancements covering system-wide intrusion detection, automated alerts, inbound and outbound communications traffic analysis, and host-based monitoring.

For organizations pursuing continuous compliance, SI-2 (Flaw Remediation) and SI-5 (Security Alerts and Advisories) are operational controls that require ongoing effort -- not one-time implementation. Auditors will look at patch management cadence, vulnerability remediation timelines, and whether your organization has a process for triaging and responding to published security advisories.

### SR: Supply Chain Risk Management (New in Rev. 5)

**Number of base controls:** 12

The SR family, added in Revision 5, addresses risks arising from the supply chain -- including the acquisition, development, integration, and maintenance of systems, components, and services from external providers. The addition of this family was driven by the recognition that modern organizations depend on complex, global supply chains that introduce risks well beyond the organization's direct control.

Key controls include supply chain risk management plan (SR-2), supply chain controls and processes (SR-3), acquisition strategies and tools (SR-5), supplier assessments and reviews (SR-6), supply chain operations security (SR-7), and component authenticity (SR-11).

The SR family is particularly relevant for organizations in critical infrastructure sectors, defense, and technology. After the SolarWinds and Log4j incidents demonstrated the cascading impact of supply chain compromises, auditors and regulators now expect mature supply chain risk management practices.

---

## NIST 800-53 Control Baselines: Low, Moderate, and High Impact

Not every organization needs to implement every control in the NIST 800-53 catalog. The baseline system, defined in NIST SP 800-53B, provides three predefined sets of controls calibrated to different impact levels.

### How Baselines Are Determined

The baseline selection process starts with **FIPS 199** (Standards for Security Categorization of Federal Information and Information Systems). Organizations categorize their information systems based on the potential impact of a compromise in three areas:

- **Confidentiality:** The unauthorized disclosure of information
- **Integrity:** The unauthorized modification or destruction of information
- **Availability:** The disruption of access to or use of information or a system

Each area is rated as Low, Moderate, or High. The overall system categorization is the **high-water mark** -- the highest impact level across the three areas. A system that is Low for confidentiality, Moderate for integrity, and Low for availability receives an overall Moderate categorization.

### Low Baseline

The Low baseline applies to systems where a breach would have a **limited adverse effect** on organizational operations, assets, or individuals. It includes approximately **131 controls and enhancements** and represents the minimum security posture for any federal information system.

Typical systems at this level include public-facing websites with no sensitive data, internal tools that process only non-sensitive information, and test/development environments that do not contain production data.

### Moderate Baseline

The Moderate baseline applies to systems where a breach would have a **serious adverse effect**. It includes approximately **325 controls and enhancements** and is the most commonly used baseline in federal environments. Roughly 80% of federal systems are categorized at the Moderate level.

This is also the baseline used for **FedRAMP Moderate authorization**, which most cloud service providers targeting the federal market must achieve. The Moderate baseline adds significant requirements around multi-factor authentication, audit log protection, incident response, configuration management, and contingency planning beyond what the Low baseline requires.

### High Baseline

The High baseline applies to systems where a breach would have a **severe or catastrophic adverse effect** -- potentially involving loss of life, massive financial loss, or significant damage to national security. It includes approximately **421 controls and enhancements** and represents the most rigorous control posture defined by NIST.

Systems at this level include classified information systems, critical infrastructure control systems, financial systems that process large-volume transactions, and systems that support emergency services. The High baseline adds requirements for advanced cryptographic protections, stringent personnel security, hardware-based security mechanisms, and extensive redundancy.

### Tailoring Baselines

Organizations are not required to implement the baseline controls exactly as defined. NIST 800-53B allows **tailoring** -- the process of modifying a baseline to account for organization-specific factors. Tailoring can include:

- **Scoping:** Removing controls that are not applicable (e.g., removing wireless access controls for a system that does not use wireless)
- **Compensating controls:** Substituting alternative controls that provide equivalent protection
- **Organization-defined parameters:** Filling in values for parameters that the controls leave to the organization (e.g., specifying the frequency of vulnerability scans)
- **Adding controls:** Selecting controls from a higher baseline or from outside the baseline when the risk assessment warrants it

The tailored set of controls is documented in the system security plan (SSP) and is the basis for the security assessment.

---

## NIST 800-53 vs. NIST CSF: How They Work Together

One of the most common sources of confusion in the security community is the relationship between NIST SP 800-53 and the NIST Cybersecurity Framework (CSF). They are related but serve fundamentally different purposes.

### NIST Cybersecurity Framework (CSF)

The [NIST CSF](/blog/nist-cybersecurity-framework-guide) is a **risk management framework** organized around five core functions: Identify, Protect, Detect, Respond, and Recover (updated to six functions in CSF 2.0 with the addition of Govern). It provides a high-level, strategic view of an organization's cybersecurity posture. The CSF does not prescribe specific controls -- it describes desired outcomes and categories of activity.

The CSF was designed for **voluntary adoption by critical infrastructure organizations** and has since been adopted across virtually every industry sector. It is intentionally high-level to be accessible to executives and board members.

### NIST 800-53

NIST 800-53 is a **control catalog** -- a detailed, granular set of specific security and privacy controls. Where the CSF says "you should manage access to assets," 800-53 tells you exactly how: implement multi-factor authentication (IA-2), enforce least privilege (AC-6), manage accounts through their lifecycle (AC-2), and so on.

### How They Complement Each Other

The relationship is hierarchical:

| Attribute | NIST CSF | NIST 800-53 |
|-----------|----------|-------------|
| **Level of detail** | Strategic | Tactical/Operational |
| **Audience** | Executives, board, risk managers | Security engineers, auditors, compliance teams |
| **Structure** | Functions > Categories > Subcategories | Families > Controls > Enhancements |
| **Mandatory?** | Voluntary (except for federal agencies under EO 13636 and subsequent directives) | Mandatory for federal systems under FISMA |
| **Purpose** | Assess and communicate cybersecurity posture | Implement specific security and privacy controls |

NIST itself publishes a mapping between CSF subcategories and 800-53 controls. A typical workflow is:

1. Use the **CSF** to assess your current cybersecurity posture and identify gaps at a strategic level.
2. For each gap, identify the corresponding **800-53 controls** that address the gap at the implementation level.
3. Use the 800-53 controls as the technical specification for what your engineering team builds and what your auditors assess.

Organizations that adopt the CSF without mapping to a control catalog like 800-53 often end up with high-level policies that lack operational specificity. Organizations that implement 800-53 controls without the CSF's strategic framework sometimes struggle to communicate their security posture to leadership. The combination of both provides strategic clarity and operational precision.

---

## NIST 800-53 vs. ISO 27001: Control Mapping

For organizations operating internationally -- or pursuing multiple certifications -- understanding how NIST 800-53 maps to [ISO 27001](/blog/what-is-iso-27001) is essential. Both frameworks aim to protect information, but they approach the problem differently.

### Structural Comparison

| Attribute | NIST 800-53 Rev. 5 | ISO 27001:2022 |
|-----------|---------------------|-----------------|
| **Origin** | U.S. Government (NIST) | International (ISO/IEC) |
| **Type** | Control catalog | Management system standard |
| **Number of controls** | 1,000+ (including enhancements) | 93 (Annex A) |
| **Organized by** | 20 control families | 4 themes (Organizational, People, Physical, Technological) |
| **Certifiable?** | No (assessed, not certified) | Yes (third-party certification) |
| **Baselines** | Low, Moderate, High | Risk-based (Statement of Applicability) |
| **Mandatory for** | U.S. federal agencies | Voluntary (but widely required by procurement) |
| **Privacy controls** | Integrated (PT family) | Limited (5.34 covers PII protection) |
| **Supply chain** | Dedicated family (SR) | 5.19-5.22 cover supplier relationships |

### Control Mapping

NIST publishes a detailed crosswalk between 800-53 and ISO 27001. The table below summarizes the mapping at the family level:

| NIST 800-53 Family | ISO 27001:2022 Controls |
|---------------------|------------------------|
| AC: Access Control | 5.15-5.18, 8.2-8.5 |
| AT: Awareness and Training | 6.3 |
| AU: Audit and Accountability | 8.15 |
| CA: Assessment and Monitoring | 5.35-5.36, 9.2-9.3 |
| CM: Configuration Management | 8.9, 8.19, 8.32 |
| CP: Contingency Planning | 5.29-5.30, 8.13-8.14 |
| IA: Identification and Authentication | 5.16-5.17, 8.5 |
| IR: Incident Response | 5.24-5.28 |
| MA: Maintenance | 7.13 (partial) |
| MP: Media Protection | 7.10, 7.14, 8.10 |
| PE: Physical and Environmental Protection | 7.1-7.14 |
| PL: Planning | 5.1, 5.8 (partial) |
| PM: Program Management | 5.1-5.4, Clauses 4-10 |
| PS: Personnel Security | 6.1-6.6 |
| PT: PII Processing and Transparency | 5.34 (limited mapping) |
| RA: Risk Assessment | Clause 6.1, 5.7, 8.8 |
| SA: System and Services Acquisition | 5.8, 5.19-5.23, 8.25-8.31 |
| SC: System and Communications Protection | 8.20-8.24, 8.26 |
| SI: System and Information Integrity | 8.7-8.8, 8.16 |
| SR: Supply Chain Risk Management | 5.19-5.22 |

### Key Differences

1. **Depth of controls.** NIST 800-53 is dramatically more granular. ISO 27001's Annex A control 5.15 (Access Control) maps to an entire NIST 800-53 family with 25 controls and dozens of enhancements. Organizations coming from ISO 27001 to NIST 800-53 will find that they need to decompose each ISO control into multiple, more specific controls.

2. **Management system vs. control catalog.** ISO 27001 requires an Information Security Management System (ISMS) with formal processes for risk assessment, management review, internal audit, and continual improvement. NIST 800-53 is a control catalog -- it does not prescribe a management system. Organizations implementing 800-53 typically use the NIST Risk Management Framework (RMF, defined in SP 800-37) as the management system layer.

3. **Certification vs. authorization.** ISO 27001 results in a certificate from an accredited certification body. NIST 800-53 compliance results in an Authorization to Operate (ATO) granted by an authorizing official. The processes, timelines, and governance structures are different.

4. **Privacy coverage.** NIST 800-53 Rev. 5 has far more extensive privacy controls than ISO 27001:2022, which addresses PII protection primarily through a single control (5.34) plus references to applicable privacy regulations.

For organizations pursuing both frameworks, the overlap is significant -- roughly 70-80% of ISO 27001 controls map directly to NIST 800-53 controls. Implementing NIST 800-53 Moderate will cover most of what ISO 27001 requires, with the main gap being the management system requirements (ISMS documentation, management review, internal audit) that ISO 27001 mandates and NIST 800-53 does not.

---

## NIST 800-53 vs. SOC 2: Which Controls Overlap?

[SOC 2](/blog/what-is-soc2) is the most common security attestation in the SaaS industry. Understanding how it relates to NIST 800-53 helps organizations that need both -- or that want to use one as a foundation for the other.

### How SOC 2 Trust Service Criteria Map to NIST 800-53

SOC 2's Trust Service Criteria (TSC) are organized around five principles: Security (Common Criteria), Availability, Processing Integrity, Confidentiality, and Privacy. The AICPA has published a mapping between the TSC and NIST 800-53 controls. Here is the high-level alignment:

| SOC 2 Trust Service Category | NIST 800-53 Families |
|------------------------------|---------------------|
| CC1: Control Environment | PM, PL, PS |
| CC2: Communication and Information | AT, PM, PL |
| CC3: Risk Assessment | RA, PM |
| CC4: Monitoring Activities | CA, AU, SI |
| CC5: Control Activities | AC, CM, SC |
| CC6: Logical and Physical Access | AC, IA, PE, MP |
| CC7: System Operations | AU, CP, IR, SI |
| CC8: Change Management | CM, SA |
| CC9: Risk Mitigation | PM, RA, SR |
| Availability (A1) | CP, SC |
| Processing Integrity (PI1) | SI, SC |
| Confidentiality (C1) | AC, SC, MP |
| Privacy (P1) | PT |

### Key Differences

1. **Scope and granularity.** SOC 2's Common Criteria contain approximately 33 points of focus across 9 categories. NIST 800-53 Moderate contains approximately 325 controls and enhancements. SOC 2 provides the "what" at a high level; NIST 800-53 provides the "how" at extreme detail.

2. **Flexibility.** SOC 2 gives organizations significant latitude in how they satisfy the criteria. Two companies with very different security architectures can both receive clean SOC 2 reports. NIST 800-53 is more prescriptive -- if the baseline calls for multi-factor authentication (IA-2), you must implement multi-factor authentication.

3. **Output.** SOC 2 results in an attestation report issued by a CPA firm. NIST 800-53 compliance results in an Authorization to Operate (ATO) or is validated through a Security Assessment Report (SAR). The audiences and use cases are different.

4. **Privacy.** SOC 2 has an optional Privacy Trust Service Category. NIST 800-53 integrates privacy controls throughout the catalog and includes the dedicated PT family. If privacy is a priority, NIST 800-53 provides more structured and comprehensive privacy controls.

### Using NIST 800-53 as a Foundation for SOC 2

Organizations that have already implemented NIST 800-53 controls will find that SOC 2 preparation is straightforward. The control overlap is extensive, and most SOC 2 criteria will be satisfied by existing 800-53 controls. The primary work will be:

- Mapping your 800-53 controls to SOC 2 criteria
- Ensuring audit evidence is organized in the format SOC 2 auditors expect
- Addressing the management system and governance elements that SOC 2 examines (tone at the top, risk assessment process, monitoring) if those are not already documented

Conversely, organizations starting from SOC 2 and moving to NIST 800-53 will find that their SOC 2 controls provide a foundation, but significant additional work is needed to meet the granularity and specificity that 800-53 requires. A [complete SOC 2 guide](/content/march-2026/pillar-soc2-complete-guide) can help you understand what your SOC 2 program already covers.

---

## Who Must Comply with NIST 800-53?

Mandatory compliance with NIST 800-53 applies to a well-defined set of organizations. Understanding whether your organization falls into this category -- and which specific requirements apply -- is critical for scoping your compliance program.

### Federal Agencies

All federal agencies are required to comply with NIST 800-53 under FISMA (Federal Information Security Modernization Act of 2014). This includes executive branch agencies, independent agencies, and government corporations. Agencies must categorize their information systems using FIPS 199, select the appropriate control baseline from SP 800-53B, implement the controls, assess them, and obtain an Authorization to Operate (ATO) from a designated authorizing official.

### FedRAMP Cloud Service Providers

Any cloud service provider (CSP) that wants to offer services to federal agencies must obtain FedRAMP (Federal Risk and Authorization Management Program) authorization. FedRAMP baselines are derived directly from NIST 800-53, with additional FedRAMP-specific requirements layered on top.

- **FedRAMP Low** is based on the NIST 800-53 Low baseline, with approximately 156 controls
- **FedRAMP Moderate** is based on the NIST 800-53 Moderate baseline, with approximately 325 controls
- **FedRAMP High** is based on the NIST 800-53 High baseline, with approximately 421 controls

Most federal agencies require Moderate authorization at minimum. Achieving [FedRAMP authorization](/content/september-2026/case-study-govtech-fedramp) is one of the most demanding compliance undertakings in the industry, typically requiring 9-18 months and a third-party assessment organization (3PAO).

### Defense Contractors (DFARS and CMMC)

Defense contractors who handle Controlled Unclassified Information (CUI) must comply with NIST SP 800-171, which is a subset of NIST 800-53 Moderate controls tailored for non-federal organizations. The Cybersecurity Maturity Model Certification (CMMC) program, which the Department of Defense is implementing, is built on NIST 800-171 requirements.

The mapping is direct: NIST 800-171 contains 110 security requirements derived from 800-53 Moderate. Contractors who already comply with 800-53 Moderate will find 800-171 compliance straightforward.

### State and Local Governments

While not mandated by federal law, many state governments have adopted NIST 800-53 or derivatives as their security standard. State agencies receiving federal grants or operating systems that process federal data may be required to implement NIST controls as a condition of funding.

### Critical Infrastructure Organizations

Executive Order 13636 (2013) and subsequent directives encourage critical infrastructure operators to adopt the NIST Cybersecurity Framework, which maps to NIST 800-53 controls. While compliance is not mandatory for most private critical infrastructure operators, regulatory agencies in specific sectors (energy, healthcare, financial services) increasingly reference NIST standards in their requirements.

---

## How Private Companies Use NIST 800-53

A growing number of private companies -- particularly in technology, financial services, and healthcare -- voluntarily adopt NIST 800-53 even though they are under no regulatory obligation to do so. Here is why, and how they do it.

### Why Private Companies Adopt NIST 800-53

**Selling to the federal government.** The most common driver. Any company targeting federal contracts needs FedRAMP or NIST 800-171 compliance, both of which are based on 800-53. Implementing 800-53 directly gives you the foundational control set that these programs require.

**Enterprise security maturity.** For companies that have outgrown SOC 2 or ISO 27001 and want a more granular, prescriptive control framework, 800-53 is the logical next step. It forces organizations to implement specific technical and operational controls rather than the higher-level requirements of SOC 2 or ISO 27001.

**Multi-framework efficiency.** Because NIST 800-53 is the most comprehensive control catalog available, organizations that implement it find that they have already satisfied the majority of controls required by SOC 2, ISO 27001, HIPAA, PCI DSS, and other frameworks. This "implement once, map to many" approach can be more efficient than pursuing each framework independently.

**Customer and partner requirements.** Large enterprises, particularly in financial services and healthcare, increasingly ask their vendors to demonstrate alignment with NIST standards. Even when a formal FedRAMP authorization is not required, demonstrating NIST 800-53 alignment can differentiate your company in competitive evaluations.

**Insurance and liability.** Cyber insurance providers increasingly reference NIST standards when evaluating an organization's security posture. Demonstrating alignment with NIST 800-53 controls can result in more favorable coverage terms and premiums.

### How Private Companies Implement 800-53

Private companies typically do not implement the full 800-53 catalog. Instead, they follow a practical approach:

1. **Select a baseline.** Most private companies start with the Moderate baseline, as it provides comprehensive coverage without the extreme rigor of the High baseline.

2. **Tailor the controls.** Using the tailoring guidance in SP 800-53B, remove controls that are not applicable (e.g., government-specific controls, physical security controls for organizations without data centers) and add controls specific to your industry or risk profile.

3. **Map to existing frameworks.** If you already have SOC 2 or ISO 27001, use the NIST crosswalks to identify which 800-53 controls you already satisfy and focus implementation effort on the gaps.

4. **Use automation.** The sheer volume of 800-53 controls makes manual compliance management impractical. Compliance automation platforms can map your existing controls to 800-53, identify gaps, and maintain continuous evidence collection. This is where QuickTrust's [multi-framework compliance capabilities](/content/july-2026/multi-framework-compliance-strategy) become critical -- the platform maps your control implementations across NIST 800-53, SOC 2, ISO 27001, and other frameworks simultaneously, eliminating redundant work.

5. **Engage a qualified assessor.** While private companies do not need an ATO, many engage third-party assessors to validate their 800-53 control implementations. This provides independent validation that carries weight with customers and partners.

---

## Frequently Asked Questions

### How many controls are in NIST 800-53 Rev. 5?

NIST 800-53 Rev. 5 contains over 1,000 individual controls and control enhancements across 20 control families. The exact number depends on how you count enhancements versus base controls. The base catalog contains approximately 322 base controls, with the remainder being enhancements that provide additional specificity and rigor.

### Is NIST 800-53 mandatory for private companies?

No. NIST 800-53 is mandatory only for federal agencies, federal contractors processing federal data, and cloud service providers seeking FedRAMP authorization. Private companies can voluntarily adopt NIST 800-53 as their security control framework, and many do -- particularly those selling to the federal government or seeking the most comprehensive control baseline available.

### What is the difference between NIST 800-53 and NIST 800-171?

NIST 800-171 (Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations) is a subset of NIST 800-53 Moderate controls tailored specifically for non-federal organizations that handle Controlled Unclassified Information (CUI). It contains 110 security requirements derived from 800-53. If you comply with NIST 800-53 Moderate, you will satisfy virtually all NIST 800-171 requirements.

### How long does it take to implement NIST 800-53?

Implementation timelines vary dramatically based on the baseline (Low, Moderate, High), your organization's current security maturity, and whether you have existing frameworks in place. As a general guide: organizations with an existing SOC 2 or ISO 27001 program can implement the incremental NIST 800-53 Moderate controls in 3-6 months. Organizations starting from scratch should plan for 9-18 months for a Moderate baseline implementation.

### How does NIST 800-53 relate to FedRAMP?

FedRAMP baselines are built directly on NIST 800-53 baselines. FedRAMP Low, Moderate, and High correspond to the NIST 800-53 Low, Moderate, and High baselines, with additional FedRAMP-specific requirements added on top. Any cloud service provider pursuing FedRAMP authorization must implement the corresponding NIST 800-53 controls.

### Can I use NIST 800-53 and ISO 27001 together?

Yes, and many organizations do. The frameworks are complementary. NIST 800-53 provides the granular control catalog, while ISO 27001 provides the management system framework (ISMS). Organizations often implement ISO 27001 as their management system and use NIST 800-53 controls as the detailed control specifications within that system. NIST publishes an official crosswalk mapping between the two standards.

### What changed between NIST 800-53 Rev. 4 and Rev. 5?

The most significant changes in Rev. 5 include: integration of privacy controls throughout the catalog (previously in a separate appendix), addition of two new control families (PT: PII Processing and Transparency, and SR: Supply Chain Risk Management), adoption of outcome-based language, removal of the "federal" designation to make the catalog applicable to any organization, and movement of control baselines to a separate publication (SP 800-53B).

### How do I know which NIST 800-53 baseline applies to my organization?

For federal agencies, the baseline is determined by the FIPS 199 security categorization of your information system. The categorization considers the potential impact of a breach on confidentiality, integrity, and availability. For private companies adopting NIST 800-53 voluntarily, the Moderate baseline is the most common starting point, as it provides comprehensive coverage without the extreme rigor of the High baseline. Your risk assessment should ultimately drive this decision.

---

## Getting Started with NIST 800-53

NIST 800-53 is the most comprehensive security and privacy control catalog available. Whether you are required to implement it or choosing to adopt it voluntarily, the depth and breadth of the framework can be overwhelming -- particularly for organizations managing compliance across multiple frameworks simultaneously.

The key to practical NIST 800-53 implementation is automation. With over 1,000 controls and enhancements, manual tracking through spreadsheets is not scalable. You need a system that maps your existing controls to the 800-53 catalog, identifies gaps against your target baseline, collects evidence continuously, and maintains your compliance posture as your systems evolve.

**QuickTrust maps NIST 800-53 controls automatically across your infrastructure.** The platform ingests your existing control implementations, maps them to NIST 800-53 families and baselines, identifies gaps in real time, and cross-references your controls against SOC 2, ISO 27001, FedRAMP, and other frameworks you may be pursuing. Instead of managing separate compliance programs for each framework, you manage one unified control environment -- and QuickTrust handles the mapping.

If your organization is evaluating NIST 800-53 -- whether for FedRAMP, defense contracts, or voluntary adoption -- [schedule a demo](https://quicktrustapp.com/demo) to see how QuickTrust turns the most demanding control catalog in information security into a manageable, automated compliance program.

---

*This guide is maintained by the QuickTrust Editorial team and updated as NIST publishes revisions to SP 800-53 and related publications. Last reviewed: March 2026.*
