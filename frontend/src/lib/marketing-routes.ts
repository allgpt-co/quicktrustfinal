import legacyContentRedirects from './marketing-content-redirects.json';

export const MARKETING_PATHS = [
  "/", "/blog", "/about", "/contact", "/pricing", "/privacy-policy", "/terms-of-service",
  "/soc-2-compliance", "/iso-27001-certification", "/hipaa-compliance",
  "/compare/quicktrust-vs-vanta", "/compare/quicktrust-vs-drata",
  "/solutions/security-questionnaire-automation",
] as const;

export const PUBLIC_ASSETS = [
  "/sitemap.xml", "/robots.txt", "/llms.txt", "/site.webmanifest", "/marketing-icon.svg",
] as const;

export const ARTICLE_REDIRECTS: Record<string, string> = {
  "quicktrust-vs-vanta": "/compare/quicktrust-vs-vanta",
  "quicktrust-vs-drata": "/compare/quicktrust-vs-drata",
};

// Exact, reviewed aliases only. Never expose arbitrary content or app prefixes.
export const CONTENT_REDIRECTS: Readonly<Record<string, string>> = {
  ...legacyContentRedirects,
  ...Object.fromEntries(Object.entries(ARTICLE_REDIRECTS).map(([slug, target]) => [`/blog/${slug}`, target])),
};

export const RESOURCE_SLUGS = [
  'soc2-readiness-scorecard', 'iso27001-gap-assessment-checklist',
  'hipaa-risk-assessment-template', 'audit-evidence-checklist',
  '15-security-policy-templates',
] as const;

export function isResourceSlug(slug: string): boolean {
  return RESOURCE_SLUGS.some((resource) => resource === slug);
}

export function canonicalMarketingHref(href: string | undefined, articlePath = '/'): string | undefined {
  if (!href || href.startsWith('#')) return href;
  try {
    const url = new URL(href, `https://quicktrustapp.com${articlePath}`);
    if (!['https:', 'http:'].includes(url.protocol) || ![
      'quicktrustapp.com', 'www.quicktrustapp.com', 'quicktrust.ai', 'www.quicktrust.ai',
    ].includes(url.hostname)) return href;
    const target = CONTENT_REDIRECTS[url.pathname];
    return target ? `${target}${url.search}${url.hash}` : href;
  } catch {
    return href;
  }
}

export function isMarketingPath(pathname: string): boolean {
  return MARKETING_PATHS.some((path) => path === pathname) || pathname.startsWith('/blog/')
    || RESOURCE_SLUGS.some((slug) => pathname === `/resources/${slug}`);
}
