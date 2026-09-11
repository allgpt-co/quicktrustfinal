// LEGAL REVIEW REQUIRED: This is a draft. Must be reviewed by legal counsel.
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Terms of Service',
  description:
    'QuickTrust terms of service. Read our terms governing use of the QuickTrust platform.',
  alternates: {
    canonical: '/terms-of-service',
  },
  robots: {
    index: false,
    follow: true,
  },
};

export default function TermsOfServicePage() {
  return (
    <div className="font-body bg-slate-950 text-slate-300 overflow-x-hidden">

        {/* Header */}
        <section className="relative pt-32 pb-12 sm:pt-40 sm:pb-16 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-transparent to-transparent" />
          <div className="max-w-4xl mx-auto px-4 sm:px-6 relative">
            <h1 className="font-display text-4xl sm:text-5xl font-bold text-slate-50 mb-4">
              Terms of Service
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
                  These Terms of Service are a draft and are pending legal review. They will be
                  updated and finalized before publication. If you have questions, please contact us
                  at{' '}
                  <a href="mailto:hello@quicktrust.io" className="text-teal-400 no-underline hover:text-teal-300">
                    hello@quicktrust.io
                  </a>.
                </p>
              </div>

              {/* Acceptance of Terms */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  1. Acceptance of Terms
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  By accessing or using the QuickTrust platform, website (quicktrustapp.com), or any
                  services provided by GPT Innovations, Inc. (&quot;QuickTrust,&quot; &quot;we,&quot;
                  &quot;us,&quot; or &quot;our&quot;), you agree to be bound by these Terms of
                  Service (&quot;Terms&quot;). If you do not agree to these Terms, please do not use
                  our services.
                </p>
                <p className="text-slate-400 leading-relaxed">
                  These Terms apply to all users of the platform, including visitors, registered
                  users, and customers. We reserve the right to update or modify these Terms at any
                  time. Your continued use of the platform after any changes constitutes acceptance
                  of the revised Terms.
                </p>
              </div>

              {/* Description of Service */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  2. Description of Service
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  QuickTrust provides a compliance automation platform combined with implementation
                  engineering services. Our services include, but are not limited to:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Compliance framework mapping and gap analysis (SOC 2, ISO 27001, HIPAA, PCI DSS, and others)',
                    'Automated evidence collection and control monitoring',
                    'Security questionnaire automation and response management',
                    'Policy drafting, review, and management',
                    'Implementation engineering services for cloud infrastructure hardening',
                    'Auditor coordination and evidence preparation',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-slate-400 leading-relaxed">
                  The specific services included in your engagement are defined in your service
                  agreement or subscription plan. We reserve the right to modify, suspend, or
                  discontinue any aspect of the service at any time with reasonable notice.
                </p>
              </div>

              {/* User Accounts */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  3. User Accounts
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  To access certain features of our platform, you must create an account. When
                  creating an account, you agree to:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Provide accurate, current, and complete information during registration',
                    'Maintain and promptly update your account information',
                    'Maintain the security and confidentiality of your login credentials',
                    'Accept responsibility for all activities that occur under your account',
                    'Notify us immediately of any unauthorized use of your account',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-slate-400 leading-relaxed">
                  We reserve the right to suspend or terminate accounts that violate these Terms or
                  that we reasonably believe are being used for unauthorized purposes.
                </p>
              </div>

              {/* Acceptable Use */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  4. Acceptable Use
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  You agree not to use the QuickTrust platform to:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Violate any applicable local, state, national, or international law or regulation',
                    'Infringe upon or violate the intellectual property rights of others',
                    'Upload or transmit viruses, malware, or any other harmful code',
                    'Attempt to gain unauthorized access to our systems or other users\' accounts',
                    'Interfere with or disrupt the integrity or performance of the platform',
                    'Use the platform for any purpose other than its intended compliance and security functions',
                    'Reverse engineer, decompile, or attempt to derive the source code of the platform',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Intellectual Property */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  5. Intellectual Property
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  The QuickTrust platform, including its software, design, text, graphics, logos,
                  icons, and all other content, is the property of GPT Innovations, Inc. and is
                  protected by copyright, trademark, and other intellectual property laws.
                </p>
                <p className="text-slate-400 leading-relaxed mb-4">
                  We grant you a limited, non-exclusive, non-transferable, revocable license to
                  access and use the platform for your internal business purposes in accordance with
                  these Terms and your service agreement.
                </p>
                <p className="text-slate-400 leading-relaxed">
                  You retain ownership of any data, documents, or content you upload to the
                  platform. By uploading content, you grant us a limited license to use, process, and
                  store that content solely for the purpose of providing our services to you.
                </p>
              </div>

              {/* Confidentiality */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  6. Confidentiality
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  We understand that you may share sensitive information with us in the course of our
                  engagement. We treat all customer data as confidential and will not disclose it to
                  third parties except as required to provide our services, as described in our{' '}
                  <Link href="/privacy-policy" className="text-teal-400 no-underline hover:text-teal-300">
                    Privacy Policy
                  </Link>, or as required by law.
                </p>
                <p className="text-slate-400 leading-relaxed">
                  You agree not to disclose any proprietary information about the QuickTrust
                  platform, our methodologies, or our internal processes that you may learn during
                  your use of our services.
                </p>
              </div>

              {/* Payment Terms */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  7. Payment Terms
                </h2>
                {/* TODO: Founder input needed — specific payment terms, refund policy, billing cycles */}
                <p className="text-slate-400 leading-relaxed mb-4">
                  Payment terms, pricing, and billing schedules are defined in your individual
                  service agreement or subscription plan. By subscribing to a paid plan, you agree
                  to pay all applicable fees in accordance with your agreement.
                </p>
                <p className="text-slate-400 leading-relaxed">
                  We reserve the right to modify pricing for future billing periods with reasonable
                  advance notice. Failure to pay outstanding fees may result in suspension or
                  termination of your access to the platform.
                </p>
              </div>

              {/* Limitation of Liability */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  8. Limitation of Liability
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  To the maximum extent permitted by applicable law, QuickTrust and GPT Innovations,
                  Inc. shall not be liable for any indirect, incidental, special, consequential, or
                  punitive damages, including but not limited to loss of profits, data, use,
                  goodwill, or other intangible losses, resulting from:
                </p>
                <ul className="space-y-2 mb-6">
                  {[
                    'Your access to or use of (or inability to access or use) the platform',
                    'Any conduct or content of any third party on the platform',
                    'Any content obtained from the platform',
                    'Unauthorized access, use, or alteration of your transmissions or content',
                    'The outcome of any compliance audit or certification process',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mt-2 flex-shrink-0" />
                      <span className="text-slate-400 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
                <p className="text-slate-400 leading-relaxed">
                  QuickTrust provides compliance automation tools and implementation services. We do
                  not guarantee the outcome of any audit or certification process. Audit outcomes are
                  determined by independent auditors based on their own assessments.
                </p>
              </div>

              {/* Disclaimer */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  9. Disclaimer of Warranties
                </h2>
                <p className="text-slate-400 leading-relaxed">
                  The platform is provided on an &quot;as is&quot; and &quot;as available&quot; basis
                  without warranties of any kind, whether express or implied, including but not
                  limited to implied warranties of merchantability, fitness for a particular purpose,
                  and non-infringement. We do not warrant that the platform will be uninterrupted,
                  secure, or error-free.
                </p>
              </div>

              {/* Termination */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  10. Termination
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  Either party may terminate these Terms at any time in accordance with the terms of
                  the applicable service agreement. We may also suspend or terminate your access to
                  the platform immediately, without prior notice, if we believe you have violated
                  these Terms.
                </p>
                <p className="text-slate-400 leading-relaxed">
                  Upon termination, your right to use the platform will cease immediately. We will
                  make your data available for export for a reasonable period following termination,
                  after which we may delete it in accordance with our data retention policies.
                </p>
              </div>

              {/* Governing Law */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  11. Governing Law
                </h2>
                {/* TODO: Founder input needed — confirm jurisdiction */}
                <p className="text-slate-400 leading-relaxed">
                  These Terms shall be governed by and construed in accordance with the laws of the
                  State of Delaware, without regard to its conflict of law provisions. Any disputes
                  arising under or in connection with these Terms shall be subject to the exclusive
                  jurisdiction of the courts located in the State of Delaware.
                </p>
              </div>

              {/* Severability */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  12. Severability
                </h2>
                <p className="text-slate-400 leading-relaxed">
                  If any provision of these Terms is held to be invalid or unenforceable, the
                  remaining provisions shall continue in full force and effect. The invalid or
                  unenforceable provision will be modified to the minimum extent necessary to make it
                  valid and enforceable.
                </p>
              </div>

              {/* Contact */}
              <div className="mb-12">
                <h2 className="font-display text-2xl font-bold text-slate-50 mb-6">
                  13. Contact
                </h2>
                <p className="text-slate-400 leading-relaxed mb-4">
                  If you have questions about these Terms of Service, please contact us:
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
