"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import api from "@/lib/api";
import { useOrgId } from "@/hooks/use-org-id";
import { toast } from "sonner";
import {
  Shield,
  Key,
  Plus,
  Trash2,
  Copy,
  CheckCircle,
  XCircle,
  Loader2,
  ArrowLeft,
  Globe,
  Lock,
} from "lucide-react";
import Link from "next/link";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface SSOConfig {
  id: string;
  provider: string;
  enabled: boolean;
  enforced: boolean;
  entity_id: string | null;
  sso_url: string | null;
  certificate_configured: boolean;
  oidc_client_id: string | null;
  oidc_issuer: string | null;
  email_domains: string | null;
  scim_enabled: boolean;
}

interface SCIMToken {
  id: string;
  name: string;
  is_active: boolean;
  last_used_at: string | null;
  created_at: string;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function SSOSettingsPage() {
  const orgId = useOrgId();
  const qc = useQueryClient();
  const [tab, setTab] = useState<"sso" | "scim">("sso");
  const [newTokenName, setNewTokenName] = useState("");
  const [createdToken, setCreatedToken] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  // SSO form state
  const [provider, setProvider] = useState("saml");
  const [enabled, setEnabled] = useState(false);
  const [enforced, setEnforced] = useState(false);
  const [entityId, setEntityId] = useState("");
  const [ssoUrl, setSsoUrl] = useState("");
  const [certificate, setCertificate] = useState("");
  const [oidcClientId, setOidcClientId] = useState("");
  const [oidcIssuer, setOidcIssuer] = useState("");
  const [emailDomains, setEmailDomains] = useState("");

  // --- Queries ---
  const { data: ssoConfig, isLoading: ssoLoading } = useQuery<SSOConfig | null>({
    queryKey: ["sso-config", orgId],
    queryFn: () => api.get(`/organizations/${orgId}/sso/config`),
    enabled: !!orgId,
  });

  const { data: tokens, isLoading: tokensLoading } = useQuery<SCIMToken[]>({
    queryKey: ["scim-tokens", orgId],
    queryFn: () => api.get(`/organizations/${orgId}/sso/scim-tokens`),
    enabled: !!orgId && tab === "scim",
  });

  // --- Mutations ---
  const saveSSO = useMutation({
    mutationFn: (data: any) => api.put(`/organizations/${orgId}/sso/config`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["sso-config"] });
      toast.success("SSO configuration saved");
    },
    onError: () => toast.error("Failed to save SSO configuration"),
  });

  const deleteSSO = useMutation({
    mutationFn: () => api.delete(`/organizations/${orgId}/sso/config`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["sso-config"] });
      toast.success("SSO configuration deleted");
    },
  });

  const createToken = useMutation({
    mutationFn: (name: string) =>
      api.post(`/organizations/${orgId}/sso/scim-tokens`, { name }),
    onSuccess: (data: any) => {
      qc.invalidateQueries({ queryKey: ["scim-tokens"] });
      setCreatedToken(data.raw_token);
      setNewTokenName("");
      toast.success("SCIM token created");
    },
    onError: () => toast.error("Failed to create token"),
  });

  const revokeToken = useMutation({
    mutationFn: (tokenId: string) =>
      api.delete(`/organizations/${orgId}/sso/scim-tokens/${tokenId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["scim-tokens"] });
      toast.success("Token revoked");
    },
  });

  const handleCopy = () => {
    if (createdToken) {
      navigator.clipboard.writeText(createdToken);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleSaveSSO = () => {
    saveSSO.mutate({
      provider,
      enabled,
      enforced,
      entity_id: entityId || null,
      sso_url: ssoUrl || null,
      certificate: certificate || null,
      oidc_client_id: oidcClientId || null,
      oidc_issuer: oidcIssuer || null,
      email_domains: emailDomains || null,
    });
  };

  // Load SSO config into form when data arrives
  if (ssoConfig && !ssoLoading && provider === "saml" && !entityId && ssoConfig.entity_id) {
    setProvider(ssoConfig.provider);
    setEnabled(ssoConfig.enabled);
    setEnforced(ssoConfig.enforced);
    setEntityId(ssoConfig.entity_id || "");
    setSsoUrl(ssoConfig.sso_url || "");
    setOidcClientId(ssoConfig.oidc_client_id || "");
    setOidcIssuer(ssoConfig.oidc_issuer || "");
    setEmailDomains(ssoConfig.email_domains || "");
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/settings">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Settings
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold">SSO & SCIM</h1>
          <p className="text-muted-foreground">
            Configure Single Sign-On and automated user provisioning
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 rounded-lg bg-muted p-1 w-fit">
        <button
          onClick={() => setTab("sso")}
          className={`flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors ${
            tab === "sso" ? "bg-background text-foreground shadow-sm" : "text-muted-foreground"
          }`}
        >
          <Shield className="h-4 w-4" />
          SSO Configuration
        </button>
        <button
          onClick={() => setTab("scim")}
          className={`flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors ${
            tab === "scim" ? "bg-background text-foreground shadow-sm" : "text-muted-foreground"
          }`}
        >
          <Key className="h-4 w-4" />
          SCIM Provisioning
        </button>
      </div>

      {/* ================================================================ */}
      {/* SSO TAB                                                          */}
      {/* ================================================================ */}
      {tab === "sso" && (
        <div className="grid gap-6 md:grid-cols-3">
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Identity Provider Configuration</CardTitle>
              <CardDescription>
                Connect your company&apos;s identity provider (Okta, Azure AD, Google Workspace) for Single Sign-On
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {ssoLoading ? (
                <Skeleton className="h-40 w-full" />
              ) : (
                <>
                  {/* Provider selector */}
                  <div>
                    <label className="text-sm font-medium">Protocol</label>
                    <div className="flex gap-2 mt-1">
                      <Button
                        size="sm"
                        variant={provider === "saml" ? "default" : "outline"}
                        onClick={() => setProvider("saml")}
                      >
                        SAML 2.0
                      </Button>
                      <Button
                        size="sm"
                        variant={provider === "oidc" ? "default" : "outline"}
                        onClick={() => setProvider("oidc")}
                      >
                        OpenID Connect
                      </Button>
                    </div>
                  </div>

                  {/* SAML fields */}
                  {provider === "saml" && (
                    <>
                      <div>
                        <label className="text-sm font-medium">IdP Entity ID</label>
                        <input
                          className="mt-1 w-full rounded-md border bg-background px-3 py-2 text-sm"
                          value={entityId}
                          onChange={(e) => setEntityId(e.target.value)}
                          placeholder="https://idp.company.com/saml/metadata"
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">SSO Login URL</label>
                        <input
                          className="mt-1 w-full rounded-md border bg-background px-3 py-2 text-sm"
                          value={ssoUrl}
                          onChange={(e) => setSsoUrl(e.target.value)}
                          placeholder="https://idp.company.com/saml/sso"
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">X.509 Certificate (PEM)</label>
                        <textarea
                          className="mt-1 w-full rounded-md border bg-background px-3 py-2 text-sm font-mono h-24"
                          value={certificate}
                          onChange={(e) => setCertificate(e.target.value)}
                          placeholder="-----BEGIN CERTIFICATE-----&#10;MIIDp...&#10;-----END CERTIFICATE-----"
                        />
                        {ssoConfig?.certificate_configured && !certificate && (
                          <p className="text-xs text-green-500 mt-1">Certificate already configured</p>
                        )}
                      </div>
                    </>
                  )}

                  {/* OIDC fields */}
                  {provider === "oidc" && (
                    <>
                      <div>
                        <label className="text-sm font-medium">Client ID</label>
                        <input
                          className="mt-1 w-full rounded-md border bg-background px-3 py-2 text-sm"
                          value={oidcClientId}
                          onChange={(e) => setOidcClientId(e.target.value)}
                          placeholder="your-oidc-client-id"
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Issuer URL</label>
                        <input
                          className="mt-1 w-full rounded-md border bg-background px-3 py-2 text-sm"
                          value={oidcIssuer}
                          onChange={(e) => setOidcIssuer(e.target.value)}
                          placeholder="https://accounts.google.com"
                        />
                      </div>
                    </>
                  )}

                  {/* Common fields */}
                  <div>
                    <label className="text-sm font-medium">Email Domains</label>
                    <input
                      className="mt-1 w-full rounded-md border bg-background px-3 py-2 text-sm"
                      value={emailDomains}
                      onChange={(e) => setEmailDomains(e.target.value)}
                      placeholder="company.com, subsidiary.com"
                    />
                    <p className="text-xs text-muted-foreground mt-1">
                      Comma-separated. Users with these email domains will be redirected to SSO.
                    </p>
                  </div>

                  {/* Toggles */}
                  <div className="flex items-center gap-6 pt-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={enabled}
                        onChange={(e) => setEnabled(e.target.checked)}
                        className="rounded"
                      />
                      <span className="text-sm font-medium">Enable SSO</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={enforced}
                        onChange={(e) => setEnforced(e.target.checked)}
                        className="rounded"
                      />
                      <span className="text-sm font-medium">Enforce SSO (disable password login)</span>
                    </label>
                  </div>

                  {/* Save */}
                  <div className="flex gap-2 pt-4">
                    <Button onClick={handleSaveSSO} disabled={saveSSO.isPending}>
                      {saveSSO.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                      Save Configuration
                    </Button>
                    {ssoConfig && (
                      <Button
                        variant="destructive"
                        onClick={() => deleteSSO.mutate()}
                        disabled={deleteSSO.isPending}
                      >
                        Delete
                      </Button>
                    )}
                  </div>
                </>
              )}
            </CardContent>
          </Card>

          {/* Status card */}
          <Card>
            <CardHeader>
              <CardTitle>Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2">
                {ssoConfig?.enabled ? (
                  <>
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-green-500 font-medium">SSO Active</span>
                  </>
                ) : (
                  <>
                    <XCircle className="h-5 w-5 text-yellow-500" />
                    <span className="text-yellow-500 font-medium">SSO Not Configured</span>
                  </>
                )}
              </div>
              {ssoConfig && (
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Protocol</span>
                    <Badge variant="outline">{ssoConfig.provider.toUpperCase()}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Enforced</span>
                    <span>{ssoConfig.enforced ? "Yes" : "No"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Certificate</span>
                    <span>{ssoConfig.certificate_configured ? "Configured" : "Missing"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">SCIM</span>
                    <span>{ssoConfig.scim_enabled ? "Enabled" : "Disabled"}</span>
                  </div>
                </div>
              )}

              <div className="border-t pt-4">
                <p className="text-xs text-muted-foreground">
                  <Globe className="inline h-3 w-3 mr-1" />
                  SP ACS URL: <code className="text-[10px]">{typeof window !== "undefined" ? window.location.origin : ""}/api/v1/auth/sso/callback</code>
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* ================================================================ */}
      {/* SCIM TAB                                                         */}
      {/* ================================================================ */}
      {tab === "scim" && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>SCIM Provisioning Tokens</CardTitle>
              <CardDescription>
                Generate bearer tokens for your identity provider (Okta, Azure AD) to automatically sync users via SCIM 2.0
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Create token */}
              <div className="flex gap-2">
                <input
                  className="flex-1 rounded-md border bg-background px-3 py-2 text-sm"
                  value={newTokenName}
                  onChange={(e) => setNewTokenName(e.target.value)}
                  placeholder="Token name (e.g., Okta Production)"
                />
                <Button
                  onClick={() => createToken.mutate(newTokenName)}
                  disabled={!newTokenName.trim() || createToken.isPending}
                >
                  {createToken.isPending ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <Plus className="mr-2 h-4 w-4" />
                  )}
                  Generate Token
                </Button>
              </div>

              {/* Show newly created token */}
              {createdToken && (
                <div className="rounded-lg border border-yellow-500/30 bg-yellow-500/10 p-4">
                  <div className="flex items-center gap-2 text-yellow-500 font-medium mb-2">
                    <Lock className="h-4 w-4" />
                    Copy this token now — it won&apos;t be shown again!
                  </div>
                  <div className="flex gap-2">
                    <code className="flex-1 rounded bg-background px-3 py-2 text-xs font-mono break-all">
                      {createdToken}
                    </code>
                    <Button size="sm" variant="outline" onClick={handleCopy}>
                      {copied ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground mt-2">
                    SCIM Base URL: <code>{typeof window !== "undefined" ? window.location.origin.replace("3001","8000") : ""}/api/v1/scim/v2</code>
                  </p>
                </div>
              )}

              {/* Token list */}
              {tokensLoading ? (
                <Skeleton className="h-20 w-full" />
              ) : !tokens || tokens.length === 0 ? (
                <p className="text-sm text-muted-foreground py-4 text-center">
                  No SCIM tokens yet. Generate one to connect your identity provider.
                </p>
              ) : (
                <div className="divide-y">
                  {tokens.map((t) => (
                    <div key={t.id} className="flex items-center justify-between py-3">
                      <div>
                        <div className="flex items-center gap-2">
                          <Key className="h-4 w-4 text-muted-foreground" />
                          <span className="font-medium text-sm">{t.name}</span>
                          {t.is_active ? (
                            <Badge className="bg-green-500/20 text-green-400 border-green-500/30">Active</Badge>
                          ) : (
                            <Badge variant="destructive">Revoked</Badge>
                          )}
                        </div>
                        <div className="text-xs text-muted-foreground mt-1">
                          Created: {new Date(t.created_at).toLocaleDateString()}
                          {t.last_used_at && (
                            <> | Last used: {new Date(t.last_used_at).toLocaleDateString()}</>
                          )}
                        </div>
                      </div>
                      {t.is_active && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => revokeToken.mutate(t.id)}
                          disabled={revokeToken.isPending}
                        >
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* How to connect */}
          <Card>
            <CardHeader>
              <CardTitle>How to Connect</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <p><strong>1.</strong> Generate a SCIM token above</p>
              <p><strong>2.</strong> In your identity provider (Okta/Azure AD), go to the SCIM provisioning settings</p>
              <p><strong>3.</strong> Enter the SCIM Base URL and Bearer Token</p>
              <p><strong>4.</strong> Enable &quot;Push Users&quot; and &quot;Push Groups&quot;</p>
              <p><strong>5.</strong> Users will be automatically created/deactivated in QuickTrust when changes happen in your IdP</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
