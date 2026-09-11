"use client";

import { usePathname } from "next/navigation";
import { isMarketingPath } from "@/lib/marketing-routes";
import { AuthProvider } from "./auth-provider";
import { QueryProvider } from "./query-provider";

export function ApplicationProviders({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  // Public pages render without session refreshes or an available backend.
  if (isMarketingPath(pathname)) return <>{children}</>;
  return <QueryProvider><AuthProvider>{children}</AuthProvider></QueryProvider>;
}
