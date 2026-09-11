import ContactForm from "@/components/marketing/homepage/ContactForm";
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Contact Us',
  description:
    'Get in touch with QuickTrust. Schedule a free readiness assessment, request a fixed-price quote, or ask about compliance automation for SOC 2, ISO 27001, HIPAA.',
  alternates: {
    canonical: 'https://quicktrustapp.com/contact',
  },
  openGraph: {
    title: 'Contact QuickTrust',
    description:
      'Schedule a free readiness assessment or request a fixed-price quote for compliance automation.',
    url: 'https://quicktrustapp.com/contact',
    siteName: 'QuickTrust',
    type: 'website',
    images: [
      {
        url: 'https://quicktrustapp.com/og/contact',
        width: 1200,
        height: 630,
        alt: 'Contact QuickTrust',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Contact QuickTrust',
    description:
      'Schedule a free readiness assessment or request a fixed-price quote.',
    images: ['https://quicktrustapp.com/og/contact'],
  },
};

// Breadcrumb schema for this page — uses hardcoded static JSON so the content
// is fully trusted and cannot be influenced by user input.
const breadcrumbSchema = JSON.stringify({
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://quicktrustapp.com' },
    { '@type': 'ListItem', position: 2, name: 'Contact', item: 'https://quicktrustapp.com/contact' },
  ],
});

export default function ContactPage() {
  return (
    <div id="main-content" className="min-h-screen bg-slate-950">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: breadcrumbSchema }}
      />

      {/* Navigation spacer */}
      <div className="h-20" />

      {/* Hero */}
      <section className="relative py-16 sm:py-24 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-transparent to-transparent" />
        <div className="max-w-4xl mx-auto px-4 sm:px-6 relative">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h1 className="font-display text-4xl sm:text-5xl font-bold text-slate-50 mb-4">
              Get in{' '}
              <span className="bg-gradient-to-r from-teal-400 to-teal-500 bg-clip-text text-transparent">
                Touch
              </span>
            </h1>
            <p className="text-lg text-slate-400">
              Whether you are starting your compliance journey or looking to switch platforms,
              we are here to help. Get a free readiness snapshot or request a fixed-price quote.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div>
              <h2 className="font-display text-2xl font-semibold text-slate-100 mb-6">Send Us a Message</h2>
              <ContactForm />
            </div>

            {/* Contact Info */}
            <div className="space-y-8">
              <div>
                <h2 className="font-display text-2xl font-semibold text-slate-100 mb-6">Other Ways to Reach Us</h2>

                <div className="space-y-6">
                  <div>
                    <h3 className="font-medium text-slate-200 mb-1">Email</h3>
                    <a
                      href="mailto:hello@quicktrust.io"
                      className="text-teal-400 hover:text-teal-300 transition-colors"
                    >
                      hello@quicktrust.io
                    </a>
                  </div>

                  <div>
                    <h3 className="font-medium text-slate-200 mb-1">Address</h3>
                    <address className="not-italic text-slate-400">
                      GPT Innovations, Inc.<br />
                      651N Broad Street, Suite 201<br />
                      Middletown, DE 19709<br />
                      United States
                    </address>
                  </div>
                </div>
              </div>

              <div className="rounded-2xl bg-gradient-to-br from-teal-500/10 to-teal-600/5 border border-teal-500/20 p-6">
                <h3 className="font-display font-semibold text-slate-100 mb-2">Free Readiness Snapshot</h3>
                <p className="text-slate-400 text-sm mb-4">
                  Not sure where you stand? Get a complimentary gap assessment.
                  We will map your current security posture against your target framework
                  and give you a clear picture of what it takes to get certified.
                </p>
                <Link
                  href="/login?mode=register"
                  className="inline-flex items-center justify-center px-6 py-2.5 rounded-xl font-display font-semibold text-sm bg-gradient-to-r from-teal-400 to-teal-500 text-slate-950 no-underline hover:-translate-y-0.5 transition-all"
                >
                  Get Your Free Snapshot
                </Link>
              </div>

              <div className="rounded-2xl bg-white/5 border border-white/10 p-6">
                <h3 className="font-display font-semibold text-slate-100 mb-2">Already evaluating platforms?</h3>
                <p className="text-slate-400 text-sm mb-4">
                  See how QuickTrust compares to Vanta, Drata, Secureframe, and others.
                </p>
                <Link
                  href="/blog/quicktrust-vs-vanta"
                  className="text-teal-400 hover:text-teal-300 text-sm no-underline transition-colors"
                >
                  View comparisons &rarr;
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 text-center">
          <Link href="/" className="text-slate-500 hover:text-slate-300 text-sm no-underline transition-colors">
            &larr; Back to QuickTrust
          </Link>
        </div>
      </footer>
    </div>
  );
}
