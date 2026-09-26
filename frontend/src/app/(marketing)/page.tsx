import type { Metadata } from 'next';
import { homepageFAQs } from '@/lib/homepage-faqs';
import Hero from '@/components/marketing/homepage/Hero';
import Platform from '@/components/marketing/homepage/Platform';
import SocialProof from '@/components/marketing/homepage/SocialProof';
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
import { serializeJsonLd } from '@/components/marketing/schema/jsonLd';

const howToSchema = serializeJsonLd({
  '@context': 'https://schema.org',
  '@type': 'HowTo',
  name: 'How to Prepare for a Compliance Assessment with QuickTrust',
  description: 'Scope requirements, implement controls and prepare evidence with QuickTrust. Audit opinions and certifications are determined independently.',
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
      name: 'Review & Maintain',
      text: 'We coordinate with auditors, maintain your evidence portal, and track changes for review. Deliverables: auditor-ready portal, ongoing monitoring, change tracking.',
    },
  ],
});

const BASE = 'https://quicktrustapp.com';

export const metadata: Metadata = {
  title: 'Compliance Automation Platform',
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
