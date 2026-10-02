import { describe, expect, test } from "vitest";
import { NextRequest } from "next/server";
import fs from "fs";
import path from "path";
import { middleware } from "@/middleware";
import { PROTECTED_APP_PREFIXES } from "@/lib/marketing-routes";

describe("route authentication middleware", () => {
  test("redirects an unauthenticated dashboard request to login", () => {
    const response = middleware(new NextRequest("http://localhost:3001/dashboard?tab=risk"));
    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe(
      "http://localhost:3001/login?returnTo=%2Fdashboard%3Ftab%3Drisk"
    );
  });

  test("allows dashboard access when a refresh session cookie is present", () => {
    const response = middleware(
      new NextRequest("http://localhost:3001/dashboard", {
        headers: { cookie: "qt_refresh=opaque-session" },
      })
    );
    expect(response.status).toBe(200);
    expect(response.headers.get("X-Request-Id")).toBeTruthy();
  });

  test("keeps login, reset, invitation, and trust routes public", () => {
    for (const path of ["/login", "/reset-password?token=x", "/invite/token", "/trust/public"]) {
      expect(middleware(new NextRequest(`http://localhost:3001${path}`)).status).toBe(200);
    }
  });
});

describe("public marketing routes", () => {
  test("serves marketing pages and crawler assets without a session", () => {
    for (const path of ["/", "/trust-center", "/integrations", "/about", "/contact", "/pricing", "/soc-2-compliance", "/iso-27001-certification", "/hipaa-compliance", "/compare/quicktrust-vs-vanta", "/compare/quicktrust-vs-drata", "/solutions/security-questionnaire-automation", "/privacy-policy", "/terms-of-service", "/blog", "/blog/pillar-soc2-complete-guide", "/resources/soc2-readiness-scorecard", "/robots.txt", "/sitemap.xml", "/llms.txt", "/site.webmanifest", "/marketing-icon.svg", "/og/home"])
      expect(middleware(new NextRequest(`http://localhost:3001${path}`)).status, path).toBe(200);
  });
  test("still sends every protected application route to login", () => {
    for (const path of ["/settings/trust-center", "/settings/integrations", "/integrations/123", "/controls", "/settings", "/frameworks", "/evidence", "/policies", "/dashboard", "/agents/remediation"])
      expect(middleware(new NextRequest(`http://localhost:3001${path}`)).status, path).toBe(307);
  });
  test("passes unknown and lookalike public paths through to the router's 404 instead of login", () => {
    for (const path of ["/blog-admin", "/contact/private", "/compare/private", "/portal-admin", "/Blog", "/no-such-page", "/content/private", "/resources/private"]) {
      const response = middleware(new NextRequest(`http://localhost:3001${path}`));
      expect(response.status, path).toBe(200);
      expect(response.headers.get("location"), path).toBeNull();
    }
  });
  test("the protected prefix list covers every top-level application route segment", () => {
    const appDir = path.join(process.cwd(), "src/app");
    const segments = fs.readdirSync(path.join(appDir, "(dashboard)"), { withFileTypes: true })
      .filter((entry) => entry.isDirectory()).map((entry) => `/${entry.name}`);
    for (const segment of segments) expect(PROTECTED_APP_PREFIXES, segment).toContain(segment);
    expect(fs.readdirSync(path.join(appDir, "(auditor)"), { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name)).toEqual(["portal"]);
    expect(fs.readdirSync(path.join(appDir, "(auth)"), { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name)).toEqual(["login"]);
  });
});
