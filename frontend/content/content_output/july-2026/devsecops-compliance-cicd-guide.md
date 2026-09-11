---
meta_description: "Build a CI/CD pipeline that satisfies SOC 2 CC8 change management and ISO 27001 Annex A requirements."
target_keyword: "devsecops compliance, ci/cd compliance, secure sdlc"
secondary_keywords: "soc 2 ci/cd requirements, devops security, change management compliance"
word_count_target: "3000"
publish_date: "July 2026"
last_updated: "2026-02-28"
---

# DevSecOps for Compliance: How to Build a CI/CD Pipeline That Passes SOC 2 and ISO 27001 Audits

Most engineering teams treat compliance as a documentation exercise. They write a change management policy, file it in a shared drive, and then continue deploying the way they always have — merging to main, running a build, shipping to production. When the auditor arrives, someone scrambles to reconstruct evidence from Git logs, Slack messages, and memory.

This approach fails. SOC 2 Trust Services Criteria CC8.1 (Change Management) and ISO 27001 Annex A controls A.8.25 through A.8.33 require documented, repeatable, and verifiable controls over how code moves from a developer's machine to production. An auditor does not want a policy document that says "we do code reviews." An auditor wants timestamped proof that every production change went through a defined approval workflow, passed automated security checks, and was logged in an immutable audit trail.

The good news: if you build your CI/CD pipeline correctly, compliance evidence generates itself. Every pull request, every scan result, every approval, every deployment becomes an audit artifact — produced automatically, stored permanently, and queryable on demand. This guide maps specific CI/CD pipeline stages to SOC 2 CC8 and ISO 27001 Annex A controls, with concrete tool configurations, code examples, and implementation patterns for GitHub Actions, GitLab CI, and ArgoCD.

---

## The Control Mapping: CI/CD Stages to Audit Requirements

Before building anything, understand exactly which audit controls map to which pipeline stages. This table is the foundation for every design decision that follows.

| CI/CD Pipeline Stage | SOC 2 TSC Control | ISO 27001 Annex A Control | What the Auditor Expects |
|---|---|---|---|
| Branch protection / PR requirements | CC8.1 (Changes are authorized) | A.8.25 (Secure development lifecycle) | Evidence that changes require approval before merge |
| Code review and approval workflows | CC8.1 (Authorized changes), CC6.1 (Logical access) | A.8.4 (Access to source code), A.8.25 | Timestamped review approvals from authorized personnel |
| SAST (Static Application Security Testing) | CC7.1 (Identify vulnerabilities), CC8.1 | A.8.25, A.8.28 (Secure coding) | Scan results with pass/fail criteria; evidence that failures block deployment |
| SCA (Software Composition Analysis) | CC7.1, CC8.1 | A.8.28, A.8.25 | Dependency vulnerability reports; SBOM generation |
| Secrets scanning | CC6.1 (Logical access controls), CC6.7 | A.8.4, A.8.11 (Data masking) | Evidence that secrets cannot enter the codebase |
| IaC scanning | CC8.1, CC7.1 | A.8.25, A.8.9 (Configuration management) | Terraform/CloudFormation scans proving infrastructure changes are validated |
| Container image scanning | CC7.1 (Vulnerability identification) | A.8.25, A.8.28 | CVE scan results for every container image deployed to production |
| DAST (Dynamic Application Security Testing) | CC7.1 | A.8.25, A.8.29 (Security testing in dev/acceptance) | Evidence that running applications are tested for runtime vulnerabilities |
| Approval gates before production | CC8.1 (Changes are authorized) | A.8.25, A.8.31 (Separation of dev/test/prod) | Manual or automated approval records before production deployment |
| Immutable deployment logging | CC8.1, CC7.2 (Monitor for anomalies) | A.8.15 (Logging), A.8.25 | Tamper-proof records of what was deployed, when, by whom |
| Rollback capability | CC8.1 (Changes can be reversed) | A.8.25, A.8.32 (Change management) | Evidence that failed deployments can be and have been rolled back |
| Environment separation | CC8.1 | A.8.31 (Separation of dev/test/prod) | Distinct environments with independent access controls |

This is not a "nice-to-have" checklist. Every row represents a control point that a SOC 2 Type II auditor or an ISO 27001 certification body will evaluate. If you cannot produce evidence for a given row, you have a control gap.

---

## Stage 1: Branch Protection and Access Controls

The pipeline starts before any code is written. Branch protection rules are the first control an auditor evaluates because they enforce the principle that no single individual can push unreviewed code to production.

### What the Frameworks Require

**SOC 2 CC8.1** requires that changes to infrastructure and software are authorized through a defined process. A developer pushing directly to `main` and triggering a production deployment is, by definition, an unauthorized change — even if the developer is the CTO.

**ISO 27001 A.8.4** requires restricted access to source code. A.8.25 requires a secure development lifecycle that includes defined rules for code changes.

### GitHub Implementation

```yaml
# .github/settings.yml (using probot/settings or GitHub API)
# Alternatively, configure via Settings > Branches > Branch protection rules

branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
        require_last_push_approval: true
      required_status_checks:
        strict: true
        contexts:
          - "sast-scan"
          - "sca-scan"
          - "secrets-scan"
          - "iac-scan"
          - "unit-tests"
      enforce_admins: true
      required_linear_history: true
      allow_force_pushes: false
      allow_deletions: false
      required_conversation_resolution: true
```

The critical settings for audit purposes:

- **`enforce_admins: true`** means even repository administrators cannot bypass protection rules. Without this, an auditor will flag that privileged users can circumvent change management.
- **`dismiss_stale_reviews: true`** ensures that if a developer pushes new commits after receiving approval, the approval resets and a new review is required.
- **`require_last_push_approval: true`** prevents a developer from approving their own final push.
- **`required_status_checks.strict: true`** requires the branch to be up to date with `main` before merging — preventing a class of issues where checks passed on a stale branch but fail on the merged result.

### GitLab Implementation

```yaml
# Configure via Settings > Repository > Protected Branches
# Or via GitLab API:

# POST /api/v4/projects/:id/protected_branches
{
  "name": "main",
  "push_access_level": 0,
  "merge_access_level": 40,
  "allow_force_push": false,
  "code_owner_approval_required": true
}

# Approval rules via Settings > Merge Requests
# POST /api/v4/projects/:id/approval_rules
{
  "name": "Security Review",
  "approvals_required": 2,
  "rule_type": "regular",
  "user_ids": [],
  "group_ids": [<security-team-group-id>]
}
```

**Audit evidence produced:** Branch protection configuration exports, access control logs showing who has write access to protected branches, merge request approval history.

---

## Stage 2: SAST and Secure Coding Analysis

Static Application Security Testing scans source code for vulnerabilities before the application is built. This is the most direct evidence of ISO 27001 A.8.28 (Secure coding) and SOC 2 CC7.1 (vulnerability identification).

### GitHub Actions Implementation

```yaml
# .github/workflows/security-scan.yml
name: Security Scans
on:
  pull_request:
    branches: [main, develop]

jobs:
  sast-scan:
    name: SAST - Semgrep
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep:latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep SAST
        run: |
          semgrep ci \
            --config "p/owasp-top-ten" \
            --config "p/cwe-top-25" \
            --config "p/security-audit" \
            --sarif --output semgrep-results.sarif \
            --error  # Exit code 1 on findings = blocks merge
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}

      - name: Upload SARIF to GitHub Security
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep-results.sarif

      - name: Archive scan results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: sast-results-${{ github.sha }}
          path: semgrep-results.sarif
          retention-days: 2555  # 7 years for SOC 2 evidence retention
```

### GitLab CI Implementation

```yaml
# .gitlab-ci.yml
sast-scan:
  stage: test
  image: semgrep/semgrep:latest
  script:
    - semgrep ci
        --config "p/owasp-top-ten"
        --config "p/cwe-top-25"
        --config "p/security-audit"
        --json --output gl-sast-report.json
        --error
  artifacts:
    reports:
      sast: gl-sast-report.json
    paths:
      - gl-sast-report.json
    expire_in: 7 years
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

**Tool alternatives:** CodeQL (GitHub-native, strong for compiled languages), SonarQube (broad language support, quality + security), Checkmarx (enterprise-grade, supports compliance-specific rule sets). Semgrep is recommended for most teams because its rules are open source, its configuration is declarative, and it produces SARIF output that integrates directly with GitHub Security.

**The audit requirement:** The scan must run on every change. Results must be stored. Findings above a defined severity threshold must block the merge. If you allow developers to override findings without a documented exception process, the control is ineffective.

---

## Stage 3: Software Composition Analysis and SBOM Generation

SCA identifies known vulnerabilities in third-party dependencies. SOC 2 CC7.1 and ISO 27001 A.8.28 both require that organizations identify and remediate vulnerabilities in software components — including components they did not write.

```yaml
  sca-scan:
    name: SCA - Dependency Review
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
          deny-licenses: "GPL-3.0, AGPL-3.0"
          allow-ghsas: ""  # No advisory bypasses without documented exception

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: spdx-json
          output-file: sbom-${{ github.sha }}.spdx.json

      - name: Scan SBOM with Grype
        uses: anchore/scan-action@v4
        with:
          sbom: sbom-${{ github.sha }}.spdx.json
          fail-build: true
          severity-cutoff: high
          output-format: sarif

      - name: Archive SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom-${{ github.sha }}
          path: sbom-${{ github.sha }}.spdx.json
          retention-days: 2555
```

The SBOM (Software Bill of Materials) is increasingly important for audits. It provides a machine-readable inventory of every dependency in your application, which directly satisfies ISO 27001 A.8.9 (Configuration management) and supports SOC 2 CC8.1 evidence by documenting the full composition of every release.

---

## Stage 4: Secrets Scanning

Hardcoded secrets in source code are among the most common SOC 2 findings. SOC 2 CC6.1 (Logical access controls) and CC6.7 (Restricting the transmission of confidential information) both apply. ISO 27001 A.8.4 (Access to source code) and A.8.11 (Data masking) are the corresponding controls.

### Pre-commit + CI Implementation

Secrets scanning must run in two places: as a pre-commit hook (catching secrets before they enter Git history) and in CI (catching anything the pre-commit hook missed).

```yaml
  secrets-scan:
    name: Secrets Detection - Gitleaks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for scanning all commits in the PR

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        with:
          args: --log-opts="origin/main..HEAD"
        env:
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
          GITLEAKS_NOTIFY_USER_LIST: "@security-team"

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: secrets-scan-${{ github.sha }}
          path: results.sarif
          retention-days: 2555
```

**Pre-commit hook (developer machine):**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

**Tool alternatives:** TruffleHog (excellent entropy-based detection), GitHub Advanced Security secret scanning (native integration, partner pattern detection), GitLab Secret Detection (built into GitLab Ultimate). Gitleaks is recommended for teams that need a tool that works across any CI system, is fully open source, and supports custom regex patterns for organization-specific secret formats.

**Critical configuration:** The `.gitleaks.toml` file must be reviewed and maintained. Allowlisting paths or patterns requires a documented exception with a justification. Auditors will check whether your allowlist effectively disables the scanner.

---

## Stage 5: Infrastructure as Code Scanning

If your infrastructure is defined in Terraform, CloudFormation, Pulumi, or Kubernetes manifests, those definitions are code — and they are subject to the same change management requirements as application code. SOC 2 CC8.1 and ISO 27001 A.8.9 (Configuration management) require that infrastructure changes go through a defined review and approval process.

```yaml
  iac-scan:
    name: IaC Security - Checkov
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: ./infrastructure/
          framework: terraform,kubernetes,dockerfile
          output_format: cli,sarif
          output_file_path: console,checkov-results.sarif
          soft_fail: false  # Hard fail = blocks merge on findings
          skip_check: ""    # No skips without documented exception
          quiet: true

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: checkov-results.sarif
```

Checkov evaluates IaC against hundreds of policies covering:

- S3 buckets without encryption (SOC 2 CC6.7, ISO 27001 A.8.24)
- Security groups with unrestricted ingress (SOC 2 CC6.6, ISO 27001 A.8.20)
- IAM policies with wildcard permissions (SOC 2 CC6.3, ISO 27001 A.8.3)
- RDS instances without encryption at rest (SOC 2 CC6.1, ISO 27001 A.8.24)
- Kubernetes pods running as root (SOC 2 CC6.1, ISO 27001 A.8.25)

**Tool alternatives:** tfsec (Terraform-specific, fast), KICS (Checkmarx, multi-framework), Trivy (Aqua Security, covers IaC + containers + SBOM in one scanner). Checkov is recommended because it covers the broadest set of IaC frameworks and outputs compliance-framework-specific results.

---

## Stage 6: Container Image Scanning

If you deploy containers, every image must be scanned before it reaches production. SOC 2 CC7.1 and ISO 27001 A.8.28 require vulnerability identification in all software components, including base images and OS-level packages.

```yaml
  container-scan:
    name: Container Image Scan - Trivy
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@0.28.0
        with:
          image-ref: "${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}"
          format: "sarif"
          output: "trivy-results.sarif"
          severity: "CRITICAL,HIGH"
          exit-code: "1"  # Fail build on CRITICAL or HIGH
          ignore-unfixed: false
          vuln-type: "os,library"

      - name: Upload Trivy scan results
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-results.sarif
```

**Audit evidence produced:** CVE scan results for every container image, linked to the specific Git commit and deployment. Auditors will verify that images with critical vulnerabilities were not deployed to production — or, if they were, that a documented risk acceptance exists.

---

## Stage 7: DAST in Staging Environments

Dynamic Application Security Testing runs against a deployed instance of your application, testing for runtime vulnerabilities that static analysis cannot detect. ISO 27001 A.8.29 specifically requires security testing in development and acceptance — DAST in a staging environment directly satisfies this control.

```yaml
  dast-scan:
    name: DAST - OWASP ZAP
    runs-on: ubuntu-latest
    needs: [deploy-staging]
    steps:
      - name: OWASP ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.11.0
        with:
          target: "https://staging.yourapp.com"
          rules_file_name: ".zap/rules.tsv"
          cmd_options: >-
            -j
            -z "-config alert.maxInstances=10"
          artifact_name: "zap-results-${{ github.sha }}"
          allow_issue_writing: false

      - name: Evaluate ZAP results
        run: |
          HIGH_ALERTS=$(jq '[.site[].alerts[] | select(.riskcode == "3")] | length' zap-results.json)
          if [ "$HIGH_ALERTS" -gt 0 ]; then
            echo "::error::DAST found $HIGH_ALERTS high-risk alerts. Blocking deployment."
            exit 1
          fi
```

DAST is typically the most time-consuming scan. Run it against staging after deployment, not in the PR pipeline. The results still gate production deployment through the approval workflow described in the next section.

---

## Stage 8: Approval Gates and Deployment Authorization

This is the stage that most directly satisfies SOC 2 CC8.1's requirement for authorized changes and ISO 27001 A.8.31's requirement for separation of development, test, and production environments.

### GitHub Environments with Required Reviewers

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: ./scripts/deploy.sh staging

  deploy-production:
    needs: [deploy-staging, dast-scan]
    environment:
      name: production
      url: https://app.yourcompany.com
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Verify all security scans passed
        run: |
          # Query GitHub API for all required check statuses
          CHECKS=$(gh api repos/${{ github.repository }}/commits/${{ github.sha }}/check-runs \
            --jq '.check_runs[] | select(.conclusion != "success") | .name')
          if [ -n "$CHECKS" ]; then
            echo "::error::The following checks have not passed: $CHECKS"
            exit 1
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Deploy to production
        run: ./scripts/deploy.sh production

      - name: Record deployment metadata
        run: |
          echo '{
            "sha": "${{ github.sha }}",
            "deployer": "${{ github.actor }}",
            "environment": "production",
            "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
            "approvers": "${{ github.event.review.user.login }}",
            "pipeline_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          }' | tee deployment-record.json

      - name: Upload deployment record
        uses: actions/upload-artifact@v4
        with:
          name: deployment-record-${{ github.sha }}
          path: deployment-record.json
          retention-days: 2555
```

The `environment: production` key is critical. Configure the `production` environment in GitHub Settings with:

- **Required reviewers:** At least one member of the infrastructure or security team must approve before the deployment job runs.
- **Wait timer:** Optional delay (e.g., 15 minutes) to allow for last-minute objections.
- **Deployment branches:** Restrict to `main` only, preventing deployments from feature branches.

### GitOps with ArgoCD

For teams using GitOps, ArgoCD provides a declarative deployment model where the desired state of production is defined in a Git repository. ArgoCD continuously reconciles the cluster state with the repository state.

```yaml
# argocd/applications/production.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-production
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: deployments
    notifications.argoproj.io/subscribe.on-sync-failed.slack: deployments
spec:
  project: production
  source:
    repoURL: https://github.com/yourorg/k8s-manifests.git
    targetRevision: main
    path: environments/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: false       # Do not auto-delete resources — require manual action
      selfHeal: true     # Revert manual cluster changes to match Git state
    syncOptions:
      - CreateNamespace=false
      - PrunePropagationPolicy=foreground
      - ApplyOutOfSyncOnly=true
```

The compliance advantage of GitOps: **Git is the audit trail.** Every production change is a Git commit. Every Git commit has an author, a timestamp, a reviewer, and a diff. ArgoCD's sync history provides a complete record of when each commit was applied to the cluster and whether it succeeded or failed.

**ArgoCD RBAC for separation of duties:**

```csv
# argocd-rbac-cm ConfigMap
p, role:developer, applications, get, production/*, allow
p, role:developer, applications, sync, staging/*, allow
p, role:deployer, applications, sync, production/*, allow
p, role:deployer, applications, get, production/*, allow
g, dev-team, role:developer
g, sre-team, role:deployer
```

This configuration ensures that developers can view production applications but cannot trigger syncs. Only SRE team members can synchronize changes to production. This is a direct implementation of ISO 27001 A.8.31 (Separation of environments) and SOC 2 CC6.1 (Role-based access).

---

## Stage 9: Immutable Audit Logging

Every stage described above produces artifacts. But artifacts are only useful for audits if they are immutable (cannot be altered after creation), centralized (queryable from a single location), and retained for the required period (SOC 2 typically requires 1 year of observation plus retention; ISO 27001 A.8.17 requires synchronized, tamper-evident logs).

### Centralized Log Pipeline

```yaml
# .github/workflows/audit-log-export.yml
name: Export Audit Logs
on:
  schedule:
    - cron: "0 2 * * *"  # Daily at 2 AM UTC

jobs:
  export-logs:
    runs-on: ubuntu-latest
    steps:
      - name: Export GitHub Audit Log
        run: |
          gh api /orgs/${{ github.repository_owner }}/audit-log \
            --paginate \
            --jq '.[] | select(.created_at > (now - 86400 | todate))' \
            > audit-log-$(date +%Y-%m-%d).json
        env:
          GH_TOKEN: ${{ secrets.AUDIT_LOG_TOKEN }}

      - name: Ship to immutable storage
        run: |
          aws s3 cp audit-log-$(date +%Y-%m-%d).json \
            s3://compliance-audit-logs/github/$(date +%Y/%m/%d)/ \
            --storage-class GLACIER_IR
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AUDIT_AWS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AUDIT_AWS_SECRET }}
```

**Immutability guarantees:**

- **S3 Object Lock** (Compliance mode): Prevents any user, including the root account, from deleting or overwriting objects for the retention period. Configure a 7-year retention period for SOC 2 evidence.
- **AWS CloudTrail** with log file validation: Provides tamper-evident logging of all API calls to the S3 bucket itself — proving that no one modified the audit logs.
- **Alternative: GCP Cloud Storage with Bucket Lock** or **Azure Blob Storage with immutability policies** provide equivalent guarantees.

### What to Log

The following data must be captured for every production deployment to satisfy auditor evidence requests:

| Data Point | Source | SOC 2 Control | ISO 27001 Control |
|---|---|---|---|
| Git commit SHA | Git / CI | CC8.1 | A.8.25 |
| Author of the change | Git commit metadata | CC8.1, CC6.1 | A.8.4, A.8.25 |
| Pull request reviewers and approvers | GitHub/GitLab API | CC8.1 | A.8.25 |
| All security scan results (SAST, SCA, DAST, secrets, IaC) | CI artifacts | CC7.1 | A.8.25, A.8.28, A.8.29 |
| Approval timestamp for production deployment | CI environment approval | CC8.1 | A.8.25 |
| Deployment timestamp and target environment | CI/ArgoCD | CC8.1 | A.8.31 |
| Deployment success/failure status | CI/ArgoCD | CC8.1 | A.8.25 |
| Rollback events (if any) | CI/ArgoCD | CC8.1 | A.8.32 |
| SBOM for the deployed artifact | CI artifacts | CC8.1 | A.8.9 |

---

## Stage 10: Rollback and Incident Response Integration

SOC 2 CC8.1 requires that changes can be reversed. ISO 27001 A.8.32 (Change management) requires defined procedures for handling failed changes. Your pipeline must support rollback, and your rollback procedures must be documented and tested.

### Automated Rollback with Health Checks

```yaml
      - name: Deploy with canary and automatic rollback
        run: |
          # Deploy canary (10% traffic)
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --record

          # Wait for rollout and monitor health
          if ! kubectl rollout status deployment/myapp --timeout=300s; then
            echo "::error::Deployment failed health check. Initiating rollback."
            kubectl rollout undo deployment/myapp

            # Log rollback event for audit trail
            echo '{
              "event": "automatic_rollback",
              "sha": "${{ github.sha }}",
              "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
              "reason": "health_check_failure",
              "pipeline_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
            }' > rollback-record.json

            exit 1
          fi
```

**For ArgoCD-based deployments:** Rollback is a Git revert. Revert the commit in the manifests repository, and ArgoCD automatically syncs the cluster back to the previous state. The Git history provides the audit trail.

---

## Putting It All Together: The Complete Pipeline Architecture

The full compliant pipeline follows this sequence:

```
Developer pushes to feature branch
    |
    v
Pull Request opened against main
    |
    +---> SAST scan (Semgrep/CodeQL)
    +---> SCA scan (Dependency Review + Grype)
    +---> Secrets scan (Gitleaks)
    +---> IaC scan (Checkov)
    +---> Unit + integration tests
    +---> Container image build + scan (Trivy)
    |
    v
All checks pass? ---- No ----> PR blocked, developer fixes findings
    |
    Yes
    |
    v
Code review by 2+ authorized reviewers
    |
    v
PR merged to main
    |
    v
Deploy to staging environment
    |
    v
DAST scan against staging (OWASP ZAP)
    |
    v
DAST passes? ---- No ----> Deployment blocked, findings triaged
    |
    Yes
    |
    v
Production deployment approval (required reviewer)
    |
    v
Deploy to production (with health checks and rollback)
    |
    v
Deployment record logged to immutable storage
    |
    v
SBOM archived with release metadata
```

Every arrow in this diagram produces audit evidence. Every gate is enforceable and verifiable. No manual steps require trust — the pipeline enforces the policy.

---

## Common Audit Findings and How to Prevent Them

Even teams with sophisticated pipelines receive audit findings. These are the most frequent gaps:

**Finding: Developers can bypass branch protection.** Root cause: `enforce_admins` is set to `false`, or organization owners are exempt from branch protection rules. Fix: Enable admin enforcement. Audit your GitHub/GitLab organization role assignments quarterly.

**Finding: Security scan results are not retained.** Root cause: CI artifacts use default retention (90 days in GitHub Actions), which is insufficient for SOC 2 observation periods. Fix: Set `retention-days: 2555` (7 years) on all compliance-relevant artifacts, or export to immutable external storage.

**Finding: No evidence of scan failures blocking deployment.** Root cause: Scans run but are configured as "informational" — they do not fail the build. Fix: Every scan must use `exit-code: 1` or equivalent hard-fail configuration. Document any exceptions in a risk acceptance register.

**Finding: Production deployment does not require separate approval.** Root cause: The same developer who wrote the code can merge the PR and deploy to production without any additional gate. Fix: Use GitHub Environments with required reviewers, or ArgoCD RBAC that restricts production sync to a separate team.

**Finding: No SBOM generated for deployed artifacts.** Root cause: Teams generate SBOMs only on demand during audits, not as part of the build process. Fix: Generate and archive an SBOM for every build that reaches production. Link the SBOM to the deployment record by Git SHA.

**Finding: Rollback procedures are documented but never tested.** Root cause: The change management policy describes rollback, but there is no evidence of rollback drills or actual rollbacks. Fix: Schedule quarterly rollback drills. Record the drill execution and results as audit evidence.

---

## How QuickTrust Automates CI/CD Compliance Evidence

QuickTrust integrates directly with your CI/CD pipeline to automate the evidence collection described in this guide. Instead of manually exporting scan results, archiving deployment records, and mapping artifacts to controls, QuickTrust:

- **Ingests CI/CD events** from GitHub Actions, GitLab CI, and ArgoCD via webhooks and API integrations
- **Maps pipeline artifacts to controls** automatically — linking your Semgrep scan results to SOC 2 CC7.1, your branch protection configuration to CC8.1, your deployment approvals to ISO 27001 A.8.25
- **Generates audit-ready evidence packages** that your auditor can review directly, with timestamped artifacts organized by control objective
- **Monitors for control drift** — alerting you if branch protection rules are weakened, if scan stages are removed from pipelines, or if deployments bypass approval gates
- **Maintains your SBOM registry** with historical records linked to every production release

The platform is open source. You can inspect the integration code, run it in your own infrastructure, and extend it for custom frameworks.

**Have our DevOps engineers set up your compliant CI/CD pipeline.** [Book a pipeline review](https://trust.quickintell.com/contact) and we will audit your current CI/CD configuration, identify control gaps against SOC 2 CC8 and ISO 27001 Annex A, and implement the pipeline stages described in this guide — configured for your specific tech stack and deployment model.
