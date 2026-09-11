import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { isMarketingPath, PUBLIC_ASSETS } from "@/lib/marketing-routes";

const PUBLIC_PATHS = ["/", "/login", "/reset-password", "/trust"];
const AUDITOR_PATHS = ["/portal"];

export function middleware(request: NextRequest) {
  const { pathname, search } = request.nextUrl;
  const isPublic = PUBLIC_PATHS.includes(pathname) || pathname.startsWith("/trust/")
    || isMarketingPath(pathname) || PUBLIC_ASSETS.some((path) => path === pathname)
    || pathname.startsWith("/og/") || pathname === "/signup";
  const isAuditor = AUDITOR_PATHS.some((path) => pathname === path || pathname.startsWith(`${path}/`));
  const isInvitation = pathname.startsWith("/invite/");

  if (!isPublic && !isAuditor && !isInvitation && !request.cookies.has("qt_refresh")) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("returnTo", `${pathname}${search}`);
    return NextResponse.redirect(loginUrl);
  }

  const response = NextResponse.next();
  response.headers.set("X-Request-Id", crypto.randomUUID());
  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
