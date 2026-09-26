import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getMarketingPage, MARKETING_ORIGIN } from '@/lib/marketing-pages';
import { getAllArticles } from '@/lib/blog';
import ArticleContent from '@/app/(marketing)/blog/[slug]/ArticleContent';
import SEOPageShell from './SEOPageShell';
import ReadinessAssessment from './ReadinessAssessment';
import ComplianceRoiCalculator from './ComplianceRoiCalculator';
import PageBreadcrumbSchema from './schema/PageBreadcrumbSchema';
import ServicePageSchema from './schema/ServicePageSchema';
import FAQSchema from './schema/FAQSchema';

export default function MarketingDetailPage({ pathname }: { pathname: string }) {
  const page = getMarketingPage(pathname);
  if (!page) notFound();
  const scenarios = pathname === '/resources/case-studies'
    ? getAllArticles().filter((article) => article.slug.startsWith('case-study-')) : [];
  return (
    <>
      <PageBreadcrumbSchema items={[{ name: 'Home', item: MARKETING_ORIGIN }, { name: page.title, item: MARKETING_ORIGIN + pathname }]} />
      {page.service && <ServicePageSchema name={page.title} description={page.description} url={MARKETING_ORIGIN + pathname} serviceType={page.title} />}
      {page.faqs.length > 0 && <FAQSchema faqs={page.faqs} />}
      <SEOPageShell eyebrow={page.eyebrow} title={page.title} description={page.description} bullets={[]}>
        <div className="mx-auto max-w-4xl px-4 sm:px-6">
          <ArticleContent content={page.content} articlePath={pathname} />
          {page.faqs.length > 0 && <section className="mt-12" aria-label="Frequently asked questions">
            <h2 className="font-display text-2xl font-semibold text-slate-50">Frequently asked questions</h2>
            {page.faqs.map((faq) => <div key={faq.question} className="mt-6">
              <h3 className="text-lg font-semibold text-slate-100">{faq.question}</h3>
              <p className="mt-2 leading-relaxed text-slate-300">{faq.answer}</p>
            </div>)}
          </section>}
          {scenarios.length > 0 && <nav aria-label="Illustrative implementation scenarios" className="mt-10">
            <h2 className="font-display text-2xl font-semibold text-slate-50">Explore the scenarios</h2>
            <ul className="mt-4 grid gap-4 sm:grid-cols-2">
              {scenarios.map((article) => <li key={article.slug}><Link className="text-teal-400 hover:text-teal-300" href={`/blog/${article.slug}`}>{article.title}</Link></li>)}
            </ul>
          </nav>}
        </div>
        {page.tool === 'readiness' && <div className="mt-12"><ReadinessAssessment /></div>}
        {page.tool === 'roi' && <div className="mt-12"><ComplianceRoiCalculator /></div>}
      </SEOPageShell>
    </>
  );
}
