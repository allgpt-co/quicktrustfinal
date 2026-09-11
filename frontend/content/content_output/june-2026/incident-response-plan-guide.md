---
meta_description: "Build an incident response plan that passes SOC 2, ISO 27001, HIPAA, and PCI DSS audits: 6 phases, roles, templates, testing, and evidence requirements."
target_keyword: "incident response plan"
secondary_keywords: "incident response plan template, IRP compliance, incident response SOC 2, incident response ISO 27001, tabletop exercise"
word_count_target: "1800"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# How to Build an Incident Response Plan That Passes Every Compliance Audit (SOC 2, ISO 27001, HIPAA, PCI DSS)

Every major compliance framework requires an incident response plan. SOC 2, ISO 27001, HIPAA, and PCI DSS all mandate that you have documented procedures for detecting, responding to, and recovering from security incidents. What none of them do particularly well is tell you how to build one that actually works in practice and satisfies all of them simultaneously.

Most organizations end up with either a generic plan downloaded from the internet that has never been tested, or a framework-specific plan that covers one standard well but leaves gaps for the others.

This guide walks through building a unified incident response plan that meets SOC 2, ISO 27001, HIPAA, and PCI DSS requirements simultaneously, follows the 6-phase methodology, and produces the evidence auditors actually examine.

---

## IRP Requirements by Framework

Before building the plan, you need to understand what each framework specifically requires.

**SOC 2 (CC7.3, CC7.4, CC7.5)**
Requires detecting anomalies, responding according to defined procedures, recovering operations, and communicating with affected parties. Auditors evaluate whether procedures exist, are followed consistently, and produce documented evidence.

**ISO 27001 (Annex A Controls A.5.24 through A.5.28)**
ISO 27001 requires incident management planning and preparation (A.5.24), assessment and decision on information security events (A.5.25), response to information security incidents (A.5.26), learning from incidents (A.5.27), and collection of evidence (A.5.28). The emphasis on learning and evidence collection is stronger in ISO 27001 than in other frameworks.

**HIPAA (Security Rule 164.308(a)(6))**
HIPAA requires covered entities and business associates to implement policies and procedures to address security incidents, including identifying and responding to suspected or known incidents, mitigating harmful effects, and documenting incidents and their outcomes. HIPAA also imposes specific breach notification timelines: 60 days for breaches affecting 500 or more individuals, with notification to affected individuals, HHS, and media.

**PCI DSS (Requirement 12.10)**
PCI DSS requires an incident response plan that addresses compromise of cardholder data specifically. The plan must be tested at least annually, include specific roles and responsibilities, cover communication and escalation procedures, reference business recovery and continuity, and include data breach notification requirements. PCI DSS v4.0 added requirements for responding to detection of PAN (primary account number) anywhere it is not expected.

**The overlap:** All four frameworks require documented procedures, defined roles, communication plans, evidence of incidents and responses, and regular testing. The differences are primarily in notification timelines, scope-specific requirements (PHI for HIPAA, cardholder data for PCI DSS), and emphasis areas. A well-structured IRP can address all four simultaneously.

---

## The 6 Phases of Incident Response

The industry-standard incident response methodology, based on the NIST Computer Security Incident Handling Guide (SP 800-61), consists of six phases. Your plan should address each one with specific procedures, responsible parties, and evidence outputs.

### Phase 1: Preparation

Preparation is everything you do before an incident occurs. This is the phase auditors scrutinize most heavily, because it determines whether your organization can execute the remaining five phases effectively.

**What preparation includes:**
- Documented incident response plan (this document)
- Defined incident response team with named roles and contact information
- Communication templates for internal and external notifications
- Escalation criteria and procedures
- Incident classification scheme (severity levels with definitions)
- Pre-authorized emergency actions (who can shut down systems, isolate networks, engage forensics)
- Relationships established with external resources (legal counsel, forensic investigators, law enforcement contacts, PR/communications firm)
- Tools and access provisioned for the incident response team (log access, forensic tools, communication channels)
- Training for incident response team members
- Regular testing through tabletop exercises and simulations

**Evidence auditors examine:** The plan document itself, team roster, training records, tabletop exercise reports, and tool readiness documentation.

### Phase 2: Identification

Identification is the process of detecting that a security event has occurred and determining whether it constitutes an incident that triggers your response procedures.

**Identification sources:**
- SIEM alerts and log analysis
- Intrusion detection/prevention system (IDS/IPS) alerts
- Endpoint detection and response (EDR) alerts
- Employee reports (suspicious emails, unusual behavior)
- Customer reports (unauthorized access, data exposure)
- Automated monitoring alerts (configuration changes, anomalous access patterns)
- Third-party notifications (vendor breach notifications, threat intelligence)

**Classification criteria:** Define severity levels with clear, objective criteria. A four-level classification works for most organizations.

| Severity | Definition | Response Timeline | Examples |
|---|---|---|---|
| Critical (P1) | Active breach, data exfiltration confirmed or highly likely, service unavailable | Immediate response, all hands | Confirmed data breach, ransomware, active intrusion |
| High (P2) | Potential breach, significant vulnerability under exploitation, partial service impact | Response within 1 hour | Suspicious access patterns, malware detection, successful phishing with credential compromise |
| Medium (P3) | Security event requiring investigation, no confirmed compromise | Response within 4 hours | Failed intrusion attempts, policy violations, minor malware on isolated system |
| Low (P4) | Security event logged for tracking, no immediate risk | Response within 24 hours | Port scans, spam campaigns, unsuccessful phishing attempts |

**Evidence auditors examine:** Detection tool configurations, alert logs, incident tickets showing classification decisions, and classification criteria documentation.

### Phase 3: Containment

Containment limits the damage from an incident by isolating affected systems and preventing the incident from spreading. There are two sub-phases: short-term containment (immediate isolation) and long-term containment (sustainable measures while you prepare for eradication).

**Short-term containment actions:**
- Isolate affected systems from the network
- Disable compromised accounts
- Block malicious IP addresses or domains
- Redirect traffic away from affected services
- Preserve forensic evidence (memory dumps, disk images) before making changes

**Long-term containment actions:**
- Deploy temporary fixes or patches
- Set up enhanced monitoring on related systems
- Implement additional access restrictions
- Bring clean backup systems online if needed

**Critical principle:** Document every containment action with timestamps, who performed it, and the rationale. This documentation is both a compliance requirement and a legal necessity.

**Evidence auditors examine:** Incident logs showing containment actions, timestamps, and decision rationale. Chain of custody documentation for preserved evidence.

### Phase 4: Eradication

Eradication removes the root cause of the incident from your environment. This might include removing malware, closing the vulnerability that was exploited, patching affected systems, rebuilding compromised servers from clean images, or revoking and reissuing all credentials that may have been compromised.

**Eradication procedures should address:**
- Root cause identification and documentation
- Removal of attacker access and persistence mechanisms
- Patching or remediation of the exploited vulnerability
- Verification that the root cause has been eliminated
- Scanning of related systems for similar compromise indicators

**Evidence auditors examine:** Root cause analysis documentation, remediation actions taken, and verification results.

### Phase 5: Recovery

Recovery restores affected systems to normal operation and confirms that the incident has been fully resolved.

**Recovery steps:**
- Restore systems from clean backups or rebuild from known-good configurations
- Gradually return systems to production with enhanced monitoring
- Verify system functionality and data integrity
- Monitor for signs of re-compromise for a defined period (minimum 30 days for critical incidents)
- Confirm with stakeholders that normal operations have resumed

**Evidence auditors examine:** Recovery timeline, system restoration records, post-recovery monitoring logs, and stakeholder confirmation.

### Phase 6: Lessons Learned

The lessons-learned phase is where ISO 27001 places the most emphasis, and it is the phase most organizations skip. This is a mistake. Auditors across all four frameworks look for evidence that you learn from incidents and improve your controls based on that learning.

**Lessons-learned process:**
- Conduct a post-incident review meeting within 5 business days of incident closure
- Document what happened, what worked, what failed, and what should change
- Identify specific improvements to controls, procedures, or tools
- Create action items with owners and deadlines for each improvement
- Track action items to completion
- Update the incident response plan based on findings

**Evidence auditors examine:** Post-incident review meeting notes, action items with completion status, and updated plan versions that reflect lessons learned.

---

## Roles and Responsibilities

A functional IRP defines specific roles, not just named individuals. People leave organizations; roles persist.

**Incident Commander:** Owns the overall incident response. Makes escalation and communication decisions. Has authority to authorize emergency actions.

**Technical Lead:** Directs technical investigation, containment, and eradication. Coordinates with engineering teams.

**Communications Lead:** Manages internal and external communications. Coordinates with legal, PR, and regulatory notification requirements.

**Documentation Lead:** Maintains the incident log throughout the response. Captures timestamps, actions, decisions, and evidence.

**Executive Sponsor:** Senior leader (typically CISO, CTO, or CEO) who is briefed on significant incidents and authorizes major decisions (customer notification, regulatory filing, law enforcement engagement).

Each role should have a primary assignee and at least one backup. Contact information, including after-hours methods, must be current and accessible.

---

## Communication Templates

Prepare templates before you need them. Under the stress of an active incident is the worst time to draft notifications.

**Templates to prepare:**
- Internal escalation notification
- Customer notification (for incidents affecting customer data)
- Regulatory notification (HIPAA breach to HHS, state attorney general)
- Law enforcement notification
- Media holding statement
- All-hands employee communication
- Board briefing

Each template should include placeholders for incident-specific details and pre-approved language that has been reviewed by legal counsel.

---

## Testing Requirements

An untested incident response plan is a theoretical document, not an operational capability. Every framework requires testing, and auditors verify it.

**Tabletop exercises** are the most common and most practical testing method. In a tabletop exercise, the incident response team walks through a realistic scenario verbally, discussing what they would do at each phase, who would be responsible, and what tools they would use. Tabletop exercises should be conducted at least twice per year with different scenarios.

**Scenario examples for tabletop exercises:**
- Ransomware attack on production systems
- Insider threat: employee exfiltrating customer data
- Third-party vendor breach affecting your data
- Compromised credentials used for unauthorized access
- Payment card data exposure (for PCI DSS scope)
- PHI breach via misconfigured system (for HIPAA scope)

**Documentation from exercises:** Date, participants, scenario description, decisions made, gaps identified, and action items for improvement.

**Functional exercises** involve actually executing parts of the response plan -- such as restoring from backups, activating the communication tree, or deploying forensic tools. These are more resource-intensive but provide stronger evidence of operational readiness.

---

## How QuickTrust Engineers Implement Incident Response

QuickTrust takes a hands-on approach to incident response implementation that goes beyond delivering a document.

**Plan development.** QuickTrust engineers build your incident response plan based on your actual infrastructure, team structure, and framework requirements. The plan is tailored to your environment -- not a template with your company name inserted.

**Detection infrastructure.** QuickTrust deploys and configures the detection capabilities that feed Phase 2: centralized logging, SIEM rules or alerts, EDR deployment, and cloud-native monitoring. These tools are configured to generate the alerts and evidence that your IRP depends on.

**Communication and escalation setup.** QuickTrust configures the communication channels, escalation procedures, and notification workflows that activate when an incident is declared. This includes PagerDuty or equivalent on-call rotations, Slack or Teams incident channels, and automated notification templates.

**Tabletop exercises.** QuickTrust facilitates tabletop exercises with your team, using scenarios tailored to your industry and risk profile. Exercises are documented with findings and action items, producing the evidence that auditors require.

**Evidence integration.** Incident response evidence -- detection logs, response actions, post-incident reviews -- is integrated into QuickTrust's continuous compliance platform, so it is always available for audit and mapped to the specific framework controls it satisfies.

The result is an incident response capability that is operational from day one, produces audit-ready evidence automatically, and satisfies SOC 2, ISO 27001, HIPAA, and PCI DSS requirements simultaneously.
