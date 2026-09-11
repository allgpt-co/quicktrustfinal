/**
 * SoftwareApplication Schema (JSON-LD)
 *
 * Place in: app/page.tsx (homepage)
 *
 * Describes the QuickTrust platform as a software application.
 * This schema type helps Google understand your product as a
 * software tool and can surface it in relevant searches.
 *
 * Google Docs: https://developers.google.com/search/docs/appearance/structured-data/software-app
 */

export default function SoftwareApplicationSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "@id": "https://quicktrustapp.com/#software",
    "name": "QuickTrust Compliance Platform",
    "description": "Compliance intelligence platform that maps every framework and customer security question to your policies and controls, surfaces gaps, and provides engineers to close them.",
    "url": "https://quicktrustapp.com",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": {
      "@type": "AggregateOffer",
      "priceCurrency": "USD",
      "offerCount": 2,
      "description": "Certification Fast Track and Continuous Compliance Program. Free Readiness Snapshot available."
    },
    "featureList": [
      "Questionnaire to Policy Mapping",
      "Policy Gap Detection",
      "Remediation Workbench",
      "Evidence Library Setup",
      "SOC 2 Compliance Automation",
      "ISO 27001 Compliance Automation",
      "HIPAA Compliance Automation",
      "PCI DSS Compliance Automation",
      "Vendor Risk Management",
      "Continuous Compliance Monitoring"
    ],
    "author": {
      "@id": "https://quicktrustapp.com/#organization"
    }
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
