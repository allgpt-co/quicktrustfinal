import { submitMarketingLead } from '@/lib/marketing-mail';
export async function POST(request: Request) { return submitMarketingLead(request, 'readiness'); }
