import { isMarketingPath } from "@/lib/marketing-routes";

export type MarketingLeadForm = "contact" | "booking" | "readiness";

export type MarketingPageView = {
  page_path: string;
  page_location: string;
  page_title: string;
  page_referrer: string;
};

type Gtag = {
  (command: "js", date: Date): void;
  (command: "consent", action: "default" | "update", parameters: ConsentParameters): void;
  (command: "config", measurementId: string, parameters: { send_page_view: false; anonymize_ip: true }): void;
  (command: "event", eventName: "generate_lead", parameters: { form_type: MarketingLeadForm }): void;
  (command: "event", eventName: "page_view", parameters: MarketingPageView): void;
};

export type ConsentParameters = {
  analytics_storage: "granted" | "denied";
  ad_storage: "granted" | "denied";
  ad_user_data: "granted" | "denied";
  ad_personalization: "granted" | "denied";
  wait_for_update?: number;
};

const consentGranted: ConsentParameters = {
  analytics_storage: "granted",
  ad_storage: "denied",
  ad_user_data: "denied",
  ad_personalization: "denied",
};

const consentDenied: ConsentParameters = {
  analytics_storage: "denied",
  ad_storage: "denied",
  ad_user_data: "denied",
  ad_personalization: "denied",
};

declare global {
  interface Window {
    dataLayer?: unknown[];
    gtag?: Gtag;
    /** Optional bridge for a consent manager to expose its current decision. */
    __qtAnalyticsConsent?: boolean;
    __qtGa4ConfiguredId?: string;
  }
}

const validMeasurementId = /^G-[A-Z0-9]+$/;
const analyticsConsentCookie = "qt_analytics_consent";
const excludedMarketingPaths = new Set(["/privacy-policy", "/terms-of-service"]);

export function getGa4MeasurementId(): string | null {
  const measurementId = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID?.trim();
  return measurementId && validMeasurementId.test(measurementId) ? measurementId : null;
}

/**
 * Analytics is opt-in. A consent manager may set this cookie and dispatch the
 * `qt:analytics-consent` event after the user accepts analytics cookies.
 */
export function hasAnalyticsConsent(): boolean {
  if (typeof window !== "undefined" && window.__qtAnalyticsConsent === true) return true;
  if (typeof document === "undefined") return false;

  return document.cookie.split(";").some((entry) => {
    const [name, ...valueParts] = entry.trim().split("=");
    if (name !== analyticsConsentCookie) return false;
    try {
      return decodeURIComponent(valueParts.join("=")) === "granted";
    } catch {
      return false;
    }
  });
}

export function getAnalyticsConsentParameters(granted: boolean): ConsentParameters {
  return granted ? consentGranted : consentDenied;
}

function normalizePathname(pathname: string): string {
  if (!pathname || !pathname.startsWith("/")) return "/";
  const withoutQuery = pathname.split(/[?#]/, 1)[0] || "/";
  if (withoutQuery === "/") return "/";
  return withoutQuery.replace(/\/+$/, "");
}

/** Only public, explicitly allowlisted marketing pages may emit analytics. */
export function isAllowedAnalyticsPath(pathname: string): boolean {
  const normalized = normalizePathname(pathname);
  if (excludedMarketingPaths.has(normalized)) return false;
  return isMarketingPath(normalized);
}

function safePageTitle(title: string): string {
  const normalized = title.replace(/\s+/g, " ").trim();
  return (normalized || "QuickTrust").slice(0, 160);
}

function safePagePath(pathname: string): string {
  const normalized = normalizePathname(pathname);
  return normalized === "/" ? "/" : normalized;
}

function safePageLocation(pathname: string): string {
  const pagePath = safePagePath(pathname);
  const origin = typeof window !== "undefined" ? window.location.origin : "https://quicktrustapp.com";
  return `${origin}${pagePath}`;
}

function safePageReferrer(): string {
  if (typeof document === "undefined" || !document.referrer) return "";
  try {
    // Preserve attribution at the origin level without forwarding an app/auth
    // pathname, query string, hash, or token from the referring URL.
    const origin = new URL(document.referrer).origin;
    return origin === "null" ? "" : origin;
  } catch {
    return "";
  }
}

/**
 * Records one sanitized page view. Query strings, hashes, referrer paths, and
 * form values are deliberately excluded from the payload.
 */
export function trackMarketingPageView(pathname: string, title?: string): boolean {
  const measurementId = getGa4MeasurementId();
  if (
    !measurementId
    || typeof window === "undefined"
    || typeof window.gtag !== "function"
    || !hasAnalyticsConsent()
    || !isAllowedAnalyticsPath(pathname)
  ) {
    return false;
  }

  window.gtag("event", "page_view", {
    page_path: safePagePath(pathname),
    page_location: safePageLocation(pathname),
    page_title: safePageTitle(title ?? document.title),
    page_referrer: safePageReferrer(),
  });
  return true;
}

/**
 * Records a successful marketing lead without sending form values or other PII.
 * Callers invoke this only after the corresponding API returns `{success:true}`;
 * this helper also enforces consent and the public marketing-route boundary.
 */
export function trackMarketingLead(form: MarketingLeadForm): boolean {
  const measurementId = getGa4MeasurementId();
  if (
    !measurementId
    || typeof window === "undefined"
    || typeof window.gtag !== "function"
    || !hasAnalyticsConsent()
    || !isAllowedAnalyticsPath(window.location.pathname)
  ) {
    return false;
  }

  window.gtag("event", "generate_lead", { form_type: form });
  return true;
}
