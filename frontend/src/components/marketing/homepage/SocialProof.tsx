import React from 'react';

export default function SocialProof() {
  return (
    <section className="bg-white/2 border-t border-white/5 border-b border-white/5 py-12 sm:py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8 sm:gap-12 md:gap-16">
          <p className="text-base sm:text-lg text-slate-400 max-w-md text-center md:text-left">
            Trusted by security-minded teams building in healthcare, fintech, SaaS,
            and enterprise IT.
          </p>
          <div className="flex gap-6 sm:gap-10 md:gap-16 w-full md:w-auto justify-center md:justify-end">
            {[
              { value: '4x', label: 'Faster readiness' },
              { value: '90%', label: 'Less eng time' },
              { value: '100+', label: 'Audits supported' },
            ].map((stat, idx) => (
              <div key={idx} className="text-center flex-1 md:flex-none">
                <div className="font-display text-2xl sm:text-3xl md:text-4xl font-bold text-slate-50 mb-1">
                  {stat.value}
                </div>
                <div className="text-xs sm:text-sm text-slate-500">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
