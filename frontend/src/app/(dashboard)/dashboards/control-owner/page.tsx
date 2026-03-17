"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useControlOwnerDashboard } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  ArrowLeft,
  AlertTriangle,
  CheckCircle,
  Clock,
  FileUp,
  ListChecks,
  XCircle,
} from "lucide-react";

export default function ControlOwnerDashboardPage() {
  const orgId = useOrgId();
  const { data, isLoading, error } = useControlOwnerDashboard(orgId);

  if (error) {
    return (
      <div className="space-y-6">
        <Header />
        <Card className="border-destructive">
          <CardContent className="p-8 text-center">
            <AlertTriangle className="h-8 w-8 text-destructive mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">{error.message}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const implementedPct = data && data.total_owned > 0
    ? Math.round((data.implemented / data.total_owned) * 100) : 0;

  return (
    <div className="space-y-6">
      <Header />

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">My Controls</CardTitle>
            <ListChecks className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-8 w-16" /> : (
              <>
                <div className="text-2xl font-bold">{data?.total_owned ?? 0}</div>
                <Progress value={implementedPct} className="mt-2" />
                <p className="text-xs text-muted-foreground mt-1">
                  {data?.implemented ?? 0} implemented ({implementedPct}%)
                </p>
              </>
            )}
          </CardContent>
        </Card>

        <Card className={data?.needs_attention ? "border-orange-500/30" : ""}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Needs Attention</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-8 w-16" /> : (
              <div className="text-2xl font-bold text-orange-500">{data?.needs_attention ?? 0}</div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Uploads</CardTitle>
            <FileUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-8 w-16" /> : (
              <>
                <div className="text-2xl font-bold">{data?.pending_evidence_uploads ?? 0}</div>
                <p className="text-xs text-muted-foreground">controls without evidence</p>
              </>
            )}
          </CardContent>
        </Card>

        <Card className={data?.overdue_items ? "border-red-500/30" : ""}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Overdue</CardTitle>
            <Clock className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-8 w-16" /> : (
              <div className="text-2xl font-bold text-red-500">{data?.overdue_items ?? 0}</div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Controls Table */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Controls Detail</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map(i => <Skeleton key={i} className="h-12 w-full" />)}
            </div>
          ) : data?.controls?.length ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-muted-foreground">
                    <th className="pb-2 font-medium">Control</th>
                    <th className="pb-2 font-medium">Status</th>
                    <th className="pb-2 font-medium text-center">Evidence</th>
                    <th className="pb-2 font-medium">Freshness</th>
                    <th className="pb-2 font-medium">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {data.controls.map((c: any) => (
                    <tr key={c.control_id} className="border-b last:border-0">
                      <td className="py-3 pr-4">
                        <div className="font-medium">{c.title}</div>
                        {c.framework_name && (
                          <span className="text-xs text-muted-foreground">{c.framework_name}</span>
                        )}
                      </td>
                      <td className="py-3 pr-4">
                        <StatusBadge status={c.status} />
                      </td>
                      <td className="py-3 pr-4 text-center">
                        {c.evidence_count}
                      </td>
                      <td className="py-3 pr-4">
                        <FreshnessBadge fresh={c.evidence_fresh} days={c.days_since_last_evidence} count={c.evidence_count} />
                      </td>
                      <td className="py-3">
                        {!c.evidence_fresh || c.status === "not_implemented" ? (
                          <Link href="/evidence" className="text-xs text-primary hover:underline">
                            Upload Evidence
                          </Link>
                        ) : (
                          <span className="text-xs text-green-600 flex items-center gap-1">
                            <CheckCircle className="h-3 w-3" /> OK
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8">
              <ListChecks className="h-12 w-12 text-muted-foreground mx-auto mb-2" />
              <p className="text-sm text-muted-foreground">No controls assigned to you yet.</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Header() {
  return (
    <div className="flex items-center gap-3">
      <Link href="/dashboards" className="text-muted-foreground hover:text-foreground">
        <ArrowLeft className="h-5 w-5" />
      </Link>
      <div>
        <h1 className="text-3xl font-bold">My Controls Dashboard</h1>
        <p className="text-muted-foreground">Controls assigned to you, evidence status, and action items</p>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const variants: Record<string, "success" | "warning" | "destructive" | "secondary"> = {
    implemented: "success",
    partially_implemented: "warning",
    not_implemented: "destructive",
    draft: "secondary",
    not_applicable: "secondary",
  };
  return <Badge variant={variants[status] || "secondary"}>{status.replace(/_/g, " ")}</Badge>;
}

function FreshnessBadge({ fresh, days, count }: { fresh: boolean; days: number | null; count: number }) {
  if (count === 0) {
    return (
      <span className="text-xs text-red-500 flex items-center gap-1">
        <XCircle className="h-3 w-3" /> No evidence
      </span>
    );
  }
  if (fresh) {
    return (
      <span className="text-xs text-green-600 flex items-center gap-1">
        <CheckCircle className="h-3 w-3" /> Fresh{days !== null ? ` (${days}d)` : ""}
      </span>
    );
  }
  return (
    <span className="text-xs text-red-500 flex items-center gap-1">
      <Clock className="h-3 w-3" /> Stale ({days}d)
    </span>
  );
}
