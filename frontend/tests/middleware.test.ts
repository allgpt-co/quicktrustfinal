import { describe, expect, test } from "vitest";
import { NextRequest } from "next/server";
import { middleware } from "@/middleware";

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
