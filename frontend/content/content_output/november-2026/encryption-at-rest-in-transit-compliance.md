---
meta_description: "Complete guide to encryption at rest and in transit for SOC 2, ISO 27001, HIPAA, and PCI DSS compliance. Covers AES-256, TLS 1.3, key management, and cloud encryption strategies."
target_keyword: "encryption at rest"
secondary_keywords: "encryption in transit, encryption compliance, data encryption requirements, AES 256 encryption, TLS encryption, encryption key management"
word_count_target: 4000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-19
---

# Encryption at Rest and In Transit: The Complete Compliance Guide for SOC 2, ISO 27001, HIPAA, and PCI DSS

In 2024, a mid-stage SaaS company lost a seven-figure enterprise deal in the final week of procurement review. The reason was not a missing feature, a pricing disagreement, or a competitor swooping in. The buyer's security team discovered that the company's PostgreSQL databases were running without encryption at rest. Customer data -- names, email addresses, API tokens, billing records -- sat on disk in plaintext. The company had TLS on its public endpoints, a SOC 2 Type II report on its website, and a security page that promised "enterprise-grade encryption." But when the buyer's team asked to see the actual encryption configuration, the gap was immediately visible.

That company is not an outlier. Encryption is one of the most universally required controls across every major compliance framework, and yet it remains one of the most frequently misconfigured, incompletely implemented, and poorly documented areas in SaaS security programs. Companies encrypt data in transit but forget data at rest. They encrypt databases but leave backups unencrypted. They enable encryption but never implement key rotation. They use encryption algorithms that were acceptable five years ago but are now deprecated.

The stakes are not theoretical. HIPAA fines for encryption failures have exceeded $1 million in individual settlements. PCI DSS assessors will issue an immediate finding for unencrypted cardholder data. SOC 2 auditors will flag missing encryption as a control deficiency that appears in the final report -- the report your customers read. And ISO 27001 certification auditors will issue a nonconformity if encryption controls do not align with the documented Statement of Applicability.

This guide covers every dimension of encryption that compliance auditors evaluate: encryption at rest, encryption in transit, encryption algorithms, key management, cloud-specific implementations, multi-tenant considerations, and the most common audit findings. It maps each requirement to the specific control references in SOC 2, ISO 27001, HIPAA, and PCI DSS so you know exactly what auditors are looking for and exactly how to satisfy it.

---

## What Is Encryption at Rest?

Encryption at rest refers to the cryptographic protection of data while it is stored on a persistent medium -- a hard disk, a solid-state drive, a database, a file system, an object storage bucket, or a backup tape. When data is "at rest," it is not actively being transmitted across a network or processed in memory. It is sitting on disk, waiting to be read.

The purpose of encryption at rest is to ensure that if the physical or logical storage medium is accessed by an unauthorized party -- through theft, improper decommissioning, unauthorized access to the storage layer, or a misconfiguration that exposes the storage volume -- the data is unintelligible without the corresponding decryption key.

### How encryption at rest works

At a technical level, encryption at rest uses a symmetric encryption algorithm (almost universally AES-256 in compliance contexts) to transform plaintext data into ciphertext before writing it to storage. The process operates at one of several layers:

- **Full-disk encryption (FDE).** The entire storage volume is encrypted. Every sector on disk is encrypted and decrypted transparently as the operating system reads and writes data. BitLocker (Windows), FileVault (macOS), and dm-crypt/LUKS (Linux) are common implementations. In cloud environments, this corresponds to encrypted EBS volumes (AWS), encrypted Persistent Disks (GCP), or Azure Disk Encryption.

- **Database-level encryption (Transparent Data Encryption / TDE).** The database engine encrypts data files, log files, and temporary files at the storage level. The application interacting with the database does not need to change -- encryption and decryption happen transparently within the database engine. PostgreSQL, MySQL, SQL Server, and Oracle all support TDE or equivalent mechanisms.

- **File and object-level encryption.** Individual files or objects are encrypted before being written to the file system or object store. Amazon S3 Server-Side Encryption (SSE), Google Cloud Storage encryption, and Azure Blob Storage encryption operate at this level.

- **Application-level encryption.** The application itself encrypts specific fields or records before sending them to the database or file system. The database stores ciphertext and has no ability to decrypt it. This provides the strongest isolation but requires the application to manage encryption and decryption logic.

- **Backup encryption.** Backup files, snapshots, and archives are encrypted either by the backup tool or by the storage layer receiving the backup. This is frequently overlooked -- companies encrypt production databases but leave nightly backup files unencrypted on an S3 bucket.

### Why encryption at rest matters

Without encryption at rest, anyone with access to the underlying storage can read the data. This includes:

- **Cloud provider employees** with access to the physical storage infrastructure (addressed by provider-side encryption, but not customer-controlled without customer-managed keys)
- **Attackers who compromise the storage layer** through misconfigured permissions, stolen credentials, or lateral movement within the environment
- **Improper media disposal** -- decommissioned disks that are not properly wiped can be recovered
- **Backup exposure** -- a misconfigured S3 bucket containing unencrypted database backups is one of the most common data breach vectors

Encryption at rest is a defense-in-depth control. It does not replace access controls, network segmentation, or monitoring. It adds a layer of protection that ensures data confidentiality even when other controls fail.

---

## What Is Encryption in Transit?

Encryption in transit (also called encryption in motion or data-in-transit encryption) protects data while it is being transmitted across a network -- from a client to a server, from one service to another, from an application to a database, or from a data center to a cloud provider.

The purpose of encryption in transit is to prevent eavesdropping, man-in-the-middle attacks, and data interception during transmission. Without it, anyone who can observe network traffic between two endpoints -- whether through a compromised router, a misconfigured network, a rogue Wi-Fi access point, or an attacker with access to the network path -- can read the data in cleartext.

### How encryption in transit works

Encryption in transit relies on transport-layer cryptographic protocols to establish encrypted channels between communicating endpoints:

- **TLS (Transport Layer Security).** The dominant protocol for encrypting data in transit. TLS 1.3 (the current standard, released in 2018) provides authenticated encryption, forward secrecy, and a streamlined handshake. TLS 1.2 remains acceptable in most compliance contexts but is being actively phased out. TLS 1.0 and 1.1 are deprecated and will generate audit findings.

- **mTLS (Mutual TLS).** Standard TLS authenticates the server to the client. Mutual TLS adds client-side certificate authentication, meaning both parties verify each other's identity. This is increasingly required for internal service-to-service communication in zero-trust architectures and is a strong differentiator during SOC 2 and ISO 27001 audits.

- **IPsec and VPN tunnels.** Encrypt network traffic at the IP layer, typically used for site-to-site connections or secure access to cloud environments. AWS Site-to-Site VPN, GCP Cloud VPN, and Azure VPN Gateway use IPsec to encrypt traffic between on-premises networks and cloud environments.

- **SSH (Secure Shell).** Encrypts remote administrative access to servers and is used for secure file transfer (SFTP/SCP). SSH is the expected standard for any administrative access to production systems.

### The difference between encryption at rest and encryption in transit

The distinction is straightforward but important because compliance frameworks treat them as separate controls:

| Dimension | Encryption at Rest | Encryption in Transit |
|---|---|---|
| **Protects data when** | Stored on disk or persistent media | Moving across a network |
| **Threat model** | Unauthorized physical or logical access to storage | Network eavesdropping, man-in-the-middle attacks |
| **Primary protocol** | AES-256 (symmetric encryption) | TLS 1.2/1.3 (asymmetric + symmetric) |
| **Implementation layer** | Disk, database, file system, application | Network, transport layer |
| **Common failure** | Unencrypted backups, unencrypted database volumes | Internal service-to-service traffic in plaintext |
| **Compliance references** | SOC 2 CC6.1, ISO A.8.24, HIPAA 164.312(a)(2)(iv), PCI DSS 3.5 | SOC 2 CC6.7, ISO A.8.24, HIPAA 164.312(e)(1), PCI DSS 4.2 |

Both are required by every major compliance framework. Implementing one without the other is insufficient. Auditors will evaluate them independently.

---

## Encryption Requirements by Compliance Framework

Every major compliance framework mandates encryption, but they do so with different levels of specificity. Understanding the exact control references allows you to map your encryption implementation directly to audit requirements -- which is what auditors expect to see.

### SOC 2 Trust Services Criteria

SOC 2 addresses encryption through two primary Common Criteria:

**CC6.1 -- Logical and physical access controls.** This criterion requires the organization to implement controls to restrict logical access to information assets. Encryption at rest is a primary mechanism for ensuring that data is protected even if access controls at the infrastructure layer are bypassed. Auditors will look for evidence that sensitive data is encrypted at rest using industry-standard algorithms and that encryption keys are appropriately managed.

**CC6.7 -- Restricts the transmission of data to authorized users.** This criterion specifically addresses encryption in transit. Auditors expect to see TLS enforced on all external-facing endpoints, HSTS headers preventing protocol downgrade attacks, and ideally encryption on internal service-to-service traffic as well.

SOC 2 does not prescribe specific algorithms or key lengths. Instead, it relies on the "industry-accepted" standard. In practice, this means AES-256 for data at rest and TLS 1.2 or higher for data in transit. An auditor who sees AES-128 will not issue a finding, but one who sees DES or 3DES will. An auditor who sees TLS 1.0 will issue a finding.

For a comprehensive overview of SOC 2 criteria, see our [Complete SOC 2 Compliance Guide](/soc-2-compliance).

### ISO 27001:2022 Annex A

ISO 27001 addresses encryption through a dedicated control:

**A.8.24 -- Use of cryptography.** This control requires the organization to define and implement rules for the effective use of cryptography, including cryptographic key management. The Statement of Applicability (SoA) must document which cryptographic controls are implemented, and the implementation must match what the SoA declares.

ISO 27001 is more flexible than other frameworks in that it allows the organization to define its own cryptographic policy -- but that policy must be documented, approved by management, and consistently followed. The standard expects the cryptographic policy to address: types of encryption algorithms and their strength, key management (generation, storage, distribution, retirement, destruction), roles and responsibilities for key management, and compliance with legal and regulatory requirements for cryptography.

Additionally, **A.5.31 -- Legal, statutory, regulatory, and contractual requirements** requires the organization to identify and comply with encryption-related legal requirements, such as export controls on cryptographic technology.

For detailed ISO 27001 implementation guidance, see our [ISO 27001 Certification Guide](/iso-27001-certification).

### HIPAA Security Rule

HIPAA addresses encryption in two specifications within the Security Rule:

**Section 164.312(a)(2)(iv) -- Encryption and decryption (Data at Rest).** This is a technical safeguard requiring covered entities and business associates to "implement a mechanism to encrypt and decrypt electronic protected health information." Critically, HIPAA classifies this as an "addressable" specification -- but "addressable" does not mean "optional." If you choose not to encrypt ePHI at rest, you must document a risk analysis explaining why encryption is not reasonable and appropriate, and implement an equivalent alternative safeguard. In practice, auditors and OCR investigators treat the absence of encryption at rest for ePHI as a significant finding. The cost and availability of AES-256 encryption in modern cloud environments makes it nearly impossible to justify not implementing it.

**Section 164.312(e)(1) -- Transmission security (Data in Transit).** This requires covered entities and business associates to "implement technical security measures to guard against unauthorized access to electronic protected health information that is being transmitted over an electronic communications network." This includes encryption of ePHI in transit using TLS or equivalent protocols. Like the at-rest specification, this is technically "addressable," but any organization transmitting ePHI over the internet without encryption will face enforcement action.

For healthcare-specific compliance guidance, see our [HIPAA Compliance Guide for Healthcare SaaS Companies](/blog/hipaa-compliance-healthcare-saas-guide).

### PCI DSS v4.0

PCI DSS is the most prescriptive of the major frameworks when it comes to encryption:

**Requirement 3.5 -- Protect stored account data.** PCI DSS requires that primary account numbers (PANs) are rendered unreadable anywhere they are stored, using one of several methods: one-way hashes, truncation, index tokens and pads, or strong cryptography with associated key management. If encryption is the chosen method, it must use industry-tested algorithms with a minimum of AES-128 (AES-256 is recommended). Key management procedures must include key generation using strong random number generators, secure key storage, cryptographic key changes for keys that have reached the end of their defined cryptoperiod, and retirement/replacement of keys when their integrity has been weakened.

**Requirement 4.2 -- Protect cardholder data with strong cryptography during transmission over open, public networks.** PCI DSS v4.0 requires TLS 1.2 or higher for any transmission of cardholder data over public networks. TLS 1.0 and 1.1 are explicitly prohibited. The requirement extends to all communication channels where cardholder data is transmitted, including web interfaces, APIs, and messaging channels.

PCI DSS also introduces requirements for **key management** in Requirement 3.6 and 3.7, specifying detailed procedures for key generation, distribution, storage, retirement, and destruction.

For a deep dive into PCI DSS requirements, see our [Complete PCI DSS Compliance Guide](/blog/pillar-pci-dss-complete-guide).

---

## Encryption Algorithms and Standards: What Auditors Accept

Not all encryption is equal. Auditors evaluate not just whether encryption is present but which algorithms, key lengths, and protocols are in use. Using a deprecated algorithm is, from an audit perspective, nearly as bad as not encrypting at all.

### Accepted algorithms for data at rest

| Algorithm | Key Length | Status | Auditor Acceptance |
|---|---|---|---|
| **AES-256** | 256-bit | Current standard | Universally accepted, preferred |
| **AES-128** | 128-bit | Current standard | Accepted by all frameworks; PCI DSS recommends AES-256 |
| **AES-192** | 192-bit | Current standard | Accepted but rarely used in practice |
| **ChaCha20-Poly1305** | 256-bit | Current standard | Accepted; common in mobile and TLS contexts |
| **3DES (Triple DES)** | 168-bit effective | **Deprecated** | Will generate findings; NIST deprecated in 2023 |
| **DES** | 56-bit | **Broken** | Immediate finding; not acceptable under any framework |
| **Blowfish** | Variable | **Legacy** | Not recommended; will likely generate auditor questions |
| **RC4** | Variable | **Broken** | Immediate finding; prohibited by PCI DSS and NIST |

**The safe choice:** AES-256 for all data at rest. There is no compliance or performance reason to choose anything else for new implementations. AES-256 is hardware-accelerated on virtually all modern processors (via AES-NI instructions), making the performance overhead negligible.

### Accepted algorithms for data in transit

| Protocol / Algorithm | Status | Auditor Acceptance |
|---|---|---|
| **TLS 1.3** | Current standard (RFC 8446) | Universally accepted, preferred |
| **TLS 1.2** | Current standard | Accepted by all frameworks; actively being phased out |
| **TLS 1.1** | **Deprecated** | Will generate findings; prohibited by PCI DSS v4.0 |
| **TLS 1.0** | **Deprecated** | Immediate finding under all frameworks |
| **SSL 3.0** | **Broken** | Critical finding; must be immediately disabled |
| **SSL 2.0** | **Broken** | Critical finding; should not exist anywhere in production |

For TLS cipher suites, auditors expect to see only suites that provide forward secrecy (ECDHE or DHE key exchange), authenticated encryption (GCM or ChaCha20-Poly1305), and SHA-256 or higher for message authentication. Cipher suites using CBC mode, MD5, SHA-1, or RSA key exchange (without ECDHE/DHE) are increasingly flagged as weak.

### Hashing algorithms

While not encryption in the traditional sense, hashing algorithms appear in compliance contexts for password storage, integrity verification, and digital signatures:

| Algorithm | Status | Use Case |
|---|---|---|
| **SHA-256, SHA-384, SHA-512** | Current standard | Integrity verification, digital signatures |
| **SHA-3 (Keccak)** | Current standard | Alternative to SHA-2 family; growing adoption |
| **bcrypt, scrypt, Argon2** | Current standard | Password hashing (preferred over raw SHA) |
| **SHA-1** | **Deprecated** | Will generate findings for new implementations; prohibited for digital signatures |
| **MD5** | **Broken** | Immediate finding; not acceptable for any security purpose |

### RSA and elliptic curve key lengths

For asymmetric encryption and digital signatures:

- **RSA-2048** is the minimum accepted key length. RSA-4096 is recommended for long-lived keys.
- **ECDSA with P-256 (secp256r1)** or **P-384** curves is accepted and preferred for TLS certificates and digital signatures due to shorter key lengths with equivalent security.
- **RSA-1024** is deprecated and will generate an immediate finding under all frameworks.
- **Ed25519** is accepted and increasingly preferred for SSH keys.

---

## Encryption at Rest: Implementation Guide

Moving from requirements to implementation, this section covers the practical steps for encrypting data at rest across the most common storage layers in a SaaS environment.

### Database encryption

**Relational databases (PostgreSQL, MySQL, SQL Server):**

Transparent Data Encryption (TDE) should be enabled for all production databases. In cloud-managed database services, this is often enabled by default but must be verified:

- **AWS RDS:** Encryption at rest is available using AES-256 via AWS KMS. It must be enabled at instance creation; you cannot encrypt an existing unencrypted RDS instance in place. For existing unencrypted instances, you must create an encrypted snapshot and restore from it.
- **GCP Cloud SQL:** Encryption at rest is enabled by default using Google-managed keys. To use customer-managed encryption keys (CMEK), configure Cloud KMS integration.
- **Azure SQL Database:** Transparent Data Encryption is enabled by default for all new databases using service-managed keys. Customer-managed keys can be configured via Azure Key Vault.

**NoSQL databases (MongoDB, DynamoDB, Firestore):**

- **MongoDB Atlas:** Encryption at rest is enabled by default using the WiredTiger storage engine's native encryption. Customer-managed keys are supported via AWS KMS, GCP KMS, or Azure Key Vault integration.
- **AWS DynamoDB:** Encryption at rest is enabled by default using AWS-owned keys. Customer-managed keys (via KMS) provide additional control and audit visibility.
- **GCP Firestore:** Encryption at rest is enabled by default with Google-managed keys. CMEK is available for additional control.

**Column-level and field-level encryption:**

For highly sensitive fields (Social Security numbers, financial account numbers, health identifiers), consider application-level encryption on individual fields. This ensures that even database administrators and users with SELECT access cannot read the plaintext values. Client-side field-level encryption is supported natively in MongoDB (Client-Side Field Level Encryption / Queryable Encryption) and can be implemented application-side for relational databases using libraries like AWS Encryption SDK or Google Tink.

### File and object storage encryption

- **AWS S3:** Enable default encryption on every bucket. Use SSE-S3 (Amazon-managed keys) as a baseline; use SSE-KMS (customer-managed KMS keys) for data subject to compliance requirements. Enable the `s3-bucket-server-side-encryption-enabled` AWS Config rule to detect non-compliant buckets.
- **GCP Cloud Storage:** All objects are encrypted by default with Google-managed keys. Use CMEK for compliance-sensitive data.
- **Azure Blob Storage:** Storage Service Encryption is enabled by default. Use customer-managed keys via Azure Key Vault for additional control.

### Full-disk encryption

- **Server endpoints:** Enable full-disk encryption on all servers, including development and staging environments. Use LUKS (Linux), BitLocker (Windows), or cloud-native volume encryption.
- **Employee endpoints:** Enforce FileVault (macOS), BitLocker (Windows), or LUKS (Linux) on all company-issued devices. Use MDM (Mobile Device Management) to verify encryption status and enforce policies. Auditors will ask for evidence that endpoint encryption is enforced across the fleet.
- **Mobile devices:** Enforce device encryption through MDM policies. Both iOS and Android encrypt device storage by default when a passcode is set, but MDM policies should verify and enforce this.

### Backup encryption

This is where many companies fail audits. Production data is encrypted, but backups are not:

- Ensure all database backups, snapshots, and archives are encrypted. If using native cloud backup services, verify that encryption is inherited from the source or explicitly configured.
- Verify that backup files stored in object storage (S3, GCS, Azure Blob) are encrypted. A nightly database dump written to an S3 bucket without encryption invalidates the encryption at rest control for that data.
- Test backup restoration from encrypted backups to verify that the encryption keys are accessible and the process works.

---

## Encryption in Transit: Implementation Guide

### TLS 1.3 deployment

TLS 1.3 should be the target protocol for all new deployments and the migration target for existing TLS 1.2 deployments. TLS 1.3 eliminates insecure cipher suites, reduces the handshake to one round trip (improving performance), and mandates forward secrecy.

**Web-facing endpoints:**

- Configure load balancers and reverse proxies (NGINX, AWS ALB, Cloudflare, GCP HTTPS Load Balancer) to support TLS 1.3 as the preferred protocol with TLS 1.2 as a fallback.
- Disable TLS 1.0 and 1.1 explicitly. Do not assume they are disabled by default.
- Use only cipher suites with forward secrecy: `TLS_AES_256_GCM_SHA384`, `TLS_AES_128_GCM_SHA256`, and `TLS_CHACHA20_POLY1305_SHA256` for TLS 1.3. For TLS 1.2, restrict to ECDHE-based cipher suites.

**API endpoints:**

- Enforce minimum TLS 1.2 on all API endpoints. Document the policy and communicate it to API consumers with a deprecation timeline for older protocols.
- Consider implementing certificate pinning for mobile applications communicating with your API, though this adds operational complexity for certificate rotation.

### Certificate management

Certificate mismanagement is one of the most common causes of encryption-related outages and audit findings:

- Use a certificate authority (CA) that supports automated issuance and renewal. Let's Encrypt provides free, automated certificates with 90-day validity. AWS Certificate Manager (ACM), GCP Certificate Manager, and Azure App Service Certificates provide managed alternatives.
- **Automate renewal.** Manual certificate renewal processes are a guaranteed source of outages and audit findings. Implement automated renewal with monitoring for certificates approaching expiration.
- **Monitor certificate expiration.** Use tools that alert on certificates within 30, 14, and 7 days of expiration. An expired certificate causes a service outage and demonstrates a control failure to auditors.
- **Use certificates with a maximum 1-year validity** for public-facing endpoints. The CA/Browser Forum reduced the maximum validity from two years to one year (398 days) in 2020, and further reductions are expected.

### HSTS (HTTP Strict Transport Security)

HSTS tells browsers to only communicate with your site over HTTPS, preventing protocol downgrade attacks and cookie hijacking:

- Add the `Strict-Transport-Security` header with a minimum `max-age` of `31536000` (one year).
- Include the `includeSubDomains` directive to protect all subdomains.
- Once you have verified correct behavior, consider submitting your domain to the HSTS preload list at hstspreload.org, which hardcodes the HSTS policy into browsers.
- Auditors will check for HSTS headers during SOC 2 and PCI DSS assessments. Missing HSTS on a public-facing application is a low-hanging finding.

### Internal service-to-service encryption

This is the area where most SaaS companies have gaps. External traffic is encrypted, but internal microservice communication often runs over plaintext HTTP:

- **Service mesh with mTLS:** Tools like Istio, Linkerd, and Consul Connect provide automatic mTLS between services. This is the gold standard for internal encryption and is increasingly expected by auditors for companies with microservice architectures.
- **Internal TLS:** If a full service mesh is not practical, configure TLS on internal services using internal CA-issued certificates. HashiCorp Vault, AWS Private CA, or step-ca can act as internal certificate authorities.
- **Database connections:** Ensure that connections from application servers to databases are encrypted. This is often overlooked -- the application connects to the database over the internal network without TLS, meaning database credentials and query results traverse the network in plaintext. All major database engines support TLS for client connections. Enable it and enforce it (`sslmode=require` or `sslmode=verify-full` for PostgreSQL; `--require_secure_transport=ON` for MySQL).

---

## Encryption Key Management: The Most Audited Control

If encryption is the lock, key management is the key. And auditors spend more time on key management than on encryption itself. An encrypted database with poorly managed keys provides a false sense of security -- if the key is stored alongside the data, hardcoded in application code, or accessible to every engineer, the encryption is effectively meaningless.

### Key management fundamentals

**Separation of data and keys.** The encryption key must never be stored in the same system as the data it encrypts. A database encryption key stored in a table in the same database, or an encryption key committed to a Git repository alongside application code, is an immediate audit finding.

**Envelope encryption.** The standard pattern in cloud environments: data is encrypted with a data encryption key (DEK), and the DEK itself is encrypted with a key encryption key (KEK) managed by a key management service. This allows efficient encryption of large data volumes while keeping the master key centrally managed and auditable. AWS KMS, GCP Cloud KMS, and Azure Key Vault all use this pattern.

**Key rotation.** Encryption keys must be rotated on a defined schedule. PCI DSS requires key rotation at the end of the defined cryptoperiod (typically annual). ISO 27001 requires documented key management procedures that include rotation. SOC 2 auditors expect documented key rotation policies and evidence that rotation has occurred.

- AWS KMS supports automatic annual rotation of customer master keys (CMKs).
- GCP Cloud KMS supports configurable automatic rotation schedules.
- Azure Key Vault supports key rotation policies with configurable intervals.

Manual rotation must be documented with evidence of when it occurred, who initiated it, and confirmation that old keys were retired appropriately.

### Key Management Services (KMS)

Cloud KMS services are the standard solution for most SaaS companies:

- **AWS KMS:** Centralized key management service integrated with virtually all AWS services. Supports customer-managed keys (CMKs), automatic key rotation, key policies, and CloudTrail audit logging for every key usage event.
- **GCP Cloud KMS:** Equivalent service for GCP. Supports CMEK integration with Cloud SQL, Cloud Storage, BigQuery, and other services. Provides IAM-based access control and Cloud Audit Logs integration.
- **Azure Key Vault:** Microsoft's key management service. Supports keys, secrets, and certificates. Integrates with Azure SQL, Blob Storage, and other services for customer-managed key encryption.

### Hardware Security Modules (HSM)

For organizations with the most stringent requirements (financial services, government, healthcare organizations handling large volumes of PHI), cloud-based or dedicated HSMs provide FIPS 140-2 Level 3 (or Level 4) validated hardware for key generation and storage:

- **AWS CloudHSM:** Dedicated HSM instances in the AWS cloud. FIPS 140-2 Level 3 validated. Required by some regulatory environments and useful for PCI DSS compliance where assessors require dedicated key storage.
- **GCP Cloud HSM:** FIPS 140-2 Level 3 validated HSM integrated with Cloud KMS. Keys can be created and used exclusively within the HSM boundary.
- **Azure Dedicated HSM:** FIPS 140-2 Level 3 validated Thales Luna HSMs dedicated to a single customer.

### Separation of duties

Auditors will verify that the person (or service account) that manages encryption keys is not the same person who accesses the encrypted data. This separation prevents a single compromised account from both accessing encrypted data and decrypting it.

Implement this through IAM policies: grant key management permissions (create, rotate, delete keys) to a security or infrastructure team, and grant key usage permissions (encrypt, decrypt) to application service accounts that need to read and write data. Use distinct IAM roles and enforce the principle of least privilege.

### BYOK vs. provider-managed keys

| Approach | Description | Compliance Implication |
|---|---|---|
| **Provider-managed keys** | The cloud provider generates and manages encryption keys entirely. | Sufficient for SOC 2 and ISO 27001 baseline. HIPAA and PCI DSS assessors may require additional assurance. |
| **Customer-managed keys (CMK)** | The customer creates keys in the cloud provider's KMS and controls access policies. | Preferred for all compliance frameworks. Provides audit trail for key usage. |
| **Bring Your Own Key (BYOK)** | The customer generates keys outside the cloud environment and imports them into the provider's KMS. | Required by some financial regulators and government contracts. Provides maximum control but adds operational complexity. |
| **Hold Your Own Key (HYOK)** | The customer holds the key externally; the cloud provider never possesses the plaintext key. | Maximum control and assurance. Limits some cloud service functionality. |

For most SaaS companies pursuing SOC 2, ISO 27001, HIPAA, or PCI DSS, **customer-managed keys (CMK)** in the cloud provider's KMS provide the optimal balance of security, auditability, and operational simplicity. BYOK adds operational overhead that is rarely justified unless a specific regulatory or contractual requirement demands it.

---

## Cloud Encryption: AWS, GCP, and Azure Approaches

Each major cloud provider has a slightly different approach to encryption. Understanding the provider-specific implementations is critical for documentation and evidence collection during audits.

For a broader overview of cloud security controls, see our [Cloud Security Compliance Guide for AWS, GCP, and Azure](/blog/cloud-security-compliance-aws-gcp-azure).

### AWS encryption architecture

**Server-Side Encryption (SSE) options for S3:**

- **SSE-S3:** Amazon manages the encryption keys entirely. AES-256 encryption. Zero configuration required beyond enabling it. Auditors accept this for SOC 2 but may prefer CMK for HIPAA and PCI DSS.
- **SSE-KMS:** Encryption using a customer-managed key in AWS KMS. Provides an audit trail (CloudTrail logs every Encrypt, Decrypt, and GenerateDataKey API call), key rotation control, and granular access policies. This is the recommended approach for compliance-sensitive data.
- **SSE-C:** Customer provides the encryption key with each request. AWS performs encryption/decryption but does not store the key. Useful for specific use cases but adds significant operational complexity.

**Encryption for other AWS services:**

- **RDS:** AES-256 encryption using KMS keys. Must be enabled at instance creation.
- **EBS:** AES-256 encryption using KMS keys. Can be enforced account-wide using the EBS encryption by default setting.
- **DynamoDB:** Encryption at rest enabled by default. Options: AWS-owned key, AWS-managed key, or customer-managed key.
- **Redshift:** AES-256 encryption at rest using KMS or CloudHSM.
- **SQS / SNS:** Server-side encryption available using KMS keys.

### GCP encryption architecture

GCP encrypts all data at rest by default using Google-managed keys -- no configuration required. This provides a baseline that exceeds most other platforms. For compliance purposes, organizations layer CMEK on top:

- **Default encryption:** All data at rest is encrypted with AES-256 using Google-managed keys. This is transparent and automatic.
- **CMEK (Customer-Managed Encryption Keys):** Keys created and managed in Cloud KMS, used to encrypt data in Cloud Storage, Cloud SQL, BigQuery, Compute Engine, and other services. Provides customer control over key lifecycle and audit visibility.
- **CSEK (Customer-Supplied Encryption Keys):** The customer generates and provides keys for Compute Engine disk encryption and Cloud Storage objects. GCP does not store the keys. Equivalent to SSE-C in AWS.

### Azure encryption architecture

**Azure Storage Service Encryption (SSE):**

- Enabled by default for all Azure Storage accounts using Microsoft-managed keys and AES-256.
- Customer-managed keys via Azure Key Vault provide additional control and audit visibility.
- Double encryption (infrastructure encryption) adds a second layer of encryption at the infrastructure level for defense in depth.

**Azure Disk Encryption:**

- Uses BitLocker (Windows VMs) or dm-crypt (Linux VMs) to encrypt OS and data disks.
- Integrated with Azure Key Vault for key management.
- Azure Disk Encryption should be enabled on all virtual machines, not just production.

**Azure SQL Transparent Data Encryption (TDE):**

- Enabled by default for all Azure SQL databases and Azure Synapse Analytics.
- Service-managed keys by default; customer-managed keys via Key Vault for compliance requirements.

### Cross-cloud encryption comparison

| Feature | AWS | GCP | Azure |
|---|---|---|---|
| Default encryption at rest | Must be enabled per service (except DynamoDB, S3 default encryption) | Enabled by default for all services | Enabled by default for storage and SQL |
| KMS service | AWS KMS | Cloud KMS | Azure Key Vault |
| HSM option | CloudHSM (FIPS 140-2 L3) | Cloud HSM (FIPS 140-2 L3) | Dedicated HSM (FIPS 140-2 L3) |
| Auto key rotation | Annual for CMKs | Configurable schedule | Configurable via Key Vault |
| Envelope encryption | Yes (native) | Yes (native) | Yes (native) |
| Audit logging | CloudTrail | Cloud Audit Logs | Azure Monitor / Activity Log |

---

## Encryption for SaaS Companies: Multi-Tenant Considerations

SaaS companies face encryption challenges that go beyond single-organization deployments. When multiple customers share infrastructure, the encryption strategy must account for tenant isolation, data segregation, and customer-specific key management requirements.

### Tenant-level encryption keys

The strongest approach to multi-tenant encryption is to assign a unique data encryption key (DEK) to each tenant. This ensures that even if one tenant's key is compromised, other tenants' data remains protected:

- **Implementation pattern:** Each tenant gets a unique DEK stored in KMS. The DEK is used to encrypt that tenant's data (database rows, file uploads, API payloads). The DEK itself is encrypted with a master KEK using envelope encryption.
- **Tenant key isolation:** Use KMS key policies or IAM conditions to ensure that a service processing Tenant A's data cannot access Tenant B's encryption key.
- **Performance considerations:** With envelope encryption, the DEK is cached in memory after initial decryption. The performance overhead of per-tenant keys is minimal because KMS is only called when the DEK is first loaded, not for every encrypt/decrypt operation.

For enterprise customers, per-tenant encryption keys are increasingly a contractual requirement. Enterprise buyers want assurance that their data can be cryptographically destroyed by deleting their encryption key when they offboard, without relying solely on database deletion.

### Field-level encryption

For the most sensitive data elements in a multi-tenant SaaS application, field-level encryption provides granular protection:

- **What to encrypt at the field level:** Social Security numbers, financial account numbers, health identifiers, API secrets, authentication tokens, and any data element that would cause significant harm if exposed.
- **Implementation:** Encrypt fields in the application layer before writing to the database. The database stores ciphertext. Decryption occurs in the application layer when the data is needed. Libraries like AWS Encryption SDK, Google Tink, or libsodium provide well-audited implementations.
- **Search considerations:** Encrypted fields cannot be searched or indexed directly. Solutions include blind indexing (storing a keyed hash of the plaintext alongside the ciphertext for exact-match queries), deterministic encryption (same plaintext produces same ciphertext, enabling equality searches but leaking frequency information), or searchable encryption schemes. Each approach has trade-offs between functionality and security.

### Customer-managed keys for enterprise tenants

Some enterprise customers require the ability to manage their own encryption keys (CMK or BYOK) for their data within your SaaS platform:

- **Architecture:** Integrate with the customer's KMS (their AWS KMS, GCP Cloud KMS, or Azure Key Vault). The customer's key encrypts the DEK for their data. They retain the ability to revoke the key, which renders their data inaccessible.
- **Operational implications:** If the customer revokes their key, your application must handle decryption failures gracefully. Implement circuit breakers and clear error messaging.
- **Compliance value:** Offering customer-managed keys is a significant differentiator in enterprise sales and security reviews. It demonstrates a mature encryption architecture and gives customers confidence that they retain cryptographic control over their data.

---

## Common Encryption Audit Findings and How to Fix Them

After reviewing hundreds of audit reports and security assessments, these are the encryption-related findings that appear most frequently. If you address these proactively, you eliminate the majority of encryption-related audit risk.

### 1. Unencrypted database backups

**Finding:** Production databases are encrypted at rest, but automated backups (database dumps, snapshots stored in object storage) are not encrypted.

**Fix:** Verify that all backup destinations have encryption enabled. For S3 bucket targets, enable default encryption with SSE-KMS. For RDS automated backups, encryption is inherited from the source instance -- but only if the source instance was encrypted at creation. For manual exports, ensure the export process includes encryption.

### 2. TLS 1.0 or 1.1 still enabled

**Finding:** Legacy TLS protocol versions are still accepted on public-facing endpoints.

**Fix:** Disable TLS 1.0 and 1.1 on all load balancers, reverse proxies, and CDN configurations. Update the minimum protocol version to TLS 1.2. Test with tools like SSL Labs (ssllabs.com/ssltest) to verify that only TLS 1.2 and 1.3 are accepted. Monitor for client compatibility issues, but in 2026, no modern browser or API client requires TLS 1.0 or 1.1.

### 3. Missing HSTS headers

**Finding:** The application does not send HSTS headers, allowing potential protocol downgrade attacks.

**Fix:** Add the `Strict-Transport-Security: max-age=31536000; includeSubDomains` header to all HTTPS responses. Test thoroughly before adding the `preload` directive, as HSTS preload is difficult to undo.

### 4. Encryption keys stored in application code or configuration files

**Finding:** Encryption keys, database passwords, or API secrets are found in source code, environment files committed to version control, or configuration files on servers.

**Fix:** Move all secrets to a dedicated secrets management service: AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, or HashiCorp Vault. Remove secrets from code repositories (and rotate them, since they have been exposed in version history). Implement pre-commit hooks (such as git-secrets or truffleHog) to prevent future secret commits.

### 5. No documented key rotation policy or evidence of rotation

**Finding:** Encryption keys have not been rotated since initial creation, or there is no documented policy defining rotation frequency.

**Fix:** Document a key rotation policy specifying rotation frequency (annual is the standard for most frameworks; PCI DSS requires rotation at the end of the cryptoperiod). Enable automatic rotation in KMS where available. For keys that require manual rotation, create a calendar-based process with documented evidence (screenshots, audit logs, change tickets) that rotation occurred.

### 6. Internal service-to-service traffic unencrypted

**Finding:** Microservices communicate over plaintext HTTP within the internal network.

**Fix:** Implement TLS on internal services. A service mesh (Istio, Linkerd) is the most comprehensive solution. As an interim step, enable TLS on internal load balancers and configure services to communicate over HTTPS. Prioritize connections that carry sensitive data (database connections, authentication services, services that handle PII).

### 7. Weak cipher suites accepted

**Finding:** The server accepts cipher suites using CBC mode, SHA-1, or RSA key exchange without forward secrecy.

**Fix:** Restrict cipher suites to those providing forward secrecy and authenticated encryption. For TLS 1.3, only AEAD cipher suites are available (this is enforced by the protocol). For TLS 1.2, configure the server to prefer ECDHE-based cipher suites with GCM mode and disable CBC-mode and SHA-1-based suites.

### 8. Development and staging environments unencrypted

**Finding:** Production encryption controls are not replicated in development and staging environments, which may contain copies of production data.

**Fix:** Apply the same encryption controls to all environments that handle customer data or production data copies. If development environments use anonymized data, document the anonymization process and confirm that no real customer data exists in unencrypted environments.

### 9. No evidence that encryption is actually enabled

**Finding:** The security policy states that encryption is used, but there is no evidence (screenshots, configuration exports, audit logs) demonstrating that encryption is active on specific resources.

**Fix:** Generate and store evidence of encryption configuration: screenshots of encryption settings in cloud consoles, AWS Config rule evaluation results, `openssl s_client` test outputs showing TLS configuration, database configuration parameters showing TDE status. QuickTrust automates evidence collection for encryption controls across cloud environments, mapping each piece of evidence to the specific framework control it satisfies.

### 10. Missing encryption on data in transit for internal database connections

**Finding:** Application servers connect to databases over the internal network without TLS, transmitting queries and results (including sensitive data) in plaintext.

**Fix:** Enable TLS on database listeners and configure application connection strings to require TLS. For PostgreSQL, set `sslmode=verify-full` in connection strings. For MySQL, use `--require_secure_transport=ON` on the server and `ssl-mode=REQUIRED` in client connections.

---

## Encryption Checklist for Compliance

Use this checklist as a quick reference to verify that your encryption implementation covers all areas that auditors evaluate. Each item maps to requirements across SOC 2, ISO 27001, HIPAA, and PCI DSS.

### Encryption at rest

- [ ] All production databases are encrypted at rest using AES-256 (or AES-128 minimum)
- [ ] All object storage buckets (S3, GCS, Azure Blob) have default encryption enabled
- [ ] All block storage volumes (EBS, Persistent Disk, Azure Disk) are encrypted
- [ ] All database backups and snapshots are encrypted
- [ ] All data warehouse and analytics stores are encrypted at rest
- [ ] Full-disk encryption is enforced on all employee endpoints (laptops, workstations)
- [ ] Mobile devices used for work have device encryption enabled and verified via MDM
- [ ] Development and staging environments with customer data copies are encrypted
- [ ] Field-level encryption is applied to the most sensitive data elements (SSNs, PANs, health identifiers)

### Encryption in transit

- [ ] TLS 1.2 is the minimum protocol version on all external-facing endpoints
- [ ] TLS 1.0 and 1.1 are explicitly disabled
- [ ] HSTS headers are configured with a minimum max-age of one year
- [ ] Internal service-to-service traffic is encrypted (TLS or mTLS)
- [ ] Database connections from application servers use TLS
- [ ] API endpoints enforce minimum TLS 1.2
- [ ] VPN or encrypted tunnels are used for any site-to-site connectivity
- [ ] SSH (not Telnet) is used for all administrative remote access
- [ ] Certificate renewal is automated with monitoring for expiring certificates

### Key management

- [ ] Encryption keys are managed through a dedicated KMS (not stored in code or config files)
- [ ] Envelope encryption is used (DEKs encrypted by KEKs)
- [ ] Key rotation policy is documented with defined rotation frequency
- [ ] Automatic key rotation is enabled where available
- [ ] Separation of duties is enforced between key administrators and data users
- [ ] Key access is logged and auditable (CloudTrail, Cloud Audit Logs, Azure Monitor)
- [ ] Key deletion requires multi-party approval or a waiting period
- [ ] Retired keys are properly decommissioned and documented

### Documentation and evidence

- [ ] Encryption policy is documented, approved by management, and reviewed at least annually
- [ ] Encryption configuration evidence is collected and stored for audit readiness
- [ ] Encryption implementation is mapped to specific framework controls (CC6.1, CC6.7, A.8.24, 164.312, Req 3.5/4.2)
- [ ] Exceptions to encryption requirements are documented with risk assessments and compensating controls

---

## Frequently Asked Questions

### Is encryption at rest required by HIPAA?

Encryption at rest is classified as an "addressable" specification under HIPAA Section 164.312(a)(2)(iv). However, "addressable" does not mean "optional." If you choose not to implement encryption at rest for ePHI, you must document a risk analysis demonstrating why encryption is not reasonable and appropriate, and implement an equivalent alternative safeguard. Given the availability and low cost of AES-256 encryption in modern cloud environments, it is virtually impossible to justify not encrypting ePHI at rest. OCR enforcement actions have repeatedly cited failure to encrypt ePHI as a basis for significant fines.

### What is the difference between AES-128 and AES-256?

AES-128 and AES-256 use the same core algorithm (Rijndael) with different key lengths. AES-128 uses a 128-bit key (2^128 possible keys), and AES-256 uses a 256-bit key (2^256 possible keys). Both are considered secure and are accepted by all major compliance frameworks. AES-256 provides a larger security margin against future cryptanalytic advances and brute-force attacks and is the recommended choice for compliance purposes. The performance difference between AES-128 and AES-256 is negligible on modern hardware with AES-NI instruction support.

### Does TLS 1.2 still pass compliance audits?

Yes, TLS 1.2 is accepted by all major compliance frameworks in 2026. However, TLS 1.3 is the current standard and is preferred by auditors. TLS 1.2 is on a deprecation trajectory -- when the industry transitions, organizations still on TLS 1.2 will need to upgrade. For new implementations, configure TLS 1.3 as the primary protocol with TLS 1.2 as a fallback. Disable TLS 1.0 and 1.1 immediately; these are explicitly prohibited by PCI DSS v4.0 and will generate findings under all frameworks.

### How often should encryption keys be rotated?

Key rotation frequency depends on the compliance framework and the type of key. PCI DSS requires rotation at the end of the defined cryptoperiod, which is typically annual. ISO 27001 requires a documented key management procedure that includes rotation schedules. SOC 2 expects documented rotation policies with evidence of execution. The industry standard is annual rotation for master keys and data encryption keys. TLS certificates should be renewed before expiration (typically annually for public certificates). SSH keys should be rotated at least annually. AWS KMS supports automatic annual rotation, making compliance straightforward.

### What is envelope encryption and why does it matter?

Envelope encryption is a two-tier encryption pattern where data is encrypted with a data encryption key (DEK), and the DEK itself is encrypted with a key encryption key (KEK) managed by a KMS. This pattern matters for three reasons. First, it is efficient: the DEK (a small symmetric key) is the only thing encrypted by the KMS, while the potentially large data payload is encrypted locally. Second, it enables key rotation without re-encrypting all data: rotating the KEK only requires re-encrypting the DEK, not the underlying data. Third, it provides a centralized audit trail: all key operations are logged in the KMS. AWS KMS, GCP Cloud KMS, and Azure Key Vault all implement envelope encryption natively.

### Can we use the cloud provider's default encryption for compliance?

Cloud provider default encryption (such as AWS SSE-S3 or GCP's default encryption) satisfies the baseline encryption at rest requirement for SOC 2 and ISO 27001. However, for HIPAA and PCI DSS, auditors typically prefer customer-managed keys (CMK) because they provide a customer-controlled audit trail of key usage and prevent the cloud provider from having sole control over decryption. Using customer-managed keys through the cloud provider's KMS (AWS KMS CMK, GCP CMEK, Azure Key Vault) is the recommended approach for all compliance frameworks. It adds minimal operational overhead while providing the audit visibility that assessors expect.

### What encryption do we need for a multi-tenant SaaS application?

At minimum, a multi-tenant SaaS application needs: encryption at rest for all databases and storage (AES-256), encryption in transit for all external and internal traffic (TLS 1.2+), and centralized key management via KMS. For enhanced security and to meet enterprise customer expectations, implement per-tenant encryption keys (each customer's data encrypted with a unique DEK), field-level encryption for the most sensitive data elements, and the ability for enterprise customers to manage their own keys (BYOK). Per-tenant encryption keys also enable cryptographic data deletion: when a customer churns, deleting their encryption key renders their data permanently unrecoverable.

### How do we prove encryption is enabled during an audit?

Auditors need evidence, not assertions. Collect and maintain the following: screenshots or configuration exports from cloud consoles showing encryption enabled on databases, storage buckets, and volumes; AWS Config rule evaluation results (or equivalent) showing compliance with encryption requirements; SSL Labs test results showing TLS configuration on public endpoints; `openssl s_client` output verifying TLS version and cipher suite on specific endpoints; KMS audit logs showing key creation, rotation, and usage events; documented encryption policy with management approval and review date; and evidence of key rotation (KMS logs, change tickets, or rotation records). QuickTrust automates evidence collection for encryption controls and maps each artifact to the specific control requirement it satisfies across SOC 2, ISO 27001, HIPAA, and PCI DSS.

---

## Take Control of Your Encryption Compliance

Encryption is not a single checkbox -- it is a system of controls spanning data at rest, data in transit, key management, cloud configuration, and continuous evidence collection. Getting it right means your data is protected even when other controls fail. Getting it wrong means audit findings, customer trust erosion, and regulatory exposure.

The gap between "we use encryption" and "we have a documented, auditable encryption implementation that satisfies SOC 2, ISO 27001, HIPAA, and PCI DSS" is where most companies struggle. It is not the encryption itself that is hard. Modern cloud platforms make enabling encryption straightforward. The hard part is ensuring every storage layer is covered, every key is managed properly, every internal connection is encrypted, every backup is protected, and the evidence is collected and organized for auditors.

That is exactly what QuickTrust automates. Our platform continuously monitors your encryption configuration across AWS, GCP, and Azure, maps every control to the specific framework requirements you are pursuing, collects audit evidence automatically, and alerts you when encryption coverage gaps appear -- before your auditor finds them.

**[Start your free QuickTrust assessment](https://quicktrustapp.com)** and see exactly where your encryption implementation stands against SOC 2, ISO 27001, HIPAA, and PCI DSS requirements. Most companies discover gaps they did not know they had.

---

### Related resources

- [The Complete SOC 2 Compliance Guide for SaaS Startups](/soc-2-compliance)
- [ISO 27001 Certification: The Complete Implementation Guide](/iso-27001-certification)
- [HIPAA Compliance for Healthcare SaaS Companies](/blog/hipaa-compliance-healthcare-saas-guide)
- [PCI DSS Compliance: The Complete Guide](/blog/pillar-pci-dss-complete-guide)
- [Data Security in the Cloud: The Compliance Controls AWS, GCP, and Azure Customers Cannot Skip](/blog/cloud-security-compliance-aws-gcp-azure)
- [Information Security Policy: The Complete Guide](/blog/information-security-policy-guide)
- [Vendor Risk Management: The Complete Program Guide](/blog/vendor-risk-management-complete-guide)
- [Incident Response Plan: How to Build One That Passes Every Audit](/blog/incident-response-plan-compliance-guide)
