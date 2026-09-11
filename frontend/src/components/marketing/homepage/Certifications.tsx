import React from 'react';

export default function Certifications() {
  const certifications = [
    { name: 'SOC 2 Type I & II', desc: 'Trust services criteria', popular: true, badge: 'Most Popular' },
    { name: 'ISO 27001', desc: 'Information security', popular: true, badge: 'Popular' },
    { name: 'ISO 42001', desc: 'AI governance', popular: false },
    { name: 'HIPAA', desc: 'Healthcare compliance', popular: false },
    { name: 'HITRUST', desc: 'Healthcare security', popular: false },
    { name: 'PCI DSS', desc: 'Payment security', popular: false },
    { name: 'GDPR', desc: 'Data protection', popular: false },
    { name: 'Custom', desc: 'Your requirements', popular: false },
  ];

  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-slate-950" id="certifications">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
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
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            Certifications We Support
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            Every framework your customers demand
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 sm:gap-5">
          {certifications.map((cert, idx) => (
            <div
              key={idx}
              className={`bg-white/2 border rounded-xl sm:rounded-2xl p-5 sm:p-6 lg:p-7 text-center transition-all hover:bg-white/5 hover:border-teal-400/30 hover:-translate-y-1 cursor-pointer relative touch-manipulation ${
                cert.popular
                  ? 'border-teal-400/30 bg-teal-400/5'
                  : 'border-white/6'
              } animate-on-scroll`}
              style={{ animationDelay: `${(idx + 1) * 0.1}s` }}
            >
              {cert.popular && (
                <div className="absolute -top-2 sm:-top-2.5 left-1/2 -translate-x-1/2 bg-gradient-primary text-slate-950 text-[10px] sm:text-xs font-bold px-2 sm:px-3 py-0.5 sm:py-1 rounded-full uppercase tracking-wider">
                  {cert.badge}
                </div>
              )}
              <div
                className={`w-10 h-10 sm:w-12 sm:h-12 mx-auto mb-3 sm:mb-4 rounded-lg sm:rounded-xl flex items-center justify-center ${
                  cert.popular ? 'bg-teal-400/15' : 'bg-white/5'
                }`}
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className={`w-5 h-5 sm:w-6 sm:h-6 ${cert.popular ? 'text-teal-400' : 'text-slate-400'}`}
                >
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
              <h4 className="font-display text-sm sm:text-base font-semibold text-slate-200 mb-1">
                {cert.name}
              </h4>
              <p className="text-[10px] sm:text-xs text-slate-500">{cert.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
