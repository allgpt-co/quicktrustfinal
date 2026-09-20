# SEO measurement and conversion completion register

**Status:** implementation complete locally; production acceptance verification pending
**Last checked:** 2026-09-20
**Site:** `https://quicktrustapp.com`

This register separates source-code readiness from external account verification. A prepared integration is not counted as verified until the production site and the owning account show the expected result.

## Current state

| Area | Source evidence | Status | Verification needed |
| --- | --- | --- | --- |
| TruConversion | `frontend/src/app/(marketing)/layout.tsx` loads site `63943` and script `013c8.js` after hydration. | Configured in source | In TruConversion, confirm marketing page sessions, form funnels and one conversion per accepted lead. |
| Lead endpoints | `/api/contact` and `/api/readiness-snapshot` return success only after SendGrid accepts the lead. | Configured in source | Submit each public form in production and confirm the matching lead arrives once. |
| Conversion events | Contact, booking and readiness forms call `trackMarketingLead` only after `result.success === true`. The event is `generate_lead` with only `form_type`. | Configured and tested locally | Confirm events in the selected analytics debugger/account; do not send names, email, phone or message text. |
| GA4 | The approved stream is `G-64YMH28D8R` (account `379364257`, property `555117580`, stream `15810585098`). The client bridge reads `NEXT_PUBLIC_GA4_MEASUREMENT_ID`, loads only after explicit `qt_analytics_consent=granted`, and is limited to public marketing paths. | Code ready; configure the approved ID in Coolify | Set `NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-64YMH28D8R`, deploy, then verify the sanitized `page_view` and `generate_lead` contract in GA4 DebugView. Do not create another property. |
| Google Search Console | No property token, API integration or report export is present in this repository. | External status unknown | Verify the `quicktrustapp.com` property, submit the canonical sitemap, and record submission/index coverage dates. DNS verification may be external to this codebase. |
| Bing Webmaster Tools | No property token, API integration or report export is present in this repository. | External status unknown | Verify the domain and submit the canonical sitemap; record the account and date. |
| SEO reporting | No committed GSC/GA4/Bing dashboard or scheduled report was found. | Not complete | Create a dated report from real account data: impressions, clicks, CTR, position, indexed URLs, traffic, accepted leads and top queries. Label unavailable metrics. |
| Deployment | `docs/marketing-website.md` identifies Coolify app `quicktrust:web` (application 13), base `/frontend`, branch `main`. | Use the existing approved workflow/webhook | Deploy the reconciled commit through the existing `quicktrust:web` path, then run the committed public acceptance script. Do not touch backend. |

## Event contract

| Event | `form_type` values | Trigger |
| --- | --- | --- |
| `generate_lead` | `contact`, `booking`, `readiness` | Exactly once after the corresponding API responds with JSON `{ "success": true }`. |
| `page_view` | `page_path`, `page_location`, `page_title`, `page_referrer` | Exactly once for each initial/client pathname after consent; query strings and hashes are excluded, and `page_referrer` is origin-only. |

The event bridge sends `send_page_view: false`, uses Consent Mode defaults denied, and updates `analytics_storage` only after explicit opt-in. The helper is a no-op when the public GA4 ID is absent or malformed, consent is missing, the route is outside the public marketing allowlist, or the GA4 loader is unavailable. TruConversion remains independent and is not removed or replaced.

## Consent-manager bridge

The site does not invent a consent decision. The consent manager should set the existing cookie and dispatch the event after the visitor opts in:

```js
document.cookie = 'qt_analytics_consent=granted; Max-Age=31536000; Path=/; Secure; SameSite=Lax';
window.dispatchEvent(new Event('qt:analytics-consent'));
```

On withdrawal, set the cookie to `denied` (or expire it), dispatch the same event, and the bridge sends a denied Consent Mode update without emitting another page view.

## Production verification checklist

- [ ] Confirm the Coolify runtime has the existing SendGrid variables: `SENDGRID_API_KEY`, `FROM_EMAIL`, and `COMPANY_EMAIL`.
- [ ] Confirm the public marketing layout still loads TruConversion site `63943`; authenticated application routes must not load it.
- [ ] Submit Contact, Booking and Readiness forms with test data; confirm one SendGrid lead per accepted request and no event on 400/502/503 responses.
- [ ] Set `NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-64YMH28D8R` in the existing Coolify web app, redeploy, and validate `page_view` plus `generate_lead` in DebugView.
- [ ] Verify no analytics payload contains form PII.
- [ ] Verify GSC and Bing ownership, sitemap submission and index coverage in their accounts.
- [ ] Check every sitemap URL, `robots.txt`, `llms.txt`, social image routes, contact validation, and login/registration redirects after rollout.
- [ ] Record URLs, timestamps, account/property names and screenshots or exports in the SEO report.

No external account changes, deployment, outreach, or messages are performed by this register.
