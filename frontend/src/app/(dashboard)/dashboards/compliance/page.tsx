"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useComplianceDashboard } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  ArrowLeft,
  AlertTriangle,
  FileCheck,
  FileText,
  ClipboardSignature,
  Shield,
} from "lucide-react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  LineChart,
  Line,
} from "recharts";
import { useChartColors } from "@/hooks/use-chart-colors";

const PIE_COLORS = ["#22c55e", "#eab308", "#ef4444"];

export default function ComplianceDashboardPage() {
  const orgId = useOrgId();
  const colors = useChartColors();
  const { data, isLoading, error } = useComplianceDashboard(orgId);

  if (error) {
    return (
      <div className="space-y-6">
        <Header />
        <Card className="border-destructive">
          <CardContent className="p-8 text-center">
            <AlertTriangle className="h-8 w-8 text-destructive mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">{error.message}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const evidencePie = data ? [
    { name: "Fresh", value: data.fresh_evidence, color: "#22c55e" },
    { name: "Stale (>90d)", value: data.stale_evidence, color: "#ef4444" },
  ].filter(d => d.value > 0) : [];

  const policyPie = data ? [
    { name: "Published", value: data.policies_published, color: "#22c55e" },
    { name: "Draft", value: data.policies_draft, color: "#eab308" },
    { name: "Other", value: Math.max(0, data.policies_total - data.policies_published - data.policies_draft), color: "#94a3b8" },
  ].filter(d => d.value > 0) : [];

  return (
    <div className="space-y-6">
      <Header />

      {/* Top Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <StatCard icon={<Shield className="h-4 w-4" />} title="Frameworks" loading={isLoading}
          value={data?.frameworks?.length ?? 0} />
        <StatCard icon={<FileCheck className="h-4 w-4" />} title="Evidence Coverage" loading={isLoading}
          value={`${data?.evidence_coverage_pct ?? 0}%`} progress={data?.evidence_coverage_pct} />
        <StatCard icon={<FileCheck className="h-4 w-4" />} title="Total Evidence" loading={isLoading}
          value={data?.total_evidence ?? 0} sub={`${data?.fresh_evidence ?? 0} fresh`} />
        <StatCard icon={<FileText className="h-4 w-4" />} title="Policies" loading={isLoading}
          value={`${data?.policies_published ?? 0}/${data?.policies_total ?? 0}`} sub="published" />
        <StatCard icon={<ClipboardSignature className="h-4 w-4" />} title="Pending Sign-offs" loading={isLoading}
          value={data?.pending_acknowledgments ?? 0}
          badge={data?.pending_acknowledgments ? `${data.pending_acknowledgments} pending` : undefined} />
      </div>

      {/* Framework Compliance Bars */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Framework Compliance</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <Skeleton className="h-[200px] w-full" />
          ) : data?.frameworks?.length ? (
            <div className="space-y-4">
              {data.frameworks.map((fw: any) => (
                <div key={fw.framework_id} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{fw.framework_name} <span className="text-muted-foreground">v{fw.version}</span></span>
                    <span className="text-muted-foreground">
                      {fw.implemented}/{fw.total_controls} ({fw.compliance_pct}%)
                    </span>
                  </div>
                  <Progress value={fw.compliance_pct} className="h-3" />
                  <div className="flex gap-3 text-xs text-muted-foreground">
                    <span className="text-green-600">{fw.implemented} implemented</span>
                    <span className="text-yellow-600">{fw.partially_implemented} partial</span>
                    <span className="text-red-600">{fw.not_implemented} not impl</span>
                    <span className="text-gray-400">{fw.not_applicable} N/A</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No frameworks loaded.</p>
          )}
        </CardContent>
      </Card>

      {/* Charts Row */}
      <div className="grid gap-4 md:grid-cols-3">
        {/* Evidence Freshness Pie */}
        <Card>
          <CardHeader><CardTitle className="text-base">Evidence Freshness</CardTitle></CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-[200px]" /> : evidencePie.length ? (
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={evidencePie} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={{ fill: colors.text, fontSize: 12 }}>
                    {evidencePie.map((d, i) => <Cell key={i} fill={d.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }} />
                  <Legend wrapperStyle={{ color: colors.text }} />
                </PieChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-muted-foreground text-center py-8">No evidence data</p>}
          </CardContent>
        </Card>

        {/* Policy Status Pie */}
        <Card>
          <CardHeader><CardTitle className="text-base">Policy Status</CardTitle></CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-[200px]" /> : policyPie.length ? (
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={policyPie} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label={{ fill: colors.text, fontSize: 12 }}>
                    {policyPie.map((d, i) => <Cell key={i} fill={d.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }} />
                  <Legend wrapperStyle={{ color: colors.text }} />
                </PieChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-muted-foreground text-center py-8">No policy data</p>}
          </CardContent>
        </Card>

        {/* Compliance Trend */}
        <Card>
          <CardHeader><CardTitle className="text-base">Compliance Trend</CardTitle></CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-[200px]" /> : (
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={data?.compliance_trend || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
                  <XAxis dataKey="date" tick={{ fontSize: 10, fill: colors.text }} stroke={colors.grid} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: colors.text }} stroke={colors.grid} />
                  <Tooltip contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }} />
                  <Line type="monotone" dataKey="score" stroke={colors.primary} strokeWidth={2} name="Score %" />
                </LineChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Evidence Gaps Table */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Evidence Gaps</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <Skeleton className="h-[150px] w-full" />
          ) : data?.evidence_gaps?.length ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-muted-foreground">
                    <th className="pb-2 font-medium">Control</th>
                    <th className="pb-2 font-medium">Status</th>
                    <th className="pb-2 font-medium">Evidence</th>
                    <th className="pb-2 font-medium">Age</th>
                  </tr>
                </thead>
                <tbody>
                  {data.evidence_gaps.map((gap: any) => (
                    <tr key={gap.control_id} className="border-b last:border-0">
                      <td className="py-2 pr-4 font-medium">{gap.control_title}</td>
                      <td className="py-2 pr-4">
                        <Badge variant={gap.status === "implemented" ? "success" : gap.status === "not_implemented" ? "destructive" : "secondary"}>
                          {gap.status}
                        </Badge>
                      </td>
                      <td className="py-2 pr-4">{gap.evidence_count}</td>
                      <td className="py-2">
                        {gap.freshest_evidence_days !== null
                          ? <span className="text-red-500">{gap.freshest_evidence_days}d old</span>
                          : <span className="text-muted-foreground">None</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">All controls have fresh evidence.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Header() {
  return (
    <div className="flex items-center gap-3">
      <Link href="/dashboards" className="text-muted-foreground hover:text-foreground">
        <ArrowLeft className="h-5 w-5" />
      </Link>
      <div>
        <h1 className="text-3xl font-bold">Compliance Manager Dashboard</h1>
        <p className="text-muted-foreground">Framework progress, evidence coverage, and policy status</p>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value, sub, badge, progress: p, loading }: {
  icon: React.ReactNode; title: string; value: any; sub?: string;
  badge?: string; progress?: number; loading?: boolean;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <span className="text-muted-foreground">{icon}</span>
      </CardHeader>
      <CardContent>
        {loading ? <Skeleton className="h-8 w-20" /> : (
          <>
            <div className="text-2xl font-bold">{value}</div>
            {p !== undefined && <Progress value={p} className="mt-2" />}
            {sub && <p className="text-xs text-muted-foreground">{sub}</p>}
            {badge && <Badge variant="warning" className="mt-1">{badge}</Badge>}
          </>
        )}
      </CardContent>
    </Card>
  );
}
