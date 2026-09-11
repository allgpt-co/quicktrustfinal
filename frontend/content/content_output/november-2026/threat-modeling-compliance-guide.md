---
meta_description: "Master threat modeling for compliance and security. Learn STRIDE, PASTA, LINDDUN, and Attack Trees methodologies with step-by-step guides, examples, and integration into your SDLC."
target_keyword: "threat modeling"
secondary_keywords: "threat modeling methodology, STRIDE threat model, threat modeling framework, threat modeling for compliance, threat analysis"
word_count_target: 4500+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-21
---

# Threat Modeling: The Complete Guide to Identifying and Mitigating Security Threats Before They Become Breaches

The most expensive vulnerability is the one you discover after it has been exploited. The second most expensive is the one you discover during a penetration test, weeks before an audit, when there is no time to redesign the system that introduced it. The least expensive -- by orders of magnitude -- is the one you identify during design, before a single line of code has been written.

That is the fundamental value proposition of threat modeling. It moves security analysis upstream, into the design phase where changes are cheap, alternatives are plentiful, and the cost of a wrong decision is measured in whiteboard sessions rather than incident response hours.

Threat modeling is the systematic process of identifying what can go wrong in a system, how likely it is, and what you should do about it -- before you build it. It is not a scan, not an assessment performed after deployment, and not a checkbox exercise that produces a document nobody reads. Done correctly, threat modeling is the activity that connects your security architecture to the actual threats your system will face, and it produces the evidence that compliance auditors increasingly demand.

Every major compliance framework now expects threat modeling in some form. SOC 2, ISO 27001, NIST CSF, PCI DSS 4.0, and CMMC all include requirements that are difficult or impossible to satisfy without a structured approach to identifying threats during design and development. Organizations that treat security as something bolted on after deployment are finding that auditors no longer accept that approach.

This guide covers everything you need to build a threat modeling practice that strengthens your security posture and satisfies compliance requirements simultaneously: the core methodologies (STRIDE, PASTA, LINDDUN, Attack Trees), a step-by-step process for conducting threat models, integration into your SDLC and CI/CD pipeline, tooling recommendations, and the specific audit evidence each framework expects.

---

## What Is Threat Modeling?

Threat modeling is a structured, repeatable process for analyzing a system's architecture to identify potential security threats, evaluate their severity, and determine appropriate countermeasures. It produces a documented record of what threats exist, which components are affected, and what controls mitigate each threat.

### Definition

At its core, threat modeling answers four questions (formalized by Adam Shostack, who led the threat modeling practice at Microsoft):

1. What are we building?
2. What can go wrong?
3. What are we going to do about it?
4. Did we do a good job?

These four questions are deceptively simple. Answering them rigorously for a modern SaaS application -- with its APIs, microservices, third-party integrations, multi-tenant data stores, and cloud infrastructure -- requires a methodology, domain knowledge, and cross-functional collaboration between engineering, security, and product teams.

### Purpose

Threat modeling serves three distinct purposes:

- **Security improvement.** It identifies threats that automated tools cannot find. Scanners detect known vulnerability patterns in code and configuration. Threat modeling identifies architectural weaknesses, trust boundary violations, and design-level flaws that no scanner can evaluate.
- **Risk prioritization.** Not all threats are equal. Threat modeling produces a ranked list of risks that allows teams to allocate engineering resources to the threats with the highest actual impact, rather than chasing low-severity scan findings.
- **Compliance evidence.** A documented threat model demonstrates to auditors that your organization identifies threats proactively, considers security during design, and makes risk-informed decisions about controls. This is the evidence required by SOC 2 CC3.2, ISO 27001 Clause 6.1, NIST CSF ID.RA, and PCI DSS Requirement 6.3.

### When to Perform Threat Modeling

Threat modeling is not a one-time activity. It should occur:

- **During initial system design** -- before architecture decisions are finalized and code is written
- **When adding significant new features** -- any feature that introduces new data flows, trust boundaries, or external integrations
- **When changing architecture** -- migration to a new cloud provider, adoption of microservices, introduction of a new data store, or changes to authentication mechanisms
- **After a security incident** -- to determine whether the threat that was exploited was identifiable through threat modeling, and to update the model accordingly
- **Periodically** -- at least annually, to account for changes in the threat landscape, new attack techniques, and incremental system changes that were not individually significant enough to trigger a review

Organizations that perform threat modeling only during initial design and never revisit it are building a snapshot that becomes less accurate with every deployment. Auditors evaluate whether the threat model reflects the current state of the system.

---

## Why Compliance Frameworks Value Threat Modeling

Compliance frameworks have shifted from prescribing specific controls to requiring organizations to demonstrate risk-based decision-making. Threat modeling is the mechanism through which you connect identified threats to the controls you implement. Without it, your control selection is either arbitrary or based on a generic checklist -- neither of which satisfies modern auditors.

### SOC 2 -- Common Criteria CC3.2

SOC 2 Trust Services Criteria CC3.2 requires organizations to "identify risks to the achievement of its objectives" and to consider "the potential for fraud" and "changes in the external environment." A threat model is one of the strongest forms of evidence for CC3.2 because it documents the specific threats the organization identified, the analysis performed, and the controls selected in response.

SOC 2 auditors evaluating CC3.2 will ask: How did you determine that your current controls are sufficient? What threats did you consider? A threat model provides a traceable answer.

For the complete SOC 2 requirements, see our [SOC 2 Compliance Guide](/soc-2-compliance).

### ISO 27001 -- A.5.7 (Threat Intelligence) and Clause 6.1

ISO 27001:2022 includes two requirements directly served by threat modeling:

- **Annex A Control A.5.7 (Threat Intelligence)** requires organizations to collect and analyze information relating to information security threats. Threat modeling is a primary mechanism for doing this at the application and system architecture level.
- **Clause 6.1.2** requires a documented information security risk assessment process that identifies risks "associated with the loss of confidentiality, integrity, and availability." Threat modeling feeds directly into this risk assessment by identifying the specific threat scenarios that the risk assessment must evaluate.

ISO 27001 certification auditors will evaluate whether your risk assessment is connected to identified threats. A threat model provides that connection.

For ISO 27001 implementation guidance, see our [ISO 27001 Certification Guide](/iso-27001-certification).

### NIST CSF -- ID.RA (Risk Assessment)

NIST CSF 2.0 Category ID.RA (Risk Assessment) requires organizations to identify and document threats, vulnerabilities, and their potential impact. Specifically:

- **ID.RA-01:** Vulnerabilities in assets are identified, validated, and recorded
- **ID.RA-02:** Cyber threat intelligence is received from information sharing forums and sources
- **ID.RA-03:** Threats, both internal and external, are identified and recorded
- **ID.RA-04:** Potential impacts and likelihoods of threats exploiting vulnerabilities are identified and recorded

Threat modeling produces the evidence for ID.RA-03 and ID.RA-04 directly, and feeds into ID.RA-01 by identifying vulnerabilities that arise from architectural decisions rather than code-level bugs.

For the complete NIST CSF guide, see our [NIST Cybersecurity Framework Implementation Guide](/nist-cybersecurity-framework).

### PCI DSS 4.0 -- Requirement 6.3

PCI DSS v4.0 Requirement 6.3 requires organizations to identify security vulnerabilities and protect system components from known vulnerabilities. More significantly, Requirement 6.2.2 requires that software development personnel working on bespoke and custom software are trained in techniques relevant to their role, including "secure software design" and "threat modeling." PCI DSS 4.0 explicitly names threat modeling as a required competency.

For organizations handling payment card data, threat modeling is no longer a best practice -- it is a stated requirement.

### CMMC -- Level 2 and Above

The Cybersecurity Maturity Model Certification (CMMC) requires organizations at Level 2 and above to implement NIST SP 800-171 controls. Practice RA.L2-3.11.1 requires organizations to "periodically assess the risk to organizational operations, organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI." Threat modeling provides the structured methodology for identifying the threats that this risk assessment must address.

For CMMC implementation details, see our [CMMC Compliance Guide](/cmmc-compliance).

---

## The 4 Questions of Threat Modeling

Adam Shostack's four-question framework provides the universal structure for every threat modeling methodology. Regardless of whether you use STRIDE, PASTA, LINDDUN, or attack trees, every threat model answers these four questions.

### Question 1: What Are We Building?

Before you can identify threats, you must understand the system. This means creating a clear representation of the system's architecture, including:

- **Components:** Services, databases, APIs, message queues, caches, load balancers, third-party integrations
- **Data flows:** How data moves between components, what data is transmitted, and the protocols used
- **Trust boundaries:** Where the level of trust changes -- the boundary between your network and the internet, between your application and a third-party API, between different tenant environments, between user-facing services and backend systems
- **Data stores:** Where sensitive data is persisted, what data is stored, and who has access
- **External entities:** Users, administrators, partner systems, third-party services, attackers

The most common representation is a **Data Flow Diagram (DFD)**, which visualizes all of these elements and their relationships. Without a DFD or equivalent system model, threat modeling devolves into brainstorming -- unstructured, incomplete, and non-repeatable.

### Question 2: What Can Go Wrong?

This is where threat classification methodologies provide structure. Without a methodology, teams tend to focus on the threats they have personally experienced or recently read about, missing entire categories of risk.

Methodologies like STRIDE provide a checklist of threat categories to evaluate against every component and data flow in the system. PASTA provides a risk-centric process for identifying threats from the attacker's perspective. LINDDUN provides a privacy-specific lens. Each methodology ensures that the analysis is systematic rather than ad hoc.

### Question 3: What Are We Going to Do About It?

For each identified threat, the team must decide on a response:

- **Mitigate:** Implement a control that reduces the likelihood or impact of the threat (e.g., add input validation, implement encryption, enforce least privilege)
- **Accept:** Document that the risk is understood and accepted because the likelihood is low, the impact is minimal, or the cost of mitigation exceeds the expected loss
- **Transfer:** Shift the risk to a third party through insurance, contractual obligations, or use of a managed service with defined SLAs
- **Avoid:** Eliminate the threat by removing the functionality or component that introduces it (e.g., stop storing a particular data element, remove an unnecessary API endpoint)

Every decision must be documented with rationale. Auditors do not simply verify that you identified threats -- they verify that you made deliberate, justified decisions about each one.

### Question 4: Did We Do a Good Job?

Validation ensures the threat model is complete and accurate. This includes:

- **Review by someone who did not build the model** -- fresh eyes catch assumptions and blind spots
- **Testing alignment** -- verifying that penetration testing and security testing target the threats identified in the model
- **Post-incident analysis** -- when a security incident occurs, evaluating whether the threat was captured in the model and, if not, why
- **Coverage metrics** -- tracking what percentage of systems and new features have been threat modeled

This fourth question turns threat modeling from a point-in-time exercise into a continuous improvement process.

---

## STRIDE: Microsoft's Threat Classification Model

STRIDE is the most widely adopted threat classification framework. Developed at Microsoft in 1999, it categorizes threats into six types based on the security property they violate. Its simplicity and completeness make it the default starting point for most organizations.

### The Six STRIDE Categories

| Threat Category | Security Property Violated | Description | Example |
|---|---|---|---|
| **Spoofing** | Authentication | Pretending to be someone or something else | An attacker forging authentication tokens to impersonate a legitimate user |
| **Tampering** | Integrity | Modifying data or code without authorization | An attacker modifying API request parameters to alter a transaction amount |
| **Repudiation** | Non-repudiation | Claiming you did not do something, or denying that something happened | A user performing a destructive action and the system having insufficient logs to prove it occurred |
| **Information Disclosure** | Confidentiality | Exposing information to someone not authorized to see it | An API endpoint returning sensitive customer data in error messages |
| **Denial of Service** | Availability | Making a system or feature unavailable | An attacker sending malformed requests that crash a microservice, taking down tenant-facing functionality |
| **Elevation of Privilege** | Authorization | Gaining capabilities you should not have | A regular user exploiting an IDOR vulnerability to access admin functionality |

### How to Apply STRIDE

STRIDE is applied by examining each element in your Data Flow Diagram and asking which STRIDE categories apply:

1. **For each external entity:** Consider Spoofing and Repudiation. Can the entity's identity be forged? Can it deny actions?
2. **For each process:** Consider all six STRIDE categories. Processes are the most common targets because they handle input, enforce logic, and interact with data.
3. **For each data store:** Consider Tampering, Information Disclosure, and Denial of Service. Can the data be modified by unauthorized parties? Can it be read by unauthorized parties? Can access be blocked?
4. **For each data flow:** Consider Tampering and Information Disclosure. Can data be modified in transit? Can data be intercepted?

This systematic approach ensures you evaluate every threat category against every component, producing a comprehensive threat inventory.

### STRIDE Strengths and Limitations

**Strengths:**
- Simple to learn and teach -- accessible to developers without deep security expertise
- Comprehensive coverage of core security properties
- Well-documented with extensive examples and case studies
- Maps cleanly to common security controls

**Limitations:**
- Does not inherently prioritize threats -- all STRIDE categories are treated as equally important without additional risk scoring
- Focuses on technical threats and does not natively address privacy or business logic threats
- Can produce large threat inventories for complex systems, requiring disciplined prioritization
- Does not capture the attacker's perspective or attack sequence (for that, see PASTA and Attack Trees)

---

## PASTA: Process for Attack Simulation and Threat Analysis

PASTA is a seven-stage, risk-centric threat modeling methodology that incorporates the attacker's perspective and explicitly connects threat analysis to business objectives and risk tolerance. Where STRIDE classifies threats by type, PASTA evaluates them in the context of actual attack scenarios and business impact.

### The 7 Stages of PASTA

**Stage 1: Define Objectives**
Identify the business objectives and security requirements for the application. What data does it process? What regulatory requirements apply? What is the risk tolerance? This stage connects threat modeling to the organization's [risk management framework](/risk-management-framework).

**Stage 2: Define Technical Scope**
Document the technical environment -- infrastructure, application components, network topology, third-party dependencies, and data flows. This produces the system model that subsequent stages analyze.

**Stage 3: Application Decomposition**
Break the application into its constituent components, identify trust boundaries, enumerate entry points, and catalog data assets. This stage produces the Data Flow Diagrams and asset inventory that serve as the foundation for threat identification.

**Stage 4: Threat Analysis**
Identify threats using threat intelligence sources, vulnerability databases (CVE, NVD), and attack pattern libraries (CAPEC, MITRE ATT&CK). This is where PASTA diverges from STRIDE -- rather than classifying threats by abstract category, PASTA identifies threats based on real-world attack intelligence specific to the application's technology stack and industry.

**Stage 5: Vulnerability Analysis**
Map the identified threats to known vulnerabilities in the system. Correlate findings from [vulnerability management](/vulnerability-management) scans, code reviews, and architecture analysis with the threat scenarios identified in Stage 4.

**Stage 6: Attack Modeling**
Build attack trees that represent how an attacker would chain multiple vulnerabilities and techniques to achieve their objective. This stage explicitly simulates the attacker's approach, identifying not just individual threats but attack paths -- sequences of actions that lead from initial access to objective completion.

**Stage 7: Risk and Impact Analysis**
Quantify the risk of each attack scenario by assessing likelihood (based on attacker capability, threat intelligence, and vulnerability exploitability) and impact (based on business objectives defined in Stage 1). Prioritize remediation based on residual risk after existing controls are considered.

### When to Use PASTA

PASTA is best suited for:

- High-risk applications processing sensitive data (financial transactions, healthcare records, personally identifiable information)
- Environments with known adversaries or targeted threats (financial services, government, defense)
- Organizations that need to quantify risk in business terms for executive decision-making
- Compliance scenarios requiring demonstrated connection between threat analysis and business risk (ISO 27001 Clause 6.1, NIST CSF ID.RA)

PASTA's seven-stage process requires more effort than STRIDE but produces richer output: prioritized threat scenarios connected to business impact, with specific attack paths and quantified risk scores.

---

## LINDDUN: Privacy Threat Modeling

LINDDUN is a privacy-focused threat modeling framework developed at KU Leuven specifically to address privacy threats that security-focused methodologies like STRIDE do not capture. For organizations subject to GDPR, CCPA, or any data protection regulation, LINDDUN fills a critical gap.

### The 7 LINDDUN Privacy Threat Categories

| Category | Privacy Property Threatened | Description |
|---|---|---|
| **Linking** | Unlinkability | Associating two or more data items, actions, or identities that were intended to remain separate |
| **Identifying** | Anonymity | Determining the identity of a person behind pseudonymous or anonymous data |
| **Non-repudiation** | Plausible Deniability | Being unable to deny having performed an action (the opposite of repudiation in STRIDE -- here, the ability to deny is a privacy property) |
| **Detecting** | Undetectability | Determining that a person performed a specific action or is using a specific service |
| **Data Disclosure** | Confidentiality | Unauthorized access to personal data |
| **Unawareness** | Content Awareness | Data subjects being unaware of what data is collected, how it is processed, or who has access |
| **Non-compliance** | Policy/Legal Compliance | Failing to comply with data protection legislation, regulations, or organizational privacy policies |

### LINDDUN and GDPR/CCPA Compliance

LINDDUN maps directly to GDPR principles:

- **Linking** and **Identifying** threats map to GDPR Article 5(1)(c) -- data minimization and purpose limitation
- **Unawareness** maps to GDPR Articles 13 and 14 -- transparency obligations
- **Non-compliance** maps to GDPR Article 5(2) -- accountability principle
- **Data Disclosure** maps to GDPR Article 32 -- security of processing

For organizations conducting [Privacy Impact Assessments](/privacy-impact-assessment) (required under GDPR Article 35 for high-risk processing), LINDDUN provides the threat identification methodology that feeds into the assessment.

### Combining LINDDUN with STRIDE

STRIDE and LINDDUN are complementary. STRIDE covers security threats; LINDDUN covers privacy threats. For systems processing personal data -- which includes virtually every SaaS application -- using both frameworks ensures comprehensive coverage:

1. Conduct STRIDE analysis to identify security threats (spoofing, tampering, information disclosure, etc.)
2. Conduct LINDDUN analysis to identify privacy threats (linking, identifying, unawareness, etc.)
3. Merge the results into a unified threat inventory with both security and privacy dimensions
4. Prioritize using your [risk assessment methodology](/risk-assessment-template)

This combined approach is particularly valuable for organizations pursuing both SOC 2 (security-focused) and GDPR compliance (privacy-focused) simultaneously.

For GDPR compliance guidance, see our [GDPR Compliance Guide for US SaaS Companies](/gdpr-compliance-us-saas).

---

## Attack Trees and MITRE ATT&CK: Adversary-Centric Approaches

While STRIDE and LINDDUN classify threats by category, attack trees and MITRE ATT&CK model threats from the attacker's perspective -- focusing on how threats are executed rather than what type they are.

### Attack Trees

Attack trees, formalized by Bruce Schneier, represent attacks as hierarchical structures where the root node is the attacker's goal and leaf nodes are the individual actions required to achieve it.

**Example: Unauthorized Access to Customer Data**

```
Root: Access customer data without authorization
├── Exploit application vulnerability
│   ├── SQL injection in search API
│   ├── IDOR in customer profile endpoint
│   └── SSRF to access internal data store
├── Compromise employee credentials
│   ├── Phishing attack on engineering team
│   ├── Credential stuffing with leaked passwords
│   └── Social engineering via support channel
├── Exploit third-party integration
│   ├── Compromise OAuth token from partner service
│   └── Exploit vulnerability in payment processor SDK
└── Insider threat
    ├── Excessive database access permissions
    └── Unmonitored direct data store access
```

Each leaf node can be annotated with likelihood, difficulty, cost to the attacker, and detectability. This allows teams to identify the cheapest attack paths -- the routes an attacker is most likely to take -- and prioritize defenses accordingly.

### MITRE ATT&CK

MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations. It catalogs how attackers actually operate, organized by:

- **Tactics:** The attacker's objective at each stage (Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact)
- **Techniques:** The specific methods used to achieve each tactic (e.g., Phishing under Initial Access, Pass the Hash under Credential Access)
- **Procedures:** Real-world examples of how specific threat groups have used each technique

### Using ATT&CK in Threat Modeling

MITRE ATT&CK enhances threat modeling by grounding it in real-world attacker behavior:

1. **Identify relevant threat groups** based on your industry and data types (ATT&CK catalogs over 130 threat groups with known TTPs)
2. **Map their known techniques** to your system's attack surface
3. **Evaluate your controls** against the specific techniques likely to be used against you
4. **Identify detection gaps** where attacker techniques would not trigger existing monitoring

This approach is particularly valuable for compliance frameworks that reference threat intelligence. ISO 27001 A.5.7 requires organizations to collect and analyze threat intelligence. NIST CSF ID.RA-02 requires receiving cyber threat intelligence from information sharing forums. ATT&CK provides the structured intelligence these controls demand.

For incident response planning informed by ATT&CK, see our [Incident Response Plan Guide](/incident-response-plan).

---

## How to Conduct a Threat Model: Step-by-Step

This section provides a practical, methodology-agnostic process for conducting a threat model. The process works with STRIDE, PASTA, or any other framework.

### Step 1: Assemble the Team

Threat modeling is a collaborative activity. The team should include:

- **A developer or architect** who knows the system's internals
- **A security engineer** who can identify threats and evaluate controls
- **A product manager or business analyst** who understands the data sensitivity and business context
- **An operations/DevOps engineer** who understands the deployment environment and infrastructure

Do not attempt to threat model in isolation. A single person, regardless of expertise, will miss threats that emerge from the intersection of design decisions, business logic, and operational reality.

### Step 2: Create the Data Flow Diagram

The DFD is the foundation of the threat model. Use standard DFD notation:

- **External entities** (rectangles): Users, external systems, third-party services
- **Processes** (circles): Application components, services, functions that process data
- **Data stores** (parallel lines): Databases, file systems, caches, message queues
- **Data flows** (arrows): Connections between elements, labeled with the data type and protocol
- **Trust boundaries** (dashed lines): Where the level of trust changes

**Example DFD for a SaaS Application:**

```
[End User] --(HTTPS/JWT)--> [API Gateway] --(gRPC)--> [Auth Service]
                                  |                         |
                                  |                    [User DB]
                                  |
                            --(gRPC)--> [Application Service] --(TLS)--> [Customer DB]
                                  |                                          |
                            --(HTTPS)--> [Payment Processor]          [Object Storage]
                                  |
                            --(AMQP)--> [Message Queue] --> [Notification Service]

Trust Boundaries:
  -- Internet / DMZ boundary (between End User and API Gateway)
  -- DMZ / Internal network boundary (between API Gateway and internal services)
  -- Internal / Third-party boundary (between Application Service and Payment Processor)
  -- Tenant isolation boundary (within Customer DB and Object Storage)
```

The DFD should represent the system at a level of abstraction appropriate for threat analysis. Too high-level and you miss threats. Too detailed and the analysis becomes unmanageable. For most SaaS applications, a DFD that shows individual services, their data stores, and external integrations is the right level.

### Step 3: Identify Trust Boundaries

Trust boundaries are the most important element on the DFD for threat modeling purposes. A trust boundary exists wherever the level of privilege, ownership, or trust changes:

- Between the internet and your network perimeter
- Between your DMZ and internal network
- Between different microservices with different privilege levels
- Between your application and a third-party service
- Between different customer tenant environments
- Between the application layer and the database layer
- Between the control plane and data plane in cloud infrastructure

Threats concentrate at trust boundaries. An attacker who can cross a trust boundary gains capabilities they should not have. Every data flow that crosses a trust boundary deserves scrutiny.

### Step 4: Enumerate Threats

Apply your chosen methodology (STRIDE, PASTA, LINDDUN) systematically to every element and data flow in the DFD, with particular attention to trust boundaries.

**Using STRIDE per element:**

For each element on the DFD, ask:

| Element | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| API Gateway | Can an attacker spoof requests? | Can requests be tampered in transit? | Can actions be denied? | Can responses leak sensitive data? | Can the gateway be overwhelmed? | Can a user gain admin access? |
| Customer DB | -- | Can data be modified by unauthorized users? | -- | Can data be read by unauthorized users? | Can the database be taken offline? | -- |
| Data flow: API Gateway to Auth Service | -- | Can gRPC calls be intercepted and modified? | -- | Can authentication tokens be intercepted? | -- | -- |

Document each identified threat with:
- **Threat ID** (for tracking)
- **Category** (STRIDE category or equivalent)
- **Affected component** (specific DFD element)
- **Description** (what the threat is, in concrete terms)
- **Prerequisites** (what conditions must exist for the threat to be viable)

### Step 5: Assess and Prioritize

Not every identified threat requires the same level of response. Prioritize using a risk scoring methodology:

**Risk = Likelihood x Impact**

For each threat, evaluate:

- **Likelihood:** How probable is exploitation? Consider attacker capability, attack surface exposure, existing controls, and known exploitation in the wild.
- **Impact:** What happens if the threat materializes? Consider data sensitivity, number of affected users, regulatory implications, financial loss, and reputational damage.

Use a consistent scoring scale (e.g., 1-5 for both likelihood and impact, producing a risk score from 1-25). This aligns with the risk assessment methodology your compliance framework requires.

For a detailed risk scoring methodology, see our [Risk Assessment Template Guide](/risk-assessment-template).

### Step 6: Define Mitigations

For each threat above your risk acceptance threshold, define a specific mitigation:

| Threat | Mitigation | Control Type | Status |
|---|---|---|---|
| Spoofing: Forged JWT tokens at API Gateway | Implement JWT signature verification with RS256, validate issuer and audience claims, enforce token expiration | Preventive | Implemented |
| Information Disclosure: Customer data in error messages | Implement structured error handling that returns generic error codes to clients and logs detailed errors server-side only | Preventive | In Progress |
| Elevation of Privilege: IDOR in customer profile endpoint | Implement object-level authorization checks that verify the requesting user has access to the specific resource | Preventive | Planned |
| Denial of Service: API Gateway overwhelm | Implement rate limiting per tenant, circuit breakers, and auto-scaling policies | Preventive + Detective | Implemented |

Each mitigation must be traceable to the threat it addresses. This traceability is the evidence auditors need to verify that your controls are risk-based rather than arbitrary.

### Step 7: Document and Review

The completed threat model should be a living document that includes:

- The DFD with trust boundaries
- The complete threat inventory with STRIDE (or equivalent) classifications
- Risk scores for each threat
- Mitigation decisions with rationale
- Accepted risks with documented justification and approval
- Review history and version tracking

Store the threat model alongside the system's architecture documentation. It should be updated whenever the architecture changes and reviewed at least annually.

---

## Threat Modeling for SaaS Applications

SaaS applications introduce specific threat categories that traditional on-premises threat models do not address. If you are building or operating a multi-tenant SaaS platform, your threat model must account for these considerations.

### Multi-Tenancy Threats

Multi-tenancy is the defining architectural characteristic of SaaS applications, and it is the source of some of the most severe threats:

- **Tenant data isolation failure:** A flaw in query filtering, authorization logic, or data partitioning that allows one tenant to access another tenant's data. This is the single most critical threat category for SaaS applications.
- **Noisy neighbor attacks:** One tenant consuming disproportionate resources (compute, storage, API calls) and degrading service for other tenants.
- **Cross-tenant privilege escalation:** A user in one tenant exploiting a vulnerability to gain access to another tenant's administrative functions.
- **Tenant enumeration:** An attacker determining which organizations use the service by probing tenant identifiers, subdomains, or API responses.

Your threat model must explicitly evaluate tenant isolation at every layer: application logic, database queries, object storage access, caching, message queuing, and logging.

### API Security Threats

SaaS applications expose functionality through APIs, making API security a core threat modeling concern:

- **Broken Object Level Authorization (BOLA/IDOR):** APIs that fail to verify the requesting user has access to the specific resource identified in the request
- **Broken Authentication:** Weak token management, missing token expiration, or insecure token storage
- **Excessive Data Exposure:** API responses including more data than the client needs, relying on the client to filter
- **Mass Assignment:** APIs accepting user input that modifies internal object properties (e.g., `is_admin: true`)
- **Rate Limiting Failures:** APIs without rate limiting that allow credential stuffing, data scraping, or resource exhaustion

The OWASP API Security Top 10 provides a structured checklist for API-specific threats that complements STRIDE analysis.

### Cloud-Native Threats

SaaS applications deployed on cloud infrastructure face threats that arise from the shared responsibility model:

- **IAM misconfigurations:** Overly permissive cloud IAM policies that allow lateral movement between services
- **Storage misconfigurations:** Public S3 buckets, unencrypted storage, or missing access logging
- **Network exposure:** Security groups or network policies that expose internal services to the internet
- **Secrets management failures:** Hardcoded credentials, unrotated API keys, or secrets stored in environment variables accessible to all services
- **Container escape:** In containerized environments, a compromised container breaking out of its isolation to access the host or other containers

For cloud security considerations, see our [Cloud Security Compliance Guide](/cloud-security-compliance-aws-gcp-azure).

---

## Integrating Threat Modeling into Your SDLC and CI/CD Pipeline

Threat modeling delivers the most value when it is embedded in your development process rather than performed as a separate, periodic activity. Integration into your SDLC and CI/CD pipeline ensures that threats are identified when they can be addressed most efficiently.

### Where Threat Modeling Fits in the SDLC

| SDLC Phase | Threat Modeling Activity | Output |
|---|---|---|
| **Requirements** | Identify security and privacy requirements based on data sensitivity and regulatory obligations | Security requirements document |
| **Design** | Conduct full threat model using DFDs, STRIDE/PASTA, and risk scoring | Documented threat model with prioritized threats and mitigations |
| **Development** | Developers reference the threat model when implementing features; security controls are built to address identified threats | Code that implements mitigations; unit tests that verify security controls |
| **Testing** | Security testing (SAST, DAST, penetration testing) targets the threats identified in the model | Test results mapped to threat model entries |
| **Deployment** | Automated checks verify that security controls are deployed correctly | Deployment validation evidence |
| **Operations** | Monitoring and alerting configured to detect exploitation of identified threats | Detection rules mapped to threat model entries |

### Threat Modeling as Code

Modern engineering teams are adopting "threat modeling as code" -- representing threat models in machine-readable formats that can be version-controlled, diffed, reviewed in pull requests, and integrated into CI/CD pipelines.

Tools like Threagile allow teams to define their system architecture and threat model in YAML, then automatically generate threat analyses, risk reports, and DFD visualizations. This approach offers several advantages:

- **Version control:** Threat models are stored in Git alongside the code they describe, providing full change history
- **Pull request review:** Changes to the threat model are reviewed alongside code changes, ensuring the model stays current
- **Automated validation:** CI/CD pipelines can check that new components have been added to the threat model and that all identified threats have documented mitigations
- **Continuous analysis:** When the architecture definition changes, the threat analysis is regenerated automatically

### Integration with CI/CD

Practical integration points for threat modeling in a CI/CD pipeline:

1. **Pre-commit / PR checks:** Verify that architectural changes (new services, new data flows, new integrations) are reflected in the threat model definition file
2. **Build stage:** Run Threagile or equivalent tool to regenerate the threat analysis from the current model definition
3. **Gate:** Fail the build if any high-severity threats lack documented mitigations
4. **Test stage:** Map SAST/DAST findings to threat model entries, identifying which modeled threats have corresponding automated detection
5. **Post-deployment:** Generate updated threat model reports as part of release documentation

For detailed CI/CD pipeline security integration, see our [DevSecOps Compliance Guide](/devsecops-compliance-cicd).

---

## Threat Modeling Tools

Several tools support the threat modeling process, ranging from free diagramming tools to enterprise platforms with automated threat generation.

### Microsoft Threat Modeling Tool (TMT)

**Cost:** Free
**Best for:** Teams already using Microsoft technologies or looking for a simple, STRIDE-based tool

Microsoft TMT provides a DFD drawing surface with built-in STRIDE threat generation. You draw your system architecture using predefined stencils (web applications, databases, processes, external services), mark trust boundaries, and the tool automatically generates a list of threats based on STRIDE categories for each element. It produces HTML reports suitable for audit evidence.

**Limitations:** Windows-only, limited customization of threat rules, no collaboration features, no API integration.

### OWASP Threat Dragon

**Cost:** Free and open source
**Best for:** Teams wanting a lightweight, cross-platform, open-source option

Threat Dragon provides a web-based DFD editor with manual threat entry. It supports STRIDE and LINDDUN threat types and produces JSON-based threat model files that can be version-controlled. It integrates with GitHub and Bitbucket for storage.

**Limitations:** Does not auto-generate threats (manual entry only), limited reporting capabilities, no risk scoring built in.

### IriusRisk

**Cost:** Commercial (enterprise licensing)
**Best for:** Organizations needing automated threat and countermeasure generation at scale

IriusRisk is a full-featured threat modeling platform that automatically generates threats and countermeasures based on system architecture questionnaires and component libraries. It includes pre-built threat libraries for common architectures (cloud-native, microservices, API-first), maps threats to compliance framework requirements, and integrates with Jira, Azure DevOps, and CI/CD pipelines.

**Strengths:** Automated threat generation, compliance mapping, workflow integration, team collaboration. Most suitable for organizations that need to threat model multiple applications at scale.

### Threagile

**Cost:** Free and open source
**Best for:** Engineering teams that want threat modeling as code

Threagile takes a YAML-based architecture definition and automatically generates a threat model, risk analysis, and DFD visualization. Because the model is defined in code, it integrates naturally with Git workflows and CI/CD pipelines. It supports custom risk rules and produces reports in multiple formats.

**Strengths:** Code-based approach, CI/CD integration, automatic risk analysis, version-controllable. Ideal for [DevSecOps](/devsecops-compliance-cicd) teams that want threat modeling embedded in their engineering workflow.

### Tool Selection Guidance

| Criterion | Microsoft TMT | Threat Dragon | IriusRisk | Threagile |
|---|---|---|---|---|
| **Cost** | Free | Free | $$$$ | Free |
| **Auto-generates threats** | Yes (STRIDE) | No | Yes (extensive) | Yes |
| **Compliance mapping** | No | No | Yes | Partial |
| **CI/CD integration** | No | No | Yes | Yes |
| **Platform** | Windows only | Web-based | Web-based | CLI / Docker |
| **Collaboration** | File-based | GitHub/Bitbucket | Built-in | Git-based |
| **Best for** | Individual analysts | Small teams | Enterprise | Engineering teams |

---

## Common Threat Modeling Mistakes

After reviewing hundreds of threat models across compliance engagements, these are the mistakes that most frequently lead to audit findings, incomplete threat coverage, or wasted effort.

### Mistake 1: Threat Modeling Too Late

Threat modeling after the system is built and deployed is an assessment, not a design activity. By that point, architectural decisions are locked in, and remediating design-level threats requires rework that is orders of magnitude more expensive than addressing them during design. Start threat modeling at the design phase, when alternatives are still available.

### Mistake 2: Treating It as a One-Time Exercise

A threat model created during initial design and never updated becomes inaccurate with every feature release, architecture change, and new integration. Auditors will ask when the threat model was last reviewed. If the answer is "two years ago" and the system has changed significantly, the model has no audit value.

### Mistake 3: No Trust Boundaries on the DFD

A DFD without trust boundaries is just an architecture diagram. Trust boundaries are where threats concentrate. Without them, the threat enumeration phase has no structure, and the resulting threat inventory will be incomplete. Every DFD used for threat modeling must include explicit trust boundaries.

### Mistake 4: Listing Threats Without Risk Scores

A list of 200 threats without severity rankings is not actionable. Teams do not know where to start, resources are not allocated efficiently, and auditors cannot determine whether your response was proportionate to the risk. Every identified threat needs a risk score based on likelihood and impact.

### Mistake 5: Generic Threats Not Specific to Your System

"SQL injection" is not a threat model finding -- it is a vulnerability class. A threat model finding is: "The search API in the Customer Service accepts user-supplied query parameters that are concatenated into a SQL query against the tenant_data table, which stores PII for all tenants in a shared schema. Successful SQL injection would allow cross-tenant data access." Specificity makes threats actionable.

### Mistake 6: No Connection Between Threats and Controls

Identifying threats without documenting the controls that address them -- or without identifying the gaps where no controls exist -- defeats the purpose of threat modeling. Every threat must map to either an existing control, a planned control, or a documented risk acceptance decision.

### Mistake 7: Ignoring Privacy Threats

STRIDE covers security threats but not privacy threats. If your application processes personal data (and almost every SaaS application does), you need LINDDUN or an equivalent privacy-focused analysis alongside STRIDE. GDPR and CCPA auditors will ask how you identified privacy risks -- STRIDE alone does not answer that question.

### Mistake 8: Excluding Third-Party Components

Many organizations threat model only the code they write, ignoring the third-party services, APIs, SDKs, and open-source libraries their application depends on. These components introduce threats that you must identify and manage. Your threat model must include third-party integrations and the trust boundaries between your code and theirs.

For managing third-party security risks, see our [Vendor Risk Management Guide](/vendor-risk-management) and [Third-Party Risk Assessment Guide](/third-party-risk-assessment).

---

## Frequently Asked Questions

### How long does a threat model take to complete?

For a moderately complex SaaS application (5-10 microservices, 2-3 external integrations, a relational database, and an object store), an initial threat model typically takes 4-8 hours of collaborative work across 1-2 sessions. Subsequent updates for new features or changes take 1-3 hours. The investment pays for itself many times over: a design-phase threat identification costs a fraction of a post-deployment vulnerability remediation.

### Do I need a dedicated security team to do threat modeling?

No. Threat modeling is most effective when performed by cross-functional teams that include developers, architects, and product managers -- not just security specialists. Security expertise is valuable but not a prerequisite. STRIDE's structured approach is accessible to any engineering team. Start with developer-led threat models and bring in security specialists for high-risk systems or periodic reviews.

### Which threat modeling methodology should I use?

Start with STRIDE. It is the simplest to learn, the most widely documented, and sufficient for the majority of applications. Add LINDDUN if you process personal data and need to demonstrate privacy threat identification for GDPR or CCPA. Consider PASTA if you operate in a high-threat environment (financial services, government, defense) and need risk-centric analysis connected to business impact. Use Attack Trees for specific high-value scenarios that require detailed attack path analysis.

### Is threat modeling required for SOC 2?

SOC 2 does not explicitly name "threat modeling" as a requirement. However, CC3.2 requires identifying risks to objectives, and CC7.1 requires identifying vulnerabilities. Threat modeling is one of the most effective ways to produce the evidence these criteria demand. Most SOC 2 auditors will view a documented threat model favorably as evidence of a mature risk identification process.

### How does threat modeling differ from a risk assessment?

A risk assessment evaluates risks across the entire organization -- operational, financial, legal, and technical. Threat modeling focuses specifically on a system's architecture and design, identifying technical threats at the component and data flow level. Threat modeling feeds into the broader risk assessment: the threats you identify through threat modeling become entries in your organization's [risk register](/risk-assessment-template). They are complementary activities, not alternatives.

### How do I prioritize threats when the list is overwhelming?

Use a quantitative risk scoring methodology. Score each threat on likelihood (1-5) and impact (1-5), multiply to get a risk score (1-25), and address threats in descending order. For initial prioritization, focus on threats that cross trust boundaries, affect sensitive data, or exploit weaknesses in authentication and authorization. Accept that you will not mitigate every threat immediately -- document risk acceptance decisions for lower-priority items and revisit them in subsequent iterations.

### Can threat modeling be automated?

Partially. Tools like IriusRisk and Threagile automatically generate threat lists based on system architecture definitions. This automates the threat enumeration step but does not replace the judgment required for risk scoring, mitigation design, and risk acceptance decisions. The best approach is to use automation for the mechanical parts (generating threat lists, mapping to STRIDE categories, producing reports) and apply human expertise for the analytical parts (evaluating relevance, scoring risk, designing mitigations).

### How do I measure the effectiveness of my threat modeling program?

Track four metrics: (1) **Coverage** -- the percentage of systems and new features that have been threat modeled. (2) **Currency** -- the age of each threat model relative to the last significant system change. (3) **Escape rate** -- the number of security vulnerabilities found in production that were in scope for threat modeling but not identified. A declining escape rate indicates the program is maturing. (4) **Remediation rate** -- the percentage of identified threats with implemented mitigations versus those in backlog or accepted status.

---

## Build a Threat Modeling Practice That Strengthens Security and Satisfies Auditors

Threat modeling is the bridge between abstract compliance requirements and concrete security architecture. It transforms "identify risks to objectives" (SOC 2 CC3.2) and "identify threats associated with loss of confidentiality, integrity, and availability" (ISO 27001 Clause 6.1.2) from vague mandates into specific, documented, actionable threat inventories tied to your actual system design.

Organizations that embed threat modeling into their development process find fewer vulnerabilities in production, spend less on post-deployment remediation, produce stronger audit evidence, and make better-informed decisions about where to invest limited security resources. Organizations that skip it are perpetually reacting to findings from penetration tests, vulnerability scans, and -- in the worst case -- real incidents.

The methodology you choose matters less than the discipline of doing it consistently. Start with STRIDE and a whiteboard. Progress to formal DFDs and documented threat inventories. Mature into threat modeling as code integrated into your CI/CD pipeline. The path is incremental, and every step improves both your security posture and your compliance position.

**QuickTrust automates the compliance evidence that threat modeling produces.** The platform maps your security controls to framework requirements across SOC 2, ISO 27001, NIST CSF, PCI DSS, and CMMC, tracks risk treatment decisions with full audit trails, and generates the evidence packages your auditors expect -- connecting your threat modeling outputs directly to the compliance controls they satisfy.

Instead of maintaining separate spreadsheets for threat inventories, risk registers, and control mappings, let QuickTrust unify your risk and compliance data into a single, audit-ready platform.

[Start your free QuickTrust assessment](https://trust.quickintell.com) and see how your threat modeling and risk management practices map to audit requirements across every framework you are pursuing.
