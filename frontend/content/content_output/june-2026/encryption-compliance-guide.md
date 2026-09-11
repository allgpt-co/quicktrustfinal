---
title: "Encryption at Rest and In Transit: The Complete Compliance Guide for SOC 2, ISO 27001, HIPAA, and PCI DSS"
meta_description: "Encryption requirements for SOC 2, ISO 27001, HIPAA, and PCI DSS. Covers AES-256, TLS, key management, cloud KMS, and common audit failures."
target_keyword: "encryption compliance requirements"
secondary_keywords: "encryption at rest SOC 2, TLS compliance HIPAA, AES-256 compliance, key management ISO 27001, PCI DSS encryption requirements, AWS KMS compliance"
word_count_target: "1500"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# Encryption at Rest and In Transit: The Complete Compliance Guide for SOC 2, ISO 27001, HIPAA, and PCI DSS

Encryption is one of the most scrutinized controls in any compliance audit. Every major framework -- SOC 2, ISO 27001, HIPAA, and PCI DSS -- requires organizations to protect sensitive data through encryption, both when it is stored (at rest) and when it moves between systems (in transit). Despite this universal requirement, encryption remains a frequent source of audit findings, not because organizations fail to encrypt, but because they encrypt inconsistently, manage keys poorly, or cannot produce evidence of their encryption posture.

This guide covers what each framework requires, which encryption standards satisfy auditors, how to implement encryption correctly across cloud environments, and where organizations most commonly fail.

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

## Key Management

Encryption without proper key management is like locking a door and leaving the key under the mat. Every framework requires a documented key management lifecycle:

**Key generation:** Keys must be generated using cryptographically secure random number generators. Hardware Security Modules (HSMs) provide the highest assurance.

**Key storage:** Encryption keys must never be stored alongside the data they protect. Use dedicated key management services (cloud KMS or HSMs) rather than storing keys in application code, configuration files, or environment variables.

**Key rotation:** Define and enforce key rotation schedules. Annual rotation is the standard expectation. PCI DSS requires rotation when there is a known or suspected compromise and recommends annual rotation as a best practice. Ensure your encryption implementation supports key rotation without data downtime.

**Key access control:** Limit key access to the minimum number of individuals required. PCI DSS requires split knowledge and dual control for manual key management operations.

**Key retirement and destruction:** Define procedures for retiring old keys and securely destroying keys that are no longer needed. Maintain records of key lifecycle events.

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

## Common Audit Failures

**Unencrypted data stores discovered during audit.** The most straightforward failure: auditors find databases, object storage buckets, or disk volumes that contain in-scope data without encryption enabled. This is particularly common with legacy systems, development environments that mirror production data, and backup storage.

**TLS misconfiguration.** Auditors run TLS scans (using tools like Qualys SSL Labs) against your endpoints. Common findings include TLS 1.0 or 1.1 still enabled, weak cipher suites in the configuration, expired or self-signed certificates on internal services that handle sensitive data, and missing HSTS headers.

**Keys stored in application code.** Hardcoded encryption keys in source code repositories, configuration files checked into version control, or environment variables accessible to broad user groups represent a fundamental key management failure.

**No key rotation evidence.** Even with encryption properly implemented, the absence of documented key rotation creates audit findings. Auditors check KMS logs, key creation dates, and rotation policies.

**Inconsistent encryption policy.** Having a policy that requires AES-256 encryption for Confidential data but deploying AES-128 or no encryption on some Confidential data stores demonstrates a gap between policy and practice.

**Missing encryption in non-production environments.** If test or staging environments contain copies of production data (especially PHI or cardholder data), those environments must meet the same encryption requirements. Auditors check non-production systems specifically for this gap.

## How QuickTrust Engineers Implement Encryption

QuickTrust engineers approach encryption as an infrastructure-level control that must be implemented consistently, verified automatically, and evidenced continuously.

The engagement begins with a data store inventory across your cloud environment, identifying every database, object store, disk volume, queue, and cache that holds in-scope data. Engineers audit existing encryption configurations and identify gaps -- unencrypted data stores, weak TLS configurations, keys stored insecurely, and missing key rotation policies.

Remediation follows a systematic approach. Engineers enable encryption at rest across all in-scope data stores using customer-managed KMS keys, configure KMS key policies with least-privilege access, set up automatic annual key rotation, harden TLS configurations across all endpoints (disabling legacy protocols and weak cipher suites), implement certificate management automation to prevent expiration-related outages, and deploy infrastructure-as-code checks that prevent deployment of unencrypted resources.

For HIPAA-covered organizations, engineers ensure ePHI data stores use AES-256 encryption with customer-managed keys and that all PHI transmission channels use TLS 1.2 or higher. For PCI DSS environments, engineers implement the specific key management procedures required by Requirements 3.6 and 3.7, including documented key custodian assignments and split knowledge procedures.

The deliverable is an encryption posture that auditors can verify through KMS logs, infrastructure configurations, TLS scan results, and key rotation records -- all produced automatically and ready for evidence collection.

## Conclusion

Encryption compliance is not about checking a box. It requires the right algorithms, proper key management, consistent implementation across all in-scope systems, and evidence that proves it. Organizations that implement encryption correctly across their infrastructure -- with documented policies, managed keys, and verifiable configurations -- will find encryption to be one of the most straightforward controls to demonstrate during an audit. Those that implement it inconsistently will find it to be one of the most common sources of findings.

Get the fundamentals right: AES-256 at rest, TLS 1.2+ in transit, keys managed in dedicated services, rotation automated, and every in-scope data store covered. The frameworks differ in specificity, but the practical requirements converge on the same set of best practices.
