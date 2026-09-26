import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { getMarketingPages, marketingPageMetadata, STATIC_DETAIL_PATHS } from '@/lib/marketing-pages';

export function generateStaticParams() {
  return getMarketingPages().filter((page) => !page.path.startsWith('/resources/') && !STATIC_DETAIL_PATHS.includes(page.path))
    .map((page) => ({ slug: page.path.slice(1).split('/') }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string[] }> }) {
  const { slug } = await params;
  return marketingPageMetadata('/' + slug.join('/'));
}

export default async function DetailPage({ params }: { params: Promise<{ slug: string[] }> }) {
  const { slug } = await params;
  return <MarketingDetailPage pathname={'/' + slug.join('/')} />;
}
