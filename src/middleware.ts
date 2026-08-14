import { NextResponse, type NextRequest } from 'next/server';

/**
 * Must match SESSION_COOKIE in src/lib/auth.ts. Inlined on purpose: middleware runs on the
 * edge runtime and lib/auth.ts pulls in node:crypto.
 */
const SESSION_COOKIE = 'sm_session';

/**
 * Presence check only — a cheap bounce for logged-out visitors so they land on /login
 * instead of a flash of admin chrome. The real gate is requireAdmin() in the admin
 * layout, which verifies the HMAC and expiry server-side.
 */
export function middleware(req: NextRequest) {
  const token = req.cookies.get(SESSION_COOKIE)?.value;
  if (token) return NextResponse.next();

  const login = new URL('/login', req.nextUrl.origin);
  // Path AND query, so a filtered view survives the round trip through login.
  // Always same-origin and relative; the login action re-validates it anyway.
  login.searchParams.set('next', `${req.nextUrl.pathname}${req.nextUrl.search}`);
  return NextResponse.redirect(login);
}

export const config = {
  // Admin routes only: /_next/*, /favicon.svg and everything else static never match.
  matcher: ['/admin', '/admin/:path*'],
};
