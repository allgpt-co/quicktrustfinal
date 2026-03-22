"use client";

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
  Database,
  Download,
  Clock,
  CheckCircle,
  XCircle,
  Loader2,
  HardDrive,
  Shield,
  RefreshCw,
} from "lucide-react";

export default function BackupsPage() {
  const orgId = useOrgId();
  const qc = useQueryClient();

  const { data: status, isLoading } = useQuery({
    queryKey: ["backup-status", orgId],
    queryFn: () => api.get<any>(`/organizations/${orgId}/backups/status`),
    enabled: !!orgId,
    refetchInterval: 10000,
  });

  const triggerBackup = useMutation({
    mutationFn: () => api.post(`/organizations/${orgId}/backups/trigger`, {}),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["backup-status"] });
      toast.success("Backup completed successfully!");
    },
    onError: (err: any) => toast.error(err.message || "Backup failed"),
  });

  const latest = status?.latest;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Link
          href="/settings"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Settings
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Database Backups</h1>
            <p className="text-muted-foreground">
              Automated nightly backups with manual trigger option
            </p>
          </div>
          <Button
            onClick={() => triggerBackup.mutate()}
            disabled={triggerBackup.isPending}
          >
            {triggerBackup.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Database className="mr-2 h-4 w-4" />
            )}
            Backup Now
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-3">
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
        </div>
      ) : (
        <>
          {/* Status cards */}
          <div className="grid gap-4 md:grid-cols-3">
            {/* Latest backup */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2 mb-3">
                  {latest?.status === "completed" ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : latest?.status === "failed" ? (
                    <XCircle className="h-5 w-5 text-red-500" />
                  ) : latest?.status === "running" ? (
                    <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
                  ) : (
                    <Clock className="h-5 w-5 text-muted-foreground" />
                  )}
                  <span className="text-sm font-medium">Latest Backup</span>
                </div>
                <Badge
                  className={
                    latest?.status === "completed"
                      ? "bg-green-500/20 text-green-500"
                      : latest?.status === "failed"
                      ? "bg-red-500/20 text-red-500"
                      : latest?.status === "running"
                      ? "bg-blue-500/20 text-blue-500"
                      : "bg-gray-500/20 text-gray-500"
                  }
                >
                  {latest?.status || "Never run"}
                </Badge>
                {latest?.completed_at && (
                  <p className="text-xs text-muted-foreground mt-2">
                    {new Date(latest.completed_at).toLocaleString()}
                  </p>
                )}
                {latest?.error && (
                  <p className="text-xs text-red-500 mt-1">{latest.error}</p>
                )}
              </CardContent>
            </Card>

            {/* Last file */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2 mb-3">
                  <HardDrive className="h-5 w-5 text-muted-foreground" />
                  <span className="text-sm font-medium">Last Backup File</span>
                </div>
                <p className="text-lg font-bold">
                  {latest?.size || "—"}
                </p>
                <p className="text-xs text-muted-foreground mt-1 truncate">
                  {latest?.filename || "No backup yet"}
                </p>
              </CardContent>
            </Card>

            {/* Schedule */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-2 mb-3">
                  <RefreshCw className="h-5 w-5 text-muted-foreground" />
                  <span className="text-sm font-medium">Schedule</span>
                </div>
                <p className="text-lg font-bold">Every night</p>
                <p className="text-xs text-muted-foreground mt-1">
                  1:00 AM UTC — automatic
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Local backup files */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Database className="h-5 w-5 text-muted-foreground" />
                <CardTitle>Backup Files</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              {status?.local_files && status.local_files.length > 0 ? (
                <div className="divide-y">
                  {status.local_files.map((f: any, i: number) => (
                    <div
                      key={i}
                      className="flex items-center justify-between py-3"
                    >
                      <div className="flex items-center gap-3">
                        <HardDrive className="h-4 w-4 text-muted-foreground" />
                        <div>
                          <p className="text-sm font-medium">{f.filename}</p>
                          <p className="text-xs text-muted-foreground">
                            {f.size} &middot;{" "}
                            {new Date(f.modified).toLocaleString()}
                          </p>
                        </div>
                      </div>
                      <Badge variant="outline" className="text-green-500">
                        <CheckCircle className="mr-1 h-3 w-3" />
                        Stored
                      </Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-8 text-center">
                  <Database className="mx-auto h-10 w-10 text-muted-foreground mb-3" />
                  <p className="text-sm text-muted-foreground">
                    No backup files yet. Click &quot;Backup Now&quot; to create
                    your first backup.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Backup history */}
          {status?.history && status.history.length > 0 && (
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Clock className="h-5 w-5 text-muted-foreground" />
                  <CardTitle>Backup History</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="divide-y">
                  {status.history.map((h: any, i: number) => (
                    <div
                      key={i}
                      className="flex items-center justify-between py-2"
                    >
                      <div className="text-sm">
                        <span className="font-medium">{h.filename}</span>
                        <span className="text-muted-foreground ml-2">
                          {h.size}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-muted-foreground">
                          {new Date(h.timestamp).toLocaleString()}
                        </span>
                        <Badge
                          className={
                            h.status === "completed"
                              ? "bg-green-500/20 text-green-500"
                              : "bg-red-500/20 text-red-500"
                          }
                        >
                          {h.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Security info */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 mb-3">
                <Shield className="h-5 w-5 text-muted-foreground" />
                <span className="font-medium">Backup Security</span>
              </div>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Backups are compressed with gzip
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Stored on encrypted volume
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Automatic retention: 30 days
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Automated nightly schedule (1:00 AM UTC)
                </li>
              </ul>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
