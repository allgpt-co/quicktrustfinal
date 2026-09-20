import type { MetadataRoute } from 'next';
import { getAllArticles } from '@/lib/blog';

// A rebuild is not a content update. Omit unknown, invalid or future dates.
function knownModificationDate(value: string | undefined): Date | undefined {
  if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return undefined;
  const date = new Date(value);
  if (Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== value || date.getTime() > Date.now()) return undefined;
  return date;
}

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://quicktrustapp.com';
  const articles = getAllArticles();


  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      changeFrequency: 'weekly',
      priority: 1.0,
    },
    {
      url: `${baseUrl}/blog`,
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/contact`,
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    // Framework pages
    {
      url: `${baseUrl}/soc-2-compliance`,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/hipaa-compliance`,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/iso-27001-certification`,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    // Comparison pages
    {
      url: `${baseUrl}/compare/quicktrust-vs-vanta`,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/compare/quicktrust-vs-drata`,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    // Solution pages
    {
      url: `${baseUrl}/solutions/security-questionnaire-automation`,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    // Trust pages
    {
      url: `${baseUrl}/pricing`,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/about`,
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    {
      url: `${baseUrl}/privacy-policy`,
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/terms-of-service`,
      changeFrequency: 'yearly',
      priority: 0.3,
    },
  ];

  const articlePages: MetadataRoute.Sitemap = articles
    .filter((a) => a.published !== false)
    .map((article) => {
      const isPillar = article.slug.startsWith('pillar-');
      const isCaseStudy = article.slug.startsWith('case-study-');
      const isComparison = article.slug.startsWith('quicktrust-vs-') || article.slug.includes('platforms-comparison');
      const isGlossary = article.slug.startsWith('what-is-');

      let priority = 0.7;
      if (isPillar) priority = 0.9;
      else if (isComparison) priority = 0.8;
      else if (isCaseStudy) priority = 0.8;
      else if (isGlossary) priority = 0.6;

      return {
        url: `${baseUrl}/blog/${article.slug}`,
        lastModified: knownModificationDate(article.last_updated),
        changeFrequency: 'monthly' as const,
        priority,
      };
    });

  return [...staticPages, ...articlePages];
}
