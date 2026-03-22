# QuickTrust -- Missing Features Implementation Guide

**Document Date:** 2026-03-17
**Companion Document:** `missingfeatures.md` (Gap Analysis)
**Target Stack:** Next.js 15 + PostgreSQL + Prisma ORM + AWS S3 + TypeScript
**Estimated Total Effort:** 26-32 engineering weeks (2 senior engineers)

---

## Table of Contents

- [Phase 0: Foundation Security (Weeks 1-2)](#phase-0-foundation-security-weeks-1-2)
- [Phase 1: Identity & Access Management (Weeks 3-6)](#phase-1-identity--access-management-weeks-3-6)
- [Phase 2: Data Protection & Encryption (Weeks 7-10)](#phase-2-data-protection--encryption-weeks-7-10)
- [Phase 3: Audit Logging & Monitoring (Weeks 11-13)](#phase-3-audit-logging--monitoring-weeks-11-13)
- [Phase 4: Enterprise Integration -- SSO & SCIM (Weeks 14-17)](#phase-4-enterprise-integration--sso--scim-weeks-14-17)
- [Phase 5: Compliance Automation Engine (Weeks 18-22)](#phase-5-compliance-automation-engine-weeks-18-22)
- [Phase 6: AI Governance & LLM Safety (Weeks 23-25)](#phase-6-ai-governance--llm-safety-weeks-23-25)
- [Phase 7: Infrastructure & DR (Weeks 26-28)](#phase-7-infrastructure--dr-weeks-26-28)
- [Phase 8: Privacy, Reporting & Advanced (Weeks 29-32)](#phase-8-privacy-reporting--advanced-weeks-29-32)

---

## Phase 0: Foundation Security (Weeks 1-2)

> These fixes address the most critical security gaps that expose the platform to immediate risk. They require minimal architectural changes and can be deployed incrementally.

---

### 0.1 Secure Cookie Configuration

**Gap Reference:** missingfeatures.md §3.6
**Compliance:** SOC 2 CC6.1, PCI DSS 8.2.8, HIPAA 164.312(d)
**File:** `app/api/auth/login/route.ts`

**Current State:** The login route sets `httpOnly: false` on the auth cookie, which means any JavaScript on the page (including injected XSS) can read the token.

**Implementation:**

**Step 1:** Update the cookie configuration in the login response.

```typescript
// File: app/api/auth/login/route.ts
// Replace the current cookie-setting block with:

const isProduction = process.env.NODE_ENV === 'production';

const response = NextResponse.json({
  message: 'Login successful',
  user: { /* ... existing user fields ... */ },
  token,
});

response.cookies.set('auth_token', token, {
  httpOnly: true,                    // CRITICAL: prevent JS access
  secure: isProduction,              // HTTPS only in production
  sameSite: 'strict',                // Prevent CSRF entirely
  path: '/',                         // Available on all routes
  maxAge: 86400,                     // 24 hours
  ...(isProduction && {
    domain: process.env.COOKIE_DOMAIN || undefined,  // Set explicit domain in prod
  }),
});
```

**Step 2:** Since `httpOnly: true` prevents client-side JS from reading the token, update `lib/auth-client.ts` to stop storing/reading tokens from cookies directly. Instead, add an API-based auth check.

```typescript
// File: lib/auth-client.ts
// Replace token getter with API-based auth check:

export async function getAuthStatus(): Promise<{ authenticated: boolean; user: any | null }> {
  try {
    const res = await fetch('/api/auth/me', { credentials: 'include' });
    if (res.ok) {
      const data = await res.json();
      return { authenticated: true, user: data.user };
    }
    return { authenticated: false, user: null };
  } catch {
    return { authenticated: false, user: null };
  }
}

// For API calls that need auth, rely on cookies being sent automatically:
export function getAuthHeaders(): Record<string, string> {
  // With httpOnly cookies, the browser sends them automatically
  // No need to manually attach Authorization header for same-origin requests
  return { 'Content-Type': 'application/json' };
}
```

**Step 3:** Add the `COOKIE_DOMAIN` to `.env.example`:

```env
# Cookie Configuration
COOKIE_DOMAIN=".quicktrustapp.com"   # Set in production only
```

**Verification:**
- Open browser DevTools → Application → Cookies
- Confirm `auth_token` shows `HttpOnly: true`, `Secure: true` (in production), `SameSite: Strict`
- Confirm `document.cookie` in console does NOT show `auth_token`

---

### 0.2 Token Revocation via Redis Blacklist

**Gap Reference:** missingfeatures.md §3.3
**Compliance:** SOC 2 CC6.1, ISO 27001 A.5.18, PCI DSS 8.2.8
**New Files:** `lib/redis.ts`, `lib/token-blacklist.ts`
**Modified Files:** `lib/jwt.ts`, `app/api/auth/logout/route.ts`
**New Dependencies:** `ioredis`

**Step 1:** Install Redis client.

```bash
npm install ioredis
npm install -D @types/ioredis
```

**Step 2:** Add Redis environment variables to `.env.example`:

```env
# Redis Configuration
REDIS_URL="redis://localhost:6379"
REDIS_PASSWORD=""
REDIS_TLS_ENABLED="false"
```

**Step 3:** Create the Redis client module.

```typescript
// File: lib/redis.ts

import Redis from 'ioredis';

let redisInstance: Redis | null = null;

export function getRedis(): Redis {
  if (redisInstance) return redisInstance;

  const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';

  redisInstance = new Redis(redisUrl, {
    password: process.env.REDIS_PASSWORD || undefined,
    tls: process.env.REDIS_TLS_ENABLED === 'true' ? {} : undefined,
    maxRetriesPerRequest: 3,
    retryStrategy(times: number) {
      if (times > 3) return null; // Stop retrying after 3 attempts
      return Math.min(times * 200, 2000);
    },
    lazyConnect: true,
  });

  redisInstance.on('error', (err) => {
    console.error('[Redis] Connection error:', err.message);
  });

  return redisInstance;
}
```

**Step 4:** Create the token blacklist module.

```typescript
// File: lib/token-blacklist.ts

import { getRedis } from './redis';
import jwt from 'jsonwebtoken';

const BLACKLIST_PREFIX = 'token:blacklist:';

/**
 * Add a token to the blacklist. The entry auto-expires when the token
 * would have expired anyway, so Redis memory stays bounded.
 */
export async function blacklistToken(token: string): Promise<void> {
  try {
    const decoded = jwt.decode(token) as { exp?: number } | null;
    if (!decoded?.exp) return;

    const ttl = decoded.exp - Math.floor(Date.now() / 1000);
    if (ttl <= 0) return; // Already expired, no need to blacklist

    const redis = getRedis();
    await redis.set(`${BLACKLIST_PREFIX}${token}`, '1', 'EX', ttl);
  } catch (err) {
    console.error('[TokenBlacklist] Failed to blacklist token:', err);
    // Fail open: if Redis is down, tokens still expire naturally
  }
}

/**
 * Check if a token has been revoked.
 */
export async function isTokenBlacklisted(token: string): Promise<boolean> {
  try {
    const redis = getRedis();
    const result = await redis.get(`${BLACKLIST_PREFIX}${token}`);
    return result !== null;
  } catch (err) {
    console.error('[TokenBlacklist] Failed to check blacklist:', err);
    return false; // Fail open
  }
}

/**
 * Blacklist ALL tokens for a user by storing a "revoked-before" timestamp.
 * Any token issued before this timestamp is considered invalid.
 */
export async function revokeAllUserTokens(userId: number): Promise<void> {
  try {
    const redis = getRedis();
    const key = `user:${userId}:tokens_revoked_at`;
    await redis.set(key, Math.floor(Date.now() / 1000).toString(), 'EX', 86400);
  } catch (err) {
    console.error('[TokenBlacklist] Failed to revoke user tokens:', err);
  }
}

/**
 * Check if a token was issued before a user-level revocation.
 */
export async function isUserTokenRevoked(userId: number, tokenIssuedAt: number): Promise<boolean> {
  try {
    const redis = getRedis();
    const revokedAt = await redis.get(`user:${userId}:tokens_revoked_at`);
    if (!revokedAt) return false;
    return tokenIssuedAt < parseInt(revokedAt, 10);
  } catch (err) {
    console.error('[TokenBlacklist] Failed to check user revocation:', err);
    return false;
  }
}
```

**Step 5:** Update `lib/jwt.ts` to check the blacklist during verification.

```typescript
// File: lib/jwt.ts
// Add to the verifyToken function:

import { isTokenBlacklisted, isUserTokenRevoked } from './token-blacklist';

export async function verifyToken(token: string): Promise<JWTPayload | null> {
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as JWTPayload & { iat?: number };

    // Check single-token blacklist
    if (await isTokenBlacklisted(token)) {
      return null;
    }

    // Check user-level revocation
    if (decoded.userId && decoded.iat) {
      if (await isUserTokenRevoked(decoded.userId, decoded.iat)) {
        return null;
      }
    }

    return decoded;
  } catch (error) {
    return null;
  }
}
```

**Note:** Since `verifyToken` becomes async, update all callers. The primary caller is `getCurrentUser` in `lib/auth.ts`:

```typescript
// File: lib/auth.ts
// Change getCurrentUser to async:

export async function getCurrentUser(request: Request): Promise<JWTPayload | null> {
  const token = getTokenFromRequest(request);
  if (!token) return null;
  return await verifyToken(token);
}
```

**Step 6:** Update all route handlers that call `getCurrentUser` to `await` it. For example:

```typescript
// Every route.ts file that does:
//   const payload = getCurrentUser(request);
// Must change to:
//   const payload = await getCurrentUser(request);
```

**Step 7:** Update the logout endpoint to actually revoke the token.

```typescript
// File: app/api/auth/logout/route.ts

import { NextResponse } from 'next/server';
import { getTokenFromRequest } from '@/lib/jwt';
import { blacklistToken } from '@/lib/token-blacklist';

export async function POST(request: Request) {
  // Get the token before clearing the cookie
  const token = getTokenFromRequest(request);

  if (token) {
    await blacklistToken(token);
  }

  const response = NextResponse.json({ message: 'Logged out successfully' });

  // Clear the cookie
  response.cookies.set('auth_token', '', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 0, // Immediate expiration
  });

  return response;
}
```

**Verification:**
1. Login, note token
2. Logout
3. Attempt to use the old token in Authorization header → should get 401
4. Login again → should get new valid token

---

### 0.3 Rate Limiting

**Gap Reference:** missingfeatures.md §14.1
**Compliance:** SOC 2 CC6.6, PCI DSS 6.5.10, OWASP API Security
**New Files:** `lib/rate-limiter.ts`, `middleware.ts`
**New Dependencies:** None (uses Redis from Step 0.2)

**Step 1:** Create the rate limiter module using a sliding window algorithm backed by Redis.

```typescript
// File: lib/rate-limiter.ts

import { getRedis } from './redis';

interface RateLimitConfig {
  windowMs: number;    // Time window in milliseconds
  maxRequests: number; // Max requests per window
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;      // Unix timestamp when window resets
  retryAfter?: number;  // Seconds until next allowed request
}

// Default limits per route category
export const RATE_LIMITS: Record<string, RateLimitConfig> = {
  auth: { windowMs: 60_000, maxRequests: 5 },         // 5 login attempts/minute
  signup: { windowMs: 3600_000, maxRequests: 10 },     // 10 signups/hour per IP
  api: { windowMs: 60_000, maxRequests: 100 },         // 100 API calls/minute
  upload: { windowMs: 3600_000, maxRequests: 50 },     // 50 uploads/hour
  aiQuery: { windowMs: 60_000, maxRequests: 10 },      // 10 AI queries/minute
  public: { windowMs: 60_000, maxRequests: 30 },       // 30 public requests/minute
};

export async function checkRateLimit(
  key: string,
  config: RateLimitConfig
): Promise<RateLimitResult> {
  const redis = getRedis();
  const now = Date.now();
  const windowStart = now - config.windowMs;
  const redisKey = `ratelimit:${key}`;

  try {
    // Use sorted set: score = timestamp, member = unique request ID
    const pipeline = redis.pipeline();
    pipeline.zremrangebyscore(redisKey, 0, windowStart); // Remove expired entries
    pipeline.zadd(redisKey, now, `${now}:${Math.random()}`); // Add current request
    pipeline.zcard(redisKey); // Count requests in window
    pipeline.expire(redisKey, Math.ceil(config.windowMs / 1000)); // Auto-cleanup

    const results = await pipeline.exec();
    const requestCount = (results?.[2]?.[1] as number) || 0;

    if (requestCount > config.maxRequests) {
      // Find the oldest request in the window to calculate retry-after
      const oldestEntries = await redis.zrangebyscore(redisKey, '-inf', '+inf', 'LIMIT', 0, 1);
      const oldestTime = oldestEntries.length > 0 ? parseInt(oldestEntries[0].split(':')[0]) : now;
      const retryAfter = Math.ceil((oldestTime + config.windowMs - now) / 1000);

      return {
        allowed: false,
        remaining: 0,
        resetAt: Math.ceil((now + config.windowMs) / 1000),
        retryAfter: Math.max(retryAfter, 1),
      };
    }

    return {
      allowed: true,
      remaining: config.maxRequests - requestCount,
      resetAt: Math.ceil((now + config.windowMs) / 1000),
    };
  } catch (err) {
    console.error('[RateLimiter] Redis error, allowing request:', err);
    return { allowed: true, remaining: config.maxRequests, resetAt: 0 };
  }
}

/**
 * Extract client IP from request, accounting for proxies.
 */
export function getClientIp(request: Request): string {
  const forwarded = request.headers.get('x-forwarded-for');
  if (forwarded) {
    return forwarded.split(',')[0].trim();
  }
  const realIp = request.headers.get('x-real-ip');
  if (realIp) return realIp;
  return '127.0.0.1';
}
```

**Step 2:** Create Next.js middleware for global rate limiting.

```typescript
// File: middleware.ts (project root)

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Note: Next.js Edge middleware cannot use ioredis directly.
// For production, use Upstash Redis or move rate limiting into API route wrappers.
// This middleware handles CSRF and auth-route redirect protection.

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // --- CSRF Protection for state-changing methods ---
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(request.method)) {
    const origin = request.headers.get('origin');
    const host = request.headers.get('host');

    // Allow if origin matches host (same-origin)
    if (origin && host) {
      const originHost = new URL(origin).host;
      if (originHost !== host) {
        return NextResponse.json(
          { error: 'CSRF validation failed: origin mismatch' },
          { status: 403 }
        );
      }
    }
  }

  // --- Protect dashboard routes ---
  if (pathname.startsWith('/dashboard')) {
    const token = request.cookies.get('auth_token')?.value;
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  // --- Add security headers ---
  const response = NextResponse.next();
  response.headers.set('X-Request-Id', crypto.randomUUID());
  return response;
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/:path*',
  ],
};
```

**Step 3:** Create a rate-limiting wrapper for use inside API routes (since Next.js Edge middleware has limited Node.js API access).

```typescript
// File: lib/api-guard.ts

import { NextResponse } from 'next/server';
import { checkRateLimit, getClientIp, RATE_LIMITS, RateLimitConfig } from './rate-limiter';
import { getCurrentUser } from './auth';
import { JWTPayload } from './jwt';

interface GuardOptions {
  rateLimit?: keyof typeof RATE_LIMITS | RateLimitConfig;
  requireAuth?: boolean;
  requireOrg?: boolean;
}

interface GuardResult {
  allowed: boolean;
  response?: NextResponse;
  user?: JWTPayload & { orgId?: number | null; role?: string };
}

/**
 * Unified API guard: rate limiting + auth + org check in one call.
 * Usage in route handlers:
 *
 *   const guard = await apiGuard(request, { rateLimit: 'api', requireAuth: true, requireOrg: true });
 *   if (!guard.allowed) return guard.response;
 *   const user = guard.user;
 */
export async function apiGuard(
  request: Request,
  options: GuardOptions = {}
): Promise<GuardResult> {
  const { rateLimit: rateLimitKey, requireAuth = false, requireOrg = false } = options;

  // --- Rate Limiting ---
  if (rateLimitKey) {
    const config = typeof rateLimitKey === 'string' ? RATE_LIMITS[rateLimitKey] : rateLimitKey;
    if (config) {
      const ip = getClientIp(request);
      const url = new URL(request.url);
      const key = `${ip}:${url.pathname}`;
      const result = await checkRateLimit(key, config);

      if (!result.allowed) {
        return {
          allowed: false,
          response: NextResponse.json(
            { error: 'Too many requests. Please try again later.' },
            {
              status: 429,
              headers: {
                'Retry-After': String(result.retryAfter || 60),
                'X-RateLimit-Limit': String(config.maxRequests),
                'X-RateLimit-Remaining': '0',
                'X-RateLimit-Reset': String(result.resetAt),
              },
            }
          ),
        };
      }
    }
  }

  // --- Authentication ---
  if (requireAuth) {
    const payload = await getCurrentUser(request);
    if (!payload) {
      return {
        allowed: false,
        response: NextResponse.json(
          { error: 'Authentication required' },
          { status: 401 }
        ),
      };
    }

    // Look up full user for org/role checks
    const { prisma } = await import('./db');
    const user = await prisma.user.findUnique({
      where: { id: payload.userId },
      select: { id: true, email: true, fullName: true, orgId: true, role: true },
    });

    if (!user) {
      return {
        allowed: false,
        response: NextResponse.json({ error: 'User not found' }, { status: 401 }),
      };
    }

    if (requireOrg && !user.orgId) {
      return {
        allowed: false,
        response: NextResponse.json(
          { error: 'You must belong to an organization to access this resource' },
          { status: 403 }
        ),
      };
    }

    return {
      allowed: true,
      user: {
        userId: user.id,
        email: user.email,
        fullName: user.fullName || undefined,
        orgId: user.orgId,
        role: user.role,
      },
    };
  }

  return { allowed: true };
}
```

**Step 4:** Retrofit existing routes. Example for the login route:

```typescript
// File: app/api/auth/login/route.ts
// At the top of the POST handler, add:

import { apiGuard } from '@/lib/api-guard';

export async function POST(request: Request) {
  const guard = await apiGuard(request, { rateLimit: 'auth' });
  if (!guard.allowed) return guard.response;

  // ... rest of existing login logic ...
}
```

Example for a protected route:

```typescript
// File: app/api/evidence/route.ts
import { apiGuard } from '@/lib/api-guard';

export async function GET(request: Request) {
  const guard = await apiGuard(request, {
    rateLimit: 'api',
    requireAuth: true,
    requireOrg: true,
  });
  if (!guard.allowed) return guard.response!;
  const user = guard.user!;

  // Use user.orgId for queries
  const evidence = await prisma.evidence.findMany({
    where: { orgId: user.orgId! },
    // ...
  });
}
```

**Verification:**
1. Hit `/api/auth/login` more than 5 times in 60 seconds → expect `429 Too Many Requests`
2. Check response headers for `X-RateLimit-Remaining`, `Retry-After`
3. Wait for window to expire → requests should succeed again

---

### 0.4 Account Lockout After Failed Login Attempts

**Gap Reference:** missingfeatures.md §1.2
**Compliance:** SOC 2 CC6.1, PCI DSS 8.3.4, NIST 800-53 AC-7

**Step 1:** Add lockout tracking fields to the User model.

```prisma
// File: prisma/schema.prisma
// Add to the User model:

model User {
  // ... existing fields ...
  failedLoginAttempts  Int       @default(0) @map("failed_login_attempts")
  lockedUntil          DateTime? @map("locked_until")
  lastFailedLogin      DateTime? @map("last_failed_login")
  passwordChangedAt    DateTime? @map("password_changed_at")
}
```

**Step 2:** Run migration.

```bash
npx prisma migrate dev --name add-account-lockout-fields
```

**Step 3:** Update `lib/auth.ts` `authenticateUser` function:

```typescript
// File: lib/auth.ts
// Replace the authenticateUser function:

const MAX_FAILED_ATTEMPTS = 5;
const LOCKOUT_DURATION_MS = 30 * 60 * 1000; // 30 minutes

export async function authenticateUser(
  email: string,
  password: string
): Promise<{ user: Omit<User, 'passwordHash'>; token: string } | { error: string; locked?: boolean }> {
  const emailLower = email.trim().toLowerCase();

  const user = await prisma.user.findUnique({
    where: { email: emailLower },
    select: {
      id: true,
      email: true,
      passwordHash: true,
      fullName: true,
      orgId: true,
      role: true,
      createdAt: true,
      lastLogin: true,
      failedLoginAttempts: true,
      lockedUntil: true,
    },
  });

  if (!user) {
    return { error: 'Invalid email or password' };
  }

  // Check if account is locked
  if (user.lockedUntil && user.lockedUntil > new Date()) {
    const remainingMs = user.lockedUntil.getTime() - Date.now();
    const remainingMin = Math.ceil(remainingMs / 60000);
    return {
      error: `Account locked. Try again in ${remainingMin} minutes.`,
      locked: true,
    };
  }

  // If lock period has expired, reset the counter
  if (user.lockedUntil && user.lockedUntil <= new Date()) {
    await prisma.user.update({
      where: { id: user.id },
      data: { failedLoginAttempts: 0, lockedUntil: null },
    });
  }

  const isValid = await comparePassword(password, user.passwordHash);

  if (!isValid) {
    const newFailedAttempts = (user.failedLoginAttempts || 0) + 1;
    const updateData: any = {
      failedLoginAttempts: newFailedAttempts,
      lastFailedLogin: new Date(),
    };

    if (newFailedAttempts >= MAX_FAILED_ATTEMPTS) {
      updateData.lockedUntil = new Date(Date.now() + LOCKOUT_DURATION_MS);
    }

    await prisma.user.update({
      where: { id: user.id },
      data: updateData,
    });

    const attemptsRemaining = MAX_FAILED_ATTEMPTS - newFailedAttempts;
    if (attemptsRemaining > 0) {
      return { error: `Invalid email or password. ${attemptsRemaining} attempts remaining.` };
    }
    return { error: 'Account locked due to too many failed attempts. Try again in 30 minutes.', locked: true };
  }

  // Successful login: reset failed attempts
  const updatedUser = await prisma.user.update({
    where: { id: user.id },
    data: {
      lastLogin: new Date(),
      failedLoginAttempts: 0,
      lockedUntil: null,
    },
    select: {
      id: true, email: true, fullName: true, orgId: true,
      role: true, createdAt: true, lastLogin: true,
    },
  });

  const token = generateToken({
    userId: user.id,
    email: user.email,
    fullName: user.fullName || undefined,
  });

  return {
    user: {
      id: updatedUser.id, email: updatedUser.email, fullName: updatedUser.fullName,
      orgId: updatedUser.orgId, role: updatedUser.role,
      createdAt: updatedUser.createdAt, lastLogin: updatedUser.lastLogin,
    },
    token,
  };
}
```

**Step 4:** Update the login route to handle the new return type:

```typescript
// File: app/api/auth/login/route.ts

const result = await authenticateUser(email, password);

if ('error' in result) {
  const status = result.locked ? 423 : 401;
  return NextResponse.json({ error: result.error }, { status });
}

// ... success path continues as before with result.user and result.token ...
```

---

### 0.5 Password Policy Engine

**Gap Reference:** missingfeatures.md §1.1
**Compliance:** SOC 2 CC6.1, ISO 27001 A.5.17, PCI DSS 8.3.6
**New File:** `lib/password-policy.ts`

**Step 1:** Create the password policy module.

```typescript
// File: lib/password-policy.ts

export interface PasswordPolicyConfig {
  minLength: number;
  maxLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecialChars: boolean;
  maxRepeatingChars: number;       // Max consecutive identical characters
  preventCommonPasswords: boolean;
  preventUserInfoInPassword: boolean;
}

// Default policy (meets PCI DSS 8.3.6 + NIST 800-63B)
export const DEFAULT_PASSWORD_POLICY: PasswordPolicyConfig = {
  minLength: 12,
  maxLength: 128,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true,
  maxRepeatingChars: 3,
  preventCommonPasswords: true,
  preventUserInfoInPassword: true,
};

// Top 100 most common passwords (truncated for brevity; use a full list in production)
const COMMON_PASSWORDS = new Set([
  'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 'master',
  'dragon', '111111', 'baseball', 'iloveyou', 'trustno1', 'sunshine',
  'letmein', 'welcome', 'shadow', 'superman', 'michael', 'password1',
  'password123', 'admin', 'admin123', 'changeme', 'p@ssw0rd',
]);

export interface PasswordValidationResult {
  valid: boolean;
  errors: string[];
}

export function validatePassword(
  password: string,
  policy: PasswordPolicyConfig = DEFAULT_PASSWORD_POLICY,
  userInfo?: { email?: string; fullName?: string }
): PasswordValidationResult {
  const errors: string[] = [];

  if (password.length < policy.minLength) {
    errors.push(`Password must be at least ${policy.minLength} characters`);
  }

  if (password.length > policy.maxLength) {
    errors.push(`Password must not exceed ${policy.maxLength} characters`);
  }

  if (policy.requireUppercase && !/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }

  if (policy.requireLowercase && !/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }

  if (policy.requireNumbers && !/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number');
  }

  if (policy.requireSpecialChars && !/[!@#$%^&*()_+\-=\[\]{}|;':",.\/<>?`~\\]/.test(password)) {
    errors.push('Password must contain at least one special character');
  }

  if (policy.maxRepeatingChars > 0) {
    const repeatingRegex = new RegExp(`(.)\\1{${policy.maxRepeatingChars},}`);
    if (repeatingRegex.test(password)) {
      errors.push(`Password must not contain more than ${policy.maxRepeatingChars} repeating characters`);
    }
  }

  if (policy.preventCommonPasswords && COMMON_PASSWORDS.has(password.toLowerCase())) {
    errors.push('Password is too common. Please choose a more unique password.');
  }

  if (policy.preventUserInfoInPassword && userInfo) {
    const lowerPassword = password.toLowerCase();
    if (userInfo.email) {
      const emailLocal = userInfo.email.split('@')[0].toLowerCase();
      if (emailLocal.length > 3 && lowerPassword.includes(emailLocal)) {
        errors.push('Password must not contain your email address');
      }
    }
    if (userInfo.fullName) {
      const nameParts = userInfo.fullName.toLowerCase().split(/\s+/);
      for (const part of nameParts) {
        if (part.length > 2 && lowerPassword.includes(part)) {
          errors.push('Password must not contain your name');
          break;
        }
      }
    }
  }

  return { valid: errors.length === 0, errors };
}
```

**Step 2:** Update `app/api/auth/signup/route.ts` to use the policy:

```typescript
// File: app/api/auth/signup/route.ts
// Replace the simple password length check with:

import { validatePassword } from '@/lib/password-policy';

// Inside POST handler, replace: if (!password || password.length < 8) { ... }
const passwordValidation = validatePassword(password, undefined, { email, fullName: full_name });
if (!passwordValidation.valid) {
  return NextResponse.json(
    { error: 'Password does not meet requirements', details: passwordValidation.errors },
    { status: 400 }
  );
}
```

---

### 0.6 S3 Server-Side Encryption

**Gap Reference:** missingfeatures.md §6.2
**Compliance:** SOC 2 CC6.7, HIPAA 164.312(a)(2)(iv), PCI DSS 3.4
**File:** `lib/s3.ts`

**Step 1:** Update the `uploadFileToS3` function to enforce SSE-KMS:

```typescript
// File: lib/s3.ts
// In the uploadFileToS3 function, update the PutObjectCommand:

const command = new PutObjectCommand({
  Bucket: getS3BucketName(),
  Key: s3Key,
  Body: fileBuffer,
  ContentType: contentType,
  // Enforce server-side encryption with AWS KMS
  ServerSideEncryption: 'aws:kms',
  SSEKMSKeyId: process.env.S3_KMS_KEY_ID || undefined,  // Uses default aws/s3 key if not set
});
```

**Step 2:** Add the KMS key ID to `.env.example`:

```env
# S3 Encryption (optional: uses default aws/s3 KMS key if not set)
S3_KMS_KEY_ID=""
```

**Step 3:** Additionally, enforce a bucket policy requiring encryption. Create a setup script:

```typescript
// File: scripts/enforce-s3-encryption.ts
// Run once during infrastructure setup

import { S3Client, PutBucketEncryptionCommand } from '@aws-sdk/client-s3';

async function enforceEncryption() {
  const client = new S3Client({ region: process.env.AWS_REGION });

  await client.send(new PutBucketEncryptionCommand({
    Bucket: process.env.S3_BUCKET_NAME!,
    ServerSideEncryptionConfiguration: {
      Rules: [{
        ApplyServerSideEncryptionByDefault: {
          SSEAlgorithm: 'aws:kms',
          KMSMasterKeyID: process.env.S3_KMS_KEY_ID || undefined,
        },
        BucketKeyEnabled: true, // Reduces KMS API costs
      }],
    },
  }));

  console.log('S3 bucket encryption enforced successfully');
}

enforceEncryption().catch(console.error);
```

---

### 0.7 Content Security Policy Header

**Gap Reference:** missingfeatures.md §14.7
**Compliance:** OWASP Top 10, SOC 2 CC6.6
**File:** `next.config.ts`

**Step 1:** Add CSP to the existing headers configuration:

```typescript
// File: next.config.ts
// Add to the headers array inside the existing headers() function:

{
  key: 'Content-Security-Policy',
  value: [
    "default-src 'self'",
    "script-src 'self' 'unsafe-eval' 'unsafe-inline'",  // Next.js requires these; tighten with nonce in Phase 3
    "style-src 'self' 'unsafe-inline'",  // Tailwind requires inline styles
    "img-src 'self' data: blob: https://quicktrustapp.com https://trust.quickintell.com",
    "font-src 'self'",
    "connect-src 'self' https://api.openai.com",  // For LLM calls
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "upgrade-insecure-requests",
  ].join('; '),
},
```

---

### 0.8 Database Connection TLS

**Gap Reference:** missingfeatures.md §6.3
**Compliance:** SOC 2 CC6.7, PCI DSS 4.1, HIPAA 164.312(e)(1)

**Step 1:** Update the `DATABASE_URL` format in `.env.example` to enforce TLS:

```env
# Production database URL should include SSL:
DATABASE_URL="postgresql://user:password@host:5432/quicktrust?schema=public&sslmode=require&sslcert=/path/to/ca-certificate.crt"
```

**Step 2:** For AWS RDS, the connection string should use:

```env
DATABASE_URL="postgresql://user:password@your-rds-endpoint:5432/quicktrust?schema=public&sslmode=verify-full&sslrootcert=/app/rds-combined-ca-bundle.pem"
```

**Step 3:** Update the Dockerfile to include the RDS CA bundle:

```dockerfile
# File: Dockerfile
# Add after the FROM base image line in the runner stage:
RUN apk add --no-cache wget && \
    wget -O /app/rds-combined-ca-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

---

## Phase 1: Identity & Access Management (Weeks 3-6)

---

### 1.1 Granular RBAC Permission System

**Gap Reference:** missingfeatures.md §4.1, §4.2, §4.3
**Compliance:** SOC 2 CC6.1, ISO 27001 A.5.15, PCI DSS 7.1, HIPAA 164.312(a)(1)

**Step 1:** Extend the Prisma schema with a full permission model.

```prisma
// File: prisma/schema.prisma

// Replace the simple UserRole enum with a granular system:

enum UserRole {
  SUPER_ADMIN    // Platform-level admin
  OWNER          // Organization owner
  ADMIN          // Organization admin
  MANAGER        // Can approve, manage users
  ANALYST        // Can create/edit content
  VIEWER         // Read-only access
  AUDITOR        // External auditor (read-only + evidence access)
}

// Define available permissions
model Permission {
  id          Int              @id @default(autoincrement())
  resource    String           // e.g., "policies", "evidence", "questions", "users", "settings"
  action      String           // e.g., "create", "read", "update", "delete", "approve", "export"
  description String?
  roles       RolePermission[]

  @@unique([resource, action])
  @@map("permissions")
}

// Map roles to permissions
model RolePermission {
  id           Int        @id @default(autoincrement())
  role         UserRole
  permissionId Int        @map("permission_id")
  permission   Permission @relation(fields: [permissionId], references: [id], onDelete: Cascade)

  @@unique([role, permissionId])
  @@map("role_permissions")
}

// Per-user permission overrides (grant/deny beyond role defaults)
model UserPermissionOverride {
  id           Int        @id @default(autoincrement())
  userId       Int        @map("user_id")
  permissionId Int        @map("permission_id")
  granted      Boolean    // true = grant, false = deny
  grantedBy    Int        @map("granted_by")
  grantedAt    DateTime   @default(now()) @map("granted_at")
  expiresAt    DateTime?  @map("expires_at")   // Time-bound permissions (PAM)

  @@unique([userId, permissionId])
  @@map("user_permission_overrides")
}
```

**Step 2:** Run the migration.

```bash
npx prisma migrate dev --name add-rbac-permission-model
```

**Step 3:** Create a seed script for default role-permission mappings.

```typescript
// File: prisma/seeds/seed-permissions.ts

import { PrismaClient, UserRole } from '@prisma/client';

const prisma = new PrismaClient();

const PERMISSIONS = [
  // Policies
  { resource: 'policies', action: 'create', description: 'Upload new policies' },
  { resource: 'policies', action: 'read', description: 'View policies' },
  { resource: 'policies', action: 'update', description: 'Edit policies' },
  { resource: 'policies', action: 'delete', description: 'Delete policies' },
  { resource: 'policies', action: 'approve', description: 'Approve policy versions' },
  // Evidence
  { resource: 'evidence', action: 'create', description: 'Upload evidence' },
  { resource: 'evidence', action: 'read', description: 'View evidence' },
  { resource: 'evidence', action: 'update', description: 'Edit evidence' },
  { resource: 'evidence', action: 'delete', description: 'Delete evidence' },
  { resource: 'evidence', action: 'approve', description: 'Approve evidence' },
  // Questions
  { resource: 'questions', action: 'create', description: 'Ask questions' },
  { resource: 'questions', action: 'read', description: 'View questions' },
  { resource: 'questions', action: 'update', description: 'Edit questions' },
  { resource: 'questions', action: 'approve', description: 'Accept/reject answers' },
  // Users
  { resource: 'users', action: 'create', description: 'Invite users' },
  { resource: 'users', action: 'read', description: 'View user list' },
  { resource: 'users', action: 'update', description: 'Edit user profiles/roles' },
  { resource: 'users', action: 'delete', description: 'Remove users' },
  // Settings
  { resource: 'settings', action: 'read', description: 'View org settings' },
  { resource: 'settings', action: 'update', description: 'Modify org settings' },
  // Reports
  { resource: 'reports', action: 'read', description: 'View reports' },
  { resource: 'reports', action: 'export', description: 'Export data' },
];

// Role hierarchy: each role inherits all permissions of roles below it
const ROLE_PERMISSIONS: Record<UserRole, { resource: string; action: string }[]> = {
  SUPER_ADMIN: PERMISSIONS.map(p => ({ resource: p.resource, action: p.action })),
  OWNER: PERMISSIONS.map(p => ({ resource: p.resource, action: p.action })),
  ADMIN: PERMISSIONS.filter(p =>
    !(p.resource === 'settings' && p.action === 'update') // Admins can't change billing
  ).map(p => ({ resource: p.resource, action: p.action })),
  MANAGER: PERMISSIONS.filter(p =>
    !['delete'].includes(p.action) || p.resource === 'evidence'
  ).filter(p =>
    !(p.resource === 'users' && ['create', 'delete'].includes(p.action))
  ).map(p => ({ resource: p.resource, action: p.action })),
  ANALYST: PERMISSIONS.filter(p =>
    ['create', 'read', 'update'].includes(p.action) &&
    ['policies', 'evidence', 'questions'].includes(p.resource)
  ).map(p => ({ resource: p.resource, action: p.action })),
  VIEWER: PERMISSIONS.filter(p =>
    p.action === 'read'
  ).map(p => ({ resource: p.resource, action: p.action })),
  AUDITOR: PERMISSIONS.filter(p =>
    p.action === 'read' || (p.resource === 'reports' && p.action === 'export')
  ).map(p => ({ resource: p.resource, action: p.action })),
};

async function seedPermissions() {
  // Create all permissions
  for (const perm of PERMISSIONS) {
    await prisma.permission.upsert({
      where: { resource_action: { resource: perm.resource, action: perm.action } },
      create: perm,
      update: perm,
    });
  }

  // Create role-permission mappings
  for (const [role, perms] of Object.entries(ROLE_PERMISSIONS)) {
    for (const perm of perms) {
      const permission = await prisma.permission.findUnique({
        where: { resource_action: { resource: perm.resource, action: perm.action } },
      });
      if (permission) {
        await prisma.rolePermission.upsert({
          where: { role_permissionId: { role: role as UserRole, permissionId: permission.id } },
          create: { role: role as UserRole, permissionId: permission.id },
          update: {},
        });
      }
    }
  }

  console.log('Permissions seeded successfully');
}

seedPermissions().catch(console.error).finally(() => prisma.$disconnect());
```

**Step 4:** Create the authorization checking library.

```typescript
// File: lib/authorization.ts

import { prisma } from './db';
import { UserRole } from '@prisma/client';

/**
 * Check if a user has a specific permission, considering:
 * 1. Role-based default permissions
 * 2. User-specific overrides (grants/denials)
 * 3. Time-bound permission expiry
 */
export async function hasPermission(
  userId: number,
  resource: string,
  action: string
): Promise<boolean> {
  // 1. Check user-specific overrides first (they take precedence)
  const override = await prisma.userPermissionOverride.findFirst({
    where: {
      userId,
      permission: { resource, action },
      OR: [
        { expiresAt: null },
        { expiresAt: { gt: new Date() } },
      ],
    },
  });

  if (override) return override.granted;

  // 2. Fall back to role-based permissions
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { role: true },
  });

  if (!user) return false;

  const rolePermission = await prisma.rolePermission.findFirst({
    where: {
      role: user.role,
      permission: { resource, action },
    },
  });

  return !!rolePermission;
}

/**
 * Require permission or return 403 response.
 * Use in route handlers:
 *
 *   const authCheck = await requirePermission(user.userId, 'policies', 'create');
 *   if (authCheck) return authCheck; // Returns 403 response if denied
 */
export async function requirePermission(
  userId: number,
  resource: string,
  action: string
): Promise<Response | null> {
  const allowed = await hasPermission(userId, resource, action);
  if (!allowed) {
    return Response.json(
      { error: `Insufficient permissions: ${action} on ${resource}` },
      { status: 403 }
    );
  }
  return null;
}
```

**Step 5:** Update the `apiGuard` to include permission checks:

```typescript
// File: lib/api-guard.ts
// Add to GuardOptions:

interface GuardOptions {
  rateLimit?: keyof typeof RATE_LIMITS | RateLimitConfig;
  requireAuth?: boolean;
  requireOrg?: boolean;
  requirePermission?: { resource: string; action: string };
}

// Add after the org check in apiGuard:
if (options.requirePermission) {
  const { resource, action } = options.requirePermission;
  const allowed = await hasPermission(user.id, resource, action);
  if (!allowed) {
    return {
      allowed: false,
      response: NextResponse.json(
        { error: `Insufficient permissions: ${action} on ${resource}` },
        { status: 403 }
      ),
    };
  }
}
```

**Step 6:** Retrofit existing routes with permission checks. Example:

```typescript
// File: app/api/policies/upload/route.ts
export async function POST(request: Request) {
  const guard = await apiGuard(request, {
    rateLimit: 'upload',
    requireAuth: true,
    requireOrg: true,
    requirePermission: { resource: 'policies', action: 'create' },
  });
  if (!guard.allowed) return guard.response!;
  // ... rest of upload logic ...
}
```

---

### 1.2 TOTP-Based Multi-Factor Authentication

**Gap Reference:** missingfeatures.md §2.1, §2.4, §2.5
**Compliance:** SOC 2 CC6.1, ISO 27001 A.8.5, PCI DSS 8.4.2, HIPAA 164.312(d)
**New Dependencies:** `otpauth`, `qrcode`
**New Files:** `lib/mfa.ts`, `app/api/auth/mfa/*`

**Step 1:** Install dependencies.

```bash
npm install otpauth qrcode
npm install -D @types/qrcode
```

**Step 2:** Add MFA fields to User model.

```prisma
// File: prisma/schema.prisma
// Add to User model:

model User {
  // ... existing fields ...
  mfaSecret           String?   @map("mfa_secret")          // Encrypted TOTP secret
  mfaEnabled          Boolean   @default(false) @map("mfa_enabled")
  mfaBackupCodes      String?   @map("mfa_backup_codes")    // JSON array, encrypted
  mfaVerifiedAt       DateTime? @map("mfa_verified_at")
}

// Add MFA enforcement at org level:
model Organization {
  // ... existing fields ...
  mfaRequired         Boolean   @default(false) @map("mfa_required")
  mfaGracePeriodDays  Int       @default(7) @map("mfa_grace_period_days")
}
```

```bash
npx prisma migrate dev --name add-mfa-fields
```

**Step 3:** Create the MFA library.

```typescript
// File: lib/mfa.ts

import * as OTPAuth from 'otpauth';
import QRCode from 'qrcode';
import crypto from 'crypto';

const MFA_ISSUER = 'QuickTrust';
const BACKUP_CODE_COUNT = 10;

// Encryption for storing MFA secrets at rest
const ENCRYPTION_KEY = process.env.MFA_ENCRYPTION_KEY || '';  // 32-byte hex key
const ALGORITHM = 'aes-256-gcm';

function encrypt(text: string): string {
  if (!ENCRYPTION_KEY) throw new Error('MFA_ENCRYPTION_KEY not configured');
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY, 'hex'), iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag().toString('hex');
  return `${iv.toString('hex')}:${authTag}:${encrypted}`;
}

function decrypt(encryptedText: string): string {
  if (!ENCRYPTION_KEY) throw new Error('MFA_ENCRYPTION_KEY not configured');
  const [ivHex, authTagHex, encrypted] = encryptedText.split(':');
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    Buffer.from(ENCRYPTION_KEY, 'hex'),
    Buffer.from(ivHex, 'hex')
  );
  decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

/**
 * Generate a new TOTP secret and QR code for enrollment.
 */
export async function generateMfaSetup(userEmail: string): Promise<{
  secret: string;           // Encrypted secret to store in DB
  qrCodeDataUrl: string;    // QR code as data URL for frontend
  manualEntryKey: string;   // For manual entry in authenticator app
  backupCodes: string[];    // One-time backup codes
}> {
  const totp = new OTPAuth.TOTP({
    issuer: MFA_ISSUER,
    label: userEmail,
    algorithm: 'SHA1',
    digits: 6,
    period: 30,
    secret: new OTPAuth.Secret({ size: 20 }),
  });

  const uri = totp.toString();
  const qrCodeDataUrl = await QRCode.toDataURL(uri);

  // Generate backup codes
  const backupCodes = Array.from({ length: BACKUP_CODE_COUNT }, () =>
    crypto.randomBytes(4).toString('hex').toUpperCase()
  );

  return {
    secret: encrypt(totp.secret.base32),
    qrCodeDataUrl,
    manualEntryKey: totp.secret.base32,
    backupCodes,
  };
}

/**
 * Verify a TOTP code.
 */
export function verifyMfaCode(encryptedSecret: string, code: string): boolean {
  const secretBase32 = decrypt(encryptedSecret);

  const totp = new OTPAuth.TOTP({
    issuer: MFA_ISSUER,
    algorithm: 'SHA1',
    digits: 6,
    period: 30,
    secret: OTPAuth.Secret.fromBase32(secretBase32),
  });

  // Allow 1 period window (30 seconds before/after) for clock skew
  const delta = totp.validate({ token: code, window: 1 });
  return delta !== null;
}

/**
 * Verify a backup code (single-use).
 */
export function verifyBackupCode(
  encryptedBackupCodes: string,
  code: string
): { valid: boolean; remainingCodes: string } {
  const codesJson = decrypt(encryptedBackupCodes);
  const codes: string[] = JSON.parse(codesJson);

  const normalizedCode = code.toUpperCase().replace(/\s/g, '');
  const index = codes.indexOf(normalizedCode);

  if (index === -1) {
    return { valid: false, remainingCodes: encryptedBackupCodes };
  }

  // Remove the used code
  codes.splice(index, 1);
  return {
    valid: true,
    remainingCodes: encrypt(JSON.stringify(codes)),
  };
}

export { encrypt as encryptMfaData, decrypt as decryptMfaData };
```

**Step 4:** Create MFA API endpoints.

```typescript
// File: app/api/auth/mfa/setup/route.ts
// POST: Initiate MFA enrollment

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { generateMfaSetup, encryptMfaData } from '@/lib/mfa';
import { prisma } from '@/lib/db';

export async function POST(request: Request) {
  const guard = await apiGuard(request, { requireAuth: true, rateLimit: 'api' });
  if (!guard.allowed) return guard.response!;

  const user = guard.user!;

  // Generate new MFA setup
  const setup = await generateMfaSetup(user.email);

  // Store the secret temporarily (not yet verified)
  await prisma.user.update({
    where: { id: user.userId },
    data: {
      mfaSecret: setup.secret,
      mfaEnabled: false,  // Not enabled until verified
    },
  });

  return NextResponse.json({
    qrCode: setup.qrCodeDataUrl,
    manualEntryKey: setup.manualEntryKey,
    backupCodes: setup.backupCodes,
    message: 'Scan the QR code with your authenticator app, then verify with a code.',
  });
}
```

```typescript
// File: app/api/auth/mfa/verify/route.ts
// POST: Verify MFA code and enable MFA

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { verifyMfaCode, encryptMfaData } from '@/lib/mfa';
import { prisma } from '@/lib/db';

export async function POST(request: Request) {
  const guard = await apiGuard(request, { requireAuth: true, rateLimit: 'auth' });
  if (!guard.allowed) return guard.response!;

  const { code, backupCodes } = await request.json();

  if (!code || typeof code !== 'string' || code.length !== 6) {
    return NextResponse.json({ error: 'Invalid MFA code format' }, { status: 400 });
  }

  const user = await prisma.user.findUnique({
    where: { id: guard.user!.userId },
    select: { mfaSecret: true, mfaEnabled: true },
  });

  if (!user?.mfaSecret) {
    return NextResponse.json({ error: 'MFA setup not initiated' }, { status: 400 });
  }

  if (user.mfaEnabled) {
    return NextResponse.json({ error: 'MFA is already enabled' }, { status: 400 });
  }

  const isValid = verifyMfaCode(user.mfaSecret, code);
  if (!isValid) {
    return NextResponse.json({ error: 'Invalid MFA code. Please try again.' }, { status: 401 });
  }

  // Enable MFA and store encrypted backup codes
  await prisma.user.update({
    where: { id: guard.user!.userId },
    data: {
      mfaEnabled: true,
      mfaVerifiedAt: new Date(),
      mfaBackupCodes: backupCodes ? encryptMfaData(JSON.stringify(backupCodes)) : null,
    },
  });

  return NextResponse.json({ message: 'MFA enabled successfully' });
}
```

**Step 5:** Update the login flow to support MFA challenge.

```typescript
// File: app/api/auth/login/route.ts
// After successful password verification but BEFORE issuing the token:

// Check if user has MFA enabled
const fullUser = await prisma.user.findUnique({
  where: { id: result.user.id },
  select: { mfaEnabled: true },
});

if (fullUser?.mfaEnabled) {
  // Issue a short-lived "mfa-pending" token instead of the full auth token
  const mfaPendingToken = jwt.sign(
    { userId: result.user.id, purpose: 'mfa-challenge' },
    JWT_SECRET,
    { expiresIn: '5m' }  // 5 minutes to complete MFA
  );

  return NextResponse.json({
    mfaRequired: true,
    mfaToken: mfaPendingToken,
    message: 'MFA verification required',
  }, { status: 200 });
}

// If no MFA, issue the full token as before
// ... existing token generation and cookie setting ...
```

```typescript
// File: app/api/auth/mfa/challenge/route.ts
// POST: Validate MFA code during login

import { NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';
import { verifyMfaCode, verifyBackupCode } from '@/lib/mfa';
import { prisma } from '@/lib/db';
import { generateToken } from '@/lib/jwt';

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

export async function POST(request: Request) {
  const { mfaToken, code, useBackupCode } = await request.json();

  if (!mfaToken || !code) {
    return NextResponse.json({ error: 'MFA token and code required' }, { status: 400 });
  }

  // Verify the MFA pending token
  let decoded: { userId: number; purpose: string };
  try {
    decoded = jwt.verify(mfaToken, JWT_SECRET) as typeof decoded;
    if (decoded.purpose !== 'mfa-challenge') {
      return NextResponse.json({ error: 'Invalid MFA token' }, { status: 401 });
    }
  } catch {
    return NextResponse.json({ error: 'MFA token expired. Please login again.' }, { status: 401 });
  }

  const user = await prisma.user.findUnique({
    where: { id: decoded.userId },
    select: {
      id: true, email: true, fullName: true, orgId: true, role: true,
      mfaSecret: true, mfaBackupCodes: true, createdAt: true, lastLogin: true,
    },
  });

  if (!user?.mfaSecret) {
    return NextResponse.json({ error: 'MFA not configured' }, { status: 400 });
  }

  let isValid = false;

  if (useBackupCode && user.mfaBackupCodes) {
    const result = verifyBackupCode(user.mfaBackupCodes, code);
    isValid = result.valid;
    if (isValid) {
      // Update remaining backup codes
      await prisma.user.update({
        where: { id: user.id },
        data: { mfaBackupCodes: result.remainingCodes },
      });
    }
  } else {
    isValid = verifyMfaCode(user.mfaSecret, code);
  }

  if (!isValid) {
    return NextResponse.json({ error: 'Invalid MFA code' }, { status: 401 });
  }

  // MFA verified -- issue full auth token
  const token = generateToken({
    userId: user.id,
    email: user.email,
    fullName: user.fullName || undefined,
  });

  // Update last login
  await prisma.user.update({
    where: { id: user.id },
    data: { lastLogin: new Date() },
  });

  const response = NextResponse.json({
    message: 'Login successful',
    user: {
      id: user.id, email: user.email, full_name: user.fullName,
      org_id: user.orgId, role: user.role,
    },
    token,
  });

  response.cookies.set('auth_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 86400,
  });

  return response;
}
```

**Step 6:** Add `MFA_ENCRYPTION_KEY` to `.env.example`:

```env
# MFA Encryption (generate with: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
MFA_ENCRYPTION_KEY=""
```

---

### 1.3 User Lifecycle Management

**Gap Reference:** missingfeatures.md §1.3, §1.4
**Compliance:** SOC 2 CC6.2, CC6.3, ISO 27001 A.5.18

**Step 1:** Add lifecycle fields to the User model.

```prisma
// File: prisma/schema.prisma

enum UserStatus {
  PENDING     // Invited, not yet registered
  ACTIVE      // Normal active user
  SUSPENDED   // Temporarily disabled
  DEACTIVATED // Permanently disabled, pending deletion
}

model User {
  // ... existing fields ...
  status              UserStatus @default(ACTIVE)
  suspendedAt         DateTime?  @map("suspended_at")
  suspendedBy         Int?       @map("suspended_by")
  suspendedReason     String?    @map("suspended_reason")
  deactivatedAt       DateTime?  @map("deactivated_at")
  deactivatedBy       Int?       @map("deactivated_by")
  lastActivityAt      DateTime?  @map("last_activity_at")
}
```

```bash
npx prisma migrate dev --name add-user-lifecycle-fields
```

**Step 2:** Create user management API endpoints.

```typescript
// File: app/api/users/route.ts

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { prisma } from '@/lib/db';

// GET: List users in the organization
export async function GET(request: Request) {
  const guard = await apiGuard(request, {
    requireAuth: true,
    requireOrg: true,
    requirePermission: { resource: 'users', action: 'read' },
  });
  if (!guard.allowed) return guard.response!;

  const users = await prisma.user.findMany({
    where: { orgId: guard.user!.orgId },
    select: {
      id: true, email: true, fullName: true, role: true,
      status: true, createdAt: true, lastLogin: true, lastActivityAt: true,
      mfaEnabled: true,
    },
    orderBy: { createdAt: 'desc' },
  });

  return NextResponse.json({ users });
}
```

```typescript
// File: app/api/users/[id]/status/route.ts

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { prisma } from '@/lib/db';
import { revokeAllUserTokens } from '@/lib/token-blacklist';

// PATCH: Suspend, activate, or deactivate a user
export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  const guard = await apiGuard(request, {
    requireAuth: true,
    requireOrg: true,
    requirePermission: { resource: 'users', action: 'update' },
  });
  if (!guard.allowed) return guard.response!;

  const targetUserId = parseInt(params.id);
  const { action, reason } = await request.json();

  // Prevent self-deactivation
  if (targetUserId === guard.user!.userId && ['suspend', 'deactivate'].includes(action)) {
    return NextResponse.json({ error: 'Cannot modify your own account status' }, { status: 400 });
  }

  // Verify target user is in same org
  const targetUser = await prisma.user.findFirst({
    where: { id: targetUserId, orgId: guard.user!.orgId },
  });

  if (!targetUser) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 });
  }

  let updateData: any = {};

  switch (action) {
    case 'suspend':
      updateData = {
        status: 'SUSPENDED',
        suspendedAt: new Date(),
        suspendedBy: guard.user!.userId,
        suspendedReason: reason || 'Suspended by administrator',
      };
      // Immediately revoke all active sessions
      await revokeAllUserTokens(targetUserId);
      break;

    case 'activate':
      updateData = {
        status: 'ACTIVE',
        suspendedAt: null,
        suspendedBy: null,
        suspendedReason: null,
      };
      break;

    case 'deactivate':
      updateData = {
        status: 'DEACTIVATED',
        deactivatedAt: new Date(),
        deactivatedBy: guard.user!.userId,
      };
      await revokeAllUserTokens(targetUserId);
      break;

    default:
      return NextResponse.json({ error: 'Invalid action. Use: suspend, activate, deactivate' }, { status: 400 });
  }

  const updated = await prisma.user.update({
    where: { id: targetUserId },
    data: updateData,
    select: { id: true, email: true, status: true },
  });

  return NextResponse.json({ user: updated, message: `User ${action}d successfully` });
}
```

**Step 3:** Add status check to the authentication flow. In `lib/auth.ts`, after finding the user:

```typescript
// In authenticateUser, after finding the user:
if (user.status === 'SUSPENDED') {
  return { error: 'Your account has been suspended. Contact your administrator.' };
}
if (user.status === 'DEACTIVATED') {
  return { error: 'Your account has been deactivated.' };
}
```

---

### 1.4 Session Management with Server-Side Store

**Gap Reference:** missingfeatures.md §3.1, §3.2, §3.4, §3.5
**Compliance:** SOC 2 CC6.1, PCI DSS 8.2.8, HIPAA 164.312(a)(2)(iii)

**Step 1:** Extend the existing Session model:

```prisma
// File: prisma/schema.prisma
// Replace the existing Session model:

model Session {
  id            Int       @id @default(autoincrement())
  userId        Int       @map("user_id")
  sessionToken  String    @unique @map("session_token")
  refreshToken  String?   @unique @map("refresh_token")
  createdAt     DateTime  @default(now()) @map("created_at")
  expiresAt     DateTime  @map("expires_at")
  lastActiveAt  DateTime  @default(now()) @map("last_active_at")
  ipAddress     String?   @map("ip_address")
  userAgent     String?   @map("user_agent")
  deviceInfo    String?   @map("device_info")
  isRevoked     Boolean   @default(false) @map("is_revoked")
  revokedAt     DateTime? @map("revoked_at")
  revokedReason String?   @map("revoked_reason")
  user          User      @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([expiresAt])
  @@map("sessions")
}
```

**Step 2:** Create the session management library.

```typescript
// File: lib/session-manager.ts

import { prisma } from './db';
import { generateToken } from './jwt';
import crypto from 'crypto';

const MAX_CONCURRENT_SESSIONS = parseInt(process.env.MAX_SESSIONS || '5');
const SESSION_IDLE_TIMEOUT_MS = parseInt(process.env.SESSION_IDLE_TIMEOUT_MS || '900000'); // 15 min
const SESSION_ABSOLUTE_TIMEOUT_MS = parseInt(process.env.SESSION_ABSOLUTE_TIMEOUT_MS || '28800000'); // 8h
const REFRESH_TOKEN_LIFETIME_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

/**
 * Create a new session, enforcing concurrent session limits.
 */
export async function createSession(
  userId: number,
  email: string,
  fullName: string | undefined,
  ipAddress: string,
  userAgent: string
): Promise<{ accessToken: string; refreshToken: string; sessionId: number }> {
  // Enforce concurrent session limit: revoke oldest sessions
  const activeSessions = await prisma.session.findMany({
    where: { userId, isRevoked: false, expiresAt: { gt: new Date() } },
    orderBy: { createdAt: 'asc' },
  });

  if (activeSessions.length >= MAX_CONCURRENT_SESSIONS) {
    const sessionsToRevoke = activeSessions.slice(0, activeSessions.length - MAX_CONCURRENT_SESSIONS + 1);
    await prisma.session.updateMany({
      where: { id: { in: sessionsToRevoke.map(s => s.id) } },
      data: { isRevoked: true, revokedAt: new Date(), revokedReason: 'concurrent_session_limit' },
    });
  }

  const accessToken = generateToken({ userId, email, fullName });
  const refreshToken = crypto.randomBytes(48).toString('hex');

  const session = await prisma.session.create({
    data: {
      userId,
      sessionToken: accessToken,
      refreshToken,
      expiresAt: new Date(Date.now() + SESSION_ABSOLUTE_TIMEOUT_MS),
      ipAddress,
      userAgent: userAgent.substring(0, 500), // Truncate long user agents
    },
  });

  return { accessToken, refreshToken, sessionId: session.id };
}

/**
 * Refresh a session using a refresh token. Rotates both tokens.
 */
export async function refreshSession(
  refreshToken: string,
  ipAddress: string
): Promise<{ accessToken: string; refreshToken: string } | null> {
  const session = await prisma.session.findUnique({
    where: { refreshToken },
    include: { user: { select: { id: true, email: true, fullName: true, status: true } } },
  });

  if (!session || session.isRevoked || session.expiresAt < new Date()) {
    // If refresh token was already used (replay attack), revoke ALL user sessions
    if (session && session.isRevoked) {
      await prisma.session.updateMany({
        where: { userId: session.userId },
        data: { isRevoked: true, revokedAt: new Date(), revokedReason: 'refresh_token_replay' },
      });
    }
    return null;
  }

  if (session.user.status !== 'ACTIVE') {
    return null;
  }

  // Check idle timeout
  const idleTime = Date.now() - session.lastActiveAt.getTime();
  if (idleTime > SESSION_IDLE_TIMEOUT_MS) {
    await prisma.session.update({
      where: { id: session.id },
      data: { isRevoked: true, revokedAt: new Date(), revokedReason: 'idle_timeout' },
    });
    return null;
  }

  // Rotate tokens
  const newAccessToken = generateToken({
    userId: session.user.id,
    email: session.user.email,
    fullName: session.user.fullName || undefined,
  });
  const newRefreshToken = crypto.randomBytes(48).toString('hex');

  await prisma.session.update({
    where: { id: session.id },
    data: {
      sessionToken: newAccessToken,
      refreshToken: newRefreshToken,
      lastActiveAt: new Date(),
      ipAddress,
    },
  });

  return { accessToken: newAccessToken, refreshToken: newRefreshToken };
}

/**
 * List active sessions for a user.
 */
export async function listUserSessions(userId: number) {
  return prisma.session.findMany({
    where: { userId, isRevoked: false, expiresAt: { gt: new Date() } },
    select: {
      id: true, createdAt: true, lastActiveAt: true,
      ipAddress: true, userAgent: true, deviceInfo: true,
    },
    orderBy: { lastActiveAt: 'desc' },
  });
}

/**
 * Revoke a specific session.
 */
export async function revokeSession(sessionId: number, reason: string = 'user_logout') {
  await prisma.session.update({
    where: { id: sessionId },
    data: { isRevoked: true, revokedAt: new Date(), revokedReason: reason },
  });
}

/**
 * Revoke all sessions for a user.
 */
export async function revokeAllSessions(userId: number, reason: string = 'force_logout') {
  await prisma.session.updateMany({
    where: { userId, isRevoked: false },
    data: { isRevoked: true, revokedAt: new Date(), revokedReason: reason },
  });
}
```

**Step 3:** Create a token refresh endpoint:

```typescript
// File: app/api/auth/refresh/route.ts

import { NextResponse } from 'next/server';
import { refreshSession } from '@/lib/session-manager';
import { getClientIp } from '@/lib/rate-limiter';

export async function POST(request: Request) {
  const { refreshToken } = await request.json();

  if (!refreshToken) {
    return NextResponse.json({ error: 'Refresh token required' }, { status: 400 });
  }

  const result = await refreshSession(refreshToken, getClientIp(request));

  if (!result) {
    return NextResponse.json({ error: 'Invalid or expired refresh token. Please login again.' }, { status: 401 });
  }

  const response = NextResponse.json({
    token: result.accessToken,
    refreshToken: result.refreshToken,
  });

  response.cookies.set('auth_token', result.accessToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 900, // 15 minutes (short-lived access token)
  });

  return response;
}
```

---

## Phase 2: Data Protection & Encryption (Weeks 7-10)

---

### 2.1 Field-Level Encryption for PII

**Gap Reference:** missingfeatures.md §6.1, §6.7
**Compliance:** SOC 2 CC6.7, HIPAA 164.312(a)(2)(iv), PCI DSS 3.4
**New File:** `lib/field-encryption.ts`

**Step 1:** Create the field encryption library using envelope encryption with AWS KMS.

```typescript
// File: lib/field-encryption.ts

import crypto from 'crypto';

const FIELD_ENCRYPTION_KEY = process.env.FIELD_ENCRYPTION_KEY || '';
const ALGORITHM = 'aes-256-gcm';

export function encryptField(plaintext: string): string {
  if (!FIELD_ENCRYPTION_KEY) {
    console.warn('[FieldEncryption] No encryption key configured, storing plaintext');
    return plaintext;
  }

  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(
    ALGORITHM,
    Buffer.from(FIELD_ENCRYPTION_KEY, 'hex'),
    iv
  );
  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag().toString('hex');

  // Prefix with 'enc:' to identify encrypted values
  return `enc:${iv.toString('hex')}:${authTag}:${encrypted}`;
}

export function decryptField(ciphertext: string): string {
  if (!ciphertext.startsWith('enc:')) {
    return ciphertext; // Not encrypted (legacy data)
  }

  if (!FIELD_ENCRYPTION_KEY) {
    throw new Error('FIELD_ENCRYPTION_KEY required to decrypt data');
  }

  const parts = ciphertext.slice(4).split(':');
  if (parts.length !== 3) throw new Error('Invalid encrypted field format');

  const [ivHex, authTagHex, encrypted] = parts;
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    Buffer.from(FIELD_ENCRYPTION_KEY, 'hex'),
    Buffer.from(ivHex, 'hex')
  );
  decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

/**
 * Encrypt sensitive fields in an object before database storage.
 */
export function encryptSensitiveFields<T extends Record<string, any>>(
  data: T,
  sensitiveFields: (keyof T)[]
): T {
  const result = { ...data };
  for (const field of sensitiveFields) {
    if (result[field] && typeof result[field] === 'string') {
      result[field] = encryptField(result[field] as string) as any;
    }
  }
  return result;
}

/**
 * Decrypt sensitive fields in an object after database retrieval.
 */
export function decryptSensitiveFields<T extends Record<string, any>>(
  data: T,
  sensitiveFields: (keyof T)[]
): T {
  const result = { ...data };
  for (const field of sensitiveFields) {
    if (result[field] && typeof result[field] === 'string') {
      result[field] = decryptField(result[field] as string) as any;
    }
  }
  return result;
}
```

**Step 2:** Add `FIELD_ENCRYPTION_KEY` to `.env.example`:

```env
# Field-Level Encryption (generate: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
FIELD_ENCRYPTION_KEY=""
```

**Step 3:** Apply encryption to user PII in the signup flow:

```typescript
// In lib/auth.ts createUser function, before creating the user:
import { encryptField } from './field-encryption';

// Encrypt PII fields
const encryptedEmail = encryptField(emailLower);
const encryptedFullName = fullName ? encryptField(fullName.trim()) : null;

// Store encrypted in DB. Note: email needs a searchable hash for lookups.
```

**Important Consideration:** Encrypting the `email` field directly breaks `findUnique({ where: { email } })`. The standard approach is to store a blind index (HMAC hash) alongside the encrypted value:

```prisma
// Add to User model:
model User {
  // ... existing fields ...
  emailHash   String?   @unique @map("email_hash") // HMAC-SHA256 for lookup
  // email field becomes the encrypted value
}
```

```typescript
// Create blind index for searching:
import crypto from 'crypto';
const HMAC_KEY = process.env.FIELD_HMAC_KEY || '';

export function createBlindIndex(value: string): string {
  return crypto.createHmac('sha256', HMAC_KEY).update(value.toLowerCase().trim()).digest('hex');
}

// At signup:
const emailHash = createBlindIndex(email);

// At login (to find user):
const user = await prisma.user.findUnique({
  where: { emailHash: createBlindIndex(email) },
});
```

---

### 2.2 Soft Delete Implementation

**Gap Reference:** missingfeatures.md §8.2
**Compliance:** SOC 2 CC6.5, ISO 27001 A.5.33

**Step 1:** Add soft delete fields to all relevant models. Create a Prisma middleware approach:

```prisma
// File: prisma/schema.prisma
// Add to EVERY model that currently uses onDelete: Cascade

// Add these fields to: User, Organization, PolicyDocument, Evidence, Question, Answer, Comment

model PolicyDocument {
  // ... existing fields ...
  deletedAt    DateTime? @map("deleted_at")
  deletedBy    Int?      @map("deleted_by")
  isDeleted    Boolean   @default(false) @map("is_deleted")
}

// Repeat for Evidence, Question, Answer, Comment, etc.
```

**Step 2:** Create Prisma middleware for automatic soft delete filtering:

```typescript
// File: lib/prisma-middleware.ts

import { PrismaClient } from '@prisma/client';

export function applySoftDeleteMiddleware(prisma: PrismaClient) {
  // Intercept findMany, findFirst, findUnique to exclude soft-deleted records
  prisma.$use(async (params, next) => {
    const softDeleteModels = [
      'PolicyDocument', 'Evidence', 'Question', 'Answer', 'Comment',
    ];

    if (!softDeleteModels.includes(params.model || '')) {
      return next(params);
    }

    // On delete, convert to soft delete
    if (params.action === 'delete') {
      params.action = 'update';
      params.args.data = {
        isDeleted: true,
        deletedAt: new Date(),
      };
      return next(params);
    }

    if (params.action === 'deleteMany') {
      params.action = 'updateMany';
      if (params.args.data) {
        params.args.data.isDeleted = true;
        params.args.data.deletedAt = new Date();
      } else {
        params.args.data = { isDeleted: true, deletedAt: new Date() };
      }
      return next(params);
    }

    // On reads, exclude deleted records unless explicitly requested
    if (['findMany', 'findFirst', 'findUnique', 'count'].includes(params.action)) {
      if (!params.args) params.args = {};
      if (!params.args.where) params.args.where = {};

      // Don't override if caller explicitly includes deleted records
      if (params.args.where.isDeleted === undefined) {
        params.args.where.isDeleted = false;
      }
    }

    return next(params);
  });
}
```

**Step 3:** Apply the middleware in `lib/db.ts`:

```typescript
// File: lib/db.ts
// After creating the PrismaClient instance:

import { applySoftDeleteMiddleware } from './prisma-middleware';

const prisma = new PrismaClient();
applySoftDeleteMiddleware(prisma);
```

---

### 2.3 Data Classification Framework

**Gap Reference:** missingfeatures.md §7.1
**Compliance:** ISO 27001 A.5.12, SOC 2 CC6.7, PCI DSS 3.1

**Step 1:** Add classification enums and fields:

```prisma
// File: prisma/schema.prisma

enum DataClassification {
  PUBLIC
  INTERNAL
  CONFIDENTIAL
  RESTRICTED
}

// Add to PolicyDocument, Evidence models:
model PolicyDocument {
  // ... existing fields ...
  classification  DataClassification @default(CONFIDENTIAL)
}

model Evidence {
  // ... existing fields ...
  classification  DataClassification @default(CONFIDENTIAL)
}
```

**Step 2:** Create classification-aware access control:

```typescript
// File: lib/data-classification.ts

import { DataClassification, UserRole } from '@prisma/client';

// Minimum role required to access each classification level
const CLASSIFICATION_ACCESS: Record<DataClassification, UserRole[]> = {
  PUBLIC: ['SUPER_ADMIN', 'OWNER', 'ADMIN', 'MANAGER', 'ANALYST', 'VIEWER', 'AUDITOR'],
  INTERNAL: ['SUPER_ADMIN', 'OWNER', 'ADMIN', 'MANAGER', 'ANALYST', 'VIEWER', 'AUDITOR'],
  CONFIDENTIAL: ['SUPER_ADMIN', 'OWNER', 'ADMIN', 'MANAGER', 'ANALYST'],
  RESTRICTED: ['SUPER_ADMIN', 'OWNER', 'ADMIN'],
};

export function canAccessClassification(
  userRole: UserRole,
  classification: DataClassification
): boolean {
  return CLASSIFICATION_ACCESS[classification].includes(userRole);
}
```

---

## Phase 3: Audit Logging & Monitoring (Weeks 11-13)

---

### 3.1 Comprehensive Audit Logging System

**Gap Reference:** missingfeatures.md §9.1, §9.2, §9.5
**Compliance:** SOC 2 CC7.2, ISO 27001 A.8.15, PCI DSS 10.2, HIPAA 164.312(b)

**Step 1:** Create a comprehensive audit log model (separate from the existing question-specific AuditTrail):

```prisma
// File: prisma/schema.prisma

model SecurityAuditLog {
  id             Int      @id @default(autoincrement())
  timestamp      DateTime @default(now())
  eventType      String   @map("event_type")       // AUTH_LOGIN, AUTH_LOGOUT, DATA_ACCESS, DATA_MODIFY, etc.
  eventCategory  String   @map("event_category")   // authentication, authorization, data, admin, system
  severity       String   @default("INFO")          // DEBUG, INFO, WARN, ERROR, CRITICAL
  actorId        Int?     @map("actor_id")          // User who performed the action (null for system)
  actorEmail     String?  @map("actor_email")
  actorRole      String?  @map("actor_role")
  actorIp        String?  @map("actor_ip")
  actorUserAgent String?  @map("actor_user_agent")
  orgId          Int?     @map("org_id")
  resource       String?                            // "policy", "evidence", "user", etc.
  resourceId     String?  @map("resource_id")       // ID of the affected resource
  action         String                             // "create", "read", "update", "delete", "login", "logout"
  outcome        String   @default("success")       // "success", "failure", "denied"
  details        Json?                              // Structured JSON with before/after state
  requestId      String?  @map("request_id")        // Correlation ID
  sessionId      String?  @map("session_id")

  @@index([timestamp])
  @@index([actorId])
  @@index([orgId, timestamp])
  @@index([eventType, timestamp])
  @@index([resource, resourceId])
  @@map("security_audit_logs")
}
```

```bash
npx prisma migrate dev --name add-security-audit-log
```

**Step 2:** Create the audit logger library.

```typescript
// File: lib/audit-logger.ts

import { prisma } from './db';

export type EventCategory = 'authentication' | 'authorization' | 'data' | 'admin' | 'system' | 'ai';
export type Severity = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR' | 'CRITICAL';

interface AuditLogEntry {
  eventType: string;
  eventCategory: EventCategory;
  severity?: Severity;
  actorId?: number | null;
  actorEmail?: string;
  actorRole?: string;
  actorIp?: string;
  actorUserAgent?: string;
  orgId?: number | null;
  resource?: string;
  resourceId?: string;
  action: string;
  outcome?: 'success' | 'failure' | 'denied';
  details?: Record<string, any>;
  requestId?: string;
  sessionId?: string;
}

/**
 * Write an audit log entry. Non-blocking -- failures are logged but don't break the request.
 */
export async function auditLog(entry: AuditLogEntry): Promise<void> {
  try {
    // Also write to structured stdout for log aggregation
    const logLine = {
      '@timestamp': new Date().toISOString(),
      level: entry.severity || 'INFO',
      event_type: entry.eventType,
      event_category: entry.eventCategory,
      actor_id: entry.actorId,
      actor_email: entry.actorEmail,
      org_id: entry.orgId,
      resource: entry.resource,
      resource_id: entry.resourceId,
      action: entry.action,
      outcome: entry.outcome || 'success',
      request_id: entry.requestId,
      message: `${entry.eventType}: ${entry.action} on ${entry.resource || 'system'} by ${entry.actorEmail || 'system'}`,
    };

    // Structured log to stdout (picked up by CloudWatch/ELK)
    console.log(JSON.stringify(logLine));

    // Persist to database
    await prisma.securityAuditLog.create({
      data: {
        eventType: entry.eventType,
        eventCategory: entry.eventCategory,
        severity: entry.severity || 'INFO',
        actorId: entry.actorId,
        actorEmail: entry.actorEmail,
        actorRole: entry.actorRole,
        actorIp: entry.actorIp,
        actorUserAgent: entry.actorUserAgent,
        orgId: entry.orgId,
        resource: entry.resource,
        resourceId: entry.resourceId ? String(entry.resourceId) : null,
        action: entry.action,
        outcome: entry.outcome || 'success',
        details: entry.details || undefined,
        requestId: entry.requestId,
        sessionId: entry.sessionId,
      },
    });
  } catch (err) {
    // Never let audit logging failures break the application
    console.error('[AuditLogger] Failed to write audit log:', err);
  }
}

// --- Convenience functions for common events ---

export async function logAuthEvent(
  eventType: 'AUTH_LOGIN' | 'AUTH_LOGOUT' | 'AUTH_FAILED' | 'AUTH_MFA_CHALLENGE' | 'AUTH_MFA_SUCCESS' | 'AUTH_MFA_FAILED' | 'AUTH_LOCKED',
  actorEmail: string,
  outcome: 'success' | 'failure',
  ip: string,
  details?: Record<string, any>
) {
  await auditLog({
    eventType,
    eventCategory: 'authentication',
    severity: outcome === 'failure' ? 'WARN' : 'INFO',
    actorEmail,
    actorIp: ip,
    action: eventType.toLowerCase(),
    outcome,
    details,
  });
}

export async function logDataEvent(
  action: 'create' | 'read' | 'update' | 'delete' | 'export',
  resource: string,
  resourceId: string | number,
  actor: { id: number; email: string; role?: string; orgId?: number | null },
  ip: string,
  details?: Record<string, any>
) {
  await auditLog({
    eventType: `DATA_${action.toUpperCase()}`,
    eventCategory: 'data',
    severity: action === 'delete' ? 'WARN' : 'INFO',
    actorId: actor.id,
    actorEmail: actor.email,
    actorRole: actor.role,
    orgId: actor.orgId,
    resource,
    resourceId: String(resourceId),
    action,
    actorIp: ip,
    details,
  });
}

export async function logAdminEvent(
  action: string,
  actor: { id: number; email: string; role?: string },
  ip: string,
  details?: Record<string, any>
) {
  await auditLog({
    eventType: 'ADMIN_ACTION',
    eventCategory: 'admin',
    severity: 'WARN',
    actorId: actor.id,
    actorEmail: actor.email,
    actorRole: actor.role,
    action,
    actorIp: ip,
    details,
  });
}
```

**Step 3:** Integrate audit logging into existing routes. Example for login:

```typescript
// File: app/api/auth/login/route.ts
// After successful login:

import { logAuthEvent } from '@/lib/audit-logger';
import { getClientIp } from '@/lib/rate-limiter';

// On success:
await logAuthEvent('AUTH_LOGIN', email, 'success', getClientIp(request));

// On failure:
await logAuthEvent('AUTH_FAILED', email, 'failure', getClientIp(request), {
  reason: 'invalid_credentials',
});

// On lockout:
await logAuthEvent('AUTH_LOCKED', email, 'failure', getClientIp(request), {
  failedAttempts: newFailedAttempts,
});
```

Example for evidence creation:

```typescript
// File: app/api/evidence/route.ts
// After creating evidence:

import { logDataEvent } from '@/lib/audit-logger';
import { getClientIp } from '@/lib/rate-limiter';

await logDataEvent('create', 'evidence', evidence.id, {
  id: user.userId, email: user.email, orgId: user.orgId,
}, getClientIp(request), {
  fileName: evidence.name,
  fileType: evidence.fileType,
  size: evidence.size,
});
```

**Step 4:** Create an audit log query endpoint for admin review:

```typescript
// File: app/api/admin/audit-logs/route.ts

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { prisma } from '@/lib/db';

export async function GET(request: Request) {
  const guard = await apiGuard(request, {
    requireAuth: true,
    requireOrg: true,
    requirePermission: { resource: 'settings', action: 'read' },
  });
  if (!guard.allowed) return guard.response!;

  const url = new URL(request.url);
  const page = parseInt(url.searchParams.get('page') || '1');
  const pageSize = Math.min(parseInt(url.searchParams.get('pageSize') || '50'), 100);
  const eventType = url.searchParams.get('eventType') || undefined;
  const actorId = url.searchParams.get('actorId') ? parseInt(url.searchParams.get('actorId')!) : undefined;
  const startDate = url.searchParams.get('startDate') ? new Date(url.searchParams.get('startDate')!) : undefined;
  const endDate = url.searchParams.get('endDate') ? new Date(url.searchParams.get('endDate')!) : undefined;

  const where: any = { orgId: guard.user!.orgId };
  if (eventType) where.eventType = eventType;
  if (actorId) where.actorId = actorId;
  if (startDate || endDate) {
    where.timestamp = {};
    if (startDate) where.timestamp.gte = startDate;
    if (endDate) where.timestamp.lte = endDate;
  }

  const [logs, total] = await Promise.all([
    prisma.securityAuditLog.findMany({
      where,
      orderBy: { timestamp: 'desc' },
      skip: (page - 1) * pageSize,
      take: pageSize,
    }),
    prisma.securityAuditLog.count({ where }),
  ]);

  return NextResponse.json({
    logs,
    pagination: { page, pageSize, total, totalPages: Math.ceil(total / pageSize) },
  });
}
```

---

### 3.2 Health Check with Real Service Checks

**Gap Reference:** Related to §11 (BC/DR) and monitoring
**File:** `app/api/health/route.ts`

**Step 1:** Replace the static health check with real service probes:

```typescript
// File: app/api/health/route.ts

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export async function GET() {
  const checks: Record<string, { status: string; latencyMs?: number; error?: string }> = {};
  let overallHealthy = true;

  // Database check
  const dbStart = Date.now();
  try {
    await prisma.$queryRaw`SELECT 1`;
    checks.database = { status: 'healthy', latencyMs: Date.now() - dbStart };
  } catch (err: any) {
    checks.database = { status: 'unhealthy', latencyMs: Date.now() - dbStart, error: 'Connection failed' };
    overallHealthy = false;
  }

  // Redis check (if configured)
  if (process.env.REDIS_URL) {
    const redisStart = Date.now();
    try {
      const { getRedis } = await import('@/lib/redis');
      await getRedis().ping();
      checks.redis = { status: 'healthy', latencyMs: Date.now() - redisStart };
    } catch {
      checks.redis = { status: 'unhealthy', latencyMs: Date.now() - redisStart, error: 'Connection failed' };
      overallHealthy = false;
    }
  }

  // S3 check
  if (process.env.S3_BUCKET_NAME) {
    const s3Start = Date.now();
    try {
      const { HeadBucketCommand } = await import('@aws-sdk/client-s3');
      const { s3Client } = await import('@/lib/s3');
      await (s3Client as any).send(new HeadBucketCommand({ Bucket: process.env.S3_BUCKET_NAME }));
      checks.s3 = { status: 'healthy', latencyMs: Date.now() - s3Start };
    } catch {
      checks.s3 = { status: 'degraded', latencyMs: Date.now() - s3Start, error: 'Bucket unreachable' };
      // S3 degradation doesn't make the whole service unhealthy
    }
  }

  return NextResponse.json({
    status: overallHealthy ? 'healthy' : 'unhealthy',
    service: 'QuickTrust Compliance Platform',
    version: process.env.APP_VERSION || '0.5.0',
    timestamp: new Date().toISOString(),
    checks,
  }, { status: overallHealthy ? 200 : 503 });
}
```

---

## Phase 4: Enterprise Integration -- SSO & SCIM (Weeks 14-17)

---

### 4.1 SAML 2.0 SSO

**Gap Reference:** missingfeatures.md §5.1
**Compliance:** SOC 2 CC6.1, ISO 27001 A.5.16
**New Dependencies:** `@node-saml/node-saml`
**New Files:** `lib/sso/saml.ts`, `app/api/auth/sso/saml/*`

**Step 1:** Install SAML library.

```bash
npm install @node-saml/node-saml
```

**Step 2:** Add SSO configuration to the Organization model.

```prisma
// File: prisma/schema.prisma

model SSOConfiguration {
  id                Int          @id @default(autoincrement())
  orgId             Int          @unique @map("org_id")
  provider          String       // "saml", "oidc"
  enabled           Boolean      @default(false)
  enforced          Boolean      @default(false) // Force SSO login (disable password)
  entityId          String?      @map("entity_id")       // SAML: SP Entity ID
  ssoUrl            String?      @map("sso_url")          // SAML: IdP SSO URL
  certificate       String?      @db.Text                  // SAML: IdP X.509 cert (PEM)
  oidcClientId      String?      @map("oidc_client_id")
  oidcClientSecret  String?      @map("oidc_client_secret") // Encrypted
  oidcIssuer        String?      @map("oidc_issuer")
  emailDomains      String[]     @map("email_domains")     // e.g., ["company.com"]
  attributeMapping  Json?        @map("attribute_mapping")  // Map IdP attrs to user fields
  createdAt         DateTime     @default(now()) @map("created_at")
  updatedAt         DateTime     @updatedAt @map("updated_at")
  organization      Organization @relation(fields: [orgId], references: [id], onDelete: Cascade)

  @@map("sso_configurations")
}

// Add to Organization model:
model Organization {
  // ... existing fields ...
  ssoConfig     SSOConfiguration?
}
```

```bash
npx prisma migrate dev --name add-sso-configuration
```

**Step 3:** Create the SAML service.

```typescript
// File: lib/sso/saml.ts

import { SAML } from '@node-saml/node-saml';
import { prisma } from '../db';

const APP_URL = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';

export async function getSamlStrategy(orgId: number): Promise<SAML | null> {
  const config = await prisma.sSOConfiguration.findUnique({
    where: { orgId },
  });

  if (!config || config.provider !== 'saml' || !config.enabled) {
    return null;
  }

  return new SAML({
    callbackUrl: `${APP_URL}/api/auth/sso/saml/callback`,
    entryPoint: config.ssoUrl!,
    issuer: config.entityId || `${APP_URL}/api/auth/sso/saml/metadata`,
    cert: config.certificate!,
    wantAssertionsSigned: true,
    wantAuthnResponseSigned: true,
    signatureAlgorithm: 'sha256',
    digestAlgorithm: 'sha256',
  });
}

/**
 * Find the SSO config for a given email domain.
 */
export async function findSSOConfigByEmail(email: string): Promise<{
  orgId: number;
  provider: string;
  enforced: boolean;
} | null> {
  const domain = email.split('@')[1]?.toLowerCase();
  if (!domain) return null;

  const config = await prisma.sSOConfiguration.findFirst({
    where: {
      enabled: true,
      emailDomains: { has: domain },
    },
    select: { orgId: true, provider: true, enforced: true },
  });

  return config;
}
```

**Step 4:** Create SAML endpoints.

```typescript
// File: app/api/auth/sso/saml/login/route.ts
// Initiates SAML authentication

import { NextResponse } from 'next/server';
import { getSamlStrategy } from '@/lib/sso/saml';

export async function GET(request: Request) {
  const url = new URL(request.url);
  const orgId = parseInt(url.searchParams.get('orgId') || '0');

  if (!orgId) {
    return NextResponse.json({ error: 'Organization ID required' }, { status: 400 });
  }

  const saml = await getSamlStrategy(orgId);
  if (!saml) {
    return NextResponse.json({ error: 'SSO not configured for this organization' }, { status: 404 });
  }

  const loginUrl = await saml.getAuthorizeUrlAsync('', undefined, {});
  return NextResponse.redirect(loginUrl);
}
```

```typescript
// File: app/api/auth/sso/saml/callback/route.ts
// Handles SAML assertion from IdP

import { NextResponse } from 'next/server';
import { getSamlStrategy } from '@/lib/sso/saml';
import { prisma } from '@/lib/db';
import { generateToken } from '@/lib/jwt';
import { logAuthEvent } from '@/lib/audit-logger';
import { getClientIp } from '@/lib/rate-limiter';

export async function POST(request: Request) {
  const formData = await request.formData();
  const samlResponse = formData.get('SAMLResponse') as string;

  if (!samlResponse) {
    return NextResponse.redirect(new URL('/login?error=saml_missing', request.url));
  }

  // Try all enabled SAML configs (in practice, use RelayState to identify org)
  const configs = await prisma.sSOConfiguration.findMany({
    where: { enabled: true, provider: 'saml' },
  });

  for (const config of configs) {
    const saml = await getSamlStrategy(config.orgId);
    if (!saml) continue;

    try {
      const result = await saml.validatePostResponseAsync({ SAMLResponse: samlResponse } as any);
      const profile = result.profile;

      if (!profile?.nameID) continue;

      const email = (profile.nameID || profile.email || '').toLowerCase();
      const fullName = profile.firstName
        ? `${profile.firstName} ${profile.lastName || ''}`
        : profile.displayName || undefined;

      // JIT (Just-In-Time) provisioning: create user if they don't exist
      let user = await prisma.user.findUnique({ where: { email } });

      if (!user) {
        user = await prisma.user.create({
          data: {
            email,
            passwordHash: '',  // SSO users don't have a password
            fullName: fullName?.trim() || null,
            orgId: config.orgId,
            role: 'MEMBER',
            status: 'ACTIVE',
          },
        });
      }

      const token = generateToken({
        userId: user.id,
        email: user.email,
        fullName: user.fullName || undefined,
      });

      await prisma.user.update({
        where: { id: user.id },
        data: { lastLogin: new Date() },
      });

      await logAuthEvent('AUTH_LOGIN', email, 'success', getClientIp(request), {
        method: 'saml_sso', orgId: config.orgId,
      });

      const response = NextResponse.redirect(new URL('/dashboard', request.url));
      response.cookies.set('auth_token', token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        path: '/',
        maxAge: 86400,
      });

      return response;
    } catch (err) {
      continue; // Try next config
    }
  }

  return NextResponse.redirect(new URL('/login?error=saml_failed', request.url));
}
```

---

### 4.2 SCIM 2.0 User Provisioning

**Gap Reference:** missingfeatures.md §5.3
**Compliance:** SOC 2 CC6.2/CC6.3, ISO 27001 A.5.18
**New Files:** `app/api/scim/v2/*`

**Step 1:** Create the SCIM Users endpoint (RFC 7644 compliant):

```typescript
// File: app/api/scim/v2/Users/route.ts

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { revokeAllUserTokens } from '@/lib/token-blacklist';

// SCIM Bearer token authentication
async function authenticateSCIM(request: Request): Promise<{ orgId: number } | null> {
  const authHeader = request.headers.get('authorization');
  if (!authHeader?.startsWith('Bearer ')) return null;

  const token = authHeader.slice(7);
  // Validate against stored SCIM tokens (you'd create a SCIMToken model)
  const scimToken = await prisma.sSOConfiguration.findFirst({
    where: { scimToken: token, enabled: true },
    select: { orgId: true },
  });

  return scimToken ? { orgId: scimToken.orgId } : null;
}

// GET: List users (SCIM filter support)
export async function GET(request: Request) {
  const auth = await authenticateSCIM(request);
  if (!auth) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const url = new URL(request.url);
  const startIndex = parseInt(url.searchParams.get('startIndex') || '1');
  const count = Math.min(parseInt(url.searchParams.get('count') || '100'), 100);
  const filter = url.searchParams.get('filter');

  let where: any = { orgId: auth.orgId };

  // Basic SCIM filter support: userName eq "email@example.com"
  if (filter) {
    const match = filter.match(/userName\s+eq\s+"([^"]+)"/);
    if (match) {
      where.email = match[1].toLowerCase();
    }
  }

  const [users, total] = await Promise.all([
    prisma.user.findMany({
      where,
      skip: startIndex - 1,
      take: count,
      select: { id: true, email: true, fullName: true, role: true, status: true, createdAt: true },
    }),
    prisma.user.count({ where }),
  ]);

  return NextResponse.json({
    schemas: ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
    totalResults: total,
    startIndex,
    itemsPerPage: count,
    Resources: users.map(userToSCIM),
  });
}

// POST: Create user
export async function POST(request: Request) {
  const auth = await authenticateSCIM(request);
  if (!auth) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const body = await request.json();
  const email = body.userName?.toLowerCase();
  const fullName = body.displayName || `${body.name?.givenName || ''} ${body.name?.familyName || ''}`.trim();
  const active = body.active !== false;

  if (!email) {
    return NextResponse.json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      detail: 'userName (email) is required',
      status: '400',
    }, { status: 400 });
  }

  const existing = await prisma.user.findUnique({ where: { email } });
  if (existing) {
    return NextResponse.json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      detail: 'User already exists',
      status: '409',
    }, { status: 409 });
  }

  const user = await prisma.user.create({
    data: {
      email,
      passwordHash: '', // SCIM-provisioned users authenticate via SSO
      fullName: fullName || null,
      orgId: auth.orgId,
      role: 'MEMBER',
      status: active ? 'ACTIVE' : 'SUSPENDED',
    },
  });

  return NextResponse.json(userToSCIM(user), { status: 201 });
}

function userToSCIM(user: any) {
  return {
    schemas: ['urn:ietf:params:scim:schemas:core:2.0:User'],
    id: String(user.id),
    userName: user.email,
    displayName: user.fullName,
    active: user.status === 'ACTIVE',
    name: {
      formatted: user.fullName,
    },
    emails: [{ value: user.email, primary: true, type: 'work' }],
    meta: {
      resourceType: 'User',
      created: user.createdAt?.toISOString(),
    },
  };
}
```

```typescript
// File: app/api/scim/v2/Users/[id]/route.ts

// GET: Get single user
// PATCH: Update user (including deactivation)
// DELETE: Remove user

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { revokeAllSessions } from '@/lib/session-manager';

// PATCH handler (SCIM uses PATCH for updates)
export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  // ... authenticate SCIM ...

  const body = await request.json();
  const userId = parseInt(params.id);
  const updateData: any = {};

  // Process SCIM Operations
  for (const op of body.Operations || []) {
    if (op.path === 'active' || (op.op === 'replace' && op.value?.active !== undefined)) {
      const active = op.value?.active ?? op.value;
      updateData.status = active ? 'ACTIVE' : 'DEACTIVATED';
      if (!active) {
        updateData.deactivatedAt = new Date();
        // Immediately revoke all sessions for deactivated user
        await revokeAllSessions(userId, 'scim_deprovisioning');
      }
    }

    if (op.path === 'displayName' || op.path === 'name.formatted') {
      updateData.fullName = op.value;
    }
  }

  if (Object.keys(updateData).length > 0) {
    await prisma.user.update({ where: { id: userId }, data: updateData });
  }

  const user = await prisma.user.findUnique({ where: { id: userId } });
  return NextResponse.json(userToSCIM(user));
}
```

---

## Phase 5: Compliance Automation Engine (Weeks 18-22)

---

### 5.1 Control Testing & Assessment Framework

**Gap Reference:** missingfeatures.md §18.1
**Compliance:** SOC 2 CC4.1, ISO 27001 A.9

**Step 1:** Add compliance management models.

```prisma
// File: prisma/schema.prisma

model ComplianceFramework {
  id          Int                  @id @default(autoincrement())
  name        String               // "SOC 2 Type II", "ISO 27001:2022"
  version     String               // "2017", "2022"
  shortCode   String               @unique @map("short_code") // "soc2", "iso27001"
  description String?
  controls    ComplianceControl[]
  orgId       Int?                 @map("org_id") // null = global template
  createdAt   DateTime             @default(now()) @map("created_at")

  @@map("compliance_frameworks")
}

model ComplianceControl {
  id              Int                  @id @default(autoincrement())
  frameworkId     Int                  @map("framework_id")
  controlId       String               @map("control_id") // e.g., "CC6.1", "A.5.15"
  title           String
  description     String?              @db.Text
  category        String?              // e.g., "Logical Access", "Encryption"
  testProcedure   String?              @map("test_procedure") @db.Text
  testFrequency   String?              @map("test_frequency") // "quarterly", "annually"
  framework       ComplianceFramework  @relation(fields: [frameworkId], references: [id])
  assessments     ControlAssessment[]
  crossMappings   CrossFrameworkMapping[] @relation("SourceControl")
  mappedFrom      CrossFrameworkMapping[] @relation("TargetControl")

  @@unique([frameworkId, controlId])
  @@map("compliance_controls")
}

model ControlAssessment {
  id               Int               @id @default(autoincrement())
  controlId        Int               @map("control_id")
  orgId            Int               @map("org_id")
  status           AssessmentStatus  @default(NOT_ASSESSED)
  maturityLevel    Int?              @map("maturity_level")  // 1-5 (CMMI)
  testedBy         Int?              @map("tested_by")
  testedAt         DateTime?         @map("tested_at")
  nextTestDate     DateTime?         @map("next_test_date")
  result           String?           // "pass", "fail", "partial", "not_applicable"
  findings         String?           @db.Text
  remediationPlan  String?           @map("remediation_plan") @db.Text
  remediationDue   DateTime?         @map("remediation_due")
  evidenceIds      Int[]             @map("evidence_ids")
  control          ComplianceControl @relation(fields: [controlId], references: [id])
  createdAt        DateTime          @default(now()) @map("created_at")
  updatedAt        DateTime          @updatedAt @map("updated_at")

  @@unique([controlId, orgId])
  @@index([orgId, status])
  @@map("control_assessments")
}

enum AssessmentStatus {
  NOT_ASSESSED
  IN_PROGRESS
  PASS
  FAIL
  PARTIAL
  NOT_APPLICABLE
  EXCEPTION
}

model CrossFrameworkMapping {
  id              Int               @id @default(autoincrement())
  sourceControlId Int               @map("source_control_id")
  targetControlId Int               @map("target_control_id")
  mappingType     String            @default("equivalent") // "equivalent", "partial", "related"
  sourceControl   ComplianceControl @relation("SourceControl", fields: [sourceControlId], references: [id])
  targetControl   ComplianceControl @relation("TargetControl", fields: [targetControlId], references: [id])

  @@unique([sourceControlId, targetControlId])
  @@map("cross_framework_mappings")
}

model ComplianceSnapshot {
  id             Int      @id @default(autoincrement())
  orgId          Int      @map("org_id")
  frameworkId    Int      @map("framework_id")
  snapshotDate   DateTime @map("snapshot_date")
  totalControls  Int      @map("total_controls")
  passedControls Int      @map("passed_controls")
  failedControls Int      @map("failed_controls")
  score          Float    // Percentage (0-100)
  details        Json?    // Full breakdown
  createdAt      DateTime @default(now()) @map("created_at")

  @@index([orgId, frameworkId, snapshotDate])
  @@map("compliance_snapshots")
}
```

```bash
npx prisma migrate dev --name add-compliance-engine
```

**Step 2:** Create the compliance posture API:

```typescript
// File: app/api/compliance/posture/route.ts

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { prisma } from '@/lib/db';

export async function GET(request: Request) {
  const guard = await apiGuard(request, {
    requireAuth: true, requireOrg: true,
    requirePermission: { resource: 'reports', action: 'read' },
  });
  if (!guard.allowed) return guard.response!;

  const url = new URL(request.url);
  const frameworkShortCode = url.searchParams.get('framework');

  const frameworks = await prisma.complianceFramework.findMany({
    where: frameworkShortCode ? { shortCode: frameworkShortCode } : undefined,
    include: {
      controls: {
        include: {
          assessments: {
            where: { orgId: guard.user!.orgId! },
          },
        },
      },
    },
  });

  const posture = frameworks.map(fw => {
    const totalControls = fw.controls.length;
    const assessments = fw.controls.flatMap(c => c.assessments);
    const passed = assessments.filter(a => a.status === 'PASS').length;
    const failed = assessments.filter(a => a.status === 'FAIL').length;
    const inProgress = assessments.filter(a => a.status === 'IN_PROGRESS').length;
    const notAssessed = totalControls - assessments.length;

    return {
      framework: fw.name,
      shortCode: fw.shortCode,
      version: fw.version,
      totalControls,
      passed,
      failed,
      inProgress,
      notAssessed,
      score: totalControls > 0 ? Math.round((passed / totalControls) * 100) : 0,
    };
  });

  return NextResponse.json({ posture });
}
```

---

### 5.2 Incident Response System

**Gap Reference:** missingfeatures.md §10.1, §10.2
**Compliance:** SOC 2 CC7.3, ISO 27001 A.5.24-A.5.28, PCI DSS 12.10

**Step 1:** Add incident management models.

```prisma
// File: prisma/schema.prisma

model SecurityIncident {
  id               Int              @id @default(autoincrement())
  orgId            Int              @map("org_id")
  title            String
  description      String           @db.Text
  severity         IncidentSeverity
  status           IncidentStatus   @default(DETECTED)
  category         String?          // "data_breach", "unauthorized_access", "malware", "phishing", etc.
  reportedBy       Int              @map("reported_by")
  assignedTo       Int?             @map("assigned_to")
  detectedAt       DateTime         @map("detected_at")
  containedAt      DateTime?        @map("contained_at")
  resolvedAt       DateTime?        @map("resolved_at")
  closedAt         DateTime?        @map("closed_at")
  rootCause        String?          @map("root_cause") @db.Text
  lessonsLearned   String?          @map("lessons_learned") @db.Text
  affectedSystems  String[]         @map("affected_systems")
  affectedUsers    Int              @default(0) @map("affected_users")
  breachNotificationRequired Boolean @default(false) @map("breach_notification_required")
  timeline         IncidentTimeline[]
  createdAt        DateTime         @default(now()) @map("created_at")
  updatedAt        DateTime         @updatedAt @map("updated_at")

  @@index([orgId, status])
  @@index([orgId, severity])
  @@map("security_incidents")
}

enum IncidentSeverity {
  P1_CRITICAL
  P2_HIGH
  P3_MEDIUM
  P4_LOW
}

enum IncidentStatus {
  DETECTED
  TRIAGED
  CONTAINED
  ERADICATED
  RECOVERED
  POST_MORTEM
  CLOSED
}

model IncidentTimeline {
  id         Int              @id @default(autoincrement())
  incidentId Int              @map("incident_id")
  action     String           @db.Text
  actorId    Int?             @map("actor_id")
  timestamp  DateTime         @default(now())
  incident   SecurityIncident @relation(fields: [incidentId], references: [id], onDelete: Cascade)

  @@index([incidentId, timestamp])
  @@map("incident_timeline")
}
```

---

### 5.3 Policy Lifecycle Management

**Gap Reference:** missingfeatures.md §18.7
**Compliance:** SOC 2 CC5.3, ISO 27001 A.5.1

**Step 1:** Extend the PolicyDocument model:

```prisma
// File: prisma/schema.prisma

enum PolicyStatus {
  DRAFT
  PENDING_REVIEW
  APPROVED
  PUBLISHED
  RETIRED
}

model PolicyDocument {
  // ... existing fields ...
  status              PolicyStatus    @default(DRAFT)
  approvedBy          Int?            @map("approved_by")
  approvedAt          DateTime?       @map("approved_at")
  nextReviewDate      DateTime?       @map("next_review_date")
  reviewFrequencyDays Int             @default(365) @map("review_frequency_days")
  policyOwner         Int?            @map("policy_owner")
  changelog           String?         @db.Text
  previousVersionId   Int?            @map("previous_version_id")
  acknowledgments     PolicyAcknowledgment[]
}

model PolicyAcknowledgment {
  id             Int            @id @default(autoincrement())
  policyId       Int            @map("policy_id")
  userId         Int            @map("user_id")
  acknowledgedAt DateTime       @default(now()) @map("acknowledged_at")
  ipAddress      String?        @map("ip_address")
  policy         PolicyDocument @relation(fields: [policyId], references: [id])

  @@unique([policyId, userId])
  @@map("policy_acknowledgments")
}
```

---

### 5.4 Risk Register

**Gap Reference:** missingfeatures.md §18.8
**Compliance:** ISO 27001 clause 6.1, SOC 2 CC3.2

```prisma
// File: prisma/schema.prisma

model Risk {
  id              Int          @id @default(autoincrement())
  orgId           Int          @map("org_id")
  title           String
  description     String       @db.Text
  category        String       // "operational", "technical", "compliance", "financial"
  likelihood      Int          // 1-5
  impact          Int          // 1-5
  riskScore       Int          @map("risk_score") // likelihood * impact
  riskLevel       String       @map("risk_level") // "low", "medium", "high", "critical"
  treatment       String       @default("mitigate") // "mitigate", "accept", "transfer", "avoid"
  treatmentPlan   String?      @map("treatment_plan") @db.Text
  ownerId         Int?         @map("owner_id")
  status          String       @default("open") // "open", "mitigating", "accepted", "closed"
  acceptedBy      Int?         @map("accepted_by")
  acceptedAt      DateTime?    @map("accepted_at")
  reviewDate      DateTime?    @map("review_date")
  relatedControls String[]     @map("related_controls") // Control IDs
  createdAt       DateTime     @default(now()) @map("created_at")
  updatedAt       DateTime     @updatedAt @map("updated_at")

  @@index([orgId, riskLevel])
  @@index([orgId, status])
  @@map("risks")
}
```

---

## Phase 6: AI Governance & LLM Safety (Weeks 23-25)

---

### 6.1 Human-in-the-Loop AI Approval Workflow

**Gap Reference:** missingfeatures.md §17.1
**Compliance:** SOC 2 CC1.4, ISO 42001

**Step 1:** Add AI output review status to the Answer model:

```prisma
// File: prisma/schema.prisma

enum AIReviewStatus {
  PENDING_REVIEW   // AI-generated, awaiting human review
  APPROVED         // Human approved
  REJECTED         // Human rejected
  MODIFIED         // Human modified and approved
}

model Answer {
  // ... existing fields ...
  aiReviewStatus    AIReviewStatus  @default(PENDING_REVIEW) @map("ai_review_status")
  reviewedBy        Int?            @map("reviewed_by")
  reviewedAt        DateTime?       @map("reviewed_at")
  reviewNotes       String?         @map("review_notes")
  originalAiOutput  String?         @map("original_ai_output") @db.Text // Preserve original before edits
  promptVersion     String?         @map("prompt_version")
  modelVersion      String?         @map("model_version")
  tokensUsed        Int?            @map("tokens_used")
  responseTimeMs    Int?            @map("response_time_ms")
  hallucination     Float?          @map("hallucination_score") // 0.0-1.0 confidence
}
```

**Step 2:** Modify the ask-question flow to set `PENDING_REVIEW` status:

```typescript
// File: app/api/ask-question/route.ts
// When creating the answer, set:

const answer = await prisma.answer.create({
  data: {
    answerText: aiResponse.answer,
    confidence: aiResponse.confidence,
    framework: aiResponse.framework,
    controlDomain: aiResponse.controlDomain,
    model: aiResponse.model || 'gpt-4',
    questionId: question.id,
    createdByUserId: user.userId,
    aiReviewStatus: 'PENDING_REVIEW',  // Requires human approval
    originalAiOutput: aiResponse.answer, // Preserve original
    promptVersion: '1.0',
    modelVersion: aiResponse.model,
    tokensUsed: aiResponse.tokensUsed,
    responseTimeMs: responseTime,
  },
});
```

**Step 3:** Create the AI review endpoint:

```typescript
// File: app/api/answers/[id]/review/route.ts

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { prisma } from '@/lib/db';
import { logDataEvent } from '@/lib/audit-logger';
import { getClientIp } from '@/lib/rate-limiter';

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  const guard = await apiGuard(request, {
    requireAuth: true, requireOrg: true,
    requirePermission: { resource: 'questions', action: 'approve' },
  });
  if (!guard.allowed) return guard.response!;

  const answerId = parseInt(params.id);
  const { action, modifiedText, reviewNotes } = await request.json();

  // Separation of duties: reviewer must not be the question asker
  const answer = await prisma.answer.findUnique({
    where: { id: answerId },
    include: { question: { select: { askedByUserId: true, orgId: true } } },
  });

  if (!answer || answer.question.orgId !== guard.user!.orgId) {
    return NextResponse.json({ error: 'Answer not found' }, { status: 404 });
  }

  if (answer.question.askedByUserId === guard.user!.userId) {
    return NextResponse.json(
      { error: 'Separation of duties: you cannot review your own question\'s answer' },
      { status: 403 }
    );
  }

  let updateData: any = {
    reviewedBy: guard.user!.userId,
    reviewedAt: new Date(),
    reviewNotes,
  };

  switch (action) {
    case 'approve':
      updateData.aiReviewStatus = 'APPROVED';
      break;
    case 'reject':
      updateData.aiReviewStatus = 'REJECTED';
      break;
    case 'modify':
      if (!modifiedText) {
        return NextResponse.json({ error: 'Modified text required' }, { status: 400 });
      }
      updateData.aiReviewStatus = 'MODIFIED';
      updateData.answerText = modifiedText;
      break;
    default:
      return NextResponse.json({ error: 'Invalid action' }, { status: 400 });
  }

  const updated = await prisma.answer.update({
    where: { id: answerId },
    data: updateData,
  });

  await logDataEvent('update', 'answer', answerId, {
    id: guard.user!.userId, email: guard.user!.email, orgId: guard.user!.orgId,
  }, getClientIp(request), { action: `ai_review_${action}` });

  return NextResponse.json({ answer: updated });
}
```

---

### 6.2 AI Cost Controls & Budget Management

**Gap Reference:** missingfeatures.md §17.4
**New File:** `lib/ai-budget.ts`

```typescript
// File: lib/ai-budget.ts

import { getRedis } from './redis';

const DEFAULT_DAILY_TOKEN_LIMIT = parseInt(process.env.AI_DAILY_TOKEN_LIMIT || '500000');
const DEFAULT_MONTHLY_TOKEN_LIMIT = parseInt(process.env.AI_MONTHLY_TOKEN_LIMIT || '10000000');

/**
 * Track and enforce AI token budgets per organization.
 */
export async function checkAndTrackTokenBudget(
  orgId: number,
  tokensUsed: number
): Promise<{ allowed: boolean; dailyUsed: number; monthlyUsed: number; dailyLimit: number; monthlyLimit: number }> {
  const redis = getRedis();
  const today = new Date().toISOString().split('T')[0];       // "2026-03-17"
  const month = today.substring(0, 7);                        // "2026-03"
  const dailyKey = `ai:budget:daily:${orgId}:${today}`;
  const monthlyKey = `ai:budget:monthly:${orgId}:${month}`;

  const pipeline = redis.pipeline();
  pipeline.incrby(dailyKey, tokensUsed);
  pipeline.expire(dailyKey, 86400 * 2);  // Auto-cleanup
  pipeline.incrby(monthlyKey, tokensUsed);
  pipeline.expire(monthlyKey, 86400 * 35);

  const results = await pipeline.exec();
  const dailyUsed = (results?.[0]?.[1] as number) || 0;
  const monthlyUsed = (results?.[2]?.[1] as number) || 0;

  const allowed = dailyUsed <= DEFAULT_DAILY_TOKEN_LIMIT && monthlyUsed <= DEFAULT_MONTHLY_TOKEN_LIMIT;

  return {
    allowed,
    dailyUsed,
    monthlyUsed,
    dailyLimit: DEFAULT_DAILY_TOKEN_LIMIT,
    monthlyLimit: DEFAULT_MONTHLY_TOKEN_LIMIT,
  };
}

/**
 * Pre-check before making an AI call.
 */
export async function canMakeAICall(orgId: number, estimatedTokens: number = 8192): Promise<boolean> {
  const budget = await checkAndTrackTokenBudget(orgId, 0); // Check without incrementing
  return (budget.dailyUsed + estimatedTokens) <= budget.dailyLimit &&
         (budget.monthlyUsed + estimatedTokens) <= budget.monthlyLimit;
}
```

---

## Phase 7: Infrastructure & DR (Weeks 26-28)

---

### 7.1 Automated Database Backups

**Gap Reference:** missingfeatures.md §11.1
**Compliance:** SOC 2 A1.2, ISO 27001 A.8.13, PCI DSS 9.5
**New File:** `scripts/backup-database.sh`

```bash
#!/bin/bash
# File: scripts/backup-database.sh
# Schedule via cron: 0 2 * * * /app/scripts/backup-database.sh

set -euo pipefail

BACKUP_DIR="/backups/postgresql"
S3_BACKUP_BUCKET="${S3_BACKUP_BUCKET:-quicktrust-backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="quicktrust_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting database backup..."

# Create compressed backup
pg_dump "$DATABASE_URL" --no-owner --no-privileges | gzip > "$BACKUP_DIR/$BACKUP_FILE"

BACKUP_SIZE=$(stat -f%z "$BACKUP_DIR/$BACKUP_FILE" 2>/dev/null || stat -c%s "$BACKUP_DIR/$BACKUP_FILE")
echo "[$(date)] Backup created: $BACKUP_FILE ($BACKUP_SIZE bytes)"

# Upload to S3 with server-side encryption
aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" \
  "s3://$S3_BACKUP_BUCKET/database/$BACKUP_FILE" \
  --sse aws:kms \
  --storage-class STANDARD_IA

echo "[$(date)] Backup uploaded to S3: s3://$S3_BACKUP_BUCKET/database/$BACKUP_FILE"

# Clean up local backups older than retention period
find "$BACKUP_DIR" -name "quicktrust_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Clean up S3 backups (handled by S3 lifecycle policy, but double-check)
echo "[$(date)] Backup complete."

# Verify backup integrity (restore to temp database)
if [ "${VERIFY_BACKUP:-false}" = "true" ]; then
  echo "[$(date)] Verifying backup integrity..."
  TEMP_DB="quicktrust_verify_${TIMESTAMP}"
  createdb "$TEMP_DB" 2>/dev/null || true
  gunzip -c "$BACKUP_DIR/$BACKUP_FILE" | psql "$TEMP_DB" > /dev/null 2>&1
  VERIFY_RESULT=$?
  dropdb "$TEMP_DB" 2>/dev/null || true

  if [ $VERIFY_RESULT -eq 0 ]; then
    echo "[$(date)] Backup verification: PASSED"
  else
    echo "[$(date)] Backup verification: FAILED" >&2
    exit 1
  fi
fi
```

---

### 7.2 CI/CD Security Gates

**Gap Reference:** missingfeatures.md §12.1, §12.3, §12.4, §15.1
**File:** `.github/workflows/security-audit.yml`

**Step 1:** Replace the minimal security audit with a comprehensive pipeline:

```yaml
# File: .github/workflows/security-audit.yml

name: Security & Quality Gates

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 3 * * 1'  # Weekly Monday 3am UTC

permissions:
  contents: read
  security-events: write

jobs:
  # --- Dependency Audit ---
  dependency-audit:
    name: Dependency Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci --legacy-peer-deps
      - name: NPM Audit (Critical + High)
        run: npm audit --audit-level=high
      - name: Check for known vulnerable packages
        run: npx better-npm-audit audit --level high

  # --- Static Analysis (SAST) ---
  sast:
    name: Static Application Security Testing
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/typescript
            p/react
            p/nextjs
            p/jwt
            p/sql-injection

  # --- TypeScript Type Checking ---
  typecheck:
    name: TypeScript Compilation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci --legacy-peer-deps
      - run: npx tsc --noEmit

  # --- Container Image Scanning ---
  container-scan:
    name: Container Image Scan
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker Image
        run: docker build -t quicktrust:scan .
      - name: Run Trivy Container Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'quicktrust:scan'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
      - name: Upload Trivy SARIF
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'

  # --- License Compliance ---
  license-check:
    name: License Compliance
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci --legacy-peer-deps
      - name: Check licenses
        run: npx license-checker --failOn 'GPL-2.0;GPL-3.0;AGPL-1.0;AGPL-3.0'

  # --- SBOM Generation ---
  sbom:
    name: Generate SBOM
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci --legacy-peer-deps
      - name: Generate CycloneDX SBOM
        run: npx @cyclonedx/cyclonedx-npm --output-file sbom.json
      - name: Upload SBOM artifact
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json
```

---

## Phase 8: Privacy, Reporting & Advanced (Weeks 29-32)

---

### 8.1 Data Retention Policy Engine

**Gap Reference:** missingfeatures.md §8.1, §8.3
**Compliance:** SOC 2 CC6.5, ISO 27001 A.5.33, GDPR Article 17, HIPAA 164.530(j)

**Step 1:** Add retention policy model:

```prisma
// File: prisma/schema.prisma

model DataRetentionPolicy {
  id               Int      @id @default(autoincrement())
  orgId            Int      @map("org_id")
  dataType         String   @map("data_type")     // "evidence", "policies", "questions", "audit_logs", "users"
  retentionDays    Int      @map("retention_days") // -1 = indefinite
  action           String   @default("archive")    // "archive", "delete", "anonymize"
  enabled          Boolean  @default(true)
  lastExecuted     DateTime? @map("last_executed")
  createdAt        DateTime @default(now()) @map("created_at")
  updatedAt        DateTime @updatedAt @map("updated_at")

  @@unique([orgId, dataType])
  @@map("data_retention_policies")
}

model LegalHold {
  id          Int       @id @default(autoincrement())
  orgId       Int       @map("org_id")
  name        String
  reason      String    @db.Text
  createdBy   Int       @map("created_by")
  startDate   DateTime  @map("start_date")
  endDate     DateTime? @map("end_date")
  dataTypes   String[]  @map("data_types")  // Which data types are held
  userIds     Int[]     @map("user_ids")     // Specific users held (empty = all)
  isActive    Boolean   @default(true) @map("is_active")
  createdAt   DateTime  @default(now()) @map("created_at")

  @@index([orgId, isActive])
  @@map("legal_holds")
}
```

**Step 2:** Create the retention enforcement service:

```typescript
// File: lib/data-retention.ts

import { prisma } from './db';
import { auditLog } from './audit-logger';

/**
 * Execute data retention policies for an organization.
 * Should be run daily via cron job.
 */
export async function enforceRetentionPolicies(orgId: number): Promise<{
  processed: number;
  archived: number;
  deleted: number;
  anonymized: number;
  skippedDueToHold: number;
}> {
  const stats = { processed: 0, archived: 0, deleted: 0, anonymized: 0, skippedDueToHold: 0 };

  // Check for active legal holds
  const activeHolds = await prisma.legalHold.findMany({
    where: { orgId, isActive: true },
  });

  const heldDataTypes = new Set(activeHolds.flatMap(h => h.dataTypes));

  const policies = await prisma.dataRetentionPolicy.findMany({
    where: { orgId, enabled: true, retentionDays: { gt: 0 } },
  });

  for (const policy of policies) {
    if (heldDataTypes.has(policy.dataType)) {
      stats.skippedDueToHold++;
      continue;
    }

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - policy.retentionDays);

    switch (policy.dataType) {
      case 'evidence':
        const expiredEvidence = await prisma.evidence.findMany({
          where: { orgId, createdAt: { lt: cutoffDate }, isDeleted: false },
          select: { id: true },
        });

        for (const ev of expiredEvidence) {
          if (policy.action === 'delete') {
            await prisma.evidence.update({
              where: { id: ev.id },
              data: { isDeleted: true, deletedAt: new Date() },
            });
            stats.deleted++;
          }
          stats.processed++;
        }
        break;

      case 'audit_logs':
        // Audit logs: archive to cold storage, then delete from active table
        if (policy.action === 'archive' || policy.action === 'delete') {
          const result = await prisma.securityAuditLog.deleteMany({
            where: { orgId, timestamp: { lt: cutoffDate } },
          });
          stats.deleted += result.count;
          stats.processed += result.count;
        }
        break;

      // Add cases for other data types...
    }

    // Record execution
    await prisma.dataRetentionPolicy.update({
      where: { id: policy.id },
      data: { lastExecuted: new Date() },
    });
  }

  await auditLog({
    eventType: 'SYSTEM_RETENTION',
    eventCategory: 'system',
    action: 'enforce_retention',
    orgId,
    details: stats,
  });

  return stats;
}
```

**Step 3:** Create a cron endpoint for retention execution:

```typescript
// File: app/api/cron/retention/route.ts

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { enforceRetentionPolicies } from '@/lib/data-retention';

export async function POST(request: Request) {
  // Verify cron secret to prevent unauthorized execution
  const cronSecret = request.headers.get('x-cron-secret');
  if (cronSecret !== process.env.CRON_SECRET) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const orgs = await prisma.organization.findMany({ select: { id: true } });
  const results: Record<number, any> = {};

  for (const org of orgs) {
    results[org.id] = await enforceRetentionPolicies(org.id);
  }

  return NextResponse.json({ message: 'Retention policies executed', results });
}
```

---

### 8.2 GDPR Data Subject Access Request (DSAR) Handler

**Gap Reference:** missingfeatures.md §8.3, §8.4
**Compliance:** GDPR Articles 15, 17, 20

```prisma
// File: prisma/schema.prisma

enum DSARType {
  ACCESS     // Right to access (Article 15)
  ERASURE    // Right to erasure (Article 17)
  PORTABILITY // Right to data portability (Article 20)
  RECTIFICATION // Right to rectification (Article 16)
  RESTRICTION // Right to restrict processing (Article 18)
}

enum DSARStatus {
  SUBMITTED
  IDENTITY_VERIFICATION
  IN_PROGRESS
  COMPLETED
  REJECTED
}

model DataSubjectRequest {
  id               Int        @id @default(autoincrement())
  orgId            Int        @map("org_id")
  requestType      DSARType   @map("request_type")
  status           DSARStatus @default(SUBMITTED)
  subjectEmail     String     @map("subject_email")
  subjectName      String?    @map("subject_name")
  description      String?    @db.Text
  assignedTo       Int?       @map("assigned_to")
  dueDate          DateTime   @map("due_date")   // 30 days from submission
  completedAt      DateTime?  @map("completed_at")
  responseData     Json?      @map("response_data")  // Collected data for export
  identityVerified Boolean    @default(false) @map("identity_verified")
  verifiedBy       Int?       @map("verified_by")
  notes            String?    @db.Text
  createdAt        DateTime   @default(now()) @map("created_at")
  updatedAt        DateTime   @updatedAt @map("updated_at")

  @@index([orgId, status])
  @@index([dueDate])
  @@map("data_subject_requests")
}
```

```typescript
// File: lib/dsar-handler.ts

import { prisma } from './db';

/**
 * Collect all data associated with a user email for DSAR Access/Portability requests.
 */
export async function collectUserData(email: string, orgId: number): Promise<Record<string, any>> {
  const user = await prisma.user.findFirst({
    where: { email, orgId },
    select: {
      id: true, email: true, fullName: true, role: true,
      createdAt: true, lastLogin: true,
    },
  });

  if (!user) return { user: null, message: 'No data found for this email' };

  const [questions, comments, evidence, auditTrail] = await Promise.all([
    prisma.question.findMany({
      where: { askedByUserId: user.id, orgId },
      include: { answer: { include: { citations: true } } },
    }),
    prisma.comment.findMany({
      where: { userId: user.id },
      select: { id: true, commentText: true, createdAt: true },
    }),
    prisma.evidence.findMany({
      where: { uploadedByUserId: user.id, orgId },
      select: { id: true, name: true, fileType: true, uploadDate: true },
    }),
    prisma.securityAuditLog.findMany({
      where: { actorId: user.id },
      select: { eventType: true, action: true, timestamp: true, actorIp: true },
      orderBy: { timestamp: 'desc' },
      take: 1000,
    }),
  ]);

  return {
    exportDate: new Date().toISOString(),
    format: 'GDPR Article 20 - Machine Readable',
    user: {
      profile: user,
      questions: questions.map(q => ({
        question: q.questionText,
        status: q.status,
        askedAt: q.createdAt,
        answer: q.answer ? {
          text: q.answer.answerText,
          confidence: q.answer.confidence,
          framework: q.answer.framework,
        } : null,
      })),
      comments: comments,
      uploadedEvidence: evidence,
      activityLog: auditTrail,
    },
  };
}

/**
 * Erase all user data for GDPR Article 17 Right to Erasure.
 */
export async function eraseUserData(
  email: string,
  orgId: number,
  requestId: number
): Promise<{ erasedRecords: Record<string, number> }> {
  const user = await prisma.user.findFirst({
    where: { email, orgId },
  });

  if (!user) return { erasedRecords: {} };

  const erasedRecords: Record<string, number> = {};

  // Soft-delete or anonymize user-associated data
  await prisma.$transaction(async (tx) => {
    // Anonymize comments (keep for audit integrity but remove PII)
    const comments = await tx.comment.updateMany({
      where: { userId: user.id },
      data: { commentText: '[REDACTED - GDPR Erasure]' },
    });
    erasedRecords.comments = comments.count;

    // Soft-delete evidence
    const evidence = await tx.evidence.updateMany({
      where: { uploadedByUserId: user.id, orgId },
      data: { isDeleted: true, deletedAt: new Date() },
    });
    erasedRecords.evidence = evidence.count;

    // Anonymize the user record (don't delete to maintain referential integrity)
    await tx.user.update({
      where: { id: user.id },
      data: {
        email: `deleted_${user.id}@redacted.local`,
        fullName: null,
        passwordHash: '',
        status: 'DEACTIVATED',
        deactivatedAt: new Date(),
      },
    });
    erasedRecords.userProfile = 1;

    // Anonymize audit logs (keep events but redact PII)
    const auditLogs = await tx.securityAuditLog.updateMany({
      where: { actorId: user.id },
      data: { actorEmail: '[REDACTED]', actorIp: '[REDACTED]' },
    });
    erasedRecords.auditLogs = auditLogs.count;
  });

  return { erasedRecords };
}
```

---

### 8.3 Compliance Report Generation

**Gap Reference:** missingfeatures.md §24.1, §24.2
**Compliance:** All frameworks require demonstrable reporting

```typescript
// File: app/api/reports/compliance/route.ts

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { prisma } from '@/lib/db';

export async function GET(request: Request) {
  const guard = await apiGuard(request, {
    requireAuth: true, requireOrg: true,
    requirePermission: { resource: 'reports', action: 'read' },
  });
  if (!guard.allowed) return guard.response!;

  const orgId = guard.user!.orgId!;
  const url = new URL(request.url);
  const frameworkCode = url.searchParams.get('framework') || 'soc2';

  // Gather all compliance data
  const [
    controlAssessments,
    policies,
    evidence,
    incidents,
    risks,
    recentAuditLogs,
  ] = await Promise.all([
    prisma.controlAssessment.findMany({
      where: { orgId },
      include: { control: { include: { framework: true } } },
    }),
    prisma.policyDocument.findMany({
      where: { orgId, isDeleted: false },
      select: { id: true, name: true, version: true, status: true, approvedAt: true, nextReviewDate: true },
    }),
    prisma.evidence.findMany({
      where: { orgId, isDeleted: false },
      select: { id: true, name: true, uploadDate: true, classification: true },
    }),
    prisma.securityIncident.count({ where: { orgId } }),
    prisma.risk.findMany({
      where: { orgId },
      select: { riskLevel: true, status: true, treatment: true },
    }),
    prisma.securityAuditLog.count({
      where: { orgId, timestamp: { gte: new Date(Date.now() - 30 * 86400000) } },
    }),
  ]);

  // Calculate compliance score
  const totalControls = controlAssessments.length;
  const passed = controlAssessments.filter(a => a.status === 'PASS').length;
  const failed = controlAssessments.filter(a => a.status === 'FAIL').length;
  const score = totalControls > 0 ? Math.round((passed / totalControls) * 100) : 0;

  // Policy health
  const overduePolicies = policies.filter(p =>
    p.nextReviewDate && p.nextReviewDate < new Date()
  ).length;

  // Risk summary
  const riskSummary = {
    critical: risks.filter(r => r.riskLevel === 'critical').length,
    high: risks.filter(r => r.riskLevel === 'high').length,
    medium: risks.filter(r => r.riskLevel === 'medium').length,
    low: risks.filter(r => r.riskLevel === 'low').length,
    accepted: risks.filter(r => r.treatment === 'accept').length,
  };

  return NextResponse.json({
    report: {
      generatedAt: new Date().toISOString(),
      organization: orgId,
      framework: frameworkCode,
      executiveSummary: {
        complianceScore: score,
        totalControls,
        controlsPassed: passed,
        controlsFailed: failed,
        controlsNotAssessed: totalControls - passed - failed,
      },
      policies: {
        total: policies.length,
        approved: policies.filter(p => p.status === 'APPROVED' || p.status === 'PUBLISHED').length,
        overdue: overduePolicies,
      },
      evidence: {
        total: evidence.length,
      },
      incidents: {
        total: incidents,
      },
      risks: riskSummary,
      auditActivity: {
        last30Days: recentAuditLogs,
      },
      controlDetails: controlAssessments.map(a => ({
        controlId: a.control.controlId,
        title: a.control.title,
        framework: a.control.framework.shortCode,
        status: a.status,
        maturityLevel: a.maturityLevel,
        lastTested: a.testedAt,
        nextTestDate: a.nextTestDate,
      })),
    },
  });
}
```

---

### 8.4 Evidence Integrity -- SHA-256 Hashing

**Gap Reference:** missingfeatures.md §23.1
**Compliance:** SOC 2 CC7.1, ISO 27001 A.8.10

**Step 1:** Add hash fields to the Evidence model:

```prisma
// File: prisma/schema.prisma

model Evidence {
  // ... existing fields ...
  sha256Hash       String?   @map("sha256_hash")
  hashVerifiedAt   DateTime? @map("hash_verified_at")
  integrityStatus  String?   @map("integrity_status") // "valid", "tampered", "unverified"
}
```

**Step 2:** Compute hash at upload time:

```typescript
// File: app/api/evidence/route.ts
// In the POST handler, after reading the file buffer:

import crypto from 'crypto';

const fileBuffer = Buffer.from(await file.arrayBuffer());
const sha256Hash = crypto.createHash('sha256').update(fileBuffer).digest('hex');

// Include in evidence creation:
const evidence = await prisma.evidence.create({
  data: {
    // ... existing fields ...
    sha256Hash,
    integrityStatus: 'valid',
  },
});
```

**Step 3:** Create a verification endpoint:

```typescript
// File: app/api/evidence/[id]/verify/route.ts

import { NextResponse } from 'next/server';
import { apiGuard } from '@/lib/api-guard';
import { prisma } from '@/lib/db';
import { getS3File } from '@/lib/s3';
import crypto from 'crypto';

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  const guard = await apiGuard(request, {
    requireAuth: true, requireOrg: true,
    requirePermission: { resource: 'evidence', action: 'read' },
  });
  if (!guard.allowed) return guard.response!;

  const evidence = await prisma.evidence.findFirst({
    where: { id: parseInt(params.id), orgId: guard.user!.orgId! },
  });

  if (!evidence?.s3Key || !evidence.sha256Hash) {
    return NextResponse.json({ error: 'Evidence not found or has no hash' }, { status: 404 });
  }

  const fileBuffer = await getS3File(evidence.s3Key);
  const currentHash = crypto.createHash('sha256').update(fileBuffer).digest('hex');
  const isValid = currentHash === evidence.sha256Hash;

  await prisma.evidence.update({
    where: { id: evidence.id },
    data: {
      hashVerifiedAt: new Date(),
      integrityStatus: isValid ? 'valid' : 'tampered',
    },
  });

  return NextResponse.json({
    evidenceId: evidence.id,
    integrityValid: isValid,
    storedHash: evidence.sha256Hash,
    currentHash,
    verifiedAt: new Date().toISOString(),
  });
}
```

---

## Summary: New Environment Variables Reference

All new environment variables introduced across all phases:

```env
# Phase 0: Foundation Security
COOKIE_DOMAIN=""                        # Production cookie domain
REDIS_URL="redis://localhost:6379"      # Redis connection
REDIS_PASSWORD=""                       # Redis authentication
REDIS_TLS_ENABLED="false"              # Redis TLS
S3_KMS_KEY_ID=""                        # S3 encryption key

# Phase 1: Identity & Access
MFA_ENCRYPTION_KEY=""                   # 32-byte hex key for MFA secret encryption
MAX_SESSIONS="5"                        # Max concurrent sessions per user
SESSION_IDLE_TIMEOUT_MS="900000"       # 15 min idle timeout
SESSION_ABSOLUTE_TIMEOUT_MS="28800000" # 8 hour absolute timeout

# Phase 2: Data Protection
FIELD_ENCRYPTION_KEY=""                 # 32-byte hex key for PII encryption
FIELD_HMAC_KEY=""                       # 32-byte hex key for blind indexes

# Phase 4: Enterprise SSO
NEXT_PUBLIC_APP_URL="https://app.quicktrustapp.com"

# Phase 6: AI Governance
AI_DAILY_TOKEN_LIMIT="500000"          # Daily token budget per org
AI_MONTHLY_TOKEN_LIMIT="10000000"      # Monthly token budget per org

# Phase 7: Infrastructure
CRON_SECRET=""                          # Secret for cron endpoint authentication
S3_BACKUP_BUCKET="quicktrust-backups"  # Backup bucket name
BACKUP_RETENTION_DAYS="30"             # Days to keep backups
APP_VERSION="0.5.0"                    # Application version for health endpoint
```

---

## Summary: New npm Dependencies

```bash
# Phase 0
npm install ioredis

# Phase 1
npm install otpauth qrcode
npm install -D @types/ioredis @types/qrcode

# Phase 4
npm install @node-saml/node-saml

# CI/CD (dev dependencies)
npm install -D @cyclonedx/cyclonedx-npm better-npm-audit license-checker
```

---

## Summary: Prisma Migration Sequence

Run these in order:

```bash
npx prisma migrate dev --name 01-add-account-lockout-fields
npx prisma migrate dev --name 02-add-rbac-permission-model
npx prisma migrate dev --name 03-add-mfa-fields
npx prisma migrate dev --name 04-add-user-lifecycle-fields
npx prisma migrate dev --name 05-extend-session-model
npx prisma migrate dev --name 06-add-soft-delete-fields
npx prisma migrate dev --name 07-add-data-classification
npx prisma migrate dev --name 08-add-security-audit-log
npx prisma migrate dev --name 09-add-sso-configuration
npx prisma migrate dev --name 10-add-compliance-engine
npx prisma migrate dev --name 11-add-incident-management
npx prisma migrate dev --name 12-add-policy-lifecycle
npx prisma migrate dev --name 13-add-risk-register
npx prisma migrate dev --name 14-add-ai-review-fields
npx prisma migrate dev --name 15-add-data-retention-policies
npx prisma migrate dev --name 16-add-dsar-management
npx prisma migrate dev --name 17-add-evidence-integrity-hash
```

---

## Verification Checklist

After completing each phase, validate:

### Phase 0
- [ ] `document.cookie` in browser console does NOT show `auth_token`
- [ ] Logout invalidates the token (reuse returns 401)
- [ ] 6th login attempt in 60 seconds returns 429
- [ ] 6th failed password attempt returns 423 (locked)
- [ ] Password "password123" is rejected at signup
- [ ] S3 objects show SSE-KMS encryption in AWS console
- [ ] Response headers include `Content-Security-Policy`
- [ ] Database connection uses SSL (check `pg_stat_ssl`)

### Phase 1
- [ ] VIEWER role cannot create policies (403)
- [ ] MFA enrollment generates valid QR code
- [ ] Login with MFA returns `mfaRequired: true` first
- [ ] Backup code works and is consumed (single-use)
- [ ] Suspended user cannot log in
- [ ] Session list shows IP and user agent
- [ ] 6th concurrent session revokes the oldest

### Phase 2
- [ ] PII fields stored encrypted in database (check via `psql`)
- [ ] Deleted records still exist with `deleted_at` timestamp
- [ ] Deleted records excluded from normal API queries
- [ ] RESTRICTED data returns 403 for VIEWER role

### Phase 3
- [ ] Login generates `AUTH_LOGIN` audit log entry
- [ ] Failed login generates `AUTH_FAILED` entry
- [ ] Evidence upload generates `DATA_CREATE` entry
- [ ] Health endpoint returns 503 when database is down
- [ ] Audit logs queryable by date range and event type

### Phase 4
- [ ] SAML login redirects to IdP
- [ ] SAML callback creates user via JIT provisioning
- [ ] SCIM POST /Users creates a new user
- [ ] SCIM PATCH with `active: false` deactivates user and revokes sessions

### Phase 5
- [ ] Compliance posture endpoint returns per-framework scores
- [ ] Incident status transitions are logged
- [ ] Policy approval requires different user than uploader
- [ ] Risk register calculates risk scores correctly

### Phase 6
- [ ] AI answers start in `PENDING_REVIEW` status
- [ ] Same user who asked question cannot approve answer (SoD)
- [ ] Token budget check returns 429 when limit exceeded
- [ ] Original AI output preserved after human modification

### Phase 7
- [ ] Backup script creates `.sql.gz` and uploads to S3
- [ ] CI pipeline fails on CRITICAL Semgrep findings
- [ ] Container scan blocks deployment with CRITICAL CVEs
- [ ] SBOM artifact generated on main branch push

### Phase 8
- [ ] Retention policy deletes evidence older than configured days
- [ ] Legal hold prevents deletion of held data
- [ ] DSAR access request returns all user data as JSON
- [ ] DSAR erasure anonymizes user records
- [ ] Evidence hash verification detects tampering
- [ ] Compliance report includes all framework scores

---

*This implementation guide provides production-ready code patterns aligned with QuickTrust's existing Next.js + Prisma + TypeScript architecture. Each section can be implemented independently, though the Phase 0 foundations (Redis, rate limiting, audit logging) are prerequisites for later phases. Estimated total effort: 26-32 engineering weeks with 2 senior engineers working in parallel.*
