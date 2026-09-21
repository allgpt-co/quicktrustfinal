"use client";

import { useEffect, useRef } from "react";
import { usePathname } from "next/navigation";
import {
  clearAnalyticsPaths,
  getAnalyticsConsentParameters,
  getGa4MeasurementId,
  hasAnalyticsConsent,
  isAllowedAnalyticsPath,
  registerAnalyticsPaths,
  trackMarketingPageView,
} from "@/lib/marketing-analytics";

const ga4ScriptId = "quicktrust-ga4-script";
type Props = { allowedPaths?: readonly string[] };

function analyticsDisableKey(measurementId: string): string { return `ga-disable-${measurementId}`; }

function sanitizedRuntimeContext(pathname: string): { page_location: string; page_title: string; page_referrer: string } {
  const path = pathname.split(/[?#]/, 1)[0] || "/";
  const origin = typeof window === "undefined" ? "https://quicktrustapp.com" : window.location.origin;
  const title = (typeof document === "undefined" ? "QuickTrust" : document.title)
    .replace(/https?:\/\/\S+/gi, "")
    .replace(/[\w.+-]+@[\w.-]+\.[a-z]{2,}/gi, "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 160) || "QuickTrust";
  let referrer = "";
  if (typeof document !== "undefined" && document.referrer) {
    try {
      const originValue = new URL(document.referrer).origin;
      referrer = originValue === "null" ? "" : originValue;
    } catch { referrer = ""; }
  }
  return { page_location: `${origin}${path}`, page_title: title, page_referrer: referrer };
}

function initializeGa4(measurementId: string, pathname: string): void {
  if (typeof window === "undefined" || typeof document === "undefined") return;
  window.dataLayer = window.dataLayer || [];
  if (!window.gtag) {
    // Match Google's queue contract exactly: push the `arguments` object so
    // the downloaded gtag library can process command positions correctly.
    window.gtag = function gtag(..._args: unknown[]) {
      window.dataLayer?.push(arguments);
    } as unknown as NonNullable<typeof window.gtag>;
  }
  const gtag = window.gtag;
  if (!gtag) return;

  const context = sanitizedRuntimeContext(pathname);
  (window as unknown as Record<string, boolean>)[analyticsDisableKey(measurementId)] = false;
  if (window.__qtGa4ConfiguredId !== measurementId) {
    gtag("consent", "default", { ...getAnalyticsConsentParameters(false), wait_for_update: 500 });
    gtag("js", new Date());
    // Automatic page_view is disabled; this component emits one sanitized view.
    gtag("config", measurementId, {
      send_page_view: false,
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      ...context,
    });
    window.__qtGa4ConfiguredId = measurementId;
  }
  gtag("set", context);
  gtag("consent", "update", getAnalyticsConsentParameters(true));
  if (!document.getElementById(ga4ScriptId)) {
    const script = document.createElement("script");
    script.id = ga4ScriptId;
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
    document.head.appendChild(script);
  }
}

function disableGa4(measurementId: string | null): void {
  if (typeof window === "undefined" || !measurementId) return;
  // Set the documented disable flag before changing consent, so a queued or
  // already-loaded tag cannot send a post-revocation event.
  (window as unknown as Record<string, boolean>)[analyticsDisableKey(measurementId)] = true;
  if (typeof window.gtag === "function") window.gtag("consent", "update", getAnalyticsConsentParameters(false));
  if (typeof document !== "undefined") {
    // Remove only GA cookies; TruConversion and auth cookies are untouched.
    for (const name of document.cookie.split(";").map((entry) => entry.trim().split("=", 1)[0])) {
      if (/^_ga(?:_|$)/.test(name)) document.cookie = `${name}=; Max-Age=0; Path=/`;
    }
  }
}

export default function MarketingAnalytics({ allowedPaths }: Props) {
  const pathname = usePathname() || "/";
  // Next normally returns a pathname without search/hash, but canonicalize the
  // value here as a defense against shallow/query-only history changes.
  const canonicalPathname = pathname.split(/[?#]/, 1)[0] || "/";
  const trackedPath = useRef<string | null>(null);

  useEffect(() => {
    if (allowedPaths) registerAnalyticsPaths(allowedPaths);
    return () => clearAnalyticsPaths();
  }, [allowedPaths]);

  useEffect(() => {
    const emitForCurrentPath = () => {
      const measurementId = getGa4MeasurementId();
      if (!measurementId || !isAllowedAnalyticsPath(canonicalPathname)) {
        trackedPath.current = null;
        disableGa4(measurementId);
        return;
      }
      if (!hasAnalyticsConsent()) {
        trackedPath.current = null;
        disableGa4(measurementId);
        return;
      }
      initializeGa4(measurementId, canonicalPathname);
      if (trackedPath.current === canonicalPathname) return;
      if (trackMarketingPageView(canonicalPathname)) trackedPath.current = canonicalPathname;
    };

    emitForCurrentPath();
    window.addEventListener("qt:analytics-consent", emitForCurrentPath);
    return () => window.removeEventListener("qt:analytics-consent", emitForCurrentPath);
  }, [canonicalPathname]);

  // A marketing layout unmount is the app/auth boundary. Disable collection
  // there even when Next keeps the already-loaded script in the document.
  useEffect(() => () => disableGa4(getGa4MeasurementId()), []);
  return null;
}
