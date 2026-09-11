/**
 * Article Schema (JSON-LD)
 *
 * Place in: app/blog/[slug]/page.tsx (every blog article page)
 *
 * Enables Article rich results in Google Search, including
 * headline, author, date published, and article body preview.
 *
 * Google Docs: https://developers.google.com/search/docs/appearance/structured-data/article
 *
 * Props:
 *   title           - article headline
 *   description     - meta description
 *   slug            - URL slug
 *   author          - author name (defaults to "QuickTrust Editorial")
 *   datePublished   - ISO 8601 date string (e.g. "2026-03-01")
 *   dateModified    - ISO 8601 date string (e.g. "2026-03-15")
 *   keywords        - comma-separated keyword string
 */

interface ArticleSchemaProps {
  title: string;
  description: string;
  slug: string;
  author?: string;
  datePublished?: string;
  dateModified?: string;
  keywords?: string;
}

export default function ArticleSchema({
  title,
  description,
  slug,
  author = "QuickTrust Editorial",
  datePublished,
  dateModified,
  keywords,
}: ArticleSchemaProps) {
  const articleUrl = `https://quicktrustapp.com/blog/${slug}`;

  const schema: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "@id": `${articleUrl}#article`,
    "headline": title,
    "description": description,
    "url": articleUrl,
    "image": {
      "@type": "ImageObject",
      "url": "https://quicktrustapp.com/og/blog",
      "width": 1200,
      "height": 630
    },
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": articleUrl
    },
    "author": {
      "@type": "Organization",
      "@id": "https://quicktrustapp.com/#organization",
      "name": "QuickTrust"
    },
    "publisher": {
      "@type": "Organization",
      "@id": "https://quicktrustapp.com/#organization",
      "name": "QuickTrust",
      "logo": {
        "@type": "ImageObject",
        "url": "https://quicktrustapp.com/marketing-icon.svg"
      }
    },
    "isPartOf": {
      "@id": "https://quicktrustapp.com/#website"
    },
    "inLanguage": "en-US"
  };

  if (datePublished) {
    schema.datePublished = datePublished;
  }
  if (dateModified) {
    schema.dateModified = dateModified;
  }
  if (keywords) {
    schema.keywords = keywords;
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
