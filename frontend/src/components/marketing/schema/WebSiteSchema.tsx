/**
 * WebSite Schema with SearchAction (JSON-LD)
 *
 * Place in: app/layout.tsx OR homepage only
 *
 * This enables the Sitelinks Search Box in Google SERPs,
 * allowing users to search your site directly from Google results.
 *
 * Google Docs: https://developers.google.com/search/docs/appearance/structured-data/sitelinks-searchbox
 */

export default function WebSiteSchema() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://quicktrustapp.com/#website",
    "name": "QuickTrust",
    "url": "https://quicktrustapp.com",
    "inLanguage": "en-US",
    "description": "Compliance automation platform with implementation engineers. Map frameworks to controls, surface gaps, and get audit-ready.",
    "publisher": {
      "@id": "https://quicktrustapp.com/#organization"
    },
    "potentialAction": {
      "@type": "SearchAction",
      "target": {
        "@type": "EntryPoint",
        "urlTemplate": "https://quicktrustapp.com/blog?q={search_term_string}"
      },
      "query-input": "required name=search_term_string"
    }
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
