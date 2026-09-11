---
meta_description: "A technical guide mapping cloud security controls in AWS, GCP, and Azure to SOC 2, ISO 27001, HIPAA, and PCI DSS requirements."
target_keyword: cloud data security
secondary_keywords: data security in cloud computing, cloud security compliance, aws security, gcp security, azure security
word_count_target: 1800
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# Data Security in the Cloud: The Compliance Controls AWS, GCP, and Azure Customers Can't Skip

Choosing AWS, GCP, or Azure does not mean you are compliant. It means you are working with a platform that has been independently audited — the cloud provider holds their own SOC 2, ISO 27001, PCI DSS, and HIPAA certifications. But those certifications cover the cloud provider's infrastructure: the physical data centers, the hypervisor layer, the managed service controls. They do not cover what you build on top.

The AWS Shared Responsibility Model, the GCP shared security model, and Azure's equivalent all say the same thing: **the provider secures the cloud; you secure what is in the cloud.** Your IAM configuration, your encryption settings, your logging pipeline, your network segmentation — these are your responsibility, not Amazon's or Google's or Microsoft's.

Most cloud security audit findings trace back to one of seven control domains: identity and access management, multi-factor authentication, encryption at rest, encryption in transit, logging and audit trails, network security, and backup/disaster recovery. This guide maps each domain to what SOC 2, ISO 27001, HIPAA, and PCI DSS actually require — with specific service names and configurations for AWS, GCP, and Azure.

---

## The Shared Responsibility Model: What Cloud Providers Do and Do Not Cover

Before going into specific controls, understand exactly where the provider's responsibility ends.

| Security Domain | Cloud Provider Responsibility | Your Responsibility |
|---|---|---|
| Physical security | Data center access controls, environmental controls | None (fully managed) |
| Hypervisor / virtualization layer | Hypervisor isolation and security | None (fully managed) |
| Network infrastructure | Core network security, DDoS protection | VPC design, security groups, network ACLs, firewall rules |
| Managed service security | Internal security of managed services (RDS, S3, BigQuery) | Configuration of those services (encryption settings, access controls, logging) |
| IAM / access management | IAM service infrastructure | Creating users, roles, policies, and permission boundaries |
| Data encryption | Encryption infrastructure (KMS, Cloud HSM) | Configuring encryption on resources, key management |
| Application layer | None | All application security |
| OS-level security (IaaS) | None (for EC2, GCE, Azure VM) | Patch management, OS hardening, firewall rules |

**The compliance implication:** When an auditor asks for evidence of your security controls, "we run on AWS" is not an answer. You need evidence of how you have configured AWS — your IAM policies, your CloudTrail logs, your S3 bucket encryption settings, your VPC network ACLs. That is what auditors are evaluating.

---

## Control Domain 1: IAM and Least Privilege

### Framework Requirements

| Framework | Requirement |
|---|---|
| SOC 2 (CC6.3) | Restricts access to information assets to authorized users based on job responsibilities |
| ISO 27001 (A.5.15, A.5.18) | Access control policy; access rights provisioned based on need-to-know |
| HIPAA (§164.312(a)(1)) | Assign a unique name and/or number for identifying and tracking user identity |
| PCI DSS v4.0 (Req. 7.2) | Access to system components and data is appropriately defined and assigned |

### AWS Implementation

- **IAM Policies:** Use JSON-based IAM policies with least-privilege permissions. Every role should grant only the actions and resources required for its function. Use the IAM Access Analyzer to identify overly permissive policies.
- **IAM Roles instead of IAM Users:** EC2 instances, Lambda functions, and ECS tasks should use IAM roles (Instance Profiles) — not hardcoded access keys.
- **AWS Organizations SCPs:** Service Control Policies set organization-wide permission guardrails that cannot be overridden by child account administrators.
- **IAM Access Analyzer:** Continuously identifies resources shared externally and unused permissions. Enable in every region.
- **AWS IAM Identity Center (SSO):** Centralizes human access to multiple AWS accounts through a single identity provider integration (Okta, Azure AD, Google Workspace).
- **Privileged Access:** Use AWS Systems Manager Session Manager for privileged access instead of SSH with key pairs — provides auditable session logs without opening inbound ports.

### GCP Implementation

- **IAM Roles:** Use predefined roles or custom roles with the minimum permissions required. Avoid using primitive roles (Owner, Editor, Viewer) at the project level for service accounts.
- **Workload Identity Federation:** Service accounts for workloads running outside GCP (GitHub Actions, on-premise systems) should use Workload Identity Federation instead of service account keys.
- **VPC Service Controls:** Define security perimeters around GCP services to prevent data exfiltration — acts as a logical boundary around BigQuery, Cloud Storage, and other services.
- **Organization Policy Service:** Enforces constraints across all projects in your organization (e.g., restrict public IP addresses on compute instances, require CMEK on all Cloud Storage buckets).
- **IAM Recommender:** Uses machine learning to identify and recommend removal of excess permissions.

### Azure Implementation

- **Azure RBAC:** Assign built-in roles (Reader, Contributor, specific service roles) or custom roles scoped to the minimum required resource level (subscription, resource group, or resource).
- **Azure AD PIM (Privileged Identity Management):** Just-in-time privileged access — administrators request elevation for specific time windows, with approval workflows and full audit logs.
- **Managed Identities:** Azure workloads (VMs, App Service, Azure Functions) should use Managed Identities for accessing Azure services — eliminates credential management.
- **Azure Policy:** Enforces organizational standards across subscriptions (require specific tags, restrict VM SKUs, mandate encryption settings).

**Audit evidence required:** IAM policy documentation, user/role inventory, quarterly access review records, privileged access logs.

---

## Control Domain 2: MFA and SSO Enforcement

### Framework Requirements

| Framework | Requirement |
|---|---|
| SOC 2 (CC6.1) | Identifies and authenticates users prior to granting access; uses multi-factor authentication where appropriate |
| ISO 27001 (A.8.5) | Secure authentication — MFA recommended as primary control |
| HIPAA (§164.312(d)) | Implement procedures to verify that a person or entity seeking access to ePHI is the one claimed |
| PCI DSS v4.0 (Req. 8.4–8.6) | MFA required for all non-console access into the CDE and for all remote access |

MFA is mandatory for all cloud console access. AWS, GCP, and Azure all support native MFA enforcement — but it must be actively configured.

**AWS:** Enforce MFA for the AWS root account (hardware MFA strongly recommended) and all IAM users with console access. Use an SCP to deny access to AWS services if MFA has not been used: `"Condition": {"BoolIfExists": {"aws:MultiFactorAuthPresent": "false"}}`. For human access, IAM Identity Center + Okta/Azure AD with MFA enforced at the IdP level is the preferred architecture.

**GCP:** Enforce MFA through the Google Admin console (Workspace/Cloud Identity) with 2-Step Verification set to mandatory. Support passkeys or hardware security keys for administrator accounts. Organization policy `constraints/iam.disableServiceAccountKeyCreation` prevents creation of downloadable service account keys.

**Azure:** Enforce MFA through Azure AD Conditional Access policies — require MFA for all users accessing Azure portal, Azure CLI, and APIs. Microsoft Authenticator with number matching and additional context enabled. Use Entra ID (Azure AD) Identity Protection to detect sign-in risk and require step-up authentication.

**Audit evidence required:** Screenshots of MFA enforcement policies, export of user MFA enrollment status, Conditional Access policy documentation.

---

## Control Domain 3: Encryption at Rest

### Framework Requirements

| Framework | Requirement |
|---|---|
| SOC 2 (CC6.7) | Restricts the transmission, movement, and removal of information to authorized internal and external users and processes |
| ISO 27001 (A.8.24) | Policy on the use of cryptographic controls |
| HIPAA (§164.312(a)(2)(iv)) | Encryption and decryption — addressable specification |
| PCI DSS v4.0 (Req. 3.5) | Primary account numbers (PANs) are secured wherever stored |

### AWS Implementation

- **S3:** Enable default bucket encryption using SSE-S3 (AES-256) or SSE-KMS (AWS Key Management Service). Apply a bucket policy that denies `s3:PutObject` unless the server-side encryption header is present.
- **RDS / Aurora:** Enable encryption at rest at database creation (cannot be enabled on an existing unencrypted RDS instance). Uses AES-256 via AWS KMS. Automated backups and snapshots are encrypted with the same key.
- **EBS volumes:** Enable default EBS encryption at the account level (EC2 console → Account settings) so all new volumes are encrypted. CMK (Customer Managed Key) in KMS is preferred over the AWS-managed key for regulated workloads.
- **DynamoDB:** Enable encryption at rest (default for new tables; uses AWS-owned keys or KMS CMK).
- **Secrets Manager / Parameter Store (SecureString):** All application secrets, API keys, and database credentials must be stored in AWS Secrets Manager or SSM Parameter Store — never in environment variables, code, or S3 objects.

### GCP Implementation

- **Cloud Storage:** All data is encrypted at rest by default with Google-managed keys. For regulated workloads, use Customer-Managed Encryption Keys (CMEK) via Cloud KMS — required for HIPAA and often required for HITRUST.
- **Cloud SQL / BigQuery:** CMEK available and recommended for workloads handling PHI or cardholder data. BigQuery also supports column-level encryption using `AEAD.ENCRYPT` functions for sensitive columns.
- **Secret Manager:** GCP's equivalent of AWS Secrets Manager. All credentials and API keys stored in Secret Manager, with IAM-controlled access and audit logging of every secret access event.

### Azure Implementation

- **Azure Storage:** Server-side encryption (SSE) is enabled by default using Microsoft-managed keys. Use Customer-Managed Keys (CMK) stored in Azure Key Vault for regulated workloads — required for HIPAA and HITRUST customer-managed key requirements.
- **Azure SQL Database / Azure Database for PostgreSQL:** Transparent Data Encryption (TDE) enabled by default. Use TDE with CMK in Azure Key Vault (customer-managed TDE) for healthcare and financial workloads.
- **Azure Key Vault:** Centralized secret, key, and certificate management. Enable soft-delete and purge protection to prevent accidental or malicious key deletion.

**Audit evidence required:** Encryption configuration documentation (screenshots of AWS console, gcloud commands output, Azure portal), KMS key policy documentation, encryption key rotation records.

---

## Control Domain 4: Encryption in Transit

### Framework Requirements

All four frameworks require encryption of data in transit. PCI DSS v4.0 Requirement 4.2.1 explicitly requires only "strong cryptography" (TLS 1.2 minimum; TLS 1.3 preferred). HIPAA's transmission security standard (§164.312(e)(2)(ii)) requires encryption of ePHI in transit as an addressable specification — in practice, treated as required by auditors.

### Implementation across all clouds

- **Enforce TLS 1.2+ at all load balancer / API gateway layers:** AWS ALB and API Gateway security policies; GCP HTTPS load balancer SSL policy; Azure Application Gateway / Front Door minimum TLS version configuration.
- **Disable older protocols:** Explicitly disable TLS 1.0 and TLS 1.1. On AWS, use a security policy that excludes CBC cipher suites and requires ECDHE key exchange.
- **HTTPS everywhere:** S3 bucket policies should include `"Condition": {"Bool": {"aws:SecureTransport": "false"}}` with Deny action — forces TLS on all S3 API calls. GCP enforces HTTPS on Cloud Storage by default. Azure Storage accounts: set "Secure transfer required" to enabled.
- **Database connections:** Require SSL/TLS on database connections. For RDS, set `rds.force_ssl` parameter to 1. For Cloud SQL, enforce SSL on instance settings. For Azure SQL, enforce TLS connections.
- **Certificate management:** Use AWS Certificate Manager (ACM), GCP Certificate Manager, or Azure-managed certificates for public-facing TLS. Automate renewal. Document certificate inventory and expiration monitoring.

---

## Control Domain 5: Logging and Audit Trails

Full logging implementation is covered in the companion article [What Is a SIEM? When SaaS Companies Need One]. The control reference table for cloud-native logging:

| Log Type | AWS | GCP | Azure | Frameworks |
|---|---|---|---|---|
| API/admin activity | CloudTrail | Cloud Audit Logs (Admin Activity) | Azure Activity Log | All four |
| Data access events | CloudTrail data events | Cloud Audit Logs (Data Access) | Azure Resource Logs | SOC 2, HIPAA, PCI DSS |
| Network traffic | VPC Flow Logs | VPC Flow Logs | NSG Flow Logs | SOC 2, ISO 27001, PCI DSS |
| Identity events | IAM Identity Center logs | Cloud Identity audit logs | Entra ID Sign-in Logs | All four |
| Threat detection | GuardDuty | Security Command Center | Defender for Cloud | SOC 2, ISO 27001 |
| Log retention | S3 + Lifecycle policies | Cloud Storage + Object Lifecycle | Log Analytics Workspace | PCI: 12 months; HIPAA: 6 years |

---

## Control Domain 6: Network Security

### Framework Requirements

| Framework | Requirement |
|---|---|
| SOC 2 (CC6.6) | Restricts logical access to information assets using security groups, network policies |
| ISO 27001 (A.8.20, A.8.21) | Network controls; security of network services |
| PCI DSS v4.0 (Req. 1.2–1.5) | Network access controls; firewall rules documentation; inbound/outbound traffic restrictions |
| HIPAA (§164.312(e)(1)) | Transmission security — protect against unauthorized access to ePHI during transmission |

**AWS:** VPCs with public and private subnet separation. Production databases and application servers in private subnets — no direct internet access. Security groups as stateful firewalls at the instance/ENI level — only the ports and protocols required by the application, from authorized sources. Network ACLs as a stateless perimeter. AWS WAF for public-facing APIs and web applications. No 0.0.0.0/0 inbound rules on production security groups (this is a common finding).

**GCP:** VPC networks with Shared VPC for multi-project organizations. Firewall rules with specific source ranges — deny-all default, allow only necessary traffic. Private Google Access for GCE instances without public IPs. Cloud Armor for WAF and DDoS mitigation. Private Service Connect for private access to GCP services.

**Azure:** Virtual Networks (VNets) with Network Security Groups (NSGs) on subnets and NICs. Azure Firewall or third-party NVA for centralized egress control. Azure Private Link / Private Endpoints for private access to Azure PaaS services (Azure SQL, Azure Storage) without internet exposure. Azure DDoS Protection Standard for production workloads.

**Audit evidence required:** VPC/network architecture diagrams, security group/firewall rule exports, network segmentation documentation, documentation that no production resources have unnecessary public access.

---

> **Mid-article CTA:** Not sure whether your cloud environment would pass a SOC 2, ISO 27001, HIPAA, or PCI DSS audit? QuickTrust's DevOps engineers run a cloud security posture assessment — reviewing your IAM, encryption, logging, and network configuration — and implement the gaps. [Book your cloud security audit at trust.quickintell.com]

---

## Control Domain 7: Backup and Disaster Recovery

### Framework Requirements

| Framework | Requirement |
|---|---|
| SOC 2 (A1.2) | Restores the availability of systems and data if outages occur |
| ISO 27001 (A.8.13) | Information backup — backup copies, tested, stored separately |
| HIPAA (§164.308(a)(7)) | Contingency plan — data backup plan, disaster recovery plan, emergency mode operation plan |
| PCI DSS v4.0 (Req. 12.3.3) | Cryptographic key recovery procedures |

**AWS:** Automated RDS snapshots (retained for 7–35 days), with cross-region snapshot copy for DR. S3 Cross-Region Replication for critical data buckets. AWS Backup for centralized backup policy management across RDS, EBS, EFS, DynamoDB, and Aurora. Backup vault lock (WORM) for immutable backup retention (required for HIPAA).

**GCP:** Cloud SQL automated backups with point-in-time recovery. Cloud Storage dual-region or multi-region buckets for critical data. Google Cloud Backup and DR for centralized backup management. Regular export of Cloud SQL databases to Cloud Storage.

**Azure:** Azure SQL automatic backups (full weekly, differential daily, transaction log every 5–12 minutes). Azure Backup for VMs, Azure SQL, and Azure Files. Geo-redundant storage (GRS) for storage accounts that must survive regional outages. Azure Site Recovery for VM-level disaster recovery with defined RPO/RTO.

**Audit evidence:** Backup configuration documentation, backup test records (restore test results with dates), RTO/RPO documentation, evidence of encrypted backup storage.

---

## Control-to-Framework Mapping Summary Table

| Control | SOC 2 | ISO 27001 | HIPAA | PCI DSS v4.0 |
|---|---|---|---|---|
| IAM least privilege | CC6.3 | A.5.15, A.5.18 | §164.312(a)(1) | Req. 7.2 |
| MFA enforcement | CC6.1 | A.8.5 | §164.312(d) | Req. 8.4–8.6 |
| Encryption at rest | CC6.7 | A.8.24 | §164.312(a)(2)(iv) | Req. 3.5 |
| Encryption in transit | CC6.7 | A.8.24 | §164.312(e)(2)(ii) | Req. 4.2.1 |
| Audit logging | CC7.2 | A.8.15 | §164.312(b) | Req. 10 |
| Log retention | CC7.2 | A.8.15, A.5.33 | §164.312(b) | Req. 10.5 |
| Network segmentation | CC6.6 | A.8.20, A.8.21 | §164.312(e)(1) | Req. 1.2–1.5 |
| Vulnerability scanning | CC7.1 | A.8.8 | — | Req. 6.3, 11.3 |
| Backup / DR | A1.2 | A.8.13 | §164.308(a)(7) | Req. 12.3 |
| Secret management | CC6.7 | A.8.12 | §164.312(a)(2)(iv) | Req. 3.6 |

---

## How QuickTrust's DevOps Engineers Implement Cloud Security Controls

QuickTrust's DevOps engineers implement these controls directly in your cloud environment — not as recommendations in a report, but as configured, tested, and documented controls that your auditors can verify.

A typical cloud security implementation sprint includes:

- IAM policy review and remediation — removing overly permissive policies, converting IAM users to SSO, implementing role-based access with documented policy documents
- MFA enforcement — Conditional Access policies, SCP-enforced MFA requirements, hardware MFA for root/admin accounts
- Encryption configuration — enabling encryption at rest for all data stores, configuring KMS/CMEK, migrating secrets to Secrets Manager/Key Vault
- TLS enforcement — load balancer policy updates, S3 secure transport policies, database SSL requirement enforcement
- Logging pipeline deployment — CloudTrail + CloudWatch + GuardDuty (AWS) or equivalent GCP/Azure stack, with documented retention policies and alerting
- Network architecture review — security group audit, VPC flow log activation, private subnet migration for production resources
- Backup configuration — automated backup policy deployment with cross-region copy, restore testing documentation

Every control implementation is documented for evidence collection — configuration screenshots, Terraform state files, policy documents — mapped to the specific framework requirements they satisfy.

**[Have our DevOps engineers audit and implement your cloud security posture — start at trust.quickintell.com]**

---

## Related Reading

- [HITRUST Certification: The Complete Guide](/blog/pillar-hitrust-complete-guide)
- [SIEM and SOC Explained](/blog/siem-soc-explained)
- [HIPAA Security Rule Guide](/blog/hipaa-security-rule-technical-safeguards)

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Data Security in the Cloud: The Compliance Controls AWS, GCP, and Azure Customers Can't Skip",
  "description": "A technical guide mapping cloud security controls in AWS, GCP, and Azure to SOC 2, ISO 27001, HIPAA, and PCI DSS requirements. Covers IAM, MFA, encryption, logging, network security, and backup — with a control-to-framework mapping table.",
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
  "datePublished": "2026-06-01",
  "dateModified": "2026-02-28"
}
</script>
