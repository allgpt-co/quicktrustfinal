"use client";

import { useAuth } from "@/providers/auth-provider";

/**
 * Returns the current organization ID.
 * Uses the authenticated application user and falls back to the demo org ID only in local development.
 */

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

export function useOrgId(): string {
  const { userInfo } = useAuth();
  return userInfo?.org_id ?? DEMO_ORG_ID;
}

export { DEMO_ORG_ID };
