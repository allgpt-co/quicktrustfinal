"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useScannerDashboard,
  useScannerScans,
  useScannerFindings,
  useScannerTrigger,
  useScannerUpdateFinding,
} from "@/hooks/use-api";
import {
  ShieldCheck,
  Play,
  Loader2,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Bug,
  KeyRound,
  FileCode,
  Globe,
  Layers,
  Container,
  X,
  ChevronLeft,
  ChevronRight,
  Eye,
  EyeOff,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

type TabValue = "dashboard" | "scans" | "findings";

const SCANNERS = [
  { id: "trivy", label: "Trivy", icon: Container, desc: "Container vulnerability scanning", placeholder: "python:3.11-slim" },
  { id: "semgrep", label: "Semgrep", icon: FileCode, desc: "Static code analysis (SAST)", placeholder: "/path/to/source" },
  { id: "gitleaks", label: "Gitleaks", icon: KeyRound, desc: "Secret detection in git repos", placeholder: "/path/to/repo" },
  { id: "checkov", label: "Checkov", icon: Layers, desc: "Infrastructure as Code scanning", placeholder: "/path/to/terraform" },
  { id: "zap", label: "OWASP ZAP", icon: Globe, desc: "Web app scanning (DAST)", placeholder: "https://myapp.com" },
  { id: "nuclei", label: "Nuclei", icon: Bug, desc: "Template-based vulnerability scanning", placeholder: "https://myapp.com" },
  { id: "prowler", label: "Prowler", icon: ShieldCheck, desc: "Cloud security posture (AWS/Azure/GCP)", placeholder: "default" },
];

const SEVERITY_COLORS: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  info: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
};

const STATUS_COLORS: Record<string, string> = {
  completed: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  running: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
  failed: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
};

const SCANNER_COLORS: Record<string, string> = {
  trivy: "bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-200",
  semgrep: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200",
  gitleaks: "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200",
  checkov: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200",
  zap: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
  nuclei: "bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-200",
  prowler: "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200",
};

export default function SecurityScannerPage() {
  const orgId = useOrgId();
  const [activeTab, setActiveTab] = useState<TabValue>("dashboard");
  const [showTrigger, setShowTrigger] = useState(false);
  const [selectedScanner, setSelectedScanner] = useState("trivy");
  const [scanTarget, setScanTarget] = useState("");
  const [scannerFilter, setScannerFilter] = useState<string | undefined>(undefined);
  const [severityFilter, setSeverityFilter] = useState<string | undefined>(undefined);
  const [findingStatusFilter, setFindingStatusFilter] = useState<string | undefined>("open");
  const [scansPage, setScansPage] = useState(1);
  const [findingsPage, setFindingsPage] = useState(1);

  const { data: dashboard, isLoading: dashLoading } = useScannerDashboard(orgId);
  const { data: scansData, isLoading: scansLoading } = useScannerScans(orgId, {
    scanner: scannerFilter,
    page: scansPage,
    page_size: 15,
  });
  const { data: findingsData, isLoading: findingsLoading } = useScannerFindings(orgId, {
    scanner: scannerFilter,
    severity: severityFilter,
    status: findingStatusFilter,
    page: findingsPage,
    page_size: 20,
  });
  const triggerScan = useScannerTrigger(orgId);
  const updateFinding = useScannerUpdateFinding(orgId);

  function handleTrigger() {
    if (!scanTarget.trim()) return;
    triggerScan.mutate(
      { scanner: selectedScanner, target: scanTarget.trim() },
      { onSuccess: () => { setShowTrigger(false); setScanTarget(""); } }
    );
  }

  const currentScannerInfo = SCANNERS.find((s) => s.id === selectedScanner);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <ShieldCheck className="h-8 w-8 text-primary" />
            Security Scanner
          </h1>
          <p className="text-muted-foreground">
            Multi-tool security scanning — Trivy, Semgrep, Gitleaks, Checkov, ZAP, Nuclei
          </p>
        </div>
        <Button onClick={() => setShowTrigger((v) => !v)} className="gap-1.5">
          <Play className="h-4 w-4" />
          New Scan
        </Button>
      </div>

      {/* Trigger Modal */}
      {showTrigger && (
        <Card className="border-primary">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Trigger Security Scan</CardTitle>
              <Button size="sm" variant="ghost" onClick={() => setShowTrigger(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
              {SCANNERS.map((s) => {
                const Icon = s.icon;
                return (
                  <button
                    key={s.id}
                    onClick={() => { setSelectedScanner(s.id); setScanTarget(""); }}
                    className={`flex items-center gap-2 rounded-lg border p-3 text-left text-sm transition-colors ${
                      selectedScanner === s.id
                        ? "border-primary bg-primary/10"
                        : "border-border hover:bg-accent/50"
                    }`}
                  >
                    <Icon className="h-5 w-5 shrink-0" />
                    <div>
                      <div className="font-medium">{s.label}</div>
                      <div className="text-xs text-muted-foreground">{s.desc}</div>
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Scan Target</label>
              <input
                type="text"
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder={currentScannerInfo?.placeholder || "Enter target..."}
                value={scanTarget}
                onChange={(e) => setScanTarget(e.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                {selectedScanner === "trivy" && "Docker image name (e.g., python:3.11-slim, node:18-alpine)"}
                {selectedScanner === "semgrep" && "Path to source code directory"}
                {selectedScanner === "gitleaks" && "Path to git repository"}
                {selectedScanner === "checkov" && "Path to IaC files (Terraform, Dockerfile, K8s YAML)"}
                {selectedScanner === "zap" && "URL of the web application to scan"}
                {selectedScanner === "nuclei" && "URL of the target to scan"}
                {selectedScanner === "prowler" && "AWS profile name (use 'default' for default profile)"}
              </p>
            </div>

            <div className="flex gap-2 pt-2">
              <Button onClick={handleTrigger} disabled={!scanTarget.trim() || triggerScan.isPending}>
                {triggerScan.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Play className="mr-2 h-4 w-4" />
                )}
                Start Scan
              </Button>
              <Button variant="ghost" onClick={() => setShowTrigger(false)}>Cancel</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tabs */}
      <div className="flex gap-2 border-b pb-1">
        {(["dashboard", "scans", "findings"] as TabValue[]).map((tab) => (
          <Button
            key={tab}
            variant={activeTab === tab ? "default" : "ghost"}
            size="sm"
            onClick={() => setActiveTab(tab)}
            className="capitalize"
          >
            {tab === "dashboard" && <ShieldCheck className="mr-1.5 h-4 w-4" />}
            {tab === "scans" && <Play className="mr-1.5 h-4 w-4" />}
            {tab === "findings" && <AlertTriangle className="mr-1.5 h-4 w-4" />}
            {tab}
          </Button>
        ))}
      </div>

      {/* ========= DASHBOARD TAB ========= */}
      {activeTab === "dashboard" && (
        <div className="space-y-6">
          {dashLoading ? (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {[1, 2, 3, 4].map((i) => <Skeleton key={i} className="h-24 rounded-xl" />)}
            </div>
          ) : dashboard ? (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <Card>
                <CardContent className="p-4 text-center">
                  <div className="text-2xl font-bold">{dashboard.total_scans}</div>
                  <div className="text-xs text-muted-foreground">Total Scans</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <div className="text-2xl font-bold text-red-600">{dashboard.critical_findings}</div>
                  <div className="text-xs text-muted-foreground">Critical</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <div className="text-2xl font-bold text-orange-600">{dashboard.high_findings}</div>
                  <div className="text-xs text-muted-foreground">High</div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <div className="text-2xl font-bold">{dashboard.open_findings}</div>
                  <div className="text-xs text-muted-foreground">Open Findings</div>
                </CardContent>
              </Card>
            </div>
          ) : null}

          {/* Scanner cards */}
          <div>
            <h2 className="mb-3 text-lg font-semibold">Available Scanners</h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {SCANNERS.map((s) => {
                const Icon = s.icon;
                const active = dashboard?.scanners_active?.includes(s.id);
                const findingCount = dashboard?.findings_by_scanner?.[s.id] || 0;
                return (
                  <Card key={s.id} className="transition-colors hover:bg-accent/30">
                    <CardContent className="flex items-start gap-3 p-4">
                      <div className={`rounded-lg p-2 ${SCANNER_COLORS[s.id] || "bg-muted"}`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-medium">{s.label}</span>
                          {active && <Badge variant="outline" className="text-[10px]">Active</Badge>}
                        </div>
                        <p className="mt-0.5 text-xs text-muted-foreground">{s.desc}</p>
                        {findingCount > 0 && (
                          <p className="mt-1 text-xs text-red-600 dark:text-red-400">{findingCount} open findings</p>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* Recent scans */}
          {dashboard?.recent_scans?.length > 0 && (
            <div>
              <h2 className="mb-3 text-lg font-semibold">Recent Scans</h2>
              <div className="space-y-2">
                {dashboard.recent_scans.slice(0, 5).map((scan: any) => (
                  <Card key={scan.id}>
                    <CardContent className="flex items-center gap-4 p-3">
                      <Badge className={SCANNER_COLORS[scan.scanner] || ""}>{scan.scanner}</Badge>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium truncate">{scan.target}</div>
                        <div className="text-xs text-muted-foreground">
                          {scan.created_at && new Date(scan.created_at).toLocaleString()}
                        </div>
                      </div>
                      <div className="text-right text-xs">
                        <span className="text-red-600">{scan.critical_count + scan.high_count} critical/high</span>
                        <span className="ml-2 text-muted-foreground">{scan.total_findings} total</span>
                      </div>
                      <Badge className={STATUS_COLORS[scan.status] || ""}>{scan.status}</Badge>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========= SCANS TAB ========= */}
      {activeTab === "scans" && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <span className="flex items-center text-sm text-muted-foreground mr-1">Scanner:</span>
            <Button variant={!scannerFilter ? "default" : "outline"} size="sm" onClick={() => { setScannerFilter(undefined); setScansPage(1); }}>All</Button>
            {SCANNERS.map((s) => (
              <Button
                key={s.id}
                variant={scannerFilter === s.id ? "default" : "outline"}
                size="sm"
                onClick={() => { setScannerFilter(s.id); setScansPage(1); }}
              >
                {s.label}
              </Button>
            ))}
          </div>

          {scansLoading ? (
            <div className="space-y-3">{[1, 2, 3].map((i) => <Skeleton key={i} className="h-16 rounded-xl" />)}</div>
          ) : scansData?.items?.length > 0 ? (
            <>
              <div className="space-y-2">
                {scansData.items.map((scan: any) => (
                  <Card key={scan.id}>
                    <CardContent className="flex items-center gap-4 p-3">
                      <Badge className={SCANNER_COLORS[scan.scanner] || ""}>{scan.scanner}</Badge>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium truncate">{scan.target}</div>
                        <div className="text-xs text-muted-foreground">
                          {scan.created_at && new Date(scan.created_at).toLocaleString()}
                          {scan.duration_seconds != null && ` · ${scan.duration_seconds.toFixed(1)}s`}
                        </div>
                      </div>
                      <div className="hidden text-right text-xs sm:block">
                        {scan.critical_count > 0 && <span className="text-red-600 mr-2">{scan.critical_count}C</span>}
                        {scan.high_count > 0 && <span className="text-orange-600 mr-2">{scan.high_count}H</span>}
                        {scan.medium_count > 0 && <span className="text-yellow-600 mr-2">{scan.medium_count}M</span>}
                        {scan.low_count > 0 && <span className="text-green-600">{scan.low_count}L</span>}
                      </div>
                      <Badge className={STATUS_COLORS[scan.status] || ""}>{scan.status}</Badge>
                    </CardContent>
                  </Card>
                ))}
              </div>
              {scansData.total_pages > 1 && (
                <div className="flex items-center justify-center gap-2">
                  <Button size="sm" variant="outline" disabled={scansPage <= 1} onClick={() => setScansPage((p) => p - 1)}>
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <span className="text-sm text-muted-foreground">Page {scansPage} of {scansData.total_pages}</span>
                  <Button size="sm" variant="outline" disabled={scansPage >= scansData.total_pages} onClick={() => setScansPage((p) => p + 1)}>
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <ShieldCheck className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No scans yet</h3>
                <p className="text-sm text-muted-foreground mt-1">Click &quot;New Scan&quot; to run your first security scan.</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* ========= FINDINGS TAB ========= */}
      {activeTab === "findings" && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <span className="flex items-center text-sm text-muted-foreground mr-1">Scanner:</span>
            <Button variant={!scannerFilter ? "default" : "outline"} size="sm" onClick={() => { setScannerFilter(undefined); setFindingsPage(1); }}>All</Button>
            {SCANNERS.map((s) => (
              <Button key={s.id} variant={scannerFilter === s.id ? "default" : "outline"} size="sm" onClick={() => { setScannerFilter(s.id); setFindingsPage(1); }}>{s.label}</Button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="flex items-center text-sm text-muted-foreground mr-1">Severity:</span>
            {[undefined, "critical", "high", "medium", "low"].map((sev) => (
              <Button key={sev || "all"} variant={severityFilter === sev ? "default" : "outline"} size="sm" onClick={() => { setSeverityFilter(sev); setFindingsPage(1); }}>
                {sev ? sev.charAt(0).toUpperCase() + sev.slice(1) : "All"}
              </Button>
            ))}
            <span className="mx-2 border-l" />
            <span className="flex items-center text-sm text-muted-foreground mr-1">Status:</span>
            {[undefined, "open", "acknowledged", "resolved", "false_positive"].map((st) => (
              <Button key={st || "all"} variant={findingStatusFilter === st ? "default" : "outline"} size="sm" onClick={() => { setFindingStatusFilter(st); setFindingsPage(1); }}>
                {st ? st.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase()) : "All"}
              </Button>
            ))}
          </div>

          {findingsLoading ? (
            <div className="space-y-3">{[1, 2, 3].map((i) => <Skeleton key={i} className="h-20 rounded-xl" />)}</div>
          ) : findingsData?.items?.length > 0 ? (
            <>
              <div className="space-y-2">
                {findingsData.items.map((finding: any) => (
                  <Card key={finding.id}>
                    <CardContent className="flex items-start gap-3 p-4">
                      {finding.severity === "critical" || finding.severity === "high" ? (
                        <XCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-500" />
                      ) : finding.status === "resolved" ? (
                        <CheckCircle className="mt-0.5 h-5 w-5 shrink-0 text-green-500" />
                      ) : (
                        <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-yellow-500" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium">{finding.title}</div>
                        {finding.location && (
                          <div className="mt-0.5 text-xs text-muted-foreground truncate">
                            {finding.location}{finding.line_number ? `:${finding.line_number}` : ""}
                          </div>
                        )}
                        {finding.remediation && (
                          <div className="mt-1 text-xs text-muted-foreground">
                            Fix: {finding.remediation.slice(0, 150)}{finding.remediation.length > 150 ? "..." : ""}
                          </div>
                        )}
                        <div className="mt-1.5 flex flex-wrap gap-1.5">
                          <Badge className={SCANNER_COLORS[finding.scanner] || ""}>{finding.scanner}</Badge>
                          {finding.cve_id && <Badge variant="outline" className="text-[10px]">{finding.cve_id}</Badge>}
                          {finding.rule_id && !finding.cve_id && <Badge variant="outline" className="text-[10px]">{finding.rule_id}</Badge>}
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-1.5 shrink-0">
                        <Badge className={SEVERITY_COLORS[finding.severity] || ""}>{finding.severity}</Badge>
                        {finding.status === "open" && (
                          <div className="flex gap-1">
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-6 px-2 text-[10px]"
                              onClick={() => updateFinding.mutate({ findingId: finding.id, status: "acknowledged" })}
                              title="Acknowledge"
                            >
                              <Eye className="h-3 w-3" />
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-6 px-2 text-[10px]"
                              onClick={() => updateFinding.mutate({ findingId: finding.id, status: "false_positive" })}
                              title="Mark as false positive"
                            >
                              <EyeOff className="h-3 w-3" />
                            </Button>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
              {findingsData.total_pages > 1 && (
                <div className="flex items-center justify-center gap-2">
                  <Button size="sm" variant="outline" disabled={findingsPage <= 1} onClick={() => setFindingsPage((p) => p - 1)}>
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <span className="text-sm text-muted-foreground">Page {findingsPage} of {findingsData.total_pages} ({findingsData.total} findings)</span>
                  <Button size="sm" variant="outline" disabled={findingsPage >= findingsData.total_pages} onClick={() => setFindingsPage((p) => p + 1)}>
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <AlertTriangle className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No findings</h3>
                <p className="text-sm text-muted-foreground mt-1">Run a security scan to see findings here.</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
