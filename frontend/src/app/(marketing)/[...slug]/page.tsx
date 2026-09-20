import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import SEOPageShell from '@/components/marketing/SEOPageShell';
import ReadinessAssessment from '@/components/marketing/ReadinessAssessment';
import ComplianceRoiCalculator from '@/components/marketing/ComplianceRoiCalculator';
import { serializeJsonLd } from '@/components/marketing/schema/jsonLd';

const BASE = 'https://quicktrustapp.com';

const pageTitles: Record<string, [string, string]> = {
  'hitrust-certification': ['HITRUST Certification Support for Growing Teams', 'Map healthcare security requirements to policies, controls, and evidence with implementation support.'],
  'pci-dss-compliance': ['PCI DSS Compliance Support for SaaS and Payment Teams', 'Reduce PCI DSS scope, document controls, and prepare evidence with technical implementation support.'],
  'gdpr-compliance': ['GDPR Compliance Support for Modern SaaS', 'Turn data inventories, privacy policies, access controls, and processor reviews into an operating program.'],
  'iso-42001-ai-governance': ['ISO 42001 AI Governance Implementation Support', 'Connect AI risks, policies, controls, owners, and evidence in a practical management system.'],
  'compare/quicktrust-vs-secureframe': ['QuickTrust vs Secureframe: Compliance Platform Comparison', 'Compare software-led workflows with QuickTrust’s platform plus implementation-engineer model.'],
  'compare/quicktrust-vs-sprinto': ['QuickTrust vs Sprinto: Compliance Platform Comparison', 'Compare compliance automation software with hands-on engineering implementation.'],
  'compare/quicktrust-vs-thoropass': ['QuickTrust vs Thoropass: Compliance Platform Comparison', 'Compare QuickTrust’s implementation-led approach with Thoropass’s compliance workflow.'],
  'solutions/evidence-collection-automation': ['Evidence Collection Automation with Implementation Support', 'Organize control evidence around owners, systems, cadence, and audit scope.'],
  'solutions/policy-gap-analysis': ['Policy Gap Analysis for Audit-Ready Programs', 'Compare framework requirements with policy language and implemented controls.'],
  'solutions/continuous-compliance-monitoring': ['Continuous Compliance Monitoring for SaaS Teams', 'Monitor control changes, evidence freshness, and implementation drift between audits.'],
  'resources/case-studies': ['QuickTrust Case Studies', 'Review documented implementation patterns with clear disclosure for composite or anonymized examples.'],
  'resources/guides': ['Compliance Guides and Playbooks', 'Read practical guides on SOC 2, ISO 27001, HIPAA, PCI DSS, and continuous compliance.'],
  'resources/templates': ['Compliance Templates and Checklists', 'Use public checklists and worksheets to organize readiness work.'],
  'resources/webinars': ['QuickTrust Webinars and Briefings', 'Access practical briefings on audit readiness, evidence operations, and implementation.'],
  'use-cases/startups': ['Compliance for Startups Preparing for Enterprise Sales', 'Build a focused compliance program around the controls enterprise buyers ask for.'],
  'use-cases/fintech': ['Compliance Operations for Fintech Teams', 'Coordinate security, privacy, payment, and vendor controls across a financial product.'],
  'use-cases/healthcare-saas': ['Compliance for Healthcare SaaS Companies', 'Connect HIPAA, SOC 2, and healthcare customer requirements to evidence and implementation.'],
  'use-cases/enterprise': ['Continuous Compliance for Enterprise Teams', 'Standardize control ownership, evidence, and exception workflows across teams.'],
  integrations: ['QuickTrust Integrations and Evidence Workflows', 'Connect cloud, identity, development, and collaboration systems to controls and evidence.'],
  'company/team': ['The QuickTrust Team', 'Connect compliance architecture, security engineering, DevOps, and evidence operations.'],
  'company/careers': ['Careers at QuickTrust', 'Help build practical compliance systems that make security and engineering easier to operate.'],
  'company/partners': ['QuickTrust Partners', 'Coordinate with auditors, technology providers, and implementation partners.'],
  'trust-center': ['QuickTrust Trust Center', 'Find current security, privacy, and trust documentation available for evaluation.'],
  'tools/soc-2-readiness-assessment': ['SOC 2 Readiness Assessment', 'Score eight control domains and identify the work to prioritize first.'],
  'tools/compliance-roi-calculator': ['Compliance ROI Calculator', 'Build a transparent first-year business case from your own assumptions.'],
};

function key(slug: string[]) { return slug.join('/'); }
function configFor(path: string) { return pageTitles[path]; }

export async function generateMetadata({ params }: { params: Promise<{ slug: string[] }> }): Promise<Metadata> {
  const { slug } = await params;
  const path = key(slug);
  const config = configFor(path);
  if (!config) return { title: 'Page Not Found', robots: { index: false, follow: false } };
  return {
    title: config[0], description: config[1], alternates: { canonical: `${BASE}/${path}` },
    openGraph: { title: config[0], description: config[1], url: `${BASE}/${path}`, siteName: 'QuickTrust', type: 'website', images: [{ url: `${BASE}/og/${slug.at(-1)}`, width: 1200, height: 630, alt: config[0] }] },
    twitter: { card: 'summary_large_image', title: config[0], description: config[1], images: [`${BASE}/og/${slug.at(-1)}`] },
  };
}

export default async function PlannedMarketingPage({ params }: { params: Promise<{ slug: string[] }> }) {
  const { slug } = await params;
  const path = key(slug);
  const config = configFor(path);
  if (!config) notFound();
  const tool = path === 'tools/soc-2-readiness-assessment' ? 'readiness' : path === 'tools/compliance-roi-calculator' ? 'roi' : null;
  const bullets = [
    'Map requirements to control owners, implementation work, and reviewable evidence.',
    'Keep policies, infrastructure, and evidence aligned as your environment changes.',
    'Use a focused readiness plan instead of relying on unsupported guarantees or placeholder claims.',
  ];
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: serializeJsonLd({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Home', item: BASE }, { '@type': 'ListItem', position: 2, name: config[0], item: `${BASE}/${path}` }] }) }} />
      <SEOPageShell eyebrow={tool ? 'Free tool' : 'QuickTrust'} title={config[0]} description={config[1]} bullets={bullets}>
        {tool === 'readiness' && <ReadinessAssessment />}
        {tool === 'roi' && <ComplianceRoiCalculator />}
        {!tool && <div className="mx-auto max-w-4xl px-4 text-center sm:px-6"><p className="text-slate-400">Use the readiness workflow to map this topic to your organization’s controls, evidence, and next implementation steps.</p><Link href="/#lead-form" className="mt-6 inline-flex text-teal-400 no-underline hover:text-teal-300">Talk to a readiness specialist →</Link></div>}
      </SEOPageShell>
    </>
  );
}
