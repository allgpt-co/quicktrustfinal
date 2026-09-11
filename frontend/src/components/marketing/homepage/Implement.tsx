import React from 'react';

export default function Implement() {
  const categories = [
    {
      title: 'Cloud & Infrastructure',
      icon: (
        <>
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
          <line x1="8" y1="21" x2="16" y2="21"></line>
          <line x1="12" y1="17" x2="12" y2="21"></line>
        </>
      ),
      items: [
        'IAM least privilege + role separation',
        'MFA/SSO enforcement',
        'Encryption at rest/in transit',
        'Network segmentation & WAF',
        'Centralized logging (SIEM-ready)',
        'Backup & DR strategy',
      ],
    },
    {
      title: 'App & SDLC Controls',
      icon: (
        <>
          <polyline points="16 18 22 12 16 6"></polyline>
          <polyline points="8 6 2 12 8 18"></polyline>
        </>
      ),
      items: [
        'Secure CI/CD pipelines',
        'SAST/DAST integration',
        'Secret scanning & rotation',
        'Change management workflows',
        'Vulnerability management',
        'Environment separation',
      ],
    },
    {
      title: 'Policies & Process',
      icon: (
        <>
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </>
      ),
      items: [
        'InfoSec policies (tailored)',
        'Risk assessments',
        'Vendor due diligence',
        'Incident response playbooks',
        'Security awareness training',
        'Access reviews (quarterly)',
      ],
    },
  ];

  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-slate-900">
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
              <polyline points="16 18 22 12 16 6"></polyline>
              <polyline points="8 6 2 12 8 18"></polyline>
            </svg>
            Developer-Led Compliance
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            What we actually{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              implement
            </span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 sm:gap-6">
          {categories.map((category, idx) => (
            <div
              key={idx}
              className="bg-white/2 border border-white/6 rounded-xl sm:rounded-2xl p-6 sm:p-8 transition-all hover:bg-white/4 hover:border-teal-400/20 animate-on-scroll"
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
                  {category.icon}
                </svg>
              </div>
              <h3 className="font-display text-lg sm:text-xl font-semibold text-slate-50 mb-3 sm:mb-4">
                {category.title}
              </h3>
              <ul className="list-none p-0 m-0 space-y-2">
                {category.items.map((item, itemIdx) => (
                  <li
                    key={itemIdx}
                    className="text-xs sm:text-sm text-slate-400 py-2 border-b border-white/5 last:border-0 flex items-center gap-2 sm:gap-2.5"
                  >
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-teal-500 flex-shrink-0"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
