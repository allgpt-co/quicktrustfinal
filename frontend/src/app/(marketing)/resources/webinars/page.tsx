import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';
export const metadata = marketingPageMetadata('/resources/webinars');
export default function WebinarsPage() { return <MarketingDetailPage pathname="/resources/webinars" />; }
