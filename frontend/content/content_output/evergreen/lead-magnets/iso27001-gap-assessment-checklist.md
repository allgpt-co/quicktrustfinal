---
meta_description: "ISO 27001 gap assessment checklist covering 150 controls across 14 domains mapped to Annex A. Assess your ISMS readiness."
target_keyword: "iso 27001 gap assessment checklist, iso 27001 gap analysis"
secondary_keywords: "iso 27001 checklist, iso 27001 annex a checklist, isms gap assessment, iso 27001 readiness checklist"
word_count_target: "2000"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# ISO 27001 Gap Assessment Checklist
## 150 Controls Across 14 Domains

**Prepared by QuickTrust | trust.quickintell.com**
*AI-Powered GRC Platform + Expert Engineering Implementation*

---

## How to Use This Checklist

This checklist maps to **ISO/IEC 27001:2013 Annex A** — the 114 controls across 14 domains that form the backbone of any ISO 27001 Information Security Management System (ISMS). Use it to assess your current state before beginning a formal certification engagement.

**For each control, mark one of:**
- `✅ Implemented` — Control is fully documented, implemented, and operating effectively with evidence
- `⚠️ Partial` — Control exists but is incomplete, inconsistently applied, or lacks documentation
- `❌ Not Implemented` — No control exists; significant gap requiring remediation
- `N/A` — Control is not applicable to your organization (document justification in your Statement of Applicability)

**After completing each domain, record:**
- Number of controls fully implemented
- Number partially implemented
- Number not implemented / not applicable

**Use your results to:**
1. Build your Statement of Applicability (SoA)
2. Prioritize your gap remediation roadmap
3. Estimate your readiness for a Stage 1 (documentation) and Stage 2 (implementation) audit

> **Important:** ISO 27001 certification requires that controls be implemented AND operating effectively with documented evidence over time. "Implemented" means you can prove it — not just that you believe it exists.

---

## Domain A.5: Information Security Policies
*Controls: A.5.1.1, A.5.1.2*

### A.5.1 Management Direction for Information Security

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.5.1.1 | **Policies for information security** — A set of policies for information security shall be defined, approved by management, published, and communicated to employees and relevant external parties | Signed policy document; distribution records; acknowledgment sign-offs; version history | Policies exist but have never been formally approved by leadership or distributed with documented acknowledgment | ☐ |
| A.5.1.2 | **Review of the policies for information security** — The policies for information security shall be reviewed at scheduled intervals or if significant changes occur, to ensure their continuing suitability, adequacy, and effectiveness | Review meeting minutes or email approval trail; version history showing annual reviews; updated effective dates | Policies were written once at the start and never reviewed or updated; no evidence of annual review | ☐ |

**Domain A.5 Score: \_\_\_ / 2 implemented**

---

## Domain A.6: Organization of Information Security
*Controls: A.6.1.1 – A.6.2.2*

### A.6.1 Internal Organization

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.6.1.1 | **Information security roles and responsibilities** — All information security responsibilities shall be defined and allocated | RACI matrix or role description documents; org chart showing security roles; job descriptions with security responsibilities | Security responsibilities are informally understood but never formally documented; no RACI exists | ☐ |
| A.6.1.2 | **Segregation of duties** — Conflicting duties and areas of responsibility shall be segregated to reduce opportunities for unauthorized or unintentional modification or misuse of the organization's assets | Evidence of access control configuration preventing one person from performing conflicting actions; documented role segregation | Single individuals have ability to initiate and approve changes, or develop and deploy code to production | ☐ |
| A.6.1.3 | **Contact with authorities** — Appropriate contacts with relevant authorities shall be maintained | Documented contacts for law enforcement, regulatory bodies, CISA/CERT; incident notification procedures referencing relevant authorities | No documented process for contacting law enforcement or regulatory bodies during a security incident | ☐ |
| A.6.1.4 | **Contact with special interest groups** — Appropriate contacts with special interest groups or other specialist security forums and professional associations shall be maintained | Membership or subscription records for threat intelligence feeds, ISACs, security mailing lists | No subscriptions to security bulletins, threat feeds, or industry groups relevant to the company's sector | ☐ |
| A.6.1.5 | **Information security in project management** — Information security shall be addressed in project management, regardless of the type of project | Project templates including security checkpoints; evidence of security reviews in project documentation | Security reviews are not included in project management methodology; no security sign-off at project milestones | ☐ |

### A.6.2 Mobile Devices and Teleworking

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.6.2.1 | **Mobile device policy** — A policy and supporting security measures shall be adopted to manage the risks introduced by using mobile devices | Mobile device / BYOD policy; MDM enrollment records; device compliance reports | No MDM platform; personal devices access company email and data without any security configuration requirements | ☐ |
| A.6.2.2 | **Teleworking** — A policy and supporting security measures shall be implemented to protect information accessed, processed, or stored at teleworking sites | Remote work security policy; VPN usage logs; evidence of remote worker security training | No formal remote work policy; employees work from home without VPN or device security requirements | ☐ |

**Domain A.6 Score: \_\_\_ / 7 implemented**

---

## Domain A.7: Human Resource Security
*Controls: A.7.1.1 – A.7.3.1*

### A.7.1 Prior to Employment

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.7.1.1 | **Screening** — Background verification checks on all candidates for employment shall be carried out in accordance with relevant laws, regulations, and ethics | Background check policy; vendor invoices or results (redacted); evidence screening is role-adjusted for sensitive positions | Background checks are done inconsistently or only for certain roles; no documentation of scope | ☐ |
| A.7.1.2 | **Terms and conditions of employment** — The contractual agreements with employees and contractors shall state their and the organization's responsibilities for information security | Employment contracts with information security obligations; contractor agreements with NDA and AUP acknowledgment | Contracts don't include information security obligations; no AUP acknowledgment at hire | ☐ |

### A.7.2 During Employment

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.7.2.1 | **Management responsibilities** — Management shall require all employees and contractors to apply information security in accordance with the established policies and procedures | Manager training records; evidence of manager accountability in performance frameworks | Managers have no documented security accountability; security is considered only an IT function | ☐ |
| A.7.2.2 | **Information security awareness, education, and training** — All employees and contractors shall receive appropriate security awareness education and training, with regular updates | Training platform records showing completion rates; training content covering relevant topics; annual recertification records | Training is done at onboarding only; no annual refresher; completion not tracked | ☐ |
| A.7.2.3 | **Disciplinary process** — There shall be a formal and communicated disciplinary process in place to take action against employees who have committed an information security breach | HR policy referencing information security violations; documented disciplinary process communicated to all staff | The disciplinary process doesn't mention information security violations; no consequence framework exists | ☐ |

### A.7.3 Termination and Change of Employment

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.7.3.1 | **Termination or change of employment responsibilities** — Information security responsibilities and duties that remain valid after termination or change of employment shall be defined, communicated to the employee or contractor, and enforced | Offboarding checklist with access revocation steps; exit documentation including confidentiality reminders; access revocation records with timestamps | No formal offboarding process; access revocation is ad hoc and often delayed days or weeks | ☐ |

**Domain A.7 Score: \_\_\_ / 6 implemented**

---

## Domain A.8: Asset Management
*Controls: A.8.1.1 – A.8.3.3*

### A.8.1 Responsibility for Assets

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.8.1.1 | **Inventory of assets** — Assets associated with information and information processing facilities shall be identified and an inventory of these assets shall be drawn up and maintained | Asset register with asset type, owner, classification, location, and status; evidence of regular updates | No formal asset inventory; assets are tracked in various spreadsheets or not at all; cloud assets untracked | ☐ |
| A.8.1.2 | **Ownership of assets** — Assets maintained in the inventory shall be owned | Asset register showing named owner for each asset; evidence owners accept responsibility | Assets exist in inventory but have no named owner; shared ownership means no one is accountable | ☐ |
| A.8.1.3 | **Acceptable use of assets** — Rules for the acceptable use of information and of assets associated with information and information processing facilities shall be identified, documented, and implemented | Acceptable Use Policy communicated to all staff; acknowledgment records | AUP exists but employees haven't signed it or been trained on it | ☐ |
| A.8.1.4 | **Return of assets** — All employees and contractors shall return all of the organizational assets in their possession upon termination of their employment, contract, or agreement | Offboarding checklist confirming device and asset return; signed asset return confirmation | Devices and access cards are not formally returned upon termination; no tracking | ☐ |

### A.8.2 Information Classification

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.8.2.1 | **Classification of information** — Information shall be classified in terms of legal requirements, value, criticality, and sensitivity to unauthorized disclosure or modification | Data Classification Policy with defined tiers; evidence that assets are labeled per classification | Classification policy exists on paper but isn't applied; data assets have no labels or tags | ☐ |
| A.8.2.2 | **Labeling of information** — An appropriate set of procedures for information labeling shall be developed and implemented in accordance with the information classification scheme | Labeling standards; evidence of labels applied to documents, email headers, storage buckets | No labeling system in use; classified documents are indistinguishable from public ones | ☐ |
| A.8.2.3 | **Handling of assets** — Procedures for handling assets shall be developed and implemented in accordance with the information classification scheme | Handling procedures per classification tier; evidence of enforcement | Classification framework defines tiers but provides no specific handling instructions | ☐ |

### A.8.3 Media Handling

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.8.3.1 | **Management of removable media** — Procedures shall be implemented for the management of removable media in accordance with the classification scheme | Removable media policy; technical controls blocking unauthorized USB devices; exception logs | No controls on USB usage; employees freely use personal USB drives on company devices | ☐ |
| A.8.3.2 | **Disposal of media** — Media shall be disposed of securely when no longer required, using formal procedures | Media disposal records; vendor certificates of destruction; secure shredding invoices | Old hard drives and laptops are disposed of without secure wiping; no disposal records | ☐ |
| A.8.3.3 | **Physical media transfer** — Media containing information shall be protected against unauthorized access, misuse, or corruption during transportation | Procedures for secure physical transfer; courier service records with chain of custody | No documented procedures for transferring physical media; no chain-of-custody process | ☐ |

**Domain A.8 Score: \_\_\_ / 10 implemented**

---

## Domain A.9: Access Control
*Controls: A.9.1.1 – A.9.4.5*

### A.9.1 Business Requirements of Access Control

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.9.1.1 | **Access control policy** — An access control policy shall be established, documented, and reviewed based on business and information security requirements | Documented Access Control Policy; evidence of annual review; management approval | No formal access control policy; access decisions are made ad hoc | ☐ |
| A.9.1.2 | **Access to networks and network services** — Users shall only be provided with access to the network and network services that they have been specifically authorized to use | Network access authorization records; firewall rules showing segmentation; VPN access controls | All employees have unrestricted network access; no segmentation between production and office networks | ☐ |

### A.9.2 User Access Management

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.9.2.1 | **User registration and de-registration** — A formal user registration and de-registration process shall be implemented to enable assignment of access rights | Onboarding/offboarding checklists with access steps; IAM provisioning/deprovisioning logs with timestamps | Access provisioning happens informally via Slack; no formal request, approval, or documentation process | ☐ |
| A.9.2.2 | **User access provisioning** — A formal user access provisioning process shall be implemented to assign or revoke access rights for all user types to all systems and services | Access request tickets with documented approval; access provisioning logs | Access is granted without formal approval; manager approval is verbal and not recorded | ☐ |
| A.9.2.3 | **Management of privileged access rights** — The allocation and use of privileged access rights shall be restricted and controlled | Privileged account inventory; PAM solution logs; quarterly review records | Privileged accounts are not inventoried; multiple people share admin credentials | ☐ |
| A.9.2.4 | **Management of secret authentication information of users** — The allocation of secret authentication information shall be controlled through a formal management process | Password manager deployment evidence; policy prohibiting password sharing; service account credential management records | Passwords are shared via email or Slack; no enterprise password manager; no service account rotation | ☐ |
| A.9.2.5 | **Review of user access rights** — Asset owners shall review users' access rights at regular intervals | Quarterly/semi-annual access review records; evidence of removals based on review | Access reviews have never been formally conducted; accounts accumulate access over time | ☐ |
| A.9.2.6 | **Removal or adjustment of access rights** — The access rights of all employees and contractors to information and information processing facilities shall be removed upon termination of their employment, contract, or agreement | Offboarding checklist with access revocation steps completed; IAM logs showing deprovisioning timestamps | Former employees' accounts remain active for days or weeks after termination | ☐ |

### A.9.3 User Responsibilities

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.9.3.1 | **Use of secret authentication information** — Users shall be required to follow the organization's practices in the use of secret authentication information | Password policy communicated to all staff; training records covering password requirements; acknowledgment | Password policy exists but was never communicated to employees; no training on password hygiene | ☐ |

### A.9.4 System and Application Access Control

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.9.4.1 | **Information access restriction** — Access to information and application system functions shall be restricted in accordance with the access control policy | Role-based access control (RBAC) configuration; evidence of least-privilege principle applied in IAM | All users have the same access level; no role-based permissions; "admin by default" configurations | ☐ |
| A.9.4.2 | **Secure log-on procedures** — Where required by the access control policy, access to systems and applications shall be controlled by a secure log-on procedure | MFA enrollment evidence; login attempt limits configured; MFA policy screenshots | MFA is optional; many accounts have single-factor authentication; no account lockout after failed attempts | ☐ |
| A.9.4.3 | **Password management system** — Password management systems shall be interactive and shall ensure quality passwords | Password manager deployment; system-enforced complexity and length requirements; configuration screenshots | Passwords are managed in spreadsheets or stored in browser; no enterprise password manager | ☐ |
| A.9.4.4 | **Use of privileged utility programs** — The use of utility programs that might be capable of overriding system and application controls shall be restricted and tightly controlled | Privileged utility access logs; documented approval process for use; restricted access list | System utilities are available to all users; no logging of utility usage; no approval process | ☐ |
| A.9.4.5 | **Access control to program source code** — Access to program source code shall be restricted | Repository access control settings; branch protection rules; access review records for code repositories | Source code repositories are open to all employees; no branch protection; no access reviews | ☐ |

**Domain A.9 Score: \_\_\_ / 14 implemented**

---

## Domain A.10: Cryptography
*Controls: A.10.1.1 – A.10.1.2*

### A.10.1 Cryptographic Controls

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.10.1.1 | **Policy on the use of cryptographic controls** — A policy on the use of cryptographic controls for protection of information shall be developed and implemented | Encryption policy document; evidence of application to data-at-rest and in-transit; management approval | No formal encryption policy; encryption decisions are made on a per-project basis with no standards | ☐ |
| A.10.1.2 | **Key management** — A policy on the use, protection, and lifetime of cryptographic keys shall be developed and implemented through their whole lifecycle | Key management policy; KMS or vault deployment evidence; key rotation logs; access controls for keys | Encryption keys are hardcoded in application config files or environment variables; no rotation history | ☐ |

**Domain A.10 Score: \_\_\_ / 2 implemented**

---

## Domain A.11: Physical and Environmental Security
*Controls: A.11.1.1 – A.11.2.9*

### A.11.1 Secure Areas

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.11.1.1 | **Physical security perimeter** — Security perimeters shall be defined and used to protect areas that contain either sensitive or critical information and information processing facilities | Physical access control system documentation; badge reader logs; facility security diagram | Office has no physical access control; anyone can enter the building or server room | ☐ |
| A.11.1.2 | **Physical entry controls** — Secure areas shall be protected by appropriate entry controls to ensure that only authorized personnel are allowed access | Access control logs; visitor management records; access rights inventory | No visitor log; visitors freely walk to any area of the office without escort | ☐ |
| A.11.1.3 | **Securing offices, rooms, and facilities** — Physical security for offices, rooms, and facilities shall be designed and applied | Evidence that sensitive areas (server rooms, archives) have additional locks; key management records | Server equipment is in an unlocked room accessible to all employees | ☐ |
| A.11.1.4 | **Protecting against external and environmental threats** — Physical protection against natural disasters, malicious attack, or accidents shall be designed and applied | Risk assessment addressing environmental threats; fire suppression, flood protection, power protection evidence | No environmental controls assessed or documented; equipment unprotected from water, fire, or power fluctuations | ☐ |
| A.11.1.5 | **Working in secure areas** — Procedures for working in secure areas shall be designed and applied | Secure area procedures; evidence of clean desk enforcement; prohibition of unauthorized devices in secure areas | No procedures govern behavior in server room; no rules about devices or photography | ☐ |
| A.11.1.6 | **Delivery and loading areas** — Access points such as delivery and loading areas and other points where unauthorized persons could enter the premises shall be controlled | Delivery procedures; evidence that deliveries are managed by authorized personnel only | No controls on deliveries; packages arrive without security screening or authorization | ☐ |

### A.11.2 Equipment Security

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.11.2.1 | **Equipment siting and protection** — Equipment shall be sited and protected to reduce the risks from environmental threats and hazards, and opportunities for unauthorized access | Equipment placement documentation; evidence of physical security measures for servers and workstations | Equipment is placed without consideration of environmental risks or visibility from unsecured areas | ☐ |
| A.11.2.2 | **Supporting utilities** — Equipment shall be protected from power failures and other disruptions caused by failures in supporting utilities | UPS installation evidence; generator maintenance records; utility failure procedures | No UPS or power conditioning; a power surge could destroy equipment and data | ☐ |
| A.11.2.3 | **Cabling security** — Power and telecommunications cabling carrying data or supporting information services shall be protected from interception, interference, or damage | Cable management documentation; evidence of protected cabling runs; network diagram | Network cables are accessible and unsecured; no documentation of cable routes | ☐ |
| A.11.2.4 | **Equipment maintenance** — Equipment shall be correctly maintained to ensure its continued availability and integrity | Hardware maintenance schedule; vendor maintenance contracts; service records | No maintenance schedule; hardware is only serviced when it breaks | ☐ |
| A.11.2.5 | **Removal of assets** — Equipment, information, or software shall not be taken off-site without prior authorization | Asset removal authorization process; asset register showing location; return confirmation records | Employees take laptops and equipment home without any logging or authorization | ☐ |
| A.11.2.6 | **Security of equipment and assets off-premises** — Security shall be applied to off-site assets taking into account the different risks of working outside the organization's premises | Remote work and mobile device policy; MDM enrollment for off-site devices | No security requirements for equipment used outside the office | ☐ |
| A.11.2.7 | **Secure disposal or reuse of equipment** — All items of equipment containing storage media shall be verified to ensure that any sensitive data and licensed software has been removed or securely overwritten prior to disposal or reuse | Equipment disposal records; secure wipe certificates; certificates of destruction for decommissioned hardware | Old devices are donated or discarded without wiping; former employee data at risk | ☐ |
| A.11.2.8 | **Unattended user equipment** — Users shall ensure that unattended equipment has appropriate protection | Screen lock policy; evidence of automatic screen lock configured; clean desk reminders | Computers are left unlocked and unattended; no screen lock timeout configured | ☐ |
| A.11.2.9 | **Clear desk and clear screen policy** — A clear desk policy for papers and removable storage media and a clear screen policy for information processing facilities shall be adopted | Clear desk/screen policy; evidence of employee acknowledgment; spot check records | No clear desk policy; sensitive documents visible on desks; screens unlocked in public view | ☐ |

**Domain A.11 Score: \_\_\_ / 15 implemented**

---

## Domain A.12: Operations Security
*Controls: A.12.1.1 – A.12.7.1*

### A.12.1 Operational Procedures and Responsibilities

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.12.1.1 | **Documented operating procedures** — Operating procedures shall be documented and made available to all users who need them | Documented runbooks and SOPs; evidence of availability to relevant staff | Procedures exist only in engineers' heads; no written runbooks or SOPs | ☐ |
| A.12.1.2 | **Change management** — Changes to the organization, business processes, information processing facilities, and systems that affect information security shall be controlled | Change management policy; ticketing system records of approved and completed changes; CAB meeting minutes | Changes are deployed to production without documentation, review, or approval | ☐ |
| A.12.1.3 | **Capacity management** — The use of resources shall be monitored, tuned, and projections made of future capacity requirements to ensure the required system performance | Capacity monitoring dashboards; alerts for resource thresholds; capacity planning documentation | No capacity monitoring; system performance issues are discovered only when users complain | ☐ |
| A.12.1.4 | **Separation of development, testing, and operational environments** — Development, testing, and operational environments shall be separated to reduce the risks of unauthorized access or changes to the operational environment | Environment separation architecture diagram; evidence of access controls per environment; no production data in dev | Developers have direct production access; production data used in testing environments | ☐ |

### A.12.2 Protection from Malware

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.12.2.1 | **Controls against malware** — Detection, prevention, and recovery controls to protect against malware shall be implemented, combined with appropriate user awareness | EDR/antivirus deployment evidence; coverage report showing all endpoints protected; alert and response logs | No endpoint protection on developer machines; basic antivirus but no EDR; no monitoring of alerts | ☐ |

### A.12.3 Backup

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.12.3.1 | **Information backup** — Backup copies of information, software, and system images shall be taken and tested regularly in accordance with an agreed backup policy | Backup policy; automated backup configuration evidence; restoration test results with timestamps | Backups are configured but never tested; no evidence restoration actually works | ☐ |

### A.12.4 Logging and Monitoring

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.12.4.1 | **Event logging** — Event logs recording user activities, exceptions, faults, and information security events shall be produced, kept, and regularly reviewed | SIEM or log aggregation configuration; sample log output; retention configuration | Logs are generated but not centralized; application logs are on individual servers with no central access | ☐ |
| A.12.4.2 | **Protection of log information** — Logging facilities and log information shall be protected against tampering and unauthorized access | Log integrity controls; restricted access to log management systems; immutable log storage configuration | Logs can be deleted by the same administrators who generate them; no tamper protection | ☐ |
| A.12.4.3 | **Administrator and operator logs** — System administrator and system operator activities shall be logged and the logs protected and regularly reviewed | Admin activity logs; evidence of separate logging for privileged users; quarterly review records | No separate logging for admin actions; privileged user activity is indistinguishable from regular users in logs | ☐ |
| A.12.4.4 | **Clock synchronisation** — The clocks of all relevant information processing systems within an organization or security domain shall be synchronised to a single reference time source | NTP configuration evidence; synchronized clock verification across systems | Systems use different time sources; log timestamps don't match, making incident investigation difficult | ☐ |

### A.12.5 Control of Operational Software

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.12.5.1 | **Installation of software on operational systems** — Procedures shall be implemented to control the installation of software on operational systems | Software installation policy; evidence of approved software list; technical controls preventing unauthorized installation | Anyone can install any software on company devices; no approved software list exists | ☐ |

### A.12.6 Technical Vulnerability Management

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.12.6.1 | **Management of technical vulnerabilities** — Information about technical vulnerabilities of information systems being used shall be obtained in a timely fashion, the organization's exposure to such vulnerabilities evaluated, and appropriate measures taken to address the associated risk | Vulnerability scanning reports; patch management records; vulnerability register with remediation status and due dates | No vulnerability scanning; patches applied only when convenient, not based on severity | ☐ |
| A.12.6.2 | **Restrictions on software installation** — Rules governing the installation of software by users shall be established and implemented | MDM or endpoint management configuration preventing unauthorized installation; software whitelist | Users have local admin rights and can install any software without restriction | ☐ |

### A.12.7 Information Systems Audit Considerations

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.12.7.1 | **Information systems audit controls** — Audit requirements and activities involving verification of operational systems shall be carefully planned and agreed to minimize disruptions to business processes | Audit planning documents; coordination with system owners before audits; audit activity logs | Audits are conducted without coordination with business teams; no documented audit activity logs | ☐ |

**Domain A.12 Score: \_\_\_ / 14 implemented**

---

## Domain A.13: Communications Security
*Controls: A.13.1.1 – A.13.2.4*

### A.13.1 Network Security Management

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.13.1.1 | **Network controls** — Networks shall be managed and controlled to protect information in systems and applications | Network security architecture; firewall rules review; network segmentation documentation | Flat network with no segmentation; all systems can communicate with all other systems | ☐ |
| A.13.1.2 | **Security of network services** — Security mechanisms, service levels, and management requirements of all network services shall be identified and included in network services agreements | Network service agreements with security terms; SLA documentation; review of provider security controls | Cloud provider contracts don't include security terms; no SLA for security events | ☐ |
| A.13.1.3 | **Segregation in networks** — Groups of information services, users, and information systems shall be segregated on networks | Network segmentation architecture; VLAN configuration; firewall rules between segments | Production and development share the same network; no separation between sensitive and non-sensitive systems | ☐ |

### A.13.2 Information Transfer

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.13.2.1 | **Information transfer policies and procedures** — Formal transfer policies, procedures, and controls shall be in place to protect the transfer of information through the use of all types of communication facilities | Data transfer policy; approved file sharing platforms; email security configuration | No policy governing how data is shared; employees use personal Dropbox or email attachments for sensitive data | ☐ |
| A.13.2.2 | **Agreements on information transfer** — Agreements shall address the secure transfer of business information between the organization and external parties | NDA and data transfer agreements with partners and customers; data processing agreements | Sensitive data is shared with partners without NDAs or data transfer agreements | ☐ |
| A.13.2.3 | **Electronic messaging** — Information involved in electronic messaging shall be appropriately protected | Email security controls (SPF, DKIM, DMARC); email encryption for sensitive communications; email DLP | No email authentication configured; DMARC not implemented; sensitive data sent in plaintext email | ☐ |
| A.13.2.4 | **Confidentiality or non-disclosure agreements** — Requirements for confidentiality or non-disclosure agreements reflecting the organization's needs for the protection of information shall be identified, regularly reviewed, and documented | NDA template; list of parties with executed NDAs; NDA review schedule | NDAs are not consistently used with contractors and vendors; no central NDA repository | ☐ |

**Domain A.13 Score: \_\_\_ / 7 implemented**

---

## Domain A.14: System Acquisition, Development and Maintenance
*Controls: A.14.1.1 – A.14.3.1*

### A.14.1 Security Requirements of Information Systems

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.14.1.1 | **Information security requirements analysis and specification** — The information security related requirements shall be included in the requirements for new information systems or enhancements to existing information systems | Security requirements in product specifications; evidence of security sign-off on project kick-offs | Security requirements are considered after development, not before | ☐ |
| A.14.1.2 | **Securing application services on public networks** — Information involved in application services passing over public networks shall be protected from fraudulent activity, contract dispute, and unauthorized disclosure and modification | TLS configuration; API authentication (OAuth, JWT); input validation controls | APIs exposed to the internet lack authentication; no TLS certificate rotation process | ☐ |
| A.14.1.3 | **Protecting application services transactions** — Information involved in application service transactions shall be protected to prevent incomplete transmission, misrouting, unauthorized message alteration, unauthorized disclosure, unauthorized message duplication, or replay | Transaction integrity controls; API payload validation; secure session management | No transaction integrity verification; sessions don't expire; no replay attack prevention | ☐ |

### A.14.2 Security in Development and Support Processes

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.14.2.1 | **Secure development policy** — Rules for the development of software and systems shall be established and applied to developments within the organization | Secure SDLC policy; developer security training records; code review requirements documentation | No secure coding standards; security is not part of the development workflow | ☐ |
| A.14.2.2 | **System change control procedures** — Changes to systems within the development lifecycle shall be controlled by the use of formal change control procedures | Change management records in version control or ticketing system; PR review history | Code goes directly to production without review or change management documentation | ☐ |
| A.14.2.3 | **Technical review of applications after operating platform changes** — When operating platforms are changed, business critical applications shall be reviewed and tested to ensure there is no adverse impact on organizational operations or security | Platform change review records; post-change testing results; documented sign-offs | Platform upgrades happen without security review of application compatibility | ☐ |
| A.14.2.4 | **Restrictions on changes to software packages** — Modifications to software packages shall be discouraged, limited to necessary changes, and all changes shall be strictly controlled | Policy on third-party software modification; change records for any package modifications | Third-party code is modified without documentation; no process for tracking modified packages | ☐ |
| A.14.2.5 | **Secure system engineering principles** — Principles for engineering secure systems shall be established, documented, maintained, and applied to any information system implementation efforts | Documented secure engineering principles; evidence applied in system design; threat modeling records | No security architecture principles; design decisions made without security consideration | ☐ |
| A.14.2.6 | **Secure development environment** — Organizations shall establish and appropriately protect secure development environments for system development and maintenance efforts that cover the entire system development lifecycle | Development environment security controls; evidence of environment access restrictions | Developers have production access; development environments lack security controls | ☐ |
| A.14.2.7 | **Outsourced development** — The organization shall supervise and monitor the activity of outsourced system development | Vendor contracts with security requirements; outsourced code review process; acceptance testing records | External developers have no security requirements in their contracts; code is not reviewed before acceptance | ☐ |
| A.14.2.8 | **System security testing** — Testing of security functionality shall be carried out during development | SAST scan results; security test cases in QA process; evidence of security testing as part of release | No security testing in CI/CD pipeline; security is tested manually only before major releases | ☐ |
| A.14.2.9 | **System acceptance testing** — Acceptance testing programs and related criteria shall be established for new information systems, upgrades, and new versions | Acceptance test plans including security criteria; sign-off records before production deployment | Acceptance testing has no security criteria; systems go live based on functional testing only | ☐ |

### A.14.3 Test Data

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.14.3.1 | **Protection of test data** — Test data shall be selected carefully, protected, and controlled | Policy prohibiting production data in test environments; evidence of data masking/anonymization; test data management records | Production databases are copied to development environments; real customer data used for testing | ☐ |

**Domain A.14 Score: \_\_\_ / 13 implemented**

---

## Domain A.15: Supplier Relationships
*Controls: A.15.1.1 – A.15.2.2*

### A.15.1 Information Security in Supplier Relationships

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.15.1.1 | **Information security policy for supplier relationships** — Information security requirements for mitigating the risks associated with supplier's access to the organization's assets shall be agreed with the supplier and documented | Vendor management policy; security addendum template used in contracts | No security requirements in supplier contracts; vendors onboarded without security review | ☐ |
| A.15.1.2 | **Addressing security within supplier agreements** — All relevant information security requirements shall be established and agreed with each supplier that may access, process, store, communicate, or provide IT infrastructure components for, the organization's information | Supplier contracts with security clauses; DPA/BAA agreements; evidence of negotiated security terms | Standard vendor contracts don't include security terms; no DPAs executed with data processors | ☐ |
| A.15.1.3 | **Information and communication technology supply chain** — Agreements with suppliers shall include requirements to address the information security risks associated with information and communications technology services and product supply chain | Supply chain risk assessment; software bill of materials (SBOM); vendor security review records | No visibility into supply chain security; third-party components used without vetting | ☐ |

### A.15.2 Supplier Service Delivery Management

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.15.2.1 | **Monitoring and review of supplier services** — Organizations shall regularly monitor, review, and audit supplier service delivery | Annual vendor review records; SOC 2 report review evidence; vendor performance assessments | Vendors are never reviewed after onboarding; no process for annual reassessment | ☐ |
| A.15.2.2 | **Managing changes to supplier services** — Changes to the provision of services by suppliers, including maintaining and improving existing information security policies, procedures, and controls, shall be managed, taking account of the criticality of business information, systems, and processes involved | Supplier change notification records; change impact assessment for supplier changes | No process for evaluating security impact of vendor-side changes to services or personnel | ☐ |

**Domain A.15 Score: \_\_\_ / 5 implemented**

---

## Domain A.16: Information Security Incident Management
*Controls: A.16.1.1 – A.16.1.7*

### A.16.1 Management of Information Security Incidents and Improvements

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.16.1.1 | **Responsibilities and procedures** — Management responsibilities and procedures shall be established to ensure a quick, effective, and orderly response to information security incidents | Incident Response Plan; defined roles and responsibilities; escalation path documentation | No formal IRP; incident response is improvised; no defined roles or escalation paths | ☐ |
| A.16.1.2 | **Reporting information security events** — Information security events shall be reported through appropriate management channels as quickly as possible | Incident reporting channel (e.g., security@company.com); employee training on reporting; evidence of reports received | Employees don't know how to report a security event; no reporting channel published | ☐ |
| A.16.1.3 | **Reporting information security weaknesses** — Employees and contractors using the organization's information systems and services shall be required to note and report any observed or suspected information security weaknesses in systems or services | Policy requiring weakness reporting; reporting channel for vulnerabilities; evidence of reports investigated | No responsible disclosure policy; employees have no channel to report suspected security weaknesses | ☐ |
| A.16.1.4 | **Assessment of and decision on information security events** — Information security events shall be assessed and it shall be decided if they are to be classified as information security incidents | Incident classification criteria; evidence of triage process; incident log with classification decisions | Security events aren't formally assessed; there's no consistent threshold for escalating to an incident | ☐ |
| A.16.1.5 | **Response to information security incidents** — Information security incidents shall be responded to in accordance with the documented procedures | Incident response records showing containment, eradication, recovery steps; timestamps; communications records | When incidents occur, response is undocumented; no record of actions taken | ☐ |
| A.16.1.6 | **Learning from information security incidents** — Knowledge gained from analysing and resolving information security incidents shall be used to reduce the likelihood or impact of future incidents | Post-incident review records; evidence that lessons learned drove policy or control changes | No post-mortem process; same incidents recur because root causes aren't fixed | ☐ |
| A.16.1.7 | **Collection of evidence** — The organization shall define and apply procedures for the identification, collection, acquisition, and preservation of information, which can serve as evidence | Evidence preservation procedures; chain of custody records; forensic capability documentation | No evidence preservation protocol; forensic evidence is often destroyed or contaminated during incident response | ☐ |

**Domain A.16 Score: \_\_\_ / 7 implemented**

---

## Domain A.17: Business Continuity Management
*Controls: A.17.1.1 – A.17.2.1*

### A.17.1 Information Security Continuity

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.17.1.1 | **Planning information security continuity** — The organization shall determine its requirements for information security and the continuity of information security management in adverse situations, e.g. during a crisis or disaster | BCP/DRP documentation addressing information security requirements; integration with business continuity planning | No BCP/DRP; the company has never formally considered what happens during a major disruption | ☐ |
| A.17.1.2 | **Implementing information security continuity** — The organization shall establish, document, implement, and maintain processes, procedures, and controls to ensure the required level of continuity for information security during an adverse situation | Implemented backup and DR infrastructure; documented recovery procedures; RTO/RPO documentation | BCP exists on paper but recovery procedures are never tested; actual recovery capability unknown | ☐ |
| A.17.1.3 | **Verify, review, and evaluate information security continuity** — The organization shall verify the established and implemented information security continuity controls at regular intervals in order to ensure that they are valid and effective during adverse situations | Annual BCP/DR test records; tabletop exercise documentation; backup restoration test results | BCP/DRP has never been tested; there's no evidence the documented recovery steps actually work | ☐ |

### A.17.2 Redundancies

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.17.2.1 | **Availability of information processing facilities** — Information processing facilities shall be implemented with redundancy sufficient to meet availability requirements | Architecture documentation showing redundancy; multi-AZ or multi-region deployment evidence; uptime monitoring records | Single points of failure in infrastructure; no redundancy for critical systems; SLA commitments not backed by infrastructure | ☐ |

**Domain A.17 Score: \_\_\_ / 4 implemented**

---

## Domain A.18: Compliance
*Controls: A.18.1.1 – A.18.2.3*

### A.18.1 Compliance with Legal and Contractual Requirements

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.18.1.1 | **Identification of applicable legislation and contractual requirements** — All relevant legislative statutory, regulatory, and contractual requirements and the organization's approach to meet these requirements shall be explicitly identified, documented, and kept up to date for each information system and the organization | Legal register documenting applicable laws and regulations; contractual obligation tracking; evidence of annual review | No formal legal register; compliance obligations are tracked informally or not at all | ☐ |
| A.18.1.2 | **Intellectual property rights** — Appropriate procedures shall be implemented to ensure compliance with legislative, regulatory, and contractual requirements related to intellectual property rights and use of proprietary software products | Software license inventory; policy prohibiting use of unlicensed software; license compliance audit records | No software license inventory; unlicensed software found on company devices; no policy | ☐ |
| A.18.1.3 | **Protection of records** — Records shall be protected from loss, destruction, falsification, unauthorized access, and unauthorized release, in accordance with legislative, statutory, regulatory, and contractual requirements | Records retention policy; data classification applied to records; access controls; backup confirmation | No records retention policy; records deleted without regard for legal retention requirements | ☐ |
| A.18.1.4 | **Privacy and protection of personally identifiable information** — Privacy and protection of personally identifiable information shall be ensured as required in relevant legislation and regulations where applicable | Privacy policy; data mapping of PII flows; GDPR/CCPA compliance records; DPA agreements with processors | No data mapping of PII; privacy policy not updated for GDPR/CCPA; no DPAs with processors | ☐ |
| A.18.1.5 | **Regulation of cryptographic controls** — Cryptographic controls shall be used in compliance with all relevant agreements, laws, and regulations | Evidence that encryption practices comply with applicable regulations; review of export control requirements | No review of cryptography regulatory requirements; encryption algorithms used without considering compliance | ☐ |

### A.18.2 Information Security Reviews

| # | Control | Evidence Required | Common Gap | Status |
|---|---------|------------------|-----------|--------|
| A.18.2.1 | **Independent review of information security** — The organization's approach to managing information security and its implementation (i.e. control objectives, controls, policies, processes, and procedures for information security) shall be reviewed independently at defined intervals or when significant changes occur | Internal audit records or external review report; evidence of independent review; management response to findings | No independent review of the security program has ever occurred; no internal audit function | ☐ |
| A.18.2.2 | **Compliance with security policies and standards** — Managers shall regularly review the compliance of information processing and procedures within their area of responsibility with the appropriate security policies, standards, and any other security requirements | Management review records; compliance audit results; corrective action tracking | Managers don't conduct compliance checks within their teams; no process exists | ☐ |
| A.18.2.3 | **Technical compliance review** — Information systems shall be regularly reviewed for compliance with the organization's information security policies and standards | Technical audit results; vulnerability scan reports; configuration compliance scanning; evidence of remediation | Technical systems have never been audited against security policy requirements | ☐ |

**Domain A.18 Score: \_\_\_ / 8 implemented**

---

## Overall Gap Assessment Summary

| Domain | Controls | Implemented | Partial | Not Implemented | N/A |
|--------|---------|-------------|---------|----------------|-----|
| A.5: Information Security Policies | 2 | | | | |
| A.6: Organization of Information Security | 7 | | | | |
| A.7: Human Resource Security | 6 | | | | |
| A.8: Asset Management | 10 | | | | |
| A.9: Access Control | 14 | | | | |
| A.10: Cryptography | 2 | | | | |
| A.11: Physical and Environmental Security | 15 | | | | |
| A.12: Operations Security | 14 | | | | |
| A.13: Communications Security | 7 | | | | |
| A.14: System Acquisition, Development and Maintenance | 13 | | | | |
| A.15: Supplier Relationships | 5 | | | | |
| A.16: Incident Management | 7 | | | | |
| A.17: Business Continuity Management | 4 | | | | |
| A.18: Compliance | 8 | | | | |
| **TOTAL** | **114** | | | | |

---

## Score Interpretation

**90–114 Implemented:** You are likely ready for an ISO 27001 Stage 1 audit. Engage a UKAS or IAF-accredited certification body and schedule your Stage 1 assessment.

**60–89 Implemented:** You have a solid foundation but material gaps to close before Stage 1. Prioritize the controls with the highest audit risk (A.9, A.12, A.16, A.18) and build your remediation roadmap with 60–90 day targets.

**30–59 Implemented:** Significant gaps across multiple domains. A structured implementation program with dedicated engineering resources is the fastest path to certification. Build your Statement of Applicability and gap assessment before attempting Stage 1.

**0–29 Implemented:** Pre-implementation stage. ISO 27001 will require a full ISMS build. This is achievable but requires a structured program with executive commitment and engineering resources. Start with A.5, A.6, A.9, and A.16 as your highest-priority domains.

---

## What Comes After This Checklist?

A gap assessment tells you where you stand. Closing the gaps requires implementation — and that's where most companies stall.

QuickTrust's engineers have implemented ISO 27001 controls across 100+ organizations, with a 100% audit pass rate. We don't just hand you a checklist. We implement the controls in your cloud, write your ISMS documentation, build your evidence library, and coordinate with your certification body — so you show up to Stage 1 ready.

**Book your free 20-minute ISO 27001 readiness call:**
[trust.quickintell.com](https://trust.quickintell.com)

*QuickTrust is an open-source, AI-powered GRC platform operated by GPT Innovations, Inc. This checklist is based on ISO/IEC 27001:2013 Annex A and is provided for informational purposes. Engage a qualified implementation partner for certification work.*

---

## Related Reading

- [The Complete Guide to ISO 27001 Certification](/blog/pillar-iso27001-complete-guide)
- [How Much Does ISO 27001 Certification Cost?](/blog/iso27001-certification-cost)

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "ISO 27001 Gap Assessment Checklist: 150 Controls Across 14 Domains",
  "description": "ISO 27001 gap assessment checklist covering 150 controls across 14 domains mapped to Annex A. Assess your ISMS readiness, build your Statement of Applicability, and prioritize remediation.",
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
