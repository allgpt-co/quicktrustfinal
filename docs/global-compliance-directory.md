# Global compliance directory

Implementation branch builds on SEO completion PR #11. Publication is a public educational draft directory, not a claim that all global requirements have been identified or that QuickTrust supports every requirement.

## Content and reference inventories

`frontend/content/compliance-directory/` contains the source register, requirements, explicit coverage rows, ISO-code snapshot, UN ISIC Rev.5 hierarchy, extra jurisdictions, UK catalogue research leads, import hashes and three source-reviewed Markdown overviews. Runtime requests do not call external sources or the application database.

- 249 countries/territories; 5,046 subdivisions via pinned Debian/pycountry data. Current ISO OBP reconciliation is pending and visible publicly.
- 830 official ISIC Rev.5 entries: sector, division, group and class. Local licensing/activity-code correspondence remains pending.
- Two documented local jurisdictions: New York City and DIFC. WORLD and EU are additional explicit groupings, not ISO country codes.
- 71 requirement records: 3 verified educational overviews, 67 drafts and 1 superseded edition. Eight records reuse existing canonical pages; 63 have a new directory detail destination.
- 452 GOV.UK catalogue leads are an unreviewed research queue, not 452 public requirement pages. Triage business/professional scope, authority, duplicates and current status before publication. Personal permits remain out of scope.

Three verified overviews: ISO 9001, Cyber Essentials and NIST CSF. NIST reuses `/blog/pillar-nist-cybersecurity-framework-guide`; its companion implementation article was corrected at the same time. GDPR and PCI use the existing canonical articles directly, not their old aliases. ISO 9001:2015 retains a historical noindex record pointing to the current family record.

## Routes and tools

- `/compliance-directory`: crawlable overview and verified starting points.
- `/countries`, `/jurisdictions/{lowercase-code}`: draft geography hubs, parent/child links and explicit source gaps.
- `/industries`, `/industries/{lowercase-isic-code}`: all activity levels, cached on demand below the sector level.
- `/requirements/{id}`: draft/verified/historical detail, or permanent redirect to an established canonical article/service page.
- `/finder`: location, subdivision/local jurisdiction, customer/export market, ISIC activity, requirement type, status and text search; GET forms and bounded pagination.
- `/compare`: up to four unique known records; mobile horizontal table region has an accessible label and keyboard focus. Verified records expose checklist links here, including records whose canonical article is outside the directory.
- `/checklists/{id}`: source-linked UTF-8 text attachment with jurisdiction, review date, scope and official URLs. Unknown record returns 404; unverified, stale or historical record returns 409; all downloads are noindex.
- `/coverage`, `/sources`, `/updates`: transparent denominators, import provenance, official sources, triage queue, material changes and source-backed upcoming dates. Missing dates are not invented.

Finder results are research candidates, not a legal applicability decision. Parent-level and international records are included; a country-level search also includes recorded local candidates. EU rules are candidates for EU member markets. Extraterritorial rules and unmapped requirements can be missing even when the result list is nonempty. Every search displays this coverage limitation. Unlisted jurisdiction/activity coverage cells default to `unreviewed`.

## Authoring and verification

1. Identify an actual requirement and official authority/scheme owner. Record an official source. Do not create town × keyword or industry × country requirement pages without evidence.
2. Add a unique requirement ID, correct type, jurisdiction/activity IDs, original summary, canonical intent decision, review schedule and change record. Unknown applicability, exemptions, documents, fees, renewal, version and effective date remain null/empty.
3. Use an existing canonical article/service URL when it serves the same intent. Redirected aliases are rejected. Existing page indexability is independent of a draft directory record.
4. Draft pages carry the exact draft banner, `noindex,follow`, and no sitemap entry. They are crawlable so search engines can see noindex. No robots.txt disallow is added for the directory.
5. To promote, review authority, applicability and limits, current status, every cited source and substantive original content. Record the reviewer and scope honestly; this release identifies the overview review as an automated editorial source review, not external legal counsel or a certification assessment. Supply source-linked checklist preparation items, review date and next review date. The schema rejects missing fields, references, duplicate canonicals and invalid hierarchies.
6. Set `quickTrustSupport` to `educational` unless a confirmed service and its canonical destination exist. The directory emits no Service schema. Official guidance/application links remain the main action.
7. Record withdrawal or supersession explicitly. Supersession requires an existing replacement ID. Review expiry removes sitemap/checklist eligibility; pages and sitemap revalidate on their configured cache schedule, while downloads check at request time.

Verified is limited to the published overview and checklist scope. It never certifies a user's compliance or exhaustive jurisdiction coverage. A reachable URL does not satisfy editorial verification. ISO publishes standards but does not issue ISO certificates; FDA registration is distinct from product approval; SOC 2 is an attestation.

## SEO and rendering

The existing 197-entry sitemap stays unchanged. Robots.txt also advertises `/compliance-directory/sitemap.xml`, an index of sitemap shards (1,000 entries per shard). Initial directory sitemap: overview, coverage methodology, ISO 9001 and Cyber Essentials (4 URLs). NIST is already in the original sitemap. All directory dates come from content records; a rebuild does not create a modification date.

Metadata has one descriptive title/H1, self canonical, description and explicit robots. Draft hubs, filter/comparison routes, source/updates indexes, downloads and historical records stay outside XML sitemaps. Verified detail pages emit Article and BreadcrumbList data with official source citations. Publication dates are separate from the legal/standard event dates in change history.

The dedicated directory namespace is public; `/frameworks`, integrations management and other application routes remain protected. The existing marketing provider boundary avoids backend/auth initialization. Top-level hubs, countries, sectors and requirements are prerendered; other known reference hubs use cached server rendering with daily revalidation. Unknown IDs return 404. Content JSON and Markdown are included explicitly in standalone output tracing.

## Measurement

GA4 events `directory_search`, `directory_compare`, `directory_source_click`, `directory_checklist_download` use existing explicit analytics consent and the known-page allowlist. Payloads contain only the fixed `content_group=compliance_directory` and sanitized page context. Query text, selected countries, market/activity filters, arbitrary URLs and form values are not event parameters. Search/comparison page titles do not include user input. Directory engagement is separate from `generate_lead`; do not mark it as a qualified lead by default. Existing form success/failure and consent behavior remain covered by regression tests.

## Maintenance and release

`python3 frontend/scripts/import-directory-taxonomies.py` refreshes only reference snapshots. It pins pycountry, preserves its license/copyright notices, imports the full official UN CSV and checks that the UK search result count matches the full catalogue before writing. Review diffs and provenance before committing; it never promotes requirement records.

`python3 frontend/scripts/check-directory-sources.py --output /new/path.json [--previous /old/path.json]` performs bounded read-only HTTP checks and emits a review queue. Response hashes can flag content/template changes for review. HTTP 403/429 are bot/access blocks, not proof of a dead link. The script does not publish or send messages. `.github/workflows/directory-maintenance.yml` schedules a weekly availability/review-queue artifact after merge; it requires no secret and restores the previous public hash receipt from an Actions cache when available. A cache miss starts a fresh baseline.

Licensing/regulation review is monthly, standards/certification quarterly, with additional review after material changes. Source monitoring is operational automation, not legal review. GSC review remains part of the existing SEO measurement runbook; no paid recurring DataForSEO job is created.

Validate locally with `pnpm --dir frontend test`, `pnpm --dir frontend exec tsc --noEmit`, and `NEXT_PUBLIC_GA4_MEASUREMENT_ID=G-64YMH28D8R pnpm --dir frontend build`. Run the existing HTTP recovery gate plus the directory HTTP/browser checks against the built server. Test browser analytics through interception and lead responses through mocks; do not send real enquiries.

Merge the SEO dependency first, then this branch through the existing frontend release workflow. No backend deploy/configuration changes are needed. After deployment, rerun acceptance against production, record its commit/time and verify the new sitemap in GSC. A local build does not mean the website is deployed or indexed.

## Local validation receipt — September 27, 2026

- 88 tests across 18 files pass, including publication transitions, source/canonical validation, finder hierarchy, download eligibility, bounded analytics, previous lead/consent behavior and application route protections.
- TypeScript and production build pass (627 prerendered pages). Trace manifests include all 11 directory JSON/Markdown runtime files. The existing multiple-lockfile and edge-runtime build notices remain.
- `verify-compliance-directory.py`: 1,444/1,444 HTTP checks pass against the built server, covering every country/territory and ISIC activity, one subdivision per represented country, all new requirement pages, eight canonical redirects, every checklist gate and both sitemap levels. Unknown IDs return 404; protected application routes redirect to login.
- Existing marketing recovery gate: 430/430 HTTP checks; four deployment identity guard tests pass.
- Chromium: 10 representative routes at 1440px and 390px (20 viewport checks), no document overflow, one H1 and labeled finder/comparison inputs. Native location→local jurisdiction→activity filtering and two-record comparison work. ISO 9001 checklist downloaded successfully.
- GA4 browser interception: no script/events before consent, one page view after allowing, bounded search/source-click/checklist events without filter/query data, and no additional events after declining. All third-party requests were intercepted. No real lead, analytics hit, email or publication was sent.
- Source availability after URL fixes: 61 reachable, 22 HTTP 403 blocks, one 429 and one timeout among 85 sources; no remaining 404. These checks are separate from substantive source reviews. HTML/template hash changes are review signals, not claimed legal changes.

Screenshots and detailed local receipts are in ignored `output/playwright/` and `/tmp/quicktrust-directory-*` artifacts. The marketing plan repository retains a summary, requirement register, keyword evidence and public source-check receipt. Run the same HTTP gate after production deployment.
