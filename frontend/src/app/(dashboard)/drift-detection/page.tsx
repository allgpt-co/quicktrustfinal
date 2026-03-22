"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useDriftEvents,
  useDriftSummary,
  useAcknowledgeDriftEvent,
  useResolveDriftEvent,
} from "@/hooks/use-api";
import {
  GitCompareArrows,
  Eye,
  CheckCircle,
  AlertTriangle,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

const severityColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

const SEVERITY_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
];

const ACK_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Open", value: "false" },
  { label: "Acknowledged", value: "true" },
];

export default function DriftDetectionPage() {
  const orgId = useOrgId();
  const [severityFilter, setSeverityFilter] = useState<string | undefined>(undefined);
  const [ackFilter, setAckFilter] = useState<string | undefined>(undefined);

  const { data: eventsData, isLoading: eventsLoading } = useDriftEvents(orgId, {
    severity: severityFilter,
    acknowledged: ackFilter,
  });
  const { data: summary } = useDriftSummary(orgId);
  const acknowledgeDrift = useAcknowledgeDriftEvent(orgId);
  const resolveDrift = useResolveDriftEvent(orgId);

  const events = eventsData?.items || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Drift Detection</h1>
        <p className="text-muted-foreground">
          Monitor configuration changes and detect unauthorized drift from baselines
        </p>
      </div>

      {/* Summary Stats */}
      {summary && (
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "Total Events", value: summary.total_events ?? 0 },
            { label: "Open Events", value: summary.open_events ?? 0 },
            { label: "Critical/High Open", value: summary.critical_high_open ?? 0 },
          ].map((s) => (
            <Card key={s.label}>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{s.value}</div>
                <div className="text-xs text-muted-foreground">{s.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <span className="flex items-center text-sm text-muted-foreground mr-1">Severity:</span>
          {SEVERITY_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={severityFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => setSeverityFilter(f.value)}
            >
              {f.label}
            </Button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="flex items-center text-sm text-muted-foreground mr-1">Status:</span>
          {ACK_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={ackFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => setAckFilter(f.value)}
            >
              {f.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Events */}
      {eventsLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : events.length > 0 ? (
        <div className="space-y-3">
          {events.map((event: any) => (
            <Card key={event.id}>
              <CardContent className="flex items-center gap-4 p-4">
                <GitCompareArrows className="h-8 w-8 text-muted-foreground shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium">
                    {event.drift_type} drift{event.field_path ? ` on ${event.field_path}` : ""}
                  </div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    {event.old_value && <>Old: {event.old_value}</>}
                    {event.new_value && <> &rarr; New: {event.new_value}</>}
                    {event.detected_at && (
                      <> &middot; {new Date(event.detected_at).toLocaleString()}</>
                    )}
                  </div>
                </div>
                <Badge className={severityColor[event.severity] || ""}>
                  {event.severity}
                </Badge>
                <Badge variant={event.acknowledged ? "secondary" : "destructive"}>
                  {event.acknowledged ? "Acknowledged" : "Open"}
                </Badge>
                {!event.acknowledged && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="gap-1"
                    onClick={() => acknowledgeDrift.mutate(event.id)}
                    disabled={acknowledgeDrift.isPending}
                  >
                    <Eye className="h-3 w-3" />
                    Acknowledge
                  </Button>
                )}
                <Button
                  size="sm"
                  variant="outline"
                  className="gap-1"
                  onClick={() => resolveDrift.mutate(event.id)}
                  disabled={resolveDrift.isPending}
                >
                  <CheckCircle className="h-3 w-3" />
                  Resolve
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertTriangle className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No drift events</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No configuration drift has been detected. Baselines are being monitored.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
