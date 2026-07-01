import { afterEach, describe, expect, test, vi } from "vitest";

async function importPublicEnv(env: Record<string, string | undefined>) {
  const originalEnv = { ...process.env };
  Object.entries(env).forEach(([key, value]) => {
    if (value === undefined) {
      delete process.env[key];
    } else {
      process.env[key] = value;
    }
  });
  vi.resetModules();

  try {
    return await import("../src/lib/public-env");
  } finally {
    process.env = originalEnv;
  }
}

describe("public environment", () => {
  afterEach(() => {
    vi.resetModules();
  });

  test("rejects localhost public URLs in production", async () => {
    await expect(
      importPublicEnv({
        NODE_ENV: "production",
        NEXT_PUBLIC_API_URL: "https://api.quicktrustapp.com",
        NEXT_PUBLIC_KEYCLOAK_URL: "http://localhost:8080",
      })
    ).rejects.toThrow("NEXT_PUBLIC_KEYCLOAK_URL");
  });

  test("uses public production defaults for known app origins", async () => {
    const env = await importPublicEnv({
      NODE_ENV: "production",
      NEXT_PUBLIC_API_URL: undefined,
      NEXT_PUBLIC_APP_URL: undefined,
      NEXT_PUBLIC_KEYCLOAK_URL: "https://keycloak.quicktrustapp.com",
    });

    expect(env.API_URL).toBe("https://api.quicktrustapp.com");
    expect(env.APP_URL).toBe("https://quicktrustapp.com");
  });
});
