'use client';

import { useState } from 'react';
import { homepageFAQs } from '@/lib/homepage-faqs';

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);



  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-slate-900" id="faq">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
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
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            FAQ
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            Questions we hear most
          </h2>
        </div>

        <div className="space-y-3 sm:space-y-4">
          {homepageFAQs.map((faq, idx) => (
            <div
              key={idx}
              className={`bg-white/2 border rounded-xl sm:rounded-2xl overflow-hidden transition-all ${
                openIndex === idx
                  ? 'border-white/10'
                  : 'border-white/6 hover:border-white/10'
              }`}
            >
              <button
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setOpenIndex(openIndex === idx ? null : idx);
                }}
                suppressHydrationWarning
                className="w-full p-4 sm:p-6 flex items-center justify-between text-left bg-transparent border-none cursor-pointer touch-manipulation"
              >
                <h4 className="font-display text-base sm:text-lg font-semibold text-slate-200 pr-3 sm:pr-4">
                  {faq.question}
                </h4>
                <div
                  className={`w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center transition-all flex-shrink-0 ${
                    openIndex === idx
                      ? 'bg-teal-400/15'
                      : 'bg-white/5'
                  }`}
                >
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className={`w-4 h-4 sm:w-4.5 sm:h-4.5 transition-transform ${
                      openIndex === idx
                        ? 'text-teal-400 rotate-180'
                        : 'text-slate-400'
                    }`}
                  >
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </div>
              </button>
              <div
                className={`overflow-hidden transition-all ${
                  openIndex === idx ? 'max-h-96' : 'max-h-0'
                }`}
              >
                <div className="px-4 sm:px-6 pb-4 sm:pb-6">
                  <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
                    {faq.answer}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
