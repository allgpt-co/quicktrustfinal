import Link from 'next/link';
import type { ReactNode } from 'react';
import PageBreadcrumbSchema from '@/components/marketing/schema/PageBreadcrumbSchema';
import { DIRECTORY_PATH as root, DIRECTORY_ORIGIN } from '@/lib/compliance-directory';

export const panel = 'rounded-2xl border border-white/10 bg-slate-900/60 p-5 sm:p-7';
export const linkStyle =
  'text-teal-300 underline decoration-teal-300/30 underline-offset-4 hover:text-teal-100';
export const buttonStyle =
  'inline-flex min-h-11 items-center justify-center rounded-lg bg-teal-300 px-5 py-3 font-semibold text-slate-950 no-underline hover:bg-teal-200';

export default function DirectoryShell({
  title,
  description,
  path,
  children,
  draft = false,
  breadcrumbs = [],
}: {
  title: string;
  description: string;
  path: string;
  children: ReactNode;
  draft?: boolean;
  breadcrumbs?: { name: string; path: string }[];
}) {
  const crumbs = [
    { name: 'Home', path: '/' },
    ...(path === root ? [] : [{ name: 'Compliance directory', path: root }]),
    ...breadcrumbs,
    { name: title, path },
  ];
  return (
    <main
      id="main-content"
      className="mx-auto min-h-screen max-w-7xl px-4 pb-20 pt-28 sm:px-6 sm:pt-36"
    >
      <PageBreadcrumbSchema
        items={crumbs.map((c) => ({ name: c.name, item: DIRECTORY_ORIGIN + c.path }))}
      />
      <nav
        aria-label="Breadcrumb"
        className="mb-7 flex flex-wrap gap-x-2 gap-y-1 text-sm text-slate-400"
      >
        {crumbs.map((c, i) => (
          <span key={c.path}>
            {i > 0 && (
              <span className="mr-2" aria-hidden="true">
                /
              </span>
            )}
            {i === crumbs.length - 1 ? (
              <span aria-current="page">{c.name}</span>
            ) : (
              <Link className={linkStyle} href={c.path}>
                {c.name}
              </Link>
            )}
          </span>
        ))}
      </nav>
      <p className="text-sm font-semibold uppercase tracking-widest text-teal-300">
        Global compliance research
      </p>
      <h1 className="mt-4 max-w-5xl font-display text-3xl font-bold leading-tight text-white sm:text-5xl">
        {title}
      </h1>
      <p className="mt-5 max-w-4xl text-lg leading-relaxed text-slate-300">{description}</p>
      <nav aria-label="Directory" className="my-8 flex flex-wrap gap-2">
        {[
          [root, 'Overview'],
          [root + '/finder', 'Find requirements'],
          [root + '/countries', 'Countries'],
          [root + '/industries', 'Industries'],
          [root + '/compare', 'Compare'],
          [root + '/coverage', 'Coverage'],
          [root + '/sources', 'Sources'],
          [root + '/updates', 'Updates'],
        ].map(([href, label]) => (
          <Link
            key={href}
            href={href}
            aria-current={path === href ? 'page' : undefined}
            className={`rounded-lg border px-3 py-2 text-sm no-underline ${path === href ? 'border-teal-400/40 bg-teal-400/10 text-teal-200' : 'border-white/10 text-slate-300 hover:border-teal-400/40'}`}
          >
            {label}
          </Link>
        ))}
      </nav>
      {draft && (
        <aside className="mb-8 rounded-xl border border-amber-300/30 bg-amber-300/5 p-5 text-amber-100">
          <strong>Draft — requirements not yet fully verified</strong>
          <p className="mt-2 text-sm leading-relaxed">
            This page is public for research and is excluded from search indexing. Missing records
            or fields do not mean that no requirements apply. Check the official authority before
            acting.
          </p>
        </aside>
      )}
      <div className="space-y-8 [&_a]:break-words [&_button]:touch-manipulation">{children}</div>
    </main>
  );
}
