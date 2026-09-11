import type { Metadata } from 'next';
import Hero from '@/components/marketing/homepage/Hero';
import Platform from '@/components/marketing/homepage/Platform';
import SocialProof from '@/components/marketing/homepage/SocialProof';
import CustomersSection from '@/components/marketing/homepage/CustomersSection';
import Problem from '@/components/marketing/homepage/Problem';
import Differentiator from '@/components/marketing/homepage/Differentiator';
import Certifications from '@/components/marketing/homepage/Certifications';
import HowItWorks from '@/components/marketing/homepage/HowItWorks';
import Implement from '@/components/marketing/homepage/Implement';
import Packages from '@/components/marketing/homepage/Packages';
import FAQ from '@/components/marketing/homepage/FAQ';
import LeadCapture from '@/components/marketing/homepage/LeadCapture';
import FinalCTA from '@/components/marketing/homepage/FinalCTA';
import FAQSchema from '@/components/marketing/schema/FAQSchema';
import ServiceSchema from '@/components/marketing/schema/ServiceSchema';
import SoftwareApplicationSchema from '@/components/marketing/schema/SoftwareApplicationSchema';
import WebPageSchema from '@/components/marketing/schema/WebPageSchema';
import OrganizationSchema from '@/components/marketing/schema/OrganizationSchema';
import WebSiteSchema from '@/components/marketing/schema/WebSiteSchema';

const howToSchema = JSON.stringify({
  '@context': 'https://schema.org',
  '@type': 'HowTo',
  name: 'How to Get Compliance Certified with QuickTrust',
  description: 'Get audit-ready and certified for SOC 2, ISO 27001, or HIPAA in three steps with QuickTrust platform and implementation engineers.',
  step: [
    {
      '@type': 'HowToStep',
      position: 1,
      name: 'Map & Score',
      text: 'We map every framework and customer questionnaire to your policies and controls, then score your coverage. Deliverables: defined scope, control map, initial gaps.',
    },
    {
      '@type': 'HowToStep',
      position: 2,
      name: 'Fix & Prove',
      text: 'Our security and DevOps engineers close gaps, validate controls, and attach audit-ready evidence. Deliverables: closed gaps, evidence pack, weekly progress reports.',
    },
    {
      '@type': 'HowToStep',
      position: 3,
      name: 'Certify & Maintain',
      text: 'We coordinate with auditors, maintain your evidence portal, and track changes to keep you compliant. Deliverables: auditor-ready portal, ongoing monitoring, change tracking.',
    },
  ],
});

const BASE = 'https://quicktrustapp.com';

export const metadata: Metadata = {
  title: 'Compliance Automation Platform | QuickTrust',
  description:
    'Map frameworks to controls, surface gaps, and get audit-ready with engineers who close them. SOC 2, ISO 27001, HIPAA. Free readiness assessment.',
  alternates: { canonical: BASE },
  openGraph: {
    title: 'Compliance Automation Platform | QuickTrust',
    description:
      'Map frameworks to controls, surface gaps, and get audit-ready with engineers who close them. SOC 2, ISO 27001, HIPAA.',
    url: BASE,
    siteName: 'QuickTrust',
    type: 'website',
    images: [{ url: `${BASE}/og/home`, width: 1200, height: 630, alt: 'QuickTrust Compliance Automation Platform' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Compliance Automation Platform | QuickTrust',
    description: 'Map frameworks to controls, surface gaps, and get audit-ready with engineers who close them.',
    images: [`${BASE}/og/home`],
  },
};

const homepageFAQs = [
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

export default function HomePage() {
  return (
    <div id="main-content" className="font-body bg-slate-950 text-slate-300 overflow-x-hidden">
      <OrganizationSchema />
      <WebSiteSchema />
      <FAQSchema faqs={homepageFAQs} />
      <ServiceSchema />
      <SoftwareApplicationSchema />
      <WebPageSchema
        name="Compliance Automation Platform | QuickTrust"
        description="Map frameworks to controls, surface gaps, and get audit-ready with engineers who close them. SOC 2, ISO 27001, HIPAA. Free readiness assessment."
        url="https://quicktrustapp.com"
      />
      {/* HowTo schema — uses hardcoded static JSON, safe from XSS */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: howToSchema }}
      />
        <Hero />
        <Platform />
        <SocialProof />
        <CustomersSection />
        <Problem />
        <Differentiator />
        <Certifications />
        <HowItWorks />
        <Implement />
        <Packages />
        <FAQ />
        <LeadCapture />
        <FinalCTA />
    </div>
  );
}
