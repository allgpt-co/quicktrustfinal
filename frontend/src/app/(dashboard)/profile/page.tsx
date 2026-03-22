"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import api from "@/lib/api";
import { useAuth } from "@/providers/auth-provider";
import { toast } from "sonner";
import {
  User,
  Shield,
  Monitor,
  LogOut,
  Key,
  Pencil,
  Save,
  X,
  CheckCircle,
  XCircle,
  Loader2,
  Smartphone,
  Globe,
  Clock,
} from "lucide-react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface Profile {
  id: string;
  email: string;
  full_name: string;
  role: string;
  department: string | null;
  org_id: string;
  is_active: boolean;
  mfa_enabled: boolean;
  created_at: string;
}

interface MfaStatus {
  mfa_enabled: boolean;
  mfa_type: string | null;
  credential_id: string | null;
}

interface Session {
  id: string;
  ip_address: string | null;
  started: string | null;
  last_access: string | null;
  clients: Record<string, string> | null;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const ROLE_COLORS: Record<string, string> = {
  super_admin: "bg-red-500/20 text-red-400 border-red-500/30",
  compliance_manager: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  control_owner: "bg-green-500/20 text-green-400 border-green-500/30",
  employee: "bg-gray-500/20 text-gray-400 border-gray-500/30",
  executive: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  auditor_internal: "bg-teal-500/20 text-teal-400 border-teal-500/30",
  auditor_external: "bg-orange-500/20 text-orange-400 border-orange-500/30",
};

function formatRole(role: string) {
  return role.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatTimestamp(ts: string | null): string {
  if (!ts) return "—";
  const n = Number(ts);
  const d = n > 1e12 ? new Date(n) : new Date(ts);
  if (isNaN(d.getTime())) return ts;
  return d.toLocaleString();
}

// ---------------------------------------------------------------------------
// Tab definitions
// ---------------------------------------------------------------------------

const TABS = ["profile", "security", "sessions"] as const;
type Tab = (typeof TABS)[number];

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function ProfilePage() {
  const qc = useQueryClient();
  const { userInfo } = useAuth();
  const [tab, setTab] = useState<Tab>("profile");
  const [editing, setEditing] = useState(false);
  const [editName, setEditName] = useState("");
  const [editDept, setEditDept] = useState("");

  // --- Queries ---
  const { data: profile, isLoading: profileLoading } = useQuery<Profile>({
    queryKey: ["profile"],
    queryFn: () => api.get("/profile/me"),
  });

  const { data: mfa, isLoading: mfaLoading } = useQuery<MfaStatus>({
    queryKey: ["mfa-status"],
    queryFn: () => api.get("/profile/mfa"),
    enabled: tab === "security",
  });

  const { data: sessions, isLoading: sessionsLoading } = useQuery<Session[]>({
    queryKey: ["sessions"],
    queryFn: () => api.get("/profile/sessions"),
    enabled: tab === "sessions",
    refetchInterval: 30000,
  });

  // --- Mutations ---
  const updateProfile = useMutation({
    mutationFn: (data: { full_name?: string; department?: string }) =>
      api.patch("/profile/me", data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["profile"] });
      toast.success("Profile updated");
      setEditing(false);
    },
    onError: () => toast.error("Failed to update profile"),
  });

  const enableMfa = useMutation({
    mutationFn: () => api.post("/profile/mfa/enable", {}),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["mfa-status"] });
      toast.success(
        "MFA enabled! You will be prompted to set up TOTP on your next login."
      );
    },
    onError: () => toast.error("Failed to enable MFA"),
  });

  const disableMfa = useMutation({
    mutationFn: () => api.post("/profile/mfa/disable", {}),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["mfa-status"] });
      toast.success("MFA disabled");
    },
    onError: () => toast.error("Failed to disable MFA"),
  });

  const logoutAll = useMutation({
    mutationFn: () => api.post("/profile/sessions/logout-all", {}),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["sessions"] });
      toast.success("All sessions terminated");
    },
    onError: () => toast.error("Failed to terminate sessions"),
  });

  const logoutSession = useMutation({
    mutationFn: (id: string) => api.delete(`/profile/sessions/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["sessions"] });
      toast.success("Session terminated");
    },
    onError: () => toast.error("Failed to terminate session"),
  });

  // --- Loading state ---
  if (profileLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  const initials = profile?.full_name
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2) || "?";

  // Direct link to Keycloak password change (uses the login-actions flow which works with existing session)
  const keycloakPasswordUrl = `${
    process.env.NEXT_PUBLIC_KEYCLOAK_URL || "http://localhost:8080"
  }/realms/${
    process.env.NEXT_PUBLIC_KEYCLOAK_REALM || "quicktrust"
  }/protocol/openid-connect/auth?client_id=quicktrust-web&redirect_uri=${encodeURIComponent("http://localhost:3001/profile")}&response_type=code&scope=openid&kc_action=UPDATE_PASSWORD`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">My Profile</h1>
        <p className="text-muted-foreground">
          Manage your account, security, and sessions
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 rounded-lg bg-muted p-1 w-fit">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors ${
              tab === t
                ? "bg-background text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t === "profile" && <User className="h-4 w-4" />}
            {t === "security" && <Shield className="h-4 w-4" />}
            {t === "sessions" && <Monitor className="h-4 w-4" />}
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {/* ================================================================ */}
      {/* PROFILE TAB                                                      */}
      {/* ================================================================ */}
      {tab === "profile" && profile && (
        <div className="grid gap-6 md:grid-cols-3">
          {/* Info card */}
          <Card className="md:col-span-2">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Personal Information</CardTitle>
              {!editing ? (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setEditName(profile.full_name);
                    setEditDept(profile.department || "");
                    setEditing(true);
                  }}
                >
                  <Pencil className="mr-2 h-4 w-4" />
                  Edit
                </Button>
              ) : (
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    onClick={() =>
                      updateProfile.mutate({
                        full_name: editName,
                        department: editDept,
                      })
                    }
                    disabled={updateProfile.isPending}
                  >
                    {updateProfile.isPending ? (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    ) : (
                      <Save className="mr-2 h-4 w-4" />
                    )}
                    Save
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setEditing(false)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-xl font-bold text-primary">
                  {initials}
                </div>
                <div>
                  {editing ? (
                    <input
                      className="rounded-md border bg-background px-3 py-1.5 text-lg font-semibold"
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                    />
                  ) : (
                    <p className="text-lg font-semibold">{profile.full_name}</p>
                  )}
                  <p className="text-sm text-muted-foreground">
                    {profile.email}
                  </p>
                </div>
              </div>

              <div className="grid gap-4 pt-4 sm:grid-cols-2">
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Role
                  </label>
                  <div className="mt-1">
                    <span
                      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${
                        ROLE_COLORS[profile.role] || "bg-gray-500/20 text-gray-400"
                      }`}
                    >
                      {formatRole(profile.role)}
                    </span>
                  </div>
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Department
                  </label>
                  {editing ? (
                    <input
                      className="mt-1 w-full rounded-md border bg-background px-3 py-1.5 text-sm"
                      value={editDept}
                      onChange={(e) => setEditDept(e.target.value)}
                      placeholder="Engineering, Sales, etc."
                    />
                  ) : (
                    <p className="mt-1 text-sm">
                      {profile.department || "Not set"}
                    </p>
                  )}
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Member Since
                  </label>
                  <p className="mt-1 text-sm">
                    {new Date(profile.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Status
                  </label>
                  <div className="mt-1">
                    {profile.is_active ? (
                      <Badge className="bg-green-500/20 text-green-400 border-green-500/30">
                        Active
                      </Badge>
                    ) : (
                      <Badge variant="destructive">Suspended</Badge>
                    )}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick actions card */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() =>
                  window.open(keycloakPasswordUrl, "_blank")
                }
              >
                <Key className="mr-2 h-4 w-4" />
                Change Password
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => setTab("security")}
              >
                <Shield className="mr-2 h-4 w-4" />
                Security Settings
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={() => setTab("sessions")}
              >
                <Monitor className="mr-2 h-4 w-4" />
                Active Sessions
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {/* ================================================================ */}
      {/* SECURITY TAB                                                     */}
      {/* ================================================================ */}
      {tab === "security" && (
        <div className="grid gap-6 md:grid-cols-2">
          {/* MFA card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Smartphone className="h-5 w-5 text-muted-foreground" />
                <CardTitle>Two-Factor Authentication</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {mfaLoading ? (
                <Skeleton className="h-20 w-full" />
              ) : mfa?.mfa_enabled ? (
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="font-medium text-green-500">
                      MFA is enabled
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Your account is protected with TOTP-based two-factor
                    authentication.
                  </p>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => disableMfa.mutate()}
                    disabled={disableMfa.isPending}
                  >
                    {disableMfa.isPending && (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    )}
                    Disable MFA
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    <XCircle className="h-5 w-5 text-yellow-500" />
                    <span className="font-medium text-yellow-500">
                      MFA is not enabled
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Add an extra layer of security to your account. Once
                    enabled, you&apos;ll be prompted to set up TOTP using an
                    authenticator app (Google Authenticator, Authy, etc.) on
                    your next login.
                  </p>
                  <Button
                    onClick={() => enableMfa.mutate()}
                    disabled={enableMfa.isPending}
                  >
                    {enableMfa.isPending && (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    )}
                    <Shield className="mr-2 h-4 w-4" />
                    Enable Two-Factor Authentication
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Password card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Key className="h-5 w-5 text-muted-foreground" />
                <CardTitle>Password</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Password changes are managed through Keycloak. Click below to
                open your account security settings.
              </p>
              <Button
                variant="outline"
                onClick={() =>
                  window.open(
                    `${keycloakPasswordUrl}/#/security/signingin`,
                    "_blank"
                  )
                }
              >
                <Key className="mr-2 h-4 w-4" />
                Change Password
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {/* ================================================================ */}
      {/* SESSIONS TAB                                                     */}
      {/* ================================================================ */}
      {tab === "sessions" && (
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <Monitor className="h-5 w-5 text-muted-foreground" />
              <CardTitle>Active Sessions</CardTitle>
            </div>
            <Button
              variant="destructive"
              size="sm"
              onClick={() => logoutAll.mutate()}
              disabled={logoutAll.isPending}
            >
              {logoutAll.isPending ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <LogOut className="mr-2 h-4 w-4" />
              )}
              Sign Out All Devices
            </Button>
          </CardHeader>
          <CardContent>
            {sessionsLoading ? (
              <div className="space-y-3">
                <Skeleton className="h-16 w-full" />
                <Skeleton className="h-16 w-full" />
              </div>
            ) : !sessions || sessions.length === 0 ? (
              <p className="py-8 text-center text-sm text-muted-foreground">
                No active sessions found.
              </p>
            ) : (
              <div className="divide-y">
                {sessions.map((s) => (
                  <div
                    key={s.id}
                    className="flex items-center justify-between py-4"
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
                        <Globe className="h-5 w-5 text-muted-foreground" />
                      </div>
                      <div>
                        <p className="text-sm font-medium">
                          {s.ip_address || "Unknown IP"}
                        </p>
                        <div className="flex items-center gap-3 text-xs text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            Last active: {formatTimestamp(s.last_access)}
                          </span>
                          {s.clients && Object.keys(s.clients).length > 0 && (
                            <span>
                              Apps:{" "}
                              {Object.values(s.clients).join(", ")}
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground">
                          Started: {formatTimestamp(s.started)}
                        </p>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => logoutSession.mutate(s.id)}
                      disabled={logoutSession.isPending}
                      title="Terminate this session"
                    >
                      <LogOut className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
