# SEO measurement and conversion completion register

**Status:** bounded consent/measurement repair implemented and tested locally; production acceptance follows the next main merge
**Last checked:** 2026-09-21
**Site:** `https://quicktrustapp.com`

This register separates source-code readiness from external account verification. A prepared integration is not counted as verified until the production site and the owning account show the expected result.

## Current state

| Area | Source evidence | Status | Verification needed |
| --- | --- | --- | --- |
| TruConversion | `frontend/src/app/(marketing)/layout.tsx` loads site `63943` and script `013c8.js` after hydration. | Configured in source | In TruConversion, confirm marketing page sessions, form funnels and one conversion per accepted lead. |
| Lead endpoints | `/api/contact` and `/api/readiness-snapshot` return success only after SendGrid accepts the lead. | Configured in source | Submit each public form in production and confirm the matching lead arrives once. |
| Conversion events | Contact, booking and readiness forms call `trackMarketingLead` only after `result.success === true`. `generate_lead` contains only the bounded `form_type` plus sanitized page context. | Configured and tested locally | Confirm events in the selected analytics debugger/account; do not send names, email, phone or message text. |
| GA4 | The approved stream is `G-64YMH28D8R` (account `379364257`, property `555117580`, stream `15810585098`). The coordinator saved `NEXT_PUBLIC_GA4_MEASUREMENT_ID` in the existing Coolify `quicktrust:web` app for build and runtime. The client loads only after explicit opt-in and only for the published public-route registry. | Configured in the approved app; repair awaiting merge/webhook | After the merge webhook, verify the sanitized `page_view` and `generate_lead` contract in GA4 DebugView. Do not create another property or manually redeploy. |
| Google Search Console | The siteOwner property and canonical sitemap were verified externally on 2026-09-20; the processed sitemap contains 179 URLs with zero errors or warnings. | Verified; no action pending | Do not resubmit the sitemap. Keep account reports and private screenshots outside this repository. |
| Bing Webmaster Tools | No property token, API integration or report export is present in this repository. | External status unknown | Verify the domain and submit the canonical sitemap; record the account and date. |
| SEO reporting | No committed GSC/GA4/Bing dashboard or scheduled report was found. | Not complete | Create a dated report from real account data: impressions, clicks, CTR, position, indexed URLs, traffic, accepted leads and top queries. Label unavailable metrics. |
| Deployment | Existing Coolify `quicktrust:web` UUID `e92mp4jy5j3nojkgsyqhqbwd`, base `/frontend`, branch `main`; merge webhook is the approved trigger. | Awaiting this bounded repair merge | Let the existing webhook deploy the merged main commit, then run the committed public acceptance script. Do not touch backend or change Coolify settings. |

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
