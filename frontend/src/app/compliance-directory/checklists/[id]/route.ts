import { checklistText, getDirectory } from '@/lib/compliance-directory';

export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const record = getDirectory().requirements.find((r) => r.id === id);
  const text = record ? checklistText(record) : null;
  if (!text)
    return new Response('A checklist is available only for a currently verified record.', {
      status: record ? 409 : 404,
      headers: { 'X-Robots-Tag': 'noindex, nofollow', 'Cache-Control': 'no-store' },
    });
  return new Response(text, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Content-Disposition': `attachment; filename="${record!.id}-checklist.txt"`,
      'X-Robots-Tag': 'noindex, nofollow',
      'Cache-Control': 'no-store',
    },
  });
}
