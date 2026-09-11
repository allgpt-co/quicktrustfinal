import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-white/5 py-12 sm:py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-10">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 sm:gap-3 no-underline mb-4">
              <div className="w-9 h-9 sm:w-11 sm:h-11 bg-gradient-primary rounded-xl relative flex items-center justify-center">
                <div className="absolute w-4 h-4 sm:w-5 sm:h-5 border-[3px] border-slate-950 rounded-full"></div>
                <div className="absolute w-1.5 h-1.5 sm:w-2 sm:h-2 bg-slate-950 rounded-full"></div>
              </div>
              <span className="font-display text-xl sm:text-2xl font-bold text-slate-50">
                QuickTrust
              </span>
            </Link>
            <p className="text-xs sm:text-sm text-slate-500 mb-4">
              Compliance + DevOps combined. Get audit-ready faster with engineers
              who implement, not just advise.
            </p>
            <div className="text-xs text-slate-500">
              <p className="mb-1"><strong className="text-slate-400">GPT Innovations, Inc.</strong></p>
              <p className="mb-1">651N Broad Street, Suite 201</p>
              <p>Middletown, Delaware 19709</p>
            </div>
          </div>

          {/* Frameworks */}
          <div>
            <h4 className="font-display text-sm font-semibold text-slate-300 mb-4">Frameworks</h4>
            <ul className="list-none p-0 m-0 space-y-2.5">
              <li><Link href="/soc-2-compliance" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">SOC 2</Link></li>
              <li><Link href="/iso-27001-certification" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">ISO 27001</Link></li>
              <li><Link href="/hipaa-compliance" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">HIPAA</Link></li>
            </ul>
          </div>

          {/* Compare */}
          <div>
            <h4 className="font-display text-sm font-semibold text-slate-300 mb-4">Compare</h4>
            <ul className="list-none p-0 m-0 space-y-2.5">
              <li><Link href="/compare/quicktrust-vs-vanta" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">vs Vanta</Link></li>
              <li><Link href="/compare/quicktrust-vs-drata" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">vs Drata</Link></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-display text-sm font-semibold text-slate-300 mb-4">Company</h4>
            <ul className="list-none p-0 m-0 space-y-2.5">
              <li><Link href="/about" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">About</Link></li>
              <li><Link href="/pricing" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">Pricing</Link></li>
              <li><Link href="/blog" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">Blog</Link></li>
              <li><Link href="/contact" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">Contact</Link></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-display text-sm font-semibold text-slate-300 mb-4">Legal</h4>
            <ul className="list-none p-0 m-0 space-y-2.5">
              <li><Link href="/privacy-policy" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">Privacy Policy</Link></li>
              <li><Link href="/terms-of-service" className="text-sm text-slate-500 no-underline hover:text-teal-400 transition-colors">Terms of Service</Link></li>
            </ul>
          </div>
        </div>

        <div className="pt-6 sm:pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 sm:gap-5">
          <p className="text-[10px] sm:text-xs text-slate-600 text-center md:text-left">
            &copy; {new Date().getFullYear()} GPT Innovations, Inc. All rights reserved.
          </p>
          <div className="flex gap-3 sm:gap-4">
            {[
              {
                name: 'LinkedIn',
                href: 'https://linkedin.com/company/quicktrust',
                icon: (
                  <>
                    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                    <rect x="2" y="9" width="4" height="12"></rect>
                    <circle cx="4" cy="4" r="2"></circle>
                  </>
                ),
              },
              {
                name: 'Twitter',
                href: 'https://twitter.com/quicktrust',
                icon: (
                  <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
                ),
              },
              {
                name: 'GitHub',
                href: 'https://github.com/quicktrust',
                icon: (
                  <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
                ),
              },
            ].map((social, idx) => (
              <a
                key={idx}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                className="w-9 h-9 sm:w-10 sm:h-10 bg-white/5 rounded-lg sm:rounded-xl flex items-center justify-center transition-all hover:bg-teal-400/15 touch-manipulation"
                aria-label={social.name}
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="w-4 h-4 sm:w-5 sm:h-5 text-slate-400 hover:text-teal-400 transition-colors"
                >
                  {social.icon}
                </svg>
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
