import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';

export const metadata = marketingPageMetadata('/compare/quicktrust-vs-vanta');
export default function Page() { return <MarketingDetailPage pathname="/compare/quicktrust-vs-vanta" />; }
