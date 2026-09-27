import Link from 'next/link';
import { isVerified, typeLabels, type Requirement } from '@/lib/directory-model';
import { linkStyle, panel } from './DirectoryShell';

export default function RequirementCards({ records }: { records: Requirement[] }) {
  if (!records.length)
    return (
      <p className={panel}>
        No records have been mapped for this selection. Coverage is incomplete; this does not
        establish that no obligations apply.
      </p>
    );
  return (
    <ul className="grid gap-4 md:grid-cols-2">
      {records.map((r) => (
        <li key={r.id} className={panel}>
          <div className="mb-3 flex flex-wrap gap-2 text-xs">
            <span className="rounded bg-white/5 px-2 py-1">{typeLabels[r.type]}</span>
            <span
              className={`rounded px-2 py-1 ${isVerified(r) ? 'bg-teal-400/10 text-teal-200' : 'bg-amber-200/10 text-amber-100'}`}
            >
              {isVerified(r)
                ? 'Overview verified'
                : r.status === 'verified'
                  ? 'Review overdue'
                  : r.status}
            </span>
          </div>
          <h3 className="text-xl font-semibold">
            <Link href={r.canonicalPath} className={linkStyle}>
              {r.name}
            </Link>
          </h3>
          <p className="mt-3 text-sm leading-relaxed text-slate-300">{r.summary}</p>
          <p className="mt-3 text-xs text-slate-400">
            {r.jurisdictions.join(', ')} · {r.authority}
          </p>
          <Link
            href={`/compliance-directory/compare?id=${r.id}`}
            className="mt-4 inline-block text-sm text-teal-300 underline underline-offset-4"
          >
            Compare this requirement
          </Link>
        </li>
      ))}
    </ul>
  );
}
