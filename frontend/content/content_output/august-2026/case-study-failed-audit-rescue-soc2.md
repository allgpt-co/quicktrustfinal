---
meta_description: "Case study: How Relaybase rescued a failed SOC 2 audit — remediating 8 exceptions in 5 weeks after a compliance automation platform showed 94% compliance but produced a qualified opinion."
target_keyword: "soc 2 audit failure, soc 2 remediation, failed soc 2 audit"
secondary_keywords: "soc 2 qualified opinion, compliance automation vs implementation, soc 2 exceptions, soc 2 findings"
word_count_target: 3500
published: true
author: QuickTrust Editorial
last_updated: 2026-02-28
---

# Case Study: How a Series B Startup Rescued a Failed SOC 2 Audit in 5 Weeks — After Their Compliance Platform Showed 94% Compliance

**Company:** Relaybase | **Industry:** Financial Services API Infrastructure | **Stage:** Series B ($15M raised) | **Employees:** 70 | **HQ:** Chicago, IL

**The problem:** A well-known compliance automation platform showed 94% compliance. The auditor issued a qualified opinion with 8 exceptions. Two enterprise customers ($3.4M combined ARR) threatened to leave.

**The outcome:** QuickTrust remediated all 8 exceptions in 5 weeks. Clean SOC 2 Type II report issued. Both customers renewed.

---

## The Situation

Relaybase had been on a tear. Their unified API layer — connecting banks, fintechs, and insurance companies through a single integration point — had found product-market fit in a sector where every new customer means another set of compliance requirements. By the time they closed their Series B at $15 million, Relaybase was processing API calls for 40+ financial institutions, and the board made one thing very clear: SOC 2 Type II was no longer optional. It was table stakes for the enterprise pipeline stacking up behind it.

CTO Damian Brooks took the assignment seriously. He evaluated three compliance approaches: hiring a full-time compliance manager, engaging a consulting firm, or adopting one of the compliance automation platforms that had become ubiquitous in the startup ecosystem. He chose the third option — a well-known compliance automation platform with a $35K/year subscription. The sales pitch was compelling: "SOC 2 in weeks, not months." Automated evidence collection. Continuous monitoring. Policy templates. Auditor-ready reports. The platform had raised hundreds of millions in venture capital and served thousands of companies. It seemed like the obvious choice.

Nine months and $120,000 later (subscription plus professional services add-ons), Relaybase had what looked like a robust compliance program:

- A dashboard showing **94% compliance** across all SOC 2 Trust Service Criteria
- **180+ automated tests** passing on a daily cadence
- **22 policies** auto-generated from the platform's template library
- Integrations with AWS, GitHub, Okta, and a dozen other services pulling evidence automatically
- A compliance posture that, on screen, looked healthy, organized, and auditor-ready

Damian felt good. The board was satisfied. Relaybase engaged a reputable mid-tier CPA firm to conduct the SOC 2 Type II audit.

The auditor began fieldwork on a Monday. By Wednesday, the lead auditor had flagged serious problems. By Friday, she had a list of eight exceptions that would result in a qualified opinion.

### The 8 Exceptions

**Exception 1: Access reviews were scheduled but never executed.** The compliance platform had configured quarterly access review reminders. The reminders fired on schedule — every 90 days, a notification appeared in the platform's dashboard. Nobody at Relaybase actually performed the reviews. No attestation records existed. No manager had ever signed off on who had access to what. When the auditor pulled the access list for the production database, she found three former contractors who still had active credentials more than four months after their contracts had been terminated. One of those contractors had last logged in two months after leaving. The compliance platform marked access reviews as "configured." The auditor asked for evidence that reviews had been "performed." Those are two fundamentally different things.

**Exception 2: Encryption key rotation was enabled but broken.** AWS KMS key rotation was configured — the compliance platform detected the configuration flag and marked the control as "compliant" with a green checkmark. What nobody knew: the rotation had silently failed six months ago due to a dependency on a deprecated AWS API call. No alert was configured for rotation failure. No one had checked whether rotation was actually occurring. The same encryption key had been in use for 11 months. The compliance platform tested: "Is key rotation enabled in configuration?" The auditor tested: "Show me the rotation log. When was the last successful rotation?" The answer was damning.

**Exception 3: Log monitoring existed on paper — nobody was watching.** AWS CloudTrail was enabled. Logs were being written to an S3 bucket. The compliance platform verified that CloudTrail was active and that logs were being stored, and marked logging as "compliant." But there was no SIEM. No alerting rules. No monitoring dashboards. No one at Relaybase had ever reviewed a single log entry. The logs were write-only — a black hole of security data that nobody had ever looked at. When the auditor asked, "Show me the last three security alerts generated from your log monitoring and how each was investigated and resolved," there was silence. There were zero alerts. Not because nothing suspicious had happened, but because no one was watching.

**Exception 4: Incident response plan was written but never tested.** The compliance platform had auto-generated an incident response plan from its template library. The document existed. It had a title page, a table of contents, escalation procedures, and communication templates. It had never been reviewed by anyone at Relaybase. It had never been customized for Relaybase's actual architecture or team structure. It had never been tested. When the auditor asked the on-call engineer to walk through the incident response process, the engineer said he had never seen the document. He didn't know it existed. A plan that nobody knows about is not a plan.

**Exception 5: Change management was documented but not enforced.** The policy — auto-generated by the compliance platform — stated that all production changes require peer review and approval before deployment. In practice, GitHub branch protection was not enabled on the main branch. Developers were pushing directly to production on a regular basis — the auditor found direct pushes happening weekly. The compliance platform verified that a change management policy existed as a document. It did not verify that the policy was enforced in the actual deployment pipeline. It checked for the existence of words on a page, not the enforcement of rules in code.

**Exception 6: Vendor management inventory was incomplete, assessments were missing.** The compliance platform tracked 12 vendors — the ones that had been manually entered during initial setup. Relaybase actually used 28 third-party services that touched, processed, or stored customer data. Sixteen vendors were completely untracked and unassessed. Three of those vendors had no SOC 2 report, no ISO 27001 certification, and no equivalent assurance documentation of any kind. The compliance platform managed the vendors you told it about. It had no way of knowing about the vendors you forgot.

**Exception 7: Policies referenced decommissioned systems.** Three of the 22 auto-generated policies referenced systems that Relaybase had decommissioned six months earlier — a CI/CD tool they had migrated away from, a legacy monitoring service they had replaced, and an SSO provider they had swapped out. The policies described controls for systems that no longer existed. Nobody had updated the policies because nobody had read them. The compliance platform generated policies at setup. It did not track whether the systems those policies described were still in use.

**Exception 8: Security awareness training records showed completion, but employees did not recall completing it.** The compliance platform recorded that 100% of employees had completed security awareness training. When the auditor interviewed three randomly selected employees, none of them recalled completing any security training. The investigation revealed that the "training" was a single-page acknowledgment form embedded in the employee onboarding flow — a checkbox that most employees clicked through without reading the content above it. The compliance platform counted a checkbox click as "training completed." The auditor counted it as no training at all.

### The Qualified Opinion

The auditor issued a **qualified opinion** — a SOC 2 Type II report with eight exceptions explicitly documented. In SOC 2 terms, a qualified opinion is a failing grade. The report told every customer and prospect that read it: Relaybase's controls were designed but did not operate effectively during the observation period.

> "I stared at the audit report and then stared at our compliance dashboard showing 94%. The dashboard was checking whether controls were configured. The auditor was checking whether controls actually worked. Those are completely different things."
>
> — **Damian Brooks, CTO, Relaybase**

The consequences arrived fast. Within two weeks, two enterprise customers sent formal remediation notices:

- **Meridian Financial** ($2.1M ARR) — a regional banking consortium that routed API traffic for 12 member banks through Relaybase
- **Atlantic Insurance Group** ($1.3M ARR) — a commercial insurance carrier that used Relaybase for claims data exchange

Both notices carried the same terms: produce a clean SOC 2 report within 90 days, or they would begin vendor transition proceedings.

Combined, those two customers represented **$3.4 million in annual recurring revenue** — nearly a third of Relaybase's total ARR.

> "We spent $120K and nine months on compliance automation. We got a qualified opinion and two customers threatening to leave. That's not a compliance program. That's an expensive false sense of security."
>
> — **Vanessa Reyes, CEO, Relaybase**

---

## The Challenge

The situation facing Relaybase was worse than a typical first-time SOC 2 engagement. Companies that have never been audited start from zero — there is no expectation to meet, no failed report on file, and no damaged relationship with an auditor. Relaybase had all three.

**The 90-day clock was non-negotiable.** Meridian Financial and Atlantic Insurance Group had issued formal remediation notices with explicit timelines. These were not friendly suggestions. Both customers had legal teams involved. Both had begun preliminary conversations with alternative API providers. Ninety days was the hard deadline, and some of that time had already elapsed by the time Relaybase fully grasped the severity of the situation.

**The 8 exceptions were not policy gaps — they were implementation gaps.** This distinction matters enormously. If Relaybase had been missing policies, the fix would be straightforward: write the policies. But the policies existed. The controls were configured. The automation was running. The gap was between "configured" and "functioning" — between a control that exists on a dashboard and a control that actually works in the real environment. This is a harder problem to solve because it requires engineering work, not document work.

**Trust with the auditor was damaged.** The CPA firm had conducted fieldwork expecting to find a well-run compliance program — Relaybase had presented the 94% compliance dashboard as evidence of readiness. Instead, the auditor found eight material exceptions. The lead auditor told Relaybase directly: any remediation would be scrutinized more carefully than a first-time engagement. They would need to see not just evidence that controls were fixed, but evidence that controls had been operating effectively over a sustained observation period. The bar was higher now.

**The engineering team was demoralized.** Relaybase's 14-person engineering team had spent months feeding the compliance platform — connecting integrations, answering questionnaires, reviewing auto-generated policies. They had done everything the platform told them to do. The qualified opinion felt like a betrayal. Several engineers expressed frustration that they had been set up to fail by a tool that told them they were succeeding. Morale was a real problem, and any remediation effort would need to bring the engineering team along rather than impose more compliance burden on people who had lost faith in the process.

**The timeline math was brutal.** Relaybase needed to: remediate all 8 exceptions, demonstrate that remediated controls were operating effectively over an observation period, and have the auditor re-examine and issue a clean report — all within 90 days. A typical SOC 2 observation period is 6 to 12 months. Even an abbreviated re-observation would need at least 6 weeks. That left roughly 5 weeks for actual remediation work, with zero margin for error.

**The compliance platform was still running.** Perhaps the most surreal detail: throughout all of this, the compliance automation platform's dashboard still showed 94% compliance. Every automated test was still passing. Every control was still marked green. The platform had no idea that the audit had failed. It was monitoring configuration, not reality, and by that measure, everything was fine.

---

## Why QuickTrust

Relaybase evaluated three paths forward:

**Option 1: The compliance platform's professional services team.** The platform vendor offered a "remediation support" package — advisory calls with their compliance team to help Relaybase address the exceptions. But this was still advisory, not implementation. Relaybase would receive guidance on what to fix; their own engineers would still need to do the fixing. And the platform's automated test suite — the same test suite that had marked all 8 exception areas as "compliant" — had already proven it could not detect the types of implementation gaps the auditor found. Trusting the same tool to guide the remediation felt like asking the broken compass for better directions.

**Option 2: An independent compliance consultant.** Relaybase received a proposal from a boutique compliance consulting firm: 12-week engagement, advisory scope, deliverables including remediation plans and policy rewrites. The consultant would tell Relaybase what to fix. Relaybase's engineers would implement. This was better than Option 1, but the 12-week timeline blew past the 90-day deadline before the observation period even started. And "advisory only" meant the same demoralized engineering team would carry the implementation load.

**Option 3: QuickTrust.** QuickTrust was the only option that offered direct implementation — engineers who would fix the actual controls, not consultants who would write reports about what needed fixing. QuickTrust's initial assessment took two days: they reviewed all 8 exceptions against the auditor's specific findings, identified root causes for each failure, and presented a 5-week remediation plan with week-by-week milestones and deliverables.

The deciding moment came during the initial assessment. QuickTrust's lead engineer asked Relaybase's team to show them the last CloudTrail alert that had been generated, triaged, and investigated. The room went silent.

"That's the difference between compliance automation and compliance implementation," the engineer said. "The platform checks if CloudTrail is on. We check if anyone is watching."

Relaybase signed with QuickTrust that week.

---

## Implementation: The 5-Week Remediation

### Week 1: Root Cause Analysis and Priority Triage

QuickTrust began by reviewing all 8 exceptions in detail — not from the compliance platform's dashboard, but from the auditor's actual findings. Each exception was categorized by failure type:

- **Control exists but does not function** (3 exceptions): Access reviews, encryption key rotation, log monitoring. These controls were configured in the environment but had never operated as intended. The automation detected the configuration; the auditor detected the non-operation.
- **Control exists on paper but is not enforced** (3 exceptions): Incident response plan, change management, security awareness training. Policies described these controls. The environment did not enforce them.
- **Incomplete scope** (2 exceptions): Vendor management, stale policies. The controls worked for what they covered — they just didn't cover enough.

Priority was set by active risk, not audit sequence. Access review was first — three former contractors with active production database credentials represented an immediate security exposure, not just a compliance finding. QuickTrust revoked those three accounts within two hours of engagement start. That was not a compliance remediation. That was incident response.

### Week 2: Access Review, Key Rotation, and Log Monitoring

**Access review remediation.** QuickTrust implemented an automated quarterly access review workflow through Okta. But unlike the compliance platform's approach — which had simply configured a reminder — the new workflow required action. Every access record required explicit manager sign-off with a timestamp. Reviews that were not completed within 5 business days escalated to the VP of Engineering. Most critically, QuickTrust built a reconciliation check: the Okta access list was automatically cross-referenced with the HR system's active employee roster. Any mismatch — an account without a corresponding active employee — triggered an immediate alert. The first review under the new system discovered 3 additional orphaned accounts beyond the 3 former contractors already revoked, bringing the total to 6 accounts that should not have existed.

**Encryption key rotation remediation.** QuickTrust diagnosed the root cause of the rotation failure: a dependency on a deprecated AWS API call that had begun returning errors silently six months prior. The fix involved migrating to the current AWS KMS API version and re-establishing the rotation schedule across all 4 KMS keys in use. QuickTrust configured a CloudWatch alarm to fire on any rotation failure — the monitoring gap that had allowed the original failure to go undetected for half a year. Rotation was tested and verified across all keys, with rotation logs confirmed going back 30 days from remediation.

**Log monitoring remediation.** This was the most significant infrastructure addition. QuickTrust deployed Datadog as a SIEM with 34 detection rules specifically tuned for Relaybase's environment. The rules covered: root account usage, failed authentication attempts exceeding 5 in a 10-minute window, IAM policy changes, S3 bucket policy modifications, security group changes, KMS key deletion attempts, and CloudTrail tampering. Each detection rule had a defined escalation path through PagerDuty with assigned on-call responders. The first real alert triggered within 48 hours of deployment — a developer had used root credentials for a test environment. This was exactly the type of event that should be caught, investigated, and documented. It was investigated, documented, and resolved within 30 minutes. The system worked.

### Week 3: Change Management, Incident Response, and Vendor Management

**Change management remediation.** QuickTrust enabled GitHub branch protection on the main branch and all production-deployment branches. The rules were explicit: all merges require a pull request with at least one reviewer approval. Direct pushes to production were blocked at the repository level — not by policy, by enforcement. A GitHub webhook was configured to log all merge events to a dedicated evidence repository, creating an auditable record of every production change, who approved it, and when. QuickTrust reviewed the last 30 days of Git history and identified 12 direct pushes to production that would have been caught under the new enforcement — a finding that underscored how wide the gap between policy and practice had been.

**Incident response remediation.** The auto-generated template was discarded. QuickTrust rewrote the incident response plan from scratch, customized for Relaybase's actual architecture: their AWS infrastructure, their API gateway, their database topology, their on-call rotation, their Slack channels, their customer communication procedures. The plan was a living document that described real systems and real people, not a generic template that described theoretical processes. QuickTrust then conducted a 2-hour tabletop exercise with the engineering team, simulating a data breach scenario involving unauthorized access to the production database via a compromised API key. The exercise was documented with timestamps, decisions made at each stage, escalation actions taken, and lessons learned. Three process gaps were identified during the exercise and incorporated into the plan before it was finalized.

**Vendor management remediation.** QuickTrust expanded the vendor inventory from 12 to 28 — every third-party service that touched, processed, stored, or had access to customer data. Each of the 28 vendors was assessed: SOC 2 report status, ISO 27001 certification, data processing agreements, subprocessor lists, and breach notification terms. Three vendors had no assurance documentation of any kind. One was non-critical and Relaybase initiated replacement. The other two had SOC 2 audits in progress; QuickTrust obtained bridge letters from both confirming their audit timelines and interim control postures. All 28 vendor assessments were documented with risk ratings and filed in the evidence repository.

### Week 4: Policy Refresh, Training, and Evidence Collection

**Policy refresh.** QuickTrust reviewed all 22 policies line by line with Relaybase's engineering leadership. References to 3 decommissioned systems were removed. References to 4 new systems deployed in the past year were added. Ownership was assigned — every policy now had a named owner responsible for annual review and ad-hoc updates when systems changed. Review dates were set. A policy review cadence was established: annual full review, with mandatory ad-hoc updates triggered by any system migration, decommission, or new service adoption. The policies were no longer auto-generated documents that nobody read. They were operational documents that described real controls in real systems, owned by real people.

**Security awareness training.** The single-page acknowledgment form was eliminated. QuickTrust helped Relaybase implement a genuine security awareness training program: a 45-minute interactive session covering phishing recognition, password hygiene and credential management, incident reporting procedures, data handling and classification, and social engineering awareness. Completion was tracked not by checkbox but by quiz — every employee had to pass a 20-question assessment with a minimum score of 80%. Employees who scored below 80% retook the training. One hundred percent of Relaybase's 70 employees completed the training within 5 business days. Training records included individual quiz scores, completion timestamps, and the specific training version completed. When the auditor asked employees about their training, they would have something to recall.

**Evidence collection.** QuickTrust compiled a comprehensive evidence package for all 8 remediations. Each exception was mapped to four elements: the root cause of the original failure, the specific remediation action taken, the evidence demonstrating the remediation was effective, and the ongoing monitoring mechanism that would prevent recurrence. This was not a spreadsheet. It was an evidence repository with timestamped artifacts, screenshots, configuration exports, log samples, and attestation records — everything the auditor would need to verify that each control was not just fixed but functioning.

### Week 5: Auditor Re-engagement and Observation Period Planning

QuickTrust presented the complete remediation evidence package to the CPA firm. The lead auditor reviewed each of the 8 exceptions against the remediation documentation. Every exception was addressed. Every root cause was identified and resolved. Every control had evidence of operation, not just configuration.

The auditor agreed to a 6-week re-observation period, starting from Week 3 of the remediation — the point at which most controls had become operational. This meant the observation period would run concurrently with the final weeks of remediation and continue for several weeks after.

During the 6-week re-observation period, the results were definitive:

- **Zero control failures** across all 8 remediated areas
- **All automated monitoring operational** with documented alert-and-response cycles
- **3 quarterly access reviews** completed with full attestation records
- **2 security alerts** properly investigated, documented, and resolved through the incident response process
- **14 production changes** deployed through the enforced pull request workflow with reviewer approvals logged

---

## The Results

The numbers tell the story:

- **All 8 exceptions remediated** within the 5-week remediation window
- **Clean (unqualified) SOC 2 Type II report** issued by the CPA firm following the 6-week re-observation period
- **6 orphaned accounts discovered and revoked** — 3 former contractors identified by the auditor, plus 3 additional accounts discovered during the first access review reconciliation
- **Security monitoring: from zero to operational** — 34 detection rules deployed, 47 alerts generated, investigated, and documented during the re-observation period
- **Change management: zero unauthorized deployments** — no direct pushes to production since branch protection was enabled
- **Vendor coverage: 133% increase** — inventory expanded from 12 tracked vendors to 28, all assessed with documented risk ratings
- **Training: 100% completion with verified comprehension** — every employee passed the quiz-based training program
- **Enterprise customers retained:** Both Meridian Financial ($2.1M ARR) and Atlantic Insurance Group ($1.3M ARR) received the clean report, withdrew their remediation notices, and renewed their contracts
- **$3.4 million in ARR preserved** that was actively at risk of churn
- **Total QuickTrust engagement cost:** Less than half of what Relaybase had already spent on the compliance automation platform over 9 months
- **Compliance platform subscription:** Canceled. Relaybase transitioned to QuickTrust's continuous monitoring program

> "The compliance platform told us we were compliant. The auditor told us we weren't. QuickTrust didn't tell us anything — they fixed the actual controls. That's the difference between a dashboard and an engineer."
>
> — **Damian Brooks, CTO, Relaybase**

> "We learned the most expensive lesson in compliance: software doesn't make you compliant. Implementation makes you compliant. A green dashboard means nothing if the controls behind it don't actually work. We won't make that mistake again."
>
> — **Vanessa Reyes, CEO, Relaybase**

> "When I joined Relaybase, I audited the compliance platform's test suite. It had 180 automated checks. Not a single one verified that a human had actually performed an action. It checked configurations, not operations. That's the fundamental gap that automation alone can't close."
>
> — **Kwame Asante, Head of Security, Relaybase** (hired post-engagement)

---

## Key Lessons

**Compliance automation platforms check configuration, not operation.** "Is CloudTrail enabled?" is a fundamentally different question from "Is anyone watching the logs?" Automation platforms are excellent at answering the first question. Auditors ask the second. The gap between these two questions is where SOC 2 audits fail.

**A 94% compliance score and a qualified opinion can coexist.** This is not a contradiction — it is the result of measuring two different things. The compliance platform measured control configuration. The auditor measured control effectiveness. Both measurements were accurate within their own frame. The problem is that only one of them matters to the person reading your SOC 2 report.

**The gap between "control exists" and "control works" is where audits fail.** Policies existed. Configurations were set. Automated tests were passing. But access reviews were not being performed. Key rotation was silently failing. Logs were unmonitored. Implementation — the work of making controls actually function in the real environment — is what bridges this gap. No amount of configuration monitoring can replace it.

**Auto-generated policies that nobody reads are worse than no policies.** If Relaybase had no policies, the auditor would have found a control design gap — a clear finding with a clear fix. Instead, the auditor found policies that described controls that did not operate as described. This is a more serious finding because it suggests either negligence or misrepresentation. Policies that accurately describe your environment are valuable. Policies auto-generated from templates and never reviewed are a liability.

**Access reviews that are scheduled but never executed are the most common SOC 2 finding.** Across all SOC 2 audits, this is the exception that appears most frequently. Automation can schedule the review. Automation can send the reminder. Automation can even pull the access list. But a human has to actually look at it, verify it, and attest to it. If that human action does not happen, the control has not operated — regardless of what the dashboard shows.

**The cost of remediation after a failed audit is often less than the original investment — but the real cost is reputational.** QuickTrust's 5-week engagement cost less than half of what Relaybase spent on the compliance platform over 9 months. The financial comparison is striking but incomplete. The real cost of the failed audit was the 90-day remediation notices from customers representing $3.4M in ARR, the damaged relationship with their auditor, the demoralized engineering team, and the months of lost time operating under a false sense of security.

---

## What's Next for Relaybase

Relaybase is now on QuickTrust's Continuous Compliance Program. Controls are monitored for operation, not just configuration. Access reviews are performed and attested. Alerts are investigated and documented. Policies are reviewed and updated when systems change.

CTO Damian Brooks now presents compliance metrics to the board quarterly — not dashboard screenshots, but operational metrics: alerts investigated, access reviews completed, changes deployed through approved workflows, vendor assessments current.

Relaybase is also pursuing **PCI DSS certification** to expand into payment processing APIs, a natural extension of their financial services platform. QuickTrust is managing that engagement from day one — no automation-only phase, no gap between configuration and implementation.

---

> **Don't confuse compliance software with compliance.**
>
> If your dashboard says you're compliant but your controls don't actually work, QuickTrust engineers will fix the implementation — not just the spreadsheet.
>
> **[Get a real compliance assessment → quicktrustapp.com](https://quicktrustapp.com)**
