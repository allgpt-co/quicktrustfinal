'use client';

import React from 'react';
import { useModal } from './ModalProvider';

export default function FinalCTA() {
  const { openModal } = useModal();
  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-gradient-to-b from-slate-900 to-slate-950 relative overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute w-[300px] h-[300px] sm:w-[400px] sm:h-[400px] lg:w-[600px] lg:h-[600px] rounded-full blur-[100px] opacity-30 bg-teal-600 top-[-50%] left-[20%]"></div>
        <div className="absolute w-[300px] h-[300px] sm:w-[400px] sm:h-[400px] lg:w-[600px] lg:h-[600px] rounded-full blur-[100px] opacity-15 bg-violet bottom-[-50%] right-[20%]"></div>
      </div>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 relative text-center">
        <div className="animate-on-scroll">
          <h2 className="font-display text-[clamp(1.75rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4 sm:mb-6">
            Ready to get certified — with engineers who{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              implement
            </span>
            , not just advise?
          </h2>
          <p className="text-lg sm:text-xl text-slate-400 mb-8 sm:mb-10">
            We work best with teams that want a real security program — not a
            paperwork exercise.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center mb-6 sm:mb-8">
            <button
              onClick={openModal}
              suppressHydrationWarning
              className="inline-flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3 sm:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] touch-manipulation"
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
              Contact Us
            </button>
            <a
              href="mailto:hello@quicktrust.io"
              className="inline-flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3 sm:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all bg-white/5 text-slate-200 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-white/20 hover:-translate-y-0.5 touch-manipulation"
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
              Email Us
            </a>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 italic">
            Typically: audit-ready in weeks, not months.
          </p>
        </div>
      </div>
    </section>
  );
}
