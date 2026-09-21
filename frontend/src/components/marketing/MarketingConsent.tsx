"use client";

import { useEffect, useRef, useState } from "react";
import {
  ANALYTICS_CONSENT_EVENT,
  getAnalyticsConsent,
  setAnalyticsConsent,
  type AnalyticsConsent,
} from "@/lib/marketing-analytics";

/**
 * A deliberately small, non-modal preference control for Google Analytics.
 * The marketing layout mounts this component only on public marketing routes;
 * app/auth routes never render it. The analytics runtime remains opt-in.
 */
export default function MarketingConsent() {
  // Keep the initial server/client markup stable. The persisted choice is read
  // after hydration so a returning visitor does not cause a hydration mismatch.
  const [consent, setConsent] = useState<AnalyticsConsent>(null);
  const [isOpen, setIsOpen] = useState(true);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const reopenRef = useRef<HTMLButtonElement>(null);
  const focusReopenAfterChoice = useRef(false);
  const focusHeadingAfterOpen = useRef(false);

  useEffect(() => {
    const currentConsent = getAnalyticsConsent();
    setConsent(currentConsent);
    setIsOpen(currentConsent === null);

    const syncConsent = () => {
      const nextConsent = getAnalyticsConsent();
      setConsent(nextConsent);
      setIsOpen(nextConsent === null);
    };
    window.addEventListener(ANALYTICS_CONSENT_EVENT, syncConsent);
    return () => window.removeEventListener(ANALYTICS_CONSENT_EVENT, syncConsent);
  }, []);

  useEffect(() => {
    if (focusReopenAfterChoice.current && consent !== null && !isOpen) {
      focusReopenAfterChoice.current = false;
      reopenRef.current?.focus();
    }
    if (focusHeadingAfterOpen.current && isOpen) {
      focusHeadingAfterOpen.current = false;
      headingRef.current?.focus();
    }
  }, [consent, isOpen]);

  function choose(nextConsent: Exclude<AnalyticsConsent, null>) {
    setAnalyticsConsent(nextConsent);
    setConsent(nextConsent);
    focusReopenAfterChoice.current = true;
    setIsOpen(false);
  }

  function reopen() {
    focusHeadingAfterOpen.current = true;
    setIsOpen(true);
  }

  const status = consent === "granted"
    ? "Google Analytics is allowed."
    : consent === "denied"
      ? "Google Analytics is declined."
      : "Google Analytics is not enabled until you choose Allow.";

  return (
    <aside
      aria-label="Google Analytics preferences"
      className="fixed inset-x-3 bottom-3 z-[60] sm:inset-x-auto sm:right-5 sm:w-[min(28rem,calc(100vw-2rem))]"
    >
      {isOpen ? (
        <section
          aria-labelledby="quicktrust-analytics-consent-title"
          className="rounded-xl border border-slate-700 bg-slate-900/95 p-5 text-slate-100 shadow-2xl backdrop-blur sm:p-6"
        >
          <h2
            id="quicktrust-analytics-consent-title"
            ref={headingRef}
            tabIndex={-1}
            className="font-display text-lg font-semibold outline-none focus-visible:ring-2 focus-visible:ring-teal-300 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900"
          >
            Choose Google Analytics preferences
          </h2>
          <p className="mt-2 text-sm leading-6 text-slate-300">
            Allow Google Analytics to help us understand visits to this public website, or decline it.
            This choice controls Google Analytics only and does not change other services.
          </p>
          <p className="mt-3 text-sm font-medium text-teal-200" role="status" aria-live="polite">
            {status}
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <button
              type="button"
              className="rounded-md bg-teal-400 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-teal-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-200 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900"
              onClick={() => choose("granted")}
            >
              Allow Google Analytics
            </button>
            <button
              type="button"
              className="rounded-md border border-slate-600 px-4 py-2.5 text-sm font-semibold text-slate-100 transition hover:border-slate-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-200 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900"
              onClick={() => choose("denied")}
            >
              Decline Google Analytics
            </button>
          </div>
          <a
            className="mt-4 inline-block text-sm text-slate-300 underline decoration-slate-500 underline-offset-4 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-200"
            href="/privacy-policy"
          >
            Read our privacy policy
          </a>
        </section>
      ) : (
        <div className="flex items-center justify-between gap-4 rounded-lg border border-slate-700 bg-slate-900/95 px-4 py-3 text-sm text-slate-200 shadow-xl backdrop-blur">
          <p role="status" aria-live="polite">{status}</p>
          <button
            ref={reopenRef}
            type="button"
            className="shrink-0 rounded-md border border-slate-600 px-3 py-2 font-semibold text-slate-100 transition hover:border-slate-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-200 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900"
            onClick={reopen}
          >
            Analytics preferences
          </button>
        </div>
      )}
    </aside>
  );
}
