import Link from 'next/link';
import { notFound, permanentRedirect } from 'next/navigation';
import type { Metadata } from 'next';
import ReactMarkdown from 'react-markdown';
import DirectoryShell, {
  buttonStyle,
  linkStyle,
  panel,
} from '@/components/marketing/directory/DirectoryShell';
import RequirementCards from '@/components/marketing/directory/RequirementCards';
import DirectoryActionLink from '@/components/marketing/directory/DirectoryActionLink';
import {
  getDirectory,
  getImports,
  getCatalogue,
  jurisdictionPath,
  industryPath,
  DIRECTORY_PATH as root,
  DIRECTORY_ORIGIN,
  DIRECTORY_UPDATED,
} from '@/lib/compliance-directory';
import { coverageFor, filterRequirements } from '@/lib/directory-search';
import { isVerified, typeLabels, type Requirement } from '@/lib/directory-model';
import { directoryMetadata } from '@/lib/directory-metadata';
import { serializeJsonLd } from '@/components/marketing/schema/jsonLd';

export const revalidate = 86400;
export const dynamicParams = true;
type Props = { params: Promise<{ segments?: string[] }> };

const pages: Record<string, [string, string]> = {
  '': [
    'Global license and compliance directory',
    'Explore business licenses, professional authorizations, regulations and voluntary standards by location and activity. Follow official sources and see exactly where research is incomplete.',
  ],
  countries: [
    'Licenses and compliance by country',
    'Choose a country or territory, then explore its recorded subdivisions and local jurisdictions. These research hubs do not yet represent complete lists of obligations.',
  ],
  industries: [
    'Licenses and compliance by industry',
    'Browse the full UN ISIC Rev.5 activity hierarchy, from broad sectors to individual activity classes. Requirement mappings remain under review.',
  ],
  coverage: [
    'Directory coverage and review status',
    'Track published requirements, reference inventories and the research still needed at national, regional, municipal and special-zone levels.',
  ],
  sources: [
    'Official sources and research inventory',
    'Start with the responsible authority. Source discovery, link availability and substantive requirement verification are separate steps.',
  ],
  updates: [
    'Requirement changes and review history',
    'Review dated changes, replaced editions and source-backed future dates. Research dates are distinct from legal commencement dates.',
  ],
};

function resolve(segments: string[]) {
  const key = segments.join('/'),
    d = getDirectory();
  if (pages[key])
    return {
      kind: 'page' as const,
      title: pages[key][0],
      description: pages[key][1],
      path: root + (key ? '/' + key : ''),
      key,
      index: ['', 'coverage'].includes(key),
    };
  if (segments.length === 2 && segments[0] === 'jurisdictions') {
    const item = d.jurisdictions.find((j) => j.id.toLowerCase() === segments[1]);
    if (item)
      return {
        kind: 'jurisdiction' as const,
        item,
        title: `${item.name}: licenses and compliance`,
        description: `Explore recorded requirements and official research sources for ${item.name}. National, regional and local coverage is incomplete.`,
        path: jurisdictionPath(item.id),
        index: false,
      };
  }
  if (segments.length === 2 && segments[0] === 'industries') {
    const item = d.industries.find((i) => i.id.toLowerCase() === segments[1]);
    if (item)
      return {
        kind: 'industry' as const,
        item,
        title: `${item.name}: compliance research`,
        description: `Browse potential licenses, permits and compliance topics for ISIC Rev.5 ${item.id}: ${item.name}. Activity mappings need local verification.`,
        path: industryPath(item.id),
        index: false,
      };
  }
  if (segments.length === 2 && segments[0] === 'requirements') {
    const item = d.requirements.find((r) => r.id === segments[1]);
    if (item)
      return {
        kind: 'requirement' as const,
        item,
        title: item.name,
        description: item.summary,
        path: item.canonicalPath,
        index: isVerified(item),
      };
  }
  return null;
}

export function generateStaticParams() {
  const d = getDirectory();
  return [
    ...Object.keys(pages).map((key) => ({ segments: key ? [key] : [] })),
    ...d.jurisdictions
      .filter((j) => j.kind !== 'subdivision')
      .map((j) => ({ segments: ['jurisdictions', j.id.toLowerCase()] })),
    ...d.industries
      .filter((i) => i.level === 'section')
      .map((i) => ({ segments: ['industries', i.id.toLowerCase()] })),
    ...d.requirements.map((r) => ({ segments: ['requirements', r.id] })),
  ];
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const resolved = resolve((await params).segments ?? []);
  return resolved
    ? directoryMetadata(resolved.title, resolved.description, resolved.path, resolved.index)
    : { title: 'Directory page not found', robots: { index: false, follow: true } };
}

function SourceLinks({ ids }: { ids: string[] }) {
  const sources = getDirectory().sources.filter((s) => ids.includes(s.id));
  if (!sources.length)
    return <p>Official regulatory source identification is pending for this scope.</p>;
  return (
    <ul className="space-y-3">
      {sources.map((s) => (
        <li key={s.id}>
          <DirectoryActionLink href={s.url} className={linkStyle}>
            {s.name}
          </DirectoryActionLink>
          <p className="mt-1 text-xs text-slate-400">
            {s.publisher} ·{' '}
            {s.reviewedAt ? `Source reviewed ${s.reviewedAt}` : 'Substantive source review pending'}
          </p>
        </li>
      ))}
    </ul>
  );
}

function RequirementDetail({ record: r }: { record: Requirement }) {
  const d = getDirectory(),
    verified = isVerified(r);
  const fields: [string, string | null][] = [
    ['Authority or scheme owner', r.authority],
    ['Current status', r.currentStatus],
    ['Who may need it', r.applicability],
    ['Exemptions and limits', r.exemptions],
    ['Application or assessment', r.application],
    ['Renewal and ongoing review', r.renewal],
    ['Fees', r.fees],
    ['Version', r.version],
    ['Effective or publication date', r.effectiveDate],
  ];
  return (
    <>
      {['withdrawn', 'superseded'].includes(r.status) && (
        <aside className={panel}>
          <strong className="text-amber-100">Historical record — {r.status}</strong>
          {r.replacementId && (
            <p className="mt-2">
              <Link
                className={linkStyle}
                href={d.requirements.find((x) => x.id === r.replacementId)!.canonicalPath}
              >
                Read the replacement record
              </Link>
            </p>
          )}
        </aside>
      )}
      {r.status === 'verified' && !verified && (
        <aside className={panel}>
          This overview is due for review. Indexing and checklist downloads are paused until its
          sources are checked again.
        </aside>
      )}
      <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <section className={panel}>
          <h2 className="mb-5 text-2xl font-semibold text-white">Requirement overview</h2>
          <dl className="space-y-5">
            {fields.map(([label, value]) => (
              <div key={label}>
                <dt className="text-sm font-semibold text-slate-200">{label}</dt>
                <dd className="mt-1 text-sm leading-relaxed text-slate-300">
                  {value || 'Pending verification against the official source.'}
                </dd>
              </div>
            ))}
          </dl>
        </section>
        <aside className={panel}>
          <p className="mb-3 text-sm text-teal-200">{typeLabels[r.type]}</p>
          <h2 className="text-xl font-semibold text-white">Start with the official source</h2>
          <DirectoryActionLink href={r.applicationUrl} className={buttonStyle + ' mt-5'}>
            Official application or guidance
          </DirectoryActionLink>
          <p className="mt-4 text-sm leading-relaxed">
            {r.quickTrustSupport === 'educational'
              ? 'This is an educational directory entry. QuickTrust support for this requirement has not been confirmed.'
              : 'QuickTrust support is limited to the scope described on the linked service page.'}
          </p>
          {r.quickTrustSupport === 'confirmed' && r.servicePath && (
            <Link href={r.servicePath} className={linkStyle}>
              Explore confirmed QuickTrust support
            </Link>
          )}
          <h3 className="mb-3 mt-7 font-semibold text-white">Jurisdiction</h3>
          <ul className="space-y-2">
            {r.jurisdictions.map((id) => (
              <li key={id}>
                <Link className={linkStyle} href={jurisdictionPath(id)}>
                  {d.jurisdictions.find((j) => j.id === id)!.name}
                </Link>
              </li>
            ))}
          </ul>
          <h3 className="mb-3 mt-7 font-semibold text-white">Activity scope</h3>
          {r.crossSector ? (
            <p className="text-sm">
              Cross-sector topic; applicability depends on the organization's circumstances.
            </p>
          ) : (
            <ul className="space-y-2">
              {r.activities.map((id) => (
                <li key={id}>
                  <Link href={industryPath(id)} className={linkStyle}>
                    {d.industries.find((i) => i.id === id)!.name}
                  </Link>
                </li>
              ))}
            </ul>
          )}
          <p className="mt-7 text-xs text-slate-400">
            {r.reviewedAt ? `Overview reviewed ${r.reviewedAt}` : 'Overview review pending'}
            <br />
            Next review: {r.nextReviewAt}
          </p>
        </aside>
      </div>
      {d.content[r.id] && (
        <article
          className={`${panel} prose prose-invert max-w-none prose-headings:text-white prose-a:text-teal-300`}
        >
          <ReactMarkdown>{d.content[r.id]}</ReactMarkdown>
        </article>
      )}
      <section className={panel}>
        <h2 className="mb-4 text-2xl font-semibold text-white">Preparation checklist</h2>
        {verified ? (
          <>
            <p className="mb-5 text-sm">{r.review!.scope}</p>
            <ul className="mb-6 list-disc space-y-3 pl-5">
              {r.documents.map((item, index) => (
                <li key={index}>
                  {item.text}{' '}
                  <DirectoryActionLink
                    href={d.sources.find((s) => s.id === item.sourceId)!.url}
                    className={linkStyle}
                  >
                    Source
                  </DirectoryActionLink>
                </li>
              ))}
            </ul>
            <DirectoryActionLink
              href={`${root}/checklists/${r.id}`}
              event="directory_checklist_download"
              className={buttonStyle}
            >
              Download source-linked checklist (.txt)
            </DirectoryActionLink>
          </>
        ) : (
          <p>
            A downloadable checklist will be available after the record's sources and substantive
            content pass review.
          </p>
        )}
      </section>
      <section className={panel}>
        <h2 className="mb-5 text-2xl font-semibold text-white">Sources and review scope</h2>
        <SourceLinks ids={r.sourceIds} />
        {r.review && (
          <p className="mt-6 text-sm text-slate-400">
            {r.review.reviewer}. {r.review.scope}
          </p>
        )}
      </section>
      <section className={panel}>
        <h2 className="mb-4 text-2xl font-semibold text-white">Change history</h2>
        <ol className="space-y-5">
          {[...r.changes]
            .sort((a, b) => b.date.localeCompare(a.date))
            .map((c, i) => (
              <li key={i}>
                <time className="text-sm text-teal-200">{c.date}</time>
                <p className="my-2">{c.summary}</p>
                <SourceLinks ids={c.sourceIds} />
              </li>
            ))}
        </ol>
      </section>
      {verified && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: serializeJsonLd({
              '@context': 'https://schema.org',
              '@type': 'Article',
              headline: r.name,
              description: r.summary,
              mainEntityOfPage: DIRECTORY_ORIGIN + r.canonicalPath,
              dateModified: r.updatedAt,
              datePublished: r.publishedAt,
              author: { '@type': 'Organization', name: 'QuickTrust' },
              publisher: { '@type': 'Organization', name: 'QuickTrust' },
              citation: r.sourceIds.map((id) => d.sources.find((s) => s.id === id)!.url),
            }),
          }}
        />
      )}
    </>
  );
}

export default async function DirectoryPage({ params }: Props) {
  const segments = (await params).segments ?? [],
    result = resolve(segments);
  if (!result) notFound();
  if (result.kind === 'requirement' && result.path !== root + '/' + segments.join('/'))
    permanentRedirect(result.path);
  const d = getDirectory(),
    countries = d.jurisdictions.filter((j) => j.kind === 'country'),
    verified = d.requirements.filter((r) => isVerified(r));
  let content: React.ReactNode;
  if (result.kind === 'requirement') content = <RequirementDetail record={result.item} />;
  else if (result.kind === 'jurisdiction') {
    const j = result.item,
      coverage = coverageFor(d, j.id),
      records = filterRequirements(d, { location: j.id });
    const children = d.jurisdictions
      .filter((x) => x.parent === j.id)
      .sort((a, b) => a.name.localeCompare(b.name));
    content = (
      <>
        <section className={panel}>
          <h2 className="mb-3 text-2xl font-semibold text-white">Coverage: {coverage.status}</h2>
          <p>{coverage.note}</p>
          <p className="mt-3 text-sm">
            {d.requirements.filter((r) => r.jurisdictions.includes(j.id)).length} records directly
            mapped to this jurisdiction. Municipal and special-zone inventories are incomplete; the
            total number of applicable obligations is unknown.
          </p>
          {j.parent && (
            <p className="mt-4">
              <Link href={jurisdictionPath(j.parent)} className={linkStyle}>
                Parent jurisdiction: {d.jurisdictions.find((x) => x.id === j.parent)!.name}
              </Link>
            </p>
          )}
          <p className="mt-4 text-xs text-slate-400">
            Reference code: {j.id}
            {j.localType ? ` · ${j.localType}` : ''}. Geography codes organize research and do not
            determine legal applicability.
          </p>
        </section>
        <section className={panel}>
          <h2 className="mb-4 text-xl font-semibold text-white">Official research sources</h2>
          <SourceLinks ids={coverage.sourceIds} />
        </section>
        {children.length > 0 && (
          <section className={panel}>
            <h2 className="mb-4 text-xl font-semibold text-white">
              Recorded subdivisions and local jurisdictions ({children.length})
            </h2>
            <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {children.map((c) => (
                <li key={c.id}>
                  <Link href={jurisdictionPath(c.id)} className={linkStyle}>
                    {c.name}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        )}
        {j.members && (
          <section className={panel}>
            <h2 className="mb-4 text-xl font-semibold text-white">Member countries</h2>
            <ul className="grid gap-3 sm:grid-cols-3">
              {j.members.map((id) => (
                <li key={id}>
                  <Link className={linkStyle} href={jurisdictionPath(id)}>
                    {d.jurisdictions.find((x) => x.id === id)!.name}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        )}
        <section>
          <h2 className="mb-3 text-2xl font-semibold text-white">
            Potentially relevant research entries
          </h2>
          <p className="mb-5 text-sm">
            Includes broader standards and recorded local requirements. Each entry needs an
            applicability check.
          </p>
          <RequirementCards records={records} />
        </section>
      </>
    );
  } else if (result.kind === 'industry') {
    const i = result.item,
      children = d.industries.filter((x) => x.parent === i.id);
    content = (
      <>
        <section className={panel}>
          <h2 className="mb-3 text-xl font-semibold text-white">
            ISIC Rev.5 {i.level}: {i.id}
          </h2>
          <p>
            Coverage status: unreviewed. This is an activity classification, not a legal
            determination or a complete license inventory. Local activity codes and licensing
            categories may differ.
          </p>
          {i.parent && (
            <p className="mt-4">
              <Link href={industryPath(i.parent)} className={linkStyle}>
                Browse parent activity
              </Link>
            </p>
          )}
          <p className="mt-4">
            <DirectoryActionLink
              href="https://unstats.un.org/unsd/classifications/Econ/isic"
              className={linkStyle}
            >
              Official UN classification source
            </DirectoryActionLink>
          </p>
        </section>
        {children.length > 0 && (
          <section className={panel}>
            <h2 className="mb-4 text-xl font-semibold text-white">More specific activities</h2>
            <ul className="grid gap-4 sm:grid-cols-2">
              {children.map((c) => (
                <li key={c.id}>
                  <Link className={linkStyle} href={industryPath(c.id)}>
                    {c.id} — {c.name}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        )}
        <Link className={buttonStyle} href={`${root}/finder?activity=${i.id}`}>
          Filter this activity by location
        </Link>
        <RequirementCards records={filterRequirements(d, { activity: i.id })} />
      </>
    );
  } else if (result.key === 'countries')
    content = (
      <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {[
          ...countries,
          ...d.jurisdictions.filter((j) => ['international', 'supranational'].includes(j.kind)),
        ]
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((j) => (
            <li key={j.id} className={panel}>
              <Link className={linkStyle} href={jurisdictionPath(j.id)}>
                {j.name}
              </Link>
              <p className="mt-2 text-xs text-slate-400">
                {j.id} · {coverageFor(d, j.id).status}
              </p>
            </li>
          ))}
      </ul>
    );
  else if (result.key === 'industries')
    content = (
      <>
        <p className={panel}>
          {d.industries.length} classification entries across{' '}
          {d.industries.filter((i) => i.level === 'section').length} sectors. Browse sector →
          division → group → class. All requirement mapping remains partial.
        </p>
        <ul className="grid gap-4 sm:grid-cols-2">
          {d.industries
            .filter((i) => i.level === 'section')
            .map((i) => (
              <li key={i.id} className={panel}>
                <Link className={linkStyle} href={industryPath(i.id)}>
                  {i.id} — {i.name}
                </Link>
              </li>
            ))}
        </ul>
      </>
    );
  else if (result.key === 'coverage')
    content = (
      <>
        <section className={panel}>
          <h2 className="mb-4 text-2xl font-semibold text-white">What the numbers measure</h2>
          <ul className="list-disc space-y-3 pl-5">
            <li>
              {verified.length} of {d.requirements.length} published requirement records have a
              current verified overview. This denominator is our recorded inventory, not all
              worldwide obligations.
            </li>
            <li>
              {countries.length} countries and territories and{' '}
              {d.jurisdictions.filter((j) => j.kind === 'subdivision').length} subdivisions in the
              imported ISO-code snapshot. Reconciliation with current ISO OBP changes is pending.
            </li>
            <li>
              {d.industries.length} of {getImports().find((x) => x.dataset.includes('ISIC'))!.count}{' '}
              entries in the official UN ISIC Rev.5 CSV are represented.
            </li>
            <li>
              {
                d.jurisdictions.filter((j) => ['municipality', 'special-zone'].includes(j.kind))
                  .length
              }{' '}
              additional municipal or special-zone jurisdictions documented. Worldwide denominator
              unknown.
            </li>
            <li>
              {getCatalogue().length} UK official catalogue leads await scope and authority triage;
              they are not verified requirements.
            </li>
            <li>
              {d.coverage.filter((c) => c.status === 'verified').length} jurisdiction/activity
              coverage cells verified against a named catalogue. Unlisted cells default to
              unreviewed.
            </li>
          </ul>
          <p className="mt-5 text-sm text-slate-400">
            Inventory release: {DIRECTORY_UPDATED}. Individual record review dates are shown on
            their pages.
          </p>
        </section>
        <section className={panel}>
          <h2 className="mb-4 text-2xl font-semibold text-white">Review states</h2>
          <dl className="space-y-4">
            {[
              [
                'Unreviewed',
                'No source reconciliation completed. Unknown is never recorded as “no requirements”.',
              ],
              [
                'Researching',
                'Official sources identified; authority, business scope and completeness are being checked.',
              ],
              [
                'Partial',
                'Some source-backed records exist; remaining catalogue entries or jurisdiction levels are outstanding.',
              ],
              [
                'Verified against a source',
                'A defined scope was reconciled against named sources on a stated date. This is not a claim to know every law.',
              ],
            ].map(([name, text]) => (
              <div key={name}>
                <dt className="font-semibold text-white">{name}</dt>
                <dd className="mt-1 text-sm">{text}</dd>
              </div>
            ))}
          </dl>
        </section>
        <section className={panel}>
          <h2 className="mb-4 text-2xl font-semibold text-white">Active research scopes</h2>
          <ul className="space-y-5">
            {d.coverage.map((c, i) => (
              <li key={i}>
                <Link href={jurisdictionPath(c.jurisdiction)} className={linkStyle}>
                  {d.jurisdictions.find((j) => j.id === c.jurisdiction)!.name}
                </Link>{' '}
                <span className="text-sm">— {c.status}</span>
                <p className="mt-1 text-sm">{c.note}</p>
              </li>
            ))}
          </ul>
          <p className="mt-5">
            <Link href={root + '/countries'} className={linkStyle}>
              See every country and its current status
            </Link>
          </p>
        </section>
        <section className={panel}>
          <h2 className="mb-4 text-2xl font-semibold text-white">
            How records become searchable in Google
          </h2>
          <p>
            Drafts are public but carry noindex and stay outside XML sitemaps. Verification requires
            current official sources, an identified authority, applicability and limitations,
            substantive original content, and a dated editorial review. A source link alone is
            insufficient. Overdue, withdrawn and superseded records are excluded from the directory
            sitemap and checklist downloads.
          </p>
          <p className="mt-4">
            Licensing and regulation reviews are scheduled monthly; standards and certifications
            quarterly. Link checks and GSC monitoring run weekly. A material source change starts a
            new review. English is the first publication language; official local names are
            retained.
          </p>
        </section>
        <section className={panel}>
          <h2 className="mb-4 text-2xl font-semibold text-white">Scope boundaries</h2>
          <p>
            Business and professional requirements across all industries are in scope. Personal
            driving, hunting, fishing and consumer permits are outside the requirement catalogue.
            National, state/provincial, municipal and special-zone sources must be checked
            separately. Official catalogue imports may contain out-of-scope leads until triage is
            complete.
          </p>
        </section>
      </>
    );
  else if (result.key === 'sources')
    content = (
      <>
        <section className={panel}>
          <h2 className="mb-5 text-2xl font-semibold text-white">
            Reference inventories and provenance
          </h2>
          <ul className="space-y-5">
            {getImports().map((s) => (
              <li key={s.dataset}>
                <DirectoryActionLink href={s.url} className={linkStyle}>
                  {s.dataset}
                </DirectoryActionLink>
                <p className="mt-2 text-sm">
                  {s.count} entries · retrieved {s.retrievedAt}. {s.verification}
                </p>
              </li>
            ))}
          </ul>
          <p className="mt-5 text-sm text-slate-400">
            Geography data derives from Debian iso-codes through pycountry; LGPL-2.1 notices and
            snapshot hashes are preserved in the source repository. Industry classification: United
            Nations Statistics Division. UK catalogue: GOV.UK, under the Open Government Licence.
          </p>
        </section>
        <section className={panel}>
          <h2 className="mb-5 text-2xl font-semibold text-white">
            Official source register ({d.sources.length})
          </h2>
          <SourceLinks ids={d.sources.map((s) => s.id)} />
        </section>
        <section className={panel}>
          <h2 className="mb-4 text-2xl font-semibold text-white">
            UK catalogue research backlog ({getCatalogue().length})
          </h2>
          <p className="mb-5 text-sm">
            These source leads include personal permits and possible duplicates. They become
            requirement pages after business/professional scope and the issuing authority are
            identified. Catalogue coverage does not establish complete UK coverage.
          </p>
          <details>
            <summary className="cursor-pointer text-teal-300">Browse all catalogue leads</summary>
            <ul className="mt-5 grid gap-4 sm:grid-cols-2">
              {getCatalogue().map((r) => (
                <li key={r.url}>
                  <DirectoryActionLink href={r.url} className={linkStyle}>
                    {r.name}
                  </DirectoryActionLink>
                  <p className="text-xs text-slate-400">Authority and scope review pending</p>
                </li>
              ))}
            </ul>
          </details>
        </section>
      </>
    );
  else if (result.key === 'updates')
    content = (
      <>
        <section className={panel}>
          <h2 className="mb-5 text-2xl font-semibold text-white">
            Material changes and editorial reviews
          </h2>
          <ol className="space-y-6">
            {d.requirements
              .filter((r) => r.reviewedAt || r.status === 'superseded')
              .flatMap((r) => r.changes.map((c) => ({ ...c, r })))
              .sort((a, b) => b.date.localeCompare(a.date))
              .map((c, i) => (
                <li key={i}>
                  <time className="text-sm text-teal-200">{c.date}</time>
                  <h3 className="my-1 font-semibold">
                    <Link href={c.r.canonicalPath} className={linkStyle}>
                      {c.r.name}
                    </Link>
                  </h3>
                  <p className="mb-3 text-sm">{c.summary}</p>
                  <SourceLinks ids={c.sourceIds} />
                </li>
              ))}
          </ol>
        </section>
        <section className={panel}>
          <h2 className="mb-4 text-2xl font-semibold text-white">Upcoming source-backed dates</h2>
          {d.requirements.some((r) => r.upcoming.length) ? (
            <ul>
              {d.requirements.flatMap((r) =>
                r.upcoming.map((u, i) => (
                  <li key={`${r.id}-${i}`}>
                    <time>{u.date}</time> — {u.summary}{' '}
                    <Link href={r.canonicalPath} className={linkStyle}>
                      {r.name}
                    </Link>
                  </li>
                )),
              )}
            </ul>
          ) : (
            <p>
              No upcoming legal or transition dates have completed verification in this release.
              This does not mean that no deadlines apply.
            </p>
          )}
        </section>
      </>
    );
  else
    content = (
      <>
        <div className="grid gap-4 sm:grid-cols-3">
          {[
            [String(countries.length), 'Countries and territories'],
            [String(d.industries.length), 'Industry classification entries'],
            [
              `${verified.length} / ${d.requirements.length}`,
              'Verified overviews / recorded requirements',
            ],
          ].map(([value, label]) => (
            <div key={label} className={panel}>
              <p className="text-4xl font-bold text-teal-200">{value}</p>
              <p className="mt-3 text-sm">{label}</p>
            </div>
          ))}
        </div>
        <section className={panel}>
          <h2 className="text-2xl font-semibold text-white">
            Begin with where and how you operate
          </h2>
          <p className="mt-4 max-w-3xl leading-relaxed">
            A business may need several permissions at different levels of government, alongside
            contractual standards and professional authorizations. Use the finder to build a
            research shortlist by location, activity and customer market. Open the official source
            to establish the actual scope before applying.
          </p>
          <div className="mt-6 flex flex-wrap items-center gap-5">
            <Link className={buttonStyle} href={root + '/finder'}>
              Find potentially relevant requirements
            </Link>
            <Link className={linkStyle} href={root + '/compare'}>
              Compare up to four requirements
            </Link>
          </div>
        </section>
        <section>
          <h2 className="mb-3 text-2xl font-semibold text-white">
            Source-reviewed starting points
          </h2>
          <p className="mb-5 text-sm">
            These educational overviews have a current source review and downloadable preparation
            checklist. They do not determine an individual organization's obligations.
          </p>
          <RequirementCards records={verified} />
        </section>
        <section className={panel}>
          <h2 className="text-2xl font-semibold text-white">
            Worldwide scope, visible research gaps
          </h2>
          <p className="mt-4 leading-relaxed">
            Country and industry hubs are public drafts. The reference inventories organize
            research; they are not counts of verified legal requirements. National, regional and
            local coverage must be reconciled separately, including special zones. Missing results
            never establish that a business has no obligations.
          </p>
          <p className="mt-4 leading-relaxed">
            This directory includes requirements outside QuickTrust's confirmed services. Official
            authority and scheme links are the primary next step. Existing QuickTrust guidance keeps
            its established URL when it covers the same topic.
          </p>
          <p className="mt-5">
            <Link className={linkStyle} href={root + '/coverage'}>
              View denominators, review states and remaining work
            </Link>
          </p>
        </section>
      </>
    );
  const draft =
    result.kind === 'jurisdiction' ||
    result.kind === 'industry' ||
    (result.kind === 'requirement' && result.item.status === 'draft') ||
    (result.kind === 'page' && ['countries', 'industries'].includes(result.key));
  return (
    <DirectoryShell
      title={result.title}
      description={result.description}
      path={result.path}
      draft={draft}
    >
      {content}
    </DirectoryShell>
  );
}
