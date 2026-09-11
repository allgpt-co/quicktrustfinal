import type { Metadata } from 'next';
import Link from 'next/link';
import FAQSchema from '@/components/marketing/schema/FAQSchema';

export const metadata: Metadata = {
  title: 'ISO 27001 Certification — Fast-Track Implementation',
  description:
    'Get ISO 27001 certified faster. Map Annex A controls, close gaps with engineers, prepare evidence. Platform + implementation. Free assessment.',
  alternates: {
    canonical: 'https://quicktrustapp.com/iso-27001-certification',
  },
  openGraph: {
    title: 'ISO 27001 Certification — Fast-Track Implementation',
    description:
      'Get ISO 27001 certified faster. Map Annex A controls, close gaps with engineers, prepare evidence. Platform + implementation.',
    url: 'https://quicktrustapp.com/iso-27001-certification',
    type: 'website',
  },
};

const faqs = [
  {
    question: 'How long does ISO 27001 certification take?',
    answer:
      'Timelines vary based on organizational complexity and current security maturity. With QuickTrust, teams with foundational security controls can often reach certification readiness in 3-6 months. We compress timelines by parallelizing ISMS documentation, control implementation, and internal audit preparation.',
  },
  {
    question: 'What is the difference between ISO 27001 and SOC 2?',
    answer:
      'ISO 27001 is an international standard focused on establishing an Information Security Management System (ISMS), while SOC 2 is a US-based audit framework focused on Trust Services Criteria. ISO 27001 results in a certification valid for 3 years (with surveillance audits), while SOC 2 produces an annual report. Many organizations pursue both for comprehensive coverage.',
  },
  {
    question: 'Do we need ISO 27001 if we already have SOC 2?',
    answer:
      'It depends on your market. ISO 27001 is widely recognized internationally and is often required by European and APAC enterprise buyers. SOC 2 is the standard in North America. If you sell globally, having both provides maximum coverage. QuickTrust maps overlapping controls so you can pursue both efficiently.',
  },
  {
    question: 'What are Annex A controls?',
    answer:
      'Annex A of ISO 27001:2022 contains 93 controls organized across 4 themes: Organizational, People, Physical, and Technological. These controls cover everything from access management and cryptography to supplier relationships and incident management. Not all controls apply to every organization — your Statement of Applicability determines which are relevant.',
  },
  {
    question: 'Does QuickTrust handle the Stage 1 and Stage 2 audits?',
    answer:
      'QuickTrust prepares you for both stages. Stage 1 (documentation review) verifies your ISMS documentation is complete. Stage 2 (implementation audit) verifies controls are operational. We ensure your documentation, evidence, and processes are ready for both stages and coordinate with your chosen certification body.',
  },
  {
    question: 'How much engineering time is required?',
    answer:
      'Our engineers handle the majority of technical implementation — configuring controls, deploying monitoring, setting up access management, and collecting evidence. Your engineering team is typically involved for approvals, access provisioning, and architecture reviews. Most customers report 2-4 hours per week of engineering involvement.',
  },
];

export default function ISO27001CertificationPage() {
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: 'https://quicktrustapp.com',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'ISO 27001 Certification',
        item: 'https://quicktrustapp.com/iso-27001-certification',
      },
    ],
  };

  return (
    <div className="font-body bg-slate-950 text-slate-300 overflow-x-hidden">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />
      <FAQSchema faqs={faqs} />
        <main className="pt-28 sm:pt-36">
          {/* Hero */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 pb-16 sm:pb-24">
            <nav className="text-sm text-slate-500 mb-8">
              <Link href="/" className="hover:text-teal-400 no-underline text-slate-500">Home</Link>
              <span className="mx-2">/</span>
              <span className="text-slate-300">ISO 27001 Certification</span>
            </nav>
            <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6 max-w-4xl">
              ISO 27001 Certification — Fast-Track Your Implementation
            </h1>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mb-10">
              ISO 27001 is the global gold standard for information security management. QuickTrust combines an
              automation platform with hands-on engineers to help you build your ISMS, implement Annex A controls,
              and prepare for certification — without overwhelming your team.
            </p>
            <Link
              href="/#lead-form"
              className="inline-flex items-center justify-center px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]"
            >
              Start ISO 27001 Readiness Assessment
            </Link>
          </section>

          {/* Why ISO 27001 Matters */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Why ISO 27001 Matters for Growing Companies
            </h2>
            <div className="grid md:grid-cols-2 gap-8 lg:gap-12">
              <div>
                <p className="text-slate-400 mb-4">
                  ISO 27001 certification tells international buyers, partners, and regulators that your
                  organization has a systematic approach to managing information security risks. Unlike
                  point-in-time assessments, ISO 27001 requires a living Information Security Management
                  System (ISMS) that continuously improves.
                </p>
                <p className="text-slate-400">
                  For SaaS companies expanding beyond North America, ISO 27001 is often a prerequisite for
                  enterprise contracts in Europe, the Middle East, and Asia-Pacific. It also provides a strong
                  foundation for meeting GDPR requirements and other regional data protection regulations.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">ISO 27001 delivers:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Access to international enterprise markets that require certification
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    3-year certification with annual surveillance audits (not annual re-certification)
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Systematic risk management across your entire organization
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Foundation for GDPR, NIS2, and other regulatory requirements
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* How QuickTrust Accelerates ISO 27001 */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              How QuickTrust Accelerates ISO 27001 Certification
            </h2>
            <p className="text-lg text-slate-400 max-w-3xl mb-12">
              ISO 27001 implementation involves building an ISMS, conducting risk assessments, implementing
              controls, and preparing for a two-stage audit. QuickTrust handles the heavy lifting at every step.
            </p>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">1</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Scope & Assess</h3>
                <p className="text-slate-400">
                  We define your ISMS scope, conduct a comprehensive risk assessment, and map your existing
                  controls to ISO 27001:2022 requirements. The platform generates your Statement of Applicability
                  and a prioritized implementation plan.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">2</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Build & Implement</h3>
                <p className="text-slate-400">
                  Our engineers build your ISMS documentation, implement Annex A controls, configure monitoring
                  and logging, and establish the management review processes your certification body will evaluate.
                  Policies, procedures, and evidence are prepared in parallel.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">3</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Audit & Certify</h3>
                <p className="text-slate-400">
                  We conduct internal audits, perform management reviews, and prepare your team for the Stage 1
                  and Stage 2 certification audits. We coordinate with your certification body and handle any
                  nonconformity remediation.
                </p>
              </div>
            </div>
          </section>

          {/* Annex A Controls Coverage */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              ISO 27001:2022 Annex A Controls Coverage
            </h2>
            <p className="text-slate-400 max-w-3xl mb-10">
              ISO 27001:2022 organizes 93 controls across four themes. QuickTrust maps your environment to every
              applicable control and helps you build evidence for your Statement of Applicability.
            </p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                <h3 className="font-display text-lg font-semibold text-teal-400 mb-3">Organizational</h3>
                <p className="text-sm text-slate-400 mb-2">37 controls covering:</p>
                <ul className="text-sm text-slate-500 space-y-1">
                  <li>Information security policies</li>
                  <li>Roles and responsibilities</li>
                  <li>Threat intelligence</li>
                  <li>Supplier relationships</li>
                  <li>Incident management</li>
                  <li>Business continuity</li>
                </ul>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                <h3 className="font-display text-lg font-semibold text-teal-400 mb-3">People</h3>
                <p className="text-sm text-slate-400 mb-2">8 controls covering:</p>
                <ul className="text-sm text-slate-500 space-y-1">
                  <li>Screening and vetting</li>
                  <li>Terms of employment</li>
                  <li>Security awareness training</li>
                  <li>Disciplinary process</li>
                  <li>Remote working</li>
                  <li>Confidentiality agreements</li>
                </ul>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                <h3 className="font-display text-lg font-semibold text-teal-400 mb-3">Physical</h3>
                <p className="text-sm text-slate-400 mb-2">14 controls covering:</p>
                <ul className="text-sm text-slate-500 space-y-1">
                  <li>Physical security perimeters</li>
                  <li>Physical entry controls</li>
                  <li>Equipment security</li>
                  <li>Secure disposal</li>
                  <li>Clear desk and screen</li>
                  <li>Storage media handling</li>
                </ul>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                <h3 className="font-display text-lg font-semibold text-teal-400 mb-3">Technological</h3>
                <p className="text-sm text-slate-400 mb-2">34 controls covering:</p>
                <ul className="text-sm text-slate-500 space-y-1">
                  <li>Access control and authentication</li>
                  <li>Cryptography</li>
                  <li>Secure development</li>
                  <li>Network security</li>
                  <li>Logging and monitoring</li>
                  <li>Data masking and DLP</li>
                </ul>
              </div>
            </div>
          </section>

          {/* ISO 27001 vs SOC 2 */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              ISO 27001 vs SOC 2: How They Compare
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="py-4 px-4 font-display text-slate-50 font-semibold">Aspect</th>
                    <th className="py-4 px-4 font-display text-teal-400 font-semibold">ISO 27001</th>
                    <th className="py-4 px-4 font-display text-slate-50 font-semibold">SOC 2</th>
                  </tr>
                </thead>
                <tbody className="text-slate-400 text-sm">
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Type</td>
                    <td className="py-3 px-4">International standard (certification)</td>
                    <td className="py-3 px-4">Audit framework (attestation report)</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Validity</td>
                    <td className="py-3 px-4">3 years with annual surveillance</td>
                    <td className="py-3 px-4">Annual report</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Recognition</td>
                    <td className="py-3 px-4">Global, especially EMEA/APAC</td>
                    <td className="py-3 px-4">Primarily North America</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Focus</td>
                    <td className="py-3 px-4">Risk-based ISMS</td>
                    <td className="py-3 px-4">Trust Services Criteria</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Auditor</td>
                    <td className="py-3 px-4">Accredited certification body</td>
                    <td className="py-3 px-4">Licensed CPA firm</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p className="text-slate-400 mt-6">
              Many organizations pursue both ISO 27001 and <Link href="/soc-2-compliance" className="text-teal-400 no-underline hover:text-teal-300">SOC 2</Link> to
              cover global and North American markets. QuickTrust maps overlapping controls so you can achieve both
              certifications efficiently, avoiding duplicate work.
            </p>
          </section>

          {/* What's Included */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              What&apos;s Included in ISO 27001 with QuickTrust
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { title: 'ISMS Documentation', desc: 'Complete ISMS documentation including scope definition, information security policy, risk assessment methodology, and Statement of Applicability.' },
                { title: 'Risk Assessment', desc: 'Comprehensive risk identification, analysis, and treatment planning aligned to your business context and ISO 27001 requirements.' },
                { title: 'Annex A Control Implementation', desc: 'Our engineers implement applicable controls across your infrastructure, processes, and systems.' },
                { title: 'Internal Audit', desc: 'Full internal audit execution to identify nonconformities before your certification body arrives.' },
                { title: 'Management Review', desc: 'Facilitated management review sessions to demonstrate leadership commitment and continuous improvement.' },
                { title: 'Certification Support', desc: 'Coordination with your certification body through Stage 1 and Stage 2 audits, including remediation of any findings.' },
              ].map((item, idx) => (
                <div key={idx} className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <h3 className="font-display text-lg font-semibold text-slate-50 mb-2">{item.title}</h3>
                  <p className="text-sm text-slate-400">{item.desc}</p>
                </div>
              ))}
            </div>
          </section>

          {/* FAQs */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              ISO 27001 Certification FAQs
            </h2>
            <div className="max-w-3xl space-y-8">
              {faqs.map((faq, idx) => (
                <div key={idx}>
                  <h3 className="font-display text-lg font-semibold text-slate-50 mb-2">{faq.question}</h3>
                  <p className="text-slate-400">{faq.answer}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Resources */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-8">
              ISO 27001 Resources
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <Link href="/blog/what-is-iso-27001" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">What Is ISO 27001?</h3>
                <p className="text-sm text-slate-400">An in-depth guide to ISO 27001 certification, the ISMS framework, and what the audit process looks like.</p>
              </Link>
              <Link href="/soc-2-compliance" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">SOC 2 Compliance</h3>
                <p className="text-sm text-slate-400">Pursuing both ISO 27001 and SOC 2? Learn how QuickTrust maps overlapping controls for efficient dual compliance.</p>
              </Link>
              <Link href="/hipaa-compliance" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">HIPAA Compliance</h3>
                <p className="text-sm text-slate-400">Healthcare tech teams can leverage ISO 27001 controls to accelerate HIPAA compliance.</p>
              </Link>
            </div>
          </section>

          {/* CTA */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <div className="bg-gradient-to-br from-teal-400/10 to-cyan-400/5 rounded-2xl p-8 sm:p-12 border border-teal-400/20 text-center">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-4">
                Ready to Fast-Track ISO 27001?
              </h2>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-8">
                Get a free readiness assessment. We&apos;ll evaluate your current security posture, map it to
                ISO 27001 requirements, and give you a clear path to certification.
              </p>
              <Link
                href="/#lead-form"
                className="inline-flex items-center justify-center px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]"
              >
                Start ISO 27001 Readiness Assessment
              </Link>
              <div className="mt-8 flex flex-wrap justify-center gap-6 text-sm text-slate-500">
                <Link href="/soc-2-compliance" className="hover:text-teal-400 no-underline text-slate-500">SOC 2 Compliance</Link>
                <Link href="/pricing" className="hover:text-teal-400 no-underline text-slate-500">Pricing</Link>
                <Link href="/hipaa-compliance" className="hover:text-teal-400 no-underline text-slate-500">HIPAA</Link>
              </div>
            </div>
          </section>
        </main>
    </div>
  );
}
