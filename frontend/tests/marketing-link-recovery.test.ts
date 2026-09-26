// @vitest-environment node
import { describe, expect, test } from 'vitest';
import { NextRequest } from 'next/server';
import { getAllSlugs, getArticleBySlug } from '@/lib/blog';
import { canonicalMarketingHref, CONTENT_REDIRECTS, MARKETING_PATHS, RESOURCE_SLUGS } from '@/lib/marketing-routes';
import { middleware } from '@/middleware';
import { GET } from '@/app/resources/[slug]/route';
import sitemap from '@/app/sitemap';
import config from '../next.config';

describe('public content link recovery', () => {
  test('all exact aliases resolve in one hop to a published canonical page', async () => {
    const canonical = new Set<string>([...MARKETING_PATHS, ...getAllSlugs().map((slug) => `/blog/${slug}`)]);
    const redirects = await config.redirects?.();
    for (const [source, destination] of Object.entries(CONTENT_REDIRECTS)) {
      expect(canonical.has(destination), `${source} -> ${destination}`).toBe(true);
      expect(CONTENT_REDIRECTS[destination]).toBeUndefined();
      expect(redirects).toContainEqual({ source, destination, permanent: true });
    }
  });
  test('rendered links go directly to the canonical path and keep attribution and anchors', () => {
    expect(canonicalMarketingHref('/blog/soc2-complete-guide?utm_source=guide#cost')).toBe('/blog/pillar-soc2-complete-guide?utm_source=guide#cost');
    expect(canonicalMarketingHref('https://quicktrustapp.com/demo')).toBe('/contact');
    expect(canonicalMarketingHref('https://www.quicktrust.ai/blog/what-is-soc-2')).toBe('/blog/what-is-soc2');
    expect(canonicalMarketingHref('pci-dss-audit-cost-guide.md', '/blog/pillar-pci-dss-complete-guide')).toBe('/blog/pci-dss-audit-cost-guide');
    expect(canonicalMarketingHref('../evergreen/iso-27001-vs-soc2-guide.md', '/blog/multi-framework-compliance-strategy')).toBe('/blog/iso27001-vs-soc2-comparison');
    for (const href of ['https://other.example/blog/what-is-soc-2', '//other.example/demo', '#section', 'mailto:info@example.com', '/dashboard', '/blog/unknown']) {
      expect(canonicalMarketingHref(href)).toBe(href);
    }
  });
  test('all five advertised resources download the complete existing template without login', async () => {
    for (const slug of RESOURCE_SLUGS) {
      const request = new NextRequest(`https://quicktrustapp.com/resources/${slug}`);
      expect(middleware(request).status).toBe(200);
      const response = await GET(request, { params: Promise.resolve({ slug }) });
      expect(response.status).toBe(200);
      expect(response.headers.get('content-type')).toContain('text/markdown');
      expect(response.headers.get('content-disposition')).toBe(`attachment; filename="${slug}.md"`);
      expect(response.headers.get('x-robots-tag')).toBe('noindex');
      expect(response.headers.get('link')).toContain(`/blog/${slug}`);
      expect(await response.text()).toBe(getArticleBySlug(slug)?.content);
    }
  });
  test('unknown resources and lookalike prefixes do not expose protected content', async () => {
    for (const path of ['/resources/private', '/resources/soc2-readiness-scorecard/private', '/resources-admin', '/content/private', '/dashboard', '/policies']) {
      expect(middleware(new NextRequest(`https://quicktrustapp.com${path}`)).status).toBe(307);
    }
    for (const slug of ['../../package.json', 'soc2-report-explained', 'unknown']) {
      expect((await GET(new Request('https://quicktrustapp.com'), { params: Promise.resolve({ slug }) })).status).toBe(404);
    }
  });
  test('sitemap excludes aliases and downloads and does not invent modification dates', () => {
    for (const entry of sitemap()) {
      const pathname = new URL(entry.url).pathname;
      expect(CONTENT_REDIRECTS[pathname]).toBeUndefined();
      expect(RESOURCE_SLUGS.some((slug) => pathname === '/resources/' + slug)).toBe(false);
      if (!pathname.startsWith('/blog/')) expect(entry.lastModified).toBeUndefined();
      if (entry.lastModified) expect(new Date(entry.lastModified).getTime()).toBeLessThanOrEqual(Date.now());
    }
  });
});
