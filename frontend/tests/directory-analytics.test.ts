import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import {
  clearAnalyticsPaths,
  registerAnalyticsPaths,
  trackDirectoryEvent,
} from '@/lib/marketing-analytics';

beforeEach(() => {
  vi.stubEnv('NEXT_PUBLIC_GA4_MEASUREMENT_ID', 'G-TEST123');
  window.gtag = vi.fn();
  window.__qtAnalyticsConsent = null;
  window.history.replaceState(
    {},
    '',
    '/compliance-directory/finder?q=private%40example.com&location=IN',
  );
  registerAnalyticsPaths(['/compliance-directory/finder']);
});
afterEach(() => {
  clearAnalyticsPaths();
  vi.unstubAllEnvs();
  window.gtag = undefined;
  window.__qtAnalyticsConsent = null;
  window.history.replaceState({}, '', '/');
});
test('directory use is opt-in, bounded and separated from qualified leads', () => {
  expect(trackDirectoryEvent('directory_search')).toBe(false);
  window.__qtAnalyticsConsent = 'granted';
  expect(trackDirectoryEvent('directory_search')).toBe(true);
  expect(window.gtag).toHaveBeenCalledWith(
    'event',
    'directory_search',
    expect.objectContaining({
      content_group: 'compliance_directory',
      page_location: 'http://localhost:3000/compliance-directory/finder',
    }),
  );
  expect(JSON.stringify(vi.mocked(window.gtag!).mock.calls)).not.toMatch(
    /private|location=IN|generate_lead/,
  );
  // Runtime validation also rejects a caller bypassing the TypeScript union.
  expect(trackDirectoryEvent('private@example.com' as never)).toBe(false);
  window.__qtAnalyticsConsent = 'denied';
  expect(trackDirectoryEvent('directory_source_click')).toBe(false);
  expect(window.gtag).toHaveBeenCalledTimes(1);
});
test('unknown directory paths cannot send events', () => {
  window.__qtAnalyticsConsent = 'granted';
  window.history.replaceState({}, '', '/compliance-directory/unknown');
  expect(trackDirectoryEvent('directory_checklist_download')).toBe(false);
});
