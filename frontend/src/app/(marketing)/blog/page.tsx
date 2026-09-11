import Link from 'next/link';
import { getArticlesByCategory, getAllArticles } from '@/lib/blog';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Compliance Resources & Guides',
  description:
    'Expert guides on SOC 2, ISO 27001, HIPAA, PCI DSS, and compliance automation. Learn how to get certified faster with actionable playbooks and frameworks.',
  alternates: {
    canonical: 'https://quicktrustapp.com/blog',
  },
  openGraph: {
    title: 'Compliance Resources & Guides | QuickTrust',
    description:
      'Expert guides on SOC 2, ISO 27001, HIPAA, PCI DSS, and compliance automation.',
    url: 'https://quicktrustapp.com/blog',
    siteName: 'QuickTrust',
    type: 'website',
    images: [{ url: 'https://quicktrustapp.com/og/blog', width: 1200, height: 630, alt: 'QuickTrust Compliance Blog' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Compliance Resources & Guides | QuickTrust',
    description: 'Expert guides on SOC 2, ISO 27001, HIPAA, PCI DSS, and compliance automation.',
    images: ['https://quicktrustapp.com/og/blog'],
  },
};

const categoryIcons: Record<string, string> = {
  'March 2026': 'SOC 2',
  'April 2026': 'ISO 27001 & HIPAA',
  'May 2026': 'PCI DSS & vCISO',
  'June 2026': 'Security & Compliance Frameworks',
  'July 2026': 'Security Policy & Strategy',
  'August 2026': 'Real-World Case Studies',
  'September 2026': 'Advanced Scenarios',
  'October 2026': 'Cyber Insurance',
  'November 2026': 'Security & Compliance Deep Dives',
  'Evergreen — Glossary': 'Glossary',
  'Evergreen — Comparisons': 'Comparisons',
  'Evergreen — Lead-magnets': 'Templates & Tools',
  'Evergreen — Use-cases': 'Use Cases',
};

const categoryDescriptions: Record<string, string> = {
  'March 2026': 'Deep dives into SOC 2 compliance — from Type I vs Type II differences to audit cost breakdowns and implementation playbooks for SaaS companies.',
  'April 2026': 'Comprehensive guides on ISO 27001 certification and HIPAA compliance, including Annex A controls, healthcare-specific requirements, and cost analysis.',
  'May 2026': 'PCI DSS compliance guides, scope reduction strategies, and expert advice on information security certifications and virtual CISO services.',
  'June 2026': 'Frameworks, policies, and security programs — from NIST and CMMC to incident response plans, risk assessments, and vendor management.',
  'July 2026': 'Security policy frameworks, compliance strategy, and revenue-focused approaches to building compliance programs from scratch.',
  'August 2026': 'Real-world case studies showcasing how companies achieved compliance certifications and the business outcomes that followed.',
  'September 2026': 'Advanced compliance scenarios including multi-framework implementations, FedRAMP, and continuous compliance strategies.',
  'October 2026': 'Cyber insurance and compliance — how certifications impact coverage, premiums, and risk posture.',
  'November 2026': 'Deep dives into security and compliance topics — from NIST frameworks to vendor risk management, encryption, and incident response.',
  'Evergreen — Glossary': 'Clear definitions of key compliance and security terms — SOC 2, ISO 27001, HIPAA, HITRUST, PCI DSS, GDPR, and more.',
  'Evergreen — Comparisons': 'Side-by-side comparisons of QuickTrust against Vanta, Drata, Secureframe, Sprinto, and other compliance automation platforms.',
  'Evergreen — Lead-magnets': 'Downloadable templates, checklists, and scorecards — SOC 2 readiness, ISO 27001 gap assessment, HIPAA risk assessment, and more.',
  'Evergreen — Use-cases': 'Industry-specific compliance guides for startups, healthcare SaaS, and other verticals navigating their first certifications.',
};

const categoryColors: Record<string, string> = {
  'March 2026': 'from-teal-500/20 to-teal-600/5 border-teal-500/30',
  'April 2026': 'from-violet-500/20 to-violet-600/5 border-violet-500/30',
  'May 2026': 'from-amber-500/20 to-amber-600/5 border-amber-500/30',
  'June 2026': 'from-rose-500/20 to-rose-600/5 border-rose-500/30',
  'July 2026': 'from-indigo-500/20 to-indigo-600/5 border-indigo-500/30',
  'August 2026': 'from-cyan-500/20 to-cyan-600/5 border-cyan-500/30',
  'September 2026': 'from-fuchsia-500/20 to-fuchsia-600/5 border-fuchsia-500/30',
  'October 2026': 'from-lime-500/20 to-lime-600/5 border-lime-500/30',
  'November 2026': 'from-blue-500/20 to-blue-600/5 border-blue-500/30',
  'Evergreen — Glossary': 'from-sky-500/20 to-sky-600/5 border-sky-500/30',
  'Evergreen — Comparisons': 'from-emerald-500/20 to-emerald-600/5 border-emerald-500/30',
  'Evergreen — Lead-magnets': 'from-orange-500/20 to-orange-600/5 border-orange-500/30',
  'Evergreen — Use-cases': 'from-cyan-500/20 to-cyan-600/5 border-cyan-500/30',
};

const tagColors: Record<string, string> = {
  'March 2026': 'bg-teal-500/20 text-teal-300',
  'April 2026': 'bg-violet-500/20 text-violet-300',
  'May 2026': 'bg-amber-500/20 text-amber-300',
  'June 2026': 'bg-rose-500/20 text-rose-300',
  'July 2026': 'bg-indigo-500/20 text-indigo-300',
  'August 2026': 'bg-cyan-500/20 text-cyan-300',
  'September 2026': 'bg-fuchsia-500/20 text-fuchsia-300',
  'October 2026': 'bg-lime-500/20 text-lime-300',
  'November 2026': 'bg-blue-500/20 text-blue-300',
  'Evergreen — Glossary': 'bg-sky-500/20 text-sky-300',
  'Evergreen — Comparisons': 'bg-emerald-500/20 text-emerald-300',
  'Evergreen — Lead-magnets': 'bg-orange-500/20 text-orange-300',
  'Evergreen — Use-cases': 'bg-cyan-500/20 text-cyan-300',
};

export default function BlogPage() {
  const grouped = getArticlesByCategory();
  const totalArticles = getAllArticles().length;

  // Define category display order
  const categoryOrder = [
    'March 2026',
    'April 2026',
    'May 2026',
    'June 2026',
    'July 2026',
    'August 2026',
    'September 2026',
    'October 2026',
    'November 2026',
    'Evergreen — Glossary',
    'Evergreen — Comparisons',
    'Evergreen — Lead-magnets',
    'Evergreen — Use-cases',
  ];

  const sortedCategories = Object.keys(grouped).sort((a, b) => {
    const aIdx = categoryOrder.indexOf(a);
    const bIdx = categoryOrder.indexOf(b);
    if (aIdx === -1 && bIdx === -1) return a.localeCompare(b);
    if (aIdx === -1) return 1;
    if (bIdx === -1) return -1;
    return aIdx - bIdx;
  });

  return (
    <div id="main-content" className="min-h-screen bg-slate-950">
      {/* Navigation spacer */}
      <div className="h-20" />

      {/* Hero */}
      <section className="relative py-16 sm:py-24 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-transparent to-transparent" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 relative">
          <div className="text-center max-w-3xl mx-auto">
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-sm font-medium mb-6">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              {totalArticles} Expert Guides
            </span>
            <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6">
              Compliance{' '}
              <span className="bg-gradient-to-r from-teal-400 to-teal-500 bg-clip-text text-transparent">
                Resources
              </span>
            </h1>
            <p className="text-lg sm:text-xl text-slate-400 leading-relaxed">
              Actionable guides on SOC 2, ISO 27001, HIPAA, PCI DSS, and security compliance.
              Written by engineers who have completed 100+ audits with a 100% pass rate.
            </p>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="pb-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          {sortedCategories.map((category) => (
            <div key={category} className="mb-16">
              <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                  <h2 className="font-display text-2xl sm:text-3xl font-bold text-slate-50">
                    {categoryIcons[category] || category}
                  </h2>
                  <span className={`text-xs font-medium px-3 py-1 rounded-full ${tagColors[category] || 'bg-slate-700 text-slate-300'}`}>
                    {grouped[category].length} articles
                  </span>
                </div>
                {categoryDescriptions[category] && (
                  <p className="text-sm text-slate-400 max-w-3xl leading-relaxed">
                    {categoryDescriptions[category]}
                  </p>
                )}
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {grouped[category].map((article) => (
                  <Link
                    key={article.slug}
                    href={`/blog/${article.slug}`}
                    className="group no-underline"
                  >
                    <article
                      className={`relative h-full rounded-2xl border bg-gradient-to-br ${
                        categoryColors[category] || 'from-slate-800/50 to-slate-900/50 border-white/10'
                      } p-6 transition-all hover:-translate-y-1 hover:shadow-lg hover:shadow-teal-500/5`}
                    >
                      {article.slug.startsWith('pillar-') && (
                        <span className="absolute top-4 right-4 text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-teal-500/20 text-teal-300 border border-teal-500/30">
                          Pillar
                        </span>
                      )}
                      {article.slug.startsWith('case-study-') && (
                        <span className="absolute top-4 right-4 text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                          Case Study
                        </span>
                      )}
                      <h3 className="font-display text-lg font-semibold text-slate-100 group-hover:text-teal-400 transition-colors mb-3 pr-16 leading-snug">
                        {article.title}
                      </h3>
                      <p className="text-sm text-slate-400 leading-relaxed line-clamp-3 mb-4">
                        {article.meta_description}
                      </p>
                      <div className="flex items-center gap-2 text-xs text-slate-500">
                        {article.target_keyword && (
                          <span className="px-2 py-0.5 rounded bg-white/5 border border-white/10">
                            {article.target_keyword.split(',')[0].trim()}
                          </span>
                        )}
                      </div>
                    </article>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="pb-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-6">
          <div className="relative rounded-3xl bg-gradient-to-br from-teal-500/10 to-violet-500/10 border border-white/10 p-8 sm:p-12 text-center overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-teal-500/5 to-transparent" />
            <div className="relative">
              <h2 className="font-display text-2xl sm:text-3xl font-bold text-slate-50 mb-4">
                Ready to Get Certified?
              </h2>
              <p className="text-slate-400 mb-8 max-w-xl mx-auto">
                Our engineers implement controls, prepare evidence, and coordinate your audit.
                100% pass rate across 100+ audits. Audit-ready in 6-10 weeks.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  href="/login?mode=register"
                  className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-gradient-primary text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] transition-all"
                >
                  Get Started Free
                </Link>
                <Link
                  href="/"
                  className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-white/5 text-slate-200 border border-white/10 no-underline hover:bg-white/10 hover:border-white/20 transition-all"
                >
                  Learn More
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 text-center">
          <Link href="/" className="text-slate-500 hover:text-slate-300 text-sm no-underline transition-colors">
            &larr; Back to QuickTrust
          </Link>
        </div>
      </footer>
    </div>
  );
}
