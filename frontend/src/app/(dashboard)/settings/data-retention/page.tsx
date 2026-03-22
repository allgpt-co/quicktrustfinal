"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { useOrgId } from "@/hooks/use-org-id";
import { toast } from "sonner";
import {
  ArrowLeft,
  Clock,
  Plus,
  Trash2,
  Shield,
  Database,
  FileText,
  Activity,
  Loader2,
  CheckCircle,
} from "lucide-react";

const entityTypeLabels: Record<string, string> = {
  audit_logs: "Audit Logs",
  agent_runs: "AI Agent Runs",
  evidences: "Evidence Records",
  incidents: "Incidents",
  policies: "Policies",
  risks: "Risks",
  notifications: "Notifications",
};

const entityTypeIcons: Record<string, any> = {
  audit_logs: Activity,
  agent_runs: Database,
  evidences: FileText,
};

export default function DataRetentionPage() {
  const orgId = useOrgId();
  const qc = useQueryClient();
  const [newType, setNewType] = useState("");
  const [newDays, setNewDays] = useState(365);
  const [newDesc, setNewDesc] = useState("");

  const { data: policies, isLoading } = useQuery({
    queryKey: ["retention-policies", orgId],
    queryFn: () => api.get<any[]>(`/organizations/${orgId}/retention-policies`),
    enabled: !!orgId,
  });

  const createPolicy = useMutation({
    mutationFn: (data: { entity_type: string; retention_days: number; description: string }) =>
      api.post(`/organizations/${orgId}/retention-policies`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["retention-policies"] });
      toast.success("Retention policy created");
      setNewType("");
      setNewDays(365);
      setNewDesc("");
    },
    onError: (err: any) => toast.error(err.message || "Failed to create policy"),
  });

  return (
    <div className="space-y-6">
      <div>
        <Link
          href="/settings"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Settings
        </Link>
        <h1 className="text-3xl font-bold">Data Retention Policies</h1>
        <p className="text-muted-foreground">
          Configure how long different types of data are retained before automatic cleanup
        </p>
      </div>

      {/* Info card */}
      <Card className="border-blue-500/30 bg-blue-500/5">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <Shield className="h-5 w-5 text-blue-500 mt-0.5" />
            <div>
              <p className="text-sm font-medium">GDPR & SOC 2 Compliance</p>
              <p className="text-xs text-muted-foreground mt-1">
                Data retention policies ensure you only keep data as long as necessary.
                Records past their retention period are automatically archived or deleted
                by the nightly scheduler (2:00 AM UTC). Legal holds override retention rules.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Add new policy */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plus className="h-5 w-5" />
            Add Retention Rule
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-4">
            <div>
              <label className="text-sm font-medium">Data Type</label>
              <select
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={newType}
                onChange={(e) => setNewType(e.target.value)}
              >
                <option value="">Select type...</option>
                {Object.entries(entityTypeLabels).map(([key, label]) => (
                  <option key={key} value={key}>{label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Retain for (days)</label>
              <input
                type="number"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={newDays}
                onChange={(e) => setNewDays(Number(e.target.value))}
                min={1}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Description</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g. GDPR requirement"
                value={newDesc}
                onChange={(e) => setNewDesc(e.target.value)}
              />
            </div>
            <div className="flex items-end">
              <Button
                onClick={() =>
                  createPolicy.mutate({
                    entity_type: newType,
                    retention_days: newDays,
                    description: newDesc,
                  })
                }
                disabled={!newType || createPolicy.isPending}
              >
                {createPolicy.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Plus className="mr-2 h-4 w-4" />
                )}
                Add Rule
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Existing policies */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5 text-muted-foreground" />
            Active Retention Rules
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              <Skeleton className="h-16 w-full" />
              <Skeleton className="h-16 w-full" />
            </div>
          ) : !policies || policies.length === 0 ? (
            <div className="py-8 text-center">
              <Clock className="mx-auto h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No retention policies configured. Add your first rule above.
              </p>
            </div>
          ) : (
            <div className="divide-y">
              {policies.map((p: any) => (
                <div key={p.id} className="flex items-center justify-between py-4">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
                      <Database className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <div>
                      <p className="text-sm font-medium">
                        {entityTypeLabels[p.entity_type] || p.entity_type}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {p.description || "No description"}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge variant="outline">
                      <Clock className="mr-1 h-3 w-3" />
                      {p.retention_days} days
                    </Badge>
                    <Badge className={p.is_active ? "bg-green-500/20 text-green-500" : "bg-gray-500/20 text-gray-500"}>
                      {p.is_active ? "Active" : "Disabled"}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Schedule info */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <span className="font-medium">Enforcement Schedule</span>
          </div>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>Retention enforcement runs nightly at 2:00 AM UTC</li>
            <li>Records past retention period are soft-deleted (recoverable for 30 days)</li>
            <li>Audit logs are hard-deleted (not recoverable) per compliance requirements</li>
            <li>Legal holds override all retention policies while active</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
