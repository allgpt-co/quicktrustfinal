---
title: "Encryption Compliance: Key Management and Evidence"
meta_description: "Encryption Compliance: Key Management and Evidence. Practical guidance for reviewing key-management operations and evidence needs."
target_keyword: "encryption compliance requirements"
secondary_keywords: "encryption at rest SOC 2, TLS compliance HIPAA, AES-256 compliance, key management ISO 27001, PCI DSS encryption requirements, AWS KMS compliance, encryption at rest"
word_count_target: "1500"
published: true
author: QuickTrust Editorial
last_updated: "2026-10-02"
---


# Encryption Compliance: Key Management and Evidence

This guide covers protection boundaries, practical implementation choices, key-management operations and the evidence auditors expect.

Encryption is one of the most scrutinized controls in any compliance audit. Every major framework -- SOC 2, ISO 27001, HIPAA, and PCI DSS -- requires organizations to protect sensitive data through encryption, both when it is stored (at rest) and when it moves between systems (in transit). Despite this universal requirement, encryption remains a frequent source of audit findings, not because organizations fail to encrypt, but because they encrypt inconsistently, manage keys poorly, or cannot produce evidence of their encryption posture.

This guide covers what each framework requires, which encryption standards satisfy auditors, how to implement encryption correctly across cloud environments, and where organizations most commonly fail.

## At Rest and In Transit Are Separate Controls

Frameworks evaluate the two independently, and auditors test them independently. Implementing one without the other is insufficient.

| Dimension | Encryption at Rest | Encryption in Transit |
|---|---|---|
| **Protects data when** | Stored on disk or persistent media | Moving across a network |
| **Threat model** | Unauthorized physical or logical access to storage | Network eavesdropping, man-in-the-middle attacks |
| **Primary mechanism** | AES-256 (symmetric) | TLS 1.2/1.3 (asymmetric key exchange plus symmetric session keys) |
| **Implementation layer** | Disk, database, file system, application | Network and transport layer |
| **Common failure** | Unencrypted backups, unencrypted database volumes | Internal service-to-service traffic in plaintext |
| **Compliance references** | SOC 2 CC6.1, ISO A.8.24, HIPAA 164.312(a)(2)(iv), PCI DSS 3.5 | SOC 2 CC6.7, ISO A.8.24, HIPAA 164.312(e)(1), PCI DSS 4.2 |

## Encryption Requirements by Framework

### SOC 2

SOC 2 does not prescribe specific encryption algorithms, but the Common Criteria and Confidentiality criteria require organizations to protect information during transmission (CC6.7) and to protect confidential information from unauthorized access (C1.1, C1.2). Auditors expect industry-standard encryption for data classified as confidential or higher. In practice, this means AES-256 for data at rest and TLS 1.2 or higher for data in transit. Failure to encrypt confidential data is treated as a control deficiency.

### ISO 27001

ISO 27001 Annex A control A.8.24 (Use of Cryptography) requires organizations to define and implement a policy on the use of cryptographic controls, including key management. The standard does not mandate specific algorithms but requires that cryptographic controls are appropriate to the classification of the information being protected. Auditors evaluate whether your cryptographic policy exists, is approved by management, and is implemented consistently across your information assets.

### HIPAA

The HIPAA Security Rule addresses encryption in two places. The transmission security standard (164.312(e)(1)) requires covered entities to implement technical security measures to guard against unauthorized access to ePHI during transmission. Encryption of ePHI in transit is an addressable implementation specification -- meaning you must implement it or document why an alternative measure provides equivalent protection. In practice, every auditor expects encryption in transit for ePHI.

Encryption at rest is not explicitly required by the Security Rule's access control standard, but it is strongly recommended as a mechanism to satisfy the integrity controls requirement (164.312(c)(1)). More importantly, under the Breach Notification Rule (164.402), encrypted ePHI that is accessed without authorization is excluded from the definition of a breach if the encryption meets NIST standards. This "safe harbor" provision makes encryption at rest effectively mandatory for any organization that wants to avoid breach notification obligations.

### PCI DSS

PCI DSS is the most prescriptive framework regarding encryption. Requirement 3 requires protection of stored cardholder data, with specific mandates for strong cryptography with associated key management processes. Requirement 4 requires encryption of cardholder data during transmission over open, public networks using strong cryptography. PCI DSS 4.0 strengthened these requirements further, explicitly requiring TLS 1.2 or higher and prohibiting the use of SSL and early TLS for protecting cardholder data.

PCI DSS also mandates specific key management practices under Requirement 3.6 and 3.7, including key generation using strong random number generators, secure key distribution, protection of stored keys, periodic key rotation, retirement and replacement of compromised keys, and split knowledge and dual control procedures.

## Encryption Standards That Satisfy Auditors

### Encryption at Rest

**AES-256** (Advanced Encryption Standard with 256-bit keys) is the gold standard for data at rest encryption across all four frameworks. AES-128 is technically acceptable under most frameworks, but AES-256 is preferred and avoids any auditor pushback. For database-level encryption, AES-256 in CBC or GCM mode is standard.

Other acceptable algorithms include:
- **AES-128:** Acceptable but may require justification for sensitive data categories
- **ChaCha20-Poly1305:** Acceptable, commonly used in mobile and IoT contexts
- **RSA-2048 or higher:** For asymmetric encryption of keys and small data payloads

Algorithms that are not acceptable:
- **DES and 3DES:** Deprecated and explicitly prohibited by PCI DSS 4.0 after December 31, 2023
- **RC4:** Known vulnerabilities, prohibited across all frameworks
- **MD5 and SHA-1 for hashing:** Not recommended; use SHA-256 or higher

### Encryption in Transit

**TLS 1.2** is the minimum acceptable version across all frameworks. TLS 1.3 is preferred where supported. Auditors will check your TLS configuration for:

- **Protocol version:** TLS 1.2 or 1.3 only. TLS 1.0 and 1.1 must be disabled.
- **Cipher suites:** Only strong cipher suites should be enabled. Disable NULL ciphers, export ciphers, DES, RC4, and any cipher suite with less than 128-bit key strength. Prefer AEAD cipher suites (GCM mode) and forward secrecy (ECDHE or DHE key exchange).
- **Certificate validity:** Certificates must be valid, not expired, issued by a trusted certificate authority, and use RSA-2048+ or ECC P-256+ keys.
- **HSTS (HTTP Strict Transport Security):** Should be enabled for web applications to prevent protocol downgrade attacks.

## Covering Every Storage Layer

Audit findings rarely come from the primary production database. They come from the layers nobody inventoried.

**Databases.** Enable Transparent Data Encryption on every production database. Cloud-managed services often enable it by default, but verify rather than assume. RDS encryption must be set at creation. Cloud SQL and Azure SQL default to provider-managed keys, and customer-managed keys must be configured deliberately. The same applies to managed NoSQL services such as DynamoDB, Firestore, and MongoDB Atlas.

**Object and block storage.** Turn on default encryption for every bucket and volume. On AWS, the `s3-bucket-server-side-encryption-enabled` Config rule detects non-compliant buckets automatically. Use customer-managed keys for data subject to compliance requirements.

**Full-disk encryption.** Enforce it on servers, including development and staging, and on every company-issued laptop through FileVault, BitLocker, or LUKS. Use MDM to verify and enforce the status, because auditors ask for fleet-wide evidence, not a policy statement.

**Backups.** Production data is encrypted but the nightly dump written to an object storage bucket is not. That single gap invalidates the control for all of that data. Verify that backups, snapshots, and archives inherit or explicitly configure encryption, and test restoration from encrypted backups to confirm the keys are accessible.

**Field-level encryption.** For the most sensitive elements (Social Security numbers, account numbers, health identifiers, API secrets), encrypt individual fields in the application layer so that database administrators and anyone with SELECT access see only ciphertext. Well-audited libraries include the AWS Encryption SDK, Google Tink, and libsodium. Encrypted fields cannot be searched directly; blind indexing (a keyed hash stored alongside the ciphertext) supports exact-match queries, and deterministic encryption supports equality searches at the cost of leaking frequency information.

## In Transit: Certificates, HSTS, and Internal Traffic

**Certificate management.** Manual renewal is a reliable source of both outages and findings. Use a CA that supports automated issuance and renewal (Let's Encrypt, AWS Certificate Manager, GCP Certificate Manager, or Azure App Service Certificates), automate renewal, and alert on certificates approaching expiration.

**HSTS configuration.** Set the `Strict-Transport-Security` header with a `max-age` of at least `31536000` and the `includeSubDomains` directive. Once behavior is verified, consider submitting the domain to the HSTS preload list. Missing HSTS on a public application is one of the easiest findings for an auditor to write.

**Internal service-to-service traffic.** This is where most SaaS companies have gaps. External traffic is encrypted while microservices talk over plaintext HTTP. A service mesh with mTLS (Istio, Linkerd, Consul Connect) is the most complete solution. If a mesh is not practical, issue internal certificates from an internal CA such as HashiCorp Vault, AWS Private CA, or step-ca, and enable TLS on internal load balancers.

**Database connections.** Application-to-database connections frequently run unencrypted over the internal network, exposing credentials and query results. Every major engine supports TLS for client connections. Enforce it: `sslmode=verify-full` for PostgreSQL, `--require_secure_transport=ON` on the server and `ssl-mode=REQUIRED` on the client for MySQL.

## Key Management

Encryption without proper key management is like locking a door and leaving the key under the mat. Every framework requires a documented key management lifecycle:

**Key generation:** Keys must be generated using cryptographically secure random number generators. Hardware Security Modules (HSMs) provide the highest assurance.

**Key storage:** Encryption keys must never be stored alongside the data they protect. Use dedicated key management services (cloud KMS or HSMs) rather than storing keys in application code, configuration files, or environment variables.

**Key rotation:** Define and enforce key rotation schedules. Annual rotation is the standard expectation. PCI DSS requires rotation when there is a known or suspected compromise and recommends annual rotation as a best practice. Ensure your encryption implementation supports key rotation without data downtime.

**Key access control:** Limit key access to the minimum number of individuals required. PCI DSS requires split knowledge and dual control for manual key management operations.

**Key retirement and destruction:** Define procedures for retiring old keys and securely destroying keys that are no longer needed. Maintain records of key lifecycle events.

### Envelope Encryption

The standard cloud pattern is two-tier. Data is encrypted with a data encryption key (DEK), and the DEK is encrypted with a key encryption key (KEK) held in the KMS. This is efficient because the KMS only handles the small DEK, not the data payload. It makes rotation practical because rotating the KEK means re-encrypting the DEK rather than all the underlying data. And it centralizes the audit trail, since every key operation is logged by the KMS. AWS KMS, GCP Cloud KMS, and Azure Key Vault all implement it natively.

### Separation of Duties

Auditors verify that the people or service accounts that manage keys are not the same ones that access encrypted data. Implement this in IAM: grant key management permissions (create, rotate, delete) to a security or infrastructure team, and grant key usage permissions (encrypt, decrypt) to the application service accounts that read and write data. Use distinct roles and least privilege. Key deletion should require multi-party approval or a waiting period.

### Provider-Managed Keys, CMK, BYOK, and HYOK

| Approach | Description | Compliance implication |
|---|---|---|
| **Provider-managed keys** | The cloud provider generates and manages keys entirely | Sufficient for a SOC 2 and ISO 27001 baseline; HIPAA and PCI DSS assessors may want more assurance |
| **Customer-managed keys (CMK)** | You create keys in the provider's KMS and control the access policies | Preferred across all frameworks; provides a customer-controlled audit trail of key usage |
| **Bring Your Own Key (BYOK)** | You generate keys outside the cloud and import them into the provider's KMS | Required by some financial regulators and government contracts; adds operational complexity |
| **Hold Your Own Key (HYOK)** | You hold the key externally and the provider never has the plaintext key | Maximum control; limits some cloud service functionality |

For most SaaS companies pursuing SOC 2, ISO 27001, HIPAA, or PCI DSS, customer-managed keys in the provider's KMS are the right balance of security, auditability, and operational simplicity. BYOK is rarely justified unless a specific regulatory or contractual requirement demands it.

## Cloud Provider Encryption Options

### AWS

**AWS KMS (Key Management Service):** Provides centralized key management with automatic key rotation (annual for AWS-managed keys). Integrates natively with S3, EBS, RDS, DynamoDB, and other AWS services for encryption at rest. Supports both AWS-managed keys and customer-managed keys (CMKs). For the highest assurance, use customer-managed CMKs with imported key material or CloudHSM-backed keys.

**AWS CloudHSM:** Provides FIPS 140-2 Level 3 validated HSMs for key storage and cryptographic operations. Required for certain PCI DSS and HIPAA deployments.

**S3 encryption options:** SSE-S3 (AWS-managed keys), SSE-KMS (KMS-managed keys), and SSE-C (customer-provided keys). For compliance, SSE-KMS with customer-managed keys provides the best balance of security and auditability.

**RDS encryption:** Enable encryption at creation time using KMS keys. Note that RDS encryption cannot be enabled on existing unencrypted instances -- you must create an encrypted snapshot and restore from it.

### Google Cloud Platform

**Cloud KMS:** Managed key service supporting symmetric and asymmetric keys with configurable rotation schedules. Integrates with GCS, Cloud SQL, BigQuery, and Compute Engine. Supports software-backed keys, HSM-backed keys (Cloud HSM), and external key manager integration.

**Customer-Managed Encryption Keys (CMEK):** Apply your own KMS keys to GCP services instead of relying on Google-managed default encryption.

**Cloud HSM:** FIPS 140-2 Level 3 validated HSMs within Cloud KMS for high-assurance key management.

### Microsoft Azure

**Azure Key Vault:** Centralized key management service supporting keys, secrets, and certificates. Offers Standard (software-protected) and Premium (HSM-protected) tiers. Integrates with Azure SQL, Blob Storage, Disk Encryption, and other Azure services.

**Azure Disk Encryption:** Uses BitLocker (Windows) or dm-crypt (Linux) with keys stored in Key Vault for virtual machine disk encryption.

**Transparent Data Encryption (TDE):** Enabled by default for Azure SQL Database and Azure Synapse Analytics. Supports service-managed keys or customer-managed keys through Key Vault.

## Multi-Tenant SaaS Considerations

When many customers share infrastructure, the encryption strategy has to account for tenant isolation and customer-specific key requirements.

**Per-tenant keys.** Assign each tenant a unique DEK stored in the KMS and wrapped by a master KEK through envelope encryption. Use KMS key policies or IAM conditions so that a service processing Tenant A's data cannot reach Tenant B's key. Performance overhead is small because the DEK is cached after the first decryption; the KMS is not called on every operation. Per-tenant keys also enable cryptographic deletion: when a customer offboards, deleting their key renders their data unrecoverable without depending on database deletion alone. Enterprise buyers increasingly ask for this contractually.

**Customer-managed keys for enterprise tenants.** Some customers require that their own KMS (AWS KMS, Cloud KMS, or Key Vault) wrap the DEK for their data, so they can revoke access at any time. Your application must handle revocation gracefully with circuit breakers and clear error messaging. Offering this is a meaningful differentiator in enterprise security reviews.

## Common Audit Failures

**Unencrypted data stores discovered during audit.** The most straightforward failure: auditors find databases, object storage buckets, or disk volumes that contain in-scope data without encryption enabled. This is particularly common with legacy systems, development environments that mirror production data, and backup storage.

**TLS misconfiguration.** Auditors run TLS scans (using tools like Qualys SSL Labs) against your endpoints. Common findings include TLS 1.0 or 1.1 still enabled, weak cipher suites in the configuration, expired or self-signed certificates on internal services that handle sensitive data, and missing HSTS headers.

**Keys stored in application code.** Hardcoded encryption keys in source code repositories, configuration files checked into version control, or environment variables accessible to broad user groups represent a fundamental key management failure.

**No key rotation evidence.** Even with encryption properly implemented, the absence of documented key rotation creates audit findings. Auditors check KMS logs, key creation dates, and rotation policies.

**Inconsistent encryption policy.** Having a policy that requires AES-256 encryption for Confidential data but deploying AES-128 or no encryption on some Confidential data stores demonstrates a gap between policy and practice.

**Missing encryption in non-production environments.** If test or staging environments contain copies of production data (especially PHI or cardholder data), those environments must meet the same encryption requirements. Auditors check non-production systems specifically for this gap.

**Internal traffic unencrypted.** Microservices and application-to-database connections run over plaintext HTTP or non-TLS database protocols inside the network. Prioritize connections that carry sensitive data: database connections, authentication services, and anything handling PII.

**No evidence that encryption is actually enabled.** The policy says encryption is used, but there are no configuration exports, screenshots, or audit logs showing it is active on specific resources. Auditors need evidence, not assertions.

## Encryption Compliance Checklist

**At rest**
- [ ] All production databases, data warehouses, and analytics stores encrypted at rest
- [ ] Default encryption enabled on every object storage bucket and block storage volume
- [ ] All database backups and snapshots encrypted
- [ ] Full-disk encryption enforced on servers and employee endpoints, verified through MDM
- [ ] Development and staging environments holding customer data copies encrypted
- [ ] Field-level encryption applied to the most sensitive data elements

**In transit**
- [ ] TLS 1.2 minimum on all external endpoints and APIs, with TLS 1.0 and 1.1 explicitly disabled
- [ ] HSTS configured with a max-age of at least one year
- [ ] Internal service-to-service traffic encrypted with TLS or mTLS
- [ ] Database connections from application servers use TLS
- [ ] VPN or encrypted tunnels for site-to-site connectivity; SSH only for administrative access
- [ ] Certificate renewal automated with expiration monitoring

**Key management**
- [ ] Keys managed in a dedicated KMS, never in code or configuration files
- [ ] Envelope encryption in use
- [ ] Rotation policy documented, automatic rotation enabled where available
- [ ] Separation of duties between key administrators and data users
- [ ] Key access logged and auditable; key deletion gated by approval or a waiting period
- [ ] Retired keys decommissioned and documented

**Documentation and evidence**
- [ ] Encryption policy approved by management and reviewed at least annually
- [ ] Configuration evidence collected and mapped to specific controls (CC6.1, CC6.7, A.8.24, 164.312, Requirements 3.5 and 4.2)
- [ ] Exceptions documented with risk assessments and compensating controls

## Frequently Asked Questions

### Can we rely on the cloud provider's default encryption?

Default encryption such as SSE-S3 or GCP's provider-managed keys satisfies the baseline at-rest requirement for SOC 2 and ISO 27001. HIPAA and PCI DSS assessors generally prefer customer-managed keys because they give you a customer-controlled audit trail and prevent the provider from having sole control over decryption. Customer-managed keys through the provider's KMS are the recommended approach for every framework.

### How do we prove encryption is enabled during an audit?

Collect and keep: configuration exports or console screenshots showing encryption on databases, buckets, and volumes; Config rule evaluation results or the equivalent; SSL Labs results and `openssl s_client` output for public endpoints showing TLS version and cipher suite; KMS audit logs showing key creation, rotation, and usage; the approved encryption policy with its review date; and rotation records such as KMS logs or change tickets. Each artifact should be mapped to the control it satisfies.

## How QuickTrust Engineers Implement Encryption

QuickTrust engineers approach encryption as an infrastructure-level control that must be implemented consistently, verified automatically, and evidenced continuously.

The engagement begins with a data store inventory across your cloud environment, identifying every database, object store, disk volume, queue, and cache that holds in-scope data. Engineers audit existing encryption configurations and identify gaps -- unencrypted data stores, weak TLS configurations, keys stored insecurely, and missing key rotation policies.

Remediation follows a systematic approach. Engineers enable encryption at rest across all in-scope data stores using customer-managed KMS keys, configure KMS key policies with least-privilege access, set up automatic annual key rotation, harden TLS configurations across all endpoints (disabling legacy protocols and weak cipher suites), implement certificate management automation to prevent expiration-related outages, and deploy infrastructure-as-code checks that prevent deployment of unencrypted resources.

For HIPAA-covered organizations, engineers ensure ePHI data stores use AES-256 encryption with customer-managed keys and that all PHI transmission channels use TLS 1.2 or higher. For PCI DSS environments, engineers implement the specific key management procedures required by Requirements 3.6 and 3.7, including documented key custodian assignments and split knowledge procedures.

The deliverable is an encryption posture that auditors can verify through KMS logs, infrastructure configurations, TLS scan results, and key rotation records -- all produced automatically and ready for evidence collection.

## Conclusion

Encryption compliance is not about checking a box. It requires the right algorithms, proper key management, consistent implementation across all in-scope systems, and evidence that proves it. Organizations that implement encryption correctly across their infrastructure -- with documented policies, managed keys, and verifiable configurations -- will find encryption to be one of the most straightforward controls to demonstrate during an audit. Those that implement it inconsistently will find it to be one of the most common sources of findings.

Get the fundamentals right: AES-256 at rest, TLS 1.2+ in transit, keys managed in dedicated services, rotation automated, and every in-scope data store covered. The frameworks differ in specificity, but the practical requirements converge on the same set of best practices.
