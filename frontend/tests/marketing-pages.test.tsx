// @vitest-environment node
import { describe, expect, test } from 'vitest';
import { renderToStaticMarkup } from 'react-dom/server';
import fs from 'fs';
import path from 'path';
import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { getMarketingPages, marketingPageMetadata } from '@/lib/marketing-pages';
import { getAllArticles, getArticleBySlug } from '@/lib/blog';
import { CONTENT_REDIRECTS, MARKETING_PATHS, RESOURCE_SLUGS } from '@/lib/marketing-routes';
import sitemap from '@/app/sitemap';

describe('completed marketing pages', () => {
  test('publication records govern metadata, canonical URLs and sitemap eligibility', () => {
    const pages = getMarketingPages();
    const urls = new Set(sitemap().map((entry) => entry.url));
    expect(pages).toHaveLength(28);
    for (const page of pages) {
      const meta = marketingPageMetadata(page.path);
      const canonical = 'https://quicktrustapp.com' + page.path;
      expect(meta.alternates?.canonical).toBe(canonical);
      expect(meta.robots).toMatchObject({ index: page.indexable });
      expect(urls.has(canonical), page.path).toBe(page.indexable);
      expect(CONTENT_REDIRECTS[page.path]).toBeUndefined();
    }
    for (const route of ['/privacy-policy', '/terms-of-service', '/company/careers', '/company/partners', '/resources/webinars']) {
      expect(urls.has('https://quicktrustapp.com' + route)).toBe(false);
    }
    expect(marketingPageMetadata('/unknown').robots).toMatchObject({ index: false });
  });

  test('four explicit HTML resource pages take precedence over the download route', () => {
    for (const slug of ['guides', 'templates', 'case-studies', 'webinars']) {
      expect(fs.existsSync(path.join(process.cwd(), 'src/app/(marketing)/resources', slug, 'page.tsx'))).toBe(true);
      const html = renderToStaticMarkup(<MarketingDetailPage pathname={'/resources/' + slug} />);
      expect(html.match(/<h1[ >]/g)).toHaveLength(1);
      expect(html).not.toContain('Resource not found');
    }
    expect(renderToStaticMarkup(<MarketingDetailPage pathname="/resources/templates" />)).toContain('/resources/audit-evidence-checklist');
  });

  test('new content links to known canonical pages or the five downloads', () => {
    const known = new Set<string>([...MARKETING_PATHS, ...getAllArticles().map((a) => '/blog/' + a.slug), ...RESOURCE_SLUGS.map((slug) => '/resources/' + slug)]);
    for (const page of getMarketingPages()) {
      for (const match of page.content.matchAll(/\]\((\/[^)]+)\)/g)) {
        const pathname = match[1].split(/[?#]/)[0];
        expect(known.has(pathname), page.path + ' -> ' + pathname).toBe(true);
        expect(CONTENT_REDIRECTS[pathname], page.path + ' -> alias ' + pathname).toBeUndefined();
      }
    }
  });

  test('public product routes do not resolve to dashboard management screens', () => {
    for (const slug of ['integrations', 'trust-center']) {
      expect(fs.existsSync(path.join(process.cwd(), 'src/app/(marketing)', slug, 'page.tsx'))).toBe(true);
      expect(fs.existsSync(path.join(process.cwd(), 'src/app/(dashboard)', slug, 'page.tsx'))).toBe(false);
      expect(fs.existsSync(path.join(process.cwd(), 'src/app/(dashboard)/settings', slug, 'page.tsx'))).toBe(true);
    }
  });

  test('FAQ structured data is also visible on the page', () => {
    const page = getMarketingPages().find((p) => p.path === '/soc-2-compliance')!;
    const html = renderToStaticMarkup(<MarketingDetailPage pathname={page.path} />);
    expect(html).toContain('"@type":"FAQPage"');
    expect(html).toContain('"@type":"Service"');
    for (const faq of page.faqs) expect(html).toContain(faq.question);
  });

  test('the editorial queue retains every canonical article and eliminates title collisions', () => {
    const articles = getAllArticles();
    expect(articles).toHaveLength(166);
    expect(new Set(articles.map((a) => a.title.toLowerCase())).size).toBe(articles.length);
    const scenarios = articles.filter((a) => a.slug.startsWith('case-study-'));
    expect(scenarios).toHaveLength(19);
    for (const article of scenarios) {
      expect(article.title).toMatch(/^Illustrative Scenario:/);
      expect(getArticleBySlug(article.slug)?.content).toContain('not a verified customer case study');
      expect(getArticleBySlug(article.slug)?.content).not.toMatch(/The Results|What They Said|\$[0-9]|\d+%|in \d+ weeks/);
    }
  });
});
