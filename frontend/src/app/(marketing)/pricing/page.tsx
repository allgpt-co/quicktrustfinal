import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Pricing — Compliance Automation Platform',
  description:
    'Transparent pricing for SOC 2, ISO 27001, HIPAA compliance. Platform + implementation. Fixed-price packages. Get a quote.',
  alternates: {
    canonical: '/pricing',
  },
  openGraph: {
    title: 'Pricing — Compliance Automation Platform',
    description:
      'Transparent pricing for SOC 2, ISO 27001, HIPAA compliance. Platform + implementation. Fixed-price packages. Get a quote.',
    type: 'website',
    siteName: 'QuickTrust',
    url: 'https://quicktrustapp.com/pricing',
  },
};

export default function PricingPage() {
  return (
    <div className="font-body bg-slate-950 text-slate-300 overflow-x-hidden">

        {/* Hero */}
        <section className="relative pt-32 pb-16 sm:pt-40 sm:pb-24 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-transparent to-transparent" />
          <div className="max-w-7xl mx-auto px-4 sm:px-6 relative">
            <div className="text-center max-w-3xl mx-auto">
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-sm font-medium mb-6">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Fixed-Price Packages
              </span>
              <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6">
                Simple, Transparent{' '}
                <span className="bg-gradient-to-r from-teal-400 to-teal-500 bg-clip-text text-transparent">
                  Compliance Pricing
                </span>
              </h1>
              <p className="text-lg sm:text-xl text-slate-400 leading-relaxed max-w-2xl mx-auto">
                Platform access plus implementation engineers. No hidden fees, no surprise overages.
                Every package includes the software and the team to get you audit-ready.
              </p>
            </div>
          </div>
        </section>

        {/* Pricing Packages */}
        <section className="py-16 sm:py-24">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-5xl mx-auto">
              {/* Certification Fast Track */}
              <div className="relative rounded-2xl border border-white/10 bg-white/[0.02] p-8 sm:p-10 flex flex-col">
                <div className="mb-8">
                  <span className="text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-full bg-teal-500/15 text-teal-400 border border-teal-500/25">
                    For Startups &amp; Growth-Stage
                  </span>
                </div>
                <h2 className="font-display text-2xl sm:text-3xl font-bold text-slate-50 mb-4">
                  Certification Fast Track
                </h2>
                <p className="text-slate-400 mb-6 leading-relaxed">
                  Get your first certification done right. Ideal for startups closing enterprise
                  deals that need SOC 2, ISO 27001, or HIPAA compliance fast.
                </p>
                {/* TODO: Founder input needed — specific pricing tiers */}
                <div className="bg-white/5 rounded-xl border border-white/10 p-6 mb-8">
                  <p className="text-sm text-slate-400 mb-1">Starting at</p>
                  <p className="font-display text-3xl font-bold text-slate-50 mb-2">Custom Quote</p>
                  <p className="text-sm text-slate-500">Based on scope, framework, and company size</p>
                </div>
                <ul className="space-y-4 mb-8 flex-1">
                  {[
                    'Single framework certification (SOC 2, ISO 27001, or HIPAA)',
                    'Full platform access — control mapping, gap analysis, evidence collection',
                    'Dedicated implementation engineer',
                    'Policy drafting and review',
                    'Cloud infrastructure hardening (AWS, GCP, Azure)',
                    'Auditor coordination and evidence preparation',
                    'Target: audit-ready in 6-10 weeks',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <svg className="w-5 h-5 text-teal-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-slate-300 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href="/#lead-form"
                  className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-white/5 text-slate-200 border border-white/10 no-underline hover:bg-white/10 hover:border-white/20 hover:-translate-y-0.5 transition-all text-center"
                >
                  Get a Custom Quote
                </Link>
              </div>

              {/* Continuous Compliance */}
              <div className="relative rounded-2xl border border-teal-500/30 bg-gradient-to-br from-teal-500/10 to-violet-500/5 p-8 sm:p-10 flex flex-col">
                <div className="mb-8 flex items-center gap-3">
                  <span className="text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-full bg-violet-500/15 text-violet-400 border border-violet-500/25">
                    For Enterprise &amp; Scale-Ups
                  </span>
                  <span className="text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-full bg-teal-500/15 text-teal-400 border border-teal-500/25">
                    Most Popular
                  </span>
                </div>
                <h2 className="font-display text-2xl sm:text-3xl font-bold text-slate-50 mb-4">
                  Continuous Compliance
                </h2>
                <p className="text-slate-400 mb-6 leading-relaxed">
                  Multi-framework compliance with ongoing monitoring. For teams that need SOC 2 +
                  ISO 27001 + HIPAA or continuous audit readiness across frameworks.
                </p>
                {/* TODO: Founder input needed — specific pricing tiers */}
                <div className="bg-white/5 rounded-xl border border-white/10 p-6 mb-8">
                  <p className="text-sm text-slate-400 mb-1">Starting at</p>
                  <p className="font-display text-3xl font-bold text-slate-50 mb-2">Custom Quote</p>
                  <p className="text-sm text-slate-500">Based on frameworks, team size, and infrastructure</p>
                </div>
                <ul className="space-y-4 mb-8 flex-1">
                  {[
                    'Multi-framework support (SOC 2, ISO 27001, HIPAA, PCI DSS, HITRUST)',
                    'Everything in Certification Fast Track',
                    'Continuous control monitoring and drift detection',
                    'Automated evidence collection pipelines',
                    'Security questionnaire automation and response library',
                    'Dedicated compliance engineering team',
                    'Quarterly access reviews and policy updates',
                    'Ongoing auditor relationship management',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <svg className="w-5 h-5 text-teal-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-slate-300 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href="/#lead-form"
                  className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-gradient-primary text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] transition-all text-center"
                >
                  Get a Custom Quote
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* What's Included */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                What&apos;s Included in Every Package
              </h2>
              <p className="text-slate-400 text-lg">
                Every QuickTrust engagement combines our compliance automation platform with
                hands-on implementation engineers. You get the software and the team.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[
                {
                  title: 'Compliance Automation Platform',
                  description:
                    'Map frameworks to controls, track evidence, surface gaps, and monitor compliance posture — all in one dashboard.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25" />
                  ),
                },
                {
                  title: 'Implementation Engineers',
                  description:
                    'Our security and DevOps engineers handle the hands-on work — IAM configs, logging, encryption, SDLC controls, and more.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
                  ),
                },
                {
                  title: 'Policy &amp; Control Library',
                  description:
                    'Professionally drafted, auditor-tested policies mapped to SOC 2, ISO 27001, HIPAA, and other frameworks.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                  ),
                },
                {
                  title: 'Gap Analysis &amp; Remediation',
                  description:
                    'We identify what is missing, prioritize fixes by risk, and implement the remediations — not just flag them.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                  ),
                },
                {
                  title: 'Auditor Coordination',
                  description:
                    'We manage timelines, prepare evidence packages, handle auditor questions, and coordinate remediation closures.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                  ),
                },
                {
                  title: 'Cloud Infrastructure Review',
                  description:
                    'Deep review of your AWS, GCP, or Azure setup. We harden configurations and implement monitoring to meet framework requirements.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z" />
                  ),
                },
              ].map((feature, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8 hover:border-teal-500/20 hover:bg-teal-500/[0.02] transition-all"
                >
                  <div className="w-12 h-12 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center mb-5">
                    <svg className="w-6 h-6 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      {feature.icon}
                    </svg>
                  </div>
                  <h3 className="font-display text-lg font-semibold text-slate-50 mb-3">{feature.title}</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-3xl mx-auto px-4 sm:px-6">
            <div className="text-center mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                Pricing FAQ
              </h2>
            </div>
            <div className="space-y-6">
              {[
                {
                  q: 'How does QuickTrust pricing work?',
                  a: 'We offer fixed-price packages based on your framework scope, company size, and infrastructure complexity. You get a single quote that covers both platform access and implementation engineering — no hourly billing surprises.',
                },
                {
                  q: 'What frameworks do you support?',
                  a: 'We support SOC 2 Type I and Type II, ISO 27001, HIPAA, PCI DSS, and HITRUST. Multi-framework engagements benefit from shared controls across frameworks, reducing total cost and timeline.',
                },
                {
                  q: 'Do I pay separately for the platform and the engineers?',
                  a: 'No. Every package includes full platform access and a dedicated implementation engineering team. The platform automates control mapping and evidence collection; the engineers handle the actual implementation work.',
                },
                {
                  q: 'How long does it take to get audit-ready?',
                  a: 'Most single-framework engagements reach audit readiness in 6-10 weeks. Multi-framework projects typically take 10-16 weeks, depending on current maturity and scope.',
                },
                {
                  q: 'Can I start with one framework and add more later?',
                  a: 'Absolutely. Many customers start with SOC 2, then add ISO 27001 or HIPAA. Since we map shared controls across frameworks, adding a second or third framework is significantly faster than the first.',
                },
                {
                  q: 'Is there a free trial or assessment?',
                  a: 'We offer a free readiness assessment where we review your current compliance posture and provide a prioritized roadmap. This helps you understand scope and timeline before committing.',
                },
              ].map((faq, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8"
                >
                  <h3 className="font-display text-lg font-semibold text-slate-50 mb-3">
                    {faq.q}
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{faq.a}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 sm:py-24">
          <div className="max-w-4xl mx-auto px-4 sm:px-6">
            <div className="relative rounded-3xl bg-gradient-to-br from-teal-500/10 to-violet-500/10 border border-white/10 p-8 sm:p-12 text-center overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-teal-500/5 to-transparent" />
              <div className="relative">
                <h2 className="font-display text-2xl sm:text-3xl font-bold text-slate-50 mb-4">
                  Get a Custom Quote
                </h2>
                <p className="text-slate-400 mb-8 max-w-xl mx-auto">
                  Tell us about your compliance goals, and we will put together a fixed-price
                  package that covers platform access, implementation, and auditor coordination.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link
                    href="/#lead-form"
                    className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-gradient-primary text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] transition-all"
                  >
                    Request a Quote
                  </Link>
                  <Link
                    href="/about"
                    className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-white/5 text-slate-200 border border-white/10 no-underline hover:bg-white/10 hover:border-white/20 transition-all"
                  >
                    Learn About Us
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Internal Links */}
        <section className="pb-16 sm:pb-24">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <Link href="/soc-2-compliance" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                SOC 2 Compliance
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/hipaa-compliance" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                HIPAA Compliance
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/iso-27001-certification" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                ISO 27001 Certification
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/about" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                About QuickTrust
              </Link>
            </div>
          </div>
        </section>
    </div>
  );
}
