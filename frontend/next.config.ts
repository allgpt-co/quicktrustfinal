import type { NextConfig } from "next";
import { CONTENT_REDIRECTS } from "./src/lib/marketing-routes";

function originFromEnv(value: string | undefined): string | null {
  if (!value) return null;
  try {
    return new URL(value).origin;
  } catch {
    return null;
  }
}

const isProduction = process.env.NODE_ENV === "production";
const ga4MeasurementId = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID?.trim();
const hasGa4MeasurementId = Boolean(ga4MeasurementId && /^G-[A-Z0-9]+$/.test(ga4MeasurementId));

function isLocalhostOrigin(origin: string): boolean {
  try {
    const hostname = new URL(origin).hostname;
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

function isAllowedConnectOrigin(origin: string | null): origin is string {
  if (!origin) return false;
  return !isProduction || !isLocalhostOrigin(origin);
}

const connectSrcOrigins = Array.from(
  new Set(
    [
      "'self'",
      ...(isProduction
        ? []
        : ["http://localhost:8000"]),
      originFromEnv(process.env.NEXT_PUBLIC_API_URL),
      "https://app.truconversion.com",
      "https://io.truconversion.com",
      "wss://io.truconversion.com",
      ...(hasGa4MeasurementId
        ? ["https://www.google-analytics.com", "https://region1.google-analytics.com", "https://analytics.google.com"]
        : []),
    ].filter(isAllowedConnectOrigin)
  )
).join(" ");

const cspDirectives = [
  "default-src 'self'",
  // Next.js emits inline bootstrap scripts; unsafe-eval stays dev-only.
  isProduction
    ? `script-src 'self' 'unsafe-inline' https://app.truconversion.com https://cdn.truconversion.com${hasGa4MeasurementId ? " https://www.googletagmanager.com" : ""}`
    : `script-src 'self' 'unsafe-eval' 'unsafe-inline' https://app.truconversion.com https://cdn.truconversion.com${hasGa4MeasurementId ? " https://www.googletagmanager.com" : ""}`,
  "style-src 'self' 'unsafe-inline'", // Tailwind requires inline styles
  "img-src 'self' data: blob: https:",
  "font-src 'self' data:",
  `connect-src ${connectSrcOrigins}`,
  "frame-src 'self' https://cdn.truconversion.com",
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "object-src 'none'",
].join("; ");

const nextConfig: NextConfig = {
  outputFileTracingIncludes: { "/*": ["./content/content_output/**/*.md"] },
  async redirects() {
    return [
      { source: "/signup", destination: "/login?mode=register", permanent: true },
      ...Object.entries(CONTENT_REDIRECTS).map(([source, destination]) => ({
        source, destination, permanent: true,
      })),
    ];
  },
  // 'standalone' output requires symlink permissions on Windows.
  // Enable only in Docker/CI builds via NEXT_OUTPUT_STANDALONE env var.
  ...(process.env.NEXT_OUTPUT_STANDALONE === "true"
    ? { output: "standalone" as const }
    : {}),
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-XSS-Protection", value: "1; mode=block" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=(), payment=()",
          },
          { key: "Content-Security-Policy", value: cspDirectives },
          { key: "X-DNS-Prefetch-Control", value: "on" },
        ],
      },
    ];
  },
};

export default nextConfig;
