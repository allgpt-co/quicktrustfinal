import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'About QuickTrust — Compliance Automation Platform',
  description:
    'QuickTrust combines compliance automation software with implementation engineers. Learn about our mission and approach.',
  alternates: {
    canonical: '/about',
  },
  openGraph: {
    title: 'About QuickTrust — Compliance Automation Platform',
    description:
      'QuickTrust combines compliance automation software with implementation engineers. Learn about our mission and approach.',
    type: 'website',
    siteName: 'QuickTrust',
    url: 'https://quicktrustapp.com/about',
  },
};

export default function AboutPage() {
  return (
    <div className="font-body bg-slate-950 text-slate-300 overflow-x-hidden">

        {/* Hero */}
        <section className="relative pt-32 pb-16 sm:pt-40 sm:pb-24 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-transparent to-transparent" />
          <div className="max-w-7xl mx-auto px-4 sm:px-6 relative">
            <div className="text-center max-w-3xl mx-auto">
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-sm font-medium mb-6">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                About Us
              </span>
              <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6">
                About{' '}
                <span className="bg-gradient-to-r from-teal-400 to-teal-500 bg-clip-text text-transparent">
                  QuickTrust
                </span>
              </h1>
              <p className="text-lg sm:text-xl text-slate-400 leading-relaxed max-w-2xl mx-auto">
                We combine compliance automation software with implementation engineers who do the
                work — so you get audit-ready faster without draining your engineering team.
              </p>
            </div>
          </div>
        </section>

        {/* Mission */}
        <section className="py-16 sm:py-24">
          <div className="max-w-4xl mx-auto px-4 sm:px-6">
            <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-teal-500/5 to-transparent p-8 sm:p-12">
              <h2 className="font-display text-2xl sm:text-3xl font-bold text-slate-50 mb-6">
                Our Mission
              </h2>
              <p className="text-slate-400 text-lg leading-relaxed mb-6">
                Compliance should not be a bottleneck for growing companies. Too many startups and
                scale-ups lose deals, delay launches, or burn engineering time trying to navigate
                SOC 2, ISO 27001, and HIPAA on their own.
              </p>
              <p className="text-slate-400 text-lg leading-relaxed">
                QuickTrust exists to remove that friction. We built a platform that automates the
                tedious parts of compliance — control mapping, gap analysis, evidence collection —
                and paired it with engineers who handle the implementation work. The result: you get
                certified faster, with less internal burden, and stay compliant as you grow.
              </p>
            </div>
          </div>
        </section>

        {/* How We're Different */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                How We&apos;re Different
              </h2>
              <p className="text-slate-400 text-lg">
                Most compliance tools give you a dashboard and leave you to figure out the rest. Most
                consultants give you a report and move on. We do both — software and engineers,
                working together.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  title: 'Platform + Engineers',
                  description:
                    'Our compliance automation platform handles control mapping, evidence tracking, and monitoring. Our implementation engineers handle IAM configs, encryption, logging, policy drafting, and everything else needed to pass your audit.',
                  highlight: 'Software alone is not enough. We do the work.',
                },
                {
                  title: 'Implementation, Not Just Advice',
                  description:
                    'We do not hand you a 50-page report and wish you luck. Our engineers configure your cloud environment, write your policies, set up monitoring, and prepare your evidence packages. Your team reviews and approves — we execute.',
                  highlight: 'Less than 2 hours/week of your engineering time.',
                },
                {
                  title: 'Multi-Framework Efficiency',
                  description:
                    'SOC 2, ISO 27001, and HIPAA share many of the same underlying controls. Our platform maps these overlaps automatically, so adding a second or third framework is significantly faster and cheaper than the first.',
                  highlight: 'One control can satisfy multiple frameworks.',
                },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8 hover:border-teal-500/20 transition-all"
                >
                  <h3 className="font-display text-xl font-semibold text-slate-50 mb-4">
                    {item.title}
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed mb-4">{item.description}</p>
                  <p className="text-teal-400 text-sm font-medium">{item.highlight}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Who We Serve */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                Who We Serve
              </h2>
              <p className="text-slate-400 text-lg">
                We work with cloud-first companies that need compliance to close deals, enter
                regulated markets, or meet customer requirements.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              {[
                {
                  title: 'Startups Closing Enterprise Deals',
                  description:
                    'Your prospect sent a security questionnaire and wants SOC 2. You need to get certified fast without pulling engineers off the product. That is exactly what we do.',
                },
                {
                  title: 'Growth-Stage SaaS Companies',
                  description:
                    'You have some security foundations in place but need to formalize them for audit. We fill the gaps, document what exists, and get you across the finish line.',
                },
                {
                  title: 'Healthcare Technology Companies',
                  description:
                    'HIPAA compliance is not optional. We help healthtech companies implement the administrative, technical, and physical safeguards required — and maintain them over time.',
                },
                {
                  title: 'Companies Scaling Internationally',
                  description:
                    'ISO 27001 is the global standard. We help companies that are expanding internationally get certified and demonstrate security maturity to global customers.',
                },
              ].map((segment, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8"
                >
                  <h3 className="font-display text-lg font-semibold text-slate-50 mb-3">
                    {segment.title}
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{segment.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Our Approach */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-4xl mx-auto px-4 sm:px-6">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-12 text-center">
              Our Approach
            </h2>
            <div className="space-y-8">
              {[
                {
                  step: '01',
                  title: 'Assess',
                  description:
                    'We start with a free readiness assessment. We review your current security posture, map it against your target framework(s), and identify exactly what needs to change.',
                },
                {
                  step: '02',
                  title: 'Implement',
                  description:
                    'Our engineers handle the implementation — cloud hardening, policy drafting, access controls, logging, encryption, SDLC controls. Your team reviews and approves; we execute.',
                },
                {
                  step: '03',
                  title: 'Evidence &amp; Audit',
                  description:
                    'We prepare comprehensive evidence packages, coordinate with your auditor, handle questions and remediation requests, and ensure you are fully prepared before the audit begins.',
                },
                {
                  step: '04',
                  title: 'Maintain',
                  description:
                    'Compliance is not a one-time event. We provide continuous monitoring, quarterly reviews, policy updates, and ongoing support to keep you audit-ready year-round.',
                },
              ].map((phase, idx) => (
                <div
                  key={idx}
                  className="flex gap-6 sm:gap-8 items-start"
                >
                  <div className="flex-shrink-0 w-14 h-14 rounded-2xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center">
                    <span className="font-display text-lg font-bold text-teal-400">
                      {phase.step}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-display text-xl font-semibold text-slate-50 mb-2">
                      {phase.title}
                    </h3>
                    <p className="text-slate-400 leading-relaxed">{phase.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Our Team — Placeholder */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center">
            {/* TODO: Founder input needed — Add real team member bios, photos, and titles. Do not fabricate team members. */}
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
              Our Team
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto mb-12">
              QuickTrust is built by security engineers, DevOps specialists, and compliance
              professionals who have collectively completed hundreds of audits across SOC 2,
              ISO 27001, HIPAA, and PCI DSS.
            </p>
            <div className="rounded-2xl border border-dashed border-white/20 bg-white/[0.01] p-12">
              <p className="text-slate-500 text-sm">
                Team member profiles coming soon. In the meantime, reach out to learn about the
                people behind QuickTrust.
              </p>
              <Link
                href="/#lead-form"
                className="inline-flex items-center justify-center px-6 py-3 mt-6 font-display font-semibold text-sm rounded-xl bg-white/5 text-slate-300 border border-white/10 no-underline hover:bg-white/10 hover:border-white/20 transition-all"
              >
                Get in Touch
              </Link>
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
                  Ready to Get Audit-Ready?
                </h2>
                <p className="text-slate-400 mb-8 max-w-xl mx-auto">
                  Start with a free readiness assessment. We will review your compliance posture and
                  give you a clear roadmap — no commitment required.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link
                    href="/#lead-form"
                    className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-gradient-primary text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] transition-all"
                  >
                    Free Readiness Assessment
                  </Link>
                  <Link
                    href="/pricing"
                    className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-white/5 text-slate-200 border border-white/10 no-underline hover:bg-white/10 hover:border-white/20 transition-all"
                  >
                    View Pricing
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
              <Link href="/pricing" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                Pricing
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/soc-2-compliance" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                SOC 2 Compliance
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/blog" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                Resources
              </Link>
            </div>
          </div>
        </section>
    </div>
  );
}
