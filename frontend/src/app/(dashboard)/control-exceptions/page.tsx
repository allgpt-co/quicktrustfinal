"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useControlExceptions,
  useCreateControlException,
  useApproveControlException,
  useDenyControlException,
  useRevokeControlException,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { ShieldOff, Plus, Loader2, Check, X, Ban } from "lucide-react";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Pending", value: "pending" },
  { label: "Approved", value: "approved" },
  { label: "Denied", value: "denied" },
  { label: "Expired", value: "expired" },
  { label: "Revoked", value: "revoked" },
];

const statusColor: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  approved: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  denied: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  expired: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
  revoked: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
};

export default function ControlExceptionsPage() {
  const orgId = useOrgId();
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined);
  const [showCreate, setShowCreate] = useState(false);
  const [denyingId, setDenyingId] = useState<string | null>(null);
  const [denialReason, setDenialReason] = useState("");
  const [form, setForm] = useState({
    control_id: "",
    title: "",
    reason: "",
    compensating_control: "",
    risk_acceptance: "",
  });

  const { data, isLoading } = useControlExceptions(orgId, { status: statusFilter });
  const createException = useCreateControlException(orgId);
  const approveException = useApproveControlException(orgId);
  const denyException = useDenyControlException(orgId);
  const revokeException = useRevokeControlException(orgId);

  const exceptions = data?.items || [];

  const resetForm = () =>
    setForm({ control_id: "", title: "", reason: "", compensating_control: "", risk_acceptance: "" });

  const handleCreate = () => {
    if (!form.title.trim()) return;
    createException.mutate(form, {
      onSuccess: () => {
        setShowCreate(false);
        resetForm();
      },
    });
  };

  const handleApprove = (id: string) => {
    const expiresAt = new Date();
    expiresAt.setMonth(expiresAt.getMonth() + 3);
    approveException.mutate({ exceptionId: id, expires_at: expiresAt.toISOString() });
  };

  const handleDeny = (id: string) => {
    if (!denialReason.trim()) return;
    denyException.mutate(
      { exceptionId: id, denial_reason: denialReason },
      { onSuccess: () => { setDenyingId(null); setDenialReason(""); } }
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Control Exceptions</h1>
          <p className="text-muted-foreground">
            Manage waivers and exceptions for non-compliant controls
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          Request Exception
        </Button>
      </div>

      {/* Stats */}
      {data && (
        <div className="grid grid-cols-5 gap-4">
          {["pending", "approved", "denied", "expired", "revoked"].map((s) => (
            <Card key={s}>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">
                  {(data.items || []).filter((e: any) => e.status === s).length}
                </div>
                <div className="text-xs text-muted-foreground capitalize">{s}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Create form */}
      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-4">
            <h2 className="text-lg font-semibold">Request Control Exception</h2>
            <div className="space-y-1">
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g., MFA exception for legacy system"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium">Reason</label>
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Why is this exception needed?"
                rows={2}
                value={form.reason}
                onChange={(e) => setForm({ ...form, reason: e.target.value })}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Compensating Control</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="What alternative measures are in place?"
                  value={form.compensating_control}
                  onChange={(e) => setForm({ ...form, compensating_control: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium">Risk Acceptance</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="Who accepted the risk?"
                  value={form.risk_acceptance}
                  onChange={(e) => setForm({ ...form, risk_acceptance: e.target.value })}
                />
              </div>
            </div>
            <div className="flex items-center gap-2 pt-2">
              <Button onClick={handleCreate} disabled={!form.title.trim() || createException.isPending}>
                {createException.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Submit Request
              </Button>
              <Button variant="outline" onClick={() => { setShowCreate(false); resetForm(); }}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        {STATUS_FILTERS.map((f) => (
          <Button
            key={f.label}
            variant={statusFilter === f.value ? "default" : "outline"}
            size="sm"
            onClick={() => setStatusFilter(f.value)}
          >
            {f.label}
          </Button>
        ))}
      </div>

      {/* List */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-28 w-full rounded-xl" />
          ))}
        </div>
      ) : exceptions.length > 0 ? (
        <div className="space-y-3">
          {exceptions.map((exc: any) => (
            <Card key={exc.id}>
              <CardContent className="p-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3 flex-1">
                    <ShieldOff className="h-6 w-6 text-muted-foreground shrink-0 mt-0.5" />
                    <div className="min-w-0 flex-1">
                      <div className="font-medium">{exc.title}</div>
                      <div className="mt-1 text-sm text-muted-foreground">{exc.reason}</div>
                      {exc.compensating_control && (
                        <div className="mt-1 text-xs text-muted-foreground">
                          <span className="font-medium">Compensating:</span> {exc.compensating_control}
                        </div>
                      )}
                      {exc.denial_reason && (
                        <div className="mt-1 text-xs text-red-600">
                          <span className="font-medium">Denied:</span> {exc.denial_reason}
                        </div>
                      )}
                      {exc.expires_at && (
                        <div className="mt-1 text-xs text-muted-foreground">
                          Expires: {new Date(exc.expires_at).toLocaleDateString()}
                        </div>
                      )}
                      <div className="mt-1 text-xs text-muted-foreground">
                        Created: {new Date(exc.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <Badge className={statusColor[exc.status] || ""}>{exc.status}</Badge>
                    {exc.status === "pending" && (
                      <>
                        <Button
                          size="sm"
                          variant="outline"
                          className="text-green-600"
                          onClick={() => handleApprove(exc.id)}
                          disabled={approveException.isPending}
                        >
                          <Check className="h-4 w-4 mr-1" />
                          Approve
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          className="text-red-600"
                          onClick={() => setDenyingId(exc.id)}
                        >
                          <X className="h-4 w-4 mr-1" />
                          Deny
                        </Button>
                      </>
                    )}
                    {exc.status === "approved" && (
                      <Button
                        size="sm"
                        variant="outline"
                        className="text-orange-600"
                        onClick={() => revokeException.mutate(exc.id)}
                        disabled={revokeException.isPending}
                      >
                        <Ban className="h-4 w-4 mr-1" />
                        Revoke
                      </Button>
                    )}
                  </div>
                </div>
                {denyingId === exc.id && (
                  <div className="mt-3 flex gap-2">
                    <input
                      type="text"
                      className="flex-1 rounded-md border bg-background p-2 text-sm"
                      placeholder="Reason for denial..."
                      value={denialReason}
                      onChange={(e) => setDenialReason(e.target.value)}
                    />
                    <Button size="sm" onClick={() => handleDeny(exc.id)} disabled={!denialReason.trim()}>
                      Confirm Deny
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => { setDenyingId(null); setDenialReason(""); }}>
                      Cancel
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <ShieldOff className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No control exceptions</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No exceptions match the current filters, or none have been requested yet.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
