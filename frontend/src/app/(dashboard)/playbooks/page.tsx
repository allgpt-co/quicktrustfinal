"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  usePlaybooks,
  useSeedPlaybooks,
  useCreatePlaybook,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  BookOpen,
  Plus,
  Loader2,
  Zap,
  ChevronDown,
  ChevronUp,
  Shield,
} from "lucide-react";

const severityColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

export default function PlaybooksPage() {
  const orgId = useOrgId();
  const [showCreate, setShowCreate] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [form, setForm] = useState({
    title: "",
    description: "",
    severity_trigger: "high",
    category_trigger: "",
    steps: [{ order: 1, title: "", description: "" }],
  });

  const { data, isLoading } = usePlaybooks(orgId);
  const seedPlaybooks = useSeedPlaybooks(orgId);
  const createPlaybook = useCreatePlaybook(orgId);

  const playbooks = data?.items || [];

  const resetForm = () =>
    setForm({
      title: "",
      description: "",
      severity_trigger: "high",
      category_trigger: "",
      steps: [{ order: 1, title: "", description: "" }],
    });

  const handleCreate = () => {
    if (!form.title.trim()) return;
    createPlaybook.mutate(form, {
      onSuccess: () => {
        setShowCreate(false);
        resetForm();
      },
    });
  };

  const addStep = () => {
    setForm({
      ...form,
      steps: [
        ...form.steps,
        { order: form.steps.length + 1, title: "", description: "" },
      ],
    });
  };

  const updateStep = (index: number, field: string, value: string) => {
    const newSteps = [...form.steps];
    (newSteps[index] as any)[field] = value;
    setForm({ ...form, steps: newSteps });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Incident Playbooks</h1>
          <p className="text-muted-foreground">
            Pre-defined response procedures for security incidents
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => seedPlaybooks.mutate()}
            disabled={seedPlaybooks.isPending}
          >
            {seedPlaybooks.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Zap className="mr-2 h-4 w-4" />
            )}
            Seed Defaults
          </Button>
          <Button onClick={() => setShowCreate((v) => !v)}>
            <Plus className="mr-2 h-4 w-4" />
            New Playbook
          </Button>
        </div>
      </div>

      {/* Seed result message */}
      {seedPlaybooks.isSuccess && (
        <Card className="border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-950">
          <CardContent className="p-3 text-sm text-green-800 dark:text-green-200">
            Default playbooks seeded successfully! Refresh to see them.
          </CardContent>
        </Card>
      )}

      {/* Create form */}
      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-4">
            <h2 className="text-lg font-semibold">Create New Playbook</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Title</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g., Data Breach Response"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium">Severity Trigger</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.severity_trigger}
                  onChange={(e) =>
                    setForm({ ...form, severity_trigger: e.target.value })
                  }
                >
                  <option value="critical">Critical</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Describe the playbook purpose"
                rows={2}
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium">Category Trigger</label>
              <input
                type="text"
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g., data_breach, ddos, malware"
                value={form.category_trigger}
                onChange={(e) =>
                  setForm({ ...form, category_trigger: e.target.value })
                }
              />
            </div>

            {/* Steps */}
            <div className="space-y-2">
              <label className="text-sm font-medium">
                Response Steps ({form.steps.length})
              </label>
              {form.steps.map((step, idx) => (
                <div key={idx} className="flex gap-2 items-start">
                  <span className="text-sm font-medium text-muted-foreground mt-2 w-6">
                    {idx + 1}.
                  </span>
                  <input
                    type="text"
                    className="flex-1 rounded-md border bg-background p-2 text-sm"
                    placeholder="Step title"
                    value={step.title}
                    onChange={(e) => updateStep(idx, "title", e.target.value)}
                  />
                  <input
                    type="text"
                    className="flex-1 rounded-md border bg-background p-2 text-sm"
                    placeholder="Step description"
                    value={step.description}
                    onChange={(e) =>
                      updateStep(idx, "description", e.target.value)
                    }
                  />
                </div>
              ))}
              <Button type="button" variant="ghost" size="sm" onClick={addStep}>
                <Plus className="h-4 w-4 mr-1" />
                Add Step
              </Button>
            </div>

            <div className="flex items-center gap-2 pt-2">
              <Button
                onClick={handleCreate}
                disabled={!form.title.trim() || createPlaybook.isPending}
              >
                {createPlaybook.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Create Playbook
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setShowCreate(false);
                  resetForm();
                }}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Playbook list */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : playbooks.length > 0 ? (
        <div className="space-y-3">
          {playbooks.map((pb: any) => (
            <Card key={pb.id}>
              <CardContent className="p-4">
                <div
                  className="flex items-center justify-between cursor-pointer"
                  onClick={() =>
                    setExpandedId(expandedId === pb.id ? null : pb.id)
                  }
                >
                  <div className="flex items-center gap-3">
                    <BookOpen className="h-6 w-6 text-muted-foreground shrink-0" />
                    <div>
                      <div className="font-medium">{pb.title}</div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        {pb.description?.slice(0, 100)}
                        {pb.description?.length > 100 ? "..." : ""}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {pb.severity_trigger && (
                      <Badge
                        className={
                          severityColor[pb.severity_trigger] || ""
                        }
                      >
                        {pb.severity_trigger}
                      </Badge>
                    )}
                    {pb.category_trigger && (
                      <Badge variant="outline">{pb.category_trigger}</Badge>
                    )}
                    <Badge variant="secondary">
                      {pb.steps?.length || 0} steps
                    </Badge>
                    {expandedId === pb.id ? (
                      <ChevronUp className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <ChevronDown className="h-4 w-4 text-muted-foreground" />
                    )}
                  </div>
                </div>

                {/* Expanded steps */}
                {expandedId === pb.id && pb.steps && (
                  <div className="mt-4 ml-9 space-y-2 border-l-2 pl-4">
                    {(pb.steps as any[]).map((step: any, idx: number) => (
                      <div key={idx} className="flex gap-2 items-start">
                        <div className="h-6 w-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-bold shrink-0">
                          {step.order || idx + 1}
                        </div>
                        <div>
                          <div className="text-sm font-medium">
                            {step.title}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {step.description}
                          </div>
                        </div>
                      </div>
                    ))}
                    {pb.compliance_references &&
                      pb.compliance_references.length > 0 && (
                        <div className="mt-3 flex gap-2 flex-wrap">
                          <Shield className="h-4 w-4 text-muted-foreground" />
                          {(pb.compliance_references as any[]).map(
                            (ref: any, idx: number) => (
                              <Badge
                                key={idx}
                                variant="outline"
                                className="text-xs"
                              >
                                {ref.framework}: {ref.control}
                              </Badge>
                            )
                          )}
                        </div>
                      )}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <BookOpen className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No playbooks yet</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Click &quot;Seed Defaults&quot; to load 5 pre-built incident
              response playbooks, or create your own.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
