import { afterEach, describe, expect, test, vi } from "vitest";

async function importPublicEnv(env: Record<string, string | undefined>) {
  const originalEnv = { ...process.env };
  Object.entries(env).forEach(([key, value]) => {
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  });
  vi.resetModules();
  try {
    return await import("../src/lib/public-env");
  } finally {
    process.env = originalEnv;
  }
}

describe("public environment", () => {
  afterEach(() => vi.resetModules());

  test("rejects a localhost API URL in production", async () => {
    await expect(importPublicEnv({ NODE_ENV: "production", NEXT_PUBLIC_API_URL: "http://localhost:8000" })).rejects.toThrow("NEXT_PUBLIC_API_URL");
  });

  test("uses public production defaults for app origins", async () => {
    const env = await importPublicEnv({ NODE_ENV: "production", NEXT_PUBLIC_API_URL: undefined, NEXT_PUBLIC_APP_URL: undefined });
    expect(env.API_URL).toBe("https://api.quicktrustapp.com");
    expect(env.APP_URL).toBe("https://quicktrustapp.com");
  });
});
