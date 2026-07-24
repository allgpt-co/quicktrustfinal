"use client";

import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import api from "@/lib/api";
import { useAuth } from "@/providers/auth-provider";
import { toast } from "sonner";
import { Clock, Globe, Key, Loader2, LogOut, Monitor, Pencil, Save, Shield, User, X } from "lucide-react";

interface Profile {
  id: string;
  email: string;
  full_name: string;
  role: string;
  department: string | null;
  org_id: string;
  is_active: boolean;
  created_at: string;
}

interface Session {
  id: string;
  ip_address: string | null;
  started: string | null;
  last_access: string | null;
  clients: Record<string, string> | null;
}

const TABS = ["profile", "security", "sessions"] as const;
type Tab = (typeof TABS)[number];

const ROLE_COLORS: Record<string, string> = {
  super_admin: "bg-red-500/20 text-red-500 border-red-500/30",
  compliance_manager: "bg-blue-500/20 text-blue-500 border-blue-500/30",
  control_owner: "bg-green-500/20 text-green-500 border-green-500/30",
  employee: "bg-gray-500/20 text-gray-500 border-gray-500/30",
  executive: "bg-amber-500/20 text-amber-500 border-amber-500/30",
  auditor_internal: "bg-teal-500/20 text-teal-500 border-teal-500/30",
  auditor_external: "bg-orange-500/20 text-orange-500 border-orange-500/30",
};

function formatRole(role: string) {
  return role.replace(/_/g, " ").replace(/\b\w/g, (character) => character.toUpperCase());
}

function formatTimestamp(value: string | null): string {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

export default function ProfilePage() {
  const queryClient = useQueryClient();
  const { logout } = useAuth();
  const [tab, setTab] = useState<Tab>("profile");
  const [editing, setEditing] = useState(false);
  const [editName, setEditName] = useState("");
  const [editDepartment, setEditDepartment] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const { data: profile, isLoading: profileLoading } = useQuery<Profile>({
    queryKey: ["profile"],
    queryFn: () => api.get("/profile/me"),
  });
  const { data: sessions, isLoading: sessionsLoading } = useQuery<Session[]>({
    queryKey: ["sessions"],
    queryFn: () => api.get("/profile/sessions"),
    enabled: tab === "sessions",
    refetchInterval: 30000,
  });

  const updateProfile = useMutation({
    mutationFn: (data: { full_name?: string; department?: string }) => api.patch("/profile/me", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["profile"] });
      toast.success("Profile updated");
      setEditing(false);
    },
    onError: (error: Error) => toast.error(error.message || "Failed to update profile"),
  });

  const updatePassword = useMutation({
    mutationFn: () => api.post("/profile/password", { current_password: currentPassword, new_password: newPassword }),
    onSuccess: async () => {
      toast.success("Password updated. Sign in again to continue.");
      await logout();
    },
    onError: (error: Error) => toast.error(error.message || "Failed to update password"),
  });

  const logoutAll = useMutation({
    mutationFn: () => api.post("/profile/sessions/logout-all", {}),
    onSuccess: async () => {
      toast.success("All sessions terminated");
      await logout();
    },
    onError: (error: Error) => toast.error(error.message || "Failed to terminate sessions"),
  });

  const logoutSession = useMutation({
    mutationFn: (id: string) => api.delete(`/profile/sessions/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sessions"] });
      toast.success("Session terminated");
    },
    onError: (error: Error) => toast.error(error.message || "Failed to terminate session"),
  });

  function submitPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (newPassword !== confirmPassword) {
      toast.error("New passwords do not match");
      return;
    }
    updatePassword.mutate();
  }

  if (profileLoading) {
    return <div className="space-y-4"><Skeleton className="h-10 w-48" /><Skeleton className="h-64 w-full" /></div>;
  }

  const initials = profile?.full_name.split(" ").map((name) => name[0]).join("").toUpperCase().slice(0, 2) || "?";

  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold">My Profile</h1><p className="text-muted-foreground">Manage your account, password, and active sessions</p></div>
      <div className="flex w-fit gap-1 rounded-lg bg-muted p-1">
        {TABS.map((item) => (
          <button key={item} onClick={() => setTab(item)} className={`flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors ${tab === item ? "bg-background text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"}`}>
            {item === "profile" ? <User className="h-4 w-4" /> : item === "security" ? <Shield className="h-4 w-4" /> : <Monitor className="h-4 w-4" />}
            {item.charAt(0).toUpperCase() + item.slice(1)}
          </button>
        ))}
      </div>

      {tab === "profile" && profile && (
        <div className="grid gap-6 md:grid-cols-3">
          <Card className="md:col-span-2">
            <CardHeader className="flex-row items-center justify-between">
              <CardTitle>Personal Information</CardTitle>
              {!editing ? (
                <Button variant="outline" size="sm" onClick={() => { setEditName(profile.full_name); setEditDepartment(profile.department || ""); setEditing(true); }}><Pencil className="mr-2 h-4 w-4" />Edit</Button>
              ) : (
                <div className="flex gap-2"><Button size="sm" disabled={updateProfile.isPending} onClick={() => updateProfile.mutate({ full_name: editName, department: editDepartment })}>{updateProfile.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}Save</Button><Button variant="ghost" size="sm" onClick={() => setEditing(false)} aria-label="Cancel editing"><X className="h-4 w-4" /></Button></div>
              )}
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="flex items-center gap-4"><div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-xl font-bold text-primary">{initials}</div><div>{editing ? <input aria-label="Full name" value={editName} onChange={(event) => setEditName(event.target.value)} className="rounded-md border bg-background px-3 py-1.5 text-lg font-semibold" /> : <p className="text-lg font-semibold">{profile.full_name}</p>}<p className="text-sm text-muted-foreground">{profile.email}</p></div></div>
              <div className="grid gap-4 border-t pt-5 sm:grid-cols-2">
                <div><span className="text-xs font-medium text-muted-foreground">Role</span><div className="mt-1"><span className={`inline-flex rounded-full border px-2.5 py-0.5 text-xs font-medium ${ROLE_COLORS[profile.role] || ROLE_COLORS.employee}`}>{formatRole(profile.role)}</span></div></div>
                <div><label htmlFor="department" className="text-xs font-medium text-muted-foreground">Department</label>{editing ? <input id="department" value={editDepartment} onChange={(event) => setEditDepartment(event.target.value)} placeholder="Engineering, Sales, etc." className="mt-1 w-full rounded-md border bg-background px-3 py-1.5 text-sm" /> : <p className="mt-1 text-sm">{profile.department || "Not set"}</p>}</div>
                <div><span className="text-xs font-medium text-muted-foreground">Member since</span><p className="mt-1 text-sm">{new Date(profile.created_at).toLocaleDateString()}</p></div>
                <div><span className="text-xs font-medium text-muted-foreground">Status</span><div className="mt-1">{profile.is_active ? <Badge className="bg-green-500/20 text-green-500 border-green-500/30">Active</Badge> : <Badge variant="destructive">Suspended</Badge>}</div></div>
              </div>
            </CardContent>
          </Card>
          <Card><CardHeader><CardTitle>Quick Actions</CardTitle></CardHeader><CardContent className="space-y-3"><Button variant="outline" className="w-full justify-start" onClick={() => setTab("security")}><Key className="mr-2 h-4 w-4" />Change Password</Button><Button variant="outline" className="w-full justify-start" onClick={() => setTab("sessions")}><Monitor className="mr-2 h-4 w-4" />Active Sessions</Button></CardContent></Card>
        </div>
      )}

      {tab === "security" && (
        <Card className="max-w-2xl"><CardHeader><div className="flex items-center gap-2"><Key className="h-5 w-5 text-muted-foreground" /><CardTitle>Change Password</CardTitle></div></CardHeader><CardContent><p className="mb-5 text-sm text-muted-foreground">Changing your password signs out every active device. Use at least 12 characters with upper/lowercase, a number, and a symbol.</p><form onSubmit={submitPassword} className="max-w-md space-y-4"><div><label htmlFor="current-password" className="text-sm font-medium">Current password</label><input id="current-password" type="password" autoComplete="current-password" required value={currentPassword} onChange={(event) => setCurrentPassword(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" /></div><div><label htmlFor="new-password" className="text-sm font-medium">New password</label><input id="new-password" type="password" autoComplete="new-password" minLength={12} required value={newPassword} onChange={(event) => setNewPassword(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" /></div><div><label htmlFor="confirm-password" className="text-sm font-medium">Confirm new password</label><input id="confirm-password" type="password" autoComplete="new-password" minLength={12} required value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" /></div><Button type="submit" disabled={updatePassword.isPending}>{updatePassword.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}Update Password</Button></form></CardContent></Card>
      )}

      {tab === "sessions" && (
        <Card><CardHeader className="flex-row items-center justify-between"><div className="flex items-center gap-2"><Monitor className="h-5 w-5 text-muted-foreground" /><CardTitle>Active Sessions</CardTitle></div><Button variant="destructive" size="sm" onClick={() => logoutAll.mutate()} disabled={logoutAll.isPending}>{logoutAll.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <LogOut className="mr-2 h-4 w-4" />}Sign Out All Devices</Button></CardHeader><CardContent>{sessionsLoading ? <div className="space-y-3"><Skeleton className="h-16 w-full" /><Skeleton className="h-16 w-full" /></div> : !sessions?.length ? <p className="py-8 text-center text-sm text-muted-foreground">No active sessions found.</p> : <div className="divide-y">{sessions.map((session) => <div key={session.id} className="flex items-center justify-between py-4"><div className="flex min-w-0 items-center gap-4"><div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-muted"><Globe className="h-5 w-5 text-muted-foreground" /></div><div className="min-w-0"><p className="text-sm font-medium">{session.ip_address || "Unknown IP"}</p><p className="truncate text-xs text-muted-foreground">{session.clients?.user_agent || "Unknown browser"}</p><p className="flex items-center gap-1 text-xs text-muted-foreground"><Clock className="h-3 w-3" />Last active: {formatTimestamp(session.last_access)}</p></div></div><Button variant="ghost" size="sm" onClick={() => logoutSession.mutate(session.id)} disabled={logoutSession.isPending} aria-label="Terminate session"><LogOut className="h-4 w-4 text-destructive" /></Button></div>)}</div>}</CardContent></Card>
      )}
    </div>
  );
}
