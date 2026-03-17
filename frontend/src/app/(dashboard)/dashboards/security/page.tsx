"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useSecurityDashboard } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  ArrowLeft,
  AlertTriangle,
  ShieldAlert,
  ShieldCheck,
  Activity,
  Bug,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { useChartColors } from "@/hooks/use-chart-colors";

const SEV_COLORS = {
  critical: "#ef4444",
  high: "#f97316",
  medium: "#eab308",
  low: "#22c55e",
};

export default function SecurityDashboardPage() {
  const orgId = useOrgId();
  const colors = useChartColors();
  const { data, isLoading, error } = useSecurityDashboard(orgId);

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

  const severityPie = data ? [
    { name: "Critical", value: data.critical_findings, color: SEV_COLORS.critical },
    { name: "High", value: data.high_findings, color: SEV_COLORS.high },
    { name: "Medium", value: data.medium_findings, color: SEV_COLORS.medium },
    { name: "Low", value: data.low_findings, color: SEV_COLORS.low },
  ].filter(d => d.value > 0) : [];

  return (
    <div className="space-y-6">
      <Header />

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
        <MetricCard title="Total Findings" value={data?.total_findings ?? 0} loading={isLoading}
          icon={<Bug className="h-4 w-4" />} />
        <MetricCard title="Critical" value={data?.critical_findings ?? 0} loading={isLoading}
          icon={<ShieldAlert className="h-4 w-4 text-red-500" />}
          className={data?.critical_findings ? "border-red-500/30" : ""} />
        <MetricCard title="High" value={data?.high_findings ?? 0} loading={isLoading}
          icon={<ShieldAlert className="h-4 w-4 text-orange-500" />} />
        <MetricCard title="Open" value={data?.open_findings ?? 0} loading={isLoading}
          icon={<AlertTriangle className="h-4 w-4" />} />
        <MetricCard title="Resolved" value={data?.resolved_findings ?? 0} loading={isLoading}
          icon={<ShieldCheck className="h-4 w-4 text-green-500" />} />
        <MetricCard title="Open Alerts" value={data?.open_alerts ?? 0} loading={isLoading}
          icon={<Activity className="h-4 w-4" />} />
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Vulnerability Trend */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Vulnerability Trend (8 Weeks)</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <Skeleton className="h-[280px] w-full" />
            ) : (
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={data?.vulnerability_trend || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
                  <XAxis dataKey="date" tick={{ fontSize: 10, fill: colors.text }} stroke={colors.grid} />
                  <YAxis tick={{ fontSize: 10, fill: colors.text }} stroke={colors.grid} />
                  <Tooltip contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }} />
                  <Legend wrapperStyle={{ color: colors.text }} />
                  <Area type="monotone" dataKey="critical" stackId="1" fill={SEV_COLORS.critical} stroke={SEV_COLORS.critical} name="Critical" />
                  <Area type="monotone" dataKey="high" stackId="1" fill={SEV_COLORS.high} stroke={SEV_COLORS.high} name="High" />
                  <Area type="monotone" dataKey="medium" stackId="1" fill={SEV_COLORS.medium} stroke={SEV_COLORS.medium} name="Medium" />
                  <Area type="monotone" dataKey="low" stackId="1" fill={SEV_COLORS.low} stroke={SEV_COLORS.low} name="Low" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>

        {/* Severity Distribution */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Severity Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <Skeleton className="h-[280px] w-full" />
            ) : severityPie.length ? (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie data={severityPie} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label={{ fill: colors.text, fontSize: 12 }}>
                    {severityPie.map((d, i) => <Cell key={i} fill={d.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }} />
                  <Legend wrapperStyle={{ color: colors.text }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[280px]">
                <div className="text-center">
                  <ShieldCheck className="h-12 w-12 text-green-500 mx-auto mb-2" />
                  <p className="text-sm text-muted-foreground">No findings detected</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Scanner Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Scanner Results</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <Skeleton className="h-[200px] w-full" />
          ) : data?.scanners?.length ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-muted-foreground">
                    <th className="pb-2 font-medium">Scanner</th>
                    <th className="pb-2 font-medium text-center">Total</th>
                    <th className="pb-2 font-medium text-center">Critical</th>
                    <th className="pb-2 font-medium text-center">High</th>
                    <th className="pb-2 font-medium text-center">Medium</th>
                    <th className="pb-2 font-medium text-center">Low</th>
                    <th className="pb-2 font-medium">Last Scan</th>
                  </tr>
                </thead>
                <tbody>
                  {data.scanners.map((s: any) => (
                    <tr key={s.scanner_name} className="border-b last:border-0">
                      <td className="py-2 pr-4 font-medium capitalize">{s.scanner_name}</td>
                      <td className="py-2 text-center">{s.total_findings}</td>
                      <td className="py-2 text-center">
                        {s.critical > 0 ? <Badge variant="destructive">{s.critical}</Badge> : <span className="text-muted-foreground">0</span>}
                      </td>
                      <td className="py-2 text-center">
                        {s.high > 0 ? <span className="text-orange-500 font-medium">{s.high}</span> : <span className="text-muted-foreground">0</span>}
                      </td>
                      <td className="py-2 text-center">{s.medium}</td>
                      <td className="py-2 text-center">{s.low}</td>
                      <td className="py-2 text-muted-foreground">{s.last_scan_date || "Never"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No scanner results yet. Run a security scan to see results.</p>
          )}
        </CardContent>
      </Card>

      {/* Monitoring Status */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-base">Monitoring Rules</CardTitle></CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-20" /> : (
              <div className="flex items-center gap-6">
                <div>
                  <div className="text-3xl font-bold">{data?.active_rules ?? 0}</div>
                  <p className="text-xs text-muted-foreground">active rules</p>
                </div>
                <div className="text-muted-foreground">/</div>
                <div>
                  <div className="text-3xl font-bold text-muted-foreground">{data?.total_monitor_rules ?? 0}</div>
                  <p className="text-xs text-muted-foreground">total rules</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Alert Status</CardTitle></CardHeader>
          <CardContent>
            {isLoading ? <Skeleton className="h-20" /> : (
              <div className="flex items-center gap-4">
                <Activity className="h-8 w-8 text-muted-foreground" />
                <div>
                  <div className="text-3xl font-bold">{data?.open_alerts ?? 0}</div>
                  <p className="text-xs text-muted-foreground">open alerts requiring attention</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
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
        <h1 className="text-3xl font-bold">Security Posture Dashboard</h1>
        <p className="text-muted-foreground">Scanner results, vulnerability trends, and monitoring</p>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, loading, className }: {
  title: string; value: number; icon: React.ReactNode; loading?: boolean; className?: string;
}) {
  return (
    <Card className={className}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <span className="text-muted-foreground">{icon}</span>
      </CardHeader>
      <CardContent>
        {loading ? <Skeleton className="h-8 w-16" /> : <div className="text-2xl font-bold">{value}</div>}
      </CardContent>
    </Card>
  );
}
