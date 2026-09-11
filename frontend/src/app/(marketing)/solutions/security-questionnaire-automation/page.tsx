import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Security Questionnaire Automation — Map & Respond Faster',
  description:
    'Automate security questionnaire responses. Map questions to policies, generate consistent answers, maintain audit trails. Free demo.',
  alternates: {
    canonical: '/solutions/security-questionnaire-automation',
  },
  openGraph: {
    title: 'Security Questionnaire Automation — Map & Respond Faster',
    description:
      'Automate security questionnaire responses. Map questions to policies, generate consistent answers, maintain audit trails. Free demo.',
    type: 'website',
    siteName: 'QuickTrust',
    url: 'https://quicktrustapp.com/solutions/security-questionnaire-automation',
  },
};

export default function SecurityQuestionnaireAutomationPage() {
  return (
    <div className="font-body bg-slate-950 text-slate-300 overflow-x-hidden">

        {/* Hero */}
        <section className="relative pt-32 pb-16 sm:pt-40 sm:pb-24 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-transparent to-transparent" />
          <div className="max-w-7xl mx-auto px-4 sm:px-6 relative">
            <div className="max-w-3xl mx-auto text-center">
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-sm font-medium mb-6">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Solutions
              </span>
              <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-50 mb-6 leading-tight">
                Security Questionnaire Automation —{' '}
                <span className="bg-gradient-to-r from-teal-400 to-teal-500 bg-clip-text text-transparent">
                  From Hours to Minutes
                </span>
              </h1>
              <p className="text-lg sm:text-xl text-slate-400 leading-relaxed max-w-2xl mx-auto mb-10">
                Stop spending days on repetitive security questionnaires. Map questions to your
                policies, generate consistent answers, and maintain a complete audit trail — automatically.
              </p>
              <Link
                href="/#lead-form"
                className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-gradient-primary text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] transition-all"
              >
                Automate Your Security Questionnaires — Free Demo
              </Link>
            </div>
          </div>
        </section>

        {/* The Problem */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="max-w-3xl mx-auto text-center mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                The Problem with Security Questionnaires
              </h2>
              <p className="text-slate-400 text-lg leading-relaxed">
                Every enterprise prospect, partner, and customer sends a different security
                questionnaire. Your team is stuck answering the same questions over and over — with
                inconsistent answers, no audit trail, and days of lost productivity.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                {
                  stat: '40+',
                  label: 'hours per month',
                  description: 'Average time security teams spend responding to questionnaires manually',
                },
                {
                  stat: '300+',
                  label: 'questions per form',
                  description: 'Typical enterprise security questionnaire length, with heavy overlap between vendors',
                },
                {
                  stat: '60%',
                  label: 'duplicated effort',
                  description: 'Questions asked repeatedly across different questionnaires with no shared response library',
                },
                {
                  stat: '0',
                  label: 'audit trails',
                  description: 'Most teams use spreadsheets with no version history, approvals, or traceability',
                },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 text-center"
                >
                  <p className="font-display text-3xl font-bold text-teal-400 mb-1">{item.stat}</p>
                  <p className="text-slate-200 text-sm font-medium mb-3">{item.label}</p>
                  <p className="text-slate-500 text-xs leading-relaxed">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How QuickTrust Automates Responses */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                How QuickTrust Automates Responses
              </h2>
              <p className="text-slate-400 text-lg">
                Upload any security questionnaire. Our platform maps each question to your existing
                policies and controls, generates draft responses, and lets your team review and
                approve — all in one workflow.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  step: '01',
                  title: 'Upload the Questionnaire',
                  description:
                    'Drop in any security questionnaire — spreadsheet, PDF, or standard format like SIG, CAIQ, or VSA. Our parser extracts every question and categorizes it by control domain.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                  ),
                },
                {
                  step: '02',
                  title: 'Auto-Map to Policies',
                  description:
                    'Each question is automatically mapped to the relevant policy section, control ID, and evidence artifact. You see exactly which policy answers each question — and where gaps exist.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                  ),
                },
                {
                  step: '03',
                  title: 'Review &amp; Submit',
                  description:
                    'Draft responses are generated from your approved response library. Your team reviews, edits if needed, and exports the completed questionnaire — with full version history and audit trail.',
                  icon: (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  ),
                },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8 hover:border-teal-500/20 transition-all"
                >
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-12 h-12 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center">
                      <svg className="w-6 h-6 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        {item.icon}
                      </svg>
                    </div>
                    <span className="font-display text-sm font-bold text-teal-400 tracking-wider">
                      STEP {item.step}
                    </span>
                  </div>
                  <h3 className="font-display text-xl font-semibold text-slate-50 mb-3">
                    {item.title}
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Question-Policy Mapping */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                  Question-to-Policy Mapping
                </h2>
                <p className="text-slate-400 text-lg leading-relaxed mb-6">
                  Every security questionnaire question is mapped to the specific policy section,
                  control ID, and evidence artifact that answers it. No more guessing which policy
                  applies or copying answers from last time.
                </p>
                <ul className="space-y-4">
                  {[
                    'Questions mapped to SOC 2 trust service criteria, ISO 27001 Annex A controls, HIPAA safeguards',
                    'Direct links to policy language — see the exact paragraph that answers each question',
                    'Gap detection — instantly see which questions have no corresponding policy or control',
                    'Cross-framework mapping — one answer can satisfy questions from multiple frameworks',
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <svg className="w-5 h-5 text-teal-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-slate-300 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8">
                <div className="space-y-4">
                  <div className="rounded-xl bg-white/5 border border-white/10 p-4">
                    <p className="text-xs font-medium text-teal-400 mb-2">QUESTION</p>
                    <p className="text-slate-300 text-sm mb-3">
                      &quot;Do you encrypt data at rest and in transit?&quot;
                    </p>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-teal-500/15 text-teal-400 border border-teal-500/25">
                        SOC 2 CC6.1
                      </span>
                      <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-violet-500/15 text-violet-400 border border-violet-500/25">
                        ISO A.10.1.1
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center justify-center">
                    <svg className="w-5 h-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                    </svg>
                  </div>
                  <div className="rounded-xl bg-teal-500/5 border border-teal-500/20 p-4">
                    <p className="text-xs font-medium text-teal-400 mb-2">MAPPED RESPONSE</p>
                    <p className="text-slate-300 text-sm mb-3">
                      &quot;Yes. All data is encrypted at rest using AES-256 and in transit using
                      TLS 1.2+. See Encryption Policy, Section 3.2.&quot;
                    </p>
                    <p className="text-xs text-slate-500">
                      Source: Encryption Policy v2.1 | Last reviewed: Q1 2026
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Consistent, Auditable Answers */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                Consistent, Auditable Answers
              </h2>
              <p className="text-slate-400 text-lg">
                Every response comes from an approved response library with version history, reviewer
                attribution, and audit trails. No more contradictory answers across different
                questionnaires.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[
                {
                  title: 'Response Library',
                  description:
                    'Build a centralized library of approved answers. When a new questionnaire arrives, responses are pulled from the library — ensuring consistency across every submission.',
                },
                {
                  title: 'Version History',
                  description:
                    'Every response edit is tracked with who made the change, when, and why. Full version history means you can always trace how an answer evolved over time.',
                },
                {
                  title: 'Reviewer Workflows',
                  description:
                    'Assign reviewers to specific control domains. Subject matter experts review and approve answers in their area before questionnaires are submitted.',
                },
                {
                  title: 'Audit Trail',
                  description:
                    'Every questionnaire submission is logged with a complete audit trail — who submitted it, when, which responses were used, and who approved each answer.',
                },
                {
                  title: 'Contradiction Detection',
                  description:
                    'Our platform flags inconsistencies across questionnaire responses. If you answered differently on two questionnaires, you will know about it before your prospect does.',
                },
                {
                  title: 'Evidence Attachment',
                  description:
                    'Attach supporting evidence directly to responses — screenshots, config exports, policy PDFs. Everything the recipient needs is in one package.',
                },
              ].map((feature, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8 hover:border-teal-500/20 transition-all"
                >
                  <h3 className="font-display text-lg font-semibold text-slate-50 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Supported Formats */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-4xl mx-auto px-4 sm:px-6">
            <div className="text-center mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                Supported Questionnaire Formats
              </h2>
              <p className="text-slate-400 text-lg">
                We support the questionnaire formats your prospects and partners actually send.
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { name: 'SIG (Standard Information Gathering)', tag: 'Shared Assessments' },
                { name: 'CAIQ (Consensus Assessments)', tag: 'Cloud Security Alliance' },
                { name: 'VSA (Vendor Security Alliance)', tag: 'VSA' },
                { name: 'Custom Spreadsheets', tag: 'XLSX / CSV' },
                { name: 'PDF Questionnaires', tag: 'PDF' },
                { name: 'Google Forms / Typeform', tag: 'Web Forms' },
              ].map((format, idx) => (
                <div
                  key={idx}
                  className="rounded-xl border border-white/10 bg-white/[0.02] p-5 flex items-center gap-4"
                >
                  <div className="w-10 h-10 rounded-lg bg-teal-500/10 border border-teal-500/20 flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-slate-200 text-sm font-medium">{format.name}</p>
                    <p className="text-slate-500 text-xs">{format.tag}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="py-16 sm:py-24 border-t border-white/5">
          <div className="max-w-3xl mx-auto px-4 sm:px-6">
            <div className="text-center mb-16">
              <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-50 mb-6">
                Security Questionnaire Automation FAQ
              </h2>
            </div>
            <div className="space-y-6">
              {[
                {
                  q: 'How does question-to-policy mapping work?',
                  a: 'When you upload a questionnaire, our platform parses each question and uses natural language matching combined with control framework taxonomy to map it to the most relevant policy section and control ID. You can review and adjust mappings before generating responses.',
                },
                {
                  q: 'Can I use my existing policies and documentation?',
                  a: 'Yes. You upload your existing policies, procedures, and documentation to QuickTrust. Our platform indexes them and uses them as the source for questionnaire responses. The more complete your policy library, the more questions we can auto-answer.',
                },
                {
                  q: 'What if a question has no matching policy?',
                  a: 'Our platform flags unmapped questions as gaps. You can then draft a new response, create the missing policy, or mark the question as not applicable with a justification — all within the platform.',
                },
                {
                  q: 'How long does it take to respond to a questionnaire?',
                  a: 'After your initial response library is built, most questionnaires can be completed in under an hour — compared to days or weeks with manual processes. The first questionnaire takes longer as you build your library, but each subsequent one is significantly faster.',
                },
                {
                  q: 'Does this integrate with our compliance certification work?',
                  a: 'Absolutely. If you are working with QuickTrust on SOC 2, ISO 27001, or HIPAA certification, the policies and controls we implement together automatically populate your questionnaire response library. Certification work and questionnaire responses share the same source of truth.',
                },
                {
                  q: 'Can multiple team members collaborate on responses?',
                  a: 'Yes. You can assign specific control domains to subject matter experts, set up review and approval workflows, and track who contributed to each response. This ensures technical accuracy while maintaining oversight.',
                },
              ].map((faq, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-white/10 bg-white/[0.02] p-6 sm:p-8"
                >
                  <h3 className="font-display text-lg font-semibold text-slate-50 mb-3">
                    {faq.q}
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{faq.a}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 sm:py-24">
          <div className="max-w-4xl mx-auto px-4 sm:px-6">
            <div className="relative rounded-3xl bg-gradient-to-br from-teal-500/10 to-violet-500/10 border border-white/10 p-8 sm:p-12 text-center overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-teal-500/5 to-transparent" />
              <div className="relative">
                <h2 className="font-display text-2xl sm:text-3xl font-bold text-slate-50 mb-4">
                  Stop Spending Days on Security Questionnaires
                </h2>
                <p className="text-slate-400 mb-8 max-w-xl mx-auto">
                  See how QuickTrust maps questions to policies, generates consistent responses, and
                  maintains audit trails — automatically.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link
                    href="/#lead-form"
                    className="inline-flex items-center justify-center px-8 py-4 font-display font-semibold text-base rounded-xl bg-gradient-primary text-slate-950 no-underline shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] transition-all"
                  >
                    Automate Your Security Questionnaires — Free Demo
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Internal Links */}
        <section className="pb-16 sm:pb-24">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <Link href="/soc-2-compliance" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                SOC 2 Compliance
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/hipaa-compliance" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                HIPAA Compliance
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/pricing" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                Pricing
              </Link>
              <span className="text-slate-700">|</span>
              <Link href="/blog/security-questionnaire-response-guide" className="text-slate-500 hover:text-teal-400 no-underline transition-colors">
                Security Questionnaire Response Guide
              </Link>
            </div>
          </div>
        </section>
    </div>
  );
}
