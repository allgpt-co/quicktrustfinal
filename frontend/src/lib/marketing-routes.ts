import legacyContentRedirects from './marketing-content-redirects.json';
import articleConsolidations from './article-consolidations.json';
import { DEMO_BOOKING_URL } from './marketing-booking';

export const MARKETING_PATHS = [
  "/", "/blog", "/about", "/contact", "/pricing", "/privacy-policy", "/terms-of-service",
  "/hitrust-certification", "/pci-dss-compliance", "/gdpr-compliance", "/iso-42001-ai-governance",
  "/compare/quicktrust-vs-secureframe", "/compare/quicktrust-vs-sprinto", "/compare/quicktrust-vs-thoropass",
  "/solutions/evidence-collection-automation", "/solutions/policy-gap-analysis", "/solutions/continuous-compliance-monitoring",
  "/resources/case-studies", "/resources/guides", "/resources/templates", "/resources/webinars",
  "/use-cases/startups", "/use-cases/fintech", "/use-cases/healthcare-saas", "/use-cases/enterprise",
  "/integrations", "/company/team", "/company/careers", "/company/partners", "/trust-center",
  "/tools/soc-2-readiness-assessment", "/tools/compliance-roi-calculator",
  "/soc-2-compliance", "/iso-27001-certification", "/hipaa-compliance",
  "/compare/quicktrust-vs-vanta", "/compare/quicktrust-vs-drata",
  "/solutions/security-questionnaire-automation",
] as const;

export const PUBLIC_ASSETS = [
  "/sitemap.xml", "/robots.txt", "/llms.txt", "/site.webmanifest", "/marketing-icon.svg",
] as const;

// Consolidated article pairs (2026-10-02): each source slug was a second article on
// the same target keyword. Google alternated between the pair and dropped one from the
// index after the July 2026 outage, so the losing slug now redirects permanently to the
// URL Google preferred before the outage. The source Markdown stays in the repository for
// editorial merging; it is never listed, rendered or included in the sitemap.
export const CONSOLIDATED_ARTICLES: Readonly<Record<string, string>> = articleConsolidations;

export const ARTICLE_REDIRECTS: Record<string, string> = {
  "quicktrust-vs-vanta": "/compare/quicktrust-vs-vanta",
  "quicktrust-vs-drata": "/compare/quicktrust-vs-drata",
  ...Object.fromEntries(Object.entries(CONSOLIDATED_ARTICLES).map(([source, target]) => [source, `/blog/${target}`])),
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
    if (url.pathname === '/demo' || url.pathname === '/demo/') return DEMO_BOOKING_URL;
    const target = CONTENT_REDIRECTS[url.pathname];
    return target ? `${target}${url.search}${url.hash}` : href;
  } catch {
    return href;
  }
}

// Top-level segments of the authenticated application. Middleware redirects these to
// login; everything else that is not public falls through to the router's 404 so a typo
// or removed marketing URL is a real not-found response instead of a login redirect.
export const PROTECTED_APP_PREFIXES = [
  "/access-reviews", "/agents", "/audit-log", "/auditor-marketplace", "/audits", "/control-exceptions",
  "/control-templates", "/control-tests", "/controls", "/dashboard", "/dashboards", "/drift-detection",
  "/evidence", "/frameworks", "/gap-analysis", "/incidents", "/integrations", "/monitoring", "/notifications",
  "/onboarding", "/playbooks", "/policies", "/privacy-requests", "/profile", "/prowler", "/questionnaires",
  "/reports", "/risks", "/settings", "/training", "/vendors", "/workflows",
] as const;

export function isProtectedAppPath(pathname: string): boolean {
  return PROTECTED_APP_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`));
}

export function isMarketingPath(pathname: string): boolean {
  return MARKETING_PATHS.some((path) => path === pathname) || pathname.startsWith('/blog/')
    || pathname === '/compliance-directory' || pathname.startsWith('/compliance-directory/')
    || RESOURCE_SLUGS.some((slug) => pathname === `/resources/${slug}`);
}
