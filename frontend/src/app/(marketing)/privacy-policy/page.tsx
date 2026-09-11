// LEGAL REVIEW REQUIRED: This is a draft privacy policy. Must be reviewed by legal counsel before final publication.
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description:
    'QuickTrust privacy policy. Learn how we collect, use, and protect your information.',
  alternates: {
    canonical: '/privacy-policy',
  },
  robots: {
    index: false,
    follow: true,
  },
};

export default function PrivacyPolicyPage() {
  return (
    <div className="font-body bg-slate-950 text-slate-300 overflow-x-hidden">

        {/* Header */}
        <section className="relative pt-32 pb-12 sm:pt-40 sm:pb-16 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-transparent to-transparent" />
          <div className="max-w-4xl mx-auto px-4 sm:px-6 relative">
            <h1 className="font-display text-4xl sm:text-5xl font-bold text-slate-50 mb-4">
              Privacy Policy
            </h1>
            <p className="text-slate-500 text-sm">
              Last updated: March 2026
            </p>
            {/* TODO: Founder input needed — confirm effective date */}
          </div>
        </section>

        {/* Content */}
        <section className="pb-24">
          <div className="max-w-4xl mx-auto px-4 sm:px-6">
            <div className="prose prose-invert prose-slate max-w-none">
              {/* Draft Notice */}
              <div className="rounded-2xl border border-amber-500/30 bg-amber-500/5 p-6 mb-12">
                <p className="text-amber-400 text-sm font-medium mb-2">Draft Notice</p>
                <p className="text-slate-400 text-sm leading-relaxed mb-0">
                  This privacy policy is a draft and is pending legal review. It will be updated and
                  finalized before publication. If you have questions, please contact us at{' '}
                  <a href="mailto:hello@quicktrust.io" className="text-teal-400 no-underline hover:text-teal-300">
                    hello@quicktrust.io
                  </a>.
                </p>
              </div>

              {/* Introduction */}
              <div className="mb-12">
                <p className="text-slate-400 leading-relaxed">
                  QuickTrust, operated by GPT Innovations, Inc. (&quot;QuickTrust,&quot;
                  &quot;we,&quot; &quot;us,&quot; or &quot;our&quot;), is committed to protecting
                  your privacy. This Privacy Policy describes how we collect, use, disclose, and
                  safeguard your information when you visit our website at quicktrustapp.com, use our
                  compliance automation platform, or interact with us in any other way.
                </p>
              </div>

              {/* Information We Collect */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  Information We Collect
                </h2>

                <h3 className="font-display text-lg font-semibold text-slate-100 mb-3">
                  Information You Provide
                </h3>
                <p className="text-slate-400 leading-relaxed mb-4">
                  We collect information you voluntarily provide when you:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Create an account or register for the platform',
                    'Request a readiness assessment or consultation',
                    'Submit a contact form, lead form, or booking request',
                    'Subscribe to our newsletter or blog updates',
                    'Communicate with us via email, chat, or phone',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-slate-400 leading-relaxed mb-6">
                  This information may include your name, email address, company name, job title,
                  phone number, and any other details you choose to provide.
                </p>

                <h3 className="font-display text-lg font-semibold text-slate-100 mb-3">
                  Information Collected Automatically
                </h3>
                <p className="text-slate-400 leading-relaxed mb-4">
                  When you access our website or platform, we may automatically collect:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Device and browser information (type, version, operating system)',
                    'IP address and approximate geographic location',
                    'Pages visited, time spent, and navigation patterns',
                    'Referring URLs and search terms',
                    'Cookies and similar tracking technologies',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>

                <h3 className="font-display text-lg font-semibold text-slate-100 mb-3">
                  Information from Third Parties
                </h3>
                <p className="text-slate-400 leading-relaxed">
                  We may receive information about you from third-party sources, such as business
                  partners, marketing partners, and publicly available databases. This may include
                  company information, professional profile data, and other details relevant to our
                  business relationship.
                </p>
              </div>

              {/* How We Use Information */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  How We Use Your Information
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  We use the information we collect to:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Provide, operate, and maintain the QuickTrust platform and services',
                    'Process your requests, assessments, and consultations',
                    'Communicate with you about your account, services, and support inquiries',
                    'Send you marketing communications (with your consent, where required)',
                    'Improve and personalize your experience with our platform',
                    'Analyze usage patterns to enhance our product and services',
                    'Detect, prevent, and address security issues and fraud',
                    'Comply with legal obligations and enforce our terms of service',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Data Security */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  Data Security
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  We implement appropriate technical and organizational measures to protect your
                  personal information against unauthorized access, alteration, disclosure, or
                  destruction. These measures include:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Encryption of data in transit (TLS) and at rest',
                    'Access controls and authentication mechanisms',
                    'Regular security assessments and monitoring',
                    'Employee training on data protection practices',
                    'Incident response procedures',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-slate-400 leading-relaxed">
                  While we strive to use commercially acceptable means to protect your personal
                  information, no method of transmission over the Internet or method of electronic
                  storage is 100% secure. We cannot guarantee absolute security.
                </p>
              </div>

              {/* Third-Party Services */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  Third-Party Services
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  We may use third-party services that collect, monitor, and analyze information to
                  improve our service and functionality. These may include:
                </p>
                {/* TODO: Founder input needed — list actual third-party services/subprocessors */}
                <ul className="space-y-2 mb-6">
                  {[
                    'Analytics providers (to understand how our website and platform are used)',
                    'Cloud infrastructure providers (to host and operate our platform)',
                    'Email service providers (to send transactional and marketing communications)',
                    'Customer support tools (to manage support inquiries)',
                    'Payment processors (to process subscription payments)',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-slate-400 leading-relaxed">
                  These third-party services have their own privacy policies governing how they use
                  your information. We encourage you to review their policies.
                </p>
              </div>

              {/* Your Rights */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  Your Rights
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  Depending on your location and applicable law, you may have the following rights
                  regarding your personal information:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Access: Request a copy of the personal information we hold about you',
                    'Correction: Request that we correct inaccurate or incomplete information',
                    'Deletion: Request that we delete your personal information',
                    'Portability: Request a copy of your data in a structured, machine-readable format',
                    'Objection: Object to the processing of your personal information in certain circumstances',
                    'Withdrawal of Consent: Withdraw your consent at any time where we rely on consent to process your data',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-slate-400 leading-relaxed">
                  To exercise any of these rights, please contact us at{' '}
                  <a href="mailto:hello@quicktrust.io" className="text-teal-400 no-underline hover:text-teal-300">
                    hello@quicktrust.io
                  </a>. We will respond to your request within a reasonable timeframe and in
                  accordance with applicable law.
                </p>
              </div>

              {/* Data Retention */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  Data Retention
                </h2>
                <p className="text-slate-400 leading-relaxed">
                  We retain your personal information for as long as necessary to fulfill the
                  purposes described in this Privacy Policy, unless a longer retention period is
                  required or permitted by law. When we no longer have a legitimate business need to
                  process your personal information, we will delete or anonymize it.
                </p>
              </div>

              {/* Changes to This Policy */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  Changes to This Privacy Policy
                </h2>
                <p className="text-slate-400 leading-relaxed">
                  We may update this Privacy Policy from time to time. We will notify you of any
                  changes by posting the new Privacy Policy on this page and updating the &quot;Last
                  updated&quot; date. We encourage you to review this Privacy Policy periodically for
                  any changes.
                </p>
              </div>

              {/* Contact Us */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  Contact Us
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  If you have questions about this Privacy Policy or our data practices, please
                  contact us:
                </p>
                <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
                  <p className="text-slate-300 font-medium mb-2">GPT Innovations, Inc. (QuickTrust)</p>
                  <p className="text-slate-400 text-sm mb-1">651N Broad Street, Suite 201</p>
                  <p className="text-slate-400 text-sm mb-3">Middletown, Delaware 19709</p>
                  <p className="text-sm">
                    <a href="mailto:hello@quicktrust.io" className="text-teal-400 no-underline hover:text-teal-300">
                      hello@quicktrust.io
                    </a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
    </div>
  );
}
