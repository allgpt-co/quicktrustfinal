// @vitest-environment node
import { afterEach, describe, expect, test, vi } from 'vitest';
import fs from 'fs';
import path from 'path';
import { getAllArticles, getAllSlugs, getArticleBySlug } from '@/lib/blog';
import sitemap from '@/app/sitemap';
import config from '../next.config';

afterEach(() => vi.restoreAllMocks());

describe('migrated marketing content', () => {
  test('lists each canonical published article once', () => {
    const articles = getAllArticles();
    expect(articles).toHaveLength(166);
    expect(new Set(articles.map((article) => article.slug)).size).toBe(articles.length);
    expect(getAllSlugs()).toEqual(articles.map((article) => article.slug));
    expect(articles.every((article) => article.title && article.published)).toBe(true);
  });
  test('resolves duplicates identically for the article and listing', () => {
    const article = getArticleBySlug('acceptable-use-policy-guide');
    expect(article?.category).toBe('June 2026');
    expect(article?.title).toBe(getAllArticles().find((a) => a.slug === article?.slug)?.title);
    expect(getArticleBySlug('../../package.json')).toBeNull();
    expect(getArticleBySlug('does-not-exist')).toBeNull();
  });
  test('unpublished winning files cannot be read or listed through a duplicate', () => {
    const original = fs.readFileSync.bind(fs);
    const filename = path.join(process.cwd(), 'content/content_output/june-2026/acceptable-use-policy-guide.md');
    vi.spyOn(fs, 'readFileSync').mockImplementation(((file: fs.PathOrFileDescriptor, options: unknown) => {
      if (file === filename) return '---\npublished: false\ntitle: Hidden\n---\n# Hidden';
      return original(file, options as BufferEncoding);
    }) as typeof fs.readFileSync);
    expect(getArticleBySlug('acceptable-use-policy-guide')).toBeNull();
    expect(getAllSlugs()).not.toContain('acceptable-use-policy-guide');
  });
  test('sitemap contains only public canonical URLs and valid dates', async () => {
    const entries = sitemap();
    expect(entries).toHaveLength(179);
    expect(new Set(entries.map((entry) => entry.url)).size).toBe(entries.length);
    expect(entries.every((entry) => entry.url.startsWith('https://quicktrustapp.com'))).toBe(true);
    expect(entries.some((entry) => /\/login|\/dashboard|\/blog\/quicktrust-vs-(vanta|drata)$/.test(entry.url))).toBe(false);
    expect(entries.every((entry) => !entry.lastModified || !Number.isNaN(new Date(entry.lastModified).getTime()))).toBe(true);
    expect(await config.redirects?.()).toEqual(expect.arrayContaining([
      expect.objectContaining({ source: '/signup', destination: '/login?mode=register' }),
      expect.objectContaining({ source: '/blog/quicktrust-vs-vanta', destination: '/compare/quicktrust-vs-vanta', permanent: true }),
    ]));
  });
});
