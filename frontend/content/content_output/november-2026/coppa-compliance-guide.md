---
meta_description: "Complete COPPA compliance guide for EdTech and app developers. Learn parental consent requirements, safe harbor programs, FTC enforcement, and how COPPA works alongside FERPA."
target_keyword: "coppa compliance"
secondary_keywords: "COPPA requirements, children's online privacy, COPPA safe harbor, COPPA parental consent, COPPA for apps, COPPA FTC"
word_count_target: 4000+
published: true
author: QuickTrust Editorial
last_updated: 2026-03-21
---

# COPPA Compliance: The Complete Guide to Children's Online Privacy for EdTech, Apps, and Websites

In December 2022, the Federal Trade Commission announced a $520 million settlement with Epic Games -- the largest COPPA enforcement action in history. The FTC alleged that Epic, the maker of Fortnite, violated the Children's Online Privacy Protection Act by collecting personal information from children under 13 without parental consent, using manipulative design patterns to encourage purchases, and enabling voice and text chat that exposed children to harmful interactions by default.

$520 million. For a company that knew children were its primary audience and chose not to build adequate consent mechanisms.

Epic Games is not an outlier. In the five years preceding that settlement, the FTC brought COPPA enforcement actions against TikTok ($5.7 million in 2019, followed by additional actions), Google and YouTube ($170 million), Zoom ($85 million for COPPA-adjacent children's privacy violations), and dozens of smaller companies operating apps, websites, and online services used by children. The FTC has made children's privacy its top enforcement priority -- and the 2024 and 2025 rule updates have expanded what COPPA covers, tightened what consent requires, and increased what non-compliance costs.

If you build, operate, or distribute a website, app, or online service that is directed at children under 13 -- or if you have actual knowledge that children under 13 use your product -- COPPA compliance is not a future consideration. It is a current legal obligation with civil penalties of up to $53,088 per violation, no cap on aggregate penalties, and an FTC that is actively investigating and prosecuting violations at an unprecedented pace.

This guide covers everything technology companies, EdTech vendors, app developers, and online service operators need to know about COPPA compliance in 2026: what the law requires, who must comply, how to obtain verifiable parental consent, how COPPA works in the education context alongside FERPA, what safe harbor programs offer, how to implement COPPA technically, and what the FTC's recent rule changes mean for your product.

---

## What Is COPPA? (Children's Online Privacy Protection Act)

COPPA -- the Children's Online Privacy Protection Act -- is a federal law enacted in 1998 that regulates the online collection, use, and disclosure of personal information from children under 13 years of age. It is codified at 15 U.S.C. Sections 6501-6506, with implementing regulations -- the COPPA Rule -- at 16 CFR Part 312. The FTC administers and enforces the COPPA Rule.

### The purpose behind COPPA

Congress passed COPPA in recognition of a specific problem: the internet was rapidly becoming a primary environment for children, and website operators were collecting vast amounts of personal information from young users -- often without any parental knowledge or involvement. Children lack the cognitive development to understand privacy disclosures, evaluate the consequences of sharing personal information, or resist persuasive design techniques that encourage data sharing. COPPA was designed to put parents in control of what information is collected from their children online.

The law does not prohibit children from using the internet. It does not ban websites from serving children. What it does is require that operators of websites and online services directed at children -- or that have actual knowledge of child users -- provide transparent notice of their data practices and obtain verifiable parental consent before collecting personal information from children under 13.

### A brief history of COPPA and its evolution

COPPA was signed into law on October 21, 1998, and the first COPPA Rule took effect on April 21, 2000. The original rule was crafted for the desktop web era -- a time when "websites" were the dominant form of online interaction and mobile apps did not exist.

Key milestones in COPPA's evolution:

- **2000:** The original COPPA Rule takes effect, establishing requirements for website operators.
- **2013:** The FTC issued a major update to the COPPA Rule, expanding the definition of "personal information" to include persistent identifiers (cookies, device IDs), photographs, video, audio recordings, and geolocation information. The 2013 update also extended COPPA's reach to cover mobile apps, connected toys, and third-party plug-ins and ad networks operating on child-directed sites.
- **2024-2025:** The FTC finalized significant amendments to the COPPA Rule addressing biometric data, push notifications as a form of contact, strengthened data retention and deletion requirements, limitations on targeted advertising to children, and new requirements around consent mechanisms. These updates represent the most substantial changes to COPPA since the 2013 overhaul.

### Who does COPPA protect?

COPPA protects children under the age of 13. This is a bright-line rule -- there is no sliding scale, no "teen" category, and no exceptions based on maturity or parental preferences. If a user is under 13, COPPA applies. The age threshold was chosen by Congress based on developmental research suggesting that children under 13 generally lack the capacity to understand the implications of sharing personal information with commercial entities.

The FTC has consistently rejected arguments that COPPA's age threshold is outdated or that it should be raised or lowered. The under-13 standard remains in effect, and the FTC has demonstrated through enforcement actions that it will hold operators accountable for collecting information from users they know or should know are under 13.

---

## Who Must Comply with COPPA?

COPPA's compliance obligations fall on "operators" -- but the definition of operator under COPPA is broader than most companies realize.

### Operators of websites or online services directed to children

If your website, app, or online service is "directed to children" under 13, you must comply with COPPA. The FTC considers the totality of circumstances to determine whether a site or service is child-directed, including:

- **Subject matter:** Is the content designed for or primarily appealing to children (games, cartoons, educational activities for young learners)?
- **Visual content:** Does the site use child-oriented characters, activities, animations, or design elements?
- **Music and audio:** Does the service use music or audio content designed to appeal to children?
- **Age of models:** Does the site feature child models or characters?
- **Presence of child celebrities or characters:** Does the service feature celebrities or characters known to appeal to children?
- **Language:** Is the language used on the site aimed at children?
- **Advertising:** Is the site advertised on children's programming or in media directed to children?
- **Empirical evidence:** Does the operator have evidence (analytics, surveys, user research) showing that a significant portion of the audience is under 13?

The FTC has emphasized that a site does not need to be exclusively designed for children to be considered child-directed. A site that targets a general audience but has a disproportionate number of child users -- and the operator knows this -- can be subject to COPPA.

### Operators with actual knowledge of child users

Even if your service is not "directed to children," COPPA applies if you have **actual knowledge** that you are collecting personal information from a child under 13. Actual knowledge can come from many sources: a user stating their age during registration, a parent contacting you about their child's account, a teacher telling you that students under 13 are using the product, or any other information that would make a reasonable person aware that a specific user is under 13.

The "actual knowledge" standard is critical for general-audience platforms. Social media platforms, communication apps, and online marketplaces that are not directed at children can still trigger COPPA obligations when they learn that specific users are under 13.

### Third-party operators and advertising networks

COPPA also applies to third parties -- including advertising networks, analytics providers, and plug-in operators -- that collect personal information through child-directed sites or services. If you operate an ad network that places tracking technology on a child-directed website, you have independent COPPA obligations even if the website operator is the one who invited you onto the page.

This is a significant compliance risk for the advertising and analytics ecosystem. The FTC's 2013 rule update made clear that third-party trackers cannot avoid COPPA by claiming ignorance of the child-directed nature of the sites on which they operate.

### How COPPA applies to app developers

Mobile apps are explicitly covered by COPPA. If you publish an app in a category marketed to children (such as the "Kids" section of the Apple App Store or Google Play), integrate SDKs or advertising networks that collect persistent identifiers, or have actual knowledge that users are under 13, COPPA applies to your app. The FTC has brought enforcement actions against app developers of all sizes -- from major studios to individual developers -- for failing to comply.

---

## What COPPA Requires: The 6 Core Obligations

COPPA and the COPPA Rule impose six core obligations on covered operators. Each is a substantive requirement, not a suggestion.

### 1. Post a clear, comprehensive privacy policy

Every covered operator must post a privacy policy on its website or within its app that describes:

- All personal information the operator collects from children, including the types of information and whether collection is active (provided by the child) or passive (collected through cookies, device IDs, or analytics)
- How the operator uses the information collected
- Whether the operator discloses personal information to third parties and, if so, the types of businesses to which disclosures are made and the purposes of those disclosures
- The parent's rights to review, delete, and refuse further collection of their child's information
- The name and contact information of all operators collecting or maintaining personal information through the site or service

The privacy policy must be clearly and prominently displayed -- directly linked from every page of the site or accessible from within the app before any data collection occurs. The FTC has emphasized that the policy must be written in language a reasonable parent can understand, not buried in legal jargon or combined with a general terms-of-service document.

### 2. Provide direct notice to parents

Before collecting personal information from a child, the operator must provide direct notice to the parent describing:

- The operator's information collection, use, and disclosure practices
- That the operator seeks parental consent for the collection, use, or disclosure of the child's personal information
- That the parent can consent to collection without consenting to disclosure to third parties
- The specific personal information the operator intends to collect and the purposes for which it will be used
- A means by which the parent can provide consent

The notice must be sent directly to the parent -- not simply posted on the website. The FTC has approved email as the primary mechanism for direct parental notice, but the content must be substantive and specific.

### 3. Obtain verifiable parental consent

This is the centerpiece of COPPA. Before collecting, using, or disclosing personal information from a child under 13, the operator must obtain **verifiable parental consent (VPC)**. The consent must be obtained from the parent, not from the child. The consent mechanism must be reasonably calculated, in light of available technology, to ensure that the person providing consent is the child's parent.

The FTC has approved several specific methods for verifiable parental consent, detailed in the next section of this guide.

### 4. Minimize data collection

Operators may not condition a child's participation in a game, the offering of a prize, or any other activity on the child disclosing more personal information than is reasonably necessary to participate in that activity. This is a data minimization requirement -- you can only collect what you actually need for the specific service the child is using.

This requirement has become increasingly important as the FTC focuses on design patterns that encourage excessive data collection from children. The principle is straightforward: if a child is playing a puzzle game, the game should not require the child to provide a street address, phone number, or photograph.

### 5. Implement reasonable data security

Operators must establish and maintain reasonable procedures to protect the confidentiality, security, and integrity of personal information collected from children. The FTC evaluates the adequacy of security measures based on the sensitivity of the data, the size and complexity of the operator's business, and the cost of available tools to improve security.

The security obligation is not prescriptive -- the COPPA Rule does not mandate specific technical controls like TLS 1.3 or AES-256 encryption. Instead, the FTC applies a reasonableness standard. However, enforcement actions have made clear that the FTC expects at least: encryption of children's personal information both in transit and at rest, access controls limiting employee access to children's data, regular security assessments, and an incident response capability. For companies seeking guidance on what "reasonable security" means in practice, the controls documented in frameworks like [SOC 2](/content/march-2026/pillar-soc2-complete-guide) provide a defensible benchmark.

### 6. Honor deletion rights and data retention limits

Parents have the right to request that the operator delete their child's personal information. The operator must honor that request. Additionally, operators must retain children's personal information only as long as is reasonably necessary to fulfill the purpose for which it was collected. Once the purpose is fulfilled, the information must be deleted using reasonable measures to protect against unauthorized access or use.

The FTC's 2024-2025 rule updates strengthened the retention and deletion requirements, making clear that operators cannot retain children's data indefinitely for analytics, product improvement, or future marketing purposes. A robust [data retention policy](/content/november-2026/data-retention-policy-guide) is essential for demonstrating compliance with this obligation.

---

## Verifiable Parental Consent Methods

The FTC has recognized that no single consent mechanism is perfect, and it has approved multiple methods for obtaining verifiable parental consent. The FTC periodically reviews and updates the list of approved methods as technology evolves.

### FTC-approved consent methods

As of 2026, the following methods are approved by the FTC for obtaining verifiable parental consent:

**Signed consent form.** The operator provides a consent form that the parent prints, signs, and returns via mail, fax, or electronic scan. This is the most traditional method and is straightforward to implement, but it introduces friction and delays that can significantly impact conversion rates.

**Credit card, debit card, or other online payment transaction.** The operator requires the parent to use a credit card, debit card, or other online payment mechanism in connection with a monetary transaction (such as a purchase, subscription, or fee). The logic is that children generally do not have access to credit cards, and the transaction itself provides a reasonable verification that an adult is involved. Note that simply requesting a credit card number without processing a transaction does not satisfy this requirement.

**Toll-free telephone number or video conference.** The operator provides a toll-free telephone number or video conference mechanism through which a parent can call or connect to provide consent. This allows the operator to verify parental identity through a real-time conversation. Video conferencing has become increasingly accepted, particularly for higher-risk data collection activities.

**Government-issued identification check.** The operator can verify parental identity by checking the parent's government-issued identification against a database, provided the identification is deleted promptly after verification. This method has grown more practical as identity verification services have matured.

**Knowledge-based authentication (KBA).** The operator asks the parent a series of questions that only the parent would be able to answer, drawn from commercially available databases (such as credit history or public records). This method must use questions that a child would be unlikely to answer correctly.

**Facial recognition comparison.** With appropriate privacy safeguards, an operator may use facial recognition to compare a photo provided by the parent with a photo on the parent's government-issued ID, then promptly delete both images after verification.

**Email plus (for limited internal use).** For operators that will use the child's personal information only internally -- not disclosing it to third parties -- the FTC permits a lower-friction "email plus" method. The operator sends an email to the parent describing the information to be collected and how it will be used, and the parent provides consent by return email. The operator must then take an additional confirming step (such as sending a delayed confirmatory email, requiring the parent to respond to a confirmation message, or calling the parent at a phone number provided) to ensure the initial consent was legitimate. This method is not sufficient if the operator intends to share the child's data with third parties.

### Choosing the right consent method

The appropriate consent method depends on several factors: the sensitivity of the data being collected, whether data will be shared with third parties, the risk profile of your service, and the user experience requirements of your product.

For most EdTech and app companies, the email-plus method provides the best balance of compliance and usability for internal-use-only data. For services that share data with third parties or collect sensitive information (biometric data, precise geolocation, photographs), the FTC expects a higher-assurance consent method such as credit card verification, video call, or government ID check.

---

## COPPA and EdTech: The School Consent Exception

For EdTech companies, COPPA includes a critically important provision: the **school consent exception**. This exception allows schools to consent to the collection of children's personal information on behalf of parents -- but only under specific conditions.

### How the school consent exception works

Under the COPPA Rule, schools may act as agents of parents and provide consent for the collection of children's personal information when the following conditions are met:

1. **The data is collected solely for school-authorized educational purposes.** The EdTech operator can only collect student data for the educational purpose that the school has authorized. The data cannot be used for commercial purposes, targeted advertising, or building user profiles for non-educational use.
2. **The school has authorized the collection.** The school (not the individual teacher, unless the teacher has been authorized by the school to make such decisions) must affirmatively authorize the EdTech operator to collect student data for the specified educational purpose.
3. **The operator does not use the data for any other commercial purpose.** This is the constraint that catches many EdTech companies. If you collect student data under the school consent exception, you cannot use that data to market other products to the student or the student's family, build advertising profiles, sell the data to third parties, or use it for product development purposes unrelated to the educational service the school authorized.

### What the school consent exception does not provide

The school consent exception is narrower than many EdTech companies assume:

- **It does not eliminate COPPA obligations entirely.** The operator must still comply with the privacy policy requirement, the data minimization requirement, the security requirement, and the deletion requirement. The school consent exception only substitutes the school's consent for individual parental consent -- it does not waive the other five COPPA obligations.
- **It does not allow commercial use of student data.** Even with school consent, the operator is strictly prohibited from using student data for commercial purposes beyond the educational service authorized by the school.
- **It does not apply to after-hours or personal use.** If a student uses the EdTech product outside of school for personal purposes (for example, using a game-based learning app at home for entertainment), the school consent may not cover that use. The operator may need independent parental consent for non-school-authorized activities.
- **It does not transfer liability to the school.** The EdTech operator retains independent responsibility for COPPA compliance. If you violate COPPA while operating under the school consent exception, the FTC will hold you -- the operator -- accountable.

### Best practices for the school consent exception

EdTech companies relying on the school consent exception should:

- Obtain written authorization from the school specifying the educational purpose and the data to be collected
- Maintain clear documentation separating school-authorized data collection from any general-audience features
- Implement technical controls that prevent school-authorized data from being used for non-educational purposes
- Provide schools with the ability to review and delete student data
- Include school consent provisions in your data processing agreements

For detailed guidance on the school-vendor relationship and contractual requirements, see our [FERPA Compliance Guide](/content/november-2026/ferpa-compliance-guide), which covers the data sharing agreements and vendor obligations that complement COPPA's school consent exception.

---

## COPPA vs FERPA: How They Work Together for EdTech

EdTech companies operating in K-12 education face a dual regulatory framework: COPPA and FERPA. These laws are complementary but distinct, and understanding how they interact is essential for any company that handles data about children in school settings.

### When each law applies

**FERPA** applies when a student's education records are disclosed by an educational institution. It governs the relationship between the school and the vendor through the school official exception. FERPA's obligations flow from the school to the vendor contractually. FERPA is enforced by the Department of Education's Student Privacy Policy Office.

**COPPA** applies when an operator of a website or online service collects personal information from a child under 13 online. It governs the operator directly. COPPA does not require a school intermediary -- it applies to any online collection of children's data, whether in an educational context or not. COPPA is enforced by the Federal Trade Commission.

### Where COPPA and FERPA overlap

For an EdTech company serving K-12 schools, both laws typically apply simultaneously:

| Dimension | FERPA | COPPA |
|---|---|---|
| **Regulated entity** | Educational institutions (schools) | Operators of websites/online services |
| **Protected population** | All students at federally funded schools | Children under 13 |
| **Enforcement agency** | Department of Education (SPPO) | Federal Trade Commission (FTC) |
| **Consent mechanism** | School official exception (contractual) | Verifiable parental consent or school consent |
| **Penalty structure** | Loss of federal education funding | Civil penalties up to $53,088 per violation |
| **Data use restrictions** | Limited to authorized educational purposes | Limited to purposes consented to; no commercial use with school consent |
| **Deletion rights** | Schools can require deletion at contract end | Parents can request deletion; retention must be limited |
| **Security requirement** | Reasonable methods to protect records | Reasonable procedures for data security |

### The gaps between COPPA and FERPA

Neither COPPA nor FERPA alone provides complete protection. Key gaps include:

- **FERPA does not apply to children under 13 who are not yet enrolled in school.** A four-year-old using an educational app at home is protected by COPPA but not by FERPA.
- **COPPA does not apply to children 13 and older.** A 14-year-old high school student is protected by FERPA but not by COPPA (though state laws may fill this gap).
- **FERPA has no direct vendor enforcement.** The Department of Education can act against schools that violate FERPA, but it cannot directly penalize vendors. The FTC, by contrast, can and does bring direct enforcement actions against vendors under COPPA.
- **Neither law comprehensively addresses AI-generated data.** When an AI tutoring system generates assessments, predictions, or behavioral profiles based on student data, the regulatory treatment of those derived data products under both COPPA and FERPA remains an evolving area.

### Practical approach for dual compliance

The most efficient approach for EdTech companies is to build a single data governance framework that satisfies both COPPA and FERPA. This means:

- Treat all student data from K-12 schools as subject to both laws simultaneously
- Use COPPA's stricter consent requirements as your baseline (since COPPA applies directly to operators while FERPA obligations are contractual)
- Implement FERPA's contractual requirements (data sharing agreements, school official provisions) as an additional compliance layer
- Conduct a [privacy impact assessment](/content/november-2026/privacy-impact-assessment-guide) that evaluates your data practices against both frameworks before launching any new feature that collects student data
- Maintain deletion and retention practices that satisfy both COPPA's deletion-on-request requirement and FERPA's end-of-contract data return/deletion obligations

---

## COPPA Safe Harbor Programs

The COPPA Rule includes a "safe harbor" provision that allows industry groups and other entities to submit self-regulatory guidelines to the FTC for approval. Operators who participate in an FTC-approved safe harbor program and comply with that program's guidelines are deemed to be in compliance with the COPPA Rule -- with the program serving as an intermediary enforcement layer.

### What safe harbor programs provide

Participation in a COPPA safe harbor program offers several advantages:

- **FTC-recognized compliance:** Operators participating in an approved safe harbor are deemed compliant with the COPPA Rule, provided they adhere to the program's guidelines.
- **Regular review and monitoring:** Safe harbor programs are required to conduct independent assessments of their members' COPPA compliance, typically through annual audits or reviews.
- **Guidance and support:** Programs provide members with implementation guidance, policy templates, and ongoing support for maintaining compliance.
- **Consumer trust signal:** Safe harbor seals and certifications serve as visible trust indicators for parents and schools.
- **Enforcement buffer:** While the FTC retains enforcement authority over all operators, it generally allows safe harbor programs to address member violations through internal mechanisms before taking direct action.

### FTC-approved COPPA safe harbor programs

The following programs are currently approved by the FTC as COPPA safe harbor programs:

**CARU (Children's Advertising Review Unit).** Operated by BBB National Programs, CARU has been the most established self-regulatory body for children's advertising and privacy since 1974. CARU's COPPA Safe Harbor Program reviews member practices, conducts compliance assessments, and handles complaints related to children's privacy. CARU is widely recognized in the entertainment, gaming, and consumer products industries.

**iKeepSafe.** Focused specifically on the intersection of technology and child safety in educational settings, iKeepSafe offers the COPPA Safe Harbor certification along with FERPA and state student privacy law assessments. iKeepSafe is particularly relevant for EdTech companies because it evaluates products against both COPPA and the educational privacy requirements that school districts demand.

**kidSAFE Seal Program.** kidSAFE provides a COPPA safe harbor certification focused on websites, apps, and other digital services directed at children. The program includes initial compliance review, ongoing monitoring, and a public-facing seal that operators can display. kidSAFE is widely used by app developers and online service providers.

**ESRB Privacy Certified.** The Entertainment Software Rating Board (ESRB), best known for rating video games, also operates a COPPA safe harbor program through its ESRB Privacy Certified program. This program is particularly relevant for game developers and interactive entertainment companies whose products are used by children.

**TRUSTe (TrustArc) Children's Privacy Program.** TrustArc, formerly TRUSTe, operates a COPPA safe harbor program that provides compliance assessments, ongoing monitoring, and dispute resolution. TrustArc's program is used by a broad range of technology companies.

### Choosing a safe harbor program

When selecting a COPPA safe harbor program, consider:

- **Your industry:** EdTech companies benefit most from programs like iKeepSafe that evaluate COPPA alongside FERPA and state student privacy laws. Game developers may prefer ESRB. General consumer apps may find CARU or kidSAFE most appropriate.
- **School district requirements:** Many school districts specifically look for iKeepSafe or kidSAFE certifications during procurement evaluations. If your primary market is K-12 education, choose a program that districts recognize.
- **Cost and effort:** Safe harbor program costs vary from a few thousand dollars annually for small operators to significantly more for large enterprises. Factor in the cost of the initial assessment, annual reviews, and any required remediation.
- **Scope of assessment:** Some programs evaluate only COPPA compliance, while others (notably iKeepSafe) evaluate across multiple frameworks. A broader assessment may be more efficient if you need to demonstrate compliance with multiple privacy laws.

---

## COPPA Technical Implementation Guide

COPPA compliance is not purely a legal or policy exercise. It requires specific technical controls embedded in your product's architecture, data flows, and user experience.

### Age gates and age screening

The most fundamental technical control for COPPA compliance is determining whether a user is under 13. Age gates -- mechanisms that ask users to confirm or provide their age before collecting personal information -- are the standard approach.

**Age gate design principles:**

- **Neutral presentation:** The age gate must not coach the user toward a particular answer. A prompt that says "You must be 13 to use this service -- enter your birthday" tells the child exactly what date to enter. Instead, use a neutral date-of-birth input without revealing the threshold.
- **No re-entry exploitation:** If a user enters an age under 13, the system must not allow the user to simply go back and enter a different age. Implement a persistent block (typically cookie-based or device-ID-based) that prevents immediate re-entry.
- **Date of birth, not yes/no:** The FTC has indicated that a simple "Are you 13 or older?" yes/no question is insufficient because it is trivially easy for a child to select "yes." A date-of-birth input provides somewhat more friction, though the FTC acknowledges no age gate is foolproof.
- **Do not retain age data unnecessarily:** If the user confirms they are 13 or older and you do not need their date of birth for any other purpose, do not retain the date of birth. The age screening itself should follow data minimization principles.

### Data collection controls

Once you have determined that a user may be under 13, your system must enforce COPPA's data minimization requirements:

- **Conditional data flows:** Your backend should support different data collection paths based on user age classification. Users classified as under-13 should trigger a restricted data collection flow that omits unnecessary fields and disables non-essential tracking.
- **SDK and third-party library management:** Audit every SDK and third-party library in your application. Many analytics and advertising SDKs collect persistent identifiers, device information, or behavioral data automatically. For users under 13, these SDKs must either be disabled entirely or configured to operate in a COPPA-compliant mode (many major SDKs offer a "child-directed" or "COPPA mode" configuration flag).
- **Server-side enforcement:** Do not rely solely on client-side controls to limit data collection. Server-side logic should validate that requests from under-13 accounts or sessions do not include data fields that should not have been collected. This defense-in-depth approach protects against client-side bypasses.

### Consent flow implementation

The parental consent flow is the most technically complex component of COPPA compliance:

1. **Child indicates age under 13** (or the service is child-directed and all users are treated as under 13).
2. **Operator collects parent's email address** (this is permitted without parental consent for the sole purpose of obtaining consent).
3. **Operator sends direct notice to parent** via email, describing the information to be collected and the purposes for which it will be used.
4. **Parent provides consent** through one of the FTC-approved methods (email plus for internal-only use, credit card transaction, video call, etc.).
5. **Operator records consent** -- timestamp, method, parent identifier, scope of consent -- in an auditable log.
6. **Operator enables data collection** only after valid consent is recorded.
7. **Operator provides ongoing mechanism** for the parent to review, revoke consent, or request deletion.

This flow must be implemented as a blocking gate: no personal information beyond the parent's contact information may be collected until valid consent is obtained and logged.

### Deletion mechanisms

COPPA requires operators to delete children's personal information upon parental request and when the information is no longer necessary for the purpose for which it was collected. Your technical architecture must support:

- **Per-user deletion:** The ability to identify and delete all personal information associated with a specific child user, including data stored across microservices, databases, caches, logs, and backups.
- **Bulk deletion:** For EdTech operators, the ability to delete all student data associated with a specific school or class upon school request or contract termination.
- **Automated retention enforcement:** Systems that automatically flag or delete children's data that has exceeded the defined retention period, consistent with your [data retention policy](/content/november-2026/data-retention-policy-guide).
- **Deletion verification:** Audit trails confirming that deletion was executed across all systems, including backup systems, within a reasonable timeframe.

### Logging and audit trails

Every consent action, data collection event, and deletion request involving a child's data should be logged in a tamper-resistant audit system. This documentation is essential for demonstrating COPPA compliance during an FTC investigation or safe harbor program review. The audit trail should capture:

- Consent granted: timestamp, method, parent identifier, scope
- Consent revoked: timestamp, parent identifier, scope of revocation
- Data collected: categories of data collected, timestamp, purpose
- Data deleted: timestamp, scope, systems affected, verification status
- Third-party disclosures: recipient, categories of data shared, purpose, timestamp

---

## COPPA Updates and Rule Changes (2024-2025)

The FTC finalized significant amendments to the COPPA Rule in 2024 and 2025, representing the most substantial update since 2013. These changes reflect the FTC's response to the evolution of technology, the proliferation of connected devices, and the increasing sophistication of data collection practices targeting children.

### Expanded definition of personal information

The updated rule expands the categories of information considered "personal information" under COPPA:

- **Biometric data:** Fingerprints, facial geometry, voiceprints, iris scans, and other biometric identifiers are now explicitly included in the definition of personal information. This is significant for apps and devices that use biometric authentication, AR/VR features involving facial mapping, or voice-activated interfaces.
- **Inferences drawn from other personal information:** Data derived from analyzing a child's behavior, preferences, or characteristics -- even if the underlying data points are individually non-identifying -- may constitute personal information if the inferences can be used to identify or contact the child.

### Strengthened consent requirements

The updates impose tighter standards on consent mechanisms:

- **Separate consent for targeted advertising:** Operators must obtain separate, affirmative consent before using children's personal information for targeted advertising. This consent must be distinct from consent for the basic operation of the service. A single blanket consent covering both service operation and advertising is no longer sufficient.
- **Consent renewal:** For certain high-risk data practices, the updated rule requires operators to renew parental consent periodically rather than relying on a single initial consent indefinitely.

### Data retention and security enhancements

- **Retention limitations:** The updated rule more explicitly requires operators to retain children's personal information only for as long as is reasonably necessary for the specific purpose for which it was collected. Indefinite retention is prohibited, and operators must define and enforce specific retention periods.
- **Security requirements:** While the rule continues to use a "reasonableness" standard, the FTC has provided additional guidance making clear that it expects encryption, access controls, incident response procedures, and regular security assessments as baseline measures for any operator handling children's data.

### Restrictions on push notifications

Push notifications that are used to encourage a child to return to an app or service, or that contain personalized content based on the child's data, are now treated as a form of "contact" under COPPA. Operators must include push notification practices in their privacy disclosures and parental consent processes.

### Implications for compliance programs

These rule changes require companies to:

- Review and update privacy policies to address biometric data, inferences, and push notifications
- Implement separate consent flows for targeted advertising (if applicable)
- Audit data retention practices and implement automated deletion for children's data
- Evaluate whether any biometric features in their products trigger additional COPPA obligations
- Update consent records to reflect the expanded scope of disclosures

Companies that built their COPPA compliance programs before 2024 should conduct a comprehensive gap assessment against the updated rule. A [privacy impact assessment](/content/november-2026/privacy-impact-assessment-guide) focused on the new rule provisions is the most effective way to identify and prioritize necessary changes.

---

## FTC COPPA Enforcement: Penalties and Notable Cases

The FTC enforces COPPA with civil penalties, injunctive relief, and consent orders that impose ongoing compliance obligations. The penalty structure and the FTC's enforcement track record make COPPA one of the most actively enforced privacy laws in the United States.

### Penalty structure

The COPPA statute authorizes civil penalties of up to $53,088 per violation (adjusted for inflation; the amount increases annually). Each instance of collecting personal information from a child without proper consent constitutes a separate violation. For a service with thousands or millions of child users, the aggregate penalty exposure is effectively unlimited.

In practice, the FTC has imposed penalties ranging from $10,000 for small operators to $520 million for large-scale violations. The amount depends on the number of children affected, the duration of the violation, the operator's knowledge and intent, the operator's cooperation with the investigation, and the operator's ability to pay.

### Notable enforcement cases

**Epic Games / Fortnite ($520 million, 2022).** The largest COPPA settlement in history. The FTC alleged that Epic Games violated COPPA by collecting personal information from children under 13 who played Fortnite, enabling real-time voice and text communications that exposed children to harassment by default, and using dark patterns to trick users into making unintended purchases. The settlement included $275 million in COPPA civil penalties and $245 million in refunds to consumers.

**Google / YouTube ($170 million, 2019).** The FTC and the New York Attorney General jointly settled with Google over allegations that YouTube illegally collected personal information from children without parental consent. YouTube used persistent identifiers to track children's viewing behavior and delivered targeted advertising based on that data. The settlement required YouTube to create a system for channel operators to identify child-directed content and to limit data collection on such content.

**TikTok / Musical.ly ($5.7 million, 2019; additional actions ongoing).** TikTok (formerly Musical.ly) settled with the FTC over allegations that it collected personal information from children under 13 without parental consent. The $5.7 million penalty was the largest COPPA fine at the time. The FTC has continued to scrutinize TikTok's compliance with the settlement and has taken additional enforcement steps related to children's privacy.

**Zoom ($85 million, 2023).** While not exclusively a COPPA case, the FTC's settlement with Zoom addressed children's privacy violations related to Zoom for Education, including inadequate security measures for children's data and misleading statements about privacy protections.

**OpenX ($2 million, 2021).** The FTC settled with the programmatic advertising company for collecting personal information from children under 13 through its real-time bidding platform, even after being notified by app developers that certain inventory was child-directed.

**HyperBeard ($150,000, 2020).** A mobile game developer settled with the FTC for allowing third-party advertising networks to collect personal information from child users of its games without parental consent. This case is notable because HyperBeard was a small developer, demonstrating that the FTC enforces COPPA regardless of company size.

### Enforcement trends

Several trends are evident in the FTC's COPPA enforcement activity:

- **Increasing penalty amounts:** Penalties have escalated dramatically, from thousands of dollars in early cases to hundreds of millions in recent cases.
- **Focus on dark patterns:** The FTC is targeting design patterns that manipulate children into providing data or making purchases.
- **Third-party accountability:** Ad networks, analytics providers, and SDK operators are being held directly accountable for data collection on child-directed properties.
- **EdTech scrutiny:** The FTC has signaled increased attention to EdTech companies, particularly those that collect data beyond what is necessary for educational purposes or that use student data for commercial purposes.
- **Ongoing monitoring:** Consent orders now commonly require 10-20 years of third-party compliance monitoring and regular reporting to the FTC.

---

## COPPA Compliance Checklist

Use this checklist to assess your organization's COPPA compliance posture. Each item represents a requirement or best practice that the FTC evaluates in enforcement investigations.

### Threshold analysis

- [ ] **Determine COPPA applicability** -- Assess whether your service is directed to children under 13 or whether you have actual knowledge that children under 13 use your service.
- [ ] **Identify all data collection points** -- Map every point in your service where personal information is collected, including passive collection through cookies, SDKs, and analytics tools.
- [ ] **Inventory third-party data collectors** -- Identify all third-party services (ad networks, analytics, social plugins) that collect data through your service.

### Privacy policy

- [ ] **COPPA-compliant privacy policy posted** -- Ensure your privacy policy addresses all COPPA-required disclosures and is written in plain language understandable to parents.
- [ ] **Policy is prominently linked** -- The privacy policy must be accessible from every page of your site or within your app before any data collection occurs.
- [ ] **All operators identified** -- The privacy policy must list all operators collecting personal information through your service.

### Parental consent

- [ ] **Direct notice mechanism implemented** -- A system to send direct notice to parents describing your data practices before collecting children's data.
- [ ] **Verifiable parental consent method implemented** -- At least one FTC-approved consent method is functional and documented.
- [ ] **Consent records maintained** -- An auditable log of all parental consents, including timestamp, method, scope, and parent identifier.
- [ ] **Consent revocation mechanism available** -- Parents can revoke consent and request cessation of data collection at any time.

### Data minimization and use restrictions

- [ ] **Data collection limited to necessity** -- You collect only the personal information reasonably necessary for the child to participate in the specific activity.
- [ ] **No conditioning on excessive collection** -- Participation in activities is not conditioned on providing more data than necessary.
- [ ] **No commercial use of school-consented data** -- If operating under the school consent exception, student data is used exclusively for authorized educational purposes.

### Security and data management

- [ ] **Reasonable security procedures implemented** -- Encryption, access controls, security assessments, and incident response procedures are in place.
- [ ] **Deletion capability confirmed** -- You can delete all personal information for a specific child upon parental request within a reasonable timeframe.
- [ ] **Retention periods defined and enforced** -- Children's data is retained only as long as necessary, with automated enforcement of retention limits.
- [ ] **Third-party SDK compliance verified** -- All third-party SDKs and libraries operate in COPPA-compliant mode for child users.

### Ongoing compliance

- [ ] **Employee training program** -- All employees who handle children's data or make product decisions affecting children receive COPPA training.
- [ ] **Annual compliance review** -- COPPA compliance is reviewed at least annually and after any significant product changes.
- [ ] **Safe harbor participation evaluated** -- Consider whether participation in an FTC-approved safe harbor program is appropriate for your business.
- [ ] **Incident response plan includes COPPA** -- Your [incident response plan](/content/november-2026/incident-response-plan-compliance-guide) includes specific procedures for breaches involving children's data.

---

## Frequently Asked Questions

### Does COPPA apply to my app if it is not specifically designed for children?

Yes, COPPA can apply even if your app targets a general audience. If you have actual knowledge that specific users are under 13, COPPA obligations attach to those users. Actual knowledge includes situations where a user provides a date of birth indicating they are under 13, a parent contacts you about their child's account, or a teacher informs you that students under 13 are using the product. Additionally, the FTC considers the totality of circumstances -- if your general-audience app has features, content, or marketing that attracts a significant child audience, the FTC may determine that it is "directed to children" and subject to COPPA in its entirety.

### What counts as "personal information" under COPPA?

COPPA defines personal information broadly. It includes: first and last name; home or physical address; email address; telephone number; Social Security number; a persistent identifier that can be used to recognize a user over time and across sites (including cookies, IP addresses, device serial numbers, and advertising IDs); a photograph, video, or audio file containing a child's image or voice; geolocation information sufficient to identify a street name and city; and, under the 2024-2025 updates, biometric data and certain inferences derived from other personal information. Importantly, persistent identifiers like cookies and device IDs are personal information under COPPA even if the operator does not know the child's name.

### Can a school provide COPPA consent for students?

Yes, but only under specific conditions. The school consent exception allows schools to authorize the collection of student data for educational purposes, effectively standing in for individual parents. However, the EdTech operator must use the data solely for the school-authorized educational purpose, cannot use the data for commercial purposes, and must still comply with all other COPPA obligations (privacy policy, data minimization, security, deletion). The school consent exception does not apply to data collection for non-educational features or to use of the product outside the school context.

### How does COPPA apply to advertising and monetization?

COPPA significantly restricts advertising and monetization activities involving children. Under the updated rule, operators must obtain separate parental consent before using children's personal information for targeted advertising. Contextual advertising (ads based on the content of the page, not the user's behavior) is generally permissible. Behavioral advertising (ads based on tracking the child's activity across sites or over time) requires consent. Many EdTech companies operating under the school consent exception choose to avoid advertising entirely for child users, as advertising is difficult to reconcile with the "educational purposes only" limitation of the school consent exception.

### What is the difference between COPPA and GDPR for children's data?

COPPA is a U.S. federal law enforced by the FTC, applying to operators of websites and online services directed at children under 13 or that have actual knowledge of child users. GDPR is the European Union's general data protection regulation, which includes specific provisions for children (Article 8) requiring parental consent for information society services offered to children under 16 (or as low as 13, depending on the member state). Key differences include: COPPA applies to operators based on the direction of the service to children, while GDPR applies based on offering services to individuals in the EU; COPPA's age threshold is uniformly 13, while GDPR's varies by member state; COPPA focuses on online collection of personal information, while GDPR covers all processing of personal data; and GDPR includes broader individual rights (data portability, right to be forgotten) that extend beyond COPPA's scope.

### How long do I have to respond to a parent's deletion request?

The COPPA Rule does not specify a precise number of days for responding to a deletion request, but the FTC expects operators to respond "promptly." In practice, the FTC's enforcement history suggests that operators should acknowledge the request within a few business days and complete the deletion within 30 days. This timeline aligns with the deletion timeframes required by other privacy frameworks, including GDPR (30 days) and CCPA (45 days). Your deletion process should include confirmation to the parent once deletion is complete.

### Can I use analytics on a child-directed site?

You can use analytics, but you must ensure that the analytics tools do not collect personal information from children in a manner that violates COPPA. Many standard analytics platforms collect persistent identifiers (cookies, device IDs) that constitute personal information under COPPA. Options include: using analytics tools that offer COPPA-compliant modes (such as Google Analytics' child-directed site settings), using server-side analytics that do not place tracking technologies on the child's device, or using aggregate analytics that do not collect information identifiable to individual children. Whatever approach you use, your privacy policy must disclose the analytics practices.

### Is a COPPA safe harbor certification required?

No. COPPA safe harbor participation is voluntary. Operators can comply with COPPA directly without participating in any safe harbor program. However, safe harbor programs provide independent validation of compliance, ongoing monitoring, and a visible trust signal for parents and schools. For EdTech companies selling to school districts, a safe harbor certification (particularly iKeepSafe or kidSAFE) can streamline procurement evaluations and differentiate your product from competitors. The cost-benefit analysis typically favors safe harbor participation for companies where children's data is a core aspect of the business.

---

## Build a COPPA Compliance Program That Scales

COPPA compliance is not a one-time project. It is a continuous obligation that must evolve with your product, your user base, and the regulatory landscape. The FTC is enforcing COPPA more aggressively than at any point in the law's history, the penalties are larger than ever, and the 2024-2025 rule updates have expanded what compliance requires.

The companies that handle this well are the ones that build COPPA compliance into their product architecture from the start -- age-gating mechanisms, consent flows, data minimization controls, deletion capabilities, and audit trails that operate as integrated features of the product rather than afterthoughts bolted on before a launch. They pair COPPA compliance with [SOC 2](/content/march-2026/pillar-soc2-complete-guide) to demonstrate that their security controls have been independently verified. They conduct [privacy impact assessments](/content/november-2026/privacy-impact-assessment-guide) before launching new features that affect children's data. And they treat compliance not as a legal burden but as a trust signal that parents, schools, and regulators all recognize.

QuickTrust helps EdTech companies, app developers, and online service operators build COPPA compliance programs that satisfy the FTC, win school district contracts, and scale with your business. Our platform maps your data practices against COPPA requirements, identifies gaps, and guides your team through the technical and policy changes needed to achieve and maintain compliance. For companies that also need [FERPA compliance](/content/november-2026/ferpa-compliance-guide) and SOC 2, we coordinate all three into a single, efficient program so you are not duplicating effort across frameworks.

Children's privacy is not a risk to manage. It is a standard to meet. The companies that meet it earn the trust of parents, schools, and the market.

**[Start your COPPA compliance program -- quicktrustapp.com](https://quicktrustapp.com)**

---

### Related resources

- [FERPA Compliance for EdTech Companies: The Complete Guide](/content/november-2026/ferpa-compliance-guide)
- [Privacy Impact Assessment (PIA): The Complete Guide](/content/november-2026/privacy-impact-assessment-guide)
- [Data Retention Policy: How to Build Retention Schedules](/content/november-2026/data-retention-policy-guide)
- [The Complete SOC 2 Compliance Guide for SaaS Startups](/content/march-2026/pillar-soc2-complete-guide)
- [Incident Response Plan: The Complete Compliance Guide](/content/november-2026/incident-response-plan-compliance-guide)
- [Case Study: How an EdTech Startup Got SOC 2 Certified and FERPA/COPPA Compliant](/content/august-2026/case-study-edtech-soc2-student-privacy)
- [Regulatory Compliance for Tech Companies: The Complete Guide](/content/november-2026/regulatory-compliance-tech-companies-guide)
