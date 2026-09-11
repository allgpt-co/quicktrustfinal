---
meta_description: "Complete guide to network segmentation for SOC 2, PCI DSS, HIPAA, and ISO 27001. Covers VPC design, micro-segmentation, and cloud implementation."
target_keyword: "network segmentation compliance"
secondary_keywords: "network segmentation, VPC design, PCI DSS segmentation, HIPAA network security, micro-segmentation, cloud network security"
word_count_target: "1800"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# Network Segmentation: The Complete Compliance Guide for SOC 2, PCI DSS, HIPAA, and ISO 27001

Network segmentation is the practice of dividing a network into isolated segments so that systems in one segment cannot freely communicate with those in another. In a compliance context, segmentation serves two purposes: it reduces the attack surface by containing breaches, and it reduces audit scope by isolating regulated data into defined boundaries.

For PCI DSS, proper segmentation can reduce the cardholder data environment (CDE) from the entire network to a single subnet. For HIPAA, segmenting ePHI systems from general infrastructure provides a defensible boundary. For SOC 2 and ISO 27001, segmentation demonstrates least privilege at the network level.

Despite its importance, segmentation is one of the most frequently misconfigured controls in cloud environments. This guide covers segmentation requirements across four major frameworks, cloud-specific implementation, and the evidence auditors expect.

---

## Why Segmentation Matters for Compliance

Every major compliance framework requires network-level access controls. The specific language varies, but the principle is consistent: systems containing sensitive data should be isolated from systems that do not need access to that data, and all network communication should follow the principle of least privilege.

Without segmentation, a single compromised system can reach every other system on the network, and the entire network is in audit scope. With proper segmentation, scope is limited to segments containing regulated data. This translates directly to lower audit costs, fewer controls to maintain, and a smaller attack surface.

---

## Framework Requirements for Network Segmentation

### PCI DSS v4.0

PCI DSS has the most explicit and detailed segmentation requirements of any major framework.

**Requirement 1.2:** Network security controls must restrict traffic between the CDE and all other networks to only what is necessary for cardholder data processing.

**Requirement 1.3:** Network security controls must be implemented between all wireless networks and the CDE.

**Requirement 1.4:** Connections between untrusted networks (including the internet) and CDE system components must be restricted.

**Scope implications:** Without segmentation, PCI DSS considers the entire network to be the CDE. Effective segmentation reduces scope to systems that process, store, or transmit cardholder data — plus connected systems.

**Segmentation validation:** PCI DSS requires validation at least every six months, including penetration testing confirming that systems outside the CDE cannot access systems inside it.

### HIPAA Security Rule

HIPAA does not use the term "network segmentation" explicitly, but several Security Rule provisions require it in practice.

**164.312(a)(1) — Access Control:** Implement technical controls to allow ePHI access only to authorized persons or programs. Network segmentation enforces this at the infrastructure level.

**164.312(e)(1) — Transmission Security:** Guard against unauthorized access to ePHI during transmission. Segmentation ensures ePHI traverses only authorized network paths.

**164.308(a)(4) — Information Access Management:** Authorize access to ePHI consistent with applicable requirements. Segmentation provides infrastructure-level enforcement.

### SOC 2 Trust Services Criteria

**CC6.1:** Implement logical access security infrastructure over protected information assets. Segmentation is a core component.

**CC6.6:** Protect against threats from sources outside system boundaries. Requires boundary protection including segmentation between internal and external networks.

**CC6.7:** Restrict transmission and movement of information to authorized users and processes. Segmentation controls data movement between network zones.

### ISO 27001 Annex A

**A.8.22 — Segregation of Networks:** Groups of information services, users, and information systems shall be segregated in networks. The most direct segmentation requirement in ISO 27001.

**A.8.20 — Network Security:** Networks shall be secured, managed, and controlled to protect information. Includes segmentation as a security control.

**A.8.21 — Security of Network Services:** Security mechanisms for network services shall be identified, implemented, and monitored.

---

## VPC Design and Subnet Strategies

In cloud environments, network segmentation starts with Virtual Private Cloud (VPC) architecture. A well-designed VPC structure enforces segmentation at the infrastructure level, making it significantly harder for misconfigurations to create unauthorized access paths.

### Multi-VPC Architecture

The most effective strategy uses separate VPCs for different trust levels:

| VPC | Purpose | Examples |
|---|---|---|
| Production VPC | Customer-serving workloads | Application servers, databases, API gateways |
| Staging/QA VPC | Pre-production testing | Staging environment, integration testing |
| Development VPC | Developer workloads | Development environments, sandboxes |
| Management VPC | Shared services | CI/CD, monitoring, logging, bastion hosts |
| Compliance VPC | Regulated data processing | PCI CDE, ePHI systems |

Each VPC operates as an isolated network. Inter-VPC communication requires explicit configuration — VPC peering, transit gateways, or private link connections — each controllable, logged, and auditable.

### Subnet Design Within VPCs

Within each VPC, subnets provide a second layer of segmentation:

**Public subnets:** Only for resources that must be directly accessible from the internet (load balancers, NAT gateways). No application servers or databases should reside in public subnets.

**Private application subnets:** Application servers, containers, and compute workloads. These subnets have no direct internet access — outbound traffic routes through NAT gateways.

**Private data subnets:** Databases, data warehouses, and persistent storage. These subnets have no internet access (inbound or outbound) and accept connections only from application subnets via specific ports.

**Management subnets:** Bastion hosts, CI/CD agents, and administrative access points. Isolated from both application and data subnets except for defined management ports.

---

## Security Groups vs. NACLs

Cloud providers offer two layers of network-level access control. Understanding the difference is critical for effective segmentation.

### Security Groups (Stateful)

Security groups act as virtual firewalls at the instance level. They are stateful — if inbound traffic is allowed, the outbound response is automatically permitted.

**Best practices for compliance:**

- Apply explicit allow rules only — all other traffic is denied by default.
- Allow traffic by specific port, protocol, and source. Never use 0.0.0.0/0 except for port 443 on public-facing load balancers.
- Reference security groups by ID rather than IP ranges for dynamic rule sets.
- Create separate security groups per application tier (web, application, database) with only required ports between tiers.

### Network ACLs (Stateless)

Network ACLs operate at the subnet level and are stateless — both inbound and outbound rules must be explicitly defined for traffic to flow. They provide a second layer of defense behind security groups.

**Best practices for compliance:**

- Use NACLs to enforce subnet-level boundaries that should never be crossed, regardless of security group configurations.
- Block all traffic between the data subnet and the public subnet at the NACL level — even if a security group misconfiguration occurs, the NACL prevents direct access.
- Log NACL deny events to detect unauthorized access attempts between network segments.

---

## Micro-Segmentation

Micro-segmentation extends segmentation to individual workloads, applying access policies based on workload identity rather than network location.

In Kubernetes environments, Network Policies control pod-to-pod communication. Without them, all pods communicate freely — a flat network that violates segmentation requirements. For compliance: default deny all ingress and egress per namespace, explicitly allow only required paths, isolate namespaces containing regulated data, and log denied events.

For service mesh environments (Istio, Linkerd), mutual TLS between services provides encryption in transit and identity-based access control, complementing network-level segmentation.

---

## Cloud-Specific Implementation

### AWS VPC

- **VPC Flow Logs:** Enable for all VPCs and subnets. Flow logs provide evidence of traffic patterns and are essential for demonstrating segmentation effectiveness.
- **Transit Gateway:** Centralize inter-VPC communication through a transit gateway with route tables that enforce which VPCs can communicate.
- **AWS PrivateLink:** Connect to AWS services (S3, SQS, KMS) through private endpoints without traffic traversing the internet.
- **AWS Network Firewall:** Stateful inspection and filtering at the VPC level for organizations requiring deep packet inspection.

### GCP VPC

- **Shared VPC:** Centralize network management in a host project while deploying workloads in service projects. Network administrators control segmentation; application teams deploy within defined boundaries.
- **VPC Firewall Rules:** Hierarchical firewall policies at the organization, folder, and project level. Use tags and service accounts to target rules dynamically.
- **Private Service Connect:** Connect to Google APIs and services through private endpoints.
- **VPC Flow Logs:** Enable on all subnets for traffic analysis and compliance evidence.

### Azure VNet

- **Virtual Network Peering:** Connect VNets with granular routing control. Peered VNets can be configured to block transitive routing.
- **Network Security Groups (NSGs):** Applied at the subnet or NIC level. Use Application Security Groups (ASGs) to group VMs logically and apply rules by application tier.
- **Azure Firewall:** Centralized network filtering with application-level rules and threat intelligence integration.
- **Private Endpoints:** Connect to Azure PaaS services (Azure SQL, Storage, Key Vault) through private IP addresses in your VNet.
- **NSG Flow Logs:** Enable for all NSGs and store in a Log Analytics Workspace for analysis and audit evidence.

---

## Evidence of Segmentation Effectiveness

Auditors do not take your word that segmentation is effective. They require evidence:

**Network architecture diagrams.** Detailed diagrams showing VPCs, subnets, security groups, NACLs, and data flows. Must accurately reflect the current state — outdated diagrams are a common finding.

**Firewall and security group rule exports.** Complete rule sets for all in-scope security groups and NACLs, verified for least privilege.

**Flow log analysis.** VPC or NSG flow logs showing traffic follows expected patterns. Denied traffic logs demonstrate active blocking of unauthorized communication.

**Penetration test results.** For PCI DSS, segmentation penetration testing is required every six months, confirming CDE isolation.

**Change management records.** Evidence that segmentation control changes follow the documented approval process.

---

## How QuickTrust Engineers Implement Segmentation

QuickTrust's engineering team designs and implements network segmentation architectures directly in your cloud environment. The implementation process follows a structured approach:

**Discovery and mapping.** Engineers map your current network architecture, identify all data flows, and classify systems by trust level and regulatory scope. This produces the baseline network architecture diagram.

**Design.** Based on your compliance requirements (PCI CDE isolation, ePHI segmentation, SOC 2 access controls), engineers design a VPC architecture with appropriate subnet tiers, security group rules, and NACL policies.

**Implementation.** Engineers implement the segmentation architecture using infrastructure as code (Terraform, CloudFormation, Pulumi) — ensuring that the configuration is version-controlled, repeatable, and auditable. Security groups, NACLs, firewall rules, and routing tables are all codified.

**Validation.** Engineers validate segmentation effectiveness through automated testing — confirming that systems in restricted segments cannot reach systems in other segments through unauthorized paths. Test results are documented as audit evidence.

**Monitoring.** QuickTrust configures flow log collection, analysis, and alerting for segmentation violations. Any traffic that crosses a segment boundary outside of defined rules triggers an alert for investigation.

The result is a segmentation architecture meeting every applicable framework's requirements, documented with audit evidence, and monitored for ongoing effectiveness. Internal engineering involvement is typically less than two hours.

---

## Conclusion

Network segmentation is not a nice-to-have security measure. It is a required control across SOC 2, PCI DSS, HIPAA, and ISO 27001, and it delivers one of the most favorable compliance cost-to-benefit ratios of any technical control. Proper segmentation reduces audit scope, limits breach impact, and provides a clear enforcement mechanism for the principle of least privilege at the network level.

In cloud environments, segmentation is easier because providers offer powerful tools (VPCs, security groups, NACLs) and harder because misconfigurations can be introduced at any time by any team member with cloud access. The solution is to codify segmentation in infrastructure as code, monitor for drift, and validate through regular testing.
