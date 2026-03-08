import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_PATHS = ["/", "/login", "/trust"];
const AUDITOR_PATHS = ["/portal"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public paths
  if (PUBLIC_PATHS.some((p) => pathname === p || pathname.startsWith("/trust/"))) {
    return NextResponse.next();
  }

  // Allow auditor paths
  if (AUDITOR_PATHS.some((p) => pathname.startsWith(p))) {
    return NextResponse.next();
  }

  // For dashboard routes, check for auth cookie/token
  // This is a basic check - the real auth happens in the AuthProvider
  const hasAuth = request.cookies.get("kc-access") || request.headers.get("authorization");
  if (!hasAuth && pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
