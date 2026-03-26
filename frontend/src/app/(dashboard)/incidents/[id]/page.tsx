"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  useIncident,
  useUpdateIncident,
  useDeleteIncident,
  useAddTimelineEvent,
  useIncidentTimeline,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  Pencil,
  Trash2,
  Loader2,
  Save,
  X,
  Clock,
  Plus,
  AlertTriangle,
  Bell,
  CheckSquare,
  Square,
  ShieldAlert,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";
import { toast } from "sonner";
import type { IncidentSeverity, IncidentStatus } from "@/lib/types";

const severityColor: Record<string, string> = {
  P1: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  P2: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  P3: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  P4: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

const statusColor: Record<string, string> = {
  open: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  investigating:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  resolved:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  closed: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

const eventTypeColor: Record<string, string> = {
  note: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  status_change:
    "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
  escalation:
    "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  resolution:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export default function IncidentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const orgId = useOrgId();
  const incidentId = params.id as string;

  const { data: incident, isLoading } = useIncident(orgId, incidentId);
  const { data: timeline, isLoading: timelineLoading } = useIncidentTimeline(
    orgId,
    incidentId
  );
  const updateIncident = useUpdateIncident(orgId);
  const deleteIncident = useDeleteIncident(orgId);
  const addTimelineEvent = useAddTimelineEvent(orgId, incidentId);

  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    severity: "P3",
    status: "open",
    category: "",
    post_mortem_notes: "",
    breach_notification_required: false,
    affected_users_count: 0,
    affected_systems: [] as string[],
  });

  const [noteText, setNoteText] = useState("");
  const [showAddNote, setShowAddNote] = useState(false);

  function enterEditMode() {
    if (!incident) return;
    setForm({
      title: incident.title || "",
      description: incident.description || "",
      severity: incident.severity || "P3",
      status: incident.status || "open",
      category: incident.category || "",
      post_mortem_notes: incident.post_mortem_notes || "",
      breach_notification_required: incident.breach_notification_required || false,
      affected_users_count: incident.affected_users_count || 0,
      affected_systems: incident.affected_systems || [],
    });
    setEditing(true);
  }

  function handleSave() {
    if (!incident) return;
    updateIncident.mutate(
      { incidentId: incident.id, ...form, severity: form.severity as IncidentSeverity, status: form.status as IncidentStatus },
      { onSuccess: () => setEditing(false) }
    );
  }

  function handleDelete() {
    if (!incident) return;
    const confirmed = window.confirm(
      `Are you sure you want to delete "${incident.title}"? This action cannot be undone.`
    );
    if (!confirmed) return;
    deleteIncident.mutate(incident.id, {
      onSuccess: () => router.push("/incidents"),
    });
  }

  function handleAddNote() {
    if (!noteText.trim()) return;
    addTimelineEvent.mutate(
      { event_type: "note", description: noteText.trim() },
      {
        onSuccess: () => {
          setNoteText("");
          setShowAddNote(false);
        },
      }
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!incident) return <p>Incident not found.</p>;

  return (
    <div className="space-y-6">
      <Link
        href="/incidents"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Incidents
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{incident.title}</h1>
        <Badge className={severityColor[incident.severity] || ""}>
          {incident.severity}
        </Badge>
        <Badge className={statusColor[incident.status] || ""}>
          {incident.status}
        </Badge>
        <div className="ml-auto flex items-center gap-2">
          {!editing && (
            <Button variant="outline" size="sm" onClick={enterEditMode}>
              <Pencil className="mr-1 h-4 w-4" />
              Edit
            </Button>
          )}
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDelete}
            disabled={deleteIncident.isPending}
          >
            {deleteIncident.isPending ? (
              <Loader2 className="mr-1 h-4 w-4 animate-spin" />
            ) : (
              <Trash2 className="mr-1 h-4 w-4" />
            )}
            Delete
          </Button>
        </div>
      </div>

      <p className="text-sm text-muted-foreground">
        {incident.category && (
          <span className="capitalize">{incident.category} &middot; </span>
        )}
        Created {new Date(incident.created_at).toLocaleDateString()}
      </p>

      {/* Edit Form */}
      {editing && (
        <Card>
          <CardHeader>
            <CardTitle>Edit Incident</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>

            <div>
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                rows={4}
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-medium">Severity</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.severity}
                  onChange={(e) =>
                    setForm({ ...form, severity: e.target.value })
                  }
                >
                  <option value="P1">P1 - Critical</option>
                  <option value="P2">P2 - High</option>
                  <option value="P3">P3 - Medium</option>
                  <option value="P4">P4 - Low</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">Status</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.status}
                  onChange={(e) =>
                    setForm({ ...form, status: e.target.value })
                  }
                >
                  <option value="open">Open</option>
                  <option value="investigating">Investigating</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">Category</label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium">Post-Mortem Notes</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                rows={4}
                placeholder="Post-mortem analysis and lessons learned..."
                value={form.post_mortem_notes}
                onChange={(e) =>
                  setForm({ ...form, post_mortem_notes: e.target.value })
                }
              />
            </div>

            {/* Breach Notification Settings */}
            <div className="rounded-md border p-4 space-y-3">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="breach_required"
                  className="h-4 w-4 rounded"
                  checked={form.breach_notification_required}
                  onChange={(e) => setForm({ ...form, breach_notification_required: e.target.checked })}
                />
                <label htmlFor="breach_required" className="text-sm font-medium">
                  Breach Notification Required (GDPR 72h)
                </label>
              </div>
              {form.breach_notification_required && (
                <div className="grid grid-cols-2 gap-3 pl-6">
                  <div>
                    <label className="text-sm font-medium">Affected Users Count</label>
                    <input
                      type="number"
                      className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                      value={form.affected_users_count}
                      onChange={(e) => setForm({ ...form, affected_users_count: parseInt(e.target.value) || 0 })}
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">Affected Systems (comma-separated)</label>
                    <input
                      type="text"
                      className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="Database, S3, Auth Service"
                      value={(form.affected_systems || []).join(", ")}
                      onChange={(e) => setForm({ ...form, affected_systems: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                    />
                  </div>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateIncident.isPending}
              >
                {updateIncident.isPending ? (
                  <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                ) : (
                  <Save className="mr-1 h-4 w-4" />
                )}
                Save
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setEditing(false)}
                disabled={updateIncident.isPending}
              >
                <X className="mr-1 h-4 w-4" />
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tabs */}
      {!editing && (
        <Tabs defaultValue="overview">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="breach">
              Breach Notification
              {incident.breach_notification_required && (
                <AlertTriangle className="ml-1 h-3.5 w-3.5 text-red-500" />
              )}
            </TabsTrigger>
            <TabsTrigger value="timeline">Timeline</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview">
            <div className="space-y-4">
              {/* Description */}
              {incident.description && (
                <Card>
                  <CardHeader>
                    <CardTitle>Description</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="whitespace-pre-wrap">{incident.description}</p>
                  </CardContent>
                </Card>
              )}

              {/* Response Timeline Markers */}
              {(incident.detected_at || incident.contained_at || incident.resolved_at) && (
                <Card>
                  <CardHeader>
                    <CardTitle>Response Timeline</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center gap-2 flex-wrap">
                      {incident.detected_at && (
                        <div className="rounded-lg border px-3 py-2 text-center">
                          <p className="text-xs text-muted-foreground">Detected</p>
                          <p className="text-sm font-medium">{new Date(incident.detected_at).toLocaleString()}</p>
                        </div>
                      )}
                      {incident.detected_at && <span className="text-muted-foreground">&rarr;</span>}
                      {incident.contained_at && (
                        <div className="rounded-lg border px-3 py-2 text-center">
                          <p className="text-xs text-muted-foreground">Contained</p>
                          <p className="text-sm font-medium">{new Date(incident.contained_at).toLocaleString()}</p>
                        </div>
                      )}
                      {incident.contained_at && <span className="text-muted-foreground">&rarr;</span>}
                      {incident.resolved_at && (
                        <div className="rounded-lg border px-3 py-2 text-center">
                          <p className="text-xs text-muted-foreground">Resolved</p>
                          <p className="text-sm font-medium">{new Date(incident.resolved_at).toLocaleString()}</p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Post-mortem */}
              {incident.post_mortem_notes && (
                <Card>
                  <CardHeader>
                    <CardTitle>Post-Mortem Notes</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="whitespace-pre-wrap">{incident.post_mortem_notes}</p>
                  </CardContent>
                </Card>
              )}

              {/* Root Cause & Lessons Learned */}
              {(incident.root_cause || incident.lessons_learned) && (
                <div className="grid gap-4 md:grid-cols-2">
                  {incident.root_cause && (
                    <Card>
                      <CardHeader><CardTitle>Root Cause</CardTitle></CardHeader>
                      <CardContent><p className="whitespace-pre-wrap text-sm">{incident.root_cause}</p></CardContent>
                    </Card>
                  )}
                  {incident.lessons_learned && (
                    <Card>
                      <CardHeader><CardTitle>Lessons Learned</CardTitle></CardHeader>
                      <CardContent><p className="whitespace-pre-wrap text-sm">{incident.lessons_learned}</p></CardContent>
                    </Card>
                  )}
                </div>
              )}
            </div>
          </TabsContent>

          {/* Breach Notification Tab */}
          <TabsContent value="breach">
            <BreachNotificationTab
              incident={incident}
              orgId={orgId}
              updateIncident={updateIncident}
            />
          </TabsContent>

          {/* Timeline Tab */}
          <TabsContent value="timeline">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Timeline</CardTitle>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setShowAddNote((v) => !v)}
                  >
                    <Plus className="mr-1 h-4 w-4" />
                    Add Note
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {showAddNote && (
                  <div className="space-y-3 rounded-lg border p-4">
                    <textarea
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      rows={3}
                      placeholder="Add a timeline note..."
                      value={noteText}
                      onChange={(e) => setNoteText(e.target.value)}
                    />
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        onClick={handleAddNote}
                        disabled={!noteText.trim() || addTimelineEvent.isPending}
                      >
                        {addTimelineEvent.isPending && (
                          <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                        )}
                        Add Note
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => {
                          setShowAddNote(false);
                          setNoteText("");
                        }}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                )}

                {timelineLoading ? (
                  <div className="space-y-3">
                    {[1, 2, 3].map((i) => (
                      <Skeleton key={i} className="h-16 w-full rounded-lg" />
                    ))}
                  </div>
                ) : timeline && timeline.length > 0 ? (
                  <div className="space-y-3">
                    {timeline.map((event: any) => (
                      <div
                        key={event.id}
                        className="flex items-start gap-3 rounded-lg border p-3"
                      >
                        <Clock className="mt-0.5 h-4 w-4 text-muted-foreground shrink-0" />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <Badge
                              className={
                                eventTypeColor[event.event_type] ||
                                "bg-gray-100 text-gray-800"
                              }
                            >
                              {event.event_type?.replace(/_/g, " ")}
                            </Badge>
                            <span className="text-xs text-muted-foreground">
                              {event.created_at &&
                                new Date(event.created_at).toLocaleString()}
                            </span>
                          </div>
                          <p className="mt-1 text-sm">{event.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center py-6 text-center">
                    <Clock className="h-10 w-10 text-muted-foreground mb-3" />
                    <p className="text-sm text-muted-foreground">
                      No timeline events yet.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}

// =====================================================================
// Breach Notification Tab Component
// =====================================================================

function BreachNotificationTab({
  incident,
  orgId,
  updateIncident,
}: {
  incident: any;
  orgId: string;
  updateIncident: any;
}) {
  const [countdown, setCountdown] = useState("");
  const [countdownColor, setCountdownColor] = useState("text-green-600");

  // Checklist state (static for demo)
  const [checklist, setChecklist] = useState({
    notify_dpa: incident.breach_notification_checklist?.notify_dpa || false,
    notify_affected_users:
      incident.breach_notification_checklist?.notify_affected_users || false,
    notify_business_partners:
      incident.breach_notification_checklist?.notify_business_partners || false,
    document_notification_details:
      incident.breach_notification_checklist?.document_notification_details ||
      false,
  });

  // Live countdown timer
  useEffect(() => {
    if (
      !incident.breach_notification_required ||
      !incident.breach_notification_deadline ||
      incident.breach_notified_at
    ) {
      return;
    }

    function updateCountdown() {
      const deadline = new Date(incident.breach_notification_deadline).getTime();
      const now = Date.now();
      const diff = deadline - now;

      if (diff <= 0) {
        setCountdown("OVERDUE");
        setCountdownColor("text-red-600");
        return;
      }

      const hours = Math.floor(diff / 3600000);
      const minutes = Math.floor((diff % 3600000) / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);

      setCountdown(
        `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`
      );

      // Color based on remaining time
      if (hours < 24) {
        setCountdownColor("text-yellow-600");
      } else {
        setCountdownColor("text-green-600");
      }
    }

    updateCountdown();
    const interval = setInterval(updateCountdown, 1000);
    return () => clearInterval(interval);
  }, [
    incident.breach_notification_required,
    incident.breach_notification_deadline,
    incident.breach_notified_at,
  ]);

  function handleMarkNotified() {
    updateIncident.mutate(
      {
        incidentId: incident.id,
        breach_notified_at: new Date().toISOString(),
      },
      {
        onSuccess: () => toast.success("Incident marked as notified"),
        onError: (e: any) => toast.error(e.message),
      }
    );
  }

  if (!incident.breach_notification_required) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center justify-center p-12 text-center">
          <ShieldAlert className="h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-medium">No breach notification required</h3>
          <p className="text-sm text-muted-foreground mt-1">
            No breach notification required for this incident.
          </p>
        </CardContent>
      </Card>
    );
  }

  const isNotified = !!incident.breach_notified_at;

  return (
    <div className="space-y-4">
      {/* Countdown Timer */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-red-500" />
            Breach Notification Deadline
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isNotified ? (
            <div className="flex items-center gap-3 rounded-lg border border-green-500/30 bg-green-500/5 p-4">
              <Bell className="h-8 w-8 text-green-500" />
              <div>
                <p className="text-sm font-medium text-green-700 dark:text-green-400">
                  Notification Sent
                </p>
                <p className="text-xs text-muted-foreground">
                  Notified at: {new Date(incident.breach_notified_at).toLocaleString()}
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center gap-4 rounded-lg border border-red-500/30 bg-red-500/5 p-6">
                <Clock className="h-10 w-10 text-red-500 shrink-0" />
                <div>
                  <p className="text-xs font-medium text-muted-foreground">
                    Time Remaining (GDPR 72h)
                  </p>
                  <p className={`text-4xl font-mono font-bold ${countdownColor}`}>
                    {countdown || "Calculating..."}
                  </p>
                  {incident.breach_notification_deadline && (
                    <p className="text-xs text-muted-foreground mt-1">
                      Deadline: {new Date(incident.breach_notification_deadline).toLocaleString()}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Impact Details */}
      <Card>
        <CardHeader>
          <CardTitle>Impact Assessment</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border p-4">
              <label className="text-xs font-medium text-muted-foreground">
                Affected Users
              </label>
              <p className="text-2xl font-bold mt-1">
                {incident.affected_users_count != null
                  ? incident.affected_users_count.toLocaleString()
                  : "Unknown"}
              </p>
            </div>
            <div className="rounded-lg border p-4">
              <label className="text-xs font-medium text-muted-foreground">
                Affected Systems
              </label>
              <div className="mt-1">
                {incident.affected_systems &&
                incident.affected_systems.length > 0 ? (
                  <div className="flex flex-wrap gap-1">
                    {incident.affected_systems.map((system: string) => (
                      <Badge key={system} variant="outline">
                        {system}
                      </Badge>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">Not specified</p>
                )}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notification Checklist */}
      <Card>
        <CardHeader>
          <CardTitle>Notification Checklist</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {[
            { key: "notify_dpa", label: "Notify Data Protection Authority" },
            {
              key: "notify_affected_users",
              label: "Notify Affected Users",
            },
            {
              key: "notify_business_partners",
              label: "Notify Business Partners",
            },
            {
              key: "document_notification_details",
              label: "Document Notification Details",
            },
          ].map((item) => (
            <button
              key={item.key}
              className="flex w-full items-center gap-3 rounded-lg border p-3 text-left hover:bg-muted/50 transition-colors"
              onClick={() =>
                setChecklist((prev) => ({
                  ...prev,
                  [item.key]: !prev[item.key as keyof typeof prev],
                }))
              }
            >
              {checklist[item.key as keyof typeof checklist] ? (
                <CheckSquare className="h-5 w-5 text-green-500 shrink-0" />
              ) : (
                <Square className="h-5 w-5 text-muted-foreground shrink-0" />
              )}
              <span className="text-sm font-medium">{item.label}</span>
            </button>
          ))}
        </CardContent>
      </Card>

      {/* Mark as Notified */}
      {!isNotified && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Mark Breach as Notified</p>
                <p className="text-sm text-muted-foreground">
                  Record that all required breach notifications have been sent.
                </p>
              </div>
              <Button
                onClick={handleMarkNotified}
                disabled={updateIncident.isPending}
              >
                {updateIncident.isPending ? (
                  <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                ) : (
                  <Bell className="mr-1 h-4 w-4" />
                )}
                Mark as Notified
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
