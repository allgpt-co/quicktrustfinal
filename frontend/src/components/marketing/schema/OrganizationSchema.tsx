/**
 * Organization Schema (JSON-LD)
 *
 * Place in: app/layout.tsx (renders on every page)
 *
 * This provides Google with core business identity information
 * that can populate Knowledge Panels and enhance search results.
 *
 * Google Docs: https://developers.google.com/search/docs/appearance/structured-data/organization
 */

export default function OrganizationSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://quicktrustapp.com/#organization",
    "name": "QuickTrust",
    "legalName": "GPT Innovations, Inc.",
    "url": "https://quicktrustapp.com",
    "logo": {
      "@type": "ImageObject",
      "url": "https://quicktrustapp.com/marketing-icon.svg",
      "width": 600,
      "height": 60
    },
    "description": "Compliance automation platform with implementation engineers. Map frameworks to controls, surface gaps, and get audit-ready with engineers who close them.",
    "foundingDate": "2025",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "651N Broad Street, Suite 201",
      "addressLocality": "Middletown",
      "addressRegion": "DE",
      "postalCode": "19709",
      "addressCountry": "US"
    },
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+1-234-567-890",
      "email": "hello@quicktrust.io",
      "contactType": "sales"
    },
    "sameAs": [
      "https://www.linkedin.com/company/quicktrust",
      "https://twitter.com/quicktrust",
      "https://github.com/rahuliitk/quicktrust"
    ],
    "knowsAbout": [
      "SOC 2 Compliance",
      "ISO 27001 Certification",
      "HIPAA Compliance",
      "PCI DSS Compliance",
      "HITRUST Certification",
      "GDPR Compliance",
      "Security Audit",
      "DevSecOps"
    ]
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
