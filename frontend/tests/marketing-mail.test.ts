// @vitest-environment node
import { beforeEach, afterEach, describe, expect, test, vi } from 'vitest';
import sgMail from '@sendgrid/mail';
import { POST as contact } from '@/app/api/contact/route';
import { POST as readiness } from '@/app/api/readiness-snapshot/route';

vi.mock('@sendgrid/mail', () => ({ default: { setApiKey: vi.fn(), send: vi.fn() } }));
const send = vi.mocked(sgMail.send);
const request = (body: unknown) => new Request('https://quicktrustapp.com/api/contact', { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } });
const lead = { fullName: '<script>bad</script>', email: 'visitor@example.com', company: 'Test & Co', message: 'Hello <b>there</b>' };

beforeEach(() => {
  vi.stubEnv('SENDGRID_API_KEY', 'test-only-key');
  vi.stubEnv('FROM_EMAIL', 'sender@example.com');
  vi.stubEnv('COMPANY_EMAIL', 'leads@example.com');
  send.mockReset();
  send.mockResolvedValue([{} as never, {}]);
  vi.spyOn(console, 'error').mockImplementation(() => {});
});
afterEach(() => { vi.unstubAllEnvs(); vi.restoreAllMocks(); });

describe('marketing lead delivery', () => {
  test('sends the escaped lead and acknowledgement', async () => {
    expect((await contact(request(lead))).status).toBe(200);
    expect(send).toHaveBeenCalledTimes(2);
    const email = send.mock.calls[0][0] as { html: string; to: string; replyTo: string };
    expect(email.to).toBe('leads@example.com');
    expect(email.replyTo).toBe(lead.email);
    expect(email.html).toContain('&lt;script&gt;');
    expect(email.html).not.toContain('<script>');
    expect(email.html).toContain('Test &amp; Co');
  });
  test('supports the readiness form contract', async () => {
    expect((await readiness(request({ email: lead.email, company: 'Test', targetFramework: 'soc2', targetTimeline: '3months' }))).status).toBe(200);
  });
  test.each([{}, { ...lead, email: 'invalid' }, { ...lead, fullName: '' }, { ...lead, message: 'x'.repeat(5001) }])('rejects invalid input before sending', async (body) => {
    expect((await contact(request(body))).status).toBe(400);
    expect(send).not.toHaveBeenCalled();
  });
  test('rejects invalid readiness choices and malformed JSON', async () => {
    expect((await readiness(request({ email: lead.email, company: 'Test', targetFramework: 'unknown', targetTimeline: '3months' }))).status).toBe(400);
    expect((await contact(new Request('https://quicktrustapp.com/api/contact', { method: 'POST', body: '{' }))).status).toBe(400);
    expect(send).not.toHaveBeenCalled();
  });
  test('returns an honest error when mail is not configured', async () => {
    vi.stubEnv('SENDGRID_API_KEY', '');
    const response = await contact(request(lead));
    expect(response.status).toBe(503);
    expect(await response.json()).not.toHaveProperty('success');
    expect(send).not.toHaveBeenCalled();
  });
  test('does not disclose provider failures or send an acknowledgement for a lost lead', async () => {
    send.mockRejectedValueOnce(new Error('private provider detail'));
    const response = await contact(request(lead));
    expect(response.status).toBe(502);
    expect(await response.text()).not.toContain('private provider detail');
    expect(send).toHaveBeenCalledTimes(1);
  });
  test('acknowledgement failure does not cause duplicate lead submissions', async () => {
    send.mockResolvedValueOnce([{} as never, {}]).mockRejectedValueOnce(new Error('ack failed'));
    const response = await contact(request(lead));
    expect(response.status).toBe(200);
    expect(await response.json()).toMatchObject({ success: true });
  });
});
