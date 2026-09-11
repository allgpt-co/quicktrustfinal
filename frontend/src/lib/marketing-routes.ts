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

export function isMarketingPath(pathname: string): boolean {
  return MARKETING_PATHS.some((path) => path === pathname) || pathname.startsWith("/blog/");
}
