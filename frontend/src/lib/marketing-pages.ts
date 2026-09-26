import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import type { Metadata } from 'next';
import { MARKETING_PATHS, CONTENT_REDIRECTS } from './marketing-routes';

export interface MarketingPage {
  path: string;
  title: string;
  description: string;
  eyebrow: string;
  indexable: boolean;
  service: boolean;
  tool?: 'readiness' | 'roi';
  faqs: Array<{ question: string; answer: string }>;
  content: string;
}
export const MARKETING_ORIGIN = 'https://quicktrustapp.com';
export const STATIC_DETAIL_PATHS = ['/trust-center', '/integrations', '/soc-2-compliance', '/hipaa-compliance', '/iso-27001-certification', '/compare/quicktrust-vs-vanta', '/compare/quicktrust-vs-drata'];
const directory = path.join(process.cwd(), 'content/marketing-pages');

/** Metadata, rendering and search discovery consume the same publication record. */
export function getMarketingPages(): MarketingPage[] {
  const seen = new Set<string>();
  return fs.readdirSync(directory).filter((file) => file.endsWith('.md')).sort().map((file) => {
    const { data, content } = matter(fs.readFileSync(path.join(directory, file), 'utf8'), {
      engines: { yaml: { parse: (value: string) => yaml.load(value, { schema: yaml.JSON_SCHEMA }) as Record<string, unknown> } },
    });
    if (!MARKETING_PATHS.some((route) => route === data.path) || CONTENT_REDIRECTS[data.path]
      || seen.has(data.path) || !data.title || !data.description || typeof data.indexable !== 'boolean'
      || (data.tool && !['readiness', 'roi'].includes(data.tool))
      || (data.faqs && (!Array.isArray(data.faqs) || !data.faqs.every((faq: { question?: unknown; answer?: unknown }) => typeof faq.question === 'string' && typeof faq.answer === 'string')))) {
      throw new Error(`Invalid marketing page publication record: ${file}`);
    }
    seen.add(data.path);
    return {
      path: data.path, title: String(data.title), description: String(data.description),
      eyebrow: String(data.eyebrow || 'QuickTrust'), indexable: data.indexable,
      service: data.service === true, tool: data.tool, faqs: data.faqs || [], content,
    };
  });
}
export function getMarketingPage(pathname: string): MarketingPage | undefined {
  return getMarketingPages().find((page) => page.path === pathname);
}
export function marketingPageMetadata(pathname: string): Metadata {
  const page = getMarketingPage(pathname);
  if (!page) return { title: 'Page Not Found', robots: { index: false, follow: false } };
  const url = MARKETING_ORIGIN + page.path;
  const image = `${MARKETING_ORIGIN}/og/${page.path.split('/').at(-1)}`;
  return {
    title: page.title, description: page.description, alternates: { canonical: url },
    robots: { index: page.indexable, follow: true },
    openGraph: { title: page.title, description: page.description, url, siteName: 'QuickTrust', type: 'website', images: [{ url: image, width: 1200, height: 630, alt: page.title }] },
    twitter: { card: 'summary_large_image', title: page.title, description: page.description, images: [image] },
  };
}
