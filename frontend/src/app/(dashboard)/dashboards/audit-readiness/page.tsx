"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuditReadinessDashboard } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  ArrowLeft,
  AlertTriangle,
  CheckCircle,
  Target,
  GraduationCap,
  UserCheck,
  ClipboardCheck,
} from "lucide-react";
import {
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";
import { useChartColors } from "@/hooks/use-chart-colors";

function getScoreColor(score: number): string {
  if (score >= 80) return "#22c55e";
  if (score >= 60) return "#eab308";
  if (score >= 40) return "#f97316";
  return "#ef4444";
}

function getScoreLabel(score: number): string {
  if (score >= 90) return "Audit Ready";
  if (score >= 75) return "Nearly Ready";
  if (score >= 50) return "Needs Work";
  return "Not Ready";
}

export default function AuditReadinessDashboardPage() {
  const orgId = useOrgId();
  const colors = useChartColors();
  const { data, isLoading, error } = useAuditReadinessDashboard(orgId);

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

  const overallScore = data?.overall_score ?? 0;
  const scoreColor = getScoreColor(overallScore);
  const scoreLabel = getScoreLabel(overallScore);

  const gaugeData = [{ name: "Score", value: overallScore, fill: scoreColor }];

  return (
    <div className="space-y-6">
      <Header />

      {/* Overall Score + Breakdown */}
      <div className="grid gap-4 md:grid-cols-3">
        {/* Radial Gauge */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle className="text-base text-center">Overall Readiness</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center">
            {isLoading ? (
              <Skeleton className="h-[200px] w-[200px] rounded-full" />
            ) : (
              <>
                <ResponsiveContainer width={200} height={200}>
                  <RadialBarChart
                    cx="50%" cy="50%"
                    innerRadius="70%" outerRadius="100%"
                    startAngle={180} endAngle={0}
                    data={gaugeData}
                  >
                    <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                    <RadialBar
                      dataKey="value"
                      cornerRadius={10}
                      background={{ fill: colors.grid }}
                    />
                  </RadialBarChart>
                </ResponsiveContainer>
                <div className="text-center -mt-16">
                  <div className="text-4xl font-bold" style={{ color: scoreColor }}>
                    {overallScore}
                  </div>
                  <div className="text-sm font-medium" style={{ color: scoreColor }}>
                    {scoreLabel}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">out of 100</p>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Score Breakdown */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="text-base">Score Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-4">
                {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-16 w-full" />)}
              </div>
            ) : (
              <div className="space-y-4">
                {data?.breakdown?.map((item: any) => (
                  <div key={item.category} className="space-y-1">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <CategoryIcon category={item.category} />
                        <span className="font-medium text-sm">{item.label}</span>
                        <Badge variant="outline" className="text-xs">
                          {Math.round(item.weight * 100)}% weight
                        </Badge>
                      </div>
                      <div className="text-right">
                        <span className="font-bold" style={{ color: getScoreColor(item.score) }}>
                          {item.score}%
                        </span>
                        <span className="text-xs text-muted-foreground ml-2">
                          ({item.weighted_score} pts)
                        </span>
                      </div>
                    </div>
                    <Progress value={item.score} className="h-2" />
                    <p className="text-xs text-muted-foreground">{item.detail}</p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Category Breakdown Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Weighted Contribution</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <Skeleton className="h-[200px] w-full" />
          ) : (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data?.breakdown || []} layout="vertical" margin={{ left: 140 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
                <XAxis type="number" domain={[0, 50]} tick={{ fontSize: 11, fill: colors.text }} stroke={colors.grid} />
                <YAxis type="category" dataKey="label" tick={{ fontSize: 11, fill: colors.text }} width={130} stroke={colors.grid} />
                <Tooltip
                  contentStyle={{ backgroundColor: colors.tooltipBg, border: `1px solid ${colors.tooltipBorder}`, color: colors.text, borderRadius: 8 }}
                  formatter={(v: number) => [`${v} pts`, "Weighted Score"]}
                />
                <Bar dataKey="weighted_score" name="Points" radius={[0, 4, 4, 0]}>
                  {(data?.breakdown || []).map((item: any, i: number) => (
                    <Cell key={i} fill={getScoreColor(item.score)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </CardContent>
      </Card>

      {/* Additional Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Training Completion" value={`${data?.training_completion_pct ?? 0}%`}
          icon={<GraduationCap className="h-4 w-4" />} loading={isLoading}
          progress={data?.training_completion_pct} />
        <StatCard title="Open Audit Findings" value={data?.open_findings ?? 0}
          icon={<AlertTriangle className="h-4 w-4" />} loading={isLoading}
          variant={data?.open_findings ? "warning" : "default"} />
        <StatCard title="Pending Access Reviews" value={data?.pending_access_reviews ?? 0}
          icon={<UserCheck className="h-4 w-4" />} loading={isLoading} />
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Target</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">90/100</div>
            <p className="text-xs text-muted-foreground">recommended before scheduling audit</p>
            {!isLoading && overallScore < 90 && (
              <p className="text-xs text-orange-500 mt-1">
                {Math.ceil(90 - overallScore)} points to go
              </p>
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
        <h1 className="text-3xl font-bold">Audit Readiness Dashboard</h1>
        <p className="text-muted-foreground">Weighted readiness score across controls, evidence, policies, and risks</p>
      </div>
    </div>
  );
}

function CategoryIcon({ category }: { category: string }) {
  const icons: Record<string, React.ReactNode> = {
    controls: <CheckCircle className="h-4 w-4 text-blue-500" />,
    evidence: <ClipboardCheck className="h-4 w-4 text-green-500" />,
    policies: <Target className="h-4 w-4 text-purple-500" />,
    risks: <AlertTriangle className="h-4 w-4 text-orange-500" />,
  };
  return <>{icons[category] || null}</>;
}

function StatCard({ title, value, icon, loading, progress: p, variant }: {
  title: string; value: any; icon: React.ReactNode; loading?: boolean;
  progress?: number; variant?: string;
}) {
  return (
    <Card className={variant === "warning" ? "border-orange-500/30" : ""}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <span className="text-muted-foreground">{icon}</span>
      </CardHeader>
      <CardContent>
        {loading ? <Skeleton className="h-8 w-20" /> : (
          <>
            <div className="text-2xl font-bold">{value}</div>
            {p !== undefined && <Progress value={p} className="mt-2" />}
          </>
        )}
      </CardContent>
    </Card>
  );
}
