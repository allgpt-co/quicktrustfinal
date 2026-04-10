"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import {
  useAccessReviewCampaigns,
  useCreateAccessReviewCampaign,
  useAccessReviewStats,
  useAccessMatrix,
  useOverProvisionedAlerts,
  type AccessMatrixEntry,
  type OverProvisionedAlert,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  ShieldCheck,
  Plus,
  Loader2,
  Users,
  AlertTriangle,
} from "lucide-react";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Draft", value: "draft" },
  { label: "Active", value: "active" },
  { label: "Completed", value: "completed" },
  { label: "Cancelled", value: "cancelled" },
];

const statusColor: Record<string, string> = {
  draft: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
  active: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  completed:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  cancelled: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

export default function AccessReviewsPage() {
  const orgId = useOrgId();
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const { data, isLoading } = useAccessReviewCampaigns(orgId, {
    status: statusFilter,
  });
  const { data: stats } = useAccessReviewStats(orgId);
  const { data: accessMatrix, isLoading: matrixLoading } =
    useAccessMatrix(orgId);
  const { data: overProvisioned, isLoading: alertsLoading } =
    useOverProvisionedAlerts(orgId);

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    due_date: "",
  });
  const createCampaign = useCreateAccessReviewCampaign(orgId);

  const resetForm = () =>
    setForm({ title: "", description: "", due_date: "" });

  const handleCreate = () => {
    createCampaign.mutate(
      {
        title: form.title,
        description: form.description || undefined,
        due_date: form.due_date || undefined,
      },
      {
        onSuccess: () => {
          setShowCreate(false);
          resetForm();
        },
      }
    );
  };

  const campaigns = data?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Access Reviews</h1>
          <p className="text-muted-foreground">
            Manage periodic access review campaigns
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          New Campaign
        </Button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Total Campaigns", value: stats.total_campaigns ?? 0 },
            { label: "Active", value: stats.active_campaigns ?? 0 },
            { label: "Pending Decisions", value: stats.pending_decisions ?? 0 },
            { label: "Total Entries", value: stats.total_entries ?? 0 },
          ].map((s) => (
            <Card key={s.label}>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{s.value}</div>
                <div className="text-xs text-muted-foreground">{s.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Access Matrix */}
      <Card>
        <CardContent className="p-4">
          <div className="mb-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              <h2 className="text-lg font-semibold">Access Matrix</h2>
            </div>
            {accessMatrix && (
              <span className="text-xs text-muted-foreground">
                {accessMatrix.total_users} user
                {accessMatrix.total_users === 1 ? "" : "s"} ×{" "}
                {accessMatrix.total_integrations} integration
                {accessMatrix.total_integrations === 1 ? "" : "s"}
              </span>
            )}
          </div>
          {matrixLoading ? (
            <Skeleton className="h-32 w-full rounded-lg" />
          ) : accessMatrix && accessMatrix.matrix.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-xs uppercase text-muted-foreground">
                    <th className="pb-2 pr-3">User</th>
                    <th className="pb-2 pr-3">Role</th>
                    <th className="pb-2 pr-3">Status</th>
                    <th className="pb-2">Integrations</th>
                  </tr>
                </thead>
                <tbody>
                  {accessMatrix.matrix.map((entry: AccessMatrixEntry) => (
                    <tr key={entry.user_id} className="border-b last:border-0">
                      <td className="py-2 pr-3">
                        <div className="font-medium">{entry.full_name}</div>
                        <div className="text-xs text-muted-foreground">
                          {entry.email}
                        </div>
                      </td>
                      <td className="py-2 pr-3">
                        <Badge variant="outline">{entry.role}</Badge>
                      </td>
                      <td className="py-2 pr-3">
                        <Badge
                          variant={entry.is_active ? "success" : "secondary"}
                        >
                          {entry.is_active ? "Active" : "Inactive"}
                        </Badge>
                      </td>
                      <td className="py-2 text-muted-foreground">
                        {entry.access.length} connected
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No users or integrations to display.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Over-Provisioned Alerts */}
      <Card>
        <CardContent className="p-4">
          <div className="mb-3 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-500" />
            <h2 className="text-lg font-semibold">Over-Provisioned Alerts</h2>
            {overProvisioned && (
              <Badge variant={overProvisioned.total_alerts > 0 ? "warning" : "success"}>
                {overProvisioned.total_alerts}
              </Badge>
            )}
          </div>
          {alertsLoading ? (
            <Skeleton className="h-24 w-full rounded-lg" />
          ) : overProvisioned && overProvisioned.alerts.length > 0 ? (
            <div className="space-y-2">
              {overProvisioned.alerts.map((alert: OverProvisionedAlert) => (
                <div
                  key={alert.user_id}
                  className="rounded-lg border border-amber-300 bg-amber-50 p-3 dark:border-amber-900 dark:bg-amber-950"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="font-medium">{alert.full_name}</div>
                      <div className="text-xs text-muted-foreground">
                        {alert.email}
                      </div>
                    </div>
                    <Badge variant="outline">{alert.role}</Badge>
                  </div>
                  <ul className="mt-2 list-disc pl-5 text-xs text-muted-foreground">
                    {alert.reasons.map((reason, idx) => (
                      <li key={idx}>{reason}</li>
                    ))}
                  </ul>
                  {alert.recommendation && (
                    <div className="mt-1 text-xs font-medium text-amber-800 dark:text-amber-200">
                      {alert.recommendation}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No over-provisioned accounts detected.
            </p>
          )}
        </CardContent>
      </Card>

      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-4">
            <h2 className="text-lg font-semibold">Create New Campaign</h2>

            <div className="space-y-1">
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                required
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Campaign title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Campaign description"
                rows={3}
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Due Date</label>
              <input
                type="date"
                className="w-full rounded-md border bg-background p-2 text-sm"
                value={form.due_date}
                onChange={(e) =>
                  setForm({ ...form, due_date: e.target.value })
                }
              />
            </div>

            <div className="flex items-center gap-2 pt-2">
              <Button
                onClick={handleCreate}
                disabled={!form.title.trim() || createCampaign.isPending}
              >
                {createCampaign.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Create Campaign
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setShowCreate(false);
                  resetForm();
                }}
              >
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

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-28 w-full rounded-xl" />
          ))}
        </div>
      ) : campaigns.length > 0 ? (
        <div className="space-y-3">
          {campaigns.map((campaign: any) => {
            const totalEntries = campaign.total_entries ?? 0;
            const decidedEntries = campaign.decided_entries ?? 0;
            const progressPct =
              totalEntries > 0
                ? Math.round((decidedEntries / totalEntries) * 100)
                : 0;

            return (
              <Link
                key={campaign.id}
                href={`/access-reviews/${campaign.id}`}
              >
                <Card className="transition-colors hover:bg-accent/50">
                  <CardContent className="p-4 space-y-3">
                    <div className="flex items-center gap-4">
                      <ShieldCheck className="h-8 w-8 text-muted-foreground shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-medium">{campaign.title}</div>
                        <div className="mt-1 text-xs text-muted-foreground">
                          {campaign.due_date && (
                            <span>
                              Due:{" "}
                              {new Date(
                                campaign.due_date
                              ).toLocaleDateString()}
                            </span>
                          )}
                          {campaign.created_at && (
                            <>
                              <span> &middot; </span>
                              <span>
                                Created{" "}
                                {new Date(
                                  campaign.created_at
                                ).toLocaleDateString()}
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                      <Badge
                        className={statusColor[campaign.status] || ""}
                      >
                        {campaign.status}
                      </Badge>
                    </div>
                    {totalEntries > 0 && (
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs text-muted-foreground">
                          <span>
                            {decidedEntries} / {totalEntries} reviewed
                          </span>
                          <span>{progressPct}%</span>
                        </div>
                        <Progress value={progressPct} />
                      </div>
                    )}
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <ShieldCheck className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No campaigns found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No access review campaigns match the current filters.
            </p>
          </CardContent>
        </Card>
      )}

      {data && data.total_pages > 1 && (
        <div className="flex justify-center gap-2 pt-4">
          <p className="text-sm text-muted-foreground">
            Page {data.page} of {data.total_pages} ({data.total} total)
          </p>
        </div>
      )}
    </div>
  );
}
