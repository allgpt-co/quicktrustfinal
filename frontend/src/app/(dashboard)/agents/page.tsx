"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { useAgentRuns } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Bot,
  ListChecks,
  FileText,
  FileCheck,
  AlertTriangle,
  Wrench,
  ClipboardCheck,
  Building2,
  Shield,
  Activity,
  HelpCircle,
  Coins,
  Zap,
  Clock,
  CheckCircle,
  XCircle,
} from "lucide-react";

const agents = [
  {
    slug: "controls-generation",
    name: "Controls Generation",
    description: "Generate tailored security controls from compliance frameworks using AI.",
    icon: ListChecks,
    category: "Compliance",
  },
  {
    slug: "policy-generation",
    name: "Policy Generation",
    description: "Auto-generate compliance policies based on frameworks and company context.",
    icon: FileText,
    category: "Compliance",
  },
  {
    slug: "evidence-generation",
    name: "Evidence Generation",
    description: "Generate evidence artifacts for controls to demonstrate compliance.",
    icon: FileCheck,
    category: "Compliance",
  },
  {
    slug: "risk-assessment",
    name: "Risk Assessment",
    description: "Identify and score potential risks based on control gaps and organizational context.",
    icon: AlertTriangle,
    category: "Risk",
  },
  {
    slug: "remediation",
    name: "Remediation Planner",
    description: "Generate step-by-step remediation plans for failing or incomplete controls.",
    icon: Wrench,
    category: "Risk",
  },
  {
    slug: "audit-preparation",
    name: "Audit Preparation",
    description: "Analyze audit readiness, identify evidence gaps, and generate workpapers.",
    icon: ClipboardCheck,
    category: "Audit",
  },
  {
    slug: "vendor-risk-assessment",
    name: "Vendor Risk Assessment",
    description: "Assess vendor risk levels, score vendors, and generate recommendations.",
    icon: Building2,
    category: "Vendor",
  },
  {
    slug: "pentest-orchestrator",
    name: "Penetration Test Planner",
    description: "Generate structured penetration test plans and simulated findings.",
    icon: Shield,
    category: "Security",
  },
  {
    slug: "questionnaire",
    name: "Questionnaire Auto-Fill",
    description: "Match security questionnaire questions to existing controls and policies, auto-generate answers with confidence scores.",
    icon: HelpCircle,
    category: "Compliance",
  },
  {
    slug: "monitoring-daemon",
    name: "Monitoring Daemon",
    description: "Run batch compliance monitoring checks and detect drift across all rules.",
    icon: Activity,
    category: "Operations",
  },
];

const categoryColors: Record<string, string> = {
  Compliance: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  Risk: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  Audit: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
  Vendor: "bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-100",
  Security: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  Operations: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export default function AgentsHubPage() {
  const orgId = useOrgId();
  const { data: runsData, isLoading } = useAgentRuns(orgId);
  const { data: budget } = useQuery({
    queryKey: ["ai-budget", orgId],
    queryFn: () => api.get<any>(`/organizations/${orgId}/agents/budget`),
    enabled: !!orgId,
  });

  // Count runs per agent type + review stats
  const runCounts: Record<string, number> = {};
  let pendingReview = 0;
  let approved = 0;
  let rejected = 0;
  if (runsData?.items) {
    for (const run of runsData.items as any[]) {
      const type = run.agent_type;
      runCounts[type] = (runCounts[type] || 0) + 1;
      if (run.approval_status === "pending_review") pendingReview++;
      else if (run.approval_status === "approved") approved++;
      else if (run.approval_status === "rejected") rejected++;
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">AI Agents</h1>
        <p className="text-muted-foreground">
          Launch AI-powered agents to automate GRC workflows
        </p>
      </div>

      {/* AI Budget + Review Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Budget Card */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-2">
              <Coins className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Monthly AI Budget</span>
            </div>
            {budget ? (
              <>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-bold">
                    {((budget.tokens_used || 0) / 1000).toFixed(0)}K
                  </span>
                  <span className="text-sm text-muted-foreground">
                    / {((budget.tokens_limit || 1000000) / 1000).toFixed(0)}K tokens
                  </span>
                </div>
                <Progress
                  value={budget.usage_percent || 0}
                  className={`mt-2 h-2 ${budget.usage_percent > 80 ? "[&>div]:bg-red-500" : ""}`}
                />
                <p className="text-xs text-muted-foreground mt-1">
                  ${(budget.cost_usd || 0).toFixed(2)} / ${(budget.cost_limit_usd || 50).toFixed(2)}
                </p>
              </>
            ) : (
              <Skeleton className="h-10 w-full" />
            )}
          </CardContent>
        </Card>

        {/* Pending Review */}
        <Link href="/agents/review-queue">
          <Card className="cursor-pointer hover:bg-muted/50 transition-colors">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="h-4 w-4 text-yellow-500" />
                <span className="text-sm font-medium">Pending Review</span>
              </div>
              <span className="text-2xl font-bold">{pendingReview}</span>
              <p className="text-xs text-muted-foreground mt-1">Click to review AI outputs</p>
            </CardContent>
          </Card>
        </Link>

        {/* Approved */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-sm font-medium">Approved</span>
            </div>
            <span className="text-2xl font-bold">{approved}</span>
            <p className="text-xs text-muted-foreground mt-1">Human-verified AI outputs</p>
          </CardContent>
        </Card>

        {/* Total Runs */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium">Total Runs</span>
            </div>
            <span className="text-2xl font-bold">{runsData?.total || 0}</span>
            <p className="text-xs text-muted-foreground mt-1">
              {rejected > 0 && <span className="text-red-500">{rejected} rejected</span>}
            </p>
          </CardContent>
        </Card>
      </div>

      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-48 w-full rounded-xl" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {agents.map((agent) => {
            const agentType = agent.slug.replace(/-/g, "_");
            const count = runCounts[agentType] || 0;
            return (
              <Link key={agent.slug} href={`/agents/${agent.slug}`}>
                <Card className="h-full transition-colors hover:bg-muted/50 cursor-pointer">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <agent.icon className="h-8 w-8 text-primary" />
                      <Badge className={categoryColors[agent.category] || ""}>
                        {agent.category}
                      </Badge>
                    </div>
                    <CardTitle className="mt-2">{agent.name}</CardTitle>
                    <CardDescription>{agent.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">
                        {count} run{count !== 1 ? "s" : ""}
                      </span>
                      <Button size="sm" variant="outline">
                        Launch
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
