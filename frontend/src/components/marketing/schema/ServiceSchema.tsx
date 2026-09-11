/**
 * Service Schema (JSON-LD)
 *
 * Place in: app/page.tsx (homepage) -- renders two service offerings
 *
 * Represents QuickTrust's two main service packages:
 * 1. Certification Fast Track (Implementation Included)
 * 2. Continuous Compliance Program (Platform + Engineers)
 *
 * These are derived directly from the Packages section on the homepage.
 */

export default function ServiceSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Service",
        "@id": "https://quicktrustapp.com/#service-fast-track",
        "name": "Certification Fast Track",
        "alternateName": "Certification Fast Track (Implementation Included)",
        "description": "Get certified without derailing product. Platform + security engineers + audit coordination. Includes defined scope and control mapping, complete policy pack, implementation sprints (DevOps + security), evidence library setup, and full audit support.",
        "provider": {
          "@id": "https://quicktrustapp.com/#organization"
        },
        "serviceType": "Compliance Certification",
        "areaServed": {
          "@type": "Country",
          "name": "US"
        },
        "audience": {
          "@type": "Audience",
          "audienceType": "Seed to Series C SaaS, fintech, and healthcare startups"
        },
        "hasOfferCatalog": {
          "@type": "OfferCatalog",
          "name": "Fast Track Features",
          "itemListElement": [
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "SOC 2 Type I & II Certification"
              }
            },
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "ISO 27001 Certification"
              }
            },
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "HIPAA Compliance"
              }
            },
            {
              "@type": "Offer",
              "itemOffered": {
                "@type": "Service",
                "name": "PCI DSS Compliance"
              }
            }
          ]
        }
      },
      {
        "@type": "Service",
        "@id": "https://quicktrustapp.com/#service-continuous",
        "name": "Continuous Compliance Program",
        "alternateName": "Continuous Compliance Program (Platform + Engineers)",
        "description": "Standardize controls across teams. Platform + security engineers + audit coordination. Includes multi-team rollout and governance, control owners and reporting, continuous compliance program, vendor risk management, and exception workflows.",
        "provider": {
          "@id": "https://quicktrustapp.com/#organization"
        },
        "serviceType": "Continuous Compliance Management",
        "areaServed": {
          "@type": "Country",
          "name": "US"
        },
        "audience": {
          "@type": "Audience",
          "audienceType": "Enterprises, regulated orgs, and global teams"
        }
      }
    ]
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
