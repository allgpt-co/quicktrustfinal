/**
 * WebPage Schema (JSON-LD)
 *
 * Place in: any page that needs explicit WebPage markup.
 * Most useful on the homepage to tie Organization + WebSite together.
 *
 * Props:
 *   name       - page title
 *   description - page meta description
 *   url        - canonical URL of the page
 */

interface WebPageSchemaProps {
  name: string;
  description: string;
  url: string;
}

export default function WebPageSchema({ name, description, url }: WebPageSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": `${url}#webpage`,
    "name": name,
    "description": description,
    "url": url,
    "isPartOf": {
      "@id": "https://quicktrustapp.com/#website"
    },
    "about": {
      "@id": "https://quicktrustapp.com/#organization"
    },
    "publisher": {
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
