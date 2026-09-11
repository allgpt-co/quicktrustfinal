import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import { ARTICLE_REDIRECTS } from './marketing-routes';

const contentDirectory = path.join(process.cwd(), 'content/content_output');
const matterOptions = {
  engines: { yaml: { parse: (source: string) => yaml.load(source, { schema: yaml.JSON_SCHEMA }) as Record<string, unknown> } },
};

export interface ArticleMeta {
  slug: string;
  title: string;
  meta_description: string;
  target_keyword: string;
  secondary_keywords?: string;
  word_count_target?: string;
  publish_date?: string;
  last_updated?: string;
  author?: string;
  published?: boolean;
  category: string;
  subcategory?: string;
}
export interface Article extends ArticleMeta { content: string }

function stringValue(value: unknown): string | undefined {
  if (value == null) return undefined;
  return Array.isArray(value) ? value.map(String).join(', ') : String(value);
}

function markdownFiles(directory: string): string[] {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const filename = path.join(directory, entry.name);
    return entry.isDirectory() ? markdownFiles(filename) : entry.name.endsWith('.md') ? [filename] : [];
  }).sort();
}

// All consumers use the same first-file-wins policy, including unpublished entries.
function articleFiles(): Map<string, string> {
  const files = new Map<string, string>();
  for (const filename of markdownFiles(contentDirectory)) {
    const slug = path.basename(filename, '.md');
    if (!files.has(slug)) files.set(slug, filename);
  }
  return files;
}

function readArticle(slug: string, filename: string): Article | null {
  const { data, content } = matter(fs.readFileSync(filename, 'utf8'), matterOptions);
  if (data.published === false) return null;
  const [folder, subfolder] = path.relative(contentDirectory, filename).split(path.sep);
  return {
    slug,
    title: stringValue(data.title) || content.match(/^#\s+(.+)$/m)?.[1] || 'Untitled',
    meta_description: stringValue(data.meta_description) || '',
    target_keyword: stringValue(data.target_keyword ?? data.target_keywords) || '',
    secondary_keywords: stringValue(data.secondary_keywords),
    word_count_target: stringValue(data.word_count_target),
    publish_date: stringValue(data.publish_date),
    last_updated: stringValue(data.last_updated),
    author: stringValue(data.author) || 'QuickTrust Editorial',
    published: true,
    category: folder === 'evergreen' ? 'Evergreen' : folder.split('-').map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
    subcategory: folder === 'evergreen' ? subfolder : undefined,
    content,
  };
}

export function getArticleBySlug(slug: string): Article | null {
  const filename = articleFiles().get(slug);
  return filename ? readArticle(slug, filename) : null;
}

export function getAllArticles(): ArticleMeta[] {
  return [...articleFiles()].filter(([slug]) => !ARTICLE_REDIRECTS[slug]).flatMap(([slug, filename]) => {
    const article = readArticle(slug, filename);
    if (!article) return [];
    const { content: _content, ...metadata } = article;
    return [metadata];
  }).sort((a, b) => Number(b.slug.startsWith('pillar-')) - Number(a.slug.startsWith('pillar-')) || a.title.localeCompare(b.title));
}

export function getAllSlugs(): string[] { return getAllArticles().map((article) => article.slug); }

export function getArticlesByCategory(): Record<string, ArticleMeta[]> {
  const grouped: Record<string, ArticleMeta[]> = {};
  for (const article of getAllArticles()) {
    const category = article.subcategory ? `${article.category} — ${article.subcategory.charAt(0).toUpperCase()}${article.subcategory.slice(1)}` : article.category;
    (grouped[category] ??= []).push(article);
  }
  return grouped;
}

export function getRelatedArticles(currentSlug: string, limit = 3): ArticleMeta[] {
  const current = getArticleBySlug(currentSlug);
  if (!current) return [];
  const keywords = `${current.target_keyword}, ${current.secondary_keywords || ''}`.toLowerCase().split(/[,\s]+/).filter(Boolean);
  return getAllArticles().filter((article) => article.slug !== currentSlug).map((article) => {
    const terms = `${article.target_keyword}, ${article.secondary_keywords || ''}`.toLowerCase().split(/[,\s]+/);
    const score = (article.category === current.category ? 3 : 0) + keywords.filter((keyword) => terms.includes(keyword)).length * 2;
    return { article, score };
  }).sort((a, b) => b.score - a.score).slice(0, limit).map(({ article }) => article);
}
