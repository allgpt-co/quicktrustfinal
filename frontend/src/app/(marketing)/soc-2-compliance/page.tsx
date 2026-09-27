import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';

export const metadata = marketingPageMetadata('/soc-2-compliance');
export default function Page() { return <MarketingDetailPage pathname="/soc-2-compliance" />; }
