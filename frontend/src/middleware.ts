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

  // Dashboard auth is handled client-side by the AuthProvider + keycloak-js.
  // keycloak-js stores tokens in memory (not cookies), so middleware cannot
  // check auth state.  The dashboard layout shows a sign-in prompt when
  // the user is not authenticated.
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
