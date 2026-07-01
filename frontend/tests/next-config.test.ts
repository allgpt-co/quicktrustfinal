import { afterEach, describe, expect, test, vi } from "vitest";

async function getCspHeaderForNodeEnv(nodeEnv: string): Promise<string> {
  const originalNodeEnv = process.env.NODE_ENV;
  process.env.NODE_ENV = nodeEnv;
  vi.resetModules();

  const { default: nextConfig } = await import("../next.config");
  const headers = await nextConfig.headers?.();

  process.env.NODE_ENV = originalNodeEnv;

  const cspHeader = headers?.[0]?.headers.find(
    (header) => header.key === "Content-Security-Policy"
  );

  if (!cspHeader) {
    throw new Error("Content-Security-Policy header was not configured");
  }

  return cspHeader.value;
}

describe("next security headers", () => {
  afterEach(() => {
    vi.resetModules();
  });

  test("allows Next.js inline bootstrap scripts in production CSP", async () => {
    const csp = await getCspHeaderForNodeEnv("production");

    expect(csp).toContain("script-src 'self' 'unsafe-inline'");
    expect(csp).not.toContain("'unsafe-eval'");
  });
});
