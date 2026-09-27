import fs from 'node:fs';
import path from 'node:path';
import { isVerified, validateDirectory, type Directory, type Requirement } from './directory-model';
import { MARKETING_PATHS, CONTENT_REDIRECTS } from './marketing-routes';
import { getAllSlugs } from './blog';

export const DIRECTORY_PATH = '/compliance-directory';
export const DIRECTORY_ORIGIN = 'https://quicktrustapp.com';
export const DIRECTORY_UPDATED = '2026-09-27';
let registry: Directory | undefined;
function contentRoot() {
  return path.join(
    process.cwd(),
    process.cwd().endsWith('/frontend') ? 'content' : 'frontend/content',
    'compliance-directory',
  );
}
function json(name: string) {
  return JSON.parse(fs.readFileSync(path.join(contentRoot(), `${name}.json`), 'utf8'));
}

export function getDirectory(): Directory {
  if (registry) return registry;
  const content: Record<string, string> = {};
  const articles = path.join(contentRoot(), 'articles');
  if (fs.existsSync(articles))
    for (const file of fs.readdirSync(articles).filter((name) => /^[a-z0-9-]+\.md$/.test(name)))
      content[file.slice(0, -3)] = fs.readFileSync(path.join(articles, file), 'utf8');
  registry = validateDirectory({
    requirements: json('requirements'),
    sources: json('sources'),
    jurisdictions: [...json('geography'), ...json('jurisdictions-extra')],
    industries: json('industries'),
    coverage: json('coverage'),
    content,
  });
  const publishedPaths = new Set<string>([
    ...MARKETING_PATHS,
    ...getAllSlugs().map((slug) => `/blog/${slug}`),
  ]);
  for (const record of registry.requirements)
    if (
      CONTENT_REDIRECTS[record.canonicalPath] ||
      (!record.canonicalPath.startsWith(DIRECTORY_PATH + '/') &&
        !publishedPaths.has(record.canonicalPath))
    )
      throw new Error(`Unreviewed or redirected canonical ${record.canonicalPath}`);
  return registry;
}

export function getImports(): {
  dataset: string;
  url: string;
  retrievedAt: string;
  sha256: string;
  count: number;
  verification: string;
}[] {
  return json('imports');
}
export function getCatalogue(): {
  name: string;
  url: string;
  locations: string[];
  activities: string[];
  status: string;
  note: string;
}[] {
  return json('uk-catalogue');
}
export function requirementPath(record: Requirement): string {
  return record.canonicalPath;
}
export function jurisdictionPath(id: string): string {
  return `${DIRECTORY_PATH}/jurisdictions/${id.toLowerCase()}`;
}
export function industryPath(id: string): string {
  return `${DIRECTORY_PATH}/industries/${id.toLowerCase()}`;
}

export function directoryAnalyticsManifest() {
  const d = getDirectory();
  return {
    jurisdictions: d.jurisdictions.map((r) => r.id.toLowerCase()),
    industries: d.industries.map((r) => r.id.toLowerCase()),
    requirements: d.requirements
      .filter((r) => r.canonicalPath.startsWith(DIRECTORY_PATH + '/'))
      .map((r) => r.id),
  };
}

export function directorySitemapEntries(asOf?: string): { path: string; updatedAt: string }[] {
  return [
    { path: DIRECTORY_PATH, updatedAt: DIRECTORY_UPDATED },
    { path: `${DIRECTORY_PATH}/coverage`, updatedAt: DIRECTORY_UPDATED },
    ...getDirectory()
      .requirements.filter(
        (r) => isVerified(r, asOf) && r.canonicalPath.startsWith(DIRECTORY_PATH + '/'),
      )
      .map((r) => ({ path: r.canonicalPath, updatedAt: r.updatedAt })),
  ];
}

export function checklistText(record: Requirement, asOf?: string): string | null {
  if (!isVerified(record, asOf)) return null;
  const d = getDirectory();
  const source = (id: string) => d.sources.find((s) => s.id === id)!.url;
  return [
    `${record.name} — preparation checklist`,
    `Jurisdiction: ${record.jurisdictions.map((id) => d.jurisdictions.find((j) => j.id === id)!.name).join('; ')}`,
    `Reviewed: ${record.reviewedAt}; next review: ${record.nextReviewAt}`,
    `Review scope: ${record.review!.scope}`,
    `Version: ${record.version ?? 'See official source'}`,
    `Page: ${DIRECTORY_ORIGIN}${record.canonicalPath}`,
    '',
    'Potential relevance must be checked for your organization. This checklist is not an exhaustive statement of legal obligations or a certificate.',
    '',
    ...record.documents.map((item) => `[ ] ${item.text}\n    Source: ${source(item.sourceId)}`),
    '',
    `Official next step: ${record.applicationUrl}`,
    '',
    'Sources:',
    ...record.sourceIds.map(source),
    '',
  ].join('\n');
}
