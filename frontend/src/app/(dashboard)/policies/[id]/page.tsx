"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { usePolicy, useUpdatePolicy } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { useQuery } from "@tanstack/react-query";
import { Download, FileText } from "lucide-react";
import api from "@/lib/api";

const statusVariant: Record<string, "default" | "secondary" | "success" | "destructive" | "outline"> = {
  draft: "secondary",
  in_review: "default",
  approved: "success",
  published: "success",
  archived: "outline",
};

const statusTransitions: Record<string, { label: string; nextStatus: string }[]> = {
  draft: [{ label: "Submit for Review", nextStatus: "in_review" }],
  in_review: [
    { label: "Approve", nextStatus: "approved" },
    { label: "Return to Draft", nextStatus: "draft" },
  ],
  approved: [{ label: "Publish", nextStatus: "published" }],
  published: [{ label: "Archive", nextStatus: "archived" }],
  archived: [{ label: "Reactivate as Draft", nextStatus: "draft" }],
};

export default function PolicyDetailPage() {
  const params = useParams();
  const orgId = useOrgId();
  const policyId = params.id as string;
  const { data: policy, isLoading } = usePolicy(orgId, policyId);
  const updatePolicy = useUpdatePolicy(orgId);
  const [diffV1, setDiffV1] = useState(1);
  const [diffV2, setDiffV2] = useState(2);

  // Version history
  const { data: policyVersions } = useQuery({
    queryKey: ["policy-versions", orgId, policyId],
    queryFn: () => api.get<any[]>(`/organizations/${orgId}/policies/${policyId}/versions`),
    enabled: !!orgId && !!policyId,
  });

  // Diff between two versions
  const { data: diffData } = useQuery({
    queryKey: ["policy-diff", orgId, policyId, diffV1, diffV2],
    queryFn: () => api.get<any>(`/organizations/${orgId}/policies/${policyId}/diff?v1=${diffV1}&v2=${diffV2}`),
    enabled: !!orgId && !!policyId && !!policyVersions && policyVersions.length >= 2,
  });
  const [editing, setEditing] = useState(false);
  const [editContent, setEditContent] = useState("");

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!policy) return <p>Policy not found.</p>;

  function handleStatusChange(nextStatus: string) {
    updatePolicy.mutate({ policyId, status: nextStatus });
  }

  function handleStartEdit() {
    setEditContent(policy!.content || "");
    setEditing(true);
  }

  function handleSaveContent() {
    updatePolicy.mutate(
      { policyId, content: editContent },
      { onSuccess: () => setEditing(false) }
    );
  }

  const transitions = statusTransitions[policy.status] || [];

  function handleExport(format: "pdf" | "docx") {
    const url = `${process.env.NEXT_PUBLIC_API_URL || ""}/api/v1/organizations/${orgId}/policies/${policyId}/export/${format}`;
    window.open(url, "_blank");
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-3xl font-bold">{policy.title}</h1>
          <Badge variant={statusVariant[policy.status] || "secondary"}>
            {policy.status.replace(/_/g, " ")}
          </Badge>
          <Badge variant="outline">v{policy.version}</Badge>
        </div>
        <p className="mt-1 text-muted-foreground">
          Created {new Date(policy.created_at).toLocaleDateString()}
          {policy.published_at &&
            ` · Published ${new Date(policy.published_at).toLocaleDateString()}`}
          {policy.next_review_date &&
            ` · Next review ${new Date(policy.next_review_date).toLocaleDateString()}`}
        </p>
        <div className="mt-3 flex gap-2 flex-wrap">
          {transitions.map((t) => (
            <Button
              key={t.nextStatus}
              size="sm"
              variant={t.nextStatus === "draft" ? "outline" : "default"}
              onClick={() => handleStatusChange(t.nextStatus)}
              disabled={updatePolicy.isPending}
            >
              {t.label}
            </Button>
          ))}
          <Button size="sm" variant="outline" onClick={() => handleExport("pdf")}>
            <Download className="mr-1 h-4 w-4" />
            Download PDF
          </Button>
          <Button size="sm" variant="outline" onClick={() => handleExport("docx")}>
            <FileText className="mr-1 h-4 w-4" />
            Download DOCX
          </Button>
        </div>
      </div>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="controls">Linked Controls</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
          <TabsTrigger value="versions">
            Versions {policyVersions && policyVersions.length > 0 && `(${policyVersions.length})`}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Policy Content</CardTitle>
              {!editing && (
                <Button variant="outline" size="sm" onClick={handleStartEdit}>
                  Edit
                </Button>
              )}
            </CardHeader>
            <CardContent>
              {editing ? (
                <div className="space-y-3">
                  <textarea
                    className="w-full min-h-[400px] rounded-md border bg-background p-3 text-sm font-mono"
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                  />
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={handleSaveContent}
                      disabled={updatePolicy.isPending}
                    >
                      Save
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setEditing(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="prose prose-sm dark:prose-invert max-w-none whitespace-pre-wrap">
                  {policy.content || "No content yet. Click Edit to add policy content."}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="controls">
          <Card>
            <CardHeader>
              <CardTitle>Linked Controls</CardTitle>
            </CardHeader>
            <CardContent>
              {policy.control_ids && policy.control_ids.length > 0 ? (
                <div className="space-y-2">
                  {policy.control_ids.map((controlId) => (
                    <div
                      key={controlId}
                      className="flex items-center gap-2 rounded-lg border p-3 text-sm"
                    >
                      <span className="font-mono text-xs text-muted-foreground">
                        {controlId.slice(0, 8)}...
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">
                  No controls linked to this policy.
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings">
          <Card>
            <CardHeader>
              <CardTitle>Policy Metadata</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <dt className="font-medium text-muted-foreground">Version</dt>
                  <dd>{policy.version}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">Status</dt>
                  <dd className="capitalize">{policy.status.replace(/_/g, " ")}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">Created</dt>
                  <dd>{new Date(policy.created_at).toLocaleDateString()}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">Last Updated</dt>
                  <dd>{new Date(policy.updated_at).toLocaleDateString()}</dd>
                </div>
                {policy.approved_at && (
                  <div>
                    <dt className="font-medium text-muted-foreground">Approved</dt>
                    <dd>{new Date(policy.approved_at).toLocaleDateString()}</dd>
                  </div>
                )}
                {policy.published_at && (
                  <div>
                    <dt className="font-medium text-muted-foreground">Published</dt>
                    <dd>{new Date(policy.published_at).toLocaleDateString()}</dd>
                  </div>
                )}
                {policy.next_review_date && (
                  <div>
                    <dt className="font-medium text-muted-foreground">Next Review</dt>
                    <dd className="flex items-center gap-2">
                      {new Date(policy.next_review_date).toLocaleDateString()}
                      {new Date(policy.next_review_date) < new Date() ? (
                        <span className="inline-flex items-center rounded-full bg-red-500/20 px-2 py-0.5 text-xs font-medium text-red-500">
                          Overdue
                        </span>
                      ) : new Date(policy.next_review_date).getTime() - Date.now() < 30 * 24 * 3600000 ? (
                        <span className="inline-flex items-center rounded-full bg-yellow-500/20 px-2 py-0.5 text-xs font-medium text-yellow-500">
                          Due Soon
                        </span>
                      ) : null}
                    </dd>
                  </div>
                )}
                {(policy as any).classification && (
                  <div>
                    <dt className="font-medium text-muted-foreground">Classification</dt>
                    <dd>
                      <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        (policy as any).classification === "RESTRICTED" ? "bg-red-500/20 text-red-500" :
                        (policy as any).classification === "CONFIDENTIAL" ? "bg-orange-500/20 text-orange-500" :
                        (policy as any).classification === "INTERNAL" ? "bg-blue-500/20 text-blue-500" :
                        "bg-green-500/20 text-green-500"
                      }`}>
                        {(policy as any).classification}
                      </span>
                    </dd>
                  </div>
                )}
                <div>
                  <dt className="font-medium text-muted-foreground">Frameworks</dt>
                  <dd>
                    {policy.framework_ids && policy.framework_ids.length > 0
                      ? `${policy.framework_ids.length} framework(s)`
                      : "None"}
                  </dd>
                </div>
              </dl>
            </CardContent>
          </Card>
        </TabsContent>
        {/* Versions Tab */}
        <TabsContent value="versions">
          <div className="space-y-6">
            {/* Version list */}
            <Card>
              <CardHeader>
                <CardTitle>Version History</CardTitle>
              </CardHeader>
              <CardContent>
                {policyVersions && policyVersions.length > 0 ? (
                  <div className="divide-y">
                    {policyVersions.map((v: any) => (
                      <div key={v.id} className="flex items-center justify-between py-3">
                        <div className="flex items-center gap-3">
                          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-xs font-bold text-primary">
                            v{v.version_number}
                          </span>
                          <div>
                            <p className="text-sm font-medium">{v.change_summary || "No summary"}</p>
                            <p className="text-xs text-muted-foreground">
                              {v.status_at_version} &middot; {v.content_length} chars
                              {v.created_at && <> &middot; {new Date(v.created_at).toLocaleString()}</>}
                            </p>
                          </div>
                        </div>
                        <Badge variant="outline">{v.status_at_version}</Badge>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="py-6 text-center text-sm text-muted-foreground">
                    No version history yet. Versions are created when the policy content is updated.
                  </p>
                )}
              </CardContent>
            </Card>

            {/* Diff viewer */}
            {policyVersions && policyVersions.length >= 2 && (
              <Card>
                <CardHeader>
                  <CardTitle>Compare Versions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center gap-4">
                    <div>
                      <label className="text-xs font-medium text-muted-foreground">From</label>
                      <select
                        className="ml-2 rounded-md border bg-background px-2 py-1 text-sm"
                        value={diffV1}
                        onChange={(e) => setDiffV1(Number(e.target.value))}
                      >
                        {policyVersions.map((v: any) => (
                          <option key={v.id} value={v.version_number}>v{v.version_number}</option>
                        ))}
                      </select>
                    </div>
                    <span className="text-muted-foreground">→</span>
                    <div>
                      <label className="text-xs font-medium text-muted-foreground">To</label>
                      <select
                        className="ml-2 rounded-md border bg-background px-2 py-1 text-sm"
                        value={diffV2}
                        onChange={(e) => setDiffV2(Number(e.target.value))}
                      >
                        {policyVersions.map((v: any) => (
                          <option key={v.id} value={v.version_number}>v{v.version_number}</option>
                        ))}
                      </select>
                    </div>
                    {diffData && (
                      <div className="flex gap-2 text-xs">
                        <span className="text-green-500">+{diffData.additions} additions</span>
                        <span className="text-red-500">-{diffData.deletions} deletions</span>
                      </div>
                    )}
                  </div>

                  {diffData?.diff_text ? (
                    <pre className="max-h-96 overflow-auto rounded-lg border bg-muted/30 p-4 text-xs font-mono whitespace-pre-wrap">
                      {diffData.diff_text.split("\n").map((line: string, i: number) => (
                        <div
                          key={i}
                          className={
                            line.startsWith("+") && !line.startsWith("+++")
                              ? "bg-green-500/10 text-green-400"
                              : line.startsWith("-") && !line.startsWith("---")
                              ? "bg-red-500/10 text-red-400"
                              : line.startsWith("@@")
                              ? "text-blue-400"
                              : ""
                          }
                        >
                          {line}
                        </div>
                      ))}
                    </pre>
                  ) : (
                    <p className="text-sm text-muted-foreground">Select two different versions to see the diff.</p>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
