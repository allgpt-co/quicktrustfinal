import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';

export const metadata = marketingPageMetadata('/trust-center');
export default function Page() { return <MarketingDetailPage pathname="/trust-center" />; }
