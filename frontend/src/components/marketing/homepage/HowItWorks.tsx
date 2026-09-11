import React from 'react';

export default function HowItWorks() {
  const steps = [
    {
      number: '1',
      title: 'Map & Score',
      subtitle: 'Question → Policy → Control coverage',
      desc: 'We map every framework and customer questionnaire to your policies and controls, then score your coverage.',
      deliverables: ['Scope', 'Control map', 'Initial gaps'],
    },
    {
      number: '2',
      title: 'Fix & Prove',
      subtitle: 'Engineers implement + evidence',
      desc: 'Our security/DevOps engineers close gaps, validate controls, and attach audit-ready evidence.',
      deliverables: ['Closed gaps', 'Evidence pack', 'Weekly progress'],
    },
    {
      number: '3',
      title: 'Certify & Maintain',
      subtitle: 'Audit coordination + continuous compliance',
      desc: 'We coordinate with auditors, maintain your evidence portal, and track changes to keep you compliant.',
      deliverables: ['Auditor-ready portal', 'Ongoing monitoring', 'Change tracking'],
    },
  ];

  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-gradient-to-b from-slate-950 to-slate-900" id="how-it-works">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
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
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
            How It Works
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            From call to certified in{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              three steps
            </span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-10 relative">
          <div className="hidden md:block absolute top-[50px] sm:top-[60px] left-[15%] right-[15%] h-0.5 bg-gradient-to-r from-teal-500 via-teal-400 to-teal-500 opacity-30"></div>
          {steps.map((step, idx) => (
            <div
              key={idx}
              className="text-center relative z-10 animate-on-scroll"
              style={{ animationDelay: `${(idx + 1) * 0.1}s` }}
            >
              <div className="w-24 h-24 sm:w-28 sm:h-28 md:w-30 md:h-30 mx-auto mb-6 sm:mb-8 bg-teal-400/10 border-2 border-teal-400/20 rounded-full flex items-center justify-center relative z-10">
                <div className="w-16 h-16 sm:w-18 sm:h-18 md:w-20 md:h-20 bg-gradient-primary rounded-full flex items-center justify-center font-display text-2xl sm:text-3xl font-bold text-slate-950">
                  {step.number}
                </div>
              </div>
              <h3 className="font-display text-lg sm:text-xl font-semibold text-slate-50 mb-2 sm:mb-3">
                {step.title}
              </h3>
              <p className="text-xs sm:text-sm text-teal-400 mb-3 sm:mb-4 font-medium">{step.subtitle}</p>
              <p className="text-xs sm:text-sm text-slate-400 max-w-xs mx-auto mb-4 sm:mb-5">
                {step.desc}
              </p>
              <div className="bg-white/3 rounded-lg sm:rounded-xl p-3 sm:p-4 text-left">
                <p className="text-[10px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                  Deliverables:
                </p>
                <ul className="list-none p-0 m-0 space-y-1">
                  {step.deliverables.map((item, itemIdx) => (
                    <li
                      key={itemIdx}
                      className="text-[10px] sm:text-xs text-slate-400 py-1 flex items-center gap-2"
                    >
                      <span className="w-1 h-1 bg-teal-400 rounded-full flex-shrink-0"></span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
