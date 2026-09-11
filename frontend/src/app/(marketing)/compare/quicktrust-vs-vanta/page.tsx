import type { Metadata } from 'next';
import Link from 'next/link';
import FAQSchema from '@/components/marketing/schema/FAQSchema';

export const metadata: Metadata = {
  title: 'QuickTrust vs Vanta — Compliance Platform Comparison (2026)',
  description:
    "Compare QuickTrust vs Vanta: features, pricing model, implementation approach. See why teams choose QuickTrust's platform + engineers model.",
  alternates: {
    canonical: 'https://quicktrustapp.com/compare/quicktrust-vs-vanta',
  },
  openGraph: {
    title: 'QuickTrust vs Vanta — Compliance Platform Comparison (2026)',
    description:
      "Compare QuickTrust vs Vanta: features, pricing model, implementation approach. See why teams choose QuickTrust's platform + engineers model.",
    url: 'https://quicktrustapp.com/compare/quicktrust-vs-vanta',
    type: 'website',
  },
};

const faqs = [
  {
    question: 'Is QuickTrust a direct replacement for Vanta?',
    answer:
      'QuickTrust and Vanta take different approaches to compliance. Vanta is primarily a SaaS platform that automates monitoring and evidence collection. QuickTrust combines automation with dedicated security engineers who implement controls, close gaps, and coordinate audits. If you need hands-on implementation support alongside software, QuickTrust may be a better fit.',
  },
  {
    question: 'How does pricing compare between QuickTrust and Vanta?',
    answer:
      'Vanta uses a recurring SaaS subscription model. QuickTrust uses a fixed-price implementation model that includes both platform access and engineering services. The right model depends on your team — if you have internal security staff to operate the platform, a SaaS subscription may work. If you need implementation help, a fixed-price model can provide more predictable costs.',
  },
  {
    question: 'Can I migrate from Vanta to QuickTrust?',
    answer:
      'Yes. Many teams evaluate QuickTrust after finding that a platform alone was not enough to reach audit readiness. We can review your existing controls, policies, and evidence collected in Vanta and build on that foundation rather than starting from scratch.',
  },
  {
    question: 'Which frameworks do both platforms support?',
    answer:
      'Both QuickTrust and Vanta support major frameworks including SOC 2, ISO 27001, HIPAA, PCI DSS, and GDPR. Framework coverage is similar between the two platforms — the key difference is in the implementation approach and level of hands-on support.',
  },
  {
    question: 'Does QuickTrust offer continuous monitoring like Vanta?',
    answer:
      'Yes. QuickTrust provides continuous monitoring of your cloud infrastructure, identity providers, and development tools. The difference is that when monitoring surfaces a gap or misconfiguration, QuickTrust engineers can remediate it — rather than leaving it to your team to address.',
  },
];

export default function QuickTrustVsVantaPage() {
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
        name: 'QuickTrust vs Vanta',
        item: 'https://quicktrustapp.com/compare/quicktrust-vs-vanta',
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
              <Link href="/compare/quicktrust-vs-vanta" className="hover:text-teal-400 no-underline text-slate-500">Compare</Link>
              <span className="mx-2">/</span>
              <span className="text-slate-300">QuickTrust vs Vanta</span>
            </nav>
            <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6 max-w-4xl">
              QuickTrust vs Vanta: Which Compliance Platform Is Right for You?
            </h1>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mb-10">
              Both QuickTrust and Vanta help companies achieve compliance, but they take fundamentally different
              approaches. Vanta provides a software platform for monitoring and evidence collection. QuickTrust
              pairs automation with dedicated engineers who implement controls and close gaps. Here&apos;s how
              they compare.
            </p>
          </section>

          {/* Overview */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Overview: Two Different Approaches to Compliance
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-3">QuickTrust</h3>
                <p className="text-slate-400 mb-4">
                  <strong className="text-slate-200">Platform + Engineers.</strong> QuickTrust provides compliance
                  automation software combined with dedicated security and DevOps engineers who implement controls,
                  write policies, configure infrastructure, collect evidence, and coordinate your audit. You get
                  the software and the people.
                </p>
                <p className="text-sm text-slate-500">
                  Model: Fixed-price implementation with platform access included.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">Vanta</h3>
                <p className="text-slate-400 mb-4">
                  <strong className="text-slate-200">Software Platform.</strong> Vanta is a compliance automation
                  platform that connects to your infrastructure, monitors controls, and collects evidence
                  automatically. Implementation and remediation are handled by your internal team or external
                  consultants.
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
                    <th className="py-4 px-4 font-display text-slate-50 font-semibold">Vanta</th>
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
                    <td className="py-3 px-4 font-medium text-slate-300">Framework Coverage</td>
                    <td className="py-3 px-4">SOC 2, ISO 27001, HIPAA, PCI DSS, GDPR</td>
                    <td className="py-3 px-4">SOC 2, ISO 27001, HIPAA, PCI DSS, GDPR, and more</td>
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
                  The biggest difference between QuickTrust and Vanta is not the software — it&apos;s the
                  implementation model. Vanta provides excellent automation tools, but your team is responsible
                  for implementing controls, writing policies, configuring infrastructure, and remediating gaps.
                </p>
                <p className="text-slate-400 mb-4">
                  QuickTrust takes a different approach. When the platform identifies a gap — say, missing
                  encryption at rest, inadequate logging, or an incomplete access review process — our engineers
                  fix it. They configure your cloud environment, update your IAM policies, set up monitoring,
                  and document everything for your auditor.
                </p>
                <p className="text-slate-400">
                  This means your engineering team can stay focused on building product while compliance moves
                  forward in parallel.
                </p>
              </div>
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">What this means in practice:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    No need to hire a dedicated compliance engineer or security team
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Engineering team involvement typically under 2 hours per week
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Controls are implemented, tested, and documented — not just identified
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Fixed-price model avoids the hidden cost of internal implementation time
                  </li>
                </ul>
              </div>
            </div>
          </section>

          {/* Who Should Choose */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              Which Platform Should You Choose?
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
                <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">Choose Vanta if:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    You have an internal security team that can implement and maintain controls
                  </li>
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    You prefer a self-service software model with broad integrations
                  </li>
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    Your team has experience running compliance programs internally
                  </li>
                  <li className="flex gap-3">
                    <span className="text-slate-500 mt-1 shrink-0">&bull;</span>
                    You need extensive framework coverage beyond the core set
                  </li>
                </ul>
              </div>
              <div className="bg-gradient-to-br from-teal-400/10 to-cyan-400/5 rounded-2xl p-6 sm:p-8 border border-teal-400/20">
                <h3 className="font-display text-xl font-semibold text-teal-400 mb-4">Choose QuickTrust if:</h3>
                <ul className="space-y-3 text-slate-400">
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    You need engineers to implement controls, not just identify them
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    Your engineering team is focused on product and cannot take on compliance work
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    You want a fixed-price engagement rather than ongoing subscription costs
                  </li>
                  <li className="flex gap-3">
                    <span className="text-teal-400 mt-1 shrink-0">&#10003;</span>
                    You want full auditor coordination and evidence preparation included
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
              Use these questions when evaluating any compliance platform — whether it&apos;s QuickTrust, Vanta,
              or another solution:
            </p>
            <div className="max-w-3xl bg-white/5 rounded-2xl p-6 sm:p-8 border border-white/10">
              <ul className="space-y-4 text-slate-400">
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Does the vendor implement controls or just identify gaps?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  How much internal engineering time will the engagement require?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Is the pricing model predictable, or are there hidden costs for support and implementation?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Does the vendor coordinate with your auditor, or is that your responsibility?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  What happens when monitoring surfaces a new gap — who remediates it?
                </li>
                <li className="flex gap-3">
                  <span className="text-teal-400 mt-0.5 shrink-0">&#9744;</span>
                  Does the platform support the specific frameworks your customers require?
                </li>
              </ul>
            </div>
          </section>

          {/* FAQs */}
          <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24 border-t border-white/5">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-10">
              QuickTrust vs Vanta FAQs
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
                Tell us about your compliance goals and we&apos;ll provide a transparent, fixed-price quote.
                No surprises, no hidden fees, no recurring subscription required.
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
                <Link href="/compare/quicktrust-vs-drata" className="hover:text-teal-400 no-underline text-slate-500">QuickTrust vs Drata</Link>
              </div>
            </div>
          </section>
        </main>
    </div>
  );
}
