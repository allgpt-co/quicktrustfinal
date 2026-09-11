import type { MetadataRoute } from 'next';
import { getAllArticles } from '@/lib/blog';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://quicktrustapp.com';
  const articles = getAllArticles();
  const now = new Date();

  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 1.0,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    // Framework pages
    {
      url: `${baseUrl}/soc-2-compliance`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/hipaa-compliance`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/iso-27001-certification`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    // Comparison pages
    {
      url: `${baseUrl}/compare/quicktrust-vs-vanta`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/compare/quicktrust-vs-drata`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    // Solution pages
    {
      url: `${baseUrl}/solutions/security-questionnaire-automation`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    // Trust pages
    {
      url: `${baseUrl}/pricing`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    {
      url: `${baseUrl}/privacy-policy`,
      lastModified: now,
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/terms-of-service`,
      lastModified: now,
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
        lastModified: article.last_updated ? new Date(article.last_updated) : now,
        changeFrequency: 'monthly' as const,
        priority,
      };
    });

  return [...staticPages, ...articlePages];
}
