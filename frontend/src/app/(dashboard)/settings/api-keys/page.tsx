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
  Key,
  Plus,
  Trash2,
  Loader2,
  Copy,
  AlertTriangle,
  ShieldAlert,
} from "lucide-react";

interface ApiKey {
  id: string;
  name: string;
  key_prefix: string;
  scopes: string[];
  last_used_at: string | null;
  created_at: string;
}

interface ApiKeyCreateResponse {
  id: string;
  name: string;
  key: string;
  key_prefix: string;
  scopes: string[];
}

const AVAILABLE_SCOPES = ["read", "write", "admin"] as const;

export default function ApiKeysPage() {
  const orgId = useOrgId();
  const qc = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [selectedScopes, setSelectedScopes] = useState<string[]>([]);
  const [newlyCreatedKey, setNewlyCreatedKey] = useState<string | null>(null);
  const [confirmRevokeId, setConfirmRevokeId] = useState<string | null>(null);

  const { data: apiKeys, isLoading } = useQuery({
    queryKey: ["api-keys", orgId],
    queryFn: () => api.get<ApiKey[]>(`/organizations/${orgId}/api-keys`),
    enabled: !!orgId,
  });

  const createKey = useMutation({
    mutationFn: () =>
      api.post<ApiKeyCreateResponse>(`/organizations/${orgId}/api-keys`, {
        name,
        scopes: selectedScopes,
      }),
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ["api-keys", orgId] });
      setNewlyCreatedKey(data.key);
      setName("");
      setSelectedScopes([]);
      toast.success("API key created");
    },
    onError: (err: any) => toast.error(err.message || "Failed to create API key"),
  });

  const revokeKey = useMutation({
    mutationFn: (keyId: string) =>
      api.delete(`/organizations/${orgId}/api-keys/${keyId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["api-keys", orgId] });
      setConfirmRevokeId(null);
      toast.success("API key revoked");
    },
    onError: (err: any) => toast.error(err.message || "Failed to revoke API key"),
  });

  function toggleScope(scope: string) {
    setSelectedScopes((prev) =>
      prev.includes(scope)
        ? prev.filter((s) => s !== scope)
        : [...prev, scope]
    );
  }

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).then(
      () => toast.success("Copied to clipboard"),
      () => toast.error("Failed to copy")
    );
  }

  function handleOpenForm() {
    setShowForm(true);
    setNewlyCreatedKey(null);
  }

  function handleCloseForm() {
    setShowForm(false);
    setNewlyCreatedKey(null);
    setName("");
    setSelectedScopes([]);
  }

  const scopeVariant: Record<string, string> = {
    read: "bg-blue-500/20 text-blue-500",
    write: "bg-yellow-500/20 text-yellow-500",
    admin: "bg-red-500/20 text-red-500",
  };

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
            <h1 className="text-3xl font-bold">API Keys</h1>
            <p className="text-muted-foreground">
              Manage API keys for service accounts and CI/CD
            </p>
          </div>
          <Button onClick={handleOpenForm}>
            <Plus className="mr-2 h-4 w-4" />
            Create API Key
          </Button>
        </div>
      </div>

      {/* Newly Created Key Banner */}
      {newlyCreatedKey && (
        <Card className="border-yellow-500/50 bg-yellow-500/5">
          <CardContent className="p-6 space-y-3">
            <div className="flex items-center gap-2 text-yellow-600 dark:text-yellow-400">
              <AlertTriangle className="h-5 w-5" />
              <span className="text-sm font-semibold">
                This key will only be shown once. Copy it now.
              </span>
            </div>
            <div className="flex items-center gap-2">
              <code className="flex-1 rounded-md border bg-muted p-3 text-sm font-mono break-all">
                {newlyCreatedKey}
              </code>
              <Button
                size="sm"
                variant="outline"
                onClick={() => copyToClipboard(newlyCreatedKey)}
              >
                <Copy className="mr-1 h-4 w-4" />
                Copy
              </Button>
            </div>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setNewlyCreatedKey(null)}
            >
              Dismiss
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Create Form */}
      {showForm && !newlyCreatedKey && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Key className="h-5 w-5" />
              New API Key
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Name</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g. CI/CD Pipeline, Monitoring Service"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Scopes</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {AVAILABLE_SCOPES.map((scope) => (
                  <label
                    key={scope}
                    className="flex items-center gap-2 rounded-md border px-3 py-2 text-sm cursor-pointer hover:bg-muted/50"
                  >
                    <input
                      type="checkbox"
                      checked={selectedScopes.includes(scope)}
                      onChange={() => toggleScope(scope)}
                      className="rounded"
                    />
                    <span className="capitalize">{scope}</span>
                  </label>
                ))}
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                Select the permission scopes this key should have
              </p>
            </div>
            <div className="flex gap-2 pt-2">
              <Button
                onClick={() => createKey.mutate()}
                disabled={
                  !name.trim() ||
                  selectedScopes.length === 0 ||
                  createKey.isPending
                }
              >
                {createKey.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Plus className="mr-2 h-4 w-4" />
                )}
                Create
              </Button>
              <Button variant="ghost" onClick={handleCloseForm}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* API Keys List */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : apiKeys && apiKeys.length > 0 ? (
        <div className="space-y-3">
          {apiKeys.map((apiKey) => (
            <Card key={apiKey.id}>
              <CardContent className="flex items-center justify-between p-4">
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <Key className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm font-medium">{apiKey.name}</span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-muted-foreground">
                    <span className="font-mono">{apiKey.key_prefix}...</span>
                    <span>
                      {apiKey.last_used_at
                        ? `Last used ${new Date(apiKey.last_used_at).toLocaleDateString()}`
                        : "Never used"}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {apiKey.scopes.map((scope) => (
                      <Badge
                        key={scope}
                        className={scopeVariant[scope] || "bg-gray-500/20 text-gray-500"}
                      >
                        {scope}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  {confirmRevokeId === apiKey.id ? (
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-destructive font-medium">
                        Confirm?
                      </span>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => revokeKey.mutate(apiKey.id)}
                        disabled={revokeKey.isPending}
                      >
                        {revokeKey.isPending ? (
                          <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                        ) : (
                          <ShieldAlert className="mr-1 h-4 w-4" />
                        )}
                        Revoke
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => setConfirmRevokeId(null)}
                      >
                        Cancel
                      </Button>
                    </div>
                  ) : (
                    <Button
                      size="sm"
                      variant="ghost"
                      className="text-destructive"
                      onClick={() => setConfirmRevokeId(apiKey.id)}
                    >
                      <Trash2 className="mr-1 h-4 w-4" />
                      Revoke
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <Key className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No API keys</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Create an API key to authenticate service accounts and CI/CD
              pipelines.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
