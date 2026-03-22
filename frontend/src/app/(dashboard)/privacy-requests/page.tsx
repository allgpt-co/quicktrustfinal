"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { useOrgId } from "@/hooks/use-org-id";
import { useAuth } from "@/providers/auth-provider";
import { toast } from "sonner";
import {
  Shield,
  UserX,
  Download,
  Clock,
  CheckCircle,
  Loader2,
  Plus,
  AlertTriangle,
  FileDown,
  Play,
} from "lucide-react";

const statusColor: Record<string, string> = {
  pending: "bg-yellow-500/20 text-yellow-500",
  processing: "bg-blue-500/20 text-blue-500",
  completed: "bg-green-500/20 text-green-500",
  failed: "bg-red-500/20 text-red-500",
};

export default function PrivacyRequestsPage() {
  const orgId = useOrgId();
  const { userInfo } = useAuth();
  const qc = useQueryClient();
  const [showNewRequest, setShowNewRequest] = useState(false);
  const [targetUserId, setTargetUserId] = useState("");
  const [reason, setReason] = useState("");

  // Fetch deletion requests
  const { data: requests, isLoading } = useQuery({
    queryKey: ["deletion-requests", orgId],
    queryFn: () => api.get<any[]>(`/organizations/${orgId}/deletion-requests`),
    enabled: !!orgId,
  });

  // Export own data
  const exportData = useMutation({
    mutationFn: () => api.get<any>("/privacy/data-export"),
    onSuccess: (data) => {
      // Download as JSON file
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `data-export-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toast.success("Data exported successfully");
    },
    onError: (err: any) => toast.error(err.message || "Export failed"),
  });

  // Create deletion request
  const createRequest = useMutation({
    mutationFn: (data: { target_user_id: string; reason: string }) =>
      api.post(`/organizations/${orgId}/deletion-requests`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["deletion-requests"] });
      toast.success("Deletion request created");
      setShowNewRequest(false);
      setTargetUserId("");
      setReason("");
    },
    onError: (err: any) => toast.error(err.message || "Failed to create request"),
  });

  // Process (execute) a deletion request
  const processRequest = useMutation({
    mutationFn: (requestId: string) =>
      api.post(`/organizations/${orgId}/deletion-requests/${requestId}/process`, {}),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["deletion-requests"] });
      toast.success("Deletion request processed — user data anonymized");
    },
    onError: (err: any) => toast.error(err.message || "Processing failed"),
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Privacy Requests</h1>
          <p className="text-muted-foreground">
            GDPR data access, export, and deletion requests
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => exportData.mutate()}
            disabled={exportData.isPending}
          >
            {exportData.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <FileDown className="mr-2 h-4 w-4" />
            )}
            Export My Data
          </Button>
          <Button onClick={() => setShowNewRequest(true)}>
            <Plus className="mr-2 h-4 w-4" />
            New Deletion Request
          </Button>
        </div>
      </div>

      {/* GDPR Rights Info */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-2">
              <Download className="h-5 w-5 text-blue-500" />
              <span className="text-sm font-medium">Right to Access</span>
            </div>
            <p className="text-xs text-muted-foreground">
              GDPR Article 15 — Users can request a copy of all their personal data.
              Click &quot;Export My Data&quot; to download.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-2">
              <UserX className="h-5 w-5 text-red-500" />
              <span className="text-sm font-medium">Right to Erasure</span>
            </div>
            <p className="text-xs text-muted-foreground">
              GDPR Article 17 — Users can request deletion of their personal data.
              Creates a deletion request that must be processed within 30 days.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="h-5 w-5 text-yellow-500" />
              <span className="text-sm font-medium">30-Day Deadline</span>
            </div>
            <p className="text-xs text-muted-foreground">
              All data subject requests must be fulfilled within 30 calendar days.
              Failure to comply can result in fines up to 4% of annual revenue.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* New request form */}
      {showNewRequest && (
        <Card className="border-red-500/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-red-500" />
              New Data Deletion Request
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Target User ID</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="UUID of the user whose data should be deleted"
                value={targetUserId}
                onChange={(e) => setTargetUserId(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Reason</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                rows={2}
                placeholder="GDPR Article 17 request from data subject..."
                value={reason}
                onChange={(e) => setReason(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <Button
                variant="destructive"
                onClick={() =>
                  createRequest.mutate({
                    target_user_id: targetUserId,
                    reason,
                  })
                }
                disabled={!targetUserId || createRequest.isPending}
              >
                {createRequest.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <UserX className="mr-2 h-4 w-4" />
                )}
                Submit Request
              </Button>
              <Button variant="outline" onClick={() => setShowNewRequest(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Requests list */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-muted-foreground" />
            Deletion Requests
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              <Skeleton className="h-16 w-full" />
              <Skeleton className="h-16 w-full" />
            </div>
          ) : !requests || requests.length === 0 ? (
            <div className="py-8 text-center">
              <Shield className="mx-auto h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No deletion requests. All user data is retained per your retention policies.
              </p>
            </div>
          ) : (
            <div className="divide-y">
              {requests.map((req: any) => (
                <div key={req.id} className="flex items-center justify-between py-4">
                  <div>
                    <p className="text-sm font-medium">
                      User: {req.target_user_id?.slice(0, 8)}...
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {req.reason || "No reason provided"} &middot;{" "}
                      {new Date(req.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge className={statusColor[req.status] || ""}>
                      {req.status}
                    </Badge>
                    {req.status === "pending" && (
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => processRequest.mutate(req.id)}
                        disabled={processRequest.isPending}
                      >
                        {processRequest.isPending ? (
                          <Loader2 className="mr-1 h-3 w-3 animate-spin" />
                        ) : (
                          <Play className="mr-1 h-3 w-3" />
                        )}
                        Process
                      </Button>
                    )}
                    {req.completed_at && (
                      <span className="text-xs text-muted-foreground">
                        Completed {new Date(req.completed_at).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
