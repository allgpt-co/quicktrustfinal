import { sitemapPageXml, xmlResponse } from '@/lib/directory-sitemap';
export const revalidate = 3600;
export async function GET(_request: Request, { params }: { params: Promise<{ file: string }> }) {
  const { file } = await params;
  return xmlResponse(
    /^(0|[1-9]\d*)\.xml$/.test(file) ? sitemapPageXml(Number(file.slice(0, -4))) : null,
  );
}
