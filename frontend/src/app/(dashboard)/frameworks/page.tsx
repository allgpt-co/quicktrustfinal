"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useFrameworks } from "@/hooks/use-api";
import api from "@/lib/api";
import { Shield, AlertTriangle, Plus, GitCompare, Copy } from "lucide-react";
import { toast } from "sonner";

export default function FrameworksPage() {
  const { data: frameworks, isLoading, error } = useFrameworks();
  const [showCompare, setShowCompare] = useState(false);
  const [sourceId, setSourceId] = useState("");
  const [targetId, setTargetId] = useState("");
  const [diffResult, setDiffResult] = useState<any>(null);
  const [diffLoading, setDiffLoading] = useState(false);
  const [versionLoading, setVersionLoading] = useState<string | null>(null);

  async function handleCompare() {
    if (!sourceId || !targetId) return;
    setDiffLoading(true);
    try {
      const result = await api.get<any>(`/frameworks/diff?source_id=${sourceId}&target_id=${targetId}`);
      setDiffResult(result);
    } catch (e: any) {
      toast.error(e.message || "Failed to compare");
    }
    setDiffLoading(false);
  }

  async function handleCreateVersion(fwId: string) {
    setVersionLoading(fwId);
    try {
      const result = await api.post<any>(`/frameworks/${fwId}/new-version`);
      toast.success(`Created ${result.name} v${result.version}`);
      window.location.reload();
    } catch (e: any) {
      toast.error(e.message || "Failed to create version");
    }
    setVersionLoading(null);
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Frameworks</h1>
          <p className="text-muted-foreground">Compliance frameworks and their requirements</p>
        </div>
        <Card className="border-destructive">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertTriangle className="h-12 w-12 text-destructive mb-4" />
            <h3 className="text-lg font-semibold">Failed to load frameworks</h3>
            <p className="text-sm text-muted-foreground mt-2">
              {error.message || "An unexpected error occurred. Please try again later."}
            </p>
            <Button className="mt-4" onClick={() => window.location.reload()}>
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Frameworks</h1>
          <p className="text-muted-foreground">Compliance frameworks and their requirements</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setShowCompare(!showCompare)}>
            <GitCompare className="h-4 w-4 mr-1" />
            Compare Frameworks
          </Button>
          <Link href="/frameworks/new">
            <Button>
              <Plus className="h-4 w-4 mr-1" />
              Create Framework
            </Button>
          </Link>
        </div>
      </div>

      {/* Compare Frameworks */}
      {showCompare && frameworks && (
        <Card>
          <CardContent className="p-6 space-y-4">
            <h2 className="text-lg font-semibold">Compare Frameworks</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">Source Framework</label>
                <select className="mt-1 w-full rounded-md border bg-background p-2 text-sm" value={sourceId} onChange={(e) => setSourceId(e.target.value)}>
                  <option value="">Select...</option>
                  {frameworks.map((fw) => (
                    <option key={fw.id} value={fw.id}>{fw.name} (v{fw.version})</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium">Target Framework</label>
                <select className="mt-1 w-full rounded-md border bg-background p-2 text-sm" value={targetId} onChange={(e) => setTargetId(e.target.value)}>
                  <option value="">Select...</option>
                  {frameworks.map((fw) => (
                    <option key={fw.id} value={fw.id}>{fw.name} (v{fw.version})</option>
                  ))}
                </select>
              </div>
            </div>
            <Button onClick={handleCompare} disabled={!sourceId || !targetId || diffLoading}>
              {diffLoading ? "Comparing..." : "Compare"}
            </Button>

            {diffResult && (
              <div className="space-y-3 pt-4 border-t">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <Card className="border-green-500/30 bg-green-500/5">
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold text-green-500">+{diffResult.added?.length || 0}</div>
                      <div className="text-xs text-muted-foreground">Added</div>
                    </CardContent>
                  </Card>
                  <Card className="border-red-500/30 bg-red-500/5">
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold text-red-500">-{diffResult.removed?.length || 0}</div>
                      <div className="text-xs text-muted-foreground">Removed</div>
                    </CardContent>
                  </Card>
                  <Card className="border-yellow-500/30 bg-yellow-500/5">
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold text-yellow-500">~{diffResult.modified?.length || 0}</div>
                      <div className="text-xs text-muted-foreground">Modified</div>
                    </CardContent>
                  </Card>
                </div>
                {diffResult.added?.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-green-600 mb-1">Added Requirements</h3>
                    <div className="space-y-1 max-h-40 overflow-y-auto">
                      {diffResult.added.slice(0, 10).map((r: any) => (
                        <div key={r.code} className="text-xs rounded bg-green-500/10 p-2">
                          <span className="font-mono font-medium">{r.code}</span> — {r.title}
                        </div>
                      ))}
                      {diffResult.added.length > 10 && <p className="text-xs text-muted-foreground">...and {diffResult.added.length - 10} more</p>}
                    </div>
                  </div>
                )}
                {diffResult.removed?.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-red-600 mb-1">Removed Requirements</h3>
                    <div className="space-y-1 max-h-40 overflow-y-auto">
                      {diffResult.removed.slice(0, 10).map((r: any) => (
                        <div key={r.code} className="text-xs rounded bg-red-500/10 p-2">
                          <span className="font-mono font-medium">{r.code}</span> — {r.title}
                        </div>
                      ))}
                      {diffResult.removed.length > 10 && <p className="text-xs text-muted-foreground">...and {diffResult.removed.length - 10} more</p>}
                    </div>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-48 w-full rounded-xl" />
          ))}
        </div>
      ) : frameworks && frameworks.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {frameworks.map((fw) => (
            <Link key={fw.id} href={`/frameworks/${fw.id}`}>
              <Card className="cursor-pointer transition-shadow hover:shadow-lg">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Shield className="h-8 w-8 text-primary" />
                    <Badge variant={fw.is_active ? "success" : "secondary"}>
                      {fw.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </div>
                  <CardTitle className="mt-2">{fw.name}</CardTitle>
                  <CardDescription>Version {fw.version}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {fw.description || "No description available."}
                  </p>
                  <div className="flex items-center gap-2 mt-3">
                    {fw.category && (
                      <Badge variant="outline">
                        {fw.category}
                      </Badge>
                    )}
                    <Button
                      size="sm"
                      variant="ghost"
                      className="ml-auto text-xs"
                      disabled={versionLoading === fw.id}
                      onClick={(e) => { e.preventDefault(); e.stopPropagation(); handleCreateVersion(fw.id); }}
                    >
                      <Copy className="h-3 w-3 mr-1" />
                      {versionLoading === fw.id ? "Creating..." : "New Version"}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-12 text-center">
            <Shield className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No frameworks loaded</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Run the seed script to load the SOC 2 framework.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
