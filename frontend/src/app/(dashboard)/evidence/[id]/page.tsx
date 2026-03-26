"use client";

import { useState, useRef } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import {
  useEvidenceDetail,
  useEvidenceVersions,
  useApproveEvidence,
  useRejectEvidence,
  useUploadEvidence,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  ArrowLeft,
  CheckCircle2,
  Circle,
  XCircle,
  History,
  FileCheck,
  Download,
  Upload,
  Loader2,
  FileText,
  Shield,
} from "lucide-react";
import api from "@/lib/api";
import { toast } from "sonner";

const statusBadgeVariant: Record<
  string,
  "default" | "secondary" | "success" | "destructive" | "outline"
> = {
  pending: "secondary",
  collected: "success",
  valid: "success",
  approved: "success",
  expired: "destructive",
  invalid: "destructive",
  rejected: "destructive",
};

const methodBadgeVariant: Record<string, "default" | "secondary" | "outline"> =
  {
    manual: "outline",
    automated: "default",
    api: "secondary",
  };

export default function EvidenceDetailPage() {
  const params = useParams();
  const orgId = useOrgId();
  const evidenceId = params.id as string;

  const { data: evidence, isLoading } = useEvidenceDetail(orgId, evidenceId);
  const { data: versions } = useEvidenceVersions(orgId, evidenceId);
  const approveEvidence = useApproveEvidence(orgId);
  const rejectEvidence = useRejectEvidence(orgId);
  const uploadEvidence = useUploadEvidence(orgId);

  const [rejectReason, setRejectReason] = useState("");
  const [showRejectForm, setShowRejectForm] = useState(false);
  const [downloadingFile, setDownloadingFile] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  function handleApprove() {
    if (!evidence) return;
    approveEvidence.mutate(evidence.id, {
      onSuccess: () => toast.success("Evidence approved"),
      onError: (e: any) => toast.error(e.message),
    });
  }

  function handleReject() {
    if (!evidence || !rejectReason.trim()) return;
    rejectEvidence.mutate(
      { evidenceId: evidence.id, reason: rejectReason.trim() },
      {
        onSuccess: () => {
          toast.success("Evidence rejected");
          setRejectReason("");
          setShowRejectForm(false);
        },
        onError: (e: any) => toast.error(e.message),
      }
    );
  }

  async function handleDownload() {
    if (!evidence) return;
    setDownloadingFile(true);
    try {
      await api.downloadRedirect(
        `/organizations/${orgId}/evidence/${evidence.id}/download`
      );
    } catch (err) {
      console.error("Download failed:", err);
      toast.error("Download failed");
    } finally {
      setDownloadingFile(false);
    }
  }

  function handleUploadClick() {
    fileInputRef.current?.click();
  }

  function handleFileSelected(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !evidence) return;
    uploadEvidence.mutate(
      { evidenceId: evidence.id, file },
      {
        onSuccess: () => toast.success("File uploaded"),
        onError: (e: any) => toast.error(e.message),
        onSettled: () => {
          if (fileInputRef.current) fileInputRef.current.value = "";
        },
      }
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!evidence) return <p>Evidence not found.</p>;

  // Chain of custody steps
  const custodySteps = [
    {
      label: "Collected",
      who: evidence.collected_by || evidence.collector,
      when: evidence.collected_at,
      done: !!evidence.collected_at,
    },
    {
      label: "Reviewed",
      who: evidence.reviewed_by,
      when: evidence.reviewed_at,
      done: !!evidence.reviewed_at,
    },
    {
      label: evidence.rejected_at ? "Rejected" : "Approved",
      who: evidence.rejected_at ? evidence.rejected_by : evidence.approved_by,
      when: evidence.rejected_at || evidence.approved_at,
      done: !!(evidence.approved_at || evidence.rejected_at),
      rejected: !!evidence.rejected_at,
    },
  ];

  const canApproveReject =
    evidence.status === "collected" && !evidence.approved_at && !evidence.rejected_at;

  return (
    <div className="space-y-6">
      {/* Hidden file input for uploads */}
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        onChange={handleFileSelected}
        accept=".pdf,.png,.jpg,.jpeg,.csv,.xlsx,.docx,.txt,.json,.zip"
      />

      <Link
        href="/evidence"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Evidence Library
      </Link>

      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-3xl font-bold">{evidence.title}</h1>
          <Badge
            variant={
              (statusBadgeVariant[evidence.status] || "secondary") as any
            }
          >
            {evidence.status}
          </Badge>
          <Badge
            variant={
              (methodBadgeVariant[evidence.collection_method] ||
                "outline") as any
            }
          >
            {evidence.collection_method}
          </Badge>
        </div>
        <p className="mt-1 text-muted-foreground">
          {evidence.collected_at &&
            `Collected ${new Date(evidence.collected_at).toLocaleDateString()}`}
          {evidence.expires_at &&
            ` \u00B7 Expires ${new Date(evidence.expires_at).toLocaleDateString()}`}
          {evidence.collector && ` \u00B7 By ${evidence.collector}`}
        </p>
      </div>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="custody">Chain of Custody</TabsTrigger>
          <TabsTrigger value="versions">
            Versions
            {versions && versions.length > 0 && (
              <span className="ml-1 text-xs text-muted-foreground">
                ({versions.length})
              </span>
            )}
          </TabsTrigger>
          <TabsTrigger value="files">Files</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Status
                  </label>
                  <p className="text-sm font-medium capitalize">
                    {evidence.status}
                  </p>
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Collection Method
                  </label>
                  <p className="text-sm font-medium capitalize">
                    {evidence.collection_method}
                  </p>
                </div>
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Control ID
                  </label>
                  <p className="text-sm font-mono">
                    {evidence.control_id || "Not linked"}
                  </p>
                </div>
                {evidence.artifact_url && (
                  <div>
                    <label className="text-xs font-medium text-muted-foreground">
                      Artifact URL
                    </label>
                    <p className="text-sm break-all">{evidence.artifact_url}</p>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Timestamps</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Created
                  </label>
                  <p className="text-sm">
                    {new Date(evidence.created_at).toLocaleString()}
                  </p>
                </div>
                {evidence.collected_at && (
                  <div>
                    <label className="text-xs font-medium text-muted-foreground">
                      Collected
                    </label>
                    <p className="text-sm">
                      {new Date(evidence.collected_at).toLocaleString()}
                    </p>
                  </div>
                )}
                {evidence.expires_at && (
                  <div>
                    <label className="text-xs font-medium text-muted-foreground">
                      Expires
                    </label>
                    <p className="text-sm">
                      {new Date(evidence.expires_at).toLocaleString()}
                    </p>
                  </div>
                )}
                <div>
                  <label className="text-xs font-medium text-muted-foreground">
                    Last Updated
                  </label>
                  <p className="text-sm">
                    {new Date(evidence.updated_at).toLocaleString()}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {evidence.data && Object.keys(evidence.data).length > 0 && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle>Evidence Data</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="whitespace-pre-wrap text-sm bg-muted/50 rounded-md p-4">
                  {JSON.stringify(evidence.data, null, 2)}
                </pre>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Chain of Custody Tab */}
        <TabsContent value="custody">
          <Card>
            <CardHeader>
              <CardTitle>Chain of Custody</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-0">
                {custodySteps.map((step, idx) => (
                  <div key={step.label} className="flex items-start gap-4">
                    {/* Stepper line and icon */}
                    <div className="flex flex-col items-center">
                      {step.rejected ? (
                        <XCircle className="h-8 w-8 text-red-500 shrink-0" />
                      ) : step.done ? (
                        <CheckCircle2 className="h-8 w-8 text-green-500 shrink-0" />
                      ) : (
                        <Circle className="h-8 w-8 text-gray-400 shrink-0" />
                      )}
                      {idx < custodySteps.length - 1 && (
                        <div
                          className={`w-0.5 h-12 ${
                            step.done ? "bg-green-300" : "bg-gray-300"
                          }`}
                        />
                      )}
                    </div>

                    {/* Step content */}
                    <div className="pb-6">
                      <div className="font-medium text-sm">{step.label}</div>
                      {step.done ? (
                        <div className="text-xs text-muted-foreground mt-1">
                          {step.who && (
                            <span>By: {step.who}</span>
                          )}
                          {step.when && (
                            <span>
                              {step.who ? " \u00B7 " : ""}
                              {new Date(step.when).toLocaleString()}
                            </span>
                          )}
                        </div>
                      ) : (
                        <div className="text-xs text-muted-foreground mt-1">
                          Pending
                        </div>
                      )}
                      {step.rejected && evidence.rejection_reason && (
                        <div className="mt-2 rounded-md border border-red-500/30 bg-red-500/5 p-3">
                          <p className="text-xs font-medium text-red-600 dark:text-red-400">
                            Rejection Reason:
                          </p>
                          <p className="text-sm mt-1">
                            {evidence.rejection_reason}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Approve / Reject buttons */}
              {canApproveReject && (
                <div className="mt-6 space-y-4 border-t pt-6">
                  <p className="text-sm text-muted-foreground">
                    This evidence is awaiting review. You can approve or reject
                    it.
                  </p>
                  <div className="flex items-center gap-3">
                    <Button
                      onClick={handleApprove}
                      disabled={approveEvidence.isPending}
                    >
                      {approveEvidence.isPending ? (
                        <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                      ) : (
                        <CheckCircle2 className="mr-1 h-4 w-4" />
                      )}
                      Approve
                    </Button>
                    <Button
                      variant="destructive"
                      onClick={() => setShowRejectForm(!showRejectForm)}
                    >
                      <XCircle className="mr-1 h-4 w-4" />
                      Reject
                    </Button>
                  </div>

                  {showRejectForm && (
                    <div className="space-y-3 rounded-lg border p-4">
                      <label className="text-sm font-medium">
                        Rejection Reason
                      </label>
                      <textarea
                        className="w-full rounded-md border bg-background p-2 text-sm"
                        rows={3}
                        placeholder="Explain why this evidence is being rejected..."
                        value={rejectReason}
                        onChange={(e) => setRejectReason(e.target.value)}
                      />
                      <div className="flex gap-2">
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={handleReject}
                          disabled={
                            !rejectReason.trim() || rejectEvidence.isPending
                          }
                        >
                          {rejectEvidence.isPending && (
                            <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                          )}
                          Confirm Rejection
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => {
                            setShowRejectForm(false);
                            setRejectReason("");
                          }}
                        >
                          Cancel
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Versions Tab */}
        <TabsContent value="versions">
          {versions && versions.length > 0 ? (
            <div className="space-y-3">
              {versions.map((v) => (
                <Card key={v.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-sm font-bold text-primary">
                      v{v.version_number}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium">
                        {v.changes_summary || "Version update"}
                      </div>
                      <div className="text-xs text-muted-foreground mt-1">
                        {v.changed_by_name && (
                          <>Changed by: {v.changed_by_name}</>
                        )}
                        {v.changed_by && !v.changed_by_name && (
                          <>Changed by: {v.changed_by}</>
                        )}
                        {v.created_at && (
                          <>
                            {(v.changed_by_name || v.changed_by)
                              ? " \u00B7 "
                              : ""}
                            {new Date(v.created_at).toLocaleString()}
                          </>
                        )}
                      </div>
                      {v.snapshot &&
                        Object.keys(v.snapshot).length > 0 && (
                          <details className="mt-2">
                            <summary className="text-xs cursor-pointer text-muted-foreground hover:text-foreground">
                              View snapshot
                            </summary>
                            <pre className="mt-1 text-xs bg-muted/50 rounded-md p-2 whitespace-pre-wrap">
                              {JSON.stringify(v.snapshot, null, 2)}
                            </pre>
                          </details>
                        )}
                    </div>
                    <Badge variant="outline">v{v.version_number}</Badge>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-8 text-center">
                <History className="h-10 w-10 text-muted-foreground mb-3" />
                <p className="text-sm text-muted-foreground">
                  No version history yet. Changes will appear here when the
                  evidence is modified.
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Files Tab */}
        <TabsContent value="files">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Files</CardTitle>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleUploadClick}
                  disabled={uploadEvidence.isPending}
                >
                  {uploadEvidence.isPending ? (
                    <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                  ) : (
                    <Upload className="mr-1 h-4 w-4" />
                  )}
                  Upload File
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {evidence.file_name || evidence.file_url ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-4 rounded-lg border p-4">
                    <FileText className="h-8 w-8 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium">
                        {evidence.file_name || "Uploaded file"}
                      </div>
                      <div className="text-xs text-muted-foreground mt-1 space-y-0.5">
                        {evidence.artifact_hash && (
                          <div>
                            <span className="font-medium">Hash:</span>{" "}
                            <span className="font-mono">
                              {evidence.artifact_hash}
                            </span>
                          </div>
                        )}
                        {evidence.file_url && (
                          <div>
                            <span className="font-medium">Location:</span>{" "}
                            {evidence.file_url}
                          </div>
                        )}
                      </div>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={handleDownload}
                      disabled={downloadingFile}
                    >
                      {downloadingFile ? (
                        <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                      ) : (
                        <Download className="mr-1 h-4 w-4" />
                      )}
                      Download
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-8 text-center">
                  <Shield className="h-10 w-10 text-muted-foreground mb-3" />
                  <p className="text-sm text-muted-foreground">
                    No files attached to this evidence yet. Upload a file to get
                    started.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
