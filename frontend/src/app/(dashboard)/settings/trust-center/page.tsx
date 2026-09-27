"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useTrustCenterConfig,
  useUpdateTrustCenterConfig,
  useTrustCenterDocuments,
  useCreateTrustCenterDocument,
  useComplianceBadges,
  usePublicTrustPage,
  useNdaSignatures,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  Globe,
  FileText,
  Plus,
  Loader2,
  Save,
  ExternalLink,
  Shield,
  ShieldCheck,
  HeartPulse,
  CreditCard,
  Building,
  Eye,
  Copy,
  Check,
  FileSignature,
} from "lucide-react";

type ComplianceBadge = {
  name: string;
  color: string;
  icon: string;
  framework_id?: string;
  framework_name?: string;
  framework_version?: string;
};

const BADGE_ICON_MAP: Record<string, typeof Shield> = {
  shield: Shield,
  "shield-check": ShieldCheck,
  globe: Globe,
  "heart-pulse": HeartPulse,
  "credit-card": CreditCard,
  building: Building,
};

const docTypeBadge: Record<string, string> = {
  policy:
    "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  certification:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  report:
    "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
  other: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

export default function TrustCenterPage() {
  const orgId = useOrgId();
  const { data: config, isLoading: configLoading } =
    useTrustCenterConfig(orgId);
  const { data: documents, isLoading: docsLoading } =
    useTrustCenterDocuments(orgId);
  const updateConfig = useUpdateTrustCenterConfig(orgId);
  const createDocument = useCreateTrustCenterDocument(orgId);
  const { data: badgesData, isLoading: badgesLoading } =
    useComplianceBadges(orgId);
  const publicSlug = config?.slug || "";
  const { data: publicPage, isLoading: publicPageLoading } =
    usePublicTrustPage(publicSlug);
  const { data: ndaSignatures, isLoading: ndaLoading } =
    useNdaSignatures(orgId);
  const [copied, setCopied] = useState(false);

  const publicUrl =
    typeof window !== "undefined" && publicSlug
      ? `${window.location.origin}/trust/${publicSlug}`
      : "";

  function handleCopyPublicUrl() {
    if (!publicUrl) return;
    navigator.clipboard.writeText(publicUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  const [configForm, setConfigForm] = useState({
    is_published: false,
    headline: "",
    description: "",
    slug: "",
    certifications: "",
    contact_email: "",
  });
  const [configDirty, setConfigDirty] = useState(false);

  const [showAddDoc, setShowAddDoc] = useState(false);
  const [docForm, setDocForm] = useState({
    title: "",
    document_type: "policy",
    is_public: true,
    requires_nda: false,
    url: "",
    description: "",
  });

  // Populate config form when data loads
  useEffect(() => {
    if (config) {
      setConfigForm({
        is_published: config.is_published ?? false,
        headline: config.headline || "",
        description: config.description || "",
        slug: config.slug || "",
        certifications: Array.isArray(config.certifications)
          ? config.certifications.join(", ")
          : config.certifications || "",
        contact_email: config.contact_email || "",
      });
    }
  }, [config]);

  function handleSaveConfig() {
    const certsArray = configForm.certifications
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    updateConfig.mutate(
      {
        is_published: configForm.is_published,
        headline: configForm.headline,
        description: configForm.description,
        slug: configForm.slug,
        certifications: certsArray,
        contact_email: configForm.contact_email,
      },
      { onSuccess: () => setConfigDirty(false) }
    );
  }

  function handleAddDocument() {
    createDocument.mutate(docForm, {
      onSuccess: () => {
        setShowAddDoc(false);
        setDocForm({
          title: "",
          document_type: "policy",
          is_public: true,
          requires_nda: false,
          url: "",
          description: "",
        });
      },
    });
  }

  function updateConfigField(field: string, value: any) {
    setConfigForm((prev) => ({ ...prev, [field]: value }));
    setConfigDirty(true);
  }

  if (configLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Trust Center</h1>
          <p className="text-muted-foreground">
            Configure your public trust center page
          </p>
        </div>
        {config?.slug && (
          <a
            href={`/trust/${config.slug}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button variant="outline" className="gap-1.5">
              <ExternalLink className="h-4 w-4" />
              View Public Page
            </Button>
          </a>
        )}
      </div>

      {/* Config Card */}
      <Card>
        <CardHeader>
          <CardTitle>Configuration</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-3">
            <label className="text-sm font-medium">Published</label>
            <input
              type="checkbox"
              checked={configForm.is_published}
              onChange={(e) =>
                updateConfigField("is_published", e.target.checked)
              }
              className="h-4 w-4 rounded border"
            />
            <span className="text-sm text-muted-foreground">
              {configForm.is_published
                ? "Trust center is live"
                : "Trust center is hidden"}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Headline</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Security & Compliance at Your Company"
                value={configForm.headline}
                onChange={(e) =>
                  updateConfigField("headline", e.target.value)
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">Slug</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="your-company"
                value={configForm.slug}
                onChange={(e) =>
                  updateConfigField("slug", e.target.value)
                }
              />
            </div>
          </div>

          <div>
            <label className="text-sm font-medium">Description</label>
            <textarea
              className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
              rows={3}
              placeholder="Describe your security program..."
              value={configForm.description}
              onChange={(e) =>
                updateConfigField("description", e.target.value)
              }
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">
                Certifications (comma-separated)
              </label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="SOC 2, ISO 27001, GDPR"
                value={configForm.certifications}
                onChange={(e) =>
                  updateConfigField("certifications", e.target.value)
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">Contact Email</label>
              <input
                type="email"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="security@company.com"
                value={configForm.contact_email}
                onChange={(e) =>
                  updateConfigField("contact_email", e.target.value)
                }
              />
            </div>
          </div>

          {configDirty && (
            <div className="flex items-center gap-2 pt-2">
              <Button
                onClick={handleSaveConfig}
                disabled={updateConfig.isPending}
              >
                {updateConfig.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Save className="mr-2 h-4 w-4" />
                )}
                Save Configuration
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Documents */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Documents</CardTitle>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowAddDoc((v) => !v)}
            >
              <Plus className="mr-1 h-4 w-4" />
              Add Document
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {showAddDoc && (
            <div className="space-y-3 rounded-lg border p-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Title</label>
                  <input
                    type="text"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="Document title"
                    value={docForm.title}
                    onChange={(e) =>
                      setDocForm({ ...docForm, title: e.target.value })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Type</label>
                  <select
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    value={docForm.document_type}
                    onChange={(e) =>
                      setDocForm({
                        ...docForm,
                        document_type: e.target.value,
                      })
                    }
                  >
                    <option value="policy">Policy</option>
                    <option value="certification">Certification</option>
                    <option value="report">Report</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">URL</label>
                <input
                  type="url"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="https://..."
                  value={docForm.url}
                  onChange={(e) =>
                    setDocForm({ ...docForm, url: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="text-sm font-medium">Description</label>
                <textarea
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  rows={2}
                  value={docForm.description}
                  onChange={(e) =>
                    setDocForm({ ...docForm, description: e.target.value })
                  }
                />
              </div>

              <div className="flex items-center gap-6">
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={docForm.is_public}
                    onChange={(e) =>
                      setDocForm({
                        ...docForm,
                        is_public: e.target.checked,
                      })
                    }
                    className="h-4 w-4 rounded border"
                  />
                  Public
                </label>
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={docForm.requires_nda}
                    onChange={(e) =>
                      setDocForm({
                        ...docForm,
                        requires_nda: e.target.checked,
                      })
                    }
                    className="h-4 w-4 rounded border"
                  />
                  Requires NDA
                </label>
              </div>

              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={handleAddDocument}
                  disabled={
                    !docForm.title.trim() || createDocument.isPending
                  }
                >
                  {createDocument.isPending && (
                    <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                  )}
                  Add
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => setShowAddDoc(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
          )}

          {docsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-16 w-full rounded-lg" />
              ))}
            </div>
          ) : documents && documents.length > 0 ? (
            <div className="space-y-3">
              {documents.map((doc: any) => (
                <div
                  key={doc.id}
                  className="flex items-center gap-4 rounded-lg border p-3"
                >
                  <FileText className="h-5 w-5 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium">{doc.title}</div>
                    {doc.description && (
                      <p className="mt-1 text-xs text-muted-foreground line-clamp-1">
                        {doc.description}
                      </p>
                    )}
                  </div>
                  <Badge
                    className={
                      docTypeBadge[doc.document_type] || docTypeBadge.other
                    }
                  >
                    {doc.document_type}
                  </Badge>
                  {doc.is_public && (
                    <Badge variant="success">Public</Badge>
                  )}
                  {doc.requires_nda && (
                    <Badge variant="warning">NDA</Badge>
                  )}
                  {doc.url && (
                    <a
                      href={doc.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Button size="sm" variant="ghost">
                        <ExternalLink className="h-4 w-4" />
                      </Button>
                    </a>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <Shield className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No documents added yet.
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Compliance Badges */}
      <Card>
        <CardHeader>
          <CardTitle>Compliance Badges</CardTitle>
        </CardHeader>
        <CardContent>
          {badgesLoading ? (
            <div className="grid grid-cols-4 gap-3">
              {[1, 2, 3, 4].map((i) => (
                <Skeleton key={i} className="h-24 w-full rounded-lg" />
              ))}
            </div>
          ) : badgesData?.badges && badgesData.badges.length > 0 ? (
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
              {badgesData.badges.map((badge: ComplianceBadge) => {
                const Icon = BADGE_ICON_MAP[badge.icon] || Shield;
                return (
                  <div
                    key={badge.framework_id || badge.name}
                    className="flex flex-col items-center gap-2 rounded-lg border p-4 text-center"
                    style={{ borderColor: badge.color }}
                  >
                    <div
                      className="flex h-12 w-12 items-center justify-center rounded-full text-white"
                      style={{ backgroundColor: badge.color }}
                    >
                      <Icon className="h-6 w-6" />
                    </div>
                    <div className="text-sm font-semibold">{badge.name}</div>
                    {badge.framework_version && (
                      <div className="text-xs text-muted-foreground">
                        {badge.framework_version}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <ShieldCheck className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                Activate a compliance framework to display badges.
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Public Page Preview */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5" />
              Public Page Preview
            </CardTitle>
            {publicSlug && (
              <Button
                size="sm"
                variant="outline"
                onClick={handleCopyPublicUrl}
                className="gap-1.5"
              >
                {copied ? (
                  <>
                    <Check className="h-4 w-4" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4" />
                    Copy Public URL
                  </>
                )}
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {!publicSlug ? (
            <p className="text-sm text-muted-foreground">
              Set a slug in the configuration section to preview the public
              page.
            </p>
          ) : publicPageLoading ? (
            <Skeleton className="h-48 w-full rounded-lg" />
          ) : publicPage ? (
            <div className="space-y-4 rounded-lg border bg-muted/30 p-6">
              <div>
                <div className="text-2xl font-bold">
                  {publicPage.organization?.name || "Your Company"}
                </div>
                {publicPage.organization?.industry && (
                  <div className="text-sm text-muted-foreground">
                    {publicPage.organization.industry}
                  </div>
                )}
              </div>

              {publicPage.config?.headline && (
                <div className="text-lg font-medium">
                  {publicPage.config.headline}
                </div>
              )}

              {publicPage.config?.welcome_message && (
                <p className="text-sm text-muted-foreground">
                  {publicPage.config.welcome_message}
                </p>
              )}

              {publicPage.badges && publicPage.badges.length > 0 && (
                <div>
                  <div className="mb-2 text-xs font-semibold uppercase text-muted-foreground">
                    Certifications
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {publicPage.badges.map((b: ComplianceBadge) => {
                      const Icon = BADGE_ICON_MAP[b.icon] || Shield;
                      return (
                        <div
                          key={b.name}
                          className="flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium text-white"
                          style={{ backgroundColor: b.color }}
                        >
                          <Icon className="h-3 w-3" />
                          {b.name}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {publicPage.documents && publicPage.documents.length > 0 && (
                <div>
                  <div className="mb-2 text-xs font-semibold uppercase text-muted-foreground">
                    Public Documents
                  </div>
                  <ul className="space-y-1">
                    {publicPage.documents.map((d: any) => (
                      <li
                        key={d.id}
                        className="flex items-center gap-2 text-sm"
                      >
                        <FileText className="h-4 w-4 text-muted-foreground" />
                        <span>{d.title}</span>
                        {d.requires_nda && (
                          <Badge variant="warning">NDA</Badge>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {publicPage.config?.contact_email && (
                <div className="text-xs text-muted-foreground">
                  Contact: {publicPage.config.contact_email}
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              Public page not available. Publish the trust center and try
              again.
            </p>
          )}
        </CardContent>
      </Card>

      {/* NDA Signatures */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileSignature className="h-5 w-5" />
            NDA Signatures
          </CardTitle>
        </CardHeader>
        <CardContent>
          {ndaLoading ? (
            <Skeleton className="h-32 w-full rounded-lg" />
          ) : ndaSignatures?.signatures &&
            ndaSignatures.signatures.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left text-xs uppercase text-muted-foreground">
                    <th className="pb-2 pr-3">Name</th>
                    <th className="pb-2 pr-3">Email</th>
                    <th className="pb-2 pr-3">Company</th>
                    <th className="pb-2 pr-3">Signed At</th>
                    <th className="pb-2">IP</th>
                  </tr>
                </thead>
                <tbody>
                  {ndaSignatures.signatures.map((s: any) => (
                    <tr key={s.id} className="border-b last:border-0">
                      <td className="py-2 pr-3 font-medium">
                        {s.signer_name}
                      </td>
                      <td className="py-2 pr-3 text-muted-foreground">
                        {s.signer_email}
                      </td>
                      <td className="py-2 pr-3 text-muted-foreground">
                        {s.signer_company || "—"}
                      </td>
                      <td className="py-2 pr-3 text-muted-foreground">
                        {s.signed_at
                          ? new Date(s.signed_at).toLocaleString()
                          : "—"}
                      </td>
                      <td className="py-2 text-xs text-muted-foreground">
                        {s.ip_address || "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="mt-3 text-xs text-muted-foreground">
                {ndaSignatures.total} total signature
                {ndaSignatures.total === 1 ? "" : "s"}
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <FileSignature className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No NDA signatures yet.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
