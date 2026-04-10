"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { useAudits, useReadinessScore, useCreateAudit, useFrameworks } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { api } from "@/lib/api";
import {
  ClipboardCheck,
  ShieldCheck,
  Plus,
  Loader2,
  Calculator,
  FileText,
  Inbox,
  ChevronDown,
  ChevronUp,
  AlertCircle,
} from "lucide-react";
import type { AuditStatus } from "@/lib/types";

type SamplingResponse = {
  population_size: number;
  confidence_level: number;
  margin_of_error: number;
  sample_size: number;
  formula_used: string;
};

type WorkpaperTemplate = {
  id: string;
  name: string;
  framework: string;
  sections: string[];
};

type WorkpaperResult = {
  audit: {
    id: string;
    name: string;
    framework: string | null;
    start_date: string | null;
    end_date: string | null;
    status: string;
  };
  generated_at: string;
  controls: Array<{
    id: string;
    title: string;
    status: string;
    evidence_count: number;
    has_gap: boolean;
  }>;
  evidence_summary: { total: number; by_status: Record<string, number> };
  findings: Array<{ id: string; title: string; severity: string; status: string }>;
  summary: {
    total_controls: number;
    implemented: number;
    total_evidence: number;
    total_findings: number;
  };
};

type EvidenceRequestItem = {
  id: string;
  title: string;
  description: string | null;
  status: string;
  deadline: string | null;
  control_id: string | null;
  created_at: string;
};

const statusColors: Record<AuditStatus, string> = {
  planning: "secondary",
  preparation: "secondary",
  fieldwork: "warning",
  reporting: "warning",
  completed: "success",
  closed: "outline",
};

const auditTypeBadgeVariant: Record<string, "default" | "outline" | "secondary"> = {
  internal: "secondary",
  external: "default",
  readiness: "outline",
};

function ReadinessGauge({ score, label }: { score: number; label: string }) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-medium">{Math.round(score)}%</span>
      </div>
      <Progress value={score} className="h-2" />
    </div>
  );
}

function ReadinessPanel({ orgId }: { orgId: string }) {
  const { data: readiness, isLoading } = useReadinessScore(orgId);

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-8">
            <Skeleton className="h-28 w-28 rounded-full" />
            <div className="flex-1 space-y-4">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!readiness) return null;

  const overall = Math.round(readiness.overall_score);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <ShieldCheck className="h-5 w-5" />
          Audit Readiness
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-8">
          {/* Large circular score */}
          <div className="relative flex h-28 w-28 shrink-0 items-center justify-center">
            <svg className="h-28 w-28 -rotate-90" viewBox="0 0 120 120">
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke="currentColor"
                strokeWidth="10"
                className="text-muted/30"
              />
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke="currentColor"
                strokeWidth="10"
                strokeDasharray={`${(overall / 100) * 2 * Math.PI * 52} ${2 * Math.PI * 52}`}
                strokeLinecap="round"
                className={
                  overall >= 80
                    ? "text-green-500"
                    : overall >= 50
                    ? "text-yellow-500"
                    : "text-red-500"
                }
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-2xl font-bold">{overall}%</span>
              <span className="text-xs text-muted-foreground">Overall</span>
            </div>
          </div>

          {/* Breakdown bars */}
          <div className="flex-1 space-y-3">
            <ReadinessGauge
              score={readiness.controls_score}
              label={`Controls (${readiness.controls_implemented}/${readiness.controls_total})`}
            />
            <ReadinessGauge
              score={readiness.evidence_score}
              label={`Evidence (${readiness.evidence_collected}/${readiness.evidence_total})`}
            />
            <ReadinessGauge
              score={readiness.policies_score}
              label={`Policies (${readiness.policies_published}/${readiness.policies_total})`}
            />
            <ReadinessGauge
              score={readiness.risks_score}
              label={`Risks (${readiness.risks_treated}/${readiness.risks_total})`}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function SamplingCalculatorCard() {
  const [populationSize, setPopulationSize] = useState<number>(1000);
  const [confidenceLevel, setConfidenceLevel] = useState<number>(95);
  const [marginOfError, setMarginOfError] = useState<number>(5);
  const [result, setResult] = useState<SamplingResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCalculate = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get<SamplingResponse>(
        `/audits/sampling-calculator?population_size=${populationSize}&confidence_level=${confidenceLevel}&margin_of_error=${marginOfError}`
      );
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to calculate");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Calculator className="h-5 w-5" />
          Audit Sampling Calculator
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Calculate the required sample size for audit testing
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-4 items-end">
          <div>
            <label className="text-sm font-medium">Population Size</label>
            <input
              type="number"
              min={1}
              className="w-full rounded-md border bg-background p-2 text-sm"
              value={populationSize}
              onChange={(e) => setPopulationSize(parseInt(e.target.value || "0", 10))}
            />
          </div>
          <div>
            <label className="text-sm font-medium">Confidence Level</label>
            <select
              className="w-full rounded-md border bg-background p-2 text-sm"
              value={confidenceLevel}
              onChange={(e) => setConfidenceLevel(parseFloat(e.target.value))}
            >
              <option value={90}>90%</option>
              <option value={95}>95%</option>
              <option value={99}>99%</option>
            </select>
          </div>
          <div>
            <label className="text-sm font-medium">Margin of Error (%)</label>
            <input
              type="number"
              min={0}
              step={0.1}
              className="w-full rounded-md border bg-background p-2 text-sm"
              value={marginOfError}
              onChange={(e) => setMarginOfError(parseFloat(e.target.value || "0"))}
            />
          </div>
          <Button onClick={handleCalculate} disabled={loading || populationSize < 1}>
            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Calculate
          </Button>
        </div>
        {error && (
          <p className="mt-4 text-sm text-red-600 flex items-center gap-2">
            <AlertCircle className="h-4 w-4" /> {error}
          </p>
        )}
        {result && (
          <div className="mt-4 rounded-md border bg-muted/50 p-4">
            <div className="text-lg font-semibold">
              Required sample size: {result.sample_size}
            </div>
            <div className="mt-1 text-xs text-muted-foreground">
              Formula: {result.formula_used}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function WorkpaperTemplatesCard() {
  const [templates, setTemplates] = useState<WorkpaperTemplate[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const data = await api.get<WorkpaperTemplate[]>("/audits/workpaper-templates");
        if (!cancelled) setTemplates(data);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5" />
          Workpaper Templates
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Pre-built workpaper structures for common frameworks
        </p>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="space-y-2">
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-12 w-full" />
          </div>
        ) : error ? (
          <p className="text-sm text-red-600">{error}</p>
        ) : templates && templates.length > 0 ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {templates.map((t) => (
              <div key={t.id} className="rounded-md border p-3">
                <div className="font-medium">{t.name}</div>
                <div className="mt-1 text-xs text-muted-foreground">{t.framework}</div>
                <div className="mt-2 flex flex-wrap gap-1">
                  {t.sections.map((s) => (
                    <Badge key={s} variant="outline" className="text-xs">
                      {s}
                    </Badge>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">No templates available.</p>
        )}
      </CardContent>
    </Card>
  );
}

function EvidenceRequestsCard({ orgId }: { orgId: string }) {
  const [items, setItems] = useState<EvidenceRequestItem[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    deadline: "",
  });

  const load = async () => {
    if (!orgId) return;
    setLoading(true);
    try {
      const data = await api.get<EvidenceRequestItem[]>(
        `/organizations/${orgId}/evidence-requests`
      );
      setItems(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orgId]);

  const handleCreate = async () => {
    if (!form.title.trim() || !orgId) return;
    setSubmitting(true);
    try {
      await api.post(`/organizations/${orgId}/evidence-requests`, {
        title: form.title,
        description: form.description || undefined,
        deadline: form.deadline ? new Date(form.deadline).toISOString() : undefined,
      });
      setForm({ title: "", description: "", deadline: "" });
      setShowForm(false);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create");
    } finally {
      setSubmitting(false);
    }
  };

  const statusVariant: Record<string, string> = {
    pending: "secondary",
    submitted: "warning",
    approved: "success",
    rejected: "destructive",
  };

  const daysUntil = (iso: string | null): string | null => {
    if (!iso) return null;
    const diff = Math.ceil(
      (new Date(iso).getTime() - Date.now()) / (1000 * 60 * 60 * 24)
    );
    if (diff < 0) return `${Math.abs(diff)}d overdue`;
    if (diff === 0) return "due today";
    return `${diff}d left`;
  };

  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between">
        <div>
          <CardTitle className="flex items-center gap-2">
            <Inbox className="h-5 w-5" />
            Evidence Requests
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            Track evidence requested from control owners
          </p>
        </div>
        <Button size="sm" onClick={() => setShowForm((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" /> New Request
        </Button>
      </CardHeader>
      <CardContent>
        {showForm && (
          <div className="mb-4 space-y-3 rounded-md border p-3">
            <div>
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g. Q4 access review screenshots"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm"
                rows={2}
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Deadline</label>
              <input
                type="date"
                className="w-full rounded-md border bg-background p-2 text-sm"
                value={form.deadline}
                onChange={(e) => setForm({ ...form, deadline: e.target.value })}
              />
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" size="sm" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
              <Button
                size="sm"
                onClick={handleCreate}
                disabled={submitting || !form.title.trim()}
              >
                {submitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Create
              </Button>
            </div>
          </div>
        )}

        {loading ? (
          <div className="space-y-2">
            <Skeleton className="h-16 w-full" />
            <Skeleton className="h-16 w-full" />
          </div>
        ) : error ? (
          <p className="text-sm text-red-600">{error}</p>
        ) : items && items.length > 0 ? (
          <div className="space-y-2">
            {items.map((r) => {
              const countdown = daysUntil(r.deadline);
              return (
                <div
                  key={r.id}
                  className="flex items-center gap-4 rounded-md border p-3"
                >
                  <div className="flex-1 min-w-0">
                    <div className="font-medium truncate">{r.title}</div>
                    {r.description && (
                      <div className="text-xs text-muted-foreground truncate">
                        {r.description}
                      </div>
                    )}
                  </div>
                  {countdown && (
                    <span className="text-xs text-muted-foreground">{countdown}</span>
                  )}
                  <Badge variant={(statusVariant[r.status] || "secondary") as any}>
                    {r.status}
                  </Badge>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">No evidence requests yet.</p>
        )}
      </CardContent>
    </Card>
  );
}

function WorkpaperButton({ orgId, auditId }: { orgId: string; auditId: string }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<WorkpaperResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (open) {
      setOpen(false);
      return;
    }
    setOpen(true);
    if (result) return;
    setLoading(true);
    try {
      const data = await api.get<WorkpaperResult>(
        `/organizations/${orgId}/audits/${auditId}/workpapers`
      );
      setResult(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button size="sm" variant="outline" onClick={handleGenerate}>
        <FileText className="mr-1 h-3 w-3" />
        {open ? "Hide" : "Workpaper"}
        {open ? <ChevronUp className="ml-1 h-3 w-3" /> : <ChevronDown className="ml-1 h-3 w-3" />}
      </Button>
      {open && (
        <div
          className="col-span-full mt-2 w-full rounded-md border bg-muted/30 p-3 text-xs"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
          }}
        >
          {loading ? (
            <Skeleton className="h-32 w-full" />
          ) : error ? (
            <p className="text-red-600">{error}</p>
          ) : result ? (
            <div className="space-y-2">
              <div className="font-medium">
                {result.audit.name} — generated{" "}
                {new Date(result.generated_at).toLocaleString()}
              </div>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                <div>
                  <div className="text-muted-foreground">Controls</div>
                  <div className="font-semibold">{result.summary.total_controls}</div>
                </div>
                <div>
                  <div className="text-muted-foreground">Implemented</div>
                  <div className="font-semibold">{result.summary.implemented}</div>
                </div>
                <div>
                  <div className="text-muted-foreground">Evidence</div>
                  <div className="font-semibold">{result.summary.total_evidence}</div>
                </div>
                <div>
                  <div className="text-muted-foreground">Findings</div>
                  <div className="font-semibold">{result.summary.total_findings}</div>
                </div>
              </div>
              <details>
                <summary className="cursor-pointer text-muted-foreground">
                  View raw JSON
                </summary>
                <pre className="mt-2 max-h-64 overflow-auto rounded bg-background p-2 text-xs">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </details>
            </div>
          ) : null}
        </div>
      )}
    </>
  );
}

export default function AuditsPage() {
  const orgId = useOrgId();
  const { data, isLoading } = useAudits(orgId);
  const audits = data?.items || [];

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    audit_type: "external",
    framework_id: "",
    auditor_firm: "",
  });

  const createAudit = useCreateAudit(orgId);
  const { data: frameworks } = useFrameworks();

  const resetForm = () =>
    setForm({ title: "", audit_type: "external", framework_id: "", auditor_firm: "" });

  const handleCreate = () => {
    if (!form.title.trim()) return;
    createAudit.mutate(
      {
        title: form.title,
        audit_type: form.audit_type,
        framework_id: form.framework_id || undefined,
        auditor_firm: form.auditor_firm || undefined,
      },
      {
        onSuccess: () => {
          setShowCreate(false);
          resetForm();
        },
      }
    );
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Audits</h1>
          <p className="text-muted-foreground">
            Manage compliance audits and readiness
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          New Audit
        </Button>
      </div>

      {/* Inline create form */}
      {showCreate && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Audit</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label className="text-sm font-medium">Title</label>
                <input
                  type="text"
                  required
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. ISO 27001 Surveillance Audit 2026"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                />
              </div>
              <div>
                <label className="text-sm font-medium">Audit Type</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.audit_type}
                  onChange={(e) => setForm({ ...form, audit_type: e.target.value })}
                >
                  <option value="internal">Internal</option>
                  <option value="external">External</option>
                  <option value="readiness">Readiness</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-medium">Framework</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.framework_id}
                  onChange={(e) => setForm({ ...form, framework_id: e.target.value })}
                >
                  <option value="">None</option>
                  {frameworks?.map((fw) => (
                    <option key={fw.id} value={fw.id}>
                      {fw.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="sm:col-span-2">
                <label className="text-sm font-medium">Auditor Firm</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. Deloitte, PwC (optional)"
                  value={form.auditor_firm}
                  onChange={(e) => setForm({ ...form, auditor_firm: e.target.value })}
                />
              </div>
            </div>
            <div className="mt-4 flex gap-2 justify-end">
              <Button
                variant="outline"
                onClick={() => {
                  setShowCreate(false);
                  resetForm();
                }}
              >
                Cancel
              </Button>
              <Button onClick={handleCreate} disabled={createAudit.isPending || !form.title.trim()}>
                {createAudit.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Create Audit
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Sampling calculator */}
      <SamplingCalculatorCard />

      {/* Readiness gauge */}
      <ReadinessPanel orgId={orgId} />

      {/* Workpaper templates */}
      <WorkpaperTemplatesCard />

      {/* Evidence requests */}
      <EvidenceRequestsCard orgId={orgId} />

      {/* Audit list */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : audits.length > 0 ? (
        <div className="space-y-3">
          {audits.map((audit) => (
            <Card key={audit.id} className="transition-colors hover:bg-muted/50">
              <CardContent className="flex flex-wrap items-center gap-4 p-4">
                <Link
                  href={`/audits/${audit.id}`}
                  className="flex flex-1 min-w-0 items-center gap-4"
                >
                  <ClipboardCheck className="h-8 w-8 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{audit.title}</div>
                    <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                      {audit.auditor_firm && <span>{audit.auditor_firm}</span>}
                      {audit.scheduled_start && audit.scheduled_end && (
                        <span>
                          {new Date(audit.scheduled_start).toLocaleDateString()} &ndash;{" "}
                          {new Date(audit.scheduled_end).toLocaleDateString()}
                        </span>
                      )}
                      {audit.readiness_score != null && (
                        <span>Readiness: {Math.round(audit.readiness_score)}%</span>
                      )}
                    </div>
                  </div>
                </Link>
                <div className="flex items-center gap-2 shrink-0">
                  <Badge
                    variant={
                      (auditTypeBadgeVariant[audit.audit_type] || "outline") as any
                    }
                  >
                    {audit.audit_type}
                  </Badge>
                  <Badge
                    variant={(statusColors[audit.status] || "secondary") as any}
                  >
                    {audit.status}
                  </Badge>
                  <WorkpaperButton orgId={orgId} auditId={audit.id} />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-12 text-center">
            <ClipboardCheck className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No audits yet</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Create your first audit to start tracking compliance readiness.
            </p>
          </CardContent>
        </Card>
      )}

      {data && data.total_pages > 1 && (
        <div className="flex justify-center gap-2 pt-4">
          <p className="text-sm text-muted-foreground">
            Page {data.page} of {data.total_pages} ({data.total} total)
          </p>
        </div>
      )}
    </div>
  );
}
