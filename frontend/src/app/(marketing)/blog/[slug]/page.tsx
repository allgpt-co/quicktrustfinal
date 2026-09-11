import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getArticleBySlug, getAllSlugs, getRelatedArticles } from '@/lib/blog';
import ArticleContent from './ArticleContent';
import ArticleSchema from '@/components/marketing/schema/ArticleSchema';
import BreadcrumbSchema from '@/components/marketing/schema/BreadcrumbSchema';
import type { Metadata } from 'next';

interface PageProps {
  params: Promise<{ slug: string }>;
}

export const dynamicParams = false;

export async function generateStaticParams() {
  const slugs = getAllSlugs();
  return slugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const article = getArticleBySlug(slug);
  if (!article) return { title: 'Article Not Found' };

  const articleUrl = `https://quicktrustapp.com/blog/${slug}`;
  return {
    title: article.title,
    description: article.meta_description,
    keywords: [article.target_keyword, article.secondary_keywords].filter(Boolean).join(', '),
    alternates: {
      canonical: articleUrl,
    },
    openGraph: {
      title: article.title,
      description: article.meta_description,
      url: articleUrl,
      type: 'article',
      siteName: 'QuickTrust',
      images: [{ url: 'https://quicktrustapp.com/og/blog', width: 1200, height: 630, alt: article.title }],
      publishedTime: article.publish_date,
      modifiedTime: article.last_updated,
      authors: [article.author || 'QuickTrust Editorial'],
    },
    twitter: {
      card: 'summary_large_image',
      title: article.title,
      description: article.meta_description,
      images: ['https://quicktrustapp.com/og/blog'],
    },
  };
}

function getCtaContent(slug: string, keyword: string) {
  const s = slug.toLowerCase();
  const k = (keyword || '').toLowerCase();
  if (s.includes('soc2') || s.includes('soc-2') || k.includes('soc 2') || k.includes('soc2')) {
    return {
      heading: 'Ready to get SOC 2 certified?',
      description: 'Our engineers implement controls, prepare evidence, and coordinate your SOC 2 audit.',
      buttonText: 'Get SOC 2 Ready',
      href: '/soc-2-compliance',
    };
  }
  if (s.includes('hipaa') || k.includes('hipaa')) {
    return {
      heading: 'Ready to get HIPAA compliant?',
      description: 'Our engineers implement HIPAA safeguards, prepare evidence, and coordinate your assessment.',
      buttonText: 'Get HIPAA Compliant',
      href: '/hipaa-compliance',
    };
  }
  if (s.includes('iso') || s.includes('27001') || k.includes('iso') || k.includes('27001')) {
    return {
      heading: 'Ready for ISO 27001 certification?',
      description: 'Our engineers implement Annex A controls, prepare evidence, and coordinate your audit.',
      buttonText: 'Start ISO 27001',
      href: '/iso-27001-certification',
    };
  }
  if (s.includes('pci') || k.includes('pci')) {
    return {
      heading: 'Need PCI DSS compliance?',
      description: 'Our engineers implement PCI controls, prepare evidence, and coordinate your assessment.',
      buttonText: 'Get PCI DSS Ready',
      href: '/#lead-form',
    };
  }
  if (s.includes('questionnaire') || k.includes('questionnaire')) {
    return {
      heading: 'Tired of slow questionnaire responses?',
      description: 'Automate security questionnaire responses with policy-backed, auditable answers.',
      buttonText: 'Automate Questionnaires',
      href: '/solutions/security-questionnaire-automation',
    };
  }
  return {
    heading: 'Ready to get audit-ready?',
    description: 'Our engineers implement controls, prepare evidence, and coordinate your audit.',
    buttonText: 'Get a Free Assessment',
    href: '/#lead-form',
  };
}

export default async function ArticlePage({ params }: PageProps) {
  const { slug } = await params;
  const article = getArticleBySlug(slug);

  if (!article) {
    notFound();
  }

  const relatedArticles = getRelatedArticles(slug, 6);
  const ctaContent = getCtaContent(slug, article.target_keyword || '');

  return (
    <main id="main-content" className="min-h-screen bg-slate-950">
      <ArticleSchema
        title={article.title}
        description={article.meta_description}
        slug={article.slug}
        author={article.author}
        datePublished={article.publish_date}
        dateModified={article.last_updated}
        keywords={[article.target_keyword, article.secondary_keywords].filter(Boolean).join(', ')}
      />
      <BreadcrumbSchema
        articleTitle={article.title}
        articleSlug={article.slug}
      />
      {/* Navigation spacer */}
      <div className="h-20" />

      {/* Breadcrumb */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 pt-6">
        <nav className="flex items-center gap-2 text-sm text-slate-500">
          <Link href="/" className="hover:text-slate-300 transition-colors no-underline text-slate-500">
            Home
          </Link>
          <span>/</span>
          <Link href="/blog" className="hover:text-slate-300 transition-colors no-underline text-slate-500">
            Resources
          </Link>
          <span>/</span>
          <span className="text-slate-400 truncate max-w-[200px]">{article.title}</span>
        </nav>
      </div>

      {/* Article Header */}
      <header className="max-w-4xl mx-auto px-4 sm:px-6 pt-8 pb-8">
        <div className="flex flex-wrap items-center gap-3 mb-6">
          <span className="text-xs font-medium px-3 py-1.5 rounded-full bg-teal-500/15 text-teal-400 border border-teal-500/25">
            {article.category}
          </span>
          {article.slug.startsWith('pillar-') && (
            <span className="text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-full bg-violet-500/15 text-violet-400 border border-violet-500/25">
              Pillar Guide
            </span>
          )}
          {article.slug.startsWith('case-study-') && (
            <span className="text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/25">
              Case Study
            </span>
          )}
          {article.target_keyword && (
            <span className="text-xs px-3 py-1.5 rounded-full bg-white/5 text-slate-400 border border-white/10">
              {article.target_keyword.split(',')[0].trim()}
            </span>
          )}
        </div>
        <h1 className="font-display text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-50 leading-tight mb-6">
          {article.title}
        </h1>
        {article.meta_description && (
          <p className="text-lg text-slate-400 leading-relaxed mb-6">
            {article.meta_description}
          </p>
        )}
        <div className="flex items-center gap-4 text-sm text-slate-500">
          <span>By {article.author || 'QuickTrust Editorial'}</span>
          {article.last_updated && (
            <>
              <span className="w-1 h-1 rounded-full bg-slate-600" />
              <span>Updated {article.last_updated}</span>
            </>
          )}
        </div>
      </header>

      {/* Divider */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className="h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
      </div>

      {/* Article Body */}
      <article className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <ArticleContent content={article.content} />
      </article>

      {/* CTA Banner — contextual to article topic */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 pb-12">
        <div className="rounded-2xl bg-gradient-to-br from-teal-500/10 to-violet-500/10 border border-white/10 p-8 sm:p-10">
          <div className="flex flex-col sm:flex-row items-center gap-6">
            <div className="flex-1">
              <h3 className="font-display text-xl sm:text-2xl font-bold text-slate-50 mb-2">
                {ctaContent.heading}
              </h3>
              <p className="text-slate-400 text-sm">
                {ctaContent.description}
              </p>
            </div>
            <Link
              href={ctaContent.href}
              className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-gradient-primary text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 transition-all whitespace-nowrap"
            >
              {ctaContent.buttonText}
            </Link>
          </div>
        </div>
      </div>

      {/* Related Articles */}
      {relatedArticles.length > 0 && (
        <section className="max-w-4xl mx-auto px-4 sm:px-6 pb-16">
          <h2 className="font-display text-2xl font-bold text-slate-50 mb-8">
            Related Articles
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {relatedArticles.slice(0, 6).map((related) => (
              <Link
                key={related.slug}
                href={`/blog/${related.slug}`}
                className="group no-underline"
              >
                <div className="rounded-xl border border-white/10 bg-white/[0.02] p-5 transition-all hover:-translate-y-1 hover:border-teal-500/30 hover:bg-teal-500/5 h-full">
                  <span className="text-[11px] font-medium text-teal-400 uppercase tracking-wider mb-2 block">
                    {related.category}
                  </span>
                  <h3 className="font-display text-sm font-semibold text-slate-200 group-hover:text-teal-400 transition-colors leading-snug">
                    {related.title}
                  </h3>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
