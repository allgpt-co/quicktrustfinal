import { sitemapIndexXml, xmlResponse } from '@/lib/directory-sitemap';
export const revalidate = 3600;
export function GET() {
  return xmlResponse(sitemapIndexXml());
}
