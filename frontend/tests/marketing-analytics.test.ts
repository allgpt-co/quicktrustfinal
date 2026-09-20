import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import {
  isAllowedAnalyticsPath,
  trackMarketingLead,
  trackMarketingPageView,
} from "@/lib/marketing-analytics";

const gtag = vi.fn();

beforeEach(() => {
  vi.stubGlobal("gtag", undefined);
  vi.stubEnv("NEXT_PUBLIC_GA4_MEASUREMENT_ID", "");
  window.gtag = undefined;
  window.__qtAnalyticsConsent = undefined;
  document.cookie = "qt_analytics_consent=; Max-Age=0; path=/";
  gtag.mockReset();
});

afterEach(() => {
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
  window.gtag = undefined;
  window.__qtAnalyticsConsent = undefined;
});

describe("trackMarketingLead", () => {
  test("is a no-op until a valid public GA4 ID is configured", () => {
    window.gtag = gtag;

    trackMarketingLead("contact");

    expect(gtag).not.toHaveBeenCalled();
  });

  test("emits only the safe form type when GA4 is configured", () => {
    vi.stubEnv("NEXT_PUBLIC_GA4_MEASUREMENT_ID", "G-QUICKTRUST123");
    document.cookie = "qt_analytics_consent=granted; path=/";
    window.gtag = gtag;
    Object.defineProperty(document, "referrer", {
      configurable: true,
      value: "https://quicktrustapp.com/dashboard?token=secret",
    });

    trackMarketingLead("readiness");

    expect(gtag).toHaveBeenCalledOnce();
    expect(gtag).toHaveBeenCalledWith("event", "generate_lead", { form_type: "readiness" });
    expect(JSON.stringify(gtag.mock.calls[0])).not.toMatch(/@|email|phone|company|message/i);
  });

  test("ignores malformed measurement IDs", () => {
    vi.stubEnv("NEXT_PUBLIC_GA4_MEASUREMENT_ID", "not-a-ga4-id");
    window.gtag = gtag;

    trackMarketingLead("booking");

    expect(gtag).not.toHaveBeenCalled();
  });

  test("does not emit before explicit analytics consent", () => {
    vi.stubEnv("NEXT_PUBLIC_GA4_MEASUREMENT_ID", "G-QUICKTRUST123");
    window.gtag = gtag;

    trackMarketingLead("contact");

    expect(gtag).not.toHaveBeenCalled();
  });

  test("emits a sanitized page view without query strings or referrer data", () => {
    vi.stubEnv("NEXT_PUBLIC_GA4_MEASUREMENT_ID", "G-QUICKTRUST123");
    document.cookie = "qt_analytics_consent=granted; path=/";
    window.gtag = gtag;

    expect(trackMarketingPageView("/contact?email=secret@example.com#form", "  Contact   | QuickTrust  ")).toBe(true);
    expect(gtag).toHaveBeenCalledWith("event", "page_view", {
      page_path: "/contact",
      page_location: "http://localhost:3000/contact",
      page_title: "Contact | QuickTrust",
      page_referrer: "https://quicktrustapp.com",
    });
    expect(JSON.stringify(gtag.mock.calls[0])).not.toMatch(/secret|email=|dashboard/i);
  });

  test("allows only public marketing paths", () => {
    expect(isAllowedAnalyticsPath("/contact")).toBe(true);
    expect(isAllowedAnalyticsPath("/blog/security-guide")).toBe(true);
    expect(isAllowedAnalyticsPath("/resources/soc2-readiness-scorecard")).toBe(true);
    expect(isAllowedAnalyticsPath("/dashboard")).toBe(false);
    expect(isAllowedAnalyticsPath("/login")).toBe(false);
    expect(isAllowedAnalyticsPath("/privacy-policy")).toBe(false);
    expect(isAllowedAnalyticsPath("/resources/private")).toBe(false);
    expect(isAllowedAnalyticsPath("/resources/soc2-readiness-scorecard")).toBe(true);
  });

  test("does not emit leads from app, legal, or unknown resource paths", () => {
    vi.stubEnv("NEXT_PUBLIC_GA4_MEASUREMENT_ID", "G-QUICKTRUST123");
    document.cookie = "qt_analytics_consent=granted; path=/";
    window.gtag = gtag;

    for (const pathname of ["/dashboard", "/privacy-policy", "/resources/private"]) {
      window.history.replaceState({}, "", pathname);
      trackMarketingLead("contact");
    }

    expect(gtag).not.toHaveBeenCalled();
  });
});
