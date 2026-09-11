import React from 'react';

export default function Differentiator(): React.JSX.Element {
  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-slate-900 relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] sm:w-[400px] sm:h-[400px] md:w-[600px] md:h-[600px] rounded-full border border-white/3"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] sm:w-[500px] sm:h-[500px] md:w-[800px] md:h-[800px] rounded-full border border-white/3"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] sm:w-[600px] sm:h-[600px] md:w-[1000px] md:h-[1000px] rounded-full border border-white/3"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
        <div className="text-center mb-12 sm:mb-16 lg:mb-20 animate-on-scroll">
          <span className="inline-flex items-center gap-2 text-sm font-semibold text-teal-400 uppercase tracking-wider mb-4">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            Why QuickTrust
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            Most firms do one thing.
            <br />
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              We do the full loop.
            </span>
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] gap-8 sm:gap-12 lg:gap-16 items-center">
          <div className="bg-white/2 border border-white/6 rounded-2xl sm:rounded-3xl p-6 sm:p-8 lg:p-10 opacity-70 animate-on-scroll">
            <div className="text-center mb-6 sm:mb-8 pb-4 sm:pb-6 border-b border-white/10">
              <h3 className="text-lg sm:text-xl text-slate-300">Traditional Approach</h3>
            </div>
            <ul className="list-none p-0 m-0 space-y-3">
              {[
                'Consultants produce documents',
                'Developers implement without audit context',
                "Auditors don't implement",
                'Your team coordinates everyone',
              ].map((item, idx) => (
                <li
                  key={idx}
                  className="flex items-start gap-3 text-sm text-slate-400 py-3"
                >
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className="w-5 h-5 text-slate-600 flex-shrink-0 mt-0.5"
                  >
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div className="hidden lg:flex w-16 h-16 xl:w-20 xl:h-20 bg-slate-800 border border-white/10 rounded-full items-center justify-center font-display text-lg xl:text-xl font-bold text-slate-400">
            VS
          </div>

          <div className="bg-white/2 border border-teal-400/30 rounded-2xl sm:rounded-3xl p-6 sm:p-8 lg:p-10 bg-teal-400/5 animate-on-scroll">
            <div className="text-center mb-6 sm:mb-8 pb-4 sm:pb-6 border-b border-white/10">
              <h3 className="text-lg sm:text-xl text-teal-400">QuickTrust</h3>
            </div>
            <ul className="list-none p-0 m-0 space-y-3">
              {[
                'Maps every framework/customer question to your policy + control library',
                'Detects policy gaps + control mismatches automatically (before audit)',
                'Turns gaps into engineering tasks; we implement + attach evidence',
                'Ongoing drift detection: policies, controls, and evidence stay aligned',
                'Compliance Architects who understand audits',
                'Security Engineers who implement controls',
                'DevOps who harden your infrastructure',
                'Evidence Ops who organize your proof',
              ].map((item, idx) => (
                <li
                  key={idx}
                  className="flex items-start gap-3 text-sm text-slate-300 py-3"
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
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
