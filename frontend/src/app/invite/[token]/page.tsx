"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/providers/auth-provider";
import api from "@/lib/api";
import { API_URL } from "@/lib/public-env";
import { Shield, Loader2, CheckCircle, XCircle, Clock } from "lucide-react";

interface InviteInfo {
  org_name: string;
  inviter_name: string;
  role: string;
  email: string;
  status: string;
  expires_at: string;
  is_expired: boolean;
}

export default function InviteAcceptPage() {
  const params = useParams();
  const router = useRouter();
  const token = params.token as string;
  const { authenticated, loading: authLoading, login } = useAuth();

  const [invite, setInvite] = useState<InviteInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [accepting, setAccepting] = useState(false);
  const [accepted, setAccepted] = useState(false);

  // Validate invitation token
  useEffect(() => {
    if (!token) return;
    setLoading(true);
    fetch(`${API_URL}/api/v1/invitations/validate/${token}`)
      .then(async (res) => {
        if (!res.ok) {
          const err = await res.json().catch(() => ({ detail: "Invalid invitation" }));
          throw new Error(err.detail || "Invalid invitation link");
        }
        return res.json();
      })
      .then((data) => {
        setInvite(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  // Accept invitation
  async function handleAccept() {
    setAccepting(true);
    try {
      await api.post(`/invitations/accept/${token}`);
      setAccepted(true);
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 2000);
    } catch (err: any) {
      setError(err.message || "Failed to accept invitation");
      setAccepting(false);
    }
  }

  function formatRole(role: string) {
    return role.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  }

  // Loading state
  if (loading || authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <Loader2 className="mx-auto h-8 w-8 animate-spin text-blue-600" />
          <p className="mt-4 text-gray-600">Validating invitation...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="mx-auto max-w-md rounded-xl bg-white p-8 shadow-lg text-center">
          <XCircle className="mx-auto h-12 w-12 text-red-500" />
          <h2 className="mt-4 text-xl font-bold text-gray-900">Invitation Error</h2>
          <p className="mt-2 text-gray-600">{error}</p>
          <button
            onClick={() => (window.location.href = "/")}
            className="mt-6 rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
          >
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  // Accepted state
  if (accepted) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="mx-auto max-w-md rounded-xl bg-white p-8 shadow-lg text-center">
          <CheckCircle className="mx-auto h-12 w-12 text-green-500" />
          <h2 className="mt-4 text-xl font-bold text-gray-900">Welcome!</h2>
          <p className="mt-2 text-gray-600">
            You have joined <strong>{invite?.org_name}</strong> as{" "}
            <strong>{formatRole(invite?.role || "")}</strong>.
          </p>
          <p className="mt-4 text-sm text-gray-500">Redirecting to dashboard...</p>
        </div>
      </div>
    );
  }

  // Expired / already used
  if (invite?.is_expired) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="mx-auto max-w-md rounded-xl bg-white p-8 shadow-lg text-center">
          <Clock className="mx-auto h-12 w-12 text-yellow-500" />
          <h2 className="mt-4 text-xl font-bold text-gray-900">
            {invite.status === "accepted"
              ? "Invitation Already Used"
              : invite.status === "revoked"
              ? "Invitation Revoked"
              : "Invitation Expired"}
          </h2>
          <p className="mt-2 text-gray-600">
            {invite.status === "accepted"
              ? "This invitation has already been accepted."
              : invite.status === "revoked"
              ? "This invitation has been revoked by the admin."
              : "This invitation has expired. Please ask your admin to send a new one."}
          </p>
          <button
            onClick={() => (window.location.href = "/")}
            className="mt-6 rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
          >
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  // Valid invitation — show accept UI
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="mx-auto max-w-md rounded-xl bg-white p-8 shadow-lg">
        <div className="text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-100">
            <Shield className="h-8 w-8 text-blue-600" />
          </div>
          <h1 className="mt-4 text-2xl font-bold text-gray-900">
            You&apos;re Invited!
          </h1>
          <p className="mt-2 text-gray-600">
            <strong>{invite?.inviter_name}</strong> has invited you to join
          </p>
        </div>

        <div className="mt-6 rounded-lg bg-gray-50 p-4">
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Organization</span>
              <span className="text-sm font-semibold text-gray-900">
                {invite?.org_name}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Your Role</span>
              <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
                {formatRole(invite?.role || "")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Email</span>
              <span className="text-sm text-gray-900">{invite?.email}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Expires</span>
              <span className="text-sm text-gray-900">
                {new Date(invite?.expires_at || "").toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>

        <div className="mt-6 space-y-3">
          {authenticated ? (
            <button
              onClick={handleAccept}
              disabled={accepting}
              className="w-full rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {accepting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Joining...
                </>
              ) : (
                "Accept Invitation"
              )}
            </button>
          ) : (
            <>
              <button
                onClick={() => login()}
                className="w-full rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700"
              >
                Sign In to Accept
              </button>
              <p className="text-center text-xs text-gray-500">
                Don&apos;t have an account? Register on the sign-in page, then come back to this link.
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
