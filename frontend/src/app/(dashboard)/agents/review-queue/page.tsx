"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useAgentRuns } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { toast } from "sonner";
import {
  ArrowLeft,
  CheckCircle,
  XCircle,
  Pencil,
  Clock,
  Bot,
  Loader2,
  ChevronDown,
  ChevronUp,
  Eye,
  Maximize2,
  X,
} from "lucide-react";

const statusColor: Record<string, string> = {
  pending_review: "bg-yellow-500/20 text-yellow-500 border-yellow-500/30",
  approved: "bg-green-500/20 text-green-500 border-green-500/30",
  rejected: "bg-red-500/20 text-red-500 border-red-500/30",
  modified: "bg-blue-500/20 text-blue-500 border-blue-500/30",
  auto: "bg-gray-500/20 text-gray-500 border-gray-500/30",
};

const agentNames: Record<string, string> = {
  controls_generation: "Controls Generation",
  policy_generation: "Policy Generation",
  evidence_generation: "Evidence Generation",
  risk_assessment: "Risk Assessment",
  remediation: "Remediation Planner",
  audit_preparation: "Audit Preparation",
  vendor_risk_assessment: "Vendor Risk Assessment",
  pentest_orchestrator: "Pentest Planner",
  monitoring_daemon: "Monitoring Daemon",
  questionnaire: "Questionnaire Auto-Fill",
};

type FilterTab = "pending_review" | "all" | "approved" | "rejected";

function generateSummary(agentType: string, output: any): string {
  if (!output) return "No output data";
  try {
    if (agentType === "monitoring_daemon") {
      const s = output.summary || output;
      return `Monitoring: ${s.passed || 0} passed, ${s.failed || 0} failed, ${s.errored || 0} errors — Pass rate: ${s.pass_rate || 0}%`;
    }
    if (agentType === "controls_generation") {
      const controls = output.controls || output.generated_controls || [];
      return `Generated ${Array.isArray(controls) ? controls.length : 0} security controls for compliance framework`;
    }
    if (agentType === "policy_generation") {
      const policies = output.policies || output.generated_policies || [];
      return `Generated ${Array.isArray(policies) ? policies.length : 0} compliance policies`;
    }
    if (agentType === "evidence_generation") {
      const evidence = output.evidence || output.generated_evidence || [];
      return `Generated ${Array.isArray(evidence) ? evidence.length : 0} evidence artifacts for controls`;
    }
    if (agentType === "risk_assessment") {
      const risks = output.risks || output.identified_risks || [];
      return `Identified ${Array.isArray(risks) ? risks.length : 0} risks — Overall risk level: ${output.overall_risk_level || output.risk_level || "N/A"}`;
    }
    if (agentType === "remediation") {
      const steps = output.remediation_steps || output.steps || [];
      return `Generated ${Array.isArray(steps) ? steps.length : 0} remediation steps for failing controls`;
    }
    if (agentType === "audit_preparation") {
      const score = output.readiness_score || output.audit_readiness_score;
      const gaps = output.gaps || output.evidence_gaps || [];
      return `Audit readiness score: ${score || "N/A"}% — ${Array.isArray(gaps) ? gaps.length : 0} evidence gaps found`;
    }
    if (agentType === "vendor_risk_assessment") {
      return `Vendor risk tier: ${output.risk_tier || output.overall_risk || "N/A"} — Score: ${output.risk_score || "N/A"}`;
    }
    if (agentType === "pentest_orchestrator") {
      return `Pentest plan: ${output.total_findings || output.findings_count || 0} findings — Risk rating: ${output.overall_risk_rating || "N/A"}`;
    }
    if (agentType === "questionnaire") {
      const answers = output.answers || [];
      return `Auto-filled ${Array.isArray(answers) ? answers.length : 0} questionnaire answers`;
    }
    // Fallback: show first few keys
    const keys = Object.keys(output).slice(0, 3).join(", ");
    return `Output contains: ${keys}...`;
  } catch {
    return "Output available — expand to view details";
  }
}

export default function ReviewQueuePage() {
  const orgId = useOrgId();
  const qc = useQueryClient();
  const { data: runsData, isLoading } = useAgentRuns(orgId);
  const [filter, setFilter] = useState<FilterTab>("pending_review");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [fullscreenRun, setFullscreenRun] = useState<any | null>(null);
  const [reviewNotes, setReviewNotes] = useState("");
  const [reviewingId, setReviewingId] = useState<string | null>(null);

  const reviewMutation = useMutation({
    mutationFn: ({
      runId,
      action,
      notes,
    }: {
      runId: string;
      action: string;
      notes: string;
    }) =>
      api.post(`/organizations/${orgId}/agents/runs/${runId}/review`, {
        action,
        review_notes: notes || null,
      }),
    onSuccess: (_data, vars) => {
      qc.invalidateQueries({ queryKey: ["agent-runs"] });
      toast.success(
        vars.action === "approve"
          ? "AI output approved"
          : vars.action === "reject"
          ? "AI output rejected"
          : "AI output modified"
      );
      setReviewingId(null);
      setReviewNotes("");
    },
    onError: (err: any) => {
      toast.error(err.message || "Review failed");
    },
  });

  const runs = (runsData?.items || []) as any[];

  const filtered = runs.filter((r: any) => {
    if (filter === "all") return true;
    return r.approval_status === filter;
  });

  const pendingCount = runs.filter(
    (r: any) => r.approval_status === "pending_review"
  ).length;
  const approvedCount = runs.filter(
    (r: any) => r.approval_status === "approved"
  ).length;
  const rejectedCount = runs.filter(
    (r: any) => r.approval_status === "rejected"
  ).length;

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Link
            href="/agents"
            className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to AI Agents
          </Link>
          <h1 className="text-3xl font-bold">AI Review Queue</h1>
          <p className="text-muted-foreground">
            Review, approve, or reject AI-generated outputs before they take
            effect
          </p>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2">
        {[
          {
            key: "pending_review" as FilterTab,
            label: "Pending",
            count: pendingCount,
            color: "text-yellow-500",
          },
          {
            key: "approved" as FilterTab,
            label: "Approved",
            count: approvedCount,
            color: "text-green-500",
          },
          {
            key: "rejected" as FilterTab,
            label: "Rejected",
            count: rejectedCount,
            color: "text-red-500",
          },
          {
            key: "all" as FilterTab,
            label: "All",
            count: runs.length,
            color: "",
          },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
              filter === tab.key
                ? "bg-primary text-primary-foreground"
                : "bg-muted text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab.label}
            <span
              className={`rounded-full px-2 py-0.5 text-xs ${
                filter === tab.key
                  ? "bg-primary-foreground/20"
                  : "bg-background"
              }`}
            >
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Run list */}
      {filtered.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <Bot className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-lg font-medium">No runs to review</p>
            <p className="text-sm text-muted-foreground mt-1">
              {filter === "pending_review"
                ? "All AI outputs have been reviewed!"
                : `No ${filter} runs found.`}
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {filtered.map((run: any) => {
            const isExpanded = expandedId === run.id;
            const isReviewing = reviewingId === run.id;
            const outputPreview = run.output_data
              ? JSON.stringify(run.output_data).slice(0, 200)
              : "No output";

            return (
              <Card
                key={run.id}
                className={
                  run.approval_status === "pending_review"
                    ? "border-yellow-500/30"
                    : ""
                }
              >
                <CardContent className="pt-4">
                  {/* Row header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Bot className="h-5 w-5 text-muted-foreground" />
                      <div>
                        <p className="font-medium">
                          {agentNames[run.agent_type] || run.agent_type}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(run.created_at).toLocaleString()}
                          {run.response_time_ms && (
                            <span> &middot; {run.response_time_ms}ms</span>
                          )}
                          {run.tokens_used && (
                            <span>
                              {" "}
                              &middot; {run.tokens_used.toLocaleString()} tokens
                            </span>
                          )}
                          {run.cost_usd != null && run.cost_usd > 0 && (
                            <span> &middot; ${run.cost_usd.toFixed(4)}</span>
                          )}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <Badge
                        className={
                          statusColor[run.approval_status] || statusColor.auto
                        }
                      >
                        {run.approval_status?.replace(/_/g, " ")}
                      </Badge>
                      <Badge
                        variant={
                          run.status === "completed"
                            ? "default"
                            : run.status === "failed"
                            ? "destructive"
                            : "secondary"
                        }
                      >
                        {run.status}
                      </Badge>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() =>
                          setExpandedId(isExpanded ? null : run.id)
                        }
                      >
                        {isExpanded ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                  </div>

                  {/* Review notes if exists */}
                  {run.review_notes && (
                    <div className="mt-2 rounded-md bg-muted/50 px-3 py-2 text-sm">
                      <span className="font-medium">Review note:</span>{" "}
                      {run.review_notes}
                    </div>
                  )}

                  {/* Expanded: show output */}
                  {isExpanded && (
                    <div className="mt-4 space-y-4">
                      {/* Human-readable summary */}
                      <div className="rounded-lg border bg-primary/5 p-4">
                        <p className="text-sm font-medium mb-1">Summary</p>
                        <p className="text-sm">
                          {generateSummary(run.agent_type, run.output_data)}
                        </p>
                      </div>

                      {/* Output with fullscreen toggle */}
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <p className="text-sm font-medium">Raw Output:</p>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setFullscreenRun(run)}
                          >
                            <Maximize2 className="mr-1 h-3 w-3" />
                            Full Screen
                          </Button>
                        </div>
                        <pre className="max-h-48 overflow-auto rounded-lg border bg-muted/30 p-3 text-xs whitespace-pre-wrap">
                          {run.output_data
                            ? JSON.stringify(run.output_data, null, 2)
                            : "No output data"}
                        </pre>
                      </div>

                      {/* Original output if modified */}
                      {run.original_output && (
                        <div>
                          <p className="text-sm font-medium mb-2 text-muted-foreground">
                            Original Output (before modification):
                          </p>
                          <pre className="max-h-32 overflow-auto rounded-lg border bg-muted/30 p-3 text-xs whitespace-pre-wrap">
                            {JSON.stringify(run.original_output, null, 2)}
                          </pre>
                        </div>
                      )}

                      {/* Review actions */}
                      {run.approval_status === "pending_review" && (
                        <div className="rounded-lg border border-yellow-500/30 bg-yellow-500/5 p-4 space-y-3">
                          <p className="text-sm font-medium">Review this output:</p>
                          <textarea
                            className="w-full rounded-md border bg-background p-2 text-sm"
                            rows={2}
                            placeholder="Optional review notes..."
                            value={isReviewing ? reviewNotes : ""}
                            onChange={(e) => {
                              setReviewingId(run.id);
                              setReviewNotes(e.target.value);
                            }}
                            onFocus={() => setReviewingId(run.id)}
                          />
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              onClick={() =>
                                reviewMutation.mutate({
                                  runId: run.id,
                                  action: "approve",
                                  notes: isReviewing ? reviewNotes : "",
                                })
                              }
                              disabled={reviewMutation.isPending}
                              className="bg-green-600 hover:bg-green-700"
                            >
                              {reviewMutation.isPending ? (
                                <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                              ) : (
                                <CheckCircle className="mr-1 h-4 w-4" />
                              )}
                              Approve
                            </Button>
                            <Button
                              size="sm"
                              variant="destructive"
                              onClick={() =>
                                reviewMutation.mutate({
                                  runId: run.id,
                                  action: "reject",
                                  notes: isReviewing ? reviewNotes : "",
                                })
                              }
                              disabled={reviewMutation.isPending}
                            >
                              {reviewMutation.isPending ? (
                                <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                              ) : (
                                <XCircle className="mr-1 h-4 w-4" />
                              )}
                              Reject
                            </Button>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Fullscreen Modal */}
      {fullscreenRun && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
          <div className="relative w-full max-w-5xl max-h-[90vh] rounded-xl border bg-background shadow-2xl flex flex-col">
            {/* Modal header */}
            <div className="flex items-center justify-between border-b px-6 py-4">
              <div>
                <h2 className="text-lg font-bold">
                  {agentNames[fullscreenRun.agent_type] || fullscreenRun.agent_type}
                </h2>
                <p className="text-sm text-muted-foreground">
                  {new Date(fullscreenRun.created_at).toLocaleString()}
                  {fullscreenRun.tokens_used && ` · ${fullscreenRun.tokens_used.toLocaleString()} tokens`}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Badge className={statusColor[fullscreenRun.approval_status] || statusColor.auto}>
                  {fullscreenRun.approval_status?.replace(/_/g, " ")}
                </Badge>
                <Button variant="ghost" size="sm" onClick={() => setFullscreenRun(null)}>
                  <X className="h-5 w-5" />
                </Button>
              </div>
            </div>

            {/* Summary */}
            <div className="border-b px-6 py-3 bg-primary/5">
              <p className="text-sm font-medium">Summary</p>
              <p className="text-sm">{generateSummary(fullscreenRun.agent_type, fullscreenRun.output_data)}</p>
            </div>

            {/* Scrollable output */}
            <div className="flex-1 overflow-auto px-6 py-4">
              <pre className="whitespace-pre-wrap text-sm font-mono">
                {fullscreenRun.output_data
                  ? JSON.stringify(fullscreenRun.output_data, null, 2)
                  : "No output data"}
              </pre>
            </div>

            {/* Modal footer with review actions */}
            {fullscreenRun.approval_status === "pending_review" && (
              <div className="border-t px-6 py-4 flex items-center gap-3">
                <textarea
                  className="flex-1 rounded-md border bg-background p-2 text-sm"
                  rows={1}
                  placeholder="Optional review notes..."
                  value={reviewingId === fullscreenRun.id ? reviewNotes : ""}
                  onChange={(e) => {
                    setReviewingId(fullscreenRun.id);
                    setReviewNotes(e.target.value);
                  }}
                  onFocus={() => setReviewingId(fullscreenRun.id)}
                />
                <Button
                  size="sm"
                  onClick={() => {
                    reviewMutation.mutate({
                      runId: fullscreenRun.id,
                      action: "approve",
                      notes: reviewingId === fullscreenRun.id ? reviewNotes : "",
                    });
                    setFullscreenRun(null);
                  }}
                  disabled={reviewMutation.isPending}
                  className="bg-green-600 hover:bg-green-700"
                >
                  <CheckCircle className="mr-1 h-4 w-4" />
                  Approve
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => {
                    reviewMutation.mutate({
                      runId: fullscreenRun.id,
                      action: "reject",
                      notes: reviewingId === fullscreenRun.id ? reviewNotes : "",
                    });
                    setFullscreenRun(null);
                  }}
                  disabled={reviewMutation.isPending}
                >
                  <XCircle className="mr-1 h-4 w-4" />
                  Reject
                </Button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
