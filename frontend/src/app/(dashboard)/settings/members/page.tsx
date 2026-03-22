"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useOrgMembers,
  useOrgInvitations,
  useSendInvitation,
  useRevokeInvitation,
  useResendInvitation,
} from "@/hooks/use-invitations";
import { useOrgId } from "@/hooks/use-org-id";
import { useAuth } from "@/providers/auth-provider";
import {
  Users,
  UserPlus,
  Mail,
  Loader2,
  Clock,
  CheckCircle,
  XCircle,
  RotateCw,
  Trash2,
  AlertTriangle,
  ArrowLeft,
  Ban,
  UserCheck,
} from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import Link from "next/link";
import { toast } from "sonner";

const ROLE_OPTIONS = [
  { value: "compliance_manager", label: "Compliance Manager" },
  { value: "control_owner", label: "Control Owner" },
  { value: "employee", label: "Employee" },
  { value: "executive", label: "Executive" },
  { value: "auditor_internal", label: "Internal Auditor" },
];

const ROLE_COLORS: Record<string, string> = {
  super_admin: "bg-red-100 text-red-800",
  compliance_manager: "bg-blue-100 text-blue-800",
  control_owner: "bg-green-100 text-green-800",
  employee: "bg-gray-100 text-gray-800",
  executive: "bg-amber-100 text-amber-800",
  auditor_internal: "bg-teal-100 text-teal-800",
  auditor_external: "bg-orange-100 text-orange-800",
};

function formatRole(role: string) {
  return role.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function InviteModal({
  open,
  onClose,
  orgId,
}: {
  open: boolean;
  onClose: () => void;
  orgId: string;
}) {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("employee");
  const sendInvite = useSendInvitation(orgId);

  function handleSend() {
    if (!email) return;
    sendInvite.mutate(
      { email, role },
      {
        onSuccess: () => {
          toast.success(`Invitation sent to ${email}`);
          setEmail("");
          setRole("employee");
          onClose();
        },
        onError: (err: any) => {
          toast.error(err.message || "Failed to send invitation");
        },
      }
    );
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="mx-4 w-full max-w-md rounded-xl bg-background text-foreground border p-6 shadow-2xl">
        <h3 className="text-lg font-semibold">Invite Team Member</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Send an invitation link via email. The link is valid for 7 days.
        </p>

        <div className="mt-4 space-y-4">
          <div>
            <label className="text-sm font-medium">Email Address</label>
            <input
              type="email"
              className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
              placeholder="colleague@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
          </div>

          <div>
            <label className="text-sm font-medium">Role</label>
            <select
              className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              {ROLE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-6 flex gap-3 justify-end">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleSend} disabled={!email || sendInvite.isPending}>
            {sendInvite.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Mail className="mr-2 h-4 w-4" />
            )}
            Send Invitation
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function MembersPage() {
  const orgId = useOrgId();
  const { userInfo } = useAuth();
  const [showInviteModal, setShowInviteModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: members, isLoading: membersLoading } = useOrgMembers(orgId);
  const { data: invitations, isLoading: invitationsLoading } = useOrgInvitations(orgId);
  const revokeInvite = useRevokeInvitation(orgId);
  const resendInvite = useResendInvitation(orgId);

  const suspendUser = useMutation({
    mutationFn: (userId: string) =>
      api.post(`/profile/organizations/${orgId}/users/${userId}/suspend`, {}),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["org-members"] });
      toast.success("User suspended");
    },
    onError: (err: any) => toast.error(err.message || "Failed to suspend user"),
  });

  const reactivateUser = useMutation({
    mutationFn: (userId: string) =>
      api.post(`/profile/organizations/${orgId}/users/${userId}/reactivate`, {}),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["org-members"] });
      toast.success("User reactivated");
    },
    onError: (err: any) => toast.error(err.message || "Failed to reactivate user"),
  });

  const isAdmin = userInfo?.role && ["super_admin", "compliance_manager"].includes(userInfo.role);

  if (membersLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  const membersList = members?.items || [];
  const invitationsList = (invitations?.items || []).filter(
    (inv: any) => inv.status === "pending"
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <Link href="/settings">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4" />
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold">Team Members</h1>
              <p className="text-muted-foreground">
                Manage your team and pending invitations
              </p>
            </div>
          </div>
        </div>
        {isAdmin && (
          <Button onClick={() => setShowInviteModal(true)}>
            <UserPlus className="mr-2 h-4 w-4" />
            Invite Member
          </Button>
        )}
      </div>

      {/* Active Members */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-muted-foreground" />
            <CardTitle>
              Active Members ({membersList.length})
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          {membersList.length === 0 ? (
            <p className="text-sm text-muted-foreground py-4 text-center">
              No team members found.
            </p>
          ) : (
            <div className="divide-y">
              {membersList.map((member: any) => (
                <div
                  key={member.id}
                  className="flex items-center justify-between py-3"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10 text-sm font-semibold text-primary">
                      {member.full_name
                        ?.split(" ")
                        .map((n: string) => n[0])
                        .join("")
                        .toUpperCase()
                        .slice(0, 2) || "?"}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{member.full_name}</p>
                      <p className="text-xs text-muted-foreground">
                        {member.email}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        ROLE_COLORS[member.role] || "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {formatRole(member.role)}
                    </span>
                    {!member.is_active && (
                      <Badge variant="destructive">Inactive</Badge>
                    )}
                    {isAdmin && member.id !== userInfo?.id && (
                      member.is_active ? (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => suspendUser.mutate(member.id)}
                          disabled={suspendUser.isPending}
                          title="Suspend user"
                        >
                          <Ban className="h-4 w-4 text-destructive" />
                        </Button>
                      ) : (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => reactivateUser.mutate(member.id)}
                          disabled={reactivateUser.isPending}
                          title="Reactivate user"
                        >
                          <UserCheck className="h-4 w-4 text-green-600" />
                        </Button>
                      )
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Pending Invitations */}
      {isAdmin && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Mail className="h-5 w-5 text-muted-foreground" />
              <CardTitle>
                Pending Invitations ({invitationsList.length})
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            {invitationsLoading ? (
              <Skeleton className="h-20 w-full" />
            ) : invitationsList.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-center">
                <UserPlus className="h-10 w-10 text-muted-foreground/30" />
                <p className="mt-2 text-sm text-muted-foreground">
                  No pending invitations.
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  className="mt-3"
                  onClick={() => setShowInviteModal(true)}
                >
                  <UserPlus className="mr-2 h-4 w-4" />
                  Invite someone
                </Button>
              </div>
            ) : (
              <div className="divide-y">
                {invitationsList.map((inv: any) => {
                  const expiresAt = new Date(inv.expires_at);
                  const daysLeft = Math.max(
                    0,
                    Math.ceil(
                      (expiresAt.getTime() - Date.now()) / (1000 * 60 * 60 * 24)
                    )
                  );

                  return (
                    <div
                      key={inv.id}
                      className="flex items-center justify-between py-3"
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-orange-100 text-sm text-orange-600">
                          <Mail className="h-4 w-4" />
                        </div>
                        <div>
                          <p className="text-sm font-medium">{inv.email}</p>
                          <p className="text-xs text-muted-foreground flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            Expires in {daysLeft} day{daysLeft !== 1 ? "s" : ""}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                            ROLE_COLORS[inv.role] || "bg-gray-100 text-gray-800"
                          }`}
                        >
                          {formatRole(inv.role)}
                        </span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() =>
                            resendInvite.mutate(inv.id, {
                              onSuccess: () =>
                                toast.success(`Invitation resent to ${inv.email}`),
                              onError: (err: any) =>
                                toast.error(err.message || "Failed to resend"),
                            })
                          }
                          title="Resend invitation"
                        >
                          <RotateCw className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() =>
                            revokeInvite.mutate(inv.id, {
                              onSuccess: () =>
                                toast.success("Invitation revoked"),
                              onError: (err: any) =>
                                toast.error(err.message || "Failed to revoke"),
                            })
                          }
                          title="Revoke invitation"
                        >
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      <InviteModal
        open={showInviteModal}
        onClose={() => setShowInviteModal(false)}
        orgId={orgId}
      />
    </div>
  );
}
