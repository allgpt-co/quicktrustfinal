import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';
export const metadata = marketingPageMetadata('/resources/case-studies');
export default function ScenariosPage() { return <MarketingDetailPage pathname="/resources/case-studies" />; }
