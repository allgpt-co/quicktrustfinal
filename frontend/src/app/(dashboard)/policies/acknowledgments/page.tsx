"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  usePolicies,
  usePolicyAcknowledgments,
  useCreatePolicyAcknowledgment,
  useAcknowledgePolicy,
  useMyPendingAcknowledgments,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { useAuth } from "@/providers/auth-provider";
import { ClipboardSignature, Plus, Loader2, CheckCircle, AlertCircle, UserCircle } from "lucide-react";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Pending", value: "pending" },
  { label: "Acknowledged", value: "acknowledged" },
  { label: "Overdue", value: "overdue" },
];

const statusColor: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  acknowledged: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  overdue: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

export default function PolicyAcknowledgmentsPage() {
  const orgId = useOrgId();
  const { userInfo } = useAuth();
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined);
  const [showCreate, setShowCreate] = useState(false);
  const [activeTab, setActiveTab] = useState<"all" | "my-pending">("all");
  const [form, setForm] = useState({ policy_id: "", user_id: "", due_date: "" });

  const { data: policiesData } = usePolicies(orgId);
  const { data, isLoading } = usePolicyAcknowledgments(orgId, { status: statusFilter });
  const { data: myPending, isLoading: pendingLoading } = useMyPendingAcknowledgments(orgId);
  const createAcknowledgment = useCreatePolicyAcknowledgment(orgId);
  const acknowledgePolicy = useAcknowledgePolicy(orgId);
  const [createError, setCreateError] = useState<string | null>(null);
  const [ackError, setAckError] = useState<string | null>(null);

  const policies = policiesData?.items || [];
  const acknowledgments = data?.items || [];
  const pendingItems = myPending || [];

  const handleCreate = () => {
    if (!form.policy_id) {
      setCreateError("Please select a policy.");
      return;
    }
    if (!form.user_id.trim()) {
      setCreateError("Please enter a User ID.");
      return;
    }
    setCreateError(null);
    createAcknowledgment.mutate(
      { ...form, due_date: form.due_date ? new Date(form.due_date).toISOString() : undefined },
      {
        onSuccess: () => {
          setShowCreate(false);
          setForm({ policy_id: "", user_id: "", due_date: "" });
          setCreateError(null);
        },
        onError: (err: any) => {
          setCreateError(err?.message || "Failed to create acknowledgment request. Check that the User ID is a valid UUID.");
        },
      }
    );
  };

  const handleAcknowledge = (id: string) => {
    setAckError(null);
    acknowledgePolicy.mutate(
      { acknowledgmentId: id, notes: "Acknowledged via UI" },
      {
        onError: (err: any) => {
          setAckError(err?.message || "Failed to acknowledge. Please try again.");
        },
      }
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Policy Acknowledgments</h1>
          <p className="text-muted-foreground">
            Track employee policy sign-offs and compliance
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          Request Acknowledgment
        </Button>
      </div>

      {/* Stats */}
      {data && (
        <div className="grid grid-cols-3 gap-4">
          {["pending", "acknowledged", "overdue"].map((s) => (
            <Card key={s}>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">
                  {acknowledgments.filter((a: any) => a.status === s).length}
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
            <h2 className="text-lg font-semibold">Request Policy Acknowledgment</h2>

            {createError && (
              <div className="flex items-center gap-2 rounded-md border border-destructive bg-destructive/10 p-3 text-sm text-destructive">
                <AlertCircle className="h-4 w-4 shrink-0" />
                {createError}
              </div>
            )}

            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Policy</label>
                {policies.length > 0 ? (
                  <select
                    className="w-full rounded-md border bg-background p-2 text-sm"
                    value={form.policy_id}
                    onChange={(e) => { setForm({ ...form, policy_id: e.target.value }); setCreateError(null); }}
                  >
                    <option value="">Select a policy...</option>
                    {policies.map((p: any) => (
                      <option key={p.id} value={p.id}>
                        {p.title} (v{p.version || "1.0"})
                      </option>
                    ))}
                  </select>
                ) : (
                  <div className="rounded-md border bg-muted p-2 text-sm text-muted-foreground">
                    No policies found. Create a policy first.
                  </div>
                )}
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium">User ID</label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    className="flex-1 rounded-md border bg-background p-2 text-sm font-mono"
                    placeholder="Application user UUID"
                    value={form.user_id}
                    onChange={(e) => { setForm({ ...form, user_id: e.target.value }); setCreateError(null); }}
                  />
                  {userInfo?.id && (
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      className="shrink-0"
                      onClick={() => { setForm({ ...form, user_id: userInfo.id! }); setCreateError(null); }}
                    >
                      <UserCircle className="mr-1 h-4 w-4" />
                      Me
                    </Button>
                  )}
                </div>
                <p className="text-[11px] text-muted-foreground">
                  Click &quot;Me&quot; to use your own ID, or paste a UUID from the Members page
                </p>
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium">Due Date</label>
                <input
                  type="date"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.due_date}
                  onChange={(e) => setForm({ ...form, due_date: e.target.value })}
                />
              </div>
            </div>
            <div className="flex items-center gap-2 pt-2">
              <Button onClick={handleCreate} disabled={!form.policy_id || createAcknowledgment.isPending}>
                {createAcknowledgment.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Send Request
              </Button>
              <Button variant="outline" onClick={() => { setShowCreate(false); setCreateError(null); }}>Cancel</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tabs */}
      <div className="flex gap-2 border-b pb-1">
        <Button
          variant={activeTab === "all" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("all")}
        >
          All Acknowledgments
        </Button>
        <Button
          variant={activeTab === "my-pending" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("my-pending")}
        >
          My Pending ({pendingItems.length})
        </Button>
      </div>

      {ackError && (
        <div className="flex items-center gap-2 rounded-md border border-destructive bg-destructive/10 p-3 text-sm text-destructive">
          <AlertCircle className="h-4 w-4 shrink-0" />
          {ackError}
        </div>
      )}

      {activeTab === "all" && (
        <>
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
                <Skeleton key={i} className="h-20 w-full rounded-xl" />
              ))}
            </div>
          ) : acknowledgments.length > 0 ? (
            <div className="space-y-3">
              {acknowledgments.map((ack: any) => (
                <Card key={ack.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <ClipboardSignature className="h-6 w-6 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium">
                        Policy: {ack.policy_id?.slice(0, 8)}...
                      </div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        User: {ack.user_id?.slice(0, 8)}...
                        {ack.policy_version && <> &middot; v{ack.policy_version}</>}
                        {ack.due_date && (
                          <> &middot; Due: {new Date(ack.due_date).toLocaleDateString()}</>
                        )}
                        {ack.acknowledged_at && (
                          <> &middot; Signed: {new Date(ack.acknowledged_at).toLocaleDateString()}</>
                        )}
                      </div>
                    </div>
                    <Badge className={statusColor[ack.status] || ""}>{ack.status}</Badge>
                    {ack.status === "pending" && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleAcknowledge(ack.id)}
                        disabled={acknowledgePolicy.isPending}
                      >
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Acknowledge
                      </Button>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <ClipboardSignature className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No acknowledgments</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  No policy acknowledgments have been requested yet.
                </p>
              </CardContent>
            </Card>
          )}
        </>
      )}

      {activeTab === "my-pending" && (
        <>
          {pendingLoading ? (
            <div className="space-y-3">
              {[1, 2].map((i) => (
                <Skeleton key={i} className="h-20 w-full rounded-xl" />
              ))}
            </div>
          ) : pendingItems.length > 0 ? (
            <div className="space-y-3">
              {pendingItems.map((ack: any) => (
                <Card key={ack.id} className="border-yellow-200 dark:border-yellow-800">
                  <CardContent className="flex items-center gap-4 p-4">
                    <ClipboardSignature className="h-6 w-6 text-yellow-600 shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium">
                        Policy: {ack.policy_id?.slice(0, 8)}...
                      </div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        v{ack.policy_version || "1.0"}
                        {ack.due_date && (
                          <> &middot; Due: {new Date(ack.due_date).toLocaleDateString()}</>
                        )}
                      </div>
                    </div>
                    <Button
                      size="sm"
                      onClick={() => handleAcknowledge(ack.id)}
                      disabled={acknowledgePolicy.isPending}
                    >
                      <CheckCircle className="h-4 w-4 mr-1" />
                      Acknowledge
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <CheckCircle className="h-12 w-12 text-green-500 mb-4" />
                <h3 className="text-lg font-medium">All caught up!</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  You have no pending policy acknowledgments.
                </p>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
