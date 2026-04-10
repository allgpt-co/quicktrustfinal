"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useApprovedResponses,
  useCreateApprovedResponse,
  useDeleteApprovedResponse,
  useSeedResponseLibrary,
  type ApprovedResponseItem,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  Library,
  Plus,
  Loader2,
  Search,
  Sparkles,
  Trash2,
  ChevronDown,
  ChevronUp,
  ArrowLeft,
} from "lucide-react";

const CATEGORY_LABELS: Record<string, string> = {
  encryption: "Encryption",
  access_control: "Access Control",
  incident_response: "Incident Response",
  compliance: "Compliance",
  business_continuity: "Business Continuity",
  data_privacy: "Data Privacy",
  vulnerability_management: "Vulnerability Management",
  secure_development: "Secure Development",
  training: "Training",
  monitoring: "Monitoring",
};

const CATEGORY_COLOR: Record<string, string> = {
  encryption:
    "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  access_control:
    "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
  incident_response:
    "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  compliance:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  business_continuity:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  data_privacy:
    "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-100",
  vulnerability_management:
    "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  secure_development:
    "bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-100",
  training:
    "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-100",
  monitoring:
    "bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-100",
};

interface ResponseCardProps {
  response: ApprovedResponseItem;
  onDelete: (id: string) => void;
  isDeleting: boolean;
}

function ResponseCard({ response, onDelete, isDeleting }: ResponseCardProps) {
  const [expanded, setExpanded] = useState(false);
  const category = response.category;
  const categoryLabel = CATEGORY_LABELS[category] || category;
  const categoryColor =
    CATEGORY_COLOR[category] ||
    "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100";

  return (
    <Card>
      <CardContent className="space-y-3 p-4">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1">
            <div className="font-medium">{response.question}</div>
            <div className="mt-1 flex flex-wrap items-center gap-2 text-xs">
              <Badge className={categoryColor}>{categoryLabel}</Badge>
              {response.tags.map((tag) => (
                <Badge key={tag} variant="outline" className="font-mono">
                  {tag}
                </Badge>
              ))}
              <span className="text-muted-foreground">
                Used {response.use_count} time
                {response.use_count === 1 ? "" : "s"}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setExpanded((v) => !v)}
              aria-label={expanded ? "Collapse" : "Expand"}
            >
              {expanded ? (
                <ChevronUp className="h-4 w-4" />
              ) : (
                <ChevronDown className="h-4 w-4" />
              )}
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onDelete(response.id)}
              disabled={isDeleting}
              aria-label="Delete response"
            >
              <Trash2 className="h-4 w-4 text-destructive" />
            </Button>
          </div>
        </div>
        {expanded && (
          <div className="rounded-md border bg-muted/30 p-3 text-sm whitespace-pre-wrap">
            {response.answer}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function ResponseLibraryPage() {
  const orgId = useOrgId();
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({
    question: "",
    answer: "",
    category: "compliance",
    tags: "",
  });

  const { data, isLoading } = useApprovedResponses(orgId, {
    search: debouncedSearch || undefined,
  });
  const createResponse = useCreateApprovedResponse(orgId);
  const deleteResponse = useDeleteApprovedResponse(orgId);
  const seedLibrary = useSeedResponseLibrary(orgId);

  // Debounce search
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(handler);
  }, [search]);

  const handleCreate = () => {
    createResponse.mutate(
      {
        question: form.question.trim(),
        answer: form.answer.trim(),
        category: form.category.trim(),
        tags: form.tags
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      },
      {
        onSuccess: () => {
          setShowAdd(false);
          setForm({
            question: "",
            answer: "",
            category: "compliance",
            tags: "",
          });
        },
      }
    );
  };

  const items = data?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/questionnaires">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <div>
            <h1 className="flex items-center gap-2 text-3xl font-bold">
              <Library className="h-7 w-7" />
              Approved Response Library
            </h1>
            <p className="text-muted-foreground">
              Pre-approved answers for reuse in security questionnaires
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            onClick={() => seedLibrary.mutate()}
            disabled={seedLibrary.isPending}
          >
            {seedLibrary.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Sparkles className="mr-2 h-4 w-4" />
            )}
            Seed Library
          </Button>
          <Button onClick={() => setShowAdd((v) => !v)}>
            <Plus className="mr-2 h-4 w-4" />
            Add Response
          </Button>
        </div>
      </div>

      {/* Search */}
      <Card>
        <CardContent className="p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              type="search"
              className="w-full rounded-md border bg-background py-2 pl-9 pr-3 text-sm"
              placeholder="Search questions and answers..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Add Form */}
      {showAdd && (
        <Card>
          <CardHeader>
            <CardTitle>Add Approved Response</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Question</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="How do you encrypt data at rest?"
                value={form.question}
                onChange={(e) =>
                  setForm({ ...form, question: e.target.value })
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">Answer</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                rows={5}
                placeholder="Enter the approved response..."
                value={form.answer}
                onChange={(e) =>
                  setForm({ ...form, answer: e.target.value })
                }
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">Category</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                >
                  {Object.entries(CATEGORY_LABELS).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium">
                  Tags (comma-separated)
                </label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="aes-256, kms"
                  value={form.tags}
                  onChange={(e) => setForm({ ...form, tags: e.target.value })}
                />
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button
                onClick={handleCreate}
                disabled={
                  !form.question.trim() ||
                  !form.answer.trim() ||
                  createResponse.isPending
                }
              >
                {createResponse.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Save Response
              </Button>
              <Button variant="outline" onClick={() => setShowAdd(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* List */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-lg" />
          ))}
        </div>
      ) : items.length > 0 ? (
        <div className="space-y-3">
          <div className="text-xs text-muted-foreground">
            {data?.total ?? 0} response{data?.total === 1 ? "" : "s"}
          </div>
          {items.map((item) => (
            <ResponseCard
              key={item.id}
              response={item}
              onDelete={(id) => deleteResponse.mutate(id)}
              isDeleting={deleteResponse.isPending}
            />
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <Library className="mb-4 h-12 w-12 text-muted-foreground" />
            <h3 className="text-lg font-medium">No approved responses</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Seed the library or add your first response to get started.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
