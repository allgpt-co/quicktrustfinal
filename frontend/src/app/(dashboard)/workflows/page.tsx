"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useWorkflows } from "@/hooks/use-api";
import { Workflow, Clock, CheckCircle, XCircle, Loader2 } from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

const statusColor: Record<string, string> = {
  completed: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  running: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  failed: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

const StatusIcon = ({ status }: { status: string }) => {
  if (status === "completed") return <CheckCircle className="h-4 w-4 text-green-600" />;
  if (status === "failed") return <XCircle className="h-4 w-4 text-red-600" />;
  if (status === "running") return <Loader2 className="h-4 w-4 text-blue-600 animate-spin" />;
  return <Clock className="h-4 w-4 text-yellow-600" />;
};

export default function WorkflowsPage() {
  const orgId = useOrgId();
  const { data: workflowsData, isLoading } = useWorkflows(orgId);

  const workflows = workflowsData?.items || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Workflows</h1>
        <p className="text-muted-foreground">
          Automated compliance workflows triggered by events and schedules
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: "Total Workflows", value: workflows.length },
          { label: "Enabled", value: workflows.filter((w: any) => w.enabled).length },
          { label: "Trigger Types", value: [...new Set(workflows.map((w: any) => w.trigger_type))].length },
        ].map((s) => (
          <Card key={s.label}>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold">{s.value}</div>
              <div className="text-xs text-muted-foreground">{s.label}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* List */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : workflows.length > 0 ? (
        <div className="space-y-3">
          {workflows.map((wf: any) => (
            <Card key={wf.id} className="transition-colors hover:bg-accent/50">
              <CardContent className="flex items-center gap-4 p-4">
                <Workflow className="h-8 w-8 text-muted-foreground shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium">{wf.name}</div>
                  {wf.description && (
                    <div className="mt-1 text-xs text-muted-foreground">{wf.description}</div>
                  )}
                  <div className="mt-1 text-xs text-muted-foreground">
                    Trigger: {wf.trigger_type}
                    {wf.steps && <> &middot; {wf.steps.length} steps</>}
                    {wf.created_at && (
                      <> &middot; Created {new Date(wf.created_at).toLocaleDateString()}</>
                    )}
                  </div>
                </div>
                <Badge variant={wf.enabled ? "success" : "secondary"}>
                  {wf.enabled ? "Enabled" : "Disabled"}
                </Badge>
                <Badge className={statusColor[wf.status] || "bg-gray-100 text-gray-800"}>
                  {wf.trigger_type}
                </Badge>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <Workflow className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No workflows configured</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Workflows automate compliance tasks like evidence collection, notifications, and remediation.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
