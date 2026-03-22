"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuditLogs, useAuditLogStats } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  History,
  Filter,
  Shield,
  Database,
  Users,
  Bot,
  Settings,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Info,
} from "lucide-react";

// ---------------------------------------------------------------------------
// Color maps
// ---------------------------------------------------------------------------

const actionColors: Record<string, string> = {
  create: "bg-green-500/20 text-green-400 border-green-500/30",
  update: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  delete: "bg-red-500/20 text-red-400 border-red-500/30",
  approve: "bg-purple-500/20 text-purple-400 border-purple-500/30",
  publish: "bg-indigo-500/20 text-indigo-400 border-indigo-500/30",
  login: "bg-teal-500/20 text-teal-400 border-teal-500/30",
  auth_login: "bg-teal-500/20 text-teal-400 border-teal-500/30",
  auth_logout: "bg-gray-500/20 text-gray-400 border-gray-500/30",
  auth_failed: "bg-red-500/20 text-red-400 border-red-500/30",
  suspend: "bg-orange-500/20 text-orange-400 border-orange-500/30",
  reactivate: "bg-green-500/20 text-green-400 border-green-500/30",
};

const severityConfig: Record<string, { color: string; icon: typeof Info }> = {
  DEBUG: { color: "text-gray-400", icon: Info },
  INFO: { color: "text-blue-400", icon: Info },
  WARN: { color: "text-yellow-400", icon: AlertTriangle },
  ERROR: { color: "text-red-400", icon: XCircle },
  CRITICAL: { color: "text-red-500", icon: XCircle },
};

const categoryIcons: Record<string, typeof Shield> = {
  authentication: Shield,
  authorization: Shield,
  data: Database,
  admin: Settings,
  system: Settings,
  ai: Bot,
};

const outcomeConfig: Record<string, { color: string; icon: typeof CheckCircle }> = {
  success: { color: "text-green-400", icon: CheckCircle },
  failure: { color: "text-red-400", icon: XCircle },
  denied: { color: "text-orange-400", icon: XCircle },
};

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function AuditLogPage() {
  const orgId = useOrgId();
  const [entityFilter, setEntityFilter] = useState<string | undefined>();
  const [actionFilter, setActionFilter] = useState<string | undefined>();
  const [categoryFilter, setCategoryFilter] = useState<string | undefined>();
  const { data: logs, isLoading } = useAuditLogs(orgId, {
    entity_type: entityFilter,
    action: actionFilter,
  });
  const { data: stats } = useAuditLogStats(orgId);

  const entityTypes = stats?.by_entity_type
    ? Object.keys(stats.by_entity_type)
    : [];
  const actions = stats?.by_action ? Object.keys(stats.by_action) : [];
  const categories = stats?.by_category
    ? Object.keys(stats.by_category)
    : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Security Audit Log</h1>
        <p className="text-muted-foreground">
          Comprehensive audit trail of all actions across your organization
        </p>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold">{stats.total}</div>
              <p className="text-xs text-muted-foreground">Total Events</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold">
                {Object.keys(stats.by_category || {}).length}
              </div>
              <p className="text-xs text-muted-foreground">Categories</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-yellow-400">
                {(stats.by_severity || {})["WARN"] || 0}
              </div>
              <p className="text-xs text-muted-foreground">Warnings</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-red-400">
                {((stats.by_severity || {})["ERROR"] || 0) +
                  ((stats.by_severity || {})["CRITICAL"] || 0)}
              </div>
              <p className="text-xs text-muted-foreground">Errors</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Category filter */}
      <div className="space-y-2">
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs font-medium text-muted-foreground w-16">Category</span>
          <Button
            size="sm"
            variant={!categoryFilter ? "default" : "outline"}
            onClick={() => setCategoryFilter(undefined)}
          >
            All
          </Button>
          {categories.map((c) => {
            const Icon = categoryIcons[c] || Settings;
            return (
              <Button
                key={c}
                size="sm"
                variant={categoryFilter === c ? "default" : "outline"}
                onClick={() => setCategoryFilter(c)}
              >
                <Icon className="mr-1 h-3 w-3" />
                {c}
              </Button>
            );
          })}
        </div>

        {/* Entity filter */}
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs font-medium text-muted-foreground w-16">Entity</span>
          <Button
            size="sm"
            variant={!entityFilter ? "default" : "outline"}
            onClick={() => setEntityFilter(undefined)}
          >
            All
          </Button>
          {entityTypes.map((et) => (
            <Button
              key={et}
              size="sm"
              variant={entityFilter === et ? "default" : "outline"}
              onClick={() => setEntityFilter(et)}
            >
              {et}
            </Button>
          ))}
        </div>

        {/* Action filter */}
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs font-medium text-muted-foreground w-16">Action</span>
          <Button
            size="sm"
            variant={!actionFilter ? "default" : "outline"}
            onClick={() => setActionFilter(undefined)}
          >
            All
          </Button>
          {actions.map((a) => (
            <Button
              key={a}
              size="sm"
              variant={actionFilter === a ? "default" : "outline"}
              onClick={() => setActionFilter(a)}
            >
              {a}
            </Button>
          ))}
        </div>
      </div>

      {/* Log entries */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </div>
      ) : logs?.items?.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12">
            <History className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No audit log entries found</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-2">
          {logs?.items?.map((log: any) => {
            const sevConfig = severityConfig[log.severity] || severityConfig.INFO;
            const SevIcon = sevConfig.icon;
            const outConfig = outcomeConfig[log.outcome] || outcomeConfig.success;
            const OutIcon = outConfig.icon;
            const CatIcon = categoryIcons[log.event_category] || Settings;

            return (
              <Card key={log.id} className="hover:border-primary/30 transition-colors">
                <CardContent className="flex items-start gap-4 p-4">
                  {/* Severity icon */}
                  <div className="pt-0.5">
                    <SevIcon className={`h-5 w-5 ${sevConfig.color}`} />
                  </div>

                  {/* Main content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <Badge
                        className={
                          actionColors[log.action] || "bg-gray-500/20 text-gray-400"
                        }
                      >
                        {log.action}
                      </Badge>
                      <Badge variant="outline">{log.entity_type}</Badge>
                      {log.event_category && (
                        <span className="flex items-center gap-1 text-xs text-muted-foreground">
                          <CatIcon className="h-3 w-3" />
                          {log.event_category}
                        </span>
                      )}
                      <span className="flex items-center gap-1 text-xs">
                        <OutIcon className={`h-3 w-3 ${outConfig.color}`} />
                        <span className={outConfig.color}>{log.outcome || "success"}</span>
                      </span>
                    </div>

                    <p className="text-sm mt-1 truncate">
                      {log.entity_id}
                    </p>

                    <div className="flex items-center gap-4 text-xs text-muted-foreground mt-1">
                      <span>
                        {log.actor_email || log.actor_id}{" "}
                        {log.actor_role && (
                          <span className="opacity-60">({log.actor_role})</span>
                        )}
                      </span>
                      {log.actor_ip && <span>IP: {log.actor_ip}</span>}
                      {log.request_id && (
                        <span className="font-mono text-[10px] opacity-50">
                          req:{log.request_id.slice(0, 8)}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Timestamp */}
                  <div className="text-xs text-muted-foreground text-right whitespace-nowrap">
                    {new Date(log.timestamp).toLocaleString()}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
