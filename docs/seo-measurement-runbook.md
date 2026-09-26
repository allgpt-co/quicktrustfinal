# SEO measurement and conversion completion register

**Status:** PR10 consent repair is merged; September 26 SEO completion is validated locally and awaits its own main merge/production gate
**Last checked:** 2026-09-26
**Site:** `https://quicktrustapp.com`

This register separates source-code readiness from external account verification. A prepared integration is not counted as verified until the production site and the owning account show the expected result.

## September 26 baseline and local release evidence

GSC finalized through Sep 23: current 28 days 6 clicks / 810 impressions / 0.74%
CTR / position 30.60; previous 28 days 13 / 257 / 5.06% / 19.75. GA4 Sep 20–25
(property timezone America/Los_Angeles) has 3 sessions, 1 user, 4 page views,
0 engaged sessions and 0 key events. All sessions are Direct. The stream is
recording data, so the old instruction to add its ID is superseded. No lead
conversion or channel performance conclusion is supported by this sample.

Production GSC sitemap still reports 179 submitted URLs with zero errors or
warnings. The source patch has 197 unique canonical indexable URLs, excluding
noindex pages and downloads. Sitemap `indexed: 0` is not a sitewide index count:
8 of 10 sampled URL inspections passed. SOC 2 retained a stale July not-found
crawl despite current HTTP 200; HITRUST was unknown. Recheck after recrawl.

Local release validation: 76 frontend tests, TypeScript, production build (272
pages), four deployment guard tests, and **430/430 HTTP checks** passed. Receipt:
`/tmp/quicktrust-seo-20260926/acceptance-local-final.json`, Sep 26 06:05 UTC. Raw analytics
exports, browser artifacts and credentials are not committed.

## Browser acceptance (local, September 26)

- Chromium checked nine representative pages at 390px and 1440px, including all
  four resource hubs, public integrations/trust, SOC 2 and both tools. All had one
  H1, no page-level horizontal overflow and no dashboard sign-in screen.
- Desktop/mobile template-hub screenshots were visually reviewed; artifacts are
  ignored under `output/playwright/`. Eight maximum self-assessment selections
  showed 16/16 points and “Higher reported coverage,” not an audit conclusion.
- Fresh preferences: no GA loader and no events before consent. Allow produced
  one sanitized guide page view, then one template page view on client navigation.
  The synthetic query email was absent. Decline set the disable flag and a
  subsequent client navigation emitted no additional event.
- Mocked accepted contact, booking and readiness requests each queued exactly one
  `generate_lead` with the matching form type. A mocked contact 503 showed an error
  and emitted no extra lead. Synthetic email, phone and message values were absent
  from queued analytics events. Unit tests additionally cover failure responses.
- All lead APIs and external analytics requests were intercepted locally. These
  are queue/UX tests, not GA4 ingestion or SendGrid delivery receipts. Local HTTP
  blocks the protocol-relative TruConversion script under the existing HTTPS CSP;
  production HTTPS tracking still requires its separate account verification.

## Current state

| Area | Source evidence | Status | Verification needed |
| --- | --- | --- | --- |
| TruConversion | `frontend/src/app/(marketing)/layout.tsx` loads site `63943` and script `013c8.js` after hydration. | Configured in source | In TruConversion, confirm marketing page sessions, form funnels and one conversion per accepted lead. |
| Lead endpoints | `/api/contact` and `/api/readiness-snapshot` return success only after SendGrid accepts the lead. | Configured in source | Submit each public form in production and confirm the matching lead arrives once. |
| Conversion events | Contact, booking and readiness forms call `trackMarketingLead` only after `result.success === true`. `generate_lead` contains only the bounded `form_type` plus sanitized page context. | Configured and tested locally | Confirm events in the selected analytics debugger/account; do not send names, email, phone or message text. |
| GA4 | The approved stream is `G-64YMH28D8R` (account `379364257`, property `555117580`, stream `15810585098`). The coordinator saved `NEXT_PUBLIC_GA4_MEASUREMENT_ID` in the existing Coolify `quicktrust:web` app for build and runtime. The client loads only after explicit opt-in and only for the published public-route registry. | Existing stream recording data; SEO content release awaiting merge | After the merge webhook, verify the sanitized `page_view` and `generate_lead` contract in GA4 DebugView. Do not create another property or manually redeploy. |
| Google Search Console | The siteOwner property and canonical sitemap were verified externally on 2026-09-20; the processed sitemap contains 179 URLs with zero errors or warnings. | Verified on Sep 26; post-merge 197-URL validation pending | Do not resubmit the sitemap. Keep account reports and private screenshots outside this repository. |
| Bing Webmaster Tools | No property token, API integration or report export is present in this repository. | External status unknown | Verify the domain and submit the canonical sitemap; record the account and date. |
| SEO reporting | Dated GSC/GA4/DataForSEO report, keyword map and read-only collector are in QuickTrustMarketing. | Baseline complete; recurring reporting pending | Run the collector into private storage; schedule no paid or credential-bearing job without configured ownership. |
| Deployment | Existing Coolify `quicktrust:web` UUID `e92mp4jy5j3nojkgsyqhqbwd`, base `/frontend`, branch `main`; merge webhook is the approved trigger. | Awaiting SEO completion merge | Let the existing webhook deploy the merged main commit, then run the committed public acceptance script. Do not touch backend or change Coolify settings. |

## Event contract

| Event | `form_type` values | Trigger |
| --- | --- | --- |
| `generate_lead` | `contact`, `booking`, `readiness` plus sanitized page context | Exactly once after the corresponding API responds with JSON `{ "success": true }`; no default monetary value or form fields. |
| `page_view` | `page_path`, `page_location`, `page_title`, `page_referrer` | Exactly once for each initial/client pathname after consent; query strings and hashes are excluded, and `page_referrer` is origin-only. |

The event bridge sends `send_page_view: false`, uses Consent Mode defaults denied, and updates `analytics_storage` only after explicit opt-in. The visitor-facing control offers equally available Allow/Decline actions and a keyboard-accessible preferences reopen control. Withdrawal sets GA4's disable flag, removes only GA cookies, and emits no further events; TruConversion remains independent and is not removed or replaced. The helper is a no-op when the public GA4 ID is absent or malformed, consent is missing, the route is outside the published public-route registry, or the GA4 loader is unavailable.

## Consent controls

The marketing layout mounts `MarketingConsent`, a small non-modal control that owns the existing cookie and dispatches the bridge event after the visitor makes a choice. An external manager, if one is ever introduced, must use the same bridge contract rather than loading a second Google snippet:

```js
document.cookie = 'qt_analytics_consent=granted; Max-Age=31536000; Path=/; Secure; SameSite=Lax';
window.dispatchEvent(new Event('qt:analytics-consent'));
```

On withdrawal, choose **Decline Google Analytics** from the reopened preferences control. The bridge sends a denied Consent Mode update without emitting another page view and leaves TruConversion untouched.

## Production verification checklist

- [ ] Confirm the Coolify runtime has the existing SendGrid variables: `SENDGRID_API_KEY`, `FROM_EMAIL`, and `COMPANY_EMAIL`.
- [ ] Confirm the public marketing layout still loads TruConversion site `63943`; authenticated application routes must not load it.
- [ ] Submit Contact, Booking and Readiness forms with test data; confirm one SendGrid lead per accepted request and no event on 400/502/503 responses.
- [x] Confirm `NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-64YMH28D8R` is saved in the existing Coolify web app; the next main merge triggers its existing webhook.
- [ ] After the webhook deployment, validate `page_view` plus `generate_lead` in DebugView with synthetic/non-PII checks only.
- [x] Verify no analytics payload contains form PII in focused tests and a local production browser.
- [x] Verify GSC siteOwner access and the processed 179-URL sitemap externally; do not resubmit.
- [ ] Check every sitemap URL, `robots.txt`, `llms.txt`, social image routes, contact validation, and login/registration redirects after rollout.
- [ ] Record URLs, timestamps, account/property names and screenshots or exports in the SEO report.

No external account changes, deployment, outreach, or messages are performed by this register.
