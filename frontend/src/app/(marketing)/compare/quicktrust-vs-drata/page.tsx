import type { Metadata } from 'next';
import Link from 'next/link';
import FAQSchema from '@/components/marketing/schema/FAQSchema';

export const metadata: Metadata = {
  title: 'QuickTrust vs Drata — Compliance Platform Comparison (2026)',
  description:
    'Compare QuickTrust vs Drata: features, pricing model, implementation. See why teams choose QuickTrust for compliance automation.',
  alternates: {
    canonical: 'https://quicktrustapp.com/compare/quicktrust-vs-drata',
  },
  openGraph: {
    title: 'QuickTrust vs Drata — Compliance Platform Comparison (2026)',
    description:
      'Compare QuickTrust vs Drata: features, pricing model, implementation. See why teams choose QuickTrust for compliance automation.',
    url: 'https://quicktrustapp.com/compare/quicktrust-vs-drata',
    type: 'website',
  },
};

const faqs = [
  {
    question: 'Is QuickTrust a direct replacement for Drata?',
    answer:
      'QuickTrust and Drata serve similar goals but take different approaches. Drata is a compliance automation platform focused on continuous monitoring and evidence collection. QuickTrust combines automation with dedicated engineers who implement controls and close gaps. If your team needs hands-on implementation support, QuickTrust may be a stronger fit.',
  },
  {
    question: 'How does pricing compare between QuickTrust and Drata?',
    answer:
      'Drata uses a recurring SaaS subscription model. QuickTrust uses a fixed-price implementation model that bundles platform access with engineering services. The total cost depends on your scope — but with QuickTrust, you avoid the hidden cost of internal engineering time spent on implementation.',
  },
  {
    question: 'Can I migrate from Drata to QuickTrust?',
    answer:
      'Yes. If you have been using Drata and have existing policies, controls, and evidence, QuickTrust can build on that foundation. We review what you have in place and focus our engineering effort on gaps rather than starting from zero.',
  },
  {
    question: 'Which frameworks do both platforms support?',
    answer:
      'Both QuickTrust and Drata support SOC 2, ISO 27001, HIPAA, PCI DSS, GDPR, and other frameworks. Drata supports a broad set of frameworks and custom frameworks. QuickTrust focuses on the frameworks most commonly required by SaaS companies and provides implementation support for each.',
  },
  {
    question: 'Does QuickTrust integrate with the same tools as Drata?',
    answer:
      'QuickTrust integrates with major cloud providers (AWS, GCP, Azure), identity providers, version control systems, HR platforms, and endpoint management tools. Drata is known for a large integration catalog. If you rely on a niche tool, check with both vendors to confirm integration availability.',
  },
];

export default function QuickTrustVsDrataPage() {
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
        name: 'Compare',
        item: 'https://quicktrustapp.com/compare',
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: 'QuickTrust vs Drata',
        item: 'https://quicktrustapp.com/compare/quicktrust-vs-drata',
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
              <Link href="/compare/quicktrust-vs-drata" className="hover:text-teal-400 no-underline text-slate-500">Compare</Link>
              <span className="mx-2">/</span>
              <span className="text-slate-300">QuickTrust vs Drata</span>
            </nav>
            <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6 max-w-4xl">
              QuickTrust vs Drata: Compliance Platform Comparison
            </h1>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mb-10">
              Looking for a Drata alternative? QuickTrust and Drata both automate compliance, but they differ in
              how much implementation support you get. Drata provides the platform; QuickTrust provides the
              platform and the engineers. Here&apos;s a detailed comparison to help you decide.
            </p>
          </section>

          {/* Overview */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Overview: Platform-Only vs Platform + Engineers
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-3">QuickTrust</h3>
                <p className="text-slate-400 mb-4">
                  <strong className="text-slate-200">Platform + Engineers.</strong> QuickTrust delivers compliance
                  automation software alongside dedicated security and DevOps engineers. Our team implements
                  controls in your environment, writes and customizes policies, collects evidence, and coordinates
                  directly with your auditor or certification body.
                </p>
                <p className="text-sm text-slate-500">
                  Model: Fixed-price implementation with platform access included.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Drata</h3>
                <p className="text-slate-400 mb-4">
                  <strong className="text-slate-200">Compliance Automation Platform.</strong> Drata provides a
                  comprehensive SaaS platform for continuous compliance monitoring, automated evidence collection,
                  and risk management. It offers a large integration catalog and supports custom frameworks.
                  Implementation is managed by your internal team.
                </p>
                <p className="text-sm text-slate-500">
                  Model: Recurring SaaS subscription.
                </p>
              </div>
            </div>
          </section>

          {/* Feature Comparison Table */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              Feature Comparison
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse min-w-[600px]">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="py-4 px-4 font-display text-slate-50 font-semibold">Feature</th>
                    <th className="py-4 px-4 font-display text-teal-400 font-semibold">QuickTrust</th>
                    <th className="py-4 px-4 font-display text-slate-50 font-semibold">Drata</th>
                  </tr>
                </thead>
                <tbody className="text-slate-400 text-sm">
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Compliance Automation</td>
                    <td className="py-3 px-4 text-teal-400">Included</td>
                    <td className="py-3 px-4">Included</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Continuous Monitoring</td>
                    <td className="py-3 px-4 text-teal-400">Included</td>
                    <td className="py-3 px-4">Included</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Evidence Collection</td>
                    <td className="py-3 px-4 text-teal-400">Automated + engineer-assisted</td>
                    <td className="py-3 px-4">Automated</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Control Implementation</td>
                    <td className="py-3 px-4 text-teal-400">Done by QuickTrust engineers</td>
                    <td className="py-3 px-4">Done by your team</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Policy Authoring</td>
                    <td className="py-3 px-4 text-teal-400">Written &amp; customized for you</td>
                    <td className="py-3 px-4">Templates provided</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Gap Remediation</td>
                    <td className="py-3 px-4 text-teal-400">Engineers remediate gaps</td>
                    <td className="py-3 px-4">Identified; your team remediates</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Auditor Coordination</td>
                    <td className="py-3 px-4 text-teal-400">Full coordination included</td>
                    <td className="py-3 px-4">Auditor network available</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Pricing Model</td>
                    <td className="py-3 px-4 text-teal-400">Fixed-price implementation</td>
                    <td className="py-3 px-4">Recurring SaaS subscription</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Eng. Time Required</td>
                    <td className="py-3 px-4 text-teal-400">Minimal (approvals &amp; access)</td>
                    <td className="py-3 px-4">Significant (implementation)</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Custom Frameworks</td>
                    <td className="py-3 px-4">Core frameworks supported</td>
                    <td className="py-3 px-4">Custom framework builder</td>
                  </tr>
                  <tr className="border-b border-white/5">
                    <td className="py-3 px-4 font-medium text-slate-300">Risk Management</td>
                    <td className="py-3 px-4 text-teal-400">Risk register + treatment</td>
                    <td className="py-3 px-4">Risk management module</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* Implementation Approach Difference */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              The Implementation Approach Difference
            </h2>
            <div className="grid md:grid-cols-2 gap-8 lg:gap-12">
              <div>
                <p className="text-slate-400 mb-4">
                  Drata provides powerful automation for compliance monitoring. It connects to your cloud
                  infrastructure, identity providers, and development tools to track control status in real time.
                  However, when the platform identifies a gap, your team is responsible for implementing the fix.
                </p>
                <p className="text-slate-400 mb-4">
                  For teams with dedicated security staff, this model works well. But for growing startups and
                  mid-market companies where engineers are focused on product, the implementation burden can
                  create bottlenecks that delay compliance timelines.
                </p>
                <p className="text-slate-400">
                  QuickTrust eliminates this bottleneck. When a gap is identified — whether it&apos;s a missing
                  MFA configuration, inadequate logging, or an incomplete vendor risk assessment — our engineers
                  address it directly. Your team stays focused on building product.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">The QuickTrust difference:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Engineers implement controls directly in your environment
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Policies are authored and customized, not just templated
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Auditor coordination is fully managed — no back-and-forth on your team
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Fixed-price model so you know the total cost upfront
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* Framework Coverage */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Framework Coverage
            </h2>
            <p className="text-slate-400 max-w-3xl mb-8">
              Both platforms support the compliance frameworks most commonly required by SaaS companies. Drata
              offers a broader set of frameworks and a custom framework builder. QuickTrust focuses on deep
              implementation support for the core frameworks.
            </p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { framework: 'SOC 2 Type I & II', qt: true, drata: true },
                { framework: 'ISO 27001', qt: true, drata: true },
                { framework: 'HIPAA', qt: true, drata: true },
                { framework: 'PCI DSS', qt: true, drata: true },
                { framework: 'GDPR', qt: true, drata: true },
                { framework: 'Custom Frameworks', qt: false, drata: true },
              ].map((item, idx) => (
                <div key={idx} className="bg-white/5 rounded-xl p-5 border border-white/10 flex items-center justify-between">
                  <span className="font-medium text-slate-300">{item.framework}</span>
                  <div className="flex gap-4 text-sm">
                    <span className={item.qt ? 'text-teal-400' : 'text-slate-600'}>
                      QT {item.qt ? '&#10003;' : '—'}
                    </span>
                    <span className={item.drata ? 'text-slate-300' : 'text-slate-600'}>
                      D {item.drata ? '&#10003;' : '—'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Who Should Choose */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              Which Platform Should You Choose?
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">Choose Drata if:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    You have internal security or compliance staff to implement controls
                  </li>
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    You need custom framework support or an extensive integration library
                  </li>
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    You prefer a self-service SaaS model with a subscription pricing structure
                  </li>
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    Your team is comfortable managing audit coordination independently
                  </li>
                </ul>
              </div>
              <div className="bg-gradient-to-br from-teal-400/10 to-cyan-400/5 rounded-2xl p-6 sm:p-8 border border-teal-400/20">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-4">Choose QuickTrust if:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    You want engineers to implement controls, not just surface gaps
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Your engineering team is stretched thin and cannot absorb compliance work
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    You want predictable, fixed-price costs rather than recurring subscriptions
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    You need end-to-end audit coordination from a single vendor
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* Evaluation Checklist */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Evaluation Checklist
            </h2>
            <p className="text-slate-400 max-w-3xl mb-8">
              Use these questions when comparing QuickTrust, Drata, or any compliance platform:
            </p>
            <div className="max-w-3xl bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
              <ul className="space-y-4 text-slate-400">
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Does the vendor implement controls or just identify them?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  How many hours per week will your engineering team need to invest?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  What is the true total cost — including internal engineering time?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Does the vendor manage auditor coordination, or is that on your team?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Can you get a fixed-price quote, or are costs unpredictable?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Does the vendor support the specific integrations you rely on?
                </li>
              </ul>
            </div>
          </section>

          {/* FAQs */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              QuickTrust vs Drata FAQs
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

          {/* CTA */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <div className="bg-gradient-to-br from-teal-400/10 to-cyan-400/5 rounded-2xl p-8 sm:p-12 border border-teal-400/20 text-center">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-4">
                See How QuickTrust Compares — Get a Fixed-Price Quote
              </h2>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-8">
                Tell us about your compliance requirements and we&apos;ll provide a transparent, fixed-price
                quote that includes platform access and engineering implementation.
              </p>
              <Link
                href="/#lead-form"
                className="inline-flex items-center justify-center px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]"
              >
                Get a Fixed-Price Quote — See How QuickTrust Compares
              </Link>
              <div className="mt-8 flex flex-wrap justify-center gap-6 text-sm text-slate-500">
                <Link href="/soc-2-compliance" className="hover:text-teal-400 no-underline text-slate-500">SOC 2 Compliance</Link>
                <Link href="/hipaa-compliance" className="hover:text-teal-400 no-underline text-slate-500">HIPAA Compliance</Link>
                <Link href="/pricing" className="hover:text-teal-400 no-underline text-slate-500">Pricing</Link>
                <Link href="/compare/quicktrust-vs-vanta" className="hover:text-teal-400 no-underline text-slate-500">QuickTrust vs Vanta</Link>
              </div>
            </div>
          </section>
        </main>
    </div>
  );
}
