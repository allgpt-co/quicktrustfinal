import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';
export const metadata = marketingPageMetadata('/resources/templates');
export default function TemplatesPage() { return <MarketingDetailPage pathname="/resources/templates" />; }
