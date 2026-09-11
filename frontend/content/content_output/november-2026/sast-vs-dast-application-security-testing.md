---
meta_description: "SAST vs DAST explained: when to use each, how they map to SOC 2 and PCI DSS compliance, and how to build a complete application security testing program with SAST, DAST, IAST, and SCA."
target_keyword: "sast dast"
secondary_keywords: "SAST vs DAST, static application security testing, dynamic application security testing, application security testing, SAST DAST IAST, AppSec testing"
word_count_target: 4000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-21
---

# SAST vs DAST: The Complete Guide to Application Security Testing for Compliance

Applications are the primary attack surface for most technology companies. Not networks. Not endpoints. Applications. The Verizon 2025 Data Breach Investigations Report found that web application attacks accounted for more than 60% of confirmed breaches -- and the trend line is going up, not down. APIs, microservices, and cloud-native architectures have expanded the attack surface faster than most security programs have adapted.

Every major compliance framework now requires organizations to test their applications for security vulnerabilities before deployment and on an ongoing basis. SOC 2, ISO 27001, PCI DSS, and NIST 800-53 all mandate some combination of code-level security analysis, runtime vulnerability testing, and third-party component scanning. The frameworks do not prescribe specific tools, but they expect organizations to demonstrate that they have a systematic, documented approach to finding and fixing application-level vulnerabilities.

This is where application security testing -- specifically SAST, DAST, IAST, and SCA -- comes in. These are not buzzwords. They are distinct testing methodologies, each designed to find different categories of vulnerabilities at different stages of the software development lifecycle. Understanding what each one does, where it fits, and how they map to compliance requirements is essential for any engineering or security leader building an audit-ready application security program.

This guide covers all four testing methodologies in depth, provides a head-to-head comparison of SAST vs DAST, maps each approach to specific compliance framework controls, and lays out a practical plan for building a complete AppSec testing program that generates audit evidence automatically.

---

## What Is Application Security Testing?

Application security testing (AST) is the practice of identifying security vulnerabilities, weaknesses, and misconfigurations in software applications through a combination of automated tools and manual techniques. It encompasses every method used to evaluate whether application code -- both proprietary and third-party -- is resistant to exploitation.

AST is not a single activity. It is a category that includes multiple distinct testing methodologies:

- **SAST (Static Application Security Testing)** -- analyzes source code, bytecode, or binaries without executing the application
- **DAST (Dynamic Application Security Testing)** -- tests a running application from the outside by sending crafted requests and analyzing responses
- **IAST (Interactive Application Security Testing)** -- instruments the running application to monitor code execution paths during testing
- **SCA (Software Composition Analysis)** -- identifies known vulnerabilities in open-source and third-party dependencies

Each methodology finds different types of vulnerabilities at different stages of the development lifecycle. No single approach covers all vulnerability classes. A mature application security program uses multiple methodologies in combination, and compliance frameworks increasingly expect evidence of exactly this layered approach.

### Why Application Security Testing Matters for Compliance

Compliance frameworks care about application security testing because applications are where sensitive data lives, where business logic is implemented, and where attackers focus their efforts. The frameworks require organizations to demonstrate three things:

1. **Prevention** -- that security is built into the development process, not bolted on after deployment
2. **Detection** -- that vulnerabilities are identified through systematic, repeatable testing before they reach production
3. **Remediation** -- that identified vulnerabilities are tracked, prioritized, and fixed within defined timelines

Application security testing provides evidence for all three. SAST in the IDE provides prevention evidence. SAST and DAST in the CI/CD pipeline provide detection evidence. Ticket-level tracking of findings provides remediation evidence. Together, they form a continuous loop that auditors can evaluate against specific framework controls.

For a broader view of how vulnerability identification fits into compliance programs, see our [Vulnerability Management Program Guide](/blog/vulnerability-management-program-guide).

---

## SAST: Static Application Security Testing

Static Application Security Testing analyzes application source code, bytecode, or compiled binaries to identify security vulnerabilities without executing the application. Think of SAST as a security-focused code review performed by a machine -- it reads the code, traces data flows through functions and modules, identifies patterns known to be dangerous, and reports findings with precise file-and-line-number references.

### How SAST Works

SAST tools operate by building a model of the application's code structure -- an abstract syntax tree (AST), control flow graph (CFG), and data flow graph (DFG) -- and then querying that model for patterns that match known vulnerability classes. The analysis follows data from its point of entry (a source) through all possible code paths to its point of use (a sink). If untrusted data flows from a source to a dangerous sink without passing through proper validation or sanitization (a sanitizer), the tool flags a potential vulnerability.

For example, SAST can trace user input from an HTTP request parameter through multiple function calls, across module boundaries, and into a database query. If the input reaches the query without parameterized binding or proper escaping, the tool identifies a SQL injection vulnerability and reports the exact file, line number, and data flow path.

### What SAST Finds

SAST excels at identifying code-level vulnerability classes:

- **Injection flaws** -- SQL injection, command injection, LDAP injection, XPath injection, expression language injection
- **Cross-site scripting (XSS)** -- reflected, stored, and DOM-based variants where untrusted data is rendered in HTML output
- **Insecure cryptography** -- use of deprecated algorithms (MD5, SHA1 for hashing passwords, DES, RC4), hardcoded encryption keys, insufficient key lengths
- **Hardcoded secrets** -- API keys, passwords, tokens, and connection strings embedded directly in source code
- **Buffer overflows and memory safety issues** -- primarily in C/C++ codebases: stack overflows, heap overflows, use-after-free
- **Authentication and session management weaknesses** -- weak password validation logic, insecure session token generation, missing authentication checks
- **Race conditions** -- time-of-check-time-of-use (TOCTOU) vulnerabilities in concurrent code
- **Insecure deserialization** -- use of unsafe deserialization functions on untrusted input
- **Path traversal** -- file operations that accept user-controlled input without proper validation

### When to Use SAST

SAST provides maximum value when integrated at two points in the development lifecycle:

**In the IDE (real-time).** Developers receive security feedback as they write code, before a commit even occurs. This is the cheapest possible point to fix a vulnerability -- the developer is already looking at the relevant code and has full context. IDE-integrated SAST plugins from tools like Semgrep, SonarLint, and Snyk Code deliver near-instant feedback.

**In the CI/CD pipeline (pre-merge).** SAST runs as a required status check on every pull request. Findings above a defined severity threshold block the merge. This ensures no known vulnerability patterns enter the main branch. Pipeline-stage SAST is the primary evidence source for SOC 2 CC7.1 and ISO 27001 A.8.25 compliance.

### SAST Limitations

SAST is powerful, but it has known blind spots that make it insufficient as a standalone testing methodology:

- **High false positive rate.** SAST tools report potential vulnerabilities based on code patterns, not confirmed exploitability. Industry benchmarks consistently show false positive rates between 30% and 60% for commercial SAST tools. Every false positive consumes developer time to triage, creates alert fatigue, and erodes trust in the tooling.
- **Cannot find runtime or configuration vulnerabilities.** SAST analyzes code in isolation. It cannot detect misconfigured servers, insecure TLS settings, missing HTTP security headers, broken access control at the deployment level, or authentication bypasses that depend on how multiple services interact.
- **Limited for business logic flaws.** SAST looks for known vulnerability patterns. It cannot understand application-specific business logic -- for example, it will not detect that a user can modify the quantity field in a shopping cart to a negative number and receive a refund.
- **Language and framework dependent.** Each SAST tool supports a specific set of programming languages and frameworks. Coverage varies significantly. A tool that provides excellent Java analysis may have superficial Python support.

---

## DAST: Dynamic Application Security Testing

Dynamic Application Security Testing evaluates a running application by interacting with it from the outside -- exactly as an attacker would. DAST tools send carefully crafted HTTP requests (and, increasingly, WebSocket messages, GraphQL queries, and gRPC calls) to the application, analyze the responses, and identify vulnerabilities based on the application's observable behavior. DAST does not look at source code. It does not require access to the codebase. It tests the deployed application as a black box.

### How DAST Works

A DAST tool begins by crawling or spidering the target application to discover all accessible endpoints, forms, parameters, and API routes. It then systematically sends attack payloads to each discovered input -- injection strings, oversized inputs, malformed data, authentication bypass attempts, and known exploit patterns. The tool analyzes HTTP responses for indicators of vulnerability: error messages that reveal stack traces, reflected input in HTML output, timing differences that suggest blind injection, authentication tokens that do not rotate, cookies missing security attributes, and responses that return data the authenticated user should not be able to access.

Modern DAST tools also support authenticated scanning, where the tool logs in as a specific user role and tests whether authorization controls are properly enforced. This is critical for finding broken access control vulnerabilities -- the OWASP Top 10 number one issue.

### What DAST Finds

DAST excels at identifying runtime and deployment-level vulnerabilities:

- **Server and infrastructure misconfigurations** -- exposed admin panels, directory listing enabled, default credentials, verbose error pages, debug modes left active in production
- **Missing or misconfigured HTTP security headers** -- absent Content-Security-Policy, X-Frame-Options, Strict-Transport-Security, X-Content-Type-Options headers
- **TLS/SSL weaknesses** -- expired certificates, weak cipher suites, missing HSTS, protocol downgrade vulnerabilities
- **Authentication vulnerabilities** -- brute force susceptibility, session fixation, insecure password reset flows, missing multi-factor authentication on sensitive endpoints
- **Broken access control** -- IDOR (Insecure Direct Object Reference), privilege escalation, horizontal access control failures, missing function-level authorization
- **Cross-site scripting (reflected)** -- confirmed XSS where injected scripts execute in the response
- **SQL injection (confirmed)** -- injection payloads that trigger observable database errors or behavior changes
- **CORS misconfigurations** -- overly permissive cross-origin resource sharing policies that enable data theft
- **API-specific vulnerabilities** -- excessive data exposure, mass assignment, missing rate limiting, broken object-level authorization

### When to Use DAST

DAST provides maximum value when deployed against a running instance of the application:

**In staging or pre-production.** DAST scans run against a deployed staging environment before code is promoted to production. This catches deployment-level vulnerabilities that SAST cannot see: misconfigured web servers, missing security headers, broken authentication flows, and TLS issues. For compliance, this is evidence that security testing occurs before production deployment -- a direct requirement of SOC 2 CC8.1 and ISO 27001 A.8.29.

**Against production (with care).** Some organizations run passive or low-impact DAST scans against production environments to catch configuration drift and newly introduced vulnerabilities. Active DAST scanning in production requires careful scoping to avoid service disruption, data corruption, or triggering WAF/IDS alerts.

**After every deployment.** In mature CI/CD environments, a lightweight DAST scan runs after each staging deployment, with a comprehensive weekly or monthly scan augmenting the continuous checks.

### DAST Limitations

- **Cannot pinpoint code location.** DAST tells you that a vulnerability exists at a specific endpoint, but it cannot tell you which file, function, or line of code is responsible. Developers receive a finding like "SQL injection on /api/users?id=1" and must trace the vulnerability back through the codebase themselves.
- **Slower than SAST.** DAST must interact with a running application over HTTP. A comprehensive scan of a large application can take hours. This makes it impractical as a pre-merge CI check for every pull request.
- **Coverage depends on crawl depth.** If the DAST tool cannot discover an endpoint -- because it is behind complex JavaScript rendering, requires multi-step authentication, or is only accessible through specific API sequences -- it will not test that endpoint. Incomplete crawling means incomplete coverage.
- **Cannot find issues in non-deployed code paths.** DAST tests what is deployed and reachable. Dead code, unused endpoints, or functionality behind feature flags will not be tested.

---

## SAST vs DAST: Head-to-Head Comparison

Understanding when to use SAST and when to use DAST is the foundation of any application security testing strategy. They are complementary, not competing. The following comparison clarifies where each methodology fits.

| Dimension | SAST | DAST |
|---|---|---|
| **What it analyzes** | Source code, bytecode, or binaries | Running application (HTTP/HTTPS interface) |
| **Code access required** | Yes -- needs access to the source code or compiled artifacts | No -- black-box testing against a deployed endpoint |
| **When it runs** | During development or at build time (pre-deployment) | After deployment, against a running instance |
| **Vulnerability types** | Code-level flaws: injection patterns, insecure crypto, hardcoded secrets, buffer overflows, XSS patterns | Runtime flaws: misconfigurations, missing headers, auth bypasses, TLS issues, CORS, confirmed injection |
| **Precision** | Higher false positive rate (30-60%); reports potential patterns | Lower false positive rate (10-25%); confirms exploitability |
| **Speed** | Fast (minutes for incremental scans, 15-60 min for full scans) | Slow (hours for comprehensive scans) |
| **Developer workflow** | Integrates into IDE and CI pipeline; findings include file/line references | Results delivered post-deployment; findings reference endpoints, not code |
| **Language support** | Language-specific; each tool supports a defined set | Language-agnostic; tests the application regardless of tech stack |
| **Coverage gaps** | Cannot find runtime/config issues, missing headers, deployment misconfigurations | Cannot find issues in undeployed code, internal logic flaws, hardcoded secrets |
| **SDLC position** | Shift left -- earliest possible detection | Post-deployment -- validates the running system |
| **Compliance mapping** | SOC 2 CC7.1, CC8.1; ISO 27001 A.8.25, A.8.28; PCI DSS 6.2.2 | SOC 2 CC7.1; ISO 27001 A.8.29; PCI DSS 6.2.4, 6.3 |
| **Cost to fix findings** | Low (developer has immediate code context) | Higher (requires tracing from endpoint back to code) |

### The Key Takeaway

SAST finds vulnerabilities in code before deployment. DAST finds vulnerabilities in running applications after deployment. Neither is sufficient alone. SAST misses runtime issues. DAST misses code-level issues. A compliance-grade application security program requires both.

This is not a theoretical position. PCI DSS 4.0 Requirement 6.2 explicitly requires both code-level analysis (SAST or manual review) and runtime testing (DAST or penetration testing) for custom software. SOC 2 and ISO 27001 are less prescriptive but auditors increasingly expect evidence of both code-level and runtime security testing as part of a mature security program.

---

## IAST: Interactive Application Security Testing

Interactive Application Security Testing combines elements of both SAST and DAST by instrumenting the running application with an agent that monitors code execution in real time during testing. The IAST agent sits inside the application runtime -- as a language-level agent, a JVM agent, or middleware -- and observes how data flows through actual code paths during functional testing, QA testing, or DAST scanning.

### How IAST Works

When a request hits the application, the IAST agent tracks the input data through every function call, library invocation, and database query it touches. If a SQL query is constructed using unsanitized user input, the IAST agent sees both the endpoint that received the request (like DAST) and the specific code line that built the vulnerable query (like SAST). This dual visibility produces findings with confirmed exploitability and exact code location -- dramatically reducing false positives.

### IAST Strengths

- **Near-zero false positives.** Because IAST observes actual data flow through running code, it confirms that a vulnerability is both present in the code and reachable through a live code path. False positive rates typically fall below 5%.
- **Precise remediation guidance.** Findings include the endpoint, the code file, the line number, the data flow trace, and the exact input that triggered the vulnerability.
- **Continuous testing.** IAST runs passively during any type of testing -- manual QA, automated integration tests, DAST scans, or even production traffic monitoring. Every test interaction generates security insights.
- **No separate scan cycle.** Unlike SAST (which requires a dedicated scan step) or DAST (which requires a dedicated crawl-and-attack phase), IAST produces security results as a byproduct of normal testing activities.

### IAST Limitations

- **Requires runtime instrumentation.** The IAST agent must be deployed into the application runtime, which introduces a runtime dependency and potential performance overhead (typically 2-5% latency increase).
- **Language-specific agents.** IAST agents are available for major languages (Java, .NET, Python, Node.js, Ruby, Go) but not all. Coverage for less common languages may be limited or unavailable.
- **Coverage depends on test coverage.** IAST only analyzes code paths that are actually exercised during testing. If your functional test suite covers 60% of code paths, IAST only evaluates that 60%. Untested code paths remain unanalyzed.
- **Deployment complexity.** Integrating an IAST agent into existing application environments requires configuration, testing, and ongoing maintenance.

### When to Use IAST

IAST is most valuable for organizations with mature QA processes and comprehensive automated test suites. Deploy the IAST agent in your staging or QA environment and let it run continuously during all testing activities. The result is a stream of high-confidence, precisely located security findings with minimal false positives.

For organizations that already run DAST scans, adding IAST instrumentation to the same environment dramatically improves the quality of findings from both tools -- the DAST tool exercises endpoints while the IAST agent provides internal visibility.

---

## SCA: Software Composition Analysis

Software Composition Analysis identifies known vulnerabilities, license risks, and outdated components in the open-source and third-party dependencies your application uses. In a modern application, proprietary code typically represents only 10-30% of the total codebase. The remaining 70-90% is open-source libraries, frameworks, and transitive dependencies pulled in by your dependency manager.

### Why SCA Matters

When a critical vulnerability is disclosed in a widely used open-source library -- Log4Shell in Apache Log4j, the Spring4Shell vulnerability in Spring Framework, or the polyfill.io supply chain attack -- the organizations that respond fastest are those with an accurate, continuously updated inventory of their dependencies. SCA provides that inventory and maps it against vulnerability databases in real time.

### How SCA Works

SCA tools analyze package manifests (package.json, requirements.txt, pom.xml, go.mod, Gemfile.lock, Cargo.lock) and, in some cases, perform binary analysis to identify all direct and transitive dependencies. Each identified component is cross-referenced against vulnerability databases -- the National Vulnerability Database (NVD), GitHub Advisory Database, OSV, and vendor-specific sources -- to identify known CVEs.

Modern SCA tools also provide:

- **Software Bill of Materials (SBOM) generation** -- a machine-readable inventory of all software components, increasingly required by government contracts and enterprise procurement
- **License compliance analysis** -- identification of copyleft, restrictive, or conflicting licenses in your dependency tree
- **Reachability analysis** -- determination of whether a vulnerable function in a dependency is actually called by your code, reducing noise from vulnerabilities in unused code paths
- **Dependency health scoring** -- metrics on maintenance activity, community size, and release frequency for each dependency

### SCA and Compliance

SCA directly supports multiple compliance framework requirements:

- **SOC 2 CC7.1** requires identification of vulnerabilities in system components, including third-party software
- **ISO 27001 A.8.28** requires secure coding practices, which includes managing dependencies
- **PCI DSS 6.3.2** requires maintaining an inventory of bespoke and custom software, including third-party components
- **NIST SP 800-53 SA-11** requires software composition analysis as part of the developer security testing process
- **Executive Order 14028** (and subsequent CISA guidance) requires SBOM generation for software sold to the US federal government

For more on how vulnerability scanning fits into a broader security program, see our [Vulnerability Management Program Guide](/blog/vulnerability-management-program-guide).

---

## How Application Security Testing Maps to Compliance

Every major compliance framework requires application security testing, but the specific requirements, control identifiers, and evidence expectations differ. This section maps each testing methodology to the frameworks your auditor is evaluating.

### SOC 2 Trust Services Criteria

| SOC 2 Control | Requirement | Applicable AST Methodology | Evidence the Auditor Expects |
|---|---|---|---|
| **CC7.1** -- The entity uses detection and monitoring procedures to identify changes to configurations that result in the introduction of new vulnerabilities and susceptibilities to newly discovered vulnerabilities | Identify vulnerabilities in applications and system components | SAST, DAST, SCA, IAST | Scan results, finding reports, remediation tickets, trend dashboards |
| **CC8.1** -- The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes | Security testing as part of the change management process | SAST in CI/CD pipeline | Evidence that SAST runs on every code change; pass/fail gate configurations; scan result logs |
| **CC7.2** -- The entity monitors system components and the operation of those components for anomalies | Ongoing monitoring for security issues | DAST (periodic), SCA (continuous) | Scheduled scan evidence, continuous dependency monitoring alerts |

SOC 2 auditors do not prescribe specific tools. They evaluate whether your security testing program is designed, implemented, and operating effectively throughout the audit period. They want evidence of consistent testing, not a single point-in-time scan.

> **Related:** [The Complete SOC 2 Compliance Guide for SaaS Startups](/blog/soc2-complete-guide)

### ISO 27001:2022 Annex A Controls

| ISO 27001 Control | Requirement | Applicable AST Methodology |
|---|---|---|
| **A.8.25** -- Secure development lifecycle | Security built into the SDLC | SAST (in IDE and CI), SCA |
| **A.8.26** -- Application security requirements | Security requirements defined and tested | SAST, DAST |
| **A.8.27** -- Secure system architecture and engineering principles | Architecture reviewed for security | Manual review, threat modeling |
| **A.8.28** -- Secure coding | Code follows secure coding practices | SAST, SCA |
| **A.8.29** -- Security testing in development and acceptance | Applications tested for security before deployment | DAST, IAST, penetration testing |

ISO 27001 is controls-based: you must demonstrate that each relevant control is implemented and effective. Application security testing maps to multiple controls in the A.8 (Technological Controls) family. Auditors expect documented procedures, tool configurations, scan schedules, and evidence of finding remediation.

> **Related:** [ISO 27001 Certification: The Complete Implementation Guide](/blog/iso27001-complete-guide)

### PCI DSS 4.0

PCI DSS 4.0 is the most prescriptive framework regarding application security testing. Requirement 6 is dedicated to secure software development.

| PCI DSS Control | Requirement | Applicable AST Methodology |
|---|---|---|
| **6.2.2** -- Software development personnel working on bespoke and custom software are trained in software security relevant to their job function | Developer security training | Supports SAST adoption (training developers to interpret findings) |
| **6.2.3** -- Bespoke and custom software is reviewed prior to being released into production to identify and correct potential coding vulnerabilities | Pre-release code review or automated analysis | SAST or manual secure code review |
| **6.2.4** -- Software engineering techniques or automated methods are defined and used to prevent or mitigate common software attacks | Runtime security testing | DAST, WAF, IAST |
| **6.3.1** -- Security vulnerabilities are identified and managed | Vulnerability identification in applications | SAST, DAST, SCA |
| **6.3.2** -- An inventory of bespoke and custom software, and third-party software components incorporated into bespoke and custom software, is maintained | Software inventory and dependency tracking | SCA (SBOM generation) |

PCI DSS explicitly distinguishes between code-level review (6.2.3, addressed by SAST) and runtime testing (6.2.4, addressed by DAST). Organizations in PCI scope must demonstrate both capabilities. For a complete walkthrough of PCI DSS requirements, see our [PCI DSS Compliance Guide](/blog/pci-dss-complete-guide).

### NIST SP 800-53 (SA-11: Developer Testing and Evaluation)

NIST SP 800-53 control SA-11 requires organizations to:

- Require the developer of the system, system component, or system service to create and implement a security assessment plan
- Perform unit, integration, system, and regression testing and evaluation at a depth and coverage defined by the organization
- Produce evidence of the execution of the security assessment plan and the results of the security testing and evaluation

SA-11 enhancements explicitly reference static analysis (SA-11(1)), dynamic analysis (SA-11(8)), and software composition analysis. Federal agencies and government contractors are expected to implement all three.

> **Related:** [NIST 800-53 Controls: A Practical Implementation Guide](/blog/nist-800-53-controls-guide)

---

## Building a Complete AppSec Testing Program

A compliance-ready application security testing program layers multiple testing methodologies across the software development lifecycle. Each layer catches different vulnerability classes at different stages, and together they create defense in depth that satisfies auditor expectations across frameworks.

Here is the recommended layered approach, ordered from earliest (cheapest to fix) to latest (most expensive to fix):

### Layer 1: SAST in the IDE (Real-Time)

**What it does:** Provides immediate security feedback to developers as they write code.

**Implementation:**
- Deploy IDE plugins (Semgrep, SonarLint, Snyk Code) to all developer workstations
- Configure rulesets to match your organization's coding standards and framework requirements
- Focus on high-severity, low-false-positive rules to maintain developer trust

**Compliance value:** Evidence that security is embedded in the earliest stage of development (ISO 27001 A.8.25, A.8.28). Demonstrates a "shift left" approach that auditors view favorably.

### Layer 2: SAST in CI/CD (Pre-Merge Gate)

**What it does:** Runs automated static analysis on every pull request before code is merged to the main branch.

**Implementation:**
- Configure SAST as a required status check in your branch protection rules
- Define severity thresholds: block merge on Critical and High findings; warn on Medium
- Store scan results as build artifacts for audit evidence
- Auto-create tickets for findings that require remediation

**Compliance value:** Direct evidence for SOC 2 CC7.1 and CC8.1, ISO 27001 A.8.25 and A.8.28, PCI DSS 6.2.3. Auditors can verify that every merged change passed static analysis.

### Layer 3: SCA Everywhere (Continuous)

**What it does:** Continuously monitors all dependencies for known vulnerabilities and license risks.

**Implementation:**
- Integrate SCA into the CI pipeline to scan on every build
- Enable continuous monitoring to receive alerts when new CVEs are disclosed against existing dependencies
- Generate and maintain an SBOM for each application
- Define policies for maximum vulnerability age by severity (e.g., Critical must be patched within 48 hours)

**Compliance value:** Addresses SOC 2 CC7.1 (vulnerability identification in third-party components), PCI DSS 6.3.2 (software inventory), ISO 27001 A.8.28 (secure coding including dependencies). SBOM generation supports federal compliance requirements.

### Layer 4: DAST in Staging (Pre-Production)

**What it does:** Tests the deployed application for runtime vulnerabilities, configuration issues, and security header compliance before production release.

**Implementation:**
- Deploy a staging environment that mirrors production configuration
- Run DAST scans after each staging deployment (lightweight) and weekly (comprehensive)
- Configure authenticated scanning with test accounts for each user role
- Define blocking thresholds: Critical and High findings block production promotion

**Compliance value:** Direct evidence for ISO 27001 A.8.29 (security testing in development and acceptance), SOC 2 CC7.1, PCI DSS 6.2.4. Demonstrates that runtime security validation occurs before every production release.

### Layer 5: Penetration Testing (Periodic Validation)

**What it does:** Qualified security professionals manually test the application to find complex vulnerabilities that automated tools miss -- business logic flaws, chained exploits, and novel attack paths.

**Implementation:**
- Conduct annual penetration tests at minimum; quarterly for high-risk applications
- Scope tests to cover web applications, APIs, and infrastructure
- Require retesting after major architecture changes
- Track remediation of all critical and high findings to closure

**Compliance value:** Required by PCI DSS (annually), expected by SOC 2 and ISO 27001. Validates that your automated testing program is effective against skilled human attackers. See our [Penetration Testing Guide](/glossary/penetration-testing) for detailed requirements.

---

## Integrating Security Testing into CI/CD Pipelines

The practical value of application security testing depends entirely on integration. Tools that run outside the development workflow -- manually triggered, run on a separate schedule, or producing reports that sit in a shared drive -- generate friction, delay remediation, and fail to produce the continuous evidence stream auditors expect.

Here is a practical pipeline architecture that integrates SAST, SCA, and DAST into a standard CI/CD workflow.

### Pipeline Stage 1: Pre-Commit (Developer Machine)

```
Developer writes code
  -> IDE SAST plugin flags issues in real time
  -> Pre-commit hook runs secrets scanner (gitleaks, trufflehog)
  -> Developer fixes before committing
```

**Tools:** Semgrep (IDE extension), SonarLint, gitleaks (pre-commit hook)

**Evidence generated:** Local scan logs (optional; not required for compliance but supports developer training metrics)

### Pipeline Stage 2: Pull Request (CI Pipeline)

```
Pull request opened
  -> SAST scan (full analysis of changed files + dependency scope)
  -> SCA scan (dependency manifest analysis)
  -> Secrets scan (codebase-wide)
  -> Unit tests with security test cases
  -> Results posted as PR comments / status checks
  -> Critical/High findings BLOCK merge
```

**Tools:** Semgrep CI, CodeQL, Snyk Code (SAST); Snyk Open Source, Dependabot, Trivy (SCA); gitleaks, trufflehog (secrets)

**Evidence generated:** Scan result artifacts attached to each pull request; pass/fail status check logs; finding-to-ticket mapping

### Pipeline Stage 3: Build and Deploy to Staging

```
Code merged to main
  -> Build and containerize
  -> Container image scan (Trivy, Grype)
  -> Deploy to staging environment
  -> Run smoke tests to verify deployment
```

**Tools:** Trivy, Grype (container scanning); ArgoCD, Flux, or CI-native deployment

**Evidence generated:** Container scan reports; deployment logs with timestamps

### Pipeline Stage 4: DAST in Staging

```
Staging deployment verified
  -> DAST scan (authenticated, against staging URL)
  -> API security scan (against staging API)
  -> Results pushed to security dashboard
  -> Critical findings trigger alerts and block production promotion
```

**Tools:** OWASP ZAP, Nuclei, Burp Suite Enterprise, StackHawk

**Evidence generated:** DAST scan reports with timestamps, endpoint coverage metrics, finding severity distributions

### Pipeline Stage 5: Production Promotion

```
All scans pass
  -> Approval gate (manual or automated based on risk level)
  -> Deploy to production
  -> Post-deployment verification
  -> Lightweight DAST smoke test against production
```

**Evidence generated:** Approval records, deployment logs, post-deployment scan results

This pipeline architecture produces a complete audit trail for every code change: who wrote it, who reviewed it, what security scans it passed, what vulnerabilities were identified, and how they were resolved. For a detailed guide on building compliance-ready CI/CD pipelines, see our [DevSecOps for Compliance Guide](/blog/devsecops-compliance-cicd-guide).

---

## Application Security Testing Tools

Choosing the right tools depends on your technology stack, team size, budget, and compliance requirements. The following recommendations cover both commercial and open-source options for each testing category.

### SAST Tools

| Tool | Type | Languages | Best For |
|---|---|---|---|
| **Semgrep** | Open-source (with commercial tier) | 30+ languages | Fast, low-false-positive scanning; custom rule authoring; CI integration |
| **CodeQL** | Free (GitHub-hosted) | Java, JavaScript/TypeScript, Python, C/C++, C#, Go, Ruby, Swift | Deep semantic analysis; GitHub-native integration |
| **SonarQube** | Open-source (Community) / Commercial | 30+ languages | Combined code quality + security analysis; broad language support |
| **Checkmarx SAST** | Commercial | 25+ languages | Enterprise-grade; compliance reporting; deep taint analysis |
| **Snyk Code** | Commercial | 10+ languages | Developer-friendly; real-time IDE integration; AI-powered fixes |
| **Fortify (OpenText)** | Commercial | 25+ languages | Large enterprise; extensive rule library; regulatory compliance focus |

**Recommendation for startups and mid-market:** Start with Semgrep (open-source rules plus custom policies) and CodeQL (free on GitHub). These cover the majority of vulnerability patterns at zero cost and integrate directly into GitHub Actions workflows.

### DAST Tools

| Tool | Type | Best For |
|---|---|---|
| **OWASP ZAP** | Free / Open-source | Budget-conscious teams; CI pipeline integration; API scanning |
| **Nuclei** | Free / Open-source | Template-based scanning; fast; community-maintained vulnerability templates |
| **Burp Suite Enterprise** | Commercial | Comprehensive web app scanning; enterprise reporting; CI integration |
| **StackHawk** | Commercial | Developer-first DAST; native CI/CD integration; API-first design |
| **Invicti (formerly Netsparker)** | Commercial | Proof-based scanning (confirmed vulnerabilities); low false positives |
| **Qualys WAS** | Commercial | Enterprise-scale; integration with broader Qualys vulnerability management |

**Recommendation:** OWASP ZAP for initial implementation (free, well-documented, CI-friendly). Upgrade to Burp Suite Enterprise or StackHawk as your program matures and you need better CI integration, API scanning depth, or enterprise reporting.

### SCA Tools

| Tool | Type | Best For |
|---|---|---|
| **Snyk Open Source** | Free tier / Commercial | Developer-friendly; automated fix PRs; broad ecosystem support |
| **Dependabot** | Free (GitHub-native) | GitHub-native dependency updates; zero configuration |
| **Trivy** | Free / Open-source | Multi-scanner (SCA + container + IaC); single-tool consolidation |
| **Grype** | Free / Open-source | Fast, standalone vulnerability scanner for container images and filesystems |
| **OWASP Dependency-Check** | Free / Open-source | Mature; OWASP-backed; supports Java, .NET, Python, Ruby, Node.js |
| **Mend (formerly WhiteSource)** | Commercial | Enterprise SCA; license compliance; policy enforcement |

**Recommendation:** Trivy for comprehensive coverage (SCA + container scanning + IaC scanning in one tool). Supplement with Dependabot for automated dependency update PRs on GitHub.

### IAST Tools

| Tool | Type | Supported Runtimes |
|---|---|---|
| **Contrast Security** | Commercial | Java, .NET, Node.js, Python, Ruby, Go |
| **Synopsys Seeker** | Commercial | Java, .NET, Node.js, Python, Ruby, Scala |
| **Hdiv (now Datadog Application Security)** | Commercial | Java, .NET |
| **OpenRASP** | Open-source | Java, PHP |

**Recommendation:** IAST is most valuable for organizations with mature QA processes. If you are early in your AppSec journey, prioritize SAST + DAST + SCA first and add IAST when your testing infrastructure can support agent-based instrumentation.

---

## AppSec Metrics: What to Measure and Report

Metrics transform application security testing from an operational activity into a manageable program. They demonstrate program effectiveness to auditors, justify tooling investments to leadership, and identify areas that need improvement.

### Core Metrics

**Finding Density**
The number of security findings per thousand lines of code (findings/KLOC), segmented by severity. Tracking this metric over time shows whether your codebase is getting more or less secure.

- **Benchmark:** Mature programs target fewer than 1 Critical/High finding per 10 KLOC
- **Auditor value:** Trend data demonstrating decreasing finding density provides strong evidence of program effectiveness

**Mean Time to Remediate (MTTR)**
The average time between finding discovery and verified remediation, segmented by severity level and finding source (SAST, DAST, SCA).

- **Target SLAs:** Critical: 48 hours; High: 7 days; Medium: 30 days; Low: 90 days
- **Auditor value:** MTTR aligned with documented SLAs demonstrates operational discipline; MTTR decreasing over time demonstrates program improvement

**Scan Coverage**
The percentage of applications, repositories, and deployment environments covered by each testing methodology.

- **Target:** 100% of production applications covered by SAST and SCA; 100% of externally accessible applications covered by DAST
- **Auditor value:** Coverage gaps are control gaps. Auditors will ask about applications not covered by scanning.

**False Positive Rate**
The percentage of findings that are triaged as false positives, segmented by tool and finding category.

- **Benchmark:** SAST: below 40%; DAST: below 20%; IAST: below 5%; SCA: below 10%
- **Operational value:** High false positive rates indicate tool misconfiguration or overly broad rulesets, and they erode developer trust

**SLA Compliance Rate**
The percentage of findings remediated within their severity-based SLA deadline.

- **Target:** Above 90% for Critical and High; above 80% for Medium
- **Auditor value:** Demonstrates that findings are not just identified but actually resolved in a timely manner

### Reporting Cadence

- **Weekly:** Operational dashboard for engineering and security teams (new findings, open findings by severity, SLA breaches)
- **Monthly:** Program summary for security leadership (MTTR trends, scan coverage, finding density trends, tool effectiveness)
- **Quarterly:** Executive report for leadership and board (program maturity, risk posture trends, compliance readiness, investment recommendations)
- **Audit period:** Comprehensive evidence package (all scan results, remediation records, SLA compliance data, exception documentation)

---

## Frequently Asked Questions

### What is the difference between SAST and DAST?

SAST (Static Application Security Testing) analyzes source code without running the application, finding code-level vulnerabilities like injection patterns, hardcoded secrets, and insecure cryptography. DAST (Dynamic Application Security Testing) tests a running application from the outside, finding runtime vulnerabilities like misconfigurations, missing security headers, and authentication bypasses. SAST works on code; DAST works on deployed applications. Both are required for comprehensive application security.

### Can SAST replace DAST, or vice versa?

No. SAST and DAST find fundamentally different categories of vulnerabilities. SAST cannot detect server misconfigurations, missing HTTP headers, or broken authentication in a deployed environment. DAST cannot find hardcoded secrets, insecure cryptographic implementations, or vulnerabilities in code paths that are not reachable through the application's external interface. Compliance frameworks -- especially PCI DSS 4.0 -- explicitly require both code-level analysis and runtime testing.

### Which should I implement first: SAST or DAST?

Start with SAST. It integrates directly into your existing development workflow (IDE and CI pipeline), provides immediate feedback to developers, and catches vulnerabilities at the cheapest point to fix them. Once SAST is operational, add SCA for dependency scanning, then implement DAST for runtime testing. This order maximizes value per unit of implementation effort.

### How does application security testing map to SOC 2 requirements?

SOC 2 Trust Services Criteria CC7.1 requires the identification of vulnerabilities in system components, which directly maps to SAST, DAST, and SCA. CC8.1 requires that changes are tested before deployment, which maps to SAST in the CI/CD pipeline. SOC 2 does not prescribe specific tools, but auditors expect evidence of systematic, continuous security testing with documented findings and remediation tracking.

### Is IAST better than SAST and DAST combined?

IAST provides unique advantages -- near-zero false positives and combined code-and-runtime visibility -- but it does not replace SAST or DAST entirely. IAST only analyzes code paths exercised during testing, so untested paths remain unanalyzed (a gap SAST fills). IAST requires the application to be running and instrumented, so it cannot provide the shift-left IDE feedback that SAST delivers. IAST is best used as a complement to SAST and DAST, not a replacement.

### What open-source tools can I use for application security testing?

For SAST: Semgrep (custom rules and community rulesets) and CodeQL (GitHub-native, deep semantic analysis). For DAST: OWASP ZAP (full-featured web application scanner) and Nuclei (template-based scanner). For SCA: Trivy (multi-purpose scanner), Grype (container and filesystem scanning), and OWASP Dependency-Check. For secrets scanning: gitleaks and trufflehog. These tools cover the majority of testing needs at zero license cost.

### How often should I run SAST and DAST scans for compliance?

SAST should run on every pull request (continuous) as part of your CI pipeline. DAST should run against staging after every deployment (lightweight scan) with a comprehensive scan at least weekly. SCA should run on every build and continuously monitor for newly disclosed vulnerabilities. Penetration testing should occur at least annually. This cadence satisfies SOC 2, ISO 27001, and PCI DSS requirements and produces the continuous evidence stream auditors expect.

### How do I reduce false positives in SAST and DAST?

For SAST: tune rulesets to your technology stack and coding patterns; suppress known false positives with inline annotations; start with high-confidence rules and expand gradually; use tools with data flow analysis rather than pure pattern matching. For DAST: use authenticated scanning to reduce noise from access-denied responses; configure scan policies to match your application's technology profile; exclude known-safe endpoints from active testing. For both: track your false positive rate as a metric and invest time in tuning -- a high false positive rate undermines developer trust and program effectiveness.

---

## Build an Audit-Ready AppSec Program Without the Manual Work

Building a layered application security testing program is the right engineering decision. But maintaining the compliance evidence that program generates -- scan results mapped to framework controls, remediation SLAs tracked across tools, trend reports prepared for auditor review -- is where the operational burden compounds.

**QuickTrust automates the compliance layer of your application security program.** The platform integrates with your existing SAST, DAST, SCA, and CI/CD tools, automatically maps security testing evidence to SOC 2, ISO 27001, PCI DSS, and NIST 800-53 controls, tracks remediation timelines against your defined SLAs, and generates audit-ready evidence packages on demand. Your engineering team focuses on building secure software. QuickTrust ensures the evidence is collected, organized, and ready when the auditor asks for it.

[Start your free QuickTrust assessment](https://trust.quickintell.com) and see how your current application security testing practices map to the compliance frameworks you are pursuing.

---

*Related reading:*

- *[DevSecOps for Compliance: How to Build a CI/CD Pipeline That Passes SOC 2 and ISO 27001 Audits](/blog/devsecops-compliance-cicd-guide)*
- *[How to Build a Vulnerability Management Program That Passes Compliance Audits](/blog/vulnerability-management-program-guide)*
- *[The Change Management Process That Passes SOC 2, ISO 27001, and PCI DSS Audits](/blog/change-management-process-compliance)*
- *[What Is Penetration Testing? How Pen Tests Fit Into Compliance](/glossary/penetration-testing)*
- *[PCI DSS Compliance: The Complete Guide](/blog/pci-dss-complete-guide)*
- *[The Complete SOC 2 Compliance Guide for SaaS Startups](/blog/soc2-complete-guide)*
