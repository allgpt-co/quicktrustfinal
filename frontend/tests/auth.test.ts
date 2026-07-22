import { afterEach, describe, expect, test, vi } from "vitest";
import { fetchCurrentUser, refreshSession, registerAccount, signIn } from "@/lib/auth";

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

describe("application authentication client", () => {
  afterEach(() => vi.unstubAllGlobals());

  test("signs in with the compatible username field and includes credentials", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ access_token: "access", token_type: "bearer", expires_in: 900 }));
    vi.stubGlobal("fetch", fetchMock);
    await signIn("person@example.com", "Strong Password 9!");
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/auth/token",
      expect.objectContaining({
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ username: "person@example.com", password: "Strong Password 9!" }),
      })
    );
  });

  test("passes an invitation through application registration", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ access_token: "access", token_type: "bearer" }));
    vi.stubGlobal("fetch", fetchMock);
    await registerAccount({
      email: "invitee@example.com",
      full_name: "Invitee User",
      password: "Strong Password 9!",
      invitation_token: "invite-token",
    });
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toMatchObject({ invitation_token: "invite-token" });
  });

  test("refreshes with the HttpOnly cookie and loads the current user with the access token", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(jsonResponse({ access_token: "rotated", token_type: "bearer" }))
      .mockResolvedValueOnce(jsonResponse({ id: "user-id", email: "person@example.com", full_name: "Person", role: "employee", org_id: "org-id" }));
    vi.stubGlobal("fetch", fetchMock);
    await refreshSession();
    await fetchCurrentUser("rotated");
    expect(fetchMock.mock.calls[0][1]).toMatchObject({ method: "POST", credentials: "include" });
    expect(fetchMock.mock.calls[1][1].headers).toMatchObject({ Authorization: "Bearer rotated" });
  });

  test("surfaces safe backend authentication errors", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({ detail: "Invalid email or password" }, 401)));
    await expect(signIn("person@example.com", "wrong")).rejects.toThrow("Invalid email or password");
  });
});
