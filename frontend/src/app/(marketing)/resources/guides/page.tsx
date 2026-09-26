import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';
export const metadata = marketingPageMetadata('/resources/guides');
export default function GuidesPage() { return <MarketingDetailPage pathname="/resources/guides" />; }
