const isProduction = process.env.NODE_ENV === "production";

function normalizeUrl(value: string): string {
  return value.replace(/\/+$/, "");
}

function isLocalhostUrl(value: string): boolean {
  try {
    const hostname = new URL(value).hostname;
    return (
      hostname === "localhost" ||
      hostname === "127.0.0.1" ||
      hostname === "0.0.0.0" ||
      hostname.endsWith(".localhost")
    );
  } catch {
    return false;
  }
}

function publicUrl(
  envKey: string,
  configuredValue: string | undefined,
  developmentDefault: string,
  productionDefault?: string
): string {
  const value = configuredValue || (isProduction ? productionDefault : developmentDefault);

  if (!value) {
    throw new Error(`${envKey} must be configured in production`);
  }

  if (isProduction && isLocalhostUrl(value)) {
    throw new Error(`${envKey} cannot use localhost in production`);
  }

  return normalizeUrl(value);
}

export const API_URL = publicUrl(
  "NEXT_PUBLIC_API_URL",
  process.env.NEXT_PUBLIC_API_URL,
  "http://localhost:8000",
  "https://api.quicktrustapp.com"
);

export const APP_URL = publicUrl(
  "NEXT_PUBLIC_APP_URL",
  process.env.NEXT_PUBLIC_APP_URL,
  "http://localhost:3001",
  "https://quicktrustapp.com"
);

export const KEYCLOAK_URL = publicUrl(
  "NEXT_PUBLIC_KEYCLOAK_URL",
  process.env.NEXT_PUBLIC_KEYCLOAK_URL,
  "http://localhost:8080",
  "https://keycloak.quicktrustapp.com"
);

export const KEYCLOAK_REALM =
  process.env.NEXT_PUBLIC_KEYCLOAK_REALM || "quicktrust";

export const KEYCLOAK_CLIENT_ID =
  process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID || "quicktrust-web";
