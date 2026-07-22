import { afterEach, describe, expect, test, vi } from "vitest";

async function getCspHeaderForNodeEnv(
  nodeEnv: string,
  env: Record<string, string | undefined> = {}
): Promise<string> {
  const originalEnv = { ...process.env };
  Object.defineProperty(process.env, "NODE_ENV", {
    value: nodeEnv,
    configurable: true,
    writable: true,
    enumerable: true,
  });
  Object.entries(env).forEach(([key, value]) => {
    if (value === undefined) {
      delete process.env[key];
    } else {
      process.env[key] = value;
    }
  });
  vi.resetModules();

  const { default: nextConfig } = await import("../next.config");
  const headers = await nextConfig.headers?.();

  process.env = originalEnv;

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

  test("does not allow localhost connections in production CSP", async () => {
    const csp = await getCspHeaderForNodeEnv("production", {
      NEXT_PUBLIC_API_URL: "https://api.quicktrustapp.com",
    });

    expect(csp).toContain("connect-src 'self'");
    expect(csp).toContain("https://api.quicktrustapp.com");
    expect(csp).not.toContain("http://localhost");
    expect(csp).not.toContain("127.0.0.1");
  });

  test("keeps localhost connections available for development CSP", async () => {
    const csp = await getCspHeaderForNodeEnv("development");

    expect(csp).toContain("http://localhost:8000");
  });
});
