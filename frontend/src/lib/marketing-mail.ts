import sgMail from '@sendgrid/mail';
import { NextResponse } from 'next/server';
import { z } from 'zod';

const email = z.string().trim().email().max(254);
const shortText = z.string().trim().max(200);
const contactSchema = z.object({
  fullName: shortText.min(1), email,
  phone: z.string().trim().max(50).optional().default(''),
  company: shortText.optional().default(''),
  framework: shortText.optional().default(''),
  message: z.string().trim().max(5000).optional().default(''),
});
const readinessSchema = z.object({
  email, company: shortText.min(1),
  targetFramework: z.enum(['soc2', 'iso27001', 'hipaa', 'hitrust', 'pci', 'gdpr', 'multiple', 'other']),
  targetTimeline: z.enum(['1month', '3months', '6months', 'flexible']),
});

export function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]!);
}

export async function submitMarketingLead(request: Request, kind: 'contact' | 'readiness') {
  let body: unknown;
  try { body = await request.json(); }
  catch { return NextResponse.json({ error: 'Please provide a valid request.' }, { status: 400 }); }

  const parsed = (kind === 'contact' ? contactSchema : readinessSchema).safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: 'Please check the required fields and email address.' }, { status: 400 });

  const apiKey = process.env.SENDGRID_API_KEY;
  const recipient = process.env.COMPANY_EMAIL?.trim();
  const from = process.env.FROM_EMAIL?.trim();
  if (!apiKey || !email.safeParse(recipient).success || !email.safeParse(from).success) {
    return NextResponse.json({ error: 'We could not submit your request. Please try again later.' }, { status: 503 });
  }

  const fields = Object.entries(parsed.data).filter(([, value]) => value);
  const labels: Record<string, string> = { fullName: 'Name', email: 'Email', phone: 'Phone', company: 'Company', framework: 'Framework', message: 'Message', targetFramework: 'Target framework', targetTimeline: 'Target timeline' };
  const subject = kind === 'contact' ? 'New QuickTrust contact request' : 'New QuickTrust readiness snapshot request';
  const html = `<h1>${subject}</h1>${fields.map(([key, value]) => `<p><strong>${labels[key]}:</strong> ${escapeHtml(value).replace(/\n/g, '<br>')}</p>`).join('')}`;
  sgMail.setApiKey(apiKey);
  try {
    await sgMail.send({
      to: recipient!, from: { email: from!, name: 'QuickTrust' }, replyTo: parsed.data.email,
      subject, text: fields.map(([key, value]) => `${labels[key]}: ${value}`).join('\n'), html,
      trackingSettings: { clickTracking: { enable: false }, openTracking: { enable: false } },
    });
  } catch {
    console.error('QuickTrust marketing lead delivery failed');
    return NextResponse.json({ error: 'We could not submit your request. Please try again later.' }, { status: 502 });
  }

  // The lead has been accepted. An acknowledgement failure must not ask the visitor to resubmit it.
  const acknowledgement = kind === 'contact'
    ? 'Thank you for contacting QuickTrust. Our team will respond within one business day.'
    : 'Thank you for requesting a QuickTrust readiness snapshot. Our team will contact you about your compliance goals.';
  try {
    await sgMail.send({
      to: parsed.data.email, from: { email: from!, name: 'QuickTrust' }, replyTo: recipient!,
      subject: 'We received your QuickTrust request',
      text: `${acknowledgement}\nhttps://quicktrustapp.com`,
      html: `<p>${acknowledgement}</p><p><a href="https://quicktrustapp.com">QuickTrust</a></p>`,
      trackingSettings: { clickTracking: { enable: false }, openTracking: { enable: false } },
    });
  } catch { console.error('QuickTrust marketing acknowledgement delivery failed'); }
  return NextResponse.json({ success: true, message: acknowledgement });
}
