'use client';

import { useState } from 'react';

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const faqs = [
    {
      question: 'How fast can we get SOC 2 Type II?',
      answer:
        'Depends on scope and current maturity. We compress timelines by implementing controls and evidence workflows in parallel — not sequentially. Most teams see audit readiness in 6-12 weeks.',
    },
    {
      question: 'Do you guarantee we pass?',
      answer:
        'No one can guarantee an audit outcome, but we drastically improve readiness by aligning controls and evidence to audit expectations before the audit begins. Our track record speaks for itself.',
    },
    {
      question: 'Will this drain our engineering time?',
      answer:
        'We minimize load by doing the implementation work and asking your team only for approvals, access, and validation. Most customers report less than 2 hours/week of eng involvement.',
    },
    {
      question: 'Do you work with our auditor?',
      answer:
        "Yes — we coordinate audit timelines, evidence requests, and remediation closures with your chosen auditor. We can also recommend auditors if you don't have one yet.",
    },
    {
      question: "We're on AWS/GCP/Azure — can you handle it?",
      answer:
        "Absolutely. We're built for cloud-first, modern SaaS environments. Our team has deep expertise across all major cloud providers and can work with your existing infrastructure.",
    },
    {
      question: 'How does the platform map questionnaires to our policies?',
      answer:
        "We map questions to control IDs + exact policy sections; you get a reusable response library with audit trails. Upload any SOC2/ISO/HIPAA questionnaire, and we'll show you which policies and controls answer each question—so responses are consistent and auditable.",
    },
    {
      question: 'What do you mean by "policy gaps"—and how do you find them?',
      answer:
        'We compare framework requirements vs. your policy language + implemented controls; we flag missing/weak areas and generate a prioritized remediation plan. For example, if SOC2 requires "quarterly access reviews" but your policy says "annual," we flag it. If a control is documented but not implemented, we surface that too.',
    },
    {
      question: 'Do you actually implement the fixes?',
      answer:
        "Yes—our security/DevOps engineers handle the changes (IAM, logging, encryption, backups, SDLC controls, etc.). Your team reviews/approves; we execute and attach evidence. We don't just tell you what to fix—we fix it, validate it, and document it for audit.",
    },
  ];

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
          {faqs.map((faq, idx) => (
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
