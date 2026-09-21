# Marketing website

The public website and GRC app share the `quicktrustfinal` frontend at
https://quicktrustapp.com. Marketing content was imported from
`allgpt-co/Quicktrust` at `a6296c6101df606a2a1af820889fb0a6ccd5e4cd`.

- `/` is the public website, including for signed-in visitors.
- `/login` and `/dashboard` retain the existing application authentication.
- `/login?mode=register` opens registration; `/signup` redirects there.
- The marketing route group owns the shared navigation, footer, modal, fonts and
  scoped styling. Marketing pages do not initialize app authentication.
- All 193 source Markdown files are retained under `frontend/content/content_output`.
  Filenames define slugs. Sorted relative paths resolve duplicate slugs, first
  file wins, before applying `published: false`. The same registry drives article
  rendering, related content, listings, static generation and sitemap generation.
- The two comparison article URLs redirect to the comparison landing pages and
  are excluded from article listings and the sitemap. There are currently 166
  canonical blog articles and 13 other sitemap URLs.
- Dates do not introduce publication scheduling. Preserve the source's explicit
  `published` flag behavior when adding content.

## Website analytics

The marketing layout loads TruConversion site `63943` (`013c8.js`) after
hydration using Next.js Script. The loader initializes `_tip` and prevents
duplicate script injection. The Content Security Policy allows its app/CDN
scripts, CDN storage frame and HTTPS/WebSocket collection endpoints. Links from
marketing pages to login or registration use full navigation so the tracker does
not persist into the authenticated application.

The approved GA4 stream is `G-64YMH28D8R` (account `379364257`, property
`555117580`, stream `15810585098`). `MarketingAnalytics` loads it only after an
explicit opt-in from the accessible `MarketingConsent` control and only inside
the published public marketing route registry. It configures
`send_page_view: false`, applies Consent Mode defaults denied, uses the real
`dataLayer.push(arguments)` queue contract, and sends one sanitized `page_view`
per initial/client pathname plus `generate_lead` only after a lead API returns
`{ "success": true }`. Event parameters are bounded to `page_path`,
`page_location`, `page_title`, `page_referrer` (origin-only) and `form_type`;
query strings, referrer paths and form fields are excluded. Reopening
preferences and declining sets the GA disable flag and removes only GA cookies;
TruConversion is independent. Set
`NEXT_PUBLIC_GA4_MEASUREMENT_ID` on the Coolify web app; do not add a second
GA4 property or copy a raw Google snippet.

## Lead delivery

The frontend exposes `POST /api/contact` and `POST /api/readiness-snapshot`.
Set these **runtime, server-only** variables on the Coolify frontend application:

| Variable | Purpose |
| --- | --- |
| `SENDGRID_API_KEY` | SendGrid credential with permission to send mail |
| `FROM_EMAIL` | Verified SendGrid sender address |
| `COMPANY_EMAIL` | Recipient for marketing leads |

Contact JSON accepts `fullName`, `email`, and optional `phone`, `company`,
`framework`, `message`. Readiness JSON accepts `email`, `company`,
`targetFramework`, `targetTimeline`. Frontend forms use these same contracts.

The lead must be accepted by SendGrid before success is returned. A failed
acknowledgement does not cause the visitor to submit the lead again. Missing
configuration returns 503; invalid input returns 400; lead delivery failure
returns 502. Unit tests mock delivery and do not send real messages.

## Build, deployment and rollback

For the workspace use `pnpm install --frozen-lockfile`, then
`pnpm --dir frontend test` and `pnpm --dir frontend build`.
The frontend also has its own lockfile because the existing Coolify service
builds with `/frontend` as its base directory. Update both lockfiles whenever
frontend dependencies change.

Deploy the existing Coolify application `quicktrust:web`
(UUID `e92mp4jy5j3nojkgsyqhqbwd`, application 13), repository
`allgpt-co/quicktrustfinal`, branch `main`, base directory `/frontend`.
It uses Nixpacks, `pnpm build`, `pnpm start`, port 3000. The backend GitHub
workflow does not deploy frontend-only changes. No DNS or database changes are
needed. The Dockerfile and Next.js file tracing retain Markdown content at
runtime as well as build time.

The manual `Verify or deploy existing frontend` workflow accepts the tested
current main SHA. By default it only checks the existing Coolify application.
With `deploy=true`, it requires a green security check on that exact main SHA,
reads and verifies the application UUID/domain/repository/branch/base directory,
then requests one deployment. It checks the terminal deployment commit and runs
the public link/download/authentication/sitemap acceptance script. The existing
`COOLIFY_API_TOKEN` must legitimately permit application inspection and deployment;
403s stop the workflow without changing permissions or app settings. An uncertain
deployment response must be reconciled in Coolify before another dispatch.

Before rollout, retain the current application image and configure lead email
variables. After rollout, check every sitemap URL, robots, social images,
contact validation, anonymous dashboard redirects and login/registration. If
routing or authentication regresses, roll the frontend back to its previous
image in Coolify; leave the backend and database untouched.
