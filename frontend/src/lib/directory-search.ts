import type { Directory, Requirement } from './directory-model';

export type DirectoryFilter = {
  query?: string;
  location?: string;
  market?: string;
  activity?: string;
  type?: string;
  status?: string;
};
export function ancestors(id: string, rows: { id: string; parent: string | null }[]): string[] {
  const result: string[] = [];
  let current: string | null = id;
  while (current && !result.includes(current)) {
    result.push(current);
    current = rows.find((r) => r.id === current)?.parent ?? null;
  }
  return result;
}
export function filterRequirements(
  d: Pick<Directory, 'requirements' | 'jurisdictions' | 'industries'>,
  filters: DirectoryFilter,
): Requirement[] {
  const q = (filters.query ?? '').trim().toLocaleLowerCase();
  const locations = [filters.location, filters.market].filter(Boolean) as string[];
  const placeMatches = (r: Requirement) =>
    !locations.length ||
    r.jurisdictions.includes('WORLD') ||
    locations.some((place) => {
      const lineage = ancestors(place, d.jurisdictions);
      return r.jurisdictions.some(
        (jurisdiction) =>
          lineage.includes(jurisdiction) ||
          // Broad country/region queries include narrower requirements as candidates.
          ancestors(jurisdiction, d.jurisdictions).includes(place) ||
          d.jurisdictions
            .find((j) => j.id === jurisdiction)
            ?.members?.some((member) => lineage.includes(member)),
      );
    });
  return d.requirements
    .filter(
      (r) =>
        (!q ||
          [r.name, ...r.aliases, r.summary, r.authority]
            .join(' ')
            .toLocaleLowerCase()
            .includes(q)) &&
        placeMatches(r) &&
        (!filters.activity ||
          r.crossSector ||
          r.activities.some(
            (id) =>
              ancestors(filters.activity!, d.industries).includes(id) ||
              ancestors(id, d.industries).includes(filters.activity!),
          )) &&
        (!filters.type || r.type === filters.type) &&
        (!filters.status || r.status === filters.status),
    )
    .sort((a, b) => a.name.localeCompare(b.name));
}

export function coverageFor(
  d: Pick<Directory, 'coverage'>,
  jurisdiction: string,
  activity?: string,
) {
  return (
    d.coverage.find(
      (c) => c.jurisdiction === jurisdiction && c.activity === (activity || null),
    ) ?? {
      jurisdiction,
      activity: activity || null,
      status: 'unreviewed' as const,
      sourceIds: [],
      reviewedAt: null,
      note: 'Requirements for this scope have not been reconciled against official sources. An empty result does not mean no obligations apply.',
    }
  );
}
