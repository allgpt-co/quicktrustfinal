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
  Bell,
  MessageSquare,
  Mail,
  Send,
  Trash2,
  Loader2,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Play,
} from "lucide-react";

export default function AlertChannelsPage() {
  const orgId = useOrgId();
  const qc = useQueryClient();
  const [webhookUrl, setWebhookUrl] = useState("");
  const [channelName, setChannelName] = useState("");

  // Fetch existing Slack config
  const { data: slackConfig, isLoading: slackLoading } = useQuery({
    queryKey: ["slack-config", orgId],
    queryFn: () => api.get<any>(`/organizations/${orgId}/notifications/slack`),
    enabled: !!orgId,
  });

  // Save Slack webhook
  const saveSlack = useMutation({
    mutationFn: () =>
      api.post(`/organizations/${orgId}/notifications/slack`, {
        webhook_url: webhookUrl,
        channel_name: channelName || null,
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["slack-config"] });
      toast.success("Slack webhook saved!");
      setWebhookUrl("");
      setChannelName("");
    },
    onError: (err: any) => toast.error(err.message || "Failed to save"),
  });

  // Test Slack
  const testSlack = useMutation({
    mutationFn: () =>
      api.post(`/organizations/${orgId}/notifications/test-slack`, {}),
    onSuccess: () => toast.success("Test message sent to Slack!"),
    onError: (err: any) => toast.error(err.message || "Test failed"),
  });

  // Delete Slack
  const deleteSlack = useMutation({
    mutationFn: () =>
      api.delete(`/organizations/${orgId}/notifications/slack`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["slack-config"] });
      toast.success("Slack webhook disabled");
    },
    onError: (err: any) => toast.error(err.message || "Failed to delete"),
  });

  // Run alert engine manually
  const runAlerts = useMutation({
    mutationFn: () =>
      api.post(`/organizations/${orgId}/notifications/run-alerts`, {}),
    onSuccess: (data: any) => {
      toast.success(
        `Alert engine completed: ${data.freshness_alerts} freshness, ${data.regression_alerts} regression alerts`
      );
    },
    onError: (err: any) => toast.error(err.message || "Alert engine failed"),
  });

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
            <h1 className="text-3xl font-bold">Alert Channels</h1>
            <p className="text-muted-foreground">
              Configure how compliance alerts are delivered to your team
            </p>
          </div>
          <Button
            onClick={() => runAlerts.mutate()}
            disabled={runAlerts.isPending}
            variant="outline"
          >
            {runAlerts.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Play className="mr-2 h-4 w-4" />
            )}
            Run Alert Check Now
          </Button>
        </div>
      </div>

      {/* Alert Types Info */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Bell className="h-5 w-5 text-muted-foreground" />
            <CardTitle>What Gets Alerted</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 md:grid-cols-2">
            <div className="flex items-start gap-3 rounded-lg border p-3">
              <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
              <div>
                <p className="text-sm font-medium">Evidence Freshness</p>
                <p className="text-xs text-muted-foreground">
                  Alert when evidence items are older than 30 days. Checked every 6 hours.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-lg border p-3">
              <AlertTriangle className="h-5 w-5 text-red-500 mt-0.5" />
              <div>
                <p className="text-sm font-medium">Compliance Regression</p>
                <p className="text-xs text-muted-foreground">
                  Alert when compliance score drops more than 5%. Auto-creates incident if drop exceeds 10%.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-lg border p-3">
              <AlertTriangle className="h-5 w-5 text-orange-500 mt-0.5" />
              <div>
                <p className="text-sm font-medium">Scanner Findings</p>
                <p className="text-xs text-muted-foreground">
                  Auto-creates incidents from critical/high scanner findings.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-lg border p-3">
              <AlertTriangle className="h-5 w-5 text-blue-500 mt-0.5" />
              <div>
                <p className="text-sm font-medium">Monitoring Failures</p>
                <p className="text-xs text-muted-foreground">
                  Auto-creates incidents when monitoring rules fail.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Slack Channel */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-muted-foreground" />
              <CardTitle>Slack</CardTitle>
            </div>
            {slackConfig && slackConfig.is_active !== false ? (
              <Badge className="bg-green-500/20 text-green-500">Connected</Badge>
            ) : (
              <Badge className="bg-gray-500/20 text-gray-500">Not configured</Badge>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {slackLoading ? (
            <Skeleton className="h-20 w-full" />
          ) : slackConfig && slackConfig.is_active !== false ? (
            <div className="space-y-3">
              <div className="rounded-lg border bg-green-500/5 border-green-500/20 p-4">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  <span className="text-sm font-medium text-green-500">
                    Slack webhook connected
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">
                  Webhook: {slackConfig.webhook_url?.slice(0, 40)}...
                </p>
                {slackConfig.channel_name && (
                  <p className="text-xs text-muted-foreground">
                    Channel: #{slackConfig.channel_name}
                  </p>
                )}
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => testSlack.mutate()}
                  disabled={testSlack.isPending}
                >
                  {testSlack.isPending ? (
                    <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="mr-1 h-4 w-4" />
                  )}
                  Send Test Message
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  className="text-destructive"
                  onClick={() => deleteSlack.mutate()}
                  disabled={deleteSlack.isPending}
                >
                  <Trash2 className="mr-1 h-4 w-4" />
                  Disconnect
                </Button>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-sm text-muted-foreground">
                Get a webhook URL from Slack: Apps → Incoming Webhooks → Add New → Copy URL
              </p>
              <div className="grid gap-3 md:grid-cols-2">
                <div>
                  <label className="text-sm font-medium">Webhook URL</label>
                  <input
                    type="url"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="https://hooks.slack.com/services/..."
                    value={webhookUrl}
                    onChange={(e) => setWebhookUrl(e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    Channel Name (optional)
                  </label>
                  <input
                    type="text"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="#compliance-alerts"
                    value={channelName}
                    onChange={(e) => setChannelName(e.target.value)}
                  />
                </div>
              </div>
              <Button
                onClick={() => saveSlack.mutate()}
                disabled={!webhookUrl.trim() || saveSlack.isPending}
              >
                {saveSlack.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <MessageSquare className="mr-2 h-4 w-4" />
                )}
                Connect Slack
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Email Channel */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Mail className="h-5 w-5 text-muted-foreground" />
              <CardTitle>Email (SMTP)</CardTitle>
            </div>
            <Badge className="bg-gray-500/20 text-gray-500">
              {process.env.NEXT_PUBLIC_SMTP_CONFIGURED === "true"
                ? "Configured"
                : "Server config required"}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Email alerts are configured at the server level via environment
            variables (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD). When
            configured, all alerts are automatically sent via email in addition
            to Slack and in-app notifications.
          </p>
          <div className="mt-3 rounded-lg border p-3">
            <p className="text-xs font-mono text-muted-foreground">
              SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL
            </p>
          </div>
        </CardContent>
      </Card>

      {/* In-App Notifications */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bell className="h-5 w-5 text-muted-foreground" />
              <CardTitle>In-App Notifications</CardTitle>
            </div>
            <Badge className="bg-green-500/20 text-green-500">Always active</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            All alerts are always delivered as in-app notifications. View them
            from the bell icon in the top navigation bar or the Notifications
            page in the sidebar.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
