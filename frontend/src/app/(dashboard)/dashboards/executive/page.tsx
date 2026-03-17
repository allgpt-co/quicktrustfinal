"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useExecutiveDashboard } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  CheckCircle,
  AlertTriangle,
  AlertCircle,
  FileText,
  GraduationCap,
  Activity,
  ArrowLeft,
} from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  Cell,
} from "recharts";
import { useChartColors } from "@/hooks/use-chart-colors";

const HEATMAP_COLORS: Record<string, string> = {
  low: "#22c55e",
  medium: "#eab308",
  high: "#f97316",
  critical: "#ef4444",
};

function getHeatmapColor(likelihood: number, impact: number): string {
  const score = likelihood * impact;
  if (score >= 16) return HEATMAP_COLORS.critical;
  if (score >= 9) return HEATMAP_COLORS.high;
  if (score >= 4) return HEATMAP_COLORS.medium;
  return HEATMAP_COLORS.low;
}

export default function ExecutiveDashboardPage() {
  const orgId = useOrgId();
  const colors = useChartColors();
  const { data, isLoading, error } = useExecutiveDashboard(orgId);

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

  return (
    <div className="space-y-6">
      <Header />

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
        <MetricCard
          title="Compliance Score"
          value={isLoading ? null : `${data?.compliance_score ?? 0}%`}
          icon={<CheckCircle className="h-4 w-4" />}
          progress={data?.compliance_score}
          loading={isLoading}
        />
        <MetricCard
          title="Controls"
          value={isLoading ? null : `${data?.implemented_controls ?? 0}/${data?.total_controls ?? 0}`}
          icon={<CheckCircle className="h-4 w-4" />}
          sub="implemented"
          loading={isLoading}
        />
        <MetricCard
          title="Open Risks"
          value={isLoading ? null : String(data?.total_risks ?? 0)}
          icon={<AlertTriangle className="h-4 w-4" />}
          badge={data?.critical_risks ? `${data.critical_risks} critical` : undefined}
          badgeVariant="destructive"
          loading={isLoading}
        />
        <MetricCard
          title="Open Incidents"
          value={isLoading ? null : String(data?.open_incidents ?? 0)}
          icon={<AlertCircle className="h-4 w-4" />}
          badge={data?.p1_incidents ? `${data.p1_incidents} P1/P2` : undefined}
          badgeVariant="destructive"
          loading={isLoading}
        />
        <MetricCard
          title="Policies"
          value={isLoading ? null : `${data?.policies_published ?? 0}/${data?.policies_total ?? 0}`}
          icon={<FileText className="h-4 w-4" />}
          sub="published"
          loading={isLoading}
        />
        <MetricCard
          title="Training"
          value={isLoading ? null : `${data?.training_completion_pct ?? 0}%`}
          icon={<GraduationCap className="h-4 w-4" />}
          sub="completion"
          loading={isLoading}
        />
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Compliance Trend */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Compliance Score Trend</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <Skeleton className="h-[250px] w-full" />
            ) : (
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={data?.compliance_trend || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
                  <XAxis dataKey="date" tick={{ fontSize: 11, fill: colors.text }} stroke={colors.grid} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: colors.text }} stroke={colors.grid} />
                  <Tooltip contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }} />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke={colors.primary}
                    strokeWidth={2}
                    dot={{ r: 4 }}
                    name="Score %"
                  />
                </LineChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>

        {/* Risk Heatmap */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Risk Heatmap</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <Skeleton className="h-[250px] w-full" />
            ) : (
              <RiskHeatmap cells={data?.risk_heatmap || []} colors={colors} />
            )}
          </CardContent>
        </Card>
      </div>

      {/* Framework Compliance */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Framework Compliance</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <Skeleton className="h-[200px] w-full" />
          ) : data?.frameworks?.length ? (
            <ResponsiveContainer width="100%" height={Math.max(200, (data.frameworks.length) * 50)}>
              <BarChart data={data.frameworks} layout="vertical" margin={{ left: 120 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11, fill: colors.text }} stroke={colors.grid} />
                <YAxis
                  type="category"
                  dataKey="framework_name"
                  tick={{ fontSize: 11, fill: colors.text }}
                  width={110}
                  stroke={colors.grid}
                />
                <Tooltip contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }} formatter={(v: number) => `${v}%`} />
                <Bar dataKey="compliance_pct" name="Compliance %" radius={[0, 4, 4, 0]}>
                  {data.frameworks.map((fw: any, i: number) => (
                    <Cell
                      key={i}
                      fill={fw.compliance_pct >= 80 ? "#22c55e" : fw.compliance_pct >= 50 ? "#eab308" : "#ef4444"}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-muted-foreground">No frameworks loaded yet.</p>
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
        <h1 className="text-3xl font-bold">Executive Dashboard</h1>
        <p className="text-muted-foreground">High-level compliance and risk overview</p>
      </div>
    </div>
  );
}

function MetricCard({
  title,
  value,
  icon,
  sub,
  badge,
  badgeVariant,
  progress: progressVal,
  loading,
}: {
  title: string;
  value: string | null;
  icon: React.ReactNode;
  sub?: string;
  badge?: string;
  badgeVariant?: "destructive" | "default";
  progress?: number;
  loading?: boolean;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <span className="text-muted-foreground">{icon}</span>
      </CardHeader>
      <CardContent>
        {loading ? (
          <Skeleton className="h-8 w-20" />
        ) : (
          <>
            <div className="text-2xl font-bold">{value}</div>
            {progressVal !== undefined && <Progress value={progressVal} className="mt-2" />}
            {sub && <p className="text-xs text-muted-foreground">{sub}</p>}
            {badge && (
              <Badge variant={badgeVariant || "default"} className="mt-1">
                {badge}
              </Badge>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}

function RiskHeatmap({ cells, colors }: { cells: Array<{ likelihood: number; impact: number; count: number }>; colors: { text: string; textMuted: string; grid: string } }) {
  const cellMap: Record<string, number> = {};
  cells.forEach((c) => {
    cellMap[`${c.likelihood}-${c.impact}`] = c.count;
  });

  const labels = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"];
  const impactLabels = ["Negligible", "Minor", "Moderate", "Major", "Severe"];

  return (
    <div className="space-y-1.5">
      {/* Impact labels across top */}
      <div className="flex items-end gap-1.5 ml-24">
        {impactLabels.map((l, i) => (
          <div key={i} className="flex-1 text-center text-xs font-semibold text-foreground">{l}</div>
        ))}
      </div>
      {[5, 4, 3, 2, 1].map((likelihood) => (
        <div key={likelihood} className="flex items-center gap-1.5">
          <div className="w-24 text-right text-xs font-semibold text-foreground pr-2">
            {labels[likelihood - 1]}
          </div>
          {[1, 2, 3, 4, 5].map((impact) => {
            const count = cellMap[`${likelihood}-${impact}`] || 0;
            return (
              <div
                key={impact}
                className="flex-1 aspect-square rounded flex items-center justify-center text-sm font-bold min-h-[40px]"
                style={{
                  backgroundColor: count > 0 ? getHeatmapColor(likelihood, impact) : colors.grid,
                  color: count > 0 ? "#fff" : colors.textMuted,
                }}
                title={`L${likelihood} x I${impact}: ${count} risks`}
              >
                {count > 0 ? count : ""}
              </div>
            );
          })}
        </div>
      ))}
      <div className="flex justify-center gap-4 mt-3 text-xs font-medium text-foreground">
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded" style={{ background: "#22c55e" }} /> Low</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded" style={{ background: "#eab308" }} /> Medium</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded" style={{ background: "#f97316" }} /> High</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded" style={{ background: "#ef4444" }} /> Critical</span>
      </div>
    </div>
  );
}
