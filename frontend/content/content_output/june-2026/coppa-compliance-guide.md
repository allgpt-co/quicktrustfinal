---
meta_description: "COPPA compliance guide for EdTech, apps, and websites. Covers under-13 data rules, parental consent, data minimization, safe harbor programs."
target_keyword: coppa compliance
secondary_keywords: coppa requirements, children's online privacy, coppa edtech, coppa parental consent, coppa penalties
word_count_target: "1500"
published: true
author: QuickTrust Editorial
last_updated: "2026-03-22"
---

# COPPA Compliance: The Complete Guide to Children's Online Privacy for EdTech, Apps, and Websites

A startup builds a reading app for elementary school students. It collects first names, email addresses, and reading progress. The founders assume they are covered by their school contracts and their standard privacy policy. Then the FTC opens an investigation, and the founders learn that the Children's Online Privacy Protection Act has its own rules, its own enforcement track, and its own penalties -- none of which are waived because the product is educational.

The FTC has brought dozens of COPPA enforcement actions, with the largest fine exceeding $170 million. COPPA is one of the most prescriptive federal privacy laws in the United States, and it applies to a wider range of companies than most founders realize. This guide covers what the law requires, how it interacts with FERPA in educational settings, and how to build a compliance program that protects both children and your business.

---

## What COPPA Covers

The Children's Online Privacy Protection Act (15 U.S.C. 6501-6506) and the FTC's implementing COPPA Rule (16 CFR Part 312) regulate the online collection, use, and disclosure of personal information from children under 13. The law applies to:

**Operators of websites or online services directed to children under 13.** "Directed to children" is determined by the FTC based on subject matter, visual content, animated characters, language, and other indicators. A product does not need to be exclusively for children -- if a portion of the audience is children and the operator knows it, COPPA applies.

**Operators of general audience services with actual knowledge of child users.** If your analytics show under-13 signups, if teachers create accounts for students, or if users self-identify as under 13 during registration, you have actual knowledge.

**Third-party services** collecting personal information from children on behalf of operators are independently responsible under COPPA.

### What Counts as Personal Information

COPPA defines "personal information" more broadly than many operators expect. It includes names, physical and email addresses, phone numbers, Social Security numbers, photographs or audio/video containing a child's image or voice, geolocation sufficient to identify a street and city, and -- critically -- persistent identifiers such as cookies, device IDs, and IP addresses when used for tracking. Many operators believe that not collecting a child's name means they are not collecting personal information. That is incorrect: advertising identifiers and device IDs qualify when used for behavioral advertising.

---

## Verifiable Parental Consent

The core COPPA requirement is verifiable parental consent (VPC) before collecting, using, or disclosing personal information from a child under 13. The consent must be obtained from a parent or legal guardian, and the method must be reasonably calculated to ensure the person providing consent is actually the child's parent.

### Approved Consent Methods

The FTC recognizes several methods for obtaining VPC:

- **Signed consent form.** A parent prints, signs, and returns a consent form by mail, fax, or electronic scan.
- **Credit card or other payment mechanism.** A monetary transaction provides reasonable verification that the consenting party is an adult.
- **Government-issued ID verification.** The parent provides a government-issued ID that is checked against a database and then deleted.
- **Knowledge-based authentication.** The parent answers questions from a database of public records that would be difficult for a child to answer.
- **Email Plus.** For internal use only (not disclosure to third parties), the operator sends a confirmation email to the parent followed by an additional verification step. This method cannot be used when personal information will be disclosed to third parties.

### What Consent Must Cover

The notice to parents must include: the name and contact information of the operator and any third parties collecting information; a description of the personal information collected and how it is used; the operator's practices regarding disclosure to third parties; a statement that the parent can refuse further collection and request deletion; and the specific consent being sought. Parents must also be given the opportunity to consent to collection without consenting to disclosure to third parties.

---

## Data Minimization and Retention

COPPA imposes strict data minimization requirements. Operators may not condition a child's participation in an activity on the child disclosing more personal information than is reasonably necessary for the activity. A reading app cannot require a child's phone number and physical address to create an account if all the app needs is a username and reading level.

Retention rules are equally direct: operators must retain personal information collected from children only as long as reasonably necessary to fulfill the purpose for which the information was collected. After the purpose is fulfilled, the information must be deleted using reasonable measures to protect against unauthorized access during the deletion process.

There is no fixed retention period in COPPA, but the FTC expects operators to define and document their retention schedules and to enforce them. Indefinite retention of children's data is a compliance violation.

---

## Safe Harbor Programs

The FTC has approved several industry self-regulatory programs, known as "safe harbor" programs, under COPPA. Participation in an FTC-approved safe harbor program provides operators with a degree of protection: the safe harbor program, rather than the FTC directly, conducts the initial review and monitoring of the operator's COPPA compliance.

Approved safe harbor programs include CARU (Children's Advertising Review Unit), iKeepSafe, kidSAFE, ESRB (Entertainment Software Rating Board), Aristotle/PRIVO, and TRUSTe/TrustArc.

Safe harbor participation does not immunize an operator from FTC enforcement, but it demonstrates good faith and can reduce enforcement severity. For EdTech companies, iKeepSafe and kidSAFE certifications are particularly relevant because school districts recognize them during procurement evaluation.

---

## COPPA vs. FERPA: The Education Intersection

The interaction between COPPA and FERPA (the Family Educational Rights and Privacy Act) is one of the most common sources of confusion in EdTech compliance.

**FERPA** is a federal law that protects the privacy of student education records. It applies to educational agencies and institutions that receive federal funding -- schools, school districts, and state education departments. FERPA does not directly regulate private companies.

**COPPA** applies to commercial operators that collect personal information from children online.

The key interaction: when a school directs students to use a third-party EdTech service, the school may provide consent on behalf of parents for COPPA purposes, but only when the information is used exclusively for a school-authorized educational purpose. This is the "school official exception."

### How the School Official Exception Works

Under the FTC's guidance, schools can consent to the collection of student personal information by EdTech operators when:

1. The collection is done on behalf of the school for an educational purpose
2. The operator does not use the information for any commercial purpose unrelated to the school context
3. The operator does not disclose the information except back to the school or as directed by the school

This means an EdTech company cannot rely on school consent and then use student data for advertising, product development unrelated to the school purpose, or sale to data brokers. The school consent is narrowly scoped.

**Bottom line for EdTech companies:** You likely need both COPPA compliance and a FERPA-compatible data governance framework. COPPA governs your direct data collection from children. FERPA shapes the contractual and operational requirements schools impose during procurement.

---

## FTC Enforcement and Penalties

COPPA is enforced by the Federal Trade Commission under Section 5 of the FTC Act. State attorneys general also have authority to bring COPPA enforcement actions in federal court.

### Penalty Structure

COPPA violations carry civil penalties of over $50,000 per violation. Each instance of unauthorized collection from a child can constitute a separate violation, which means penalties scale rapidly. Recent FTC settlements have included multi-million dollar fines, requirements to delete all data collected in violation, mandatory comprehensive privacy programs with independent auditing, and multi-year consent decrees with ongoing FTC monitoring.

Beyond direct FTC penalties, COPPA violations create secondary business consequences: loss of school district contracts, removal from app stores (both Apple and Google enforce COPPA compliance for apps in their children's categories), reputational damage, and potential class action litigation.

---

## Building a COPPA Compliance Program

A defensible COPPA compliance program requires the following components:

**1. Audience assessment.** Determine whether your service is directed to children under 13 or whether you have actual knowledge of child users. Document your analysis.

**2. Age screening.** Implement neutral age gates that route users under 13 to a COPPA-compliant experience. The FTC disfavors age gates easily bypassed by entering a false birthdate.

**3. Parental consent mechanism.** Select and implement an FTC-approved VPC method. Document the method and maintain consent records.

**4. Privacy notice.** Publish a children's privacy notice that is separate from your general privacy policy, describing what you collect, how you use it, and how parents can review, delete, or withdraw consent.

**5. Data minimization controls.** Implement technical controls limiting collection to what is necessary. Disable behavioral advertising for child users.

**6. Retention and deletion.** Define retention periods, implement automated deletion, and provide a mechanism for parents to request deletion.

**7. Safe harbor participation.** Consider joining an FTC-approved safe harbor program for independent oversight and procurement advantages in the education market.

**8. Vendor management.** Ensure third-party services that may access children's data are contractually bound to COPPA requirements.

---

## How COPPA Compliance Supports Education Market Entry

School districts are under increasing pressure from parents, state legislatures, and advocacy organizations to vet EdTech vendors rigorously. Forty-five states have enacted student data privacy laws, many of which impose requirements beyond COPPA.

A documented COPPA compliance program -- ideally backed by a safe harbor certification -- is becoming a minimum requirement for EdTech procurement. Districts that adopted standardized data privacy agreements (such as the SDPC National DPA) expect vendors to demonstrate COPPA compliance, define data retention schedules, commit to data minimization, and provide incident notification commitments.

For SaaS companies building for the education market, COPPA compliance is not a regulatory burden to manage around -- it is a market access requirement that, when done well, becomes a competitive advantage.

---

## Where QuickTrust Fits

QuickTrust helps EdTech companies, app developers, and SaaS platforms build COPPA compliance programs that satisfy both FTC requirements and school district procurement standards. The platform maps COPPA requirements to specific controls and policies, identifies gaps in your current program, and provides engineering implementation for technical controls -- age gating, consent management, data minimization, automated retention enforcement, and audit logging. Our team has supported organizations through safe harbor certification processes and FTC compliance reviews, with a 100% audit pass rate across 100+ engagements.

If you are building for children or the education market, a 20-minute readiness call can identify your COPPA exposure and map a path to compliance that supports -- rather than slows -- your go-to-market timeline.
