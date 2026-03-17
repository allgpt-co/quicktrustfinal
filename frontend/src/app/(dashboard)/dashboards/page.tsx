"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import {
  Crown,
  Shield,
  ShieldCheck,
  ClipboardCheck,
  UserCog,
} from "lucide-react";

const dashboards = [
  {
    href: "/dashboards/executive",
    title: "Executive Dashboard",
    description: "High-level compliance scores, risk heatmap, and key metrics for board presentations.",
    icon: Crown,
    color: "text-amber-500",
    bg: "bg-amber-500/10",
  },
  {
    href: "/dashboards/compliance",
    title: "Compliance Manager",
    description: "Framework progress, evidence gaps, policy status, and acknowledgment tracking.",
    icon: Shield,
    color: "text-blue-500",
    bg: "bg-blue-500/10",
  },
  {
    href: "/dashboards/security",
    title: "Security Posture",
    description: "Scanner results, vulnerability trends, and monitoring alerts overview.",
    icon: ShieldCheck,
    color: "text-green-500",
    bg: "bg-green-500/10",
  },
  {
    href: "/dashboards/audit-readiness",
    title: "Audit Readiness",
    description: "Weighted readiness score: controls, evidence, policies, and risks.",
    icon: ClipboardCheck,
    color: "text-purple-500",
    bg: "bg-purple-500/10",
  },
  {
    href: "/dashboards/control-owner",
    title: "My Controls",
    description: "Controls assigned to you, evidence status, and overdue items.",
    icon: UserCog,
    color: "text-teal-500",
    bg: "bg-teal-500/10",
  },
];

export default function DashboardsHubPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboards</h1>
        <p className="text-muted-foreground">
          Role-based views of your compliance, security, and audit posture
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {dashboards.map((d) => (
          <Link key={d.href} href={d.href}>
            <Card className="transition-all hover:shadow-md hover:border-primary/30 cursor-pointer h-full">
              <CardHeader className="flex flex-row items-start gap-4">
                <div className={`rounded-lg p-2 ${d.bg}`}>
                  <d.icon className={`h-6 w-6 ${d.color}`} />
                </div>
                <div className="space-y-1">
                  <CardTitle className="text-lg">{d.title}</CardTitle>
                  <CardDescription>{d.description}</CardDescription>
                </div>
              </CardHeader>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
