"use client";

import { useState, useRef } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useEvidence, useCreateEvidence, useUploadEvidence, useEvidenceFreshness } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import api from "@/lib/api";
import {
  Shield,
  FileCheck,
  AlertTriangle,
  Upload,
  Plus,
  Loader2,
  FileUp,
  Download,
  ChevronLeft,
  ChevronRight,
  Activity,
} from "lucide-react";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Pending", value: "pending" },
  { label: "Collected", value: "collected" },
  { label: "Valid", value: "valid" },
  { label: "Expired", value: "expired" },
];

const METHOD_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Manual", value: "manual" },
  { label: "Automated", value: "automated" },
  { label: "API", value: "api" },
];

const statusBadgeVariant: Record<
  string,
  "default" | "secondary" | "success" | "destructive" | "outline"
> = {
  pending: "secondary",
  collected: "success",
  valid: "success",
  expired: "destructive",
  invalid: "destructive",
};

const methodBadgeVariant: Record<string, "default" | "secondary" | "outline"> =
  {
    manual: "outline",
    automated: "default",
    api: "secondary",
  };

export default function EvidencePage() {
  const orgId = useOrgId();
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const [methodFilter, setMethodFilter] = useState<string | undefined>(
    undefined
  );

  // Reset to page 1 when filters change
  function handleStatusFilter(value: string | undefined) {
    setStatusFilter(value);
    setPage(1);
  }
  function handleMethodFilter(value: string | undefined) {
    setMethodFilter(value);
    setPage(1);
  }
  const [showCreate, setShowCreate] = useState(false);
  const [createTitle, setCreateTitle] = useState("");
  const [uploadingId, setUploadingId] = useState<string | null>(null);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data, isLoading, error } = useEvidence(orgId, { page });
  const createEvidence = useCreateEvidence(orgId);
  const uploadEvidence = useUploadEvidence(orgId);
  const { data: freshness } = useEvidenceFreshness(orgId, 30);

  const allItems = data?.items || [];

  const evidenceItems = allItems.filter((item) => {
    if (statusFilter && item.status !== statusFilter) return false;
    if (methodFilter && item.collection_method !== methodFilter) return false;
    return true;
  });

  function handleCreate() {
    if (!createTitle.trim()) return;
    createEvidence.mutate(
      { title: createTitle, status: "pending", collection_method: "manual" },
      {
        onSuccess: () => {
          setCreateTitle("");
          setShowCreate(false);
        },
      }
    );
  }

  function handleUploadClick(evidenceId: string) {
    setUploadingId(evidenceId);
    fileInputRef.current?.click();
  }

  function handleFileSelected(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !uploadingId) return;
    uploadEvidence.mutate(
      { evidenceId: uploadingId, file },
      {
        onSettled: () => {
          setUploadingId(null);
          if (fileInputRef.current) fileInputRef.current.value = "";
        },
      }
    );
  }

  async function handleDownload(evidenceId: string) {
    setDownloadingId(evidenceId);
    try {
      await api.downloadRedirect(
        `/organizations/${orgId}/evidence/${evidenceId}/download`
      );
    } catch (err) {
      console.error("Download failed:", err);
    } finally {
      setDownloadingId(null);
    }
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Evidence Library</h1>
          <p className="text-muted-foreground">
            Track evidence collection status
          </p>
        </div>
        <Card className="border-destructive">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertTriangle className="h-12 w-12 text-destructive mb-4" />
            <h3 className="text-lg font-semibold">Failed to load evidence</h3>
            <p className="text-sm text-muted-foreground mt-2">
              {error.message ||
                "An unexpected error occurred. Please try again later."}
            </p>
            <Button className="mt-4" onClick={() => window.location.reload()}>
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const totalPages = data?.total_pages || 1;
  const showingFiltered = !!(statusFilter || methodFilter);
  const filteredCount = evidenceItems.length;

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

      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Evidence Library</h1>
          <p className="text-muted-foreground">
            Track evidence collection status
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          Add Evidence
        </Button>
      </div>

      {/* Evidence Freshness Dashboard */}
      {freshness && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2 mb-3">
              <Activity className="h-5 w-5 text-primary" />
              <h2 className="font-semibold">Evidence Freshness (30-day window)</h2>
            </div>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold">{freshness.total}</div>
                <div className="text-xs text-muted-foreground">Total</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{freshness.fresh}</div>
                <div className="text-xs text-muted-foreground">Fresh</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">{freshness.stale}</div>
                <div className="text-xs text-muted-foreground">Stale</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">{freshness.expired}</div>
                <div className="text-xs text-muted-foreground">Expired</div>
              </div>
            </div>
            <div className="mt-3">
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-muted-foreground">Freshness Rate</span>
                <span className="font-medium">{freshness.freshness_rate}%</span>
              </div>
              <div className="h-2 bg-muted rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${
                    freshness.freshness_rate >= 80 ? "bg-green-500" :
                    freshness.freshness_rate >= 50 ? "bg-yellow-500" : "bg-red-500"
                  }`}
                  style={{ width: `${freshness.freshness_rate}%` }}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Create evidence form */}
      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-3">
            <div>
              <label className="text-sm font-medium">Evidence Title</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g., MFA Enrollment Screenshot"
                value={createTitle}
                onChange={(e) => setCreateTitle(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <Button
                size="sm"
                onClick={handleCreate}
                disabled={!createTitle.trim() || createEvidence.isPending}
              >
                {createEvidence.isPending && (
                  <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                )}
                Create
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setShowCreate(false)}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
          {STATUS_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={statusFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => handleStatusFilter(f.value)}
            >
              {f.label}
            </Button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="flex items-center text-sm text-muted-foreground mr-1">
            Method:
          </span>
          {METHOD_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={methodFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => handleMethodFilter(f.value)}
            >
              {f.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Evidence list */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : evidenceItems.length > 0 ? (
        <div className="space-y-3">
          {evidenceItems.map((evidence) => (
            <Card
              key={evidence.id}
              className="transition-colors hover:bg-muted/50"
            >
              <CardContent className="flex items-center gap-4 p-4">
                <Shield className="h-8 w-8 text-muted-foreground shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium">{evidence.title}</div>
                  <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                    {evidence.collected_at && (
                      <span>
                        Collected{" "}
                        {new Date(evidence.collected_at).toLocaleDateString()}
                      </span>
                    )}
                    {evidence.expires_at && (
                      <>
                        <span>&middot;</span>
                        <span>
                          Expires{" "}
                          {new Date(evidence.expires_at).toLocaleDateString()}
                        </span>
                      </>
                    )}
                    {evidence.collector && (
                      <>
                        <span>&middot;</span>
                        <span>{evidence.collector}</span>
                      </>
                    )}
                    {evidence.file_name && (
                      <>
                        <span>&middot;</span>
                        <FileUp className="h-3 w-3 inline" />
                        <span>{evidence.file_name}</span>
                      </>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {/* Upload / Download button */}
                  {evidence.file_url ? (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDownload(evidence.id)}
                      disabled={downloadingId === evidence.id}
                    >
                      {downloadingId === evidence.id ? (
                        <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                      ) : (
                        <Download className="mr-1 h-4 w-4" />
                      )}
                      Download
                    </Button>
                  ) : (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleUploadClick(evidence.id)}
                      disabled={
                        uploadEvidence.isPending && uploadingId === evidence.id
                      }
                    >
                      {uploadEvidence.isPending &&
                      uploadingId === evidence.id ? (
                        <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                      ) : (
                        <Upload className="mr-1 h-4 w-4" />
                      )}
                      Upload
                    </Button>
                  )}
                  <Badge
                    variant={
                      (methodBadgeVariant[evidence.collection_method] ||
                        "outline") as any
                    }
                  >
                    {evidence.collection_method}
                  </Badge>
                  <Badge
                    variant={
                      (statusBadgeVariant[evidence.status] ||
                        "secondary") as any
                    }
                  >
                    {evidence.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <FileCheck className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No evidence found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No evidence items match the current filters, or the evidence
              library is empty.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 pt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page <= 1}
          >
            <ChevronLeft className="mr-1 h-4 w-4" />
            Previous
          </Button>
          <span className="text-sm text-muted-foreground">
            Page {page} of {totalPages} ({data?.total || 0} total{showingFiltered ? `, ${filteredCount} shown` : ""})
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page >= totalPages}
          >
            Next
            <ChevronRight className="ml-1 h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
}
