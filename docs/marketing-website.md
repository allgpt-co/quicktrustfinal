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

Before rollout, retain the current application image and configure lead email
variables. After rollout, check every sitemap URL, robots, social images,
contact validation, anonymous dashboard redirects and login/registration. If
routing or authentication regresses, roll the frontend back to its previous
image in Coolify; leave the backend and database untouched.
