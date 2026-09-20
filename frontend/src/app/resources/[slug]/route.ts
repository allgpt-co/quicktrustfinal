import { getArticleBySlug } from '@/lib/blog';
import { isResourceSlug } from '@/lib/marketing-routes';

// Downloads reuse the complete published template rather than duplicating content.
export async function GET(_request: Request, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const article = isResourceSlug(slug) ? getArticleBySlug(slug) : null;
  if (!article) return new Response('Resource not found', { status: 404 });
  return new Response(article.content, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Content-Disposition': `attachment; filename="${slug}.md"`,
      'X-Robots-Tag': 'noindex',
      'Link': `<https://quicktrustapp.com/blog/${slug}>; rel="canonical"`,
      'X-Content-Type-Options': 'nosniff',
    },
  });
}
