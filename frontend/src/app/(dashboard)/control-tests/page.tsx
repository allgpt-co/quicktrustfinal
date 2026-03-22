"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useControlTestDefinitions,
  useControlTestResults,
  useCreateControlTestDefinition,
  useDeleteControlTestDefinition,
  useRunControlTest,
  useRunAllControlTests,
  useControls,
} from "@/hooks/use-api";
import {
  FlaskConical,
  Plus,
  Loader2,
  Play,
  Trash2,
  CheckCircle,
  XCircle,
  AlertTriangle,
  PlayCircle,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

type TabValue = "definitions" | "results";

const resultColor: Record<string, string> = {
  pass: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  fail: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  error: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
};

const ResultIcon = ({ result }: { result: string }) => {
  if (result === "pass") return <CheckCircle className="h-4 w-4 text-green-600" />;
  if (result === "fail") return <XCircle className="h-4 w-4 text-red-600" />;
  return <AlertTriangle className="h-4 w-4 text-yellow-600" />;
};

export default function ControlTestsPage() {
  const orgId = useOrgId();
  const [activeTab, setActiveTab] = useState<TabValue>("definitions");
  const [showCreate, setShowCreate] = useState(false);

  const { data: defsData, isLoading: defsLoading } = useControlTestDefinitions(orgId);
  const { data: resultsData, isLoading: resultsLoading } = useControlTestResults(orgId);
  const { data: controlsData } = useControls(orgId, { page: 1 });

  const createDef = useCreateControlTestDefinition(orgId);
  const deleteDef = useDeleteControlTestDefinition(orgId);
  const runTest = useRunControlTest(orgId);
  const runAll = useRunAllControlTests(orgId);

  const [form, setForm] = useState({
    control_id: "",
    name: "",
    description: "",
    collector_type: "manual",
    assertion_field: "",
    assertion_operator: "eq",
    assertion_value: "",
    schedule: "daily",
  });

  const resetForm = () =>
    setForm({
      control_id: "",
      name: "",
      description: "",
      collector_type: "manual",
      assertion_field: "",
      assertion_operator: "eq",
      assertion_value: "",
      schedule: "daily",
    });

  const handleCreate = () => {
    createDef.mutate(form, {
      onSuccess: () => {
        setShowCreate(false);
        resetForm();
      },
    });
  };

  const definitions = defsData?.items || [];
  const results = resultsData?.items || [];
  const controls = controlsData?.items || [];

  const passCount = results.filter((r: any) => r.result === "pass").length;
  const failCount = results.filter((r: any) => r.result === "fail").length;
  const errorCount = results.filter((r: any) => r.result === "error").length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Control Tests</h1>
          <p className="text-muted-foreground">
            Define and run automated tests to validate control effectiveness
          </p>
        </div>
        <Button
          variant="outline"
          className="gap-1.5"
          onClick={() => runAll.mutate()}
          disabled={runAll.isPending}
        >
          {runAll.isPending ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <PlayCircle className="h-4 w-4" />
          )}
          Run All Tests
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Definitions", value: definitions.length },
          { label: "Passed", value: passCount },
          { label: "Failed", value: failCount },
          { label: "Errors", value: errorCount },
        ].map((s) => (
          <Card key={s.label}>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold">{s.value}</div>
              <div className="text-xs text-muted-foreground">{s.label}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Tab buttons */}
      <div className="flex gap-2 border-b pb-1">
        <Button
          variant={activeTab === "definitions" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("definitions")}
          className="gap-1.5"
        >
          <FlaskConical className="h-4 w-4" />
          Definitions
        </Button>
        <Button
          variant={activeTab === "results" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("results")}
          className="gap-1.5"
        >
          <CheckCircle className="h-4 w-4" />
          Results
        </Button>
      </div>

      {/* Definitions Tab */}
      {activeTab === "definitions" && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <Button
              size="sm"
              onClick={() => setShowCreate((v) => !v)}
              className="gap-1.5"
            >
              <Plus className="h-4 w-4" />
              New Test Definition
            </Button>
          </div>

          {showCreate && (
            <Card>
              <CardContent className="p-4 space-y-4">
                <h2 className="text-lg font-semibold">Create Test Definition</h2>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Name</label>
                    <input
                      type="text"
                      required
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="e.g. Verify MFA enabled"
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Control</label>
                    <select
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      value={form.control_id}
                      onChange={(e) => setForm({ ...form, control_id: e.target.value })}
                    >
                      <option value="">Select a control...</option>
                      {controls.map((c: any) => (
                        <option key={c.id} value={c.id}>
                          {c.title || c.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium">Description</label>
                  <input
                    type="text"
                    className="w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="What does this test verify?"
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                  />
                </div>

                <div className="grid grid-cols-4 gap-4">
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Collector Type</label>
                    <input
                      type="text"
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="e.g. aws_config"
                      value={form.collector_type}
                      onChange={(e) => setForm({ ...form, collector_type: e.target.value })}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Assertion Field</label>
                    <input
                      type="text"
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="e.g. mfa_enabled"
                      value={form.assertion_field}
                      onChange={(e) => setForm({ ...form, assertion_field: e.target.value })}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Operator</label>
                    <select
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      value={form.assertion_operator}
                      onChange={(e) => setForm({ ...form, assertion_operator: e.target.value })}
                    >
                      <option value="eq">Equals</option>
                      <option value="neq">Not Equals</option>
                      <option value="gt">Greater Than</option>
                      <option value="gte">Greater or Equal</option>
                      <option value="lt">Less Than</option>
                      <option value="lte">Less or Equal</option>
                      <option value="contains">Contains</option>
                      <option value="exists">Exists</option>
                    </select>
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Expected Value</label>
                    <input
                      type="text"
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="e.g. true"
                      value={form.assertion_value}
                      onChange={(e) => setForm({ ...form, assertion_value: e.target.value })}
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium">Schedule</label>
                  <select
                    className="w-full max-w-xs rounded-md border bg-background p-2 text-sm"
                    value={form.schedule}
                    onChange={(e) => setForm({ ...form, schedule: e.target.value })}
                  >
                    <option value="hourly">Hourly</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                  </select>
                </div>

                <div className="flex items-center gap-2 pt-2">
                  <Button
                    onClick={handleCreate}
                    disabled={!form.name.trim() || !form.control_id || !form.assertion_field || !form.assertion_value || createDef.isPending}
                  >
                    {createDef.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                    Create
                  </Button>
                  <Button variant="outline" onClick={() => { setShowCreate(false); resetForm(); }}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {defsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-24 w-full rounded-xl" />
              ))}
            </div>
          ) : definitions.length > 0 ? (
            <div className="space-y-3">
              {definitions.map((def: any) => (
                <Card key={def.id} className="transition-colors hover:bg-accent/50">
                  <CardContent className="flex items-center gap-4 p-4">
                    <FlaskConical className="h-8 w-8 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium">{def.name}</div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        {def.collector_type} &middot; {def.assertion_field} {def.assertion_operator} {def.assertion_value} &middot; {def.schedule}
                      </div>
                      {def.description && (
                        <div className="mt-1 text-xs text-muted-foreground">{def.description}</div>
                      )}
                    </div>
                    <Badge variant={def.is_active ? "success" : "secondary"}>
                      {def.is_active ? "Active" : "Inactive"}
                    </Badge>
                    <Button
                      size="sm"
                      variant="outline"
                      className="gap-1"
                      onClick={() => runTest.mutate(def.id)}
                      disabled={runTest.isPending}
                    >
                      <Play className="h-3 w-3" />
                      Run
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      className="gap-1 text-destructive"
                      onClick={() => deleteDef.mutate(def.id)}
                      disabled={deleteDef.isPending}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <FlaskConical className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No test definitions</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Create test definitions to automatically validate your controls.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Results Tab */}
      {activeTab === "results" && (
        <div className="space-y-4">
          {resultsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-20 w-full rounded-xl" />
              ))}
            </div>
          ) : results.length > 0 ? (
            <div className="space-y-3">
              {results.map((r: any) => (
                <Card key={r.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <ResultIcon result={r.result} />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium">
                        Test {r.test_definition_id?.slice(0, 8)}...
                      </div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        Expected: {r.expected_value}
                        {r.actual_value && <> &middot; Actual: {r.actual_value}</>}
                        {r.duration_ms != null && <> &middot; {r.duration_ms}ms</>}
                        {r.executed_at && (
                          <> &middot; {new Date(r.executed_at).toLocaleString()}</>
                        )}
                      </div>
                      {r.error_message && (
                        <div className="mt-1 text-xs text-red-600 dark:text-red-400">
                          {r.error_message}
                        </div>
                      )}
                    </div>
                    <Badge className={resultColor[r.result] || ""}>
                      {r.result}
                    </Badge>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <CheckCircle className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No test results yet</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Run tests from the Definitions tab to see results here.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
