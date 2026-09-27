import Link from 'next/link';
import DirectoryShell, { linkStyle, panel } from '@/components/marketing/directory/DirectoryShell';
import DirectoryFinderForm from '@/components/marketing/directory/DirectoryFinderForm';
import RequirementCards from '@/components/marketing/directory/RequirementCards';
import { getDirectory, DIRECTORY_PATH as root } from '@/lib/compliance-directory';
import {
  ancestors,
  coverageFor,
  filterRequirements,
  type DirectoryFilter,
} from '@/lib/directory-search';
import { directoryMetadata } from '@/lib/directory-metadata';
import { requirementTypes } from '@/lib/directory-model';

export const metadata = directoryMetadata(
  'Find licenses and compliance requirements',
  'Build a source-linked research shortlist by operating location, industry and market. Results are potentially relevant and coverage is incomplete.',
  root + '/finder',
);
type Query = Record<string, string | string[] | undefined>;
export default async function FinderPage({ searchParams }: { searchParams: Promise<Query> }) {
  const query = await searchParams,
    d = getDirectory();
  const value = (key: string) => (typeof query[key] === 'string' ? (query[key] as string) : '');
  const validGeo = (id: string) => (d.jurisdictions.some((j) => j.id === id) ? id : '');
  const location = validGeo(value('location')),
    subdivision = validGeo(value('subdivision'));
  const filters: DirectoryFilter = {
    query: value('q').slice(0, 120),
    location:
      subdivision && location && ancestors(subdivision, d.jurisdictions).includes(location)
        ? subdivision
        : location,
    market: validGeo(value('market')),
    activity: d.industries.some((i) => i.id === value('activity')) ? value('activity') : '',
    type: requirementTypes.some((t) => t === value('type')) ? value('type') : '',
    status: ['draft', 'verified', 'withdrawn', 'superseded'].includes(value('status'))
      ? value('status')
      : '',
  };
  const results = filterRequirements(d, filters),
    pageCount = Math.max(1, Math.ceil(results.length / 24));
  const requestedPage = Number(value('page'));
  const page = Number.isSafeInteger(requestedPage)
    ? Math.min(pageCount, Math.max(1, requestedPage))
    : 1;
  const href = (number: number) => {
    const params = new URLSearchParams();
    for (const [k, v] of Object.entries({
      q: filters.query,
      location,
      subdivision,
      market: filters.market,
      activity: filters.activity,
      type: filters.type,
      status: filters.status,
    }))
      if (v) params.set(k, v);
    params.set('page', String(number));
    return root + '/finder?' + params.toString();
  };
  return (
    <DirectoryShell
      title="Find licenses and compliance requirements"
      description="Select where you operate and what you do to build a research shortlist. Results are potentially relevant; the responsible authority must confirm applicability."
      path={root + '/finder'}
    >
      <DirectoryFinderForm
        jurisdictions={d.jurisdictions}
        industries={d.industries}
        initial={filters}
      />
      <aside className={panel}>
        <h2 className="mb-3 text-xl font-semibold text-amber-100">
          Coverage gaps remain for this selection
        </h2>
        <p>
          {filters.location
            ? coverageFor(d, filters.location, filters.activity).note
            : 'Worldwide coverage is incomplete. National, regional, municipal and special-zone requirements are still being mapped.'}
        </p>
        <p className="mt-3 text-sm">
          An empty result does not mean no obligations apply. International standards, wider
          jurisdictions and narrower local records may be included as research candidates.
          Extraterritorial rules can apply even if a location filter does not surface them.
        </p>
        <Link className={linkStyle + ' mt-4 inline-block'} href={root + '/coverage'}>
          See coverage and review definitions
        </Link>
      </aside>
      <section aria-labelledby="results-heading">
        <h2 id="results-heading" className="mb-5 text-2xl font-semibold text-white">
          {results.length} potentially relevant research{' '}
          {results.length === 1 ? 'entry' : 'entries'}
        </h2>
        <RequirementCards records={results.slice((page - 1) * 24, page * 24)} />
      </section>
      {pageCount > 1 && (
        <nav aria-label="Search results pagination" className="flex items-center gap-6">
          {page > 1 && (
            <Link className={linkStyle} href={href(page - 1)}>
              Previous page
            </Link>
          )}
          <span className="text-sm">
            Page {page} of {pageCount}
          </span>
          {page < pageCount && (
            <Link className={linkStyle} href={href(page + 1)}>
              Next page
            </Link>
          )}
        </nav>
      )}
    </DirectoryShell>
  );
}
