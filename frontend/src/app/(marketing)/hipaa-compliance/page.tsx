import type { Metadata } from 'next';
import Link from 'next/link';
import FAQSchema from '@/components/marketing/schema/FAQSchema';

export const metadata: Metadata = {
  title: 'HIPAA Compliance Software — Automated Readiness for Healthcare Tech',
  description:
    'Automate HIPAA compliance for healthcare SaaS. Map safeguards, close gaps, collect evidence, get audit-ready. Platform + engineers. Free assessment.',
  alternates: {
    canonical: 'https://quicktrustapp.com/hipaa-compliance',
  },
  openGraph: {
    title: 'HIPAA Compliance Software — Automated Readiness for Healthcare Tech',
    description:
      'Automate HIPAA compliance for healthcare SaaS. Map safeguards, close gaps, collect evidence, get audit-ready.',
    url: 'https://quicktrustapp.com/hipaa-compliance',
    type: 'website',
  },
};

const faqs = [
  {
    question: 'Who needs to be HIPAA compliant?',
    answer:
      'Any organization that creates, receives, maintains, or transmits protected health information (PHI) electronically must comply with HIPAA. This includes covered entities (healthcare providers, health plans, clearinghouses) and their business associates — including SaaS companies that handle PHI on behalf of covered entities.',
  },
  {
    question: 'Does QuickTrust help with BAA management?',
    answer:
      'Yes. QuickTrust helps you track, manage, and maintain Business Associate Agreements with all vendors and subcontractors who access PHI. We provide BAA templates, track execution status, and ensure your vendor chain is properly documented for audit.',
  },
  {
    question: 'How does HIPAA compliance differ from SOC 2?',
    answer:
      'HIPAA is a federal regulation specific to protected health information, while SOC 2 is a voluntary audit framework focused on broader security controls. Many healthcare SaaS companies pursue both — SOC 2 for enterprise sales and HIPAA for regulatory compliance. QuickTrust can help you achieve both efficiently by mapping overlapping controls.',
  },
  {
    question: 'What happens if we have a HIPAA breach?',
    answer:
      'HIPAA requires breach notification to affected individuals, HHS, and potentially the media depending on the size of the breach. QuickTrust helps you build incident response procedures that include HIPAA-specific notification requirements, documentation workflows, and remediation plans to reduce breach impact.',
  },
  {
    question: 'Can QuickTrust help us pass a HIPAA audit?',
    answer:
      'While no one can guarantee audit outcomes, QuickTrust significantly improves your readiness by implementing all required safeguards, documenting policies, collecting evidence, and coordinating with your assessor. We align your controls to the HIPAA Security Rule, Privacy Rule, and Breach Notification Rule requirements.',
  },
  {
    question: 'How long does HIPAA compliance take?',
    answer:
      'Timelines depend on your current security maturity and the complexity of your PHI handling. Organizations with some security controls in place can often reach compliance readiness in 8-16 weeks. QuickTrust accelerates this by parallelizing safeguard implementation and evidence collection.',
  },
];

export default function HIPAACompliancePage() {
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
        name: 'HIPAA Compliance',
        item: 'https://quicktrustapp.com/hipaa-compliance',
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
              <span className="text-slate-300">HIPAA Compliance</span>
            </nav>
            <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6 max-w-4xl">
              HIPAA Compliance Software for Healthcare Tech Teams
            </h1>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mb-10">
              Building healthcare SaaS means handling PHI — and that means HIPAA compliance is not optional.
              QuickTrust automates safeguard mapping, gap identification, and evidence collection while our
              engineers implement the technical, administrative, and physical controls you need.
            </p>
            <Link
              href="/#lead-form"
              className="inline-flex items-center justify-center px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]"
            >
              Get HIPAA Compliant — Free Readiness Assessment
            </Link>
          </section>

          {/* Why HIPAA Compliance Matters */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Why HIPAA Compliance Matters for Healthcare SaaS
            </h2>
            <div className="grid md:grid-cols-2 gap-8 lg:gap-12">
              <div>
                <p className="text-slate-400 mb-4">
                  HIPAA violations carry severe consequences — penalties can reach millions of dollars per violation
                  category, and breaches can result in criminal charges for willful neglect. Beyond financial risk,
                  a HIPAA breach can permanently damage your reputation in the healthcare market.
                </p>
                <p className="text-slate-400">
                  For healthcare SaaS companies, HIPAA compliance is also a sales enabler. Covered entities require
                  their business associates to demonstrate HIPAA compliance before signing contracts. Without it,
                  you cannot sell to hospitals, health systems, payers, or digital health companies that handle PHI.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">HIPAA compliance enables:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Contracts with hospitals, health systems, and payers who require BAAs
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Reduced risk of costly breaches and OCR enforcement actions
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Trust with patients and providers who entrust you with sensitive health data
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Competitive advantage in a market where compliance is table stakes
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* How QuickTrust Automates HIPAA */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              How QuickTrust Automates HIPAA Compliance
            </h2>
            <p className="text-lg text-slate-400 max-w-3xl mb-12">
              HIPAA requires a comprehensive set of safeguards across your organization. QuickTrust maps every
              requirement, identifies where you fall short, and deploys engineers to close the gaps — so your
              team can stay focused on building product.
            </p>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">1</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Assess</h3>
                <p className="text-slate-400">
                  We conduct a comprehensive risk assessment across your PHI data flows, systems, and processes.
                  The platform maps your current controls to HIPAA Security Rule, Privacy Rule, and Breach
                  Notification Rule requirements.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">2</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Implement</h3>
                <p className="text-slate-400">
                  Our engineers deploy the technical safeguards you need — encryption at rest and in transit,
                  access controls, audit logging, backup procedures, and integrity controls. Administrative
                  and physical safeguards are documented and operationalized.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <div className="w-12 h-12 bg-teal-400/10 rounded-xl flex items-center justify-center mb-4">
                  <span className="font-display text-2xl font-bold text-teal-400">3</span>
                </div>
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Maintain</h3>
                <p className="text-slate-400">
                  HIPAA compliance is ongoing. QuickTrust provides continuous monitoring, periodic risk assessments,
                  workforce training tracking, and incident response procedures to keep your compliance posture
                  strong over time.
                </p>
              </div>
            </div>
          </section>

          {/* Safeguards Covered */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              HIPAA Safeguards Covered by QuickTrust
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-4">Technical Safeguards</h3>
                <ul className="space-y-2 text-slate-400 text-sm">
                  <li>Access controls and unique user identification</li>
                  <li>Encryption of ePHI at rest and in transit</li>
                  <li>Audit controls and logging</li>
                  <li>Integrity controls for ePHI</li>
                  <li>Transmission security (TLS/SSL)</li>
                  <li>Automatic session management and logoff</li>
                  <li>Emergency access procedures</li>
                </ul>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-4">Administrative Safeguards</h3>
                <ul className="space-y-2 text-slate-400 text-sm">
                  <li>Security risk assessments</li>
                  <li>Workforce security and training</li>
                  <li>Information access management</li>
                  <li>Security incident procedures</li>
                  <li>Contingency planning</li>
                  <li>Evaluation and ongoing review</li>
                  <li>Business Associate Agreements</li>
                </ul>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-4">Physical Safeguards</h3>
                <ul className="space-y-2 text-slate-400 text-sm">
                  <li>Facility access controls</li>
                  <li>Workstation use policies</li>
                  <li>Workstation security</li>
                  <li>Device and media controls</li>
                  <li>Data disposal and re-use procedures</li>
                  <li>Cloud infrastructure security</li>
                  <li>Data center compliance (AWS/GCP/Azure)</li>
                </ul>
              </div>
            </div>
          </section>

          {/* BAA Management */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Business Associate Agreement (BAA) Management
            </h2>
            <div className="grid md:grid-cols-2 gap-8 lg:gap-12 items-center">
              <div>
                <p className="text-slate-400 mb-4">
                  Every vendor, subcontractor, and cloud provider that accesses PHI on your behalf must have a
                  signed BAA. Managing these agreements across your vendor ecosystem can be complex and
                  time-consuming.
                </p>
                <p className="text-slate-400 mb-4">
                  QuickTrust provides a centralized BAA management system that tracks agreement status, renewal
                  dates, and vendor risk assessments. We also provide BAA templates that meet HIPAA requirements
                  and can be customized for your specific use cases.
                </p>
                <p className="text-slate-400">
                  Our platform integrates with your existing vendor management workflows to ensure no business
                  associate relationship goes undocumented — a common finding in HIPAA audits.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">What&apos;s Included</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    BAA template library aligned to HIPAA requirements
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Vendor inventory and risk assessment tracking
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Automated renewal reminders and status dashboards
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Audit trail for all BAA-related activities
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* FAQs */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              HIPAA Compliance FAQs
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
              HIPAA Resources
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <Link href="/blog/what-is-hipaa" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">What Is HIPAA?</h3>
                <p className="text-sm text-slate-400">A comprehensive overview of the Health Insurance Portability and Accountability Act and what it means for tech companies.</p>
              </Link>
              <Link href="/soc-2-compliance" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">SOC 2 Compliance</h3>
                <p className="text-sm text-slate-400">Many healthcare SaaS companies pursue SOC 2 alongside HIPAA. Learn how QuickTrust handles both frameworks.</p>
              </Link>
              <Link href="/iso-27001-certification" className="bg-white/5 rounded-xl p-6 border border-white/10 no-underline hover:border-teal-400/30 transition-colors group">
                <h3 className="font-display text-lg font-semibold text-slate-50 mb-2 group-hover:text-teal-400 transition-colors">ISO 27001 Certification</h3>
                <p className="text-sm text-slate-400">Expanding globally? ISO 27001 provides an internationally recognized information security management framework.</p>
              </Link>
            </div>
          </section>

          {/* CTA */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <div className="bg-gradient-to-br from-teal-400/10 to-cyan-400/5 rounded-2xl p-8 sm:p-12 border border-teal-400/20 text-center">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-4">
                Ready to Get HIPAA Compliant?
              </h2>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-8">
                Get a free readiness assessment. We&apos;ll evaluate your current HIPAA posture, map your PHI
                data flows, and provide a clear roadmap to compliance.
              </p>
              <Link
                href="/#lead-form"
                className="inline-flex items-center justify-center px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]"
              >
                Get HIPAA Compliant — Free Readiness Assessment
              </Link>
              <div className="mt-8 flex flex-wrap justify-center gap-6 text-sm text-slate-500">
                <Link href="/soc-2-compliance" className="hover:text-teal-400 no-underline text-slate-500">SOC 2 Compliance</Link>
                <Link href="/pricing" className="hover:text-teal-400 no-underline text-slate-500">Pricing</Link>
                <Link href="/iso-27001-certification" className="hover:text-teal-400 no-underline text-slate-500">ISO 27001</Link>
              </div>
            </div>
          </section>
        </main>
    </div>
  );
}
