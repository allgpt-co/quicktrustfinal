'use client';

import React from 'react';
import { useModal } from './ModalProvider';

export default function Packages() {
  const { openModal } = useModal();
  const packages = [
    {
      title: 'Certification Fast Track',
      subtitle: '(Implementation Included)',
      tagline: '"Get certified without derailing product."',
      desc: 'Platform + security engineers + audit coordination.',
      features: [
        'Defined scope + control mapping',
        'Complete policy pack',
        'Implementation sprints (DevOps + security)',
        'Evidence library setup',
        'Full audit support',
      ],
      bestFor: 'Seed to Series C SaaS, fintech, and healthcare startups',
      buttonText: 'Get SOC 2 Ready',
      featured: false,
    },
    {
      title: 'Continuous Compliance Program',
      subtitle: '(Platform + Engineers)',
      tagline: '"Standardize controls across teams."',
      desc: 'Platform + security engineers + audit coordination.',
      features: [
        'Multi-team rollout & governance',
        'Control owners & reporting',
        'Continuous compliance program',
        'Vendor risk management',
        'Exception workflows',
      ],
      bestFor: 'Enterprises, regulated orgs, and global teams',
      buttonText: 'Talk to a Program Lead',
      featured: true,
      badge: 'Recommended',
    },
  ];

  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-slate-950 relative overflow-hidden" id="packages">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-[radial-gradient(ellipse_at_center,rgba(45,212,191,0.05)_0%,transparent_50%)]"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 relative">
        <div className="text-center mb-12 sm:mb-16 animate-on-scroll">
          <span className="inline-flex items-center gap-2 text-sm font-semibold text-teal-400 uppercase tracking-wider mb-4">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
            Packages
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            Choose your path to{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              compliance
            </span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {packages.map((pkg, idx) => (
            <div
              key={idx}
              className={`bg-gradient-to-br from-white/5 to-white/2 border rounded-2xl sm:rounded-3xl p-6 sm:p-8 lg:p-12 relative overflow-hidden transition-all hover:border-white/15 hover:-translate-y-1 ${
                pkg.featured
                  ? 'border-teal-400/30 bg-gradient-to-br from-teal-400/8 to-teal-400/2'
                  : 'border-white/8'
              } animate-on-scroll`}
              style={{ animationDelay: `${(idx + 1) * 0.1}s` }}
            >
              {pkg.featured && (
                <>
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-primary"></div>
                  <div className="absolute top-4 right-4 sm:top-6 sm:right-6 bg-teal-400/15 text-teal-400 text-[10px] sm:text-xs font-semibold px-2 sm:px-3 py-1 sm:py-1.5 rounded-full uppercase tracking-wider">
                    {pkg.badge}
                  </div>
                </>
              )}
              <div className="mb-6 sm:mb-8">
                <h3 className="font-display text-xl sm:text-2xl font-bold text-slate-50 mb-2">
                  {pkg.title}
                  <br />
                  <span className="text-xs sm:text-sm text-slate-500 font-normal not-italic">
                    {pkg.subtitle}
                  </span>
                </h3>
                <p className="text-base sm:text-lg text-slate-400 italic mb-2">{pkg.tagline}</p>
                <p className="text-xs sm:text-sm text-slate-500 not-italic">{pkg.desc}</p>
              </div>
              <ul className="list-none p-0 m-0 mb-8 space-y-3">
                {pkg.features.map((feature, featureIdx) => (
                  <li
                    key={featureIdx}
                    className="flex items-start gap-3 py-3 border-b border-white/5 last:border-0 text-sm text-slate-300"
                  >
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      className="w-5 h-5 text-teal-400 flex-shrink-0 mt-0.5"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              <div className="bg-black/20 rounded-lg sm:rounded-xl p-3 sm:p-4 mb-6 sm:mb-8">
                <p className="text-[10px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                  Best for
                </p>
                <p className="text-xs sm:text-sm text-slate-400">{pkg.bestFor}</p>
              </div>
              <button
                onClick={openModal}
                suppressHydrationWarning
                className={`w-full inline-flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3 sm:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all touch-manipulation ${
                  pkg.featured
                    ? 'bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)]'
                    : 'bg-white/5 text-slate-200 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-white/20 hover:-translate-y-0.5'
                }`}
              >
                {pkg.buttonText}
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
