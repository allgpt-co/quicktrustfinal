'use client';

import { FormEvent, useState, useRef } from 'react';

export default function LeadCapture() {
  const formRef = useRef<HTMLFormElement>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('idle');
    setErrorMessage('');

    const form = e.currentTarget || formRef.current;
    if (!form) {
      console.error('Form element not found');
      setIsSubmitting(false);
      return;
    }

    const formData = new FormData(form);
    const data = {
      email: formData.get('email') as string,
      company: formData.get('company') as string,
      targetFramework: formData.get('targetFramework') as string,
      targetTimeline: formData.get('targetTimeline') as string,
    };

    try {
      const response = await fetch('/api/readiness-snapshot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      // Check if response is ok before trying to parse JSON
      if (!response.ok) {
        let errorMessage = 'Failed to submit request';
        try {
          const errorResult = await response.json();
          errorMessage = errorResult.error || errorResult.details || errorMessage;
        } catch (parseError) {
          // If JSON parsing fails, use status text
          errorMessage = response.statusText || `Server error (${response.status})`;
        }
        throw new Error(errorMessage);
      }

      const result = await response.json();

      // Double check the result for success
      if (!result.success && result.error) {
        throw new Error(result.error);
      }

      setSubmitStatus('success');

      // Reset form safely using ref
      if (formRef.current) {
        formRef.current.reset();
      }

      // Reset success message after 5 seconds
      setTimeout(() => {
        setSubmitStatus('idle');
      }, 5000);
    } catch (error: any) {
      console.error('Error submitting form:', error);
      setSubmitStatus('error');

      // Provide user-friendly error messages
      let userMessage = 'Failed to submit request. Please try again.';
      if (error.message) {
        if (error.message.includes('email')) {
          userMessage = 'Please check your email address and try again.';
        } else if (error.message.includes('configured') || error.message.includes('service')) {
          userMessage = 'Service temporarily unavailable. Please try again later or contact support.';
        } else {
          userMessage = error.message;
        }
      }
      setErrorMessage(userMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-slate-950 relative overflow-hidden" id="lead-form">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_center,rgba(45,212,191,0.1)_0%,transparent_50%)]"></div>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 relative">
        <div className="text-center mb-8 sm:mb-12 animate-on-scroll">
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
            Free Assessment
          </span>
          <h2 className="font-display text-[clamp(2rem,4vw,3rem)] font-bold tracking-[-0.02em] text-slate-50 mb-4">
            Get a Free Readiness Snapshot
          </h2>
          <p className="text-lg text-slate-400">
            In 48 hours, we&apos;ll return your certification path, scope outline, top
            10 gaps, and estimated timeline.
          </p>
        </div>

        <form
          ref={formRef}
          onSubmit={handleSubmit}
          suppressHydrationWarning
          className="bg-gradient-to-br from-white/5 to-white/2 border border-white/10 rounded-2xl sm:rounded-3xl p-6 sm:p-8 lg:p-12 text-left animate-on-scroll"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-5 mb-4 sm:mb-5">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-slate-300">
                Work Email
              </label>
              <input
                type="email"
                name="email"
                suppressHydrationWarning
                className="px-4 py-3.5 bg-black/30 border border-white/10 rounded-xl font-body text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 placeholder:text-slate-600"
                placeholder="you@company.com"
                required
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-slate-300">Company</label>
              <input
                type="text"
                name="company"
                suppressHydrationWarning
                className="px-4 py-3.5 bg-black/30 border border-white/10 rounded-xl font-body text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 placeholder:text-slate-600"
                placeholder="Company name"
                required
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-slate-300">
                Target Framework
              </label>
              <select
                name="targetFramework"
                suppressHydrationWarning
                className="px-4 py-3.5 bg-black/30 border border-white/10 rounded-xl font-body text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 cursor-pointer appearance-none bg-[url('data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'20\' height=\'20\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%2394a3b8\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E')] bg-no-repeat bg-[right_16px_center] pr-12"
                required
              >
                <option value="">Select framework</option>
                <option value="soc2">SOC 2</option>
                <option value="iso27001">ISO 27001</option>
                <option value="hipaa">HIPAA</option>
                <option value="hitrust">HITRUST</option>
                <option value="pci">PCI DSS</option>
                <option value="gdpr">GDPR</option>
                <option value="multiple">Multiple frameworks</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-slate-300">
                Target Timeline
              </label>
              <select
                name="targetTimeline"
                suppressHydrationWarning
                className="px-4 py-3.5 bg-black/30 border border-white/10 rounded-xl font-body text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 cursor-pointer appearance-none bg-[url('data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'20\' height=\'20\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%2394a3b8\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E')] bg-no-repeat bg-[right_16px_center] pr-12"
                required
              >
                <option value="">Select timeline</option>
                <option value="1month">Within 1 month</option>
                <option value="3months">1-3 months</option>
                <option value="6months">3-6 months</option>
                <option value="flexible">Flexible</option>
              </select>
            </div>
          </div>
          <button
            type="submit"
            disabled={isSubmitting}
            suppressHydrationWarning
            className="w-full mt-3 inline-flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3 sm:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] touch-manipulation disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0"
          >
            {isSubmitting ? (
              <>
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Submitting...
              </>
            ) : (
              'Get My Readiness Snapshot'
            )}
          </button>

          {submitStatus === 'success' && (
            <div className="mt-4 p-4 bg-teal-500/10 border border-teal-500/30 rounded-xl text-center">
              <p className="text-sm font-medium text-teal-400">
                ✓ Thank you! We&apos;ll send your Readiness Snapshot within 48 hours.
              </p>
            </div>
          )}

          {submitStatus === 'error' && errorMessage && (
            <div className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-center">
              <p className="text-sm font-medium text-red-400">
                {errorMessage}
              </p>
            </div>
          )}

          <div className="text-center mt-4 sm:mt-5">
            <p className="text-xs text-slate-500">
              No spam. We&apos;ll reach out within one business day.
            </p>
          </div>
        </form>
      </div>
    </section>
  );
}
