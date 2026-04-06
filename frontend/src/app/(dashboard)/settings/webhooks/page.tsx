"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { useOrgId } from "@/hooks/use-org-id";
import { toast } from "sonner";
import {
  ArrowLeft,
  Globe,
  Plus,
  Trash2,
  Loader2,
  Send,
  CheckCircle,
  XCircle,
} from "lucide-react";

interface WebhookDelivery {
  id: string;
  status_code: number;
  success: boolean;
  delivered_at: string;
}

interface Webhook {
  id: string;
  url: string;
  events: string[];
  is_active: boolean;
  failure_count: number;
  recent_deliveries?: WebhookDelivery[];
}

const AVAILABLE_EVENTS = [
  "incident.created",
  "control.status_changed",
  "scan.completed",
  "compliance.regression",
  "policy.published",
] as const;

export default function WebhooksPage() {
  const orgId = useOrgId();
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [url, setUrl] = useState("");
  const [secret, setSecret] = useState("");
  const [selectedEvents, setSelectedEvents] = useState<string[]>([]);

  const { data: webhooks, isLoading } = useQuery({
    queryKey: ["webhooks", orgId],
    queryFn: () => api.get<Webhook[]>(`/organizations/${orgId}/webhooks`),
    enabled: !!orgId,
  });

  const createWebhook = useMutation({
    mutationFn: () =>
      api.post(`/organizations/${orgId}/webhooks`, {
        url,
        secret,
        events: selectedEvents,
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["webhooks", orgId] });
      toast.success("Webhook created successfully");
      setUrl("");
      setSecret("");
      setSelectedEvents([]);
      setShowForm(false);
    },
    onError: (err: any) => toast.error(err.message || "Failed to create webhook"),
  });

  const testWebhook = useMutation({
    mutationFn: (webhookId: string) =>
      api.post(`/organizations/${orgId}/webhooks/${webhookId}/test`, {}),
    onSuccess: () => toast.success("Test event sent successfully"),
    onError: (err: any) => toast.error(err.message || "Test failed"),
  });

  const deleteWebhook = useMutation({
    mutationFn: (webhookId: string) =>
      api.delete(`/organizations/${orgId}/webhooks/${webhookId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["webhooks", orgId] });
      toast.success("Webhook deleted");
    },
    onError: (err: any) => toast.error(err.message || "Failed to delete webhook"),
  });

  function toggleEvent(event: string) {
    setSelectedEvents((prev) =>
      prev.includes(event)
        ? prev.filter((e) => e !== event)
        : [...prev, event]
    );
  }

  function truncateUrl(rawUrl: string, maxLength: number = 50): string {
    if (rawUrl.length <= maxLength) return rawUrl;
    return rawUrl.slice(0, maxLength) + "...";
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Link
          href="/settings"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Settings
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Webhooks</h1>
            <p className="text-muted-foreground">
              Configure outbound event webhooks
            </p>
          </div>
          <Button onClick={() => setShowForm((prev) => !prev)}>
            <Plus className="mr-2 h-4 w-4" />
            Add Webhook
          </Button>
        </div>
      </div>

      {/* Create Form */}
      {showForm && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5" />
              New Webhook
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">URL</label>
              <input
                type="url"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="https://example.com/webhook"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Secret</label>
              <input
                type="password"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Signing secret for payload verification"
                value={secret}
                onChange={(e) => setSecret(e.target.value)}
              />
              <p className="mt-1 text-xs text-muted-foreground">
                Used to sign webhook payloads so you can verify authenticity
              </p>
            </div>
            <div>
              <label className="text-sm font-medium">Events</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {AVAILABLE_EVENTS.map((event) => (
                  <label
                    key={event}
                    className="flex items-center gap-2 rounded-md border px-3 py-2 text-sm cursor-pointer hover:bg-muted/50"
                  >
                    <input
                      type="checkbox"
                      checked={selectedEvents.includes(event)}
                      onChange={() => toggleEvent(event)}
                      className="rounded"
                    />
                    {event}
                  </label>
                ))}
              </div>
            </div>
            <div className="flex gap-2 pt-2">
              <Button
                onClick={() => createWebhook.mutate()}
                disabled={
                  !url.trim() ||
                  selectedEvents.length === 0 ||
                  createWebhook.isPending
                }
              >
                {createWebhook.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Plus className="mr-2 h-4 w-4" />
                )}
                Create
              </Button>
              <Button variant="ghost" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Webhook List */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-32 w-full rounded-xl" />
          ))}
        </div>
      ) : webhooks && webhooks.length > 0 ? (
        <div className="space-y-4">
          {webhooks.map((webhook) => (
            <Card key={webhook.id}>
              <CardContent className="p-6 space-y-4">
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Globe className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm font-mono font-medium">
                        {truncateUrl(webhook.url)}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {webhook.events.map((event) => (
                        <Badge key={event} variant="secondary" className="text-xs">
                          {event}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {webhook.is_active ? (
                      <Badge className="bg-green-500/20 text-green-500">
                        Active
                      </Badge>
                    ) : (
                      <Badge className="bg-gray-500/20 text-gray-500">
                        Inactive
                      </Badge>
                    )}
                    {webhook.failure_count > 0 && (
                      <Badge className="bg-red-500/20 text-red-500">
                        {webhook.failure_count} failures
                      </Badge>
                    )}
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => testWebhook.mutate(webhook.id)}
                    disabled={testWebhook.isPending}
                  >
                    {testWebhook.isPending ? (
                      <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="mr-1 h-4 w-4" />
                    )}
                    Test
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="text-destructive"
                    onClick={() => deleteWebhook.mutate(webhook.id)}
                    disabled={deleteWebhook.isPending}
                  >
                    {deleteWebhook.isPending ? (
                      <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                    ) : (
                      <Trash2 className="mr-1 h-4 w-4" />
                    )}
                    Delete
                  </Button>
                </div>

                {/* Recent Deliveries */}
                {webhook.recent_deliveries &&
                  webhook.recent_deliveries.length > 0 && (
                    <div className="border-t pt-3">
                      <p className="text-xs font-medium text-muted-foreground mb-2">
                        Recent Deliveries
                      </p>
                      <div className="space-y-1">
                        {webhook.recent_deliveries.map((delivery) => (
                          <div
                            key={delivery.id}
                            className="flex items-center gap-3 text-xs"
                          >
                            {delivery.success ? (
                              <CheckCircle className="h-3 w-3 text-green-500" />
                            ) : (
                              <XCircle className="h-3 w-3 text-red-500" />
                            )}
                            <span className="font-mono">
                              {delivery.status_code}
                            </span>
                            <span className="text-muted-foreground">
                              {new Date(delivery.delivered_at).toLocaleString()}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <Globe className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No webhooks configured</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Add a webhook to receive real-time event notifications via HTTP POST.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
