"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { useControl, useEvidence } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { Shield, FileCheck, ChevronDown, ChevronUp, History, Link2, Clock, Trash2, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { toast } from "sonner";

const testResultVariant: Record<string, "success" | "destructive" | "secondary"> = {
  pass: "success",
  fail: "destructive",
  error: "destructive",
};

export default function ControlDetailPage() {
  const params = useParams();
  const orgId = useOrgId();
  const controlId = params.id as string;
  const { data: control, isLoading } = useControl(orgId, controlId);
  const { data: evidenceData, isLoading: evidenceLoading } = useEvidence(
    orgId,
    { control_id: controlId }
  );
  const [showProcedure, setShowProcedure] = useState(false);
  const [showAddDep, setShowAddDep] = useState(false);
  const [depControlId, setDepControlId] = useState("");
  const qc = useQueryClient();

  // Version history
  const { data: versions } = useQuery({
    queryKey: ["control-versions", orgId, controlId],
    queryFn: () => api.get<any[]>(`/organizations/${orgId}/controls/${controlId}/versions`),
    enabled: !!orgId && !!controlId,
  });

  // Dependencies
  const { data: dependencies } = useQuery({
    queryKey: ["control-deps", orgId, controlId],
    queryFn: () => api.get<any[]>(`/organizations/${orgId}/controls/${controlId}/dependencies`),
    enabled: !!orgId && !!controlId,
  });

  const addDep = useMutation({
    mutationFn: (depId: string) =>
      api.post(`/organizations/${orgId}/controls/${controlId}/dependencies`, { depends_on_id: depId }),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["control-deps"] }); setShowAddDep(false); setDepControlId(""); toast.success("Dependency added"); },
    onError: (e: any) => toast.error(e.message),
  });

  const removeDep = useMutation({
    mutationFn: (depId: string) =>
      api.delete(`/organizations/${orgId}/controls/${controlId}/dependencies/${depId}`),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["control-deps"] }); toast.success("Dependency removed"); },
  });

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!control) return <p>Control not found.</p>;

  const mappings = control.framework_mappings || [];
  const evidenceItems = evidenceData?.items || [];

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-3xl font-bold">{control.title}</h1>
          <Badge>{control.status.replace(/_/g, " ")}</Badge>
        </div>
        <p className="mt-1 text-muted-foreground">
          Automation: {control.automation_level} &middot; Created{" "}
          {new Date(control.created_at).toLocaleDateString()}
        </p>
      </div>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="mappings">
            Framework Mappings
            {mappings.length > 0 && (
              <span className="ml-1 text-xs text-muted-foreground">
                ({mappings.length})
              </span>
            )}
          </TabsTrigger>
          <TabsTrigger value="evidence">
            Evidence
            {evidenceItems.length > 0 && (
              <span className="ml-1 text-xs text-muted-foreground">
                ({evidenceItems.length})
              </span>
            )}
          </TabsTrigger>
          <TabsTrigger value="testing">Test History</TabsTrigger>
          <TabsTrigger value="versions">
            Versions
            {versions && versions.length > 0 && (
              <span className="ml-1 text-xs text-muted-foreground">({versions.length})</span>
            )}
          </TabsTrigger>
          <TabsTrigger value="dependencies">
            Dependencies
            {dependencies && dependencies.length > 0 && (
              <span className="ml-1 text-xs text-muted-foreground">({dependencies.length})</span>
            )}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="whitespace-pre-wrap">
                {control.description || "No description provided."}
              </p>
            </CardContent>
          </Card>

          {control.implementation_details && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle>Implementation Details</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="whitespace-pre-wrap">
                  {control.implementation_details}
                </p>
              </CardContent>
            </Card>
          )}

          {control.test_procedure && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle>Test Procedure</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="whitespace-pre-wrap">{control.test_procedure}</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="mappings">
          {mappings.length > 0 ? (
            <div className="space-y-3">
              {mappings.map((mapping) => (
                <Card key={mapping.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <Shield className="h-8 w-8 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium">
                        {mapping.framework_name || "Unknown Framework"}
                      </div>
                      {mapping.requirement_code && (
                        <div className="text-sm text-muted-foreground mt-1">
                          <span className="font-mono font-medium">
                            {mapping.requirement_code}
                          </span>
                          {mapping.requirement_title && (
                            <span> — {mapping.requirement_title}</span>
                          )}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-8 text-center">
                <Shield className="h-10 w-10 text-muted-foreground mb-3" />
                <p className="text-sm text-muted-foreground">
                  No framework mappings for this control.
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="evidence">
          {evidenceLoading ? (
            <div className="space-y-3">
              {[1, 2].map((i) => (
                <Skeleton key={i} className="h-20 w-full" />
              ))}
            </div>
          ) : evidenceItems.length > 0 ? (
            <div className="space-y-3">
              {evidenceItems.map((evidence) => (
                <Card key={evidence.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <FileCheck className="h-8 w-8 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium">{evidence.title}</div>
                      <div className="text-xs text-muted-foreground mt-1">
                        {evidence.collection_method}
                        {evidence.collected_at &&
                          ` · Collected ${new Date(evidence.collected_at).toLocaleDateString()}`}
                        {evidence.expires_at &&
                          ` · Expires ${new Date(evidence.expires_at).toLocaleDateString()}`}
                      </div>
                    </div>
                    <Badge
                      variant={
                        evidence.status === "collected"
                          ? "success"
                          : evidence.status === "expired"
                          ? "destructive"
                          : "secondary"
                      }
                    >
                      {evidence.status}
                    </Badge>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-8 text-center">
                <FileCheck className="h-10 w-10 text-muted-foreground mb-3" />
                <p className="text-sm text-muted-foreground">
                  No evidence linked to this control yet.
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="testing">
          <Card>
            <CardHeader>
              <CardTitle>Test Status</CardTitle>
            </CardHeader>
            <CardContent>
              {control.last_test_date ? (
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <Badge
                      variant={
                        testResultVariant[control.last_test_result || ""] || "secondary"
                      }
                      className="text-sm px-3 py-1"
                    >
                      {control.last_test_result || "N/A"}
                    </Badge>
                    <div className="text-sm text-muted-foreground">
                      Last tested:{" "}
                      {new Date(control.last_test_date).toLocaleDateString()}
                    </div>
                  </div>

                  {control.test_procedure && (
                    <div>
                      <button
                        className="flex items-center gap-1 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                        onClick={() => setShowProcedure(!showProcedure)}
                      >
                        Test Procedure
                        {showProcedure ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </button>
                      {showProcedure && (
                        <div className="mt-2 rounded-md border bg-muted/50 p-3">
                          <p className="whitespace-pre-wrap text-sm">
                            {control.test_procedure}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">
                  No tests have been run for this control yet.
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
        {/* Version History Tab */}
        <TabsContent value="versions">
          {versions && versions.length > 0 ? (
            <div className="space-y-3">
              {versions.map((v: any) => (
                <Card key={v.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-sm font-bold text-primary">
                      v{v.version_number}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium">{v.title}</div>
                      <div className="text-xs text-muted-foreground mt-1">
                        Status: {v.status}
                        {v.change_reason && <> &middot; Reason: {v.change_reason}</>}
                        {v.created_at && <> &middot; {new Date(v.created_at).toLocaleString()}</>}
                      </div>
                      {v.changes && Object.keys(v.changes).length > 0 && (
                        <div className="mt-2 text-xs">
                          {Object.entries(v.changes).map(([field, change]: [string, any]) => (
                            <div key={field} className="flex gap-2">
                              <span className="font-medium">{field}:</span>
                              <span className="text-red-400 line-through">{change.old || "—"}</span>
                              <span>→</span>
                              <span className="text-green-400">{change.new || "—"}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    <Badge variant="outline">{v.status}</Badge>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-8 text-center">
                <History className="h-10 w-10 text-muted-foreground mb-3" />
                <p className="text-sm text-muted-foreground">No version history yet. Changes will appear here when the control is modified.</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Dependencies Tab */}
        <TabsContent value="dependencies">
          <div className="space-y-4">
            <div className="flex justify-end">
              <Button size="sm" variant="outline" onClick={() => setShowAddDep(!showAddDep)}>
                <Plus className="mr-1 h-4 w-4" />
                Add Dependency
              </Button>
            </div>

            {showAddDep && (
              <Card>
                <CardContent className="p-4 space-y-3">
                  <label className="text-sm font-medium">Control ID this depends on:</label>
                  <input
                    type="text"
                    className="w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="Paste control UUID..."
                    value={depControlId}
                    onChange={(e) => setDepControlId(e.target.value)}
                  />
                  <div className="flex gap-2">
                    <Button size="sm" onClick={() => addDep.mutate(depControlId)} disabled={!depControlId || addDep.isPending}>
                      Add
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => setShowAddDep(false)}>Cancel</Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {dependencies && dependencies.length > 0 ? (
              <div className="space-y-3">
                {dependencies.map((dep: any) => (
                  <Card key={dep.id}>
                    <CardContent className="flex items-center gap-4 p-4">
                      <Link2 className="h-6 w-6 text-muted-foreground shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-medium">{dep.depends_on_title || "Unknown Control"}</div>
                        <div className="text-xs text-muted-foreground mt-1">
                          Type: {dep.dependency_type}
                          {dep.notes && <> &middot; {dep.notes}</>}
                        </div>
                      </div>
                      <Badge variant="outline">{dep.dependency_type}</Badge>
                      <Button size="sm" variant="ghost" onClick={() => removeDep.mutate(dep.id)}>
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <Card>
                <CardContent className="flex flex-col items-center justify-center p-8 text-center">
                  <Link2 className="h-10 w-10 text-muted-foreground mb-3" />
                  <p className="text-sm text-muted-foreground">No dependencies defined. Add dependencies to track which controls this one relies on.</p>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
