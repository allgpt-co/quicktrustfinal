'use client';

import { FormEvent, useEffect, useState, useRef } from 'react';

interface BookingModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function BookingModal({ isOpen, onClose }: BookingModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const formRef = useRef<HTMLFormElement>(null);
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      // Reset form state when modal opens
      setSubmitStatus('idle');
      setErrorMessage('');
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('idle');
    setErrorMessage('');

    const formData = new FormData(e.currentTarget);
    const data = {
      fullName: formData.get('fullName') as string,
      email: formData.get('email') as string,
      phone: formData.get('phone') as string,
      message: formData.get('message') as string,
    };

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      // Check if response is ok before trying to parse JSON
      if (!response.ok) {
        let errorMessage = 'Failed to send message';
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

      // Close modal after 2 seconds
      setTimeout(() => {
        onClose();
        setSubmitStatus('idle');
      }, 2000);
    } catch (error: any) {
      console.error('Error submitting form:', error);
      setSubmitStatus('error');

      // Provide user-friendly error messages
      let userMessage = 'Failed to send message. Please try again.';
      if (error.message) {
        userMessage = error.message;
      } else if (error instanceof TypeError && error.message.includes('fetch')) {
        userMessage = 'Network error. Please check your connection and try again.';
      }

      setErrorMessage(userMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/80 backdrop-blur-md z-[2000] flex items-center justify-center p-4 sm:p-6"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-white/10 rounded-2xl sm:rounded-3xl max-w-lg w-full max-h-[90vh] overflow-y-auto relative animate-modalIn"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 sm:top-5 sm:right-5 w-8 h-8 sm:w-10 sm:h-10 bg-white/5 border-none rounded-lg sm:rounded-xl cursor-pointer flex items-center justify-center transition-all hover:bg-white/10 touch-manipulation"
          aria-label="Close modal"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="w-5 h-5 text-slate-400"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <div className="p-6 sm:p-8 lg:p-12">
          <div className="text-center mb-6 sm:mb-8">
            <div className="w-12 h-12 sm:w-16 sm:h-16 bg-teal-400/10 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-5">
              <svg
                width="34"
                height="25"
                viewBox="0 0 34 25"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="w-6 h-6 sm:w-8 sm:h-8 text-teal-400"
              >
                <path d="M30.5156 0.960938H3.17188C1.42188 0.960938 0 2.38281 0 4.13281V20.9219C0 22.6719 1.42188 24.0938 3.17188 24.0938H30.5156C32.2656 24.0938 33.6875 22.6719 33.6875 20.9219V4.13281C33.6875 2.38281 32.2656 0.960938 30.5156 0.960938ZM30.5156 2.875C30.7891 2.875 31.0078 2.92969 31.2266 3.09375L17.6094 11.3516C17.1172 11.625 16.5703 11.625 16.0781 11.3516L2.46094 3.09375C2.67969 2.98438 2.89844 2.875 3.17188 2.875H30.5156ZM30.5156 22.125H3.17188C2.51562 22.125 1.91406 21.5781 1.91406 20.8672V5.00781L15.0391 12.9922C15.5859 13.3203 16.1875 13.4844 16.7891 13.4844C17.3906 13.4844 17.9922 13.3203 18.5391 12.9922L31.6641 5.00781V20.8672C31.7734 21.5781 31.1719 22.125 30.5156 22.125Z" />
              </svg>
            </div>
            <h3 className="font-display text-xl sm:text-2xl font-bold text-slate-50 mb-2">
              Contact Us
            </h3>
            <p className="text-xs sm:text-sm text-slate-400">
              Let&apos;s talk about your compliance needs
            </p>
          </div>
          <form ref={formRef} onSubmit={handleSubmit} suppressHydrationWarning className="flex flex-col gap-3 sm:gap-4">
            <div className="flex flex-col gap-2">
              <label className="text-xs sm:text-sm font-medium text-slate-300">
                Full Name*
              </label>
              <input
                type="text"
                name="fullName"
                suppressHydrationWarning
                className="px-4 py-3 sm:py-3.5 bg-black/30 border border-white/10 rounded-lg sm:rounded-xl font-body text-sm sm:text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 placeholder:text-slate-600"
                placeholder="Adam Gelius"
                required
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs sm:text-sm font-medium text-slate-300">
                Email*
              </label>
              <input
                type="email"
                name="email"
                suppressHydrationWarning
                className="px-4 py-3 sm:py-3.5 bg-black/30 border border-white/10 rounded-lg sm:rounded-xl font-body text-sm sm:text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 placeholder:text-slate-600"
                placeholder="example@quicktrust.io"
                required
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs sm:text-sm font-medium text-slate-300">
                Phone*
              </label>
              <input
                type="text"
                name="phone"
                suppressHydrationWarning
                className="px-4 py-3 sm:py-3.5 bg-black/30 border border-white/10 rounded-lg sm:rounded-xl font-body text-sm sm:text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 placeholder:text-slate-600"
                placeholder="+1 234 567 8900"
                required
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs sm:text-sm font-medium text-slate-300">
                Message*
              </label>
              <textarea
                name="message"
                rows={4}
                suppressHydrationWarning
                className="px-4 py-3 sm:py-3.5 bg-black/30 border border-white/10 rounded-lg sm:rounded-xl font-body text-sm sm:text-base text-slate-200 transition-all focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/10 placeholder:text-slate-600 resize-none"
                placeholder="Type your message here"
                required
              ></textarea>
            </div>
            {submitStatus === 'success' && (
              <div className="w-full mt-2 p-4 bg-teal-400/10 border border-teal-400/30 rounded-xl text-center">
                <p className="text-sm font-medium text-teal-400">
                  ✓ Thank you! We&apos;ll be in touch soon.
                </p>
              </div>
            )}
            {submitStatus === 'error' && (
              <div className="w-full mt-2 p-4 bg-red-400/10 border border-red-400/30 rounded-xl text-center">
                <p className="text-sm font-medium text-red-400">
                  {errorMessage || 'Failed to send message. Please try again.'}
                </p>
              </div>
            )}
            <button
              type="submit"
              disabled={isSubmitting}
              suppressHydrationWarning
              className="w-full mt-2 inline-flex items-center justify-center gap-2.5 px-6 sm:px-8 py-3 sm:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] touch-manipulation disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0"
            >
              {isSubmitting ? (
                <>
                  <svg
                    className="animate-spin h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Sending...
                </>
              ) : (
                'Send'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
