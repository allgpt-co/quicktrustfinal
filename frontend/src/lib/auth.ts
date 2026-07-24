import { API_URL } from "@/lib/public-env";

export interface TokenResponse {
  access_token: string;
  refresh_token?: string | null;
  token_type: string;
  expires_in?: number | null;
}

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: string;
  org_id: string | null;
}

async function authRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}/api/v1${path}`, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }));
    const detail = body.detail;
    const message = Array.isArray(detail)
      ? detail.map((item: { msg?: string }) => item.msg || "Invalid request").join("; ")
      : typeof detail === "string"
        ? detail
        : `Authentication request failed (${response.status})`;
    throw new Error(message);
  }
  return response.json();
}

export function signIn(email: string, password: string): Promise<TokenResponse> {
  return authRequest("/auth/token", {
    method: "POST",
    body: JSON.stringify({ username: email, password }),
  });
}

export function registerAccount(input: {
  email: string;
  full_name: string;
  password: string;
  invitation_token?: string;
}): Promise<TokenResponse> {
  return authRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function refreshSession(): Promise<TokenResponse> {
  return authRequest("/auth/refresh", { method: "POST" });
}

export async function fetchCurrentUser(accessToken: string): Promise<AuthUser> {
  return authRequest("/auth/me", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export async function revokeSession(accessToken: string): Promise<void> {
  await authRequest("/auth/logout", {
    method: "POST",
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export async function requestPasswordReset(email: string): Promise<void> {
  await authRequest("/auth/password/forgot", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function resetPassword(token: string, newPassword: string): Promise<void> {
  await authRequest("/auth/password/reset", {
    method: "POST",
    body: JSON.stringify({ token, new_password: newPassword }),
  });
}
