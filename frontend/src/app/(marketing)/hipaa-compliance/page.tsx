import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';

export const metadata = marketingPageMetadata('/hipaa-compliance');
export default function Page() { return <MarketingDetailPage pathname="/hipaa-compliance" />; }
