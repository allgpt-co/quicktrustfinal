import React from 'react';

export default function Platform() {
  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-12 sm:mb-16 animate-on-scroll">
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            Meet the Compliance Intelligence Platform
            <br />
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              (with engineers who execute)
            </span>
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            We don&apos;t just track compliance—we map the questions, find the gaps,
            and our engineers fix them.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {[
            {
              icon: (
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              ),
              title: 'Questionnaire → Policy Mapping',
              desc: 'Upload your customer security questionnaire (or choose SOC2/ISO/HIPAA). QuickTrust maps each question to the exact policy sections and controls—so answers are consistent, auditable, and fast.',
            },
            {
              icon: (
                <>
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </>
              ),
              title: 'Policy Gap Finder',
              desc: 'Our platform flags missing policy language, weak statements, and control mismatches—so you know exactly what will fail under audit or procurement review.',
            },
            {
              icon: (
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              ),
              title: 'Remediation Workbench',
              subtitle: '(Engineers Included)',
              desc: 'Every gap becomes an implementation task. Our security/DevOps engineers close it, validate it, and attach evidence—so progress is measurable, not theoretical.',
            },
          ].map((item, idx) => (
            <div
              key={idx}
              className="bg-white/2 border border-white/6 rounded-xl sm:rounded-2xl p-6 sm:p-8 transition-all hover:bg-white/4 hover:border-teal-400/20 hover:-translate-y-1 animate-on-scroll"
              style={{ animationDelay: `${(idx + 1) * 0.1}s` }}
            >
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-teal-400/10 rounded-xl sm:rounded-2xl flex items-center justify-center mb-4 sm:mb-6">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="w-6 h-6 sm:w-7 sm:h-7 text-teal-400"
                >
                  {item.icon}
                </svg>
              </div>
              <h3 className="font-display text-lg sm:text-xl font-semibold text-slate-50 mb-2 sm:mb-3">
                {item.title}
                {item.subtitle && (
                  <span className="block text-xs sm:text-sm text-slate-500 font-normal mt-1">
                    {item.subtitle}
                  </span>
                )}
              </h3>
              <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
