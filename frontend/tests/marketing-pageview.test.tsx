import { cleanup, render, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import MarketingAnalytics from "@/components/marketing/MarketingAnalytics";
import { setAnalyticsConsent } from "@/lib/marketing-analytics";

let currentPath = "/contact";
const gtag = vi.fn();

vi.mock("next/navigation", () => ({
  usePathname: () => currentPath,
}));

beforeEach(() => {
  currentPath = "/contact";
  vi.stubEnv("NEXT_PUBLIC_GA4_MEASUREMENT_ID", "G-QUICKTRUST123");
  document.cookie = "qt_analytics_consent=granted; path=/";
  window.__qtAnalyticsConsent = undefined;
  window.__qtGa4ConfiguredId = undefined;
  window.dataLayer = [];
  window.gtag = gtag;
  gtag.mockReset();
  document.getElementById("quicktrust-ga4-script")?.remove();
});

afterEach(() => {
  cleanup();
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
  document.getElementById("quicktrust-ga4-script")?.remove();
  document.cookie = "qt_analytics_consent=; Max-Age=0; path=/";
  window.gtag = undefined;
  window.__qtGa4ConfiguredId = undefined;
});

describe("MarketingAnalytics", () => {
  test("configures GA4 without automatic page views and sends one sanitized initial view", async () => {
    render(<MarketingAnalytics />);

    await waitFor(() => expect(gtag).toHaveBeenCalledWith("event", "page_view", expect.any(Object)));
    expect(gtag).toHaveBeenCalledWith("consent", "default", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      wait_for_update: 500,
    });
    expect(gtag).toHaveBeenCalledWith("consent", "update", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    expect(gtag).toHaveBeenCalledWith("config", "G-QUICKTRUST123", expect.objectContaining({
      send_page_view: false,
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      page_location: "http://localhost:3000/contact",
      page_referrer: "",
    }));
    expect(gtag.mock.calls.filter(([command, name]) => command === "event" && name === "page_view")).toHaveLength(1);
    expect(gtag.mock.calls.find(([command, name]) => command === "event" && name === "page_view")?.[2]).toEqual({
      page_path: "/contact",
      page_location: "http://localhost:3000/contact",
      page_title: expect.any(String),
      page_referrer: "",
    });
  });

  test("sends one page view for each client pathname and never includes query values", async () => {
    const view = render(<MarketingAnalytics />);
    await waitFor(() => expect(gtag.mock.calls.filter(([command, name]) => command === "event" && name === "page_view")).toHaveLength(1));

    currentPath = "/pricing?company=secret";
    view.rerender(<MarketingAnalytics />);
    await waitFor(() => expect(gtag.mock.calls.filter(([command, name]) => command === "event" && name === "page_view")).toHaveLength(2));

    const pageViews = gtag.mock.calls.filter(([command, name]) => command === "event" && name === "page_view");
    expect(pageViews[1][2]).toMatchObject({ page_path: "/pricing", page_location: "http://localhost:3000/pricing" });
    expect(JSON.stringify(pageViews)).not.toContain("secret");

    // Query-only changes are not new canonical pages and must not duplicate it.
    currentPath = "/pricing?another=secret";
    view.rerender(<MarketingAnalytics />);
    expect(gtag.mock.calls.filter(([command, name]) => command === "event" && name === "page_view")).toHaveLength(2);

    // Re-rendering without a route change must not duplicate the view.
    view.rerender(<MarketingAnalytics />);
    expect(gtag.mock.calls.filter(([command, name]) => command === "event" && name === "page_view")).toHaveLength(2);
  });

  test("does not load or emit analytics without consent or on app routes", async () => {
    document.cookie = "qt_analytics_consent=; Max-Age=0; path=/";
    const view = render(<MarketingAnalytics />);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(gtag.mock.calls.filter(([command, name]) => command === "event" && name === "page_view")).toHaveLength(0);
    expect(document.getElementById("quicktrust-ga4-script")).toBeNull();

    document.cookie = "qt_analytics_consent=granted; path=/";
    currentPath = "/dashboard";
    view.rerender(<MarketingAnalytics />);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(gtag.mock.calls.filter(([command, name]) => command === "event")).toHaveLength(0);
    expect(document.getElementById("quicktrust-ga4-script")).toBeNull();
  });

  test("uses the real gtag arguments-object queue and revocation blocks later views", async () => {
    window.gtag = undefined;
    const view = render(<MarketingAnalytics />);
    await waitFor(() => expect(window.dataLayer?.length).toBeGreaterThan(0));

    const queued = window.dataLayer?.find((entry) => {
      return typeof entry === "object" && entry !== null && !Array.isArray(entry)
        && Array.from(entry as IArguments)[0] === "event";
    });
    expect(queued).toBeDefined();
    expect(Array.isArray(queued)).toBe(false);
    expect(Array.from(queued as IArguments)).toEqual([
      "event",
      "page_view",
      expect.objectContaining({
        page_location: "http://localhost:3000/contact",
        page_referrer: "",
      }),
    ]);

    const pageViewsBeforeRevoke = window.dataLayer?.filter((entry) => Array.from(entry as IArguments)[1] === "page_view").length;
    setAnalyticsConsent("denied");
    await waitFor(() => expect((window as unknown as Record<string, boolean>)["ga-disable-G-QUICKTRUST123"]).toBe(true));
    expect(window.dataLayer?.filter((entry) => Array.from(entry as IArguments)[1] === "page_view").length).toBe(pageViewsBeforeRevoke);

    currentPath = "/dashboard";
    view.rerender(<MarketingAnalytics />);
    setAnalyticsConsent("granted");
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(window.dataLayer?.filter((entry) => Array.from(entry as IArguments)[1] === "page_view").length).toBe(pageViewsBeforeRevoke);
  });
});
