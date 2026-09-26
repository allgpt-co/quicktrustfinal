import MarketingDetailPage from '@/components/marketing/MarketingDetailPage';
import { marketingPageMetadata } from '@/lib/marketing-pages';

export const metadata = marketingPageMetadata('/iso-27001-certification');
export default function Page() { return <MarketingDetailPage pathname="/iso-27001-certification" />; }
