import type { Metadata } from 'next';
import Link from 'next/link';
import FAQSchema from '@/components/marketing/schema/FAQSchema';

export const metadata: Metadata = {
  title: 'SOC 2 Compliance Software — Get Audit-Ready in Weeks',
  description:
    'Automate SOC 2 Type I & II compliance. Map controls, close gaps with engineers, collect evidence, and coordinate your audit. Free readiness assessment.',
  alternates: {
    canonical: 'https://quicktrustapp.com/soc-2-compliance',
  },
  openGraph: {
    title: 'SOC 2 Compliance Software — Get Audit-Ready in Weeks',
    description:
      'Automate SOC 2 Type I & II compliance. Map controls, close gaps with engineers, collect evidence, and coordinate your audit.',
    url: 'https://quicktrustapp.com/soc-2-compliance',
    type: 'website',
  },
};

const faqs = [
  {
    question: 'How long does it take to get SOC 2 compliant with QuickTrust?',
    answer:
      'Timelines depend on your current security posture and scope. Teams with some controls in place can often reach audit readiness in 6-12 weeks. We compress timelines by running control implementation and evidence collection in parallel rather than sequentially.',
  },
  {
    question: 'Do I need SOC 2 Type I before Type II?',
    answer:
      'Not necessarily. Type I evaluates the design of controls at a point in time, while Type II evaluates operating effectiveness over a period (typically 3-12 months). Some organizations skip Type I and go directly to Type II, though a Type I can help build confidence with prospects faster.',
  },
  {
    question: 'Which Trust Services Criteria does QuickTrust cover?',
    answer:
      'QuickTrust covers all five Trust Services Criteria: Security (Common Criteria), Availability, Processing Integrity, Confidentiality, and Privacy. Most organizations start with Security (required) and add additional criteria based on customer requirements and business needs.',
  },
  {
    question: 'Will SOC 2 compliance drain our engineering resources?',
    answer:
      'We designed our process to minimize engineering involvement. Our engineers handle control implementation, configuration changes, and evidence collection. Your team is typically involved for approvals, access provisioning, and validation — most customers report under 2 hours per week of engineering time.',
  },
  {
    question: 'Can QuickTrust help us choose an auditor?',
    answer:
      'Yes. We work with a network of accredited CPA firms experienced in SOC 2 audits. We can recommend auditors based on your industry, scope, and timeline, or we can coordinate with your existing auditor to streamline the process.',
  },
  {
    question: 'What cloud platforms does QuickTrust support for SOC 2?',
    answer:
      'QuickTrust supports AWS, Google Cloud, Microsoft Azure, and hybrid environments. Our engineers have deep expertise across all major cloud providers and can implement controls regardless of your infrastructure stack.',
  },
];

export default function SOC2CompliancePage() {
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
        name: 'SOC 2 Compliance',
        item: 'https://quicktrustapp.com/soc-2-compliance',
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
              <span className="text-slate-300">SOC 2 Compliance</span>
            </nav>
            <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6 max-w-4xl">
              SOC 2 Compliance Software That Gets You Audit-Ready
            </h1>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mb-10">
              Map your controls to SOC 2 Trust Services Criteria, identify gaps, and close them with dedicated
              compliance engineers — not just software. QuickTrust combines a compliance automation platform with
              hands-on implementation to help accelerate your path to a clean SOC 2 report.
            </p>
            <Link
              href="/#lead-form"
              className="inline-flex items-center justify-center px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]"
            >
              Get SOC 2 Ready — Free 48-Hour Readiness Assessment
            </Link>
          </section>

          {/* Why SOC 2 Matters */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Why SOC 2 Matters for Growing SaaS Companies
            </h2>
            <div className="grid md:grid-cols-2 gap-8 lg:gap-12">
              <div>
                <p className="text-slate-400 mb-4">
                  SOC 2 has become the de facto security standard for SaaS companies selling to enterprise buyers.
                  Without a SOC 2 report, deals stall in security review, procurement cycles lengthen, and competitors
                  with reports in hand move ahead.
                </p>
                <p className="text-slate-400">
                  Beyond closing deals, SOC 2 compliance signals operational maturity. It demonstrates that your
                  organization has implemented controls around security, availability, and data handling — and that
                  those controls have been independently verified by a CPA firm.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">SOC 2 unlocks:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Faster enterprise sales cycles — share your report instead of filling out security questionnaires
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Upmarket expansion into regulated industries like fintech and healthcare
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Reduced risk of data breaches through systematic security controls
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Board and investor confidence in your security posture
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* How QuickTrust Accelerates SOC 2 */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              How QuickTrust Accelerates SOC 2 Compliance
            </h2>
            <p className="text-lg text-slate-400 max-w-3xl mb-12">
              Most compliance platforms give you software and leave you to figure out the rest. QuickTrust pairs
              automation with dedicated security engineers who implement controls, collect evidence, and coordinate
              with your auditor.
            </p>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">1</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Map</h3>
                <p className="text-slate-400">
                  We map your existing infrastructure, policies, and tools to SOC 2 Trust Services Criteria.
                  The platform identifies which controls you already satisfy and where gaps remain — producing a
                  prioritized remediation roadmap.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">2</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Fix</h3>
                <p className="text-slate-400">
                  Our engineers implement the controls your team needs — IAM policies, logging configurations,
                  encryption settings, SDLC controls, access reviews, and more. Your team reviews and approves;
                  we execute and document everything for audit.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">3</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Certify</h3>
                <p className="text-slate-400">
                  We coordinate with your auditor, prepare evidence packages, handle audit inquiries, and manage
                  remediation of any findings. You get a clean SOC 2 report with minimal disruption to your team.
                </p>
              </div>
            </div>
          </section>

          {/* SOC 2 Type I vs Type II */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              SOC 2 Type I vs Type II: Which Do You Need?
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-3">SOC 2 Type I</h3>
                <p className="text-slate-400 mb-4">
                  Evaluates the <strong className="text-slate-200">design</strong> of your controls at a specific
                  point in time. Useful for organizations that need to demonstrate security posture quickly to
                  close deals or satisfy investor requirements.
                </p>
                <p className="text-sm text-slate-500">
                  Typical timeline: Can often be achieved in weeks with the right preparation.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-3">SOC 2 Type II</h3>
                <p className="text-slate-400 mb-4">
                  Evaluates the <strong className="text-slate-200">operating effectiveness</strong> of your
                  controls over a period (typically 3-12 months). The gold standard for enterprise buyers and
                  regulated industries. Most organizations aim for Type II.
                </p>
                <p className="text-sm text-slate-500">
                  Typical timeline: Requires an observation period after controls are in place.
                </p>
              </div>
            </div>
            <p className="text-slate-400 mt-8">
              QuickTrust supports both Type I and Type II engagements. Many teams start with Type I for quick wins
              and transition to Type II for long-term compliance. We help you choose the right path based on your
              business priorities and customer requirements.
            </p>
          </section>

          {/* What's Included */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              What&apos;s Included in SOC 2 with QuickTrust
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { title: 'Control Mapping', desc: 'Automated mapping of your infrastructure to all five Trust Services Criteria with gap identification.' },
                { title: 'Policy Library', desc: 'Customizable policy templates aligned to SOC 2 requirements — access control, incident response, change management, and more.' },
                { title: 'Evidence Collection', desc: 'Automated evidence gathering from your cloud providers, identity providers, and development tools.' },
                { title: 'Engineer-Led Remediation', desc: 'Dedicated security engineers who implement controls, configure tools, and close gaps in your environment.' },
                { title: 'Auditor Coordination', desc: 'We manage audit timelines, evidence requests, and finding remediation so your team stays focused on product.' },
                { title: 'Continuous Monitoring', desc: 'Ongoing control monitoring and alerting so you maintain compliance between audit cycles.' },
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
              SOC 2 Compliance FAQs
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
              SOC 2 Resources
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <Link href="/blog/what-is-soc2" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">What Is SOC 2?</h3>
                <p className="text-sm text-slate-400">A complete guide to SOC 2 compliance, Trust Services Criteria, and what to expect from the audit process.</p>
              </Link>
              <Link href="/hipaa-compliance" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">HIPAA Compliance</h3>
                <p className="text-sm text-slate-400">Building healthcare SaaS? Learn how QuickTrust automates HIPAA compliance alongside SOC 2.</p>
              </Link>
              <Link href="/iso-27001-certification" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">ISO 27001 Certification</h3>
                <p className="text-sm text-slate-400">Expanding internationally? See how ISO 27001 complements SOC 2 and how to pursue both efficiently.</p>
              </Link>
            </div>
          </section>

          {/* CTA */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <div className="bg-gradient-to-br from-teal-400/10 to-cyan-400/5 rounded-2xl p-8 sm:p-12 border border-teal-400/20 text-center">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-4">
                Ready to Get SOC 2 Compliant?
              </h2>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-8">
                Get a free 48-hour readiness assessment. We&apos;ll evaluate your current posture, identify gaps,
                and give you a clear roadmap to audit readiness.
              </p>
              <Link
                href="/#lead-form"
                className="inline-flex items-center justify-center px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]"
              >
                Get SOC 2 Ready — Free 48-Hour Readiness Assessment
              </Link>
              <div className="mt-8 flex flex-wrap justify-center gap-6 text-sm text-slate-500">
                <Link href="/compare/quicktrust-vs-vanta" className="hover:text-teal-400 no-underline text-slate-500">QuickTrust vs Vanta</Link>
                <Link href="/pricing" className="hover:text-teal-400 no-underline text-slate-500">Pricing</Link>
                <Link href="/iso-27001-certification" className="hover:text-teal-400 no-underline text-slate-500">ISO 27001</Link>
                <Link href="/hipaa-compliance" className="hover:text-teal-400 no-underline text-slate-500">HIPAA</Link>
              </div>
            </div>
          </section>
        </main>
    </div>
  );
}
