import Link from 'next/link';
import type { ReactNode } from 'react';

interface SEOPageShellProps {
  eyebrow: string;
  title: string;
  description: string;
  bullets: string[];
  children?: ReactNode;
  ctaHref?: string;
  ctaLabel?: string;
}

export default function SEOPageShell({
  eyebrow,
  title,
  description,
  bullets,
  children,
  ctaHref = '/#lead-form',
  ctaLabel = 'Get a readiness snapshot',
}: SEOPageShellProps) {
  return (
    <main id="main-content" className="min-h-screen bg-slate-950 pt-28 sm:pt-36">
      <section className="max-w-7xl mx-auto px-4 sm:px-6 pb-16 sm:pb-24">
        <nav className="text-sm text-slate-500 mb-8" aria-label="Breadcrumb">
          <Link href="/" className="text-slate-500 hover:text-teal-400 no-underline">Home</Link>
          <span className="mx-2">/</span>
          <span className="text-slate-300">{title}</span>
        </nav>
        <span className="inline-flex rounded-full border border-teal-500/20 bg-teal-500/10 px-4 py-2 text-sm font-medium text-teal-300">
          {eyebrow}
        </span>
        <h1 className="mt-6 max-w-4xl font-display text-4xl font-bold leading-tight text-slate-50 sm:text-5xl lg:text-6xl">
          {title}
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-relaxed text-slate-400 sm:text-xl">{description}</p>
        <Link
          href={ctaHref}
          className="mt-10 inline-flex items-center justify-center rounded-xl bg-gradient-primary px-7 py-3.5 font-display font-semibold text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.3)] transition hover:-translate-y-0.5"
        >
          {ctaLabel}
        </Link>
      </section>

      {bullets.length > 0 && <section className="border-t border-white/5 py-16 sm:py-24">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 sm:px-6 md:grid-cols-2">
          {bullets.map((bullet) => (
            <div key={bullet} className="rounded-2xl border border-white/10 bg-white/5 p-6 sm:p-8">
              <p className="leading-relaxed text-slate-300">{bullet}</p>
            </div>
          ))}
        </div>
      </section>}

      {children && <section className="border-t border-white/5 py-16 sm:py-24">{children}</section>}
    </main>
  );
}
