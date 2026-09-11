---
meta_description: "Build a CI/CD pipeline that passes SOC 2 and ISO 27001 audits. SAST, DAST, secret scanning, change management, and evidence collection for DevSecOps."
target_keyword: "DevSecOps compliance"
secondary_keywords: "CI/CD SOC 2, DevSecOps audit, SAST DAST compliance, change management CI/CD, ISO 27001 DevOps, secure CI/CD pipeline"
word_count_target: "2000"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# DevSecOps for Compliance: How to Build a CI/CD Pipeline That Passes SOC 2 and ISO 27001 Audits

Your CI/CD pipeline is not just a deployment tool. To an auditor, it is the primary evidence of how your organization manages changes to production systems. Every commit, every pull request, every deployment, and every test result tells a story about your change management controls, your code quality practices, and your security posture.

Most engineering teams build CI/CD pipelines optimized for speed and developer experience. Then, when an audit approaches, they discover that their pipeline does not produce the evidence auditors need, does not enforce the controls frameworks require, and does not document the approvals regulators expect.

The fix is not to slow down your pipeline. It is to design security and compliance controls into the pipeline from the start -- so that the same process that ships code fast also produces a continuous stream of audit-ready evidence. That is what DevSecOps for compliance looks like in practice.

This guide covers the specific controls SOC 2 and ISO 27001 auditors look for in your CI/CD pipeline, the tools that implement them, and how to set it all up without grinding your engineering velocity to a halt.

## What Auditors Actually Look For in Your CI/CD Pipeline

Auditors are not CI/CD experts. They are not going to review your GitHub Actions workflow files line by line. What they will do is ask questions that map to specific control requirements, and they will expect you to produce evidence that those controls are enforced consistently.

Here is what they care about, mapped to the frameworks:

### SOC 2 (Trust Services Criteria)

**CC8.1 -- Changes to Infrastructure and Software.** The organization authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures to meet its objectives.

In practice, this means: every change to production must be authorized (approved by someone other than the author), tested (automated tests pass), and documented (there is a record of what changed, who approved it, and when it was deployed).

**CC7.1 -- Detection and Monitoring.** The organization detects and monitors for security events. Your pipeline should include security scanning (SAST, DAST, dependency scanning) that detects vulnerabilities before they reach production.

**CC6.1 -- Logical Access.** Controls over who can access what. In the CI/CD context, this means controlling who can merge to protected branches, who can trigger production deployments, and who can modify pipeline configurations.

### ISO 27001 (Annex A Controls)

**A.8.25 -- Secure Development Life Cycle.** Rules for the secure development of software and systems shall be established and applied. This maps directly to your SDLC practices: code review, testing, security scanning, and change management.

**A.8.26 -- Application Security Requirements.** Information security requirements shall be identified, specified, and approved when developing or acquiring applications.

**A.8.27 -- Secure System Architecture and Engineering Principles.** Principles for engineering secure systems shall be established, documented, maintained, and applied to any information system development activity.

**A.8.28 -- Secure Coding.** Secure coding principles shall be applied to software development. Auditors will look for evidence of SAST, code review practices, and coding standards enforcement.

**A.8.32 -- Change Management.** Changes to information processing facilities and information systems shall be subject to change management procedures.

## The Six Pillars of a Compliant CI/CD Pipeline

### 1. Branch Protection and Code Review

Branch protection is the foundation of change management in a Git-based workflow. At minimum, your production branch (main/master) should enforce:

- **Required pull request reviews.** At least one reviewer who is not the author must approve every change before it can be merged. This satisfies the "authorized by someone other than the developer" requirement in CC8.1.
- **Required status checks.** Automated tests and security scans must pass before a merge is allowed. This ensures that no untested code reaches production.
- **No direct pushes.** Nobody -- not even administrators -- should be able to push directly to the production branch. All changes flow through the pull request process.
- **Signed commits** (recommended but not always required). Cryptographic commit signing provides non-repudiation -- proof that the person who authored the commit is who they claim to be.

**Evidence to collect:** Branch protection rule configurations (screenshots or API exports from GitHub/GitLab), pull request history showing reviewer approvals, and audit logs showing that protection rules have not been modified or bypassed.

**Implementation in GitHub:**

```yaml
# GitHub branch protection settings (configured via UI or API)
# Required for 'main' branch:
#   - Require pull request reviews: 1 minimum
#   - Dismiss stale pull request approvals when new commits are pushed
#   - Require status checks to pass before merging
#   - Require branches to be up to date before merging
#   - Include administrators in restrictions
```

### 2. SAST (Static Application Security Testing)

SAST tools analyze your source code for security vulnerabilities without executing it. They catch issues like SQL injection, cross-site scripting, insecure deserialization, and hardcoded credentials before code is merged.

**What auditors expect:** Evidence that SAST runs on every pull request, that findings are reviewed, and that critical/high findings are remediated before deployment.

**Tools by language ecosystem:**

| Tool | Languages | Integration |
|---|---|---|
| Semgrep | Python, JavaScript, Go, Java, Ruby, and more | GitHub Actions, GitLab CI, CLI |
| SonarQube / SonarCloud | 30+ languages | GitHub Actions, GitLab CI, Jenkins |
| CodeQL (GitHub) | C/C++, C#, Go, Java, JavaScript, Python, Ruby | Native GitHub Actions |
| Bandit | Python | GitHub Actions, GitLab CI, CLI |
| Brakeman | Ruby on Rails | GitHub Actions, GitLab CI, CLI |

**Example GitHub Actions integration:**

```yaml
name: SAST Scan
on:
  pull_request:
    branches: [main]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/default
            p/owasp-top-ten
            p/security-audit
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
```

The SARIF upload is important for compliance -- it creates a persistent, auditable record of scan results within your repository's security tab.

### 3. DAST (Dynamic Application Security Testing)

DAST tools test your running application for vulnerabilities by simulating attacks against it. While SAST catches code-level issues, DAST catches runtime vulnerabilities like misconfigured headers, authentication bypasses, and server-side request forgery.

**What auditors expect:** Evidence that DAST scans run regularly (at minimum before major releases, ideally in CI/CD on staging environments), and that findings are tracked and remediated.

**Common tools:** OWASP ZAP (open source), Burp Suite, Nuclei, Dastardly (by PortSwigger).

DAST is typically run against a staging environment rather than in the PR pipeline, since it requires a running application. A common pattern is to trigger a DAST scan after deploying to staging and gate the production deployment on DAST results.

### 4. Secret Scanning

Hardcoded secrets -- API keys, database passwords, private keys, tokens -- in source code are one of the most common and most damaging security issues. A single committed AWS key can lead to a full infrastructure compromise within minutes.

**What auditors expect:** Evidence that secret scanning is active, that it runs on every commit (not just PRs), and that detected secrets are rotated and remediated.

**Tools:**

| Tool | Approach | Integration |
|---|---|---|
| GitHub Secret Scanning | Native GitHub feature | Automatic for public repos; available for private repos with Advanced Security |
| GitLeaks | Open source, regex-based | GitHub Actions, GitLab CI, pre-commit hook |
| TruffleHog | Open source, entropy + regex | GitHub Actions, GitLab CI, CLI |
| detect-secrets (Yelp) | Open source, plugin-based | Pre-commit hook, CI/CD |

**Best practice:** Run secret scanning as both a pre-commit hook (to prevent secrets from ever being committed) and in CI/CD (to catch secrets that bypass the hook). This defense-in-depth approach satisfies auditors who want to see preventive and detective controls.

```yaml
name: Secret Scanning
on: [push, pull_request]

jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 5. Dependency Scanning and Software Composition Analysis

Modern applications are built on hundreds of open-source dependencies, each of which can introduce vulnerabilities. SCA (Software Composition Analysis) tools scan your dependency tree for known CVEs.

**What auditors expect:** Evidence that dependency scanning runs in CI/CD, that vulnerable dependencies are identified and tracked, and that critical vulnerabilities are remediated within defined SLAs (e.g., critical within 7 days, high within 30 days).

**Tools:** Dependabot (GitHub native), Snyk, Renovate, OWASP Dependency-Check, Trivy (also handles container scanning).

This is one of the easiest controls to implement and one of the first auditors check. If you are not scanning dependencies, start here.

### 6. Environment Separation and Deployment Controls

Auditors want to see clear separation between development, staging, and production environments, with increasing controls as code moves toward production.

**What auditors expect:**

- **Environment separation.** Development, staging, and production environments are isolated. Developers cannot access production data from development environments. Infrastructure configurations enforce this separation.
- **Deployment approvals.** Production deployments require explicit approval from an authorized person. This can be a manual approval gate in your pipeline, a deployment review in GitHub Environments, or a change advisory board (CAB) process.
- **Deployment audit trail.** Every production deployment is logged with who initiated it, who approved it, what was deployed (commit SHA), and when it occurred.
- **Rollback capability.** The ability to quickly revert a production deployment if issues are detected. This satisfies availability and processing integrity requirements.

**GitHub Environments configuration:**

```yaml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - name: Deploy to production
        run: ./deploy.sh
```

When you configure the `production` environment in GitHub with required reviewers, every deployment to production will pause and wait for manual approval before proceeding. The approval is logged with the approver's identity and timestamp -- exactly the evidence auditors need.

## Evidence Collection: Making Your Pipeline Audit-Ready

The controls described above are only valuable if you can prove they exist and operate consistently. Here is how to collect evidence from your CI/CD pipeline:

### Key Evidence Sources

Your pipeline produces evidence from pull request history (code review approvals), branch protection audit logs (rules are active), CI/CD run logs (tests and scans execute on every change), SAST/DAST scan results in SARIF format (vulnerabilities tracked), secret scanning alerts (secrets detected before deployment), dependency scan results (vulnerable libraries identified), and deployment logs (production changes authorized and recorded).

### Evidence Collection Automation

Do not wait until audit time to collect evidence. Build evidence collection into your pipeline:

- **Export CI/CD run summaries** to a centralized evidence repository on a weekly or monthly basis.
- **Generate compliance reports** from your security scanning tools that show trends, remediation times, and current vulnerability counts.
- **Maintain a change log** that correlates every production deployment to its pull request, approvers, test results, and scan outcomes.

For SOC 2 Type II specifically, auditors need evidence that controls operated effectively over the entire observation period (typically 3-12 months), not just at a single point in time. Continuous evidence collection is essential.

## Putting It All Together: A Complete Pipeline

Here is what a compliant CI/CD pipeline looks like end to end:

1. **Developer creates a feature branch** and writes code.
2. **Pre-commit hooks** run secret scanning and basic linting locally.
3. **Developer opens a pull request** against the main branch.
4. **CI/CD pipeline triggers automatically** and runs:
   - Unit and integration tests
   - SAST scan (Semgrep, CodeQL, or SonarQube)
   - Dependency scan (Dependabot, Snyk, or Trivy)
   - Secret scan (Gitleaks or TruffleHog)
   - Container image scan (if applicable)
5. **All status checks must pass** before the PR can be merged (enforced by branch protection).
6. **At least one reviewer** (not the author) reviews and approves the PR.
7. **PR is merged** to main. The merge is logged with the author, reviewer, and timestamp.
8. **Staging deployment** triggers automatically. DAST scan runs against staging.
9. **Production deployment** requires manual approval through GitHub Environments or equivalent.
10. **Authorized reviewer approves** the production deployment. Deployment proceeds.
11. **Post-deployment monitoring** verifies the deployment is healthy.
12. **All artifacts** (test results, scan results, approvals, deployment logs) are archived for audit evidence.

Every step in this pipeline produces evidence. Every control is enforced automatically. The developer experience remains fast -- the security and compliance controls run in parallel with functional tests and add minimal overhead to the deployment cycle.

## How QuickTrust Engineers Implement These Controls

QuickTrust's approach to DevSecOps compliance is hands-on. Our Security and DevOps engineers work directly in your cloud environment and CI/CD platform to implement these controls. Here is what a typical engagement looks like:

**Assessment (Days 1-3).** Engineers review your current CI/CD pipeline, identify gaps against SOC 2 and ISO 27001 requirements, and produce a prioritized implementation plan.

**Branch protection and access controls (Days 4-5).** Configure branch protection rules, repository access controls, and environment-level permissions. Implement the principle of least privilege across your development infrastructure.

**Security scanning integration (Days 6-10).** Integrate SAST, DAST, dependency scanning, and secret scanning into your pipeline. Configure alert routing, severity thresholds, and blocking rules. Set up SARIF reporting for centralized vulnerability tracking.

**Deployment controls (Days 11-14).** Configure environment separation, deployment approval gates, and deployment audit logging. Implement rollback procedures and document the deployment process.

**Evidence collection automation (Days 15-18).** Build automated evidence collection that continuously exports compliance-relevant artifacts to your evidence repository. Configure dashboards and reports for ongoing monitoring.

**Documentation and training (Days 19-21).** Document all implemented controls, create runbooks for common operations, and train your team on the new processes.

The entire implementation typically takes 3 weeks. Your engineering team's involvement is limited to approximately 2 hours per week for context and approvals. At the end, you have a CI/CD pipeline that ships code fast and produces a continuous stream of audit-ready evidence.

## The Bottom Line

DevSecOps for compliance is not about adding friction to your development process. It is about designing your development process so that security and compliance are byproducts of the normal workflow. Every pull request is a change management record. Every CI/CD run is a security scan. Every deployment is an auditable event.

The engineering teams that embrace this approach find that compliance audits become straightforward evidence collection exercises rather than frantic scrambles. The controls are already in place. The evidence is already collected. The auditor reviews the artifacts, confirms the controls operate effectively, and the audit passes.

QuickTrust's engineers have implemented these controls for over 100 companies with a 100% audit pass rate. If your CI/CD pipeline is not yet audit-ready, [schedule a 20-minute readiness call](https://trust.quickintell.com) and our team will assess your current pipeline and outline the path to compliance-ready DevSecOps.
