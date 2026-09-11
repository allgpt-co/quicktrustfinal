'use client';

import { useModal } from './ModalProvider';

export default function Hero() {
  const { openModal } = useModal();
  return (
    <section className="min-h-screen flex items-center relative pt-[80px] sm:pt-[100px] overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute w-[400px] h-[400px] sm:w-[600px] sm:h-[600px] lg:w-[800px] lg:h-[800px] rounded-full blur-[120px] opacity-40 bg-teal-600 top-[-20%] right-[-10%] animate-float"></div>
        <div className="absolute w-[400px] h-[400px] sm:w-[600px] sm:h-[600px] lg:w-[800px] lg:h-[800px] rounded-full blur-[120px] opacity-20 bg-purple-500 bottom-[-30%] left-[-10%] animate-float-reverse"></div>
      </div>
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[length:40px_40px] sm:bg-[length:60px_60px] [mask-image:radial-gradient(ellipse_at_center,black_30%,transparent_70%)]"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 relative z-10 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 sm:gap-16 lg:gap-20 items-center">
          <div className="animate-fadeInUp">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-teal-400/10 border border-teal-400/20 rounded-full text-sm text-teal-400 mb-6">
              <span className="w-2 h-2 bg-teal-400 rounded-full animate-pulse-slow"></span>
              Compliance Platform + Implementation Partner
            </div>
            <h1 className="font-display text-[clamp(2.5rem,6vw,4.5rem)] font-bold tracking-[-0.03em] text-slate-50 mb-6 leading-tight">
              Compliance Automation<br />
              <span className="bg-gradient-primary bg-clip-text text-transparent">
                Platform
              </span>{' '}
              for Audit-Ready Teams
            </h1>
            <p className="text-xl text-slate-400 mb-10 max-w-[540px]">
              QuickTrust is a compliance platform <em>plus</em> an implementation
              team. We map every framework and customer security question to your
              policies and controls, instantly surface gaps, and then our engineers
              close them—so you get certified faster with minimal internal lift.
            </p>
            <ul className="list-none p-0 m-0 mb-8 flex flex-col gap-3">
              {[
                {
                  title: 'Question → Policy Mapping:',
                  desc: 'Answer SOC2/ISO/HIPAA questionnaires with a policy-backed control map.',
                },
                {
                  title: 'Gap Detection:',
                  desc: 'Find missing policy language + control gaps before your auditor (or customer) does.',
                },
                {
                  title: 'Remediation Delivered:',
                  desc: 'Security/DevOps engineers implement the fixes + package audit-ready evidence.',
                },
              ].map((item, idx) => (
                <li
                  key={idx}
                  className="flex items-start gap-3 text-slate-300 text-[0.95rem]"
                >
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="var(--tw-color-teal-400)"
                    strokeWidth="2"
                    className="flex-shrink-0 mt-0.5"
                  >
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  <span>
                    <strong>{item.title}</strong> {item.desc}
                  </span>
                </li>
              ))}
            </ul>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 mb-8 sm:mb-12">
              <button
                onClick={openModal}
                suppressHydrationWarning
                className="inline-flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3.5 sm:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] relative overflow-hidden touch-manipulation"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="flex-shrink-0"
                >
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
                <span className="whitespace-nowrap">Contact Us</span>
              </button>
              <a
                href="#lead-form"
                className="inline-flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3.5 sm:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all bg-white/5 text-slate-200 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-white/20 hover:-translate-y-0.5 touch-manipulation"
              >
                Get a Fixed-Price Quote
              </a>
            </div>
            <p className="mt-4 text-sm text-slate-500 italic">
              Leave with a scope + control map + top risks + next steps (no prep
              required).
            </p>
            <p className="mt-3 text-[0.9rem] text-slate-400">
              After the call, we deliver your Readiness Snapshot in 48 hours:
              scope + control map + top 10 gaps + timeline.
            </p>
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 pt-6 sm:pt-8 border-t border-white/10 mt-8 sm:mt-12">
              <div className="flex">
                {['JM', 'SK', 'AL', 'RK'].map((initials, idx) => (
                  <div
                    key={idx}
                    className="w-8 h-8 sm:w-10 sm:h-10 rounded-full border-2 border-slate-900 -ml-2 sm:-ml-3 first:ml-0 bg-slate-700 flex items-center justify-center text-xs font-semibold text-slate-300"
                  >
                    {initials}
                  </div>
                ))}
              </div>
              <p className="text-sm text-slate-400">
                <strong className="text-slate-200">Audit-ready in weeks</strong> —
                Measurable control coverage, cleaner evidence, fewer surprises.
              </p>
            </div>
          </div>
          <div className="animate-fadeInUp-delayed relative mt-8 lg:mt-0">
            <div className="bg-gradient-to-br from-white/5 to-white/2 border border-white/10 rounded-2xl sm:rounded-3xl p-4 sm:p-6 lg:p-8 backdrop-blur-xl relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
              <div className="flex items-center justify-between mb-4 sm:mb-6">
                <span className="text-xs sm:text-sm text-slate-400 font-medium">
                  Compliance Dashboard
                </span>
                <div className="flex items-center gap-1.5 text-xs text-teal-400 font-semibold">
                  <span className="w-1.5 h-1.5 bg-teal-400 rounded-full"></span>
                  <span>Live</span>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2 sm:gap-3 mb-4 sm:mb-6">
                {[
                  { name: 'SOC 2', icon: 'shield' },
                  { name: 'ISO 27001', icon: 'clock' },
                  { name: 'HIPAA', icon: 'zap' },
                  { name: 'PCI DSS', icon: 'lock' },
                  { name: 'HITRUST', icon: 'settings' },
                  { name: 'GDPR', icon: 'cube' },
                ].map((item, idx) => (
                  <div
                    key={idx}
                    className="bg-white/3 border border-white/6 rounded-lg sm:rounded-xl p-2 sm:p-3 lg:p-4 text-center transition-all hover:bg-white/6 hover:border-teal-400/30 hover:-translate-y-0.5"
                  >
                    <div className="w-7 h-7 sm:w-8 sm:h-9 mx-auto mb-1.5 sm:mb-2 bg-teal-400/10 rounded-lg flex items-center justify-center">
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        className="w-4 h-4 sm:w-5 sm:h-5 text-teal-400"
                      >
                        {item.icon === 'shield' && (
                          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                        )}
                        {item.icon === 'clock' && (
                          <>
                            <circle cx="12" cy="12" r="10"></circle>
                            <path d="M12 6v6l4 2"></path>
                          </>
                        )}
                        {item.icon === 'zap' && (
                          <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                        )}
                        {item.icon === 'lock' && (
                          <>
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                          </>
                        )}
                        {item.icon === 'settings' && (
                          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                        )}
                        {item.icon === 'cube' && (
                          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                        )}
                      </svg>
                    </div>
                    <div className="text-[10px] sm:text-xs font-semibold text-slate-200 leading-tight">
                      {item.name}
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-black/20 rounded-lg sm:rounded-xl p-3 sm:p-4">
                <div className="flex justify-between items-center mb-2 sm:mb-3">
                  <span className="text-[10px] sm:text-xs text-slate-400">
                    Overall Audit Readiness
                  </span>
                  <span className="text-xs sm:text-sm font-semibold text-teal-400">78%</span>
                </div>
                <div className="h-1.5 sm:h-2 bg-white/10 rounded overflow-hidden">
                  <div
                    className="h-full bg-gradient-primary rounded animate-progressGrow"
                    style={{ width: '78%' }}
                  ></div>
                </div>
              </div>
            </div>
            <div className="hidden sm:block absolute top-[15%] lg:top-[20%] right-[-10px] lg:right-[-20px] bg-slate-800 border border-white/10 rounded-lg sm:rounded-xl px-3 sm:px-4 py-2 sm:py-3 flex items-center gap-2 text-xs sm:text-sm text-slate-200 shadow-xl animate-float">
              <div className="w-6 h-6 sm:w-8 sm:h-8 rounded-lg bg-teal-400/15 flex items-center justify-center flex-shrink-0">
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#2dd4bf"
                  strokeWidth="2"
                  className="sm:w-[18px] sm:h-[18px]"
                >
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <span className="whitespace-nowrap">Evidence uploaded</span>
            </div>
            <div className="hidden sm:block absolute bottom-[10%] lg:bottom-[15%] left-[-10px] lg:left-[-30px] bg-slate-800 border border-white/10 rounded-lg sm:rounded-xl px-3 sm:px-4 py-2 sm:py-3 flex items-center gap-2 text-xs sm:text-sm text-slate-200 shadow-xl animate-float" style={{ animationDelay: '1s' }}>
              <div className="w-6 h-6 sm:w-8 sm:h-8 rounded-lg bg-amber-400/15 flex items-center justify-center flex-shrink-0">
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#fbbf24"
                  strokeWidth="2"
                  className="sm:w-[18px] sm:h-[18px]"
                >
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
              <span className="whitespace-nowrap">3 gaps to resolve</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
