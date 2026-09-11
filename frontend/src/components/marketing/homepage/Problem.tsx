import React from 'react';

export default function Problem() {
  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-gradient-to-b from-slate-950 to-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-12 sm:mb-16 lg:mb-20 max-w-2xl mx-auto animate-on-scroll">
          <span className="inline-flex items-center gap-2 text-sm font-semibold text-teal-400 uppercase tracking-wider mb-4">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            The Problem
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            Compliance isn&apos;t hard.{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              It&apos;s distracting.
            </span>
          </h2>
          <p className="text-lg text-slate-400">
            It steals engineering cycles, delays enterprise deals, and creates
            last-minute audit surprises.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          {[
            {
              number: '01',
              icon: (
                <>
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </>
              ),
              title: 'For CEOs/Founders:',
              subtitle: '"Enterprise deals stall in security review."',
              desc: 'Procurement questionnaires pile up. Answers are inconsistent. Deals get delayed or lost.',
            },
            {
              number: '02',
              icon: (
                <>
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </>
              ),
              title: 'For CTOs/CIOs:',
              subtitle: '"Your roadmap gets hijacked by compliance busywork."',
              desc: "Security and compliance work gets deprioritized when product deadlines loom—until it can't be ignored.",
            },
            {
              number: '03',
              icon: (
                <>
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="9" y1="15" x2="15" y2="15"></line>
                </>
              ),
              title: 'For CISOs:',
              subtitle: '"Evidence is scattered, policies drift, and audits become fire drills."',
              desc: 'Documentation without implementation leaves you exposed during technical audits. Last-minute scrambling becomes the norm.',
            },
          ].map((problem, idx) => (
            <div
              key={idx}
              className="bg-white/2 border border-white/6 rounded-xl sm:rounded-2xl p-6 sm:p-8 relative transition-all hover:bg-white/4 hover:border-coral/30 hover:-translate-y-1 animate-on-scroll"
              style={{ animationDelay: `${(idx + 1) * 0.1}s` }}
            >
              <div className="absolute top-4 right-4 sm:top-6 sm:right-6 font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-white/3 leading-none">
                {problem.number}
              </div>
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-coral/10 rounded-xl sm:rounded-2xl flex items-center justify-center mb-4 sm:mb-5">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="w-6 h-6 sm:w-7 sm:h-7 text-coral"
                >
                  {problem.icon}
                </svg>
              </div>
              <h3 className="font-display text-base sm:text-lg font-semibold text-slate-200 mb-2 sm:mb-3">
                {problem.title}
                <br />
                {problem.subtitle}
              </h3>
              <p className="text-xs sm:text-sm text-slate-500">{problem.desc}</p>
            </div>
          ))}
        </div>

        <div className="bg-gradient-to-br from-white/5 to-white/2 border border-teal-400/20 rounded-xl sm:rounded-2xl p-6 sm:p-8 lg:p-10 text-center relative overflow-hidden animate-on-scroll">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(45,212,191,0.1)_0%,transparent_70%)]"></div>
          <h3 className="font-display text-xl sm:text-2xl font-semibold text-slate-50 mb-2 sm:mb-3 relative">
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              QuickTrust is the platform that finds the gaps—and the team that fixes
              them.
            </span>
          </h3>
          <p className="text-base sm:text-lg text-slate-400 max-w-2xl mx-auto relative">
            We don&apos;t just track compliance—we map the questions, find the gaps, and
            our engineers fix them.
          </p>
        </div>
      </div>
    </section>
  );
}
