import { MARKETING_PATHS, RESOURCE_SLUGS } from "@/lib/marketing-routes";

export type MarketingLeadForm = "contact" | "booking" | "readiness";
export type AnalyticsConsent = "granted" | "denied" | null;
export const ANALYTICS_CONSENT_EVENT = "qt:analytics-consent";

export type MarketingPageView = {
  page_path: string;
  page_location: string;
  page_title: string;
  page_referrer: string;
};
type AnalyticsContext = Pick<MarketingPageView, "page_location" | "page_title" | "page_referrer">;

type Gtag = {
  (command: "js", date: Date): void;
  (command: "consent", action: "default" | "update", parameters: ConsentParameters): void;
  (command: "config", measurementId: string, parameters: ConfigParameters): void;
  (command: "set", parameters: AnalyticsContext): void;
  (command: "event", eventName: "generate_lead", parameters: { form_type: MarketingLeadForm } & AnalyticsContext): void;
  (command: "event", eventName: "page_view", parameters: MarketingPageView): void;
};

type ConfigParameters = {
  send_page_view: false;
  anonymize_ip: true;
  allow_google_signals: false;
  allow_ad_personalization_signals: false;
} & AnalyticsContext;

export type ConsentParameters = {
  analytics_storage: "granted" | "denied";
  ad_storage: "granted" | "denied";
  ad_user_data: "granted" | "denied";
  ad_personalization: "granted" | "denied";
  wait_for_update?: number;
};

const consentGranted: ConsentParameters = {
  analytics_storage: "granted", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied",
};
const consentDenied: ConsentParameters = {
  analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied",
};

declare global {
  interface Window {
    // The real gtag snippet pushes its `arguments` object, not a rest-args array.
    dataLayer?: Array<unknown[] | IArguments>;
    gtag?: Gtag;
    __qtAnalyticsConsent?: AnalyticsConsent;
    __qtGa4ConfiguredId?: string;
  }
}

const validMeasurementId = /^G-[A-Z0-9]+$/;
const analyticsConsentCookie = "qt_analytics_consent";
const excludedMarketingPaths = new Set([
  "/privacy-policy", "/terms-of-service",
  ...RESOURCE_SLUGS.map((slug) => `/resources/${slug}`),
]);
const staticAnalyticsPaths = new Set<string>(MARKETING_PATHS.filter((path) => !excludedMarketingPaths.has(path)));
let registeredAnalyticsPaths: Set<string> | null = null;

function normalizePathname(pathname: string): string {
  if (!pathname || !pathname.startsWith("/")) return "/";
  const withoutQuery = pathname.split(/[?#]/, 1)[0] || "/";
  if (withoutQuery === "/") return "/";
  return withoutQuery.replace(/\/+$/, "");
}

export function registerAnalyticsPaths(paths: readonly string[]): void {
  registeredAnalyticsPaths = new Set(paths.map(normalizePathname).filter((path) => !excludedMarketingPaths.has(path)));
}

export function clearAnalyticsPaths(): void {
  registeredAnalyticsPaths = null;
}

export function getGa4MeasurementId(): string | null {
  const measurementId = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID?.trim();
  return measurementId && validMeasurementId.test(measurementId) ? measurementId : null;
}

function readConsentCookie(): AnalyticsConsent {
  if (typeof document === "undefined") return null;
  for (const entry of document.cookie.split(";")) {
    const [name, ...valueParts] = entry.trim().split("=");
    if (name !== analyticsConsentCookie) continue;
    try {
      const value = decodeURIComponent(valueParts.join("="));
      return value === "granted" || value === "denied" ? value : null;
    } catch { return null; }
  }
  return null;
}

export function getAnalyticsConsent(): AnalyticsConsent {
  if (typeof window !== "undefined" && window.__qtAnalyticsConsent !== undefined) return window.__qtAnalyticsConsent;
  return readConsentCookie();
}

export function setAnalyticsConsent(consent: Exclude<AnalyticsConsent, null>): void {
  if (typeof window !== "undefined") window.__qtAnalyticsConsent = consent;
  if (typeof document !== "undefined") {
    const secure = typeof window !== "undefined" && window.location.protocol === "https:" ? "; Secure" : "";
    document.cookie = `${analyticsConsentCookie}=${consent}; Max-Age=31536000; Path=/; SameSite=Lax${secure}`;
  }
  if (typeof window !== "undefined") window.dispatchEvent(new Event(ANALYTICS_CONSENT_EVENT));
}

/** Analytics is opt-in: missing and denied decisions both block collection. */
export function hasAnalyticsConsent(): boolean { return getAnalyticsConsent() === "granted"; }

export function getAnalyticsConsentParameters(granted: boolean): ConsentParameters {
  return granted ? consentGranted : consentDenied;
}

/** Only public, explicitly allowlisted marketing pages may emit analytics. */
export function isAllowedAnalyticsPath(pathname: string): boolean {
  const normalized = normalizePathname(pathname);
  if (excludedMarketingPaths.has(normalized)) return false;
  if (registeredAnalyticsPaths) return registeredAnalyticsPaths.has(normalized);
  // Published blog paths are registered by the server marketing layout. Never
  // treat an arbitrary /blog/* or app path as a public analytics destination.
  return staticAnalyticsPaths.has(normalized);
}

function safePageTitle(title: string): string {
  const normalized = title.replace(/https?:\/\/\S+/gi, "").replace(/[\w.+-]+@[\w.-]+\.[a-z]{2,}/gi, "").replace(/\s+/g, " ").trim();
  return (normalized || "QuickTrust").slice(0, 160);
}

function safePagePath(pathname: string): string { const normalized = normalizePathname(pathname); return normalized === "/" ? "/" : normalized; }

function safePageLocation(pathname: string): string {
  const origin = typeof window !== "undefined" ? window.location.origin : "https://quicktrustapp.com";
  return `${origin}${safePagePath(pathname)}`;
}

function safePageReferrer(): string {
  if (typeof document === "undefined" || !document.referrer) return "";
  try {
    const origin = new URL(document.referrer).origin;
    return origin === "null" ? "" : origin;
  } catch { return ""; }
}

function safeContext(pathname: string, title?: string): AnalyticsContext {
  return {
    page_location: safePageLocation(pathname),
    page_title: safePageTitle(title ?? (typeof document === "undefined" ? "QuickTrust" : document.title)),
    page_referrer: safePageReferrer(),
  };
}

function validLeadForm(form: MarketingLeadForm): form is MarketingLeadForm {
  return form === "contact" || form === "booking" || form === "readiness";
}

/** Records one sanitized page view, with no query/hash/referrer path. */
export function trackMarketingPageView(pathname: string, title?: string): boolean {
  const measurementId = getGa4MeasurementId();
  const normalizedPath = safePagePath(pathname);
  if (!measurementId || typeof window === "undefined" || typeof window.gtag !== "function" || !hasAnalyticsConsent() || !isAllowedAnalyticsPath(normalizedPath)) return false;
  window.gtag("event", "page_view", { page_path: normalizedPath, ...safeContext(normalizedPath, title) });
  return true;
}

/** Records a successful marketing lead without form values or other PII. */
export function trackMarketingLead(form: MarketingLeadForm): boolean {
  const measurementId = getGa4MeasurementId();
  const pathname = typeof window === "undefined" ? "/" : window.location.pathname;
  if (!measurementId || !validLeadForm(form) || typeof window === "undefined" || typeof window.gtag !== "function" || !hasAnalyticsConsent() || !isAllowedAnalyticsPath(pathname)) return false;
  window.gtag("event", "generate_lead", { form_type: form, ...safeContext(pathname) });
  return true;
}
