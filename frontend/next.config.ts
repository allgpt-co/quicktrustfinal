import type { NextConfig } from "next";
import { ARTICLE_REDIRECTS } from "./src/lib/marketing-routes";

function originFromEnv(value: string | undefined): string | null {
  if (!value) return null;
  try {
    return new URL(value).origin;
  } catch {
    return null;
  }
}

const isProduction = process.env.NODE_ENV === "production";

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
    ].filter(isAllowedConnectOrigin)
  )
).join(" ");

const cspDirectives = [
  "default-src 'self'",
  // Next.js emits inline bootstrap scripts; unsafe-eval stays dev-only.
  isProduction
    ? "script-src 'self' 'unsafe-inline'"
    : "script-src 'self' 'unsafe-eval' 'unsafe-inline'",
  "style-src 'self' 'unsafe-inline'", // Tailwind requires inline styles
  "img-src 'self' data: blob: https:",
  "font-src 'self' data:",
  `connect-src ${connectSrcOrigins}`,
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
      ...Object.entries(ARTICLE_REDIRECTS).map(([slug, destination]) => ({
        source: `/blog/${slug}`, destination, permanent: true,
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
