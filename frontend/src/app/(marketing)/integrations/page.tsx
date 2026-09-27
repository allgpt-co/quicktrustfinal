import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';

export const metadata = marketingPageMetadata('/integrations');
export default function Page() { return <MarketingDetailPage pathname="/integrations" />; }
