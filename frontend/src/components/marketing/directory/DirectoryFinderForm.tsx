'use client';
import { useState } from 'react';
import type { Industry, Jurisdiction, Requirement } from '@/lib/directory-model';
import { requirementTypes, typeLabels } from '@/lib/directory-model';
import { ancestors, type DirectoryFilter } from '@/lib/directory-search';
import { trackDirectoryEvent } from '@/lib/marketing-analytics';

const inputStyle =
  'mt-2 block min-h-11 w-full min-w-0 rounded-lg border border-slate-600 bg-slate-950 p-3 text-base text-white';
export default function DirectoryFinderForm({
  jurisdictions,
  industries,
  initial,
}: {
  jurisdictions: Jurisdiction[];
  industries: Industry[];
  initial: DirectoryFilter;
}) {
  const countryFor = (id?: string) =>
    id
      ? ancestors(id, jurisdictions).find(
          (x) => jurisdictions.find((j) => j.id === x)?.kind === 'country',
        ) || id
      : '';
  const [location, setLocation] = useState(countryFor(initial.location));
  const [subdivision, setSubdivision] = useState(
    initial.location !== countryFor(initial.location) ? initial.location || '' : '',
  );
  const countries = jurisdictions
    .filter((j) => ['country', 'supranational', 'international'].includes(j.kind))
    .sort((a, b) => a.name.localeCompare(b.name));
  const regions = jurisdictions
    .filter((j) => j.id !== location && ancestors(j.id, jurisdictions).includes(location))
    .sort((a, b) => a.name.localeCompare(b.name));
  return (
    <form
      action="/compliance-directory/finder"
      method="get"
      onSubmit={() => trackDirectoryEvent('directory_search')}
      className="rounded-2xl border border-white/10 bg-slate-900/60 p-5 sm:p-7"
    >
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <label className="min-w-0 text-sm font-medium">
          Operating country or territory
          <select
            name="location"
            value={location}
            onChange={(e) => {
              setLocation(e.target.value);
              setSubdivision('');
            }}
            className={inputStyle}
          >
            <option value="">Any location</option>
            {countries.map((j) => (
              <option key={j.id} value={j.id}>
                {j.name}
              </option>
            ))}
          </select>
        </label>
        <label className="min-w-0 text-sm font-medium">
          State, province or local jurisdiction
          <select
            name="subdivision"
            value={subdivision}
            onChange={(e) => setSubdivision(e.target.value)}
            className={inputStyle}
          >
            <option value="">All recorded jurisdictions</option>
            {regions.map((j) => (
              <option key={j.id} value={j.id}>
                {j.name} ({j.id})
              </option>
            ))}
          </select>
        </label>
        <label className="min-w-0 text-sm font-medium">
          Customer or export market
          <select name="market" defaultValue={initial.market || ''} className={inputStyle}>
            <option value="">No additional market selected</option>
            {countries.map((j) => (
              <option key={j.id} value={j.id}>
                {j.name}
              </option>
            ))}
          </select>
        </label>
        <label className="min-w-0 text-sm font-medium">
          Business activity (ISIC Rev.5)
          <select name="activity" defaultValue={initial.activity || ''} className={inputStyle}>
            <option value="">All activities</option>
            {industries.map((i) => (
              <option key={i.id} value={i.id}>
                {i.id} — {i.name}
              </option>
            ))}
          </select>
        </label>
        <label className="min-w-0 text-sm font-medium">
          Requirement type
          <select name="type" defaultValue={initial.type || ''} className={inputStyle}>
            <option value="">All types</option>
            {requirementTypes.map((t) => (
              <option key={t} value={t}>
                {typeLabels[t]}
              </option>
            ))}
          </select>
        </label>
        <label className="min-w-0 text-sm font-medium">
          Review status
          <select name="status" defaultValue={initial.status || ''} className={inputStyle}>
            <option value="">All statuses</option>
            <option value="draft">Draft</option>
            <option value="verified">Verified overview</option>
            <option value="superseded">Superseded</option>
            <option value="withdrawn">Withdrawn</option>
          </select>
        </label>
        <label className="min-w-0 text-sm font-medium sm:col-span-2">
          Requirement name or keyword
          <input
            name="q"
            type="search"
            maxLength={120}
            defaultValue={initial.query || ''}
            className={inputStyle}
            placeholder="For example, food, contractor or ISO 9001"
          />
        </label>
      </div>
      <div className="mt-6 flex flex-wrap items-center gap-5">
        <button
          type="submit"
          className="min-h-11 rounded-lg bg-teal-300 px-6 py-3 font-semibold text-slate-950"
        >
          Find potentially relevant requirements
        </button>
        <a className="text-sm text-teal-300 underline" href="/compliance-directory/finder">
          Clear filters
        </a>
      </div>
      <p className="mt-4 text-xs leading-relaxed text-slate-400">
        Local jurisdictions are still being added. Market selection broadens the research results;
        it does not determine extraterritorial legal applicability. Search terms and selections are
        not sent to Google Analytics.
      </p>
    </form>
  );
}

export function ComparisonForm({
  records,
  selected,
}: {
  records: Pick<Requirement, 'id' | 'name'>[];
  selected: string[];
}) {
  return (
    <form
      action="/compliance-directory/compare"
      method="get"
      onSubmit={() => trackDirectoryEvent('directory_compare')}
      className="rounded-2xl border border-white/10 bg-slate-900/60 p-5"
    >
      <div className="grid gap-4 sm:grid-cols-2">
        {[0, 1, 2, 3].map((index) => (
          <label key={index} className="min-w-0 text-sm">
            Requirement {index + 1}
            <select name="id" defaultValue={selected[index] || ''} className={inputStyle}>
              <option value="">Choose a requirement</option>
              {records.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name}
                </option>
              ))}
            </select>
          </label>
        ))}
      </div>
      <button
        type="submit"
        className="mt-5 min-h-11 rounded-lg bg-teal-300 px-6 py-3 font-semibold text-slate-950"
      >
        Compare selected requirements
      </button>
    </form>
  );
}
