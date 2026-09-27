import { directorySitemapEntries, DIRECTORY_ORIGIN, DIRECTORY_PATH } from './compliance-directory';

const SIZE = 1000;
export const xmlEscape = (s: string) =>
  s.replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[c]!,
  );
export function sitemapIndexXml(): string {
  const count = Math.ceil(directorySitemapEntries().length / SIZE);
  return `<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${Array.from({ length: count }, (_, i) => `<sitemap><loc>${DIRECTORY_ORIGIN}${DIRECTORY_PATH}/sitemaps/${i}.xml</loc></sitemap>`).join('')}</sitemapindex>`;
}
export function sitemapPageXml(page: number, asOf?: string): string | null {
  const rows = directorySitemapEntries(asOf).slice(page * SIZE, (page + 1) * SIZE);
  if (!rows.length || page < 0 || !Number.isSafeInteger(page)) return null;
  return `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${rows.map((r) => `<url><loc>${xmlEscape(DIRECTORY_ORIGIN + r.path)}</loc><lastmod>${r.updatedAt}</lastmod></url>`).join('')}</urlset>`;
}
export function xmlResponse(xml: string | null): Response {
  return new Response(xml ?? 'Not found', {
    status: xml ? 200 : 404,
    headers: {
      'Content-Type': xml ? 'application/xml; charset=utf-8' : 'text/plain',
      'X-Robots-Tag': 'noindex',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
