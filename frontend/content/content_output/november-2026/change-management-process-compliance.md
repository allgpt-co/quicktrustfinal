---
meta_description: "Master the change management process for SOC 2, ISO 27001, and PCI DSS compliance. Learn how to build auditor-approved change control workflows with templates and real examples."
target_keyword: "change management process"
secondary_keywords: "change management policy, change control process, change management compliance, change advisory board, change management for SOC 2"
word_count_target: 4000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-19
---

# The Change Management Process That Passes SOC 2, ISO 27001, and PCI DSS Audits: A Complete Implementation Guide

A failed change management process is the number one reason companies fail SOC 2 audits. Not missing encryption. Not weak passwords. Not a lack of monitoring. Change management.

The pattern is painfully consistent. Engineering teams deploy code to production multiple times a day. Every deploy is tracked in Git. Every pull request has a reviewer. The team believes — genuinely — that their process is solid. Then the auditor arrives and asks three questions: Where is the formal record of change approval? Where is the risk assessment for this production change? Where is the evidence that testing was completed before deployment?

The Git log does not answer those questions. Neither does the Slack thread where someone typed "LGTM." The team scrambles. The auditor writes a finding. The audit drags on for weeks longer than planned.

Here is the good news: the fix is simpler than most teams think. Change management for compliance is not a heavyweight ITIL bureaucracy that slows engineering to a crawl. It is a structured workflow — request, classify, assess, approve, implement, verify, close — that maps directly to how modern engineering teams already work. The gap is almost never process. The gap is documentation and evidence.

This guide covers exactly how to build a change management process that satisfies SOC 2, ISO 27001, and PCI DSS requirements, integrates cleanly with DevOps and CI/CD workflows, and generates audit evidence automatically. It is written for CTOs, engineering leads, and compliance practitioners who need a process that works in practice — not just on paper.

---

## What Is Change Management in a Compliance Context?

The term "change management" creates confusion because it means two entirely different things depending on who is using it.

**Organizational change management** is the discipline of managing how people adopt new business processes, technologies, or structures. It involves communication plans, stakeholder buy-in, training programs, and cultural alignment. This is what McKinsey writes about. This is what your HR team runs when the company switches from Slack to Teams.

**IT change management** — the subject of this guide — is the discipline of controlling modifications to IT systems, infrastructure, applications, and configurations. It is a technical control that ensures every change to a production environment is requested, classified, assessed for risk, approved by authorized personnel, tested, implemented with a rollback plan, verified, and documented.

In a compliance context, change management refers exclusively to the IT definition. When a SOC 2 auditor evaluates your change management controls, they are not asking whether your team handled the emotional journey of adopting Kubernetes. They are asking: can you prove that every change to your production environment went through a defined, repeatable, documented process?

The scope of IT change management for compliance purposes includes:

- **Application code changes** — new features, bug fixes, refactors, dependency updates
- **Infrastructure changes** — server provisioning, network configuration, firewall rules, load balancer settings
- **Database changes** — schema migrations, stored procedures, data transformations
- **Configuration changes** — environment variables, feature flags, third-party service configurations
- **Access control changes** — IAM policies, role assignments, permission modifications
- **Security tool changes** — SIEM rules, WAF configurations, endpoint protection policies

If it can affect the security, availability, or integrity of your production environment, it falls within the scope of your change management process.

---

## Why Every Compliance Framework Requires Change Management

Change management is not a nice-to-have that auditors invented to create work. It exists because uncontrolled changes are the single most common cause of security incidents, outages, and data breaches. Every major compliance framework recognizes this reality and requires formal change management controls.

### SOC 2: CC8.1 (Change Management)

SOC 2 Trust Services Criteria CC8.1 states: *"The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures to meet its objectives."*

This is one of the most frequently tested controls in a SOC 2 Type II audit. The auditor will typically sample 25-40 changes from your observation period and verify that each one followed your documented change management process. For each sampled change, the auditor expects to see:

- A formal change request with a description of the change
- Classification of the change type and risk level
- Evidence of risk assessment or impact analysis
- Approval from an authorized individual (not the person who made the change)
- Evidence that the change was tested before production deployment
- A documented rollback plan
- Verification that the change was implemented successfully
- Closure documentation

If even a handful of sampled changes are missing any of these elements, you will receive a control exception — and enough exceptions can lead to a qualified opinion.

### ISO 27001: Annex A Control A.8.32 (Change Management)

ISO 27001:2022 Annex A Control A.8.32 requires that *"changes to information processing facilities and information systems shall be subject to change management procedures."* This control is part of the broader A.8 (Technological Controls) family and works alongside:

- **A.8.25** — Secure development lifecycle
- **A.8.29** — Security testing in development and acceptance
- **A.8.31** — Separation of development, test, and production environments
- **A.8.33** — Test information

ISO 27001 auditors expect a documented change management policy, a defined process, and evidence that the process is followed consistently. The ISO framework is less prescriptive about exactly what the process must look like — but it is uncompromising about the requirement that a process exists, is documented, and is followed.

For a complete overview of ISO 27001 controls and audit expectations, see our [ISO 27001 Complete Implementation Guide](/iso-27001-certification-guide).

### PCI DSS 4.0: Requirement 6.5.x (Change and Software Management)

PCI DSS 4.0 Requirement 6.5 mandates that *"changes to all system components in the production environment are managed."* Specific sub-requirements include:

- **6.5.1** — Changes are documented with reason, approval, testing, and rollback procedures
- **6.5.2** — Changes are confirmed to not adversely impact security after deployment
- **6.5.3** — Pre-production environments are separated from production
- **6.5.4** — Custom code changes are reviewed before release to production
- **6.5.5** — Live PANs (Primary Account Numbers) are not used in testing
- **6.5.6** — Test accounts and data are removed before production systems go live

PCI DSS is particularly strict about change management because the cardholder data environment (CDE) requires the highest levels of control. Every change that could affect the CDE — even indirectly — must go through formal change management.

### The Common Thread

Across all three frameworks, the auditor is asking the same fundamental question: **do you have a defined, documented, consistently followed process for managing changes to your production environment?** The specific control numbers differ, but the evidence requirements converge:

| Evidence Element | SOC 2 CC8.1 | ISO 27001 A.8.32 | PCI DSS 6.5.x |
|---|---|---|---|
| Change request/ticket | Required | Required | Required |
| Risk assessment | Required | Required | Required |
| Approval by authorized person | Required | Required | Required |
| Testing evidence | Required | Required | Required |
| Rollback plan | Required | Recommended | Required |
| Post-implementation verification | Required | Required | Required |
| Separation of duties | Required | Required | Required |

---

## The Change Management Lifecycle: 7 Steps

A compliant change management process follows a lifecycle with seven discrete steps. Each step produces specific evidence that auditors evaluate. Skipping any step creates a control gap.

### Step 1: Request

Every change begins with a formal request. This is not optional. A developer pushing code without a corresponding change request is, from an audit perspective, an unauthorized change — regardless of whether the code was reviewed.

The change request must include:

- **Description of the change** — what is being modified and why
- **Requestor identity** — who is asking for the change
- **Affected systems** — which components, services, or infrastructure are impacted
- **Business justification** — why this change is needed
- **Requested timeline** — when the change should be deployed

In practice, this is usually a Jira ticket, a GitHub issue, or a ServiceNow change request. The tool does not matter. What matters is that every production change has a corresponding, timestamped record that was created before the change was implemented.

### Step 2: Classify

Not all changes carry the same risk. Classification determines the approval path, testing requirements, and urgency. There are three standard classifications (covered in detail in the next section):

- **Standard changes** — pre-approved, low-risk, routine changes
- **Normal changes** — changes that require full assessment and approval
- **Emergency changes** — urgent changes needed to restore service or patch critical vulnerabilities

Classification should happen immediately after the request is created, ideally by the requestor with validation from the team lead or change manager.

### Step 3: Assess

Risk assessment evaluates the potential impact of the change on system security, availability, and integrity. For a normal change, the assessment should answer:

- What could go wrong if this change fails?
- What is the blast radius — which systems, users, or data could be affected?
- Are there dependencies on other systems or changes?
- What is the risk of not making the change?
- Does this change affect any systems in the compliance scope?

The assessment does not need to be a formal risk matrix for every change. For most engineering teams, a structured section in the change ticket — impact level (low/medium/high), affected services, and dependencies — is sufficient. What auditors care about is that the assessment happened, was documented, and informed the approval decision.

### Step 4: Approve

Approval is the control point that auditors scrutinize most carefully. The core requirement is **separation of duties**: the person who approves the change must not be the same person who implements it. A developer approving their own pull request and then merging it is a separation of duties violation, full stop.

For normal changes, approval authority should be defined in your change management policy. Typical approvers include:

- Engineering team leads or managers
- Change Advisory Board (CAB) for high-risk changes
- Security team for changes affecting security controls
- Database administrators for schema changes

The approval must be timestamped and attributable to a specific individual. A pull request approval in GitHub with a named reviewer satisfies this requirement. A Slack message saying "go ahead" does not, unless it is captured as part of a formal audit trail.

### Step 5: Implement

Implementation is the execution of the change itself — the code deploy, the infrastructure update, the configuration change. From a compliance perspective, what matters during implementation is:

- **The change matches the approved request.** If the approved change was "update the payment API rate limits" and the actual deployment included a database schema migration, there is a scope deviation.
- **The change is deployed to a test environment first.** SOC 2, ISO 27001, and PCI DSS all require separation between development, test, and production environments.
- **A rollback plan exists.** Before implementing the change in production, the team must have a documented plan for reverting if something goes wrong. This can be as simple as "revert to the previous container image" or as detailed as a step-by-step database rollback script.

### Step 6: Verify

After implementation, the change must be verified. Verification confirms that:

- The change was deployed successfully
- The change behaves as expected
- No unintended side effects occurred
- Security controls remain intact

Verification evidence includes post-deployment smoke tests, monitoring dashboard screenshots, automated test results, and explicit confirmation from the implementer or a designated verifier.

### Step 7: Close

Closure is the formal completion of the change record. The change ticket is updated with:

- Implementation date and time
- Verification results
- Any issues encountered during deployment
- Final status (successful, rolled back, partial)

A closed change record is the single most important audit artifact. When an auditor samples a change, they pull the closed ticket and evaluate whether all seven steps are documented. Missing closure documentation is one of the most common audit findings — teams implement changes correctly but never go back to close the ticket.

---

## Change Types: Standard, Normal, and Emergency Changes

Not every change requires a full CAB review and a five-page risk assessment. Classifying changes into types allows you to apply the right level of rigor without creating unnecessary overhead.

### Standard Changes

Standard changes are pre-approved changes that follow a well-understood, low-risk, repeatable procedure. They do not require individual approval for each instance because the change type itself has already been assessed and approved.

**Examples:**

- Deploying a dependency version bump that passes all automated tests
- Rotating scheduled credentials or API keys
- Scaling infrastructure within pre-defined parameters (adding pods, increasing instance count)
- Updating static content (documentation, marketing pages)
- Applying vendor-released security patches to non-production systems

**Approval path:** No individual approval required. The standard change catalog itself is approved by the CAB or change management authority. Each standard change execution is logged automatically.

**Audit evidence:** A documented standard change catalog, plus automated records showing each standard change was executed within the defined parameters.

The key risk with standard changes is scope creep — teams labeling complex changes as "standard" to avoid the approval process. Your standard change catalog must be reviewed quarterly, and any change that deviates from the catalog parameters must be reclassified as normal.

### Normal Changes

Normal changes are the default classification. They represent changes that require individual assessment, approval, and testing. Most feature deployments, infrastructure modifications, and configuration changes fall into this category.

**Examples:**

- Deploying a new feature to production
- Modifying database schemas
- Changing network configurations, firewall rules, or security group settings
- Integrating a new third-party service
- Modifying authentication or authorization logic
- Changing infrastructure architecture (new services, regions, or accounts)

**Approval path:** Full lifecycle — request, classify, assess, approve (by an authorized approver who is not the implementer), implement, verify, close.

**Audit evidence:** Complete change ticket with all seven lifecycle stages documented, including risk assessment, named approver with timestamp, testing evidence, and closure.

### Emergency Changes

Emergency changes are changes that must be implemented immediately to restore service, patch a critical vulnerability, or mitigate an active security incident. They bypass the normal approval process — but they are not exempt from documentation.

**Examples:**

- Hotfixing a production outage
- Patching a zero-day vulnerability that is actively being exploited
- Revoking compromised credentials
- Blocking malicious IP addresses during an active attack

**Approval path:** The change can be implemented first and documented afterward. However, there must be a defined emergency change process that specifies:

- Who is authorized to declare an emergency change
- What constitutes a valid emergency (not "the product manager wants this feature by Friday")
- A maximum timeframe for retroactive documentation (typically 24-48 hours)
- A mandatory post-implementation review

**Audit evidence:** An emergency change record that includes the justification for bypassing normal procedures, the approving authority, retroactive documentation of all standard fields, and a post-implementation review.

Auditors will scrutinize your emergency change volume. If more than 5-10% of your changes are classified as emergencies, the auditor will question whether your process is being circumvented. A high emergency change rate is a red flag that triggers deeper sampling.

---

## Building a Change Advisory Board (CAB): Roles, Responsibilities, and Meeting Cadence

A Change Advisory Board is a cross-functional group responsible for reviewing, prioritizing, and approving changes that carry significant risk. Not every organization needs a formal CAB — for small engineering teams, an approval workflow with designated approvers may suffice. But as your organization scales and your compliance scope expands across multiple frameworks, a CAB becomes essential.

### CAB Composition

| Role | Responsibility | Why They Are Needed |
|---|---|---|
| CAB Chair | Facilitates meetings, ensures process adherence, makes final approval decisions when consensus cannot be reached | Provides governance and accountability |
| Engineering Lead(s) | Assesses technical risk, validates testing adequacy, evaluates implementation plans | Technical authority on feasibility and impact |
| Security/Compliance Lead | Evaluates changes for security implications, ensures compliance requirements are met | Prevents changes that create compliance gaps |
| Infrastructure/DevOps Lead | Assesses infrastructure impact, validates deployment procedures, confirms rollback plans | Operational authority on deployment risk |
| Product Representative | Provides business context, prioritizes conflicting changes, validates business justification | Ensures changes align with business objectives |
| QA Representative | Validates testing coverage, identifies gaps in test plans | Ensures adequate testing before production |

### Meeting Cadence

The CAB meeting cadence depends on your deployment velocity:

**High-velocity teams (multiple deploys per day):** Weekly CAB meetings to review upcoming high-risk changes. Standard and pre-approved normal changes proceed through automated workflows without CAB review. The CAB focuses exclusively on changes classified as high-risk or changes that affect the compliance scope boundary.

**Moderate-velocity teams (daily or weekly deploys):** Bi-weekly CAB meetings. All normal changes above a defined risk threshold are reviewed. Standard changes proceed without review.

**Regulated environments with strict change windows:** Weekly CAB meetings with a formal change calendar. All normal and emergency changes are reviewed. Changes are scheduled into approved change windows.

### What the CAB Reviews

For each change brought to the CAB, the board evaluates:

1. Is the business justification valid?
2. Has the risk assessment been completed and is the risk level acceptable?
3. Is the testing plan adequate for the risk level?
4. Is the rollback plan credible and tested?
5. Are there scheduling conflicts with other changes?
6. Are there compliance implications (does this change affect systems in scope)?

### CAB Meeting Documentation

Every CAB meeting must produce a documented record that includes:

- Date, attendees, and changes reviewed
- Approval or rejection decisions with rationale
- Conditions placed on approved changes (e.g., "approved contingent on completing load testing")
- Action items and owners
- Deferred changes and reasons for deferral

This documentation is audit evidence. Store it in a system that produces timestamped, immutable records — not a Google Doc that anyone can edit.

---

## Change Management for DevOps and CI/CD Pipelines

This is where most engineering teams push back. "We deploy 50 times a day. We can't file a change ticket for every deploy. Change management will destroy our velocity."

This concern is valid — if change management means a manual, paper-based, ITIL-heavy process designed for quarterly mainframe updates. It is not valid if change management means a structured workflow integrated into your existing CI/CD pipeline that generates evidence automatically.

The goal is not to slow down deployment. The goal is to prove that every deployment went through a defined process. Here is how to do that without sacrificing velocity.

### Map the CI/CD Pipeline to Change Management Steps

| Change Management Step | CI/CD Implementation | Evidence Generated |
|---|---|---|
| Request | GitHub Issue or Jira ticket linked to PR | Timestamped ticket with description and requester |
| Classify | Labels or fields on the ticket (standard/normal/emergency) | Classification record |
| Assess | PR description template with impact analysis section | Documented risk assessment |
| Approve | PR review approval from a reviewer who is not the author | Timestamped approval from named approver |
| Implement | Merge to main, CI/CD deploys to staging then production | Deployment logs with timestamps |
| Verify | Automated smoke tests, monitoring checks post-deploy | Test results, monitoring data |
| Close | Ticket auto-closed on successful deployment | Closure timestamp and final status |

### Enforce Separation of Duties in Code

Branch protection rules enforce the most critical audit requirement: separation of duties. Configure your repository so that:

- Pull requests require at least one approval from a reviewer who did not author the PR
- The PR author cannot approve their own PR
- Admin override is disabled (enforce_admins = true in GitHub)
- Status checks must pass before merge is allowed
- Stale reviews are dismissed when new commits are pushed

This configuration means that no single individual can make a production change without another authorized person reviewing and approving it. This is exactly what SOC 2 CC8.1 requires, and it happens automatically within your normal development workflow.

### Automate Classification

Use PR labels, Jira workflow automation, or CI pipeline logic to automatically classify changes:

- Changes that only modify documentation files or test files: classify as standard
- Changes that modify source code but are within a pre-defined scope (e.g., a single microservice with no database changes): classify as normal-low
- Changes that modify infrastructure-as-code, database migrations, authentication logic, or security controls: classify as normal-high, requiring additional review
- Changes deployed outside of normal hours or bypassing the standard PR process: flag as potential emergency changes requiring retroactive documentation

### Use Deployment Pipelines as Evidence Trails

Your CI/CD pipeline, configured correctly, is the change management evidence trail. Every pipeline run should capture and store:

- The commit SHA and PR number
- The linked ticket or issue number
- The pipeline stages executed and their results (SAST scan, unit tests, integration tests, security scan)
- The approval that authorized the merge
- The deployment timestamp and target environment
- Post-deployment verification results

Store these records in an immutable log. If you are using GitHub Actions, the workflow run logs serve this purpose. If you are using Jenkins, configure archival of build logs to an immutable store (S3 with object lock, for example).

For a detailed implementation guide on building a compliant CI/CD pipeline, see our [DevSecOps for Compliance guide](/devsecops-compliance-cicd-guide).

---

## Change Management Documentation: What Auditors Want to See

Understanding what auditors evaluate during a change management audit eliminates the guesswork. Here is exactly what they look for, organized by audit phase.

### Policy Documentation

The auditor's first request will be your change management policy. This is the governing document that defines your process. It must include:

- **Scope** — what systems, environments, and change types are covered
- **Roles and responsibilities** — who can request, approve, and implement changes
- **Change classification scheme** — definitions for standard, normal, and emergency changes
- **Approval authority matrix** — who approves what, and under what conditions
- **Testing requirements** — what must be tested and how, for each change type
- **Emergency change procedures** — when and how normal procedures can be bypassed
- **Documentation requirements** — what records must be maintained for each change

### Process Evidence (Sample Testing)

After reviewing your policy, the auditor samples actual changes. For a SOC 2 Type II audit with a 12-month observation period, expect the auditor to sample 25-40 changes. For each change, they will verify:

**Change ticket completeness:**
- Is there a formal change request with a description?
- Was the change classified?
- Is there a documented risk assessment?
- Was the change approved by an authorized person?
- Is the approver different from the implementer?
- Was the approval given before implementation (not retroactive)?

**Testing evidence:**
- Was the change tested in a non-production environment?
- Are test results documented?
- Did the tests pass before production deployment?

**Implementation evidence:**
- Is there a deployment record with timestamp?
- Was a rollback plan documented?
- Was post-implementation verification performed?

**Closure:**
- Was the change ticket closed with a final status?
- Were any issues during implementation documented?

### The Evidence Package

For each sampled change, you should be able to produce what we call a "change evidence package" — the complete set of records for that change. Ideally, this package can be assembled automatically from your tools. A strong change evidence package looks like this:

1. Jira ticket (or equivalent) with change request, classification, risk assessment
2. Pull request with code diff, reviewer comments, and approval
3. CI/CD pipeline results showing all checks passed
4. Deployment log showing when and where the change was deployed
5. Post-deployment monitoring data confirming successful implementation
6. Ticket closure record

If you can produce this package for any change the auditor selects, in under five minutes, you will pass the change management portion of the audit.

---

## Change Management Tools: GitHub PRs, Jira, ServiceNow as Audit Evidence

Your toolchain matters — not because auditors require specific tools, but because different tools produce different qualities of audit evidence. Here is how common engineering tools map to change management evidence requirements.

### GitHub / GitLab as Change Management Systems

For many engineering teams, the Git-based development workflow already contains most of the change management evidence an auditor needs. A well-structured pull request serves as a change request, risk assessment, approval record, testing record, and implementation log — all in one artifact.

**What makes a PR audit-ready:**

- **PR template** with mandatory fields for change description, risk assessment, testing plan, and rollback plan
- **Linked issue or ticket** connecting the code change to a business requirement
- **Named reviewer approval** with timestamp (not a bot, not a team alias)
- **Required status checks** showing CI pipeline results (tests, scans, builds)
- **Merge commit** with deployment metadata
- **Branch protection** preventing bypass of the above requirements

**What GitHub/GitLab does NOT provide natively:**

- Change classification (standard/normal/emergency)
- CAB approval records for high-risk changes
- Post-implementation verification records (unless you build custom automation)
- Aggregated change management reporting for audit periods

### Jira as the Change Request System

Many teams use Jira as the system of record for change requests, with GitHub handling the implementation and approval. This is an effective combination:

- **Jira** captures the change request, classification, risk assessment, CAB approval (if needed), and closure
- **GitHub** captures the code review, technical approval, CI/CD results, and deployment
- **Links between the two** (Jira ticket number in the PR, PR link in the Jira ticket) create a complete audit trail

Configure Jira with a dedicated change request issue type that includes mandatory fields for classification, risk level, affected systems, and rollback plan. Use workflow transitions to enforce the lifecycle: Open, Classified, Assessed, Approved, Implementing, Verifying, Closed.

### ServiceNow for Enterprise Change Management

For organizations operating at enterprise scale or managing changes across multiple compliance frameworks, ServiceNow's Change Management module provides a purpose-built solution:

- Formal change request records with full audit trail
- Automated risk assessment scoring
- CAB scheduling and approval workflows
- Integration with CI/CD tools via APIs
- Compliance reporting and dashboards
- Conflict detection across concurrent changes

The trade-off is implementation complexity and cost. ServiceNow is overkill for a 20-person startup. It becomes valuable when you are managing hundreds of changes per month across multiple teams and frameworks.

### The Integration Imperative

Regardless of which tools you use, the critical requirement is that they are integrated. A Jira ticket that says "deployed to production" without a link to the actual deployment record is not verifiable evidence. A GitHub PR that was merged without a corresponding change ticket leaves a documentation gap.

The minimum viable integration:

1. Every PR must reference a change ticket (enforced via commit hooks or PR template validation)
2. Every change ticket must link to the PR and deployment record
3. Ticket status must update automatically based on PR and deployment events
4. All records must be immutable and timestamped

---

## Automating Change Management Evidence Collection

Manual evidence collection is the reason compliance teams dread audit season. An engineer deploys a change, forgets to update the Jira ticket, the ticket sits in "In Progress" for three months, and when the auditor asks for evidence, someone has to reconstruct the timeline from Git logs and deployment dashboards.

Automation eliminates this failure mode. Here is what to automate and how.

### Automated Ticket Creation

When a pull request is opened, automatically create or link a change request ticket. Use GitHub Actions, GitLab CI, or a webhook integration:

- Parse the PR description for a ticket reference
- If no ticket exists, create one automatically with metadata from the PR (title, author, files changed, linked issues)
- If a ticket exists, update it with the PR link and classify based on the files modified

### Automated Classification

Use the content of the change to drive classification:

- Changes to `docs/` or `README` files only: standard change
- Changes to application code within a single service: normal-low
- Changes to `infrastructure/`, `terraform/`, `helm/`, or `k8s/` directories: normal-high
- Changes to `auth/`, `security/`, `iam/`, or encryption-related code: normal-high, flag for security review
- Database migration files present: normal-high, flag for DBA review

### Automated Evidence Capture

At each stage of the CI/CD pipeline, capture evidence and attach it to the change record:

- **PR creation** — capture the change request metadata, diff summary, and requester
- **Review approval** — capture the reviewer name, timestamp, and review comments
- **CI pipeline completion** — capture test results, scan results, and pass/fail status
- **Deployment to staging** — capture deployment timestamp, environment, and artifact version
- **Deployment to production** — capture deployment timestamp, approver, and artifact version
- **Post-deployment checks** — capture smoke test results and monitoring status

### Automated Ticket Closure

When a deployment succeeds and post-deployment verification passes, automatically update the change ticket to "Closed - Successful." If the deployment fails and a rollback occurs, update the ticket to "Closed - Rolled Back" with the rollback details.

### The QuickTrust Approach

QuickTrust integrates with your existing development tools — GitHub, GitLab, Jira, CI/CD pipelines — and automatically maps every change to the compliance controls it satisfies. Every pull request, approval, test result, and deployment becomes a compliance artifact that is indexed, searchable, and ready for auditor review. When the auditor requests a sample of changes from the observation period, you pull the evidence package from QuickTrust in seconds, not hours.

This is not a replacement for your engineering workflow. It is a compliance layer that sits on top of your existing tools and generates audit evidence from the work your team is already doing. For more on how continuous compliance monitoring works, see our [guide to building a continuous compliance program](/continuous-compliance-beyond-annual-audit).

---

## Common Change Management Audit Findings (and How to Prevent Them)

After reviewing thousands of SOC 2, ISO 27001, and PCI DSS audit reports, these are the ten most common change management findings — and how to prevent each one.

### Finding 1: Changes Deployed Without Documented Approval

**What the auditor found:** Production changes were merged and deployed without a documented approval from an authorized reviewer. Pull requests were self-merged or merged by the author after their own approval.

**How to prevent it:** Enable branch protection rules that require at least one approval from a reviewer who is not the PR author. Disable admin bypass. Audit branch protection settings quarterly.

### Finding 2: No Separation of Duties

**What the auditor found:** The same individual requested, approved, and implemented the change. There was no independent review or approval.

**How to prevent it:** Define and enforce separation of duties in your change management policy. Configure tooling (branch protection, Jira workflows) to prevent the same person from occupying multiple roles in the change lifecycle.

### Finding 3: Missing Risk Assessment

**What the auditor found:** Change tickets did not include a risk assessment or impact analysis. The auditor could not determine whether the risk of the change was evaluated before approval.

**How to prevent it:** Add mandatory risk assessment fields to your PR template and change request ticket type. Use dropdown fields (Low/Medium/High impact) and a required free-text field for impact description. Block ticket progression without these fields completed.

### Finding 4: Emergency Changes Without Retroactive Documentation

**What the auditor found:** Emergency changes were implemented to resolve production incidents, but no retroactive change ticket was created. The change has no formal record.

**How to prevent it:** Define a maximum retroactive documentation window (24-48 hours) in your emergency change procedure. Create an automated reminder that triggers when a direct push to production is detected or when an emergency deployment occurs without a linked ticket.

### Finding 5: Testing Evidence Not Documented

**What the auditor found:** Changes were approved and deployed, but there was no evidence that testing was performed in a non-production environment before production deployment.

**How to prevent it:** Require CI pipeline status checks to pass before merge. Configure your pipeline to run tests automatically and store results as artifacts. Link test results to the change ticket.

### Finding 6: Rollback Plan Not Documented

**What the auditor found:** Change tickets did not include a rollback plan. The auditor could not confirm that the team had a plan for reverting failed changes.

**How to prevent it:** Add a mandatory rollback plan field to your change request template. For standard changes, the rollback plan can reference the standard procedure (e.g., "revert to previous container image via automated rollback"). For normal changes, require a specific rollback procedure.

### Finding 7: Change Tickets Not Closed

**What the auditor found:** Changes were implemented successfully, but the corresponding tickets remained open for weeks or months. The change record was incomplete.

**How to prevent it:** Automate ticket closure based on deployment status. If manual closure is required, set up automated reminders for open tickets older than 48 hours after deployment.

### Finding 8: Standard Change Catalog Not Maintained

**What the auditor found:** The organization classified changes as "standard" but did not maintain an approved catalog of standard change types. The auditor could not verify that these changes were pre-approved.

**How to prevent it:** Create and maintain a formal standard change catalog. Review it quarterly with the CAB. Document the approval date and approving authority for each standard change type.

### Finding 9: Inconsistent Process Across Teams

**What the auditor found:** Different engineering teams followed different change management processes. Some teams used PR-based approvals, others used Slack-based approvals, and some had no defined process.

**How to prevent it:** Establish a single change management policy that applies to all teams. Configure tooling centrally (organization-wide branch protection rules, standardized Jira workflows). Conduct quarterly audits of process compliance across teams.

### Finding 10: No Evidence of Post-Implementation Verification

**What the auditor found:** Changes were deployed to production, but there was no evidence that the team verified the change was successful after deployment.

**How to prevent it:** Require post-deployment verification as a mandatory step before ticket closure. Automate where possible — run smoke tests after deployment, capture monitoring data, and attach results to the change ticket.

---

## Change Management Policy Template: Key Sections

Your change management policy is the foundation document that auditors review first. A complete policy includes the following sections. This is a structural template — adapt the content to your organization's specific tools, team structure, and risk tolerance.

### Section 1: Purpose and Scope

Define what the policy covers (all changes to production systems, infrastructure, and configurations), what it does not cover (organizational changes, HR processes), and which compliance frameworks it addresses (SOC 2 CC8.1, ISO 27001 A.8.32, PCI DSS 6.5.x).

### Section 2: Definitions

Define key terms: change, change request, change management, standard change, normal change, emergency change, change advisory board, rollback, backout plan, post-implementation review.

### Section 3: Roles and Responsibilities

Define who can perform each role in the change management process:

- **Change Requester** — any team member can submit a change request
- **Change Manager** — responsible for overseeing the process, reviewing classifications, ensuring compliance
- **Change Approver** — authorized to approve changes (engineering leads, CAB members, security team)
- **Change Implementer** — the person executing the change (must be different from the approver)
- **CAB Members** — cross-functional team responsible for reviewing high-risk changes

### Section 4: Change Classification

Define the three change types with specific criteria for each:

- Standard changes: criteria, examples, pre-approval process, and the standard change catalog
- Normal changes: criteria, examples, risk assessment requirements, approval authority
- Emergency changes: criteria for declaring an emergency, authorized declarers, retroactive documentation requirements, post-implementation review requirements

### Section 5: Change Management Process

Document each step of the seven-step lifecycle with:

- Required actions
- Required documentation
- Responsible role
- Tools used
- SLAs (e.g., "normal changes must be assessed within 2 business days of submission")

### Section 6: Approval Authority Matrix

Define who can approve which types of changes:

| Change Type | Risk Level | Approver |
|---|---|---|
| Standard | Pre-approved | No individual approval required |
| Normal | Low | Engineering team lead |
| Normal | Medium | Engineering team lead + one additional reviewer |
| Normal | High | Change Advisory Board |
| Emergency | Any | On-call engineering lead (retroactive CAB review within 48 hours) |

### Section 7: Testing Requirements

Define minimum testing requirements for each change type and risk level. Include requirements for unit tests, integration tests, staging environment validation, and production smoke tests.

### Section 8: Emergency Change Procedures

Document the complete emergency change process, including who can declare an emergency, the expedited approval process, retroactive documentation requirements, and mandatory post-implementation review.

### Section 9: Reporting and Metrics

Define what change management metrics are tracked and reported:

- Total changes by type and risk level per month
- Emergency change rate (percentage of total changes)
- Change failure rate (changes that required rollback)
- Average change lead time
- Audit findings related to change management

### Section 10: Policy Review

Define the policy review schedule (at least annually), the review authority (typically the CAB or security/compliance committee), and the version control process for the policy document itself.

For a comprehensive library of compliance policy templates, including change management, see our [Security Policy Templates resource](/security-policy-templates).

---

## Frequently Asked Questions

### How is IT change management different from organizational change management?

IT change management controls modifications to technology systems — code, infrastructure, configurations, and databases. It is a technical control evaluated during compliance audits. Organizational change management is a business discipline focused on how people adopt new processes or technologies. When an auditor asks about your change management process, they are asking about IT change management exclusively. The two disciplines share a name but have entirely different scopes, audiences, and evaluation criteria.

### How many changes do auditors typically sample during a SOC 2 audit?

For a SOC 2 Type II audit with a 12-month observation period, auditors typically sample 25-40 changes. The sample size depends on the total volume of changes, the auditor's risk assessment, and whether any exceptions are found. If early samples reveal exceptions, auditors will expand the sample size. The sample includes a mix of standard, normal, and emergency changes to verify that all change types are handled according to policy.

### Can we use GitHub pull requests as our change management system?

Yes, but with important caveats. A well-configured GitHub workflow — with branch protection, required reviews, status checks, and PR templates that capture risk assessment and rollback plans — satisfies most change management evidence requirements. The gaps are typically around change classification, CAB approval for high-risk changes, and post-implementation verification. Many teams supplement GitHub with Jira or a similar system for the elements that GitHub does not natively support. The combination of GitHub (for technical review and approval) and Jira (for classification, risk assessment, and lifecycle tracking) covers all audit requirements.

### What percentage of emergency changes is acceptable before auditors flag it as a concern?

There is no official threshold, but general industry guidance is that emergency changes should represent less than 5-10% of total changes. If your emergency change rate consistently exceeds 10%, auditors will question whether your team is using emergency procedures to circumvent normal change management. High emergency change rates also signal operational problems — either your systems are unstable (causing frequent emergency fixes) or your normal change process is too slow (causing teams to classify non-emergencies as emergencies to bypass it). Track and report your emergency change rate monthly.

### How do we handle change management for automated deployments in a CI/CD pipeline?

Automated deployments are fully compatible with change management compliance. The key is to map each CI/CD pipeline stage to a change management step and ensure that evidence is captured automatically at each stage. The pull request serves as the change request and risk assessment. The PR review serves as the approval. The CI pipeline captures testing evidence. The deployment logs capture implementation records. Post-deployment health checks capture verification. Automated ticket updates capture closure. The entire lifecycle happens within your normal development workflow — the compliance layer is the evidence capture, not additional manual steps. See our [DevSecOps for Compliance guide](/devsecops-compliance-cicd-guide) for detailed implementation patterns.

### Do we need a Change Advisory Board if we are a small team?

Not necessarily. The requirement is that changes are reviewed and approved by an authorized person who is not the implementer — not that a formal board exists. For teams of 5-15 engineers, peer review through pull requests with enforced branch protection rules can satisfy the approval requirement for most changes. You may still want a lightweight review process for high-risk changes (infrastructure modifications, security control changes, database migrations) that involves a broader group. As your team grows past 20-30 engineers, or as your compliance scope expands to cover multiple frameworks, a formal CAB becomes increasingly valuable for coordination and risk management.

### What is the difference between a change management policy and a change management process?

The policy is the governing document that defines what must happen — scope, roles, requirements, and authority. The process is how it happens — the specific steps, tools, workflows, and procedures that implement the policy. Your auditor will review both. The policy should be a relatively stable document that changes annually. The process documentation may change more frequently as your tools and workflows evolve. Both must be version-controlled and approved by management.

### How do we prove that our change management process was followed consistently throughout the entire audit observation period?

Consistency is proven through sample testing, not exhaustive review. The auditor samples changes from throughout the observation period — beginning, middle, and end — and verifies that each sampled change followed the documented process. The best defense is automation: if your CI/CD pipeline enforces the process (required reviews, required status checks, automated ticket creation and closure), then the process is followed consistently by design, not by discipline. Automated enforcement means that deviations from the process are technically impossible, which is the strongest evidence of consistency an auditor can receive.

---

## Build a Change Management Process That Runs Itself

Change management is not a compliance checkbox. It is the operational foundation that prevents unauthorized, untested, and undocumented changes from reaching production. Every major compliance framework requires it. Every auditor evaluates it. And every engineering team that builds it correctly discovers that it does not slow them down — it gives them confidence that their deployment process is airtight.

The companies that struggle with change management audits are the ones trying to retrofit documentation onto an undocumented process. The companies that pass effortlessly are the ones whose process generates documentation automatically — through branch protection, CI/CD pipelines, automated ticket management, and integrated tooling.

QuickTrust automates the evidence layer. It connects to your GitHub repositories, CI/CD pipelines, Jira projects, and cloud infrastructure to continuously capture change management evidence — approvals, test results, deployment records, and verification data — and maps every artifact to the specific SOC 2, ISO 27001, and PCI DSS controls it satisfies. When your auditor requests a sample of changes, you pull the complete evidence package from a single dashboard. No scrambling. No reconstructing timelines from Slack messages. No last-minute ticket cleanup.

**[Start a free QuickTrust assessment](https://quicktrustapp.com)** to see how your current change management process maps to SOC 2 CC8.1, ISO 27001 A.8.32, and PCI DSS 6.5.x requirements — and where the evidence gaps are.

---

*Related reading:*

- [The Complete SOC 2 Compliance Guide for SaaS Startups](/soc-2-compliance)
- [ISO 27001 Certification: The Complete Implementation Guide](/iso-27001-certification-guide)
- [DevSecOps for Compliance: CI/CD Pipelines That Pass Audits](/devsecops-compliance-cicd-guide)
- [Beyond the Annual Audit: Building a Continuous Compliance Program](/continuous-compliance-beyond-annual-audit)
