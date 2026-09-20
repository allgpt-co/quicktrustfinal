"use client";

import { useEffect, useRef } from "react";
import { usePathname } from "next/navigation";
import {
  getAnalyticsConsentParameters,
  getGa4MeasurementId,
  hasAnalyticsConsent,
  isAllowedAnalyticsPath,
  trackMarketingPageView,
} from "@/lib/marketing-analytics";

const ga4ScriptId = "quicktrust-ga4-script";

function initializeGa4(measurementId: string): void {
  if (typeof window === "undefined" || typeof document === "undefined") return;

  window.dataLayer = window.dataLayer || [];
  if (!window.gtag) {
    window.gtag = ((...args: unknown[]) => {
      window.dataLayer?.push(args);
    }) as unknown as NonNullable<typeof window.gtag>;
  }
  const gtag = window.gtag;
  if (!gtag) return;

  if (window.__qtGa4ConfiguredId !== measurementId) {
    gtag("consent", "default", {
      ...getAnalyticsConsentParameters(false),
      wait_for_update: 500,
    });
    gtag("js", new Date());
    // Automatic page_view is disabled. MarketingAnalytics emits one sanitized
    // page_view for each initial/client pathname instead.
    gtag("config", measurementId, { send_page_view: false, anonymize_ip: true });
    window.__qtGa4ConfiguredId = measurementId;
  }

  // The script is only loaded after opt-in. Keep the tag's consent state in
  // sync if a consent manager changes its decision during the session.
  gtag("consent", "update", getAnalyticsConsentParameters(true));

  if (!document.getElementById(ga4ScriptId)) {
    const script = document.createElement("script");
    script.id = ga4ScriptId;
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
    document.head.appendChild(script);
  }
}

export default function MarketingAnalytics() {
  const pathname = usePathname() || "/";
  const trackedPath = useRef<string | null>(null);

  useEffect(() => {
    const emitForCurrentPath = () => {
      const measurementId = getGa4MeasurementId();
      if (!measurementId || !isAllowedAnalyticsPath(pathname)) return;
      if (!hasAnalyticsConsent()) {
        if (typeof window.gtag === "function") {
          window.gtag("consent", "update", getAnalyticsConsentParameters(false));
        }
        return;
      }

      initializeGa4(measurementId);
      if (trackedPath.current === pathname) return;
      if (trackMarketingPageView(pathname)) trackedPath.current = pathname;
    };

    emitForCurrentPath();
    window.addEventListener("qt:analytics-consent", emitForCurrentPath);
    return () => window.removeEventListener("qt:analytics-consent", emitForCurrentPath);
  }, [pathname]);

  return null;
}
