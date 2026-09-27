import Link from 'next/link';
import DirectoryShell, { linkStyle, panel } from '@/components/marketing/directory/DirectoryShell';
import { ComparisonForm } from '@/components/marketing/directory/DirectoryFinderForm';
import DirectoryActionLink from '@/components/marketing/directory/DirectoryActionLink';
import { getDirectory, DIRECTORY_PATH as root } from '@/lib/compliance-directory';
import { directoryMetadata } from '@/lib/directory-metadata';
import { isVerified, typeLabels, type Requirement } from '@/lib/directory-model';

export const metadata = directoryMetadata(
  'Compare licenses and compliance requirements',
  'Compare scope, authority, assessment evidence, renewal and review status for up to four directory records.',
  root + '/compare',
);
export default async function ComparePage({
  searchParams,
}: {
  searchParams: Promise<{ id?: string | string[] }>;
}) {
  const { id } = await searchParams,
    d = getDirectory();
  const requested = [...new Set((Array.isArray(id) ? id : id ? [id] : []).filter(Boolean))];
  const selected = requested
    .filter((value) => d.requirements.some((r) => r.id === value))
    .slice(0, 4);
  const records = selected.map((value) => d.requirements.find((r) => r.id === value)!);
  const rows: [string, (r: Requirement) => React.ReactNode][] = [
    ['Type', (r) => typeLabels[r.type]],
    [
      'Review status',
      (r) =>
        isVerified(r)
          ? `Overview verified ${r.reviewedAt}`
          : r.status === 'verified'
            ? 'Review overdue'
            : r.status,
    ],
    [
      'Jurisdiction',
      (r) => r.jurisdictions.map((id) => d.jurisdictions.find((j) => j.id === id)!.name).join('; '),
    ],
    ['Authority / scheme owner', (r) => r.authority],
    ['Potential applicability', (r) => r.applicability || 'Pending verification'],
    ['Application / assessment', (r) => r.application || 'Pending verification'],
    [
      'Preparation evidence',
      (r) =>
        r.documents.length ? (
          <ul className="list-disc space-y-2 pl-4">
            {r.documents.map((x, i) => (
              <li key={i}>{x.text}</li>
            ))}
          </ul>
        ) : (
          'Pending verification'
        ),
    ],
    ['Renewal', (r) => r.renewal || 'Pending verification'],
    ['Current edition / status', (r) => r.version || r.currentStatus],
    ['Next review', (r) => r.nextReviewAt],
    [
      'Official next step',
      (r) => (
        <DirectoryActionLink href={r.applicationUrl} className={linkStyle}>
          Official application or guidance
        </DirectoryActionLink>
      ),
    ],
    [
      'Checklist',
      (r) =>
        isVerified(r) ? (
          <DirectoryActionLink
            href={`${root}/checklists/${r.id}`}
            event="directory_checklist_download"
            className={linkStyle}
          >
            Download reviewed preparation checklist (.txt)
          </DirectoryActionLink>
        ) : (
          'Available after verification'
        ),
    ],
  ];
  return (
    <DirectoryShell
      title="Compare requirements"
      description="Compare up to four records before opening the official authority or scheme guidance. A comparison does not establish which requirements apply to your organization."
      path={root + '/compare'}
    >
      <ComparisonForm
        records={d.requirements
          .map(({ id, name }) => ({ id, name }))
          .sort((a, b) => a.name.localeCompare(b.name))}
        selected={selected}
      />
      {requested.length !== selected.length && (
        <p role="status" className={panel}>
          Choose up to four known directory records. Unknown or excess selections were omitted.
        </p>
      )}
      {records.length ? (
        <div
          className="overflow-x-auto rounded-xl border border-white/10"
          tabIndex={0}
          role="region"
          aria-label="Requirement comparison table; scroll horizontally on smaller screens"
        >
          <table className="w-full min-w-[640px] border-collapse text-left text-sm">
            <caption className="p-5 text-left text-base text-slate-200">
              Educational comparison · draft fields remain unverified
            </caption>
            <thead>
              <tr>
                <th scope="col" className="bg-slate-900 p-4">
                  Comparison
                </th>
                {records.map((r) => (
                  <th key={r.id} scope="col" className="min-w-56 bg-slate-900 p-4">
                    <Link href={r.canonicalPath} className={linkStyle}>
                      {r.name}
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map(([label, render]) => (
                <tr key={label} className="border-t border-white/10">
                  <th scope="row" className="p-4 align-top font-semibold text-slate-200">
                    {label}
                  </th>
                  {records.map((r) => (
                    <td key={r.id} className="p-4 align-top leading-relaxed">
                      {render(r)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className={panel}>
          Select requirements above to compare their scope, authority, evidence and renewal
          information.
        </p>
      )}
      <p className="text-sm text-slate-400">
        On small screens, scroll the table horizontally to compare each requirement. Verified means
        the published overview was checked against its named sources. It does not mean your
        organization is compliant, certified or licensed.
      </p>
    </DirectoryShell>
  );
}
