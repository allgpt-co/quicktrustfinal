---
path: "/integrations"
title: "Integrations and Evidence Workflows"
description: "Plan evidence connections for cloud, identity, development, and collaboration systems with clear scope, permissions, and validation."
eyebrow: "Connect your operating systems"
indexable: true
---

## Choose a connection for the evidence you need

Start with a control question and its source system. An integration is useful when it can collect the right evidence for your scope with appropriate permissions and a dependable review process. A vendor logo alone does not establish that every relevant control is covered.

QuickTrust's provider catalog includes AWS, GitHub, Okta, Prowler, Slack, Jira, Azure, Google Cloud, and GitLab. Availability for your deployment, credentials, service permissions, and the exact evidence collected must be confirmed during setup. This catalog describes supported workflow areas; it is not a claim of certified partnership with those providers.

| Workflow area | Evidence topics to validate |
| --- | --- |
| AWS | Identity and MFA, CloudTrail status, encryption configuration |
| GitHub and GitLab | Branch protection, security alerts or pipeline and review records |
| Okta | Identity and MFA enrollment records |
| Azure and Google Cloud | Identity, storage or key configuration, network rules |
| Prowler | Scoped cloud security assessment findings |
| Slack | Notifications and workspace evidence |
| Jira | Remediation tickets and change-management records |

## Agree access and scope before connecting

Identify the system owner, account or organization boundary, required permissions, and the person authorized to grant access. Prefer a dedicated, revocable connection with the least access needed for the collection task. Keep credentials out of support messages, policy documents, and uploaded evidence.

Test a bounded scope first. Check whether the result includes all expected resources, whether names and identifiers are understandable, and whether sensitive values should be removed before broader sharing. Record the collection timestamp and the control it supports.

## Validate the failure path

A successful connection test is only the start. Decide who handles expired credentials, API limits, changed permissions, missing resources, and stale results. Do not interpret a failed collection as a passing control or assume yesterday's data reflects today's environment.

Use a documented manual export where automation cannot provide the required record. Label the collection method clearly and retain the review decision. Some controls depend on operating procedures and human judgment rather than configuration checks.

## Separate evidence access from implementation access

Reading evidence and changing production are different responsibilities. When remediation requires engineering work, define its approval, scope, rollback, and verification separately from the evidence connection. Your organization should be able to revoke each access path without ambiguity.

Review [evidence collection](/solutions/evidence-collection-automation) and [continuous monitoring](/solutions/continuous-compliance-monitoring), or [ask about your stack](/contact). Include the system, control question, deployment context, and data restrictions so the discussion can focus on a concrete workflow.
