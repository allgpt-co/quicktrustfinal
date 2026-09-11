/**
 * BreadcrumbList Schema (JSON-LD)
 *
 * Place in: app/blog/[slug]/page.tsx (blog article pages)
 *
 * Generates breadcrumb rich results in Google SERPs:
 *   Home > Resources > Article Title
 *
 * Google Docs: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
 *
 * Props:
 *   articleTitle - the title of the current article
 *   articleSlug  - the URL slug of the current article
 */

interface BreadcrumbSchemaProps {
  articleTitle: string;
  articleSlug: string;
}

export default function BreadcrumbSchema({ articleTitle, articleSlug }: BreadcrumbSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://quicktrustapp.com"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Resources",
        "item": "https://quicktrustapp.com/blog"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": articleTitle,
        "item": `https://quicktrustapp.com/blog/${articleSlug}`
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
