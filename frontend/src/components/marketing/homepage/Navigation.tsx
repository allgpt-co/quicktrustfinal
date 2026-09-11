'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useModal } from './ModalProvider';

export default function Navigation() {
  const { openModal } = useModal();
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    // Set initial scroll state
    handleScroll();
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [mobileMenuOpen]);

  return (
    <>
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-[9999] focus:px-4 focus:py-2 focus:bg-teal-500 focus:text-slate-950 focus:rounded-lg focus:font-semibold"
      >
        Skip to main content
      </a>
      <nav
        className={`fixed top-0 left-0 right-0 z-[1000] py-3 sm:py-5 transition-all ${
          mounted && scrolled
            ? 'bg-slate-950/90 backdrop-blur-xl border-b border-white/5 py-2 sm:py-4'
            : ''
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2 sm:gap-3 no-underline">
              <div className="w-9 h-9 sm:w-11 sm:h-11 bg-gradient-primary rounded-xl relative flex items-center justify-center">
                <div className="absolute w-4 h-4 sm:w-5 sm:h-5 border-[3px] border-slate-950 rounded-full"></div>
                <div className="absolute w-1.5 h-1.5 sm:w-2 sm:h-2 bg-slate-950 rounded-full"></div>
              </div>
              <span className="font-display text-xl sm:text-2xl font-bold text-slate-50">
                QuickTrust
              </span>
            </Link>
            <ul className="hidden md:flex items-center gap-4 lg:gap-8 list-none m-0 p-0">
              <li className="relative group">
                <span className="text-slate-400 font-medium text-[0.95rem] transition-colors hover:text-slate-50 cursor-pointer">
                  Frameworks
                </span>
                <div className="absolute top-full left-0 pt-2 hidden group-hover:block z-50">
                  <div className="bg-slate-900 border border-white/10 rounded-xl p-2 min-w-[200px] shadow-xl">
                    <Link href="/soc-2-compliance" className="block px-4 py-2.5 text-sm text-slate-300 no-underline rounded-lg hover:bg-white/5 hover:text-teal-400 transition-colors">SOC 2 Compliance</Link>
                    <Link href="/iso-27001-certification" className="block px-4 py-2.5 text-sm text-slate-300 no-underline rounded-lg hover:bg-white/5 hover:text-teal-400 transition-colors">ISO 27001 Certification</Link>
                    <Link href="/hipaa-compliance" className="block px-4 py-2.5 text-sm text-slate-300 no-underline rounded-lg hover:bg-white/5 hover:text-teal-400 transition-colors">HIPAA Compliance</Link>
                  </div>
                </div>
              </li>
              <li className="relative group">
                <span className="text-slate-400 font-medium text-[0.95rem] transition-colors hover:text-slate-50 cursor-pointer">
                  Compare
                </span>
                <div className="absolute top-full left-0 pt-2 hidden group-hover:block z-50">
                  <div className="bg-slate-900 border border-white/10 rounded-xl p-2 min-w-[220px] shadow-xl">
                    <Link href="/compare/quicktrust-vs-vanta" className="block px-4 py-2.5 text-sm text-slate-300 no-underline rounded-lg hover:bg-white/5 hover:text-teal-400 transition-colors">QuickTrust vs Vanta</Link>
                    <Link href="/compare/quicktrust-vs-drata" className="block px-4 py-2.5 text-sm text-slate-300 no-underline rounded-lg hover:bg-white/5 hover:text-teal-400 transition-colors">QuickTrust vs Drata</Link>
                  </div>
                </div>
              </li>
              <li>
                <Link
                  href="/solutions/security-questionnaire-automation"
                  className="text-slate-400 no-underline font-medium text-[0.95rem] transition-colors hover:text-slate-50 relative group"
                >
                  Solutions
                  <span className="absolute bottom-[-4px] left-0 w-0 h-0.5 bg-teal-400 transition-all group-hover:w-full"></span>
                </Link>
              </li>
              <li>
                <Link
                  href="/pricing"
                  className="text-slate-400 no-underline font-medium text-[0.95rem] transition-colors hover:text-slate-50 relative group"
                >
                  Pricing
                  <span className="absolute bottom-[-4px] left-0 w-0 h-0.5 bg-teal-400 transition-all group-hover:w-full"></span>
                </Link>
              </li>
              <li>
                <Link
                  href="/blog"
                  className="text-slate-400 no-underline font-medium text-[0.95rem] transition-colors hover:text-slate-50 relative group"
                >
                  Resources
                  <span className="absolute bottom-[-4px] left-0 w-0 h-0.5 bg-teal-400 transition-all group-hover:w-full"></span>
                </Link>
              </li>
            </ul>
            <div className="flex items-center gap-2 sm:gap-3">
              <Link
                href="/login"
                className="hidden md:inline-flex items-center justify-center gap-2.5 px-6 lg:px-8 py-3 lg:py-4 font-display text-sm lg:text-base font-semibold no-underline rounded-xl transition-all bg-white/5 text-slate-200 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-white/20 hover:-translate-y-0.5"
              >
                Sign In
              </Link>
              <Link
                href="/login?mode=register"
                className="inline-flex items-center justify-center gap-2 px-4 sm:px-6 lg:px-8 py-2.5 sm:py-3 lg:py-4 font-display text-sm sm:text-base font-semibold no-underline rounded-xl transition-all bg-gradient-primary text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] relative overflow-hidden"
              >
                <span className="relative z-10 hidden sm:inline">Get Started</span>
                <span className="relative z-10 sm:hidden">Start</span>
                <span className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity"></span>
              </Link>
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden flex flex-col gap-1.5 bg-transparent border-none cursor-pointer p-2 touch-manipulation"
                aria-label="Toggle menu"
                suppressHydrationWarning
              >
                <span className={`w-6 h-0.5 bg-slate-300 rounded-sm transition-all ${mobileMenuOpen ? 'rotate-45 translate-y-2' : ''}`}></span>
                <span className={`w-6 h-0.5 bg-slate-300 rounded-sm transition-all ${mobileMenuOpen ? 'opacity-0' : ''}`}></span>
                <span className={`w-6 h-0.5 bg-slate-300 rounded-sm transition-all ${mobileMenuOpen ? '-rotate-45 -translate-y-2' : ''}`}></span>
              </button>
            </div>
          </div>
        </div>
      </nav>
      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 top-[60px] md:hidden z-[999] bg-slate-950/95 backdrop-blur-xl">
          <div className="flex flex-col px-6 py-8 space-y-4">
            <p className="text-xs uppercase tracking-wider text-slate-600 font-semibold">Frameworks</p>
            <Link href="/soc-2-compliance" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-base py-2 transition-colors hover:text-teal-400 pl-2">SOC 2 Compliance</Link>
            <Link href="/iso-27001-certification" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-base py-2 transition-colors hover:text-teal-400 pl-2">ISO 27001 Certification</Link>
            <Link href="/hipaa-compliance" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-base py-2 border-b border-white/10 transition-colors hover:text-teal-400 pl-2">HIPAA Compliance</Link>
            <p className="text-xs uppercase tracking-wider text-slate-600 font-semibold pt-2">Compare</p>
            <Link href="/compare/quicktrust-vs-vanta" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-base py-2 transition-colors hover:text-teal-400 pl-2">vs Vanta</Link>
            <Link href="/compare/quicktrust-vs-drata" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-base py-2 border-b border-white/10 transition-colors hover:text-teal-400 pl-2">vs Drata</Link>
            <Link href="/solutions/security-questionnaire-automation" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-lg py-3 border-b border-white/10 transition-colors hover:text-teal-400">Solutions</Link>
            <Link href="/pricing" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-lg py-3 border-b border-white/10 transition-colors hover:text-teal-400">Pricing</Link>
            <Link href="/blog" onClick={() => setMobileMenuOpen(false)} className="text-slate-300 no-underline font-medium text-lg py-3 border-b border-white/10 transition-colors hover:text-teal-400">Resources</Link>
            <Link
              href="/login"
              onClick={() => setMobileMenuOpen(false)}
              className="inline-flex items-center justify-center gap-2.5 px-8 py-4 font-display text-base font-semibold no-underline rounded-xl transition-all bg-white/5 text-slate-200 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-white/20 mt-4"
            >
              Sign In
            </Link>
          </div>
        </div>
      )}
    </>
  );
}
