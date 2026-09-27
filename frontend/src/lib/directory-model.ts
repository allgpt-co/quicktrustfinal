import { z } from 'zod';

const date = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/)
  .refine(
    (s) => !Number.isNaN(Date.parse(s)) && new Date(s).toISOString().slice(0, 10) === s,
    'Invalid calendar date',
  );
const id = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
const text = z.string().trim().min(1);
const officialUrl = z
  .url()
  .refine(
    (s) => new URL(s).protocol === 'https:' && !new URL(s).username && !new URL(s).password,
    'Use a public HTTPS source',
  );
export const requirementTypes = [
  'license',
  'permit',
  'registration',
  'professional-authorization',
  'product-approval',
  'certification',
  'attestation',
  'regulation',
  'framework',
] as const;
export const typeLabels: Record<(typeof requirementTypes)[number], string> = {
  license: 'Business license',
  permit: 'Permit',
  registration: 'Registration',
  'professional-authorization': 'Professional authorization',
  'product-approval': 'Product approval',
  certification: 'Certification',
  attestation: 'Attestation',
  regulation: 'Regulation',
  framework: 'Framework',
};
export const sourceSchema = z
  .object({
    id,
    name: text,
    publisher: text,
    url: officialUrl,
    kind: z.literal('official'),
    checkedAt: date.nullable(),
    reviewedAt: date.nullable(),
  })
  .strict();
export const jurisdictionSchema = z
  .object({
    id: text,
    name: text,
    officialName: text.optional(),
    kind: z.enum([
      'country',
      'subdivision',
      'municipality',
      'special-zone',
      'international',
      'supranational',
    ]),
    parent: text.nullable(),
    sourceId: id,
    localType: text.optional(),
    members: z.array(text).optional(),
  })
  .strict();
export const industrySchema = z
  .object({
    id: z.string().regex(/^([A-V]|\d{2,4})$/),
    name: text,
    parent: text.nullable(),
    level: z.enum(['section', 'division', 'group', 'class']),
  })
  .strict();
export const coverageSchema = z
  .object({
    jurisdiction: text,
    activity: text.nullable(),
    status: z.enum(['unreviewed', 'researching', 'partial', 'verified']),
    sourceIds: z.array(id),
    reviewedAt: date.nullable(),
    note: text,
  })
  .strict();
export const requirementSchema = z
  .object({
    id,
    name: text,
    aliases: z.array(text),
    type: z.enum(requirementTypes),
    jurisdictions: z.array(text).min(1),
    activities: z.array(text),
    crossSector: z.boolean(),
    authority: text,
    summary: text,
    status: z.enum(['draft', 'verified', 'withdrawn', 'superseded']),
    currentStatus: text,
    canonicalPath: z.string().regex(/^\/[a-z0-9/-]+$/),
    sourceIds: z.array(id).min(1),
    applicationUrl: officialUrl,
    applicability: text.nullable(),
    exemptions: text.nullable(),
    application: text.nullable(),
    renewal: text.nullable(),
    fees: text.nullable(),
    documents: z.array(z.object({ text, sourceId: id }).strict()),
    version: text.nullable(),
    effectiveDate: date.nullable(),
    reviewedAt: date.nullable(),
    nextReviewAt: date,
    updatedAt: date,
    publishedAt: date,
    review: z
      .object({
        reviewer: text,
        scope: text,
        authority: z.literal(true),
        applicability: z.literal(true),
        currentStatus: z.literal(true),
        sources: z.literal(true),
        substantiveContent: z.literal(true),
      })
      .strict()
      .nullable(),
    quickTrustSupport: z.enum(['educational', 'confirmed']),
    servicePath: z.string().nullable(),
    replacementId: id.optional(),
    changes: z
      .array(z.object({ date, summary: text, sourceIds: z.array(id).min(1) }).strict())
      .min(1),
    upcoming: z.array(z.object({ date, summary: text, sourceId: id }).strict()),
  })
  .strict();

export type Requirement = z.infer<typeof requirementSchema>;
export type Source = z.infer<typeof sourceSchema>;
export type Jurisdiction = z.infer<typeof jurisdictionSchema>;
export type Industry = z.infer<typeof industrySchema>;
export type Coverage = z.infer<typeof coverageSchema>;
export type Directory = {
  requirements: Requirement[];
  sources: Source[];
  jurisdictions: Jurisdiction[];
  industries: Industry[];
  coverage: Coverage[];
  content: Record<string, string>;
};

export function today(): string {
  return new Date().toISOString().slice(0, 10);
}
export function isVerified(record: Requirement, asOf = today()): boolean {
  return (
    record.status === 'verified' &&
    record.review !== null &&
    record.reviewedAt !== null &&
    record.reviewedAt <= asOf &&
    record.nextReviewAt >= asOf
  );
}

/** Strict content gate shared by build validation, sitemap and checklist generation. */
export function validateDirectory(input: Directory): Directory {
  const d: Directory = {
    requirements: z.array(requirementSchema).parse(input.requirements),
    sources: z.array(sourceSchema).parse(input.sources),
    jurisdictions: z.array(jurisdictionSchema).parse(input.jurisdictions),
    industries: z.array(industrySchema).parse(input.industries),
    coverage: z.array(coverageSchema).parse(input.coverage),
    content: input.content,
  };
  const assert = (ok: unknown, message: string) => {
    if (!ok) throw new Error(`Directory: ${message}`);
  };
  const unique = (rows: { id: string }[], name: string) => {
    const ids = new Set(rows.map((r) => r.id));
    assert(ids.size === rows.length, `duplicate ${name} ID`);
    return ids;
  };
  const reqIds = unique(d.requirements, 'requirement'),
    sourceIds = unique(d.sources, 'source');
  const geoIds = unique(d.jurisdictions, 'jurisdiction'),
    industryIds = unique(d.industries, 'industry');
  const references = (ids: string[], known: Set<string>, context: string) =>
    ids.forEach((value) => assert(known.has(value), `${context}: unknown ${value}`));
  const hierarchy = (rows: { id: string; parent: string | null }[], ids: Set<string>) =>
    rows.forEach((row) => {
      const visited = new Set([row.id]);
      let parent = row.parent;
      while (parent) {
        assert(
          ids.has(parent) && !visited.has(parent),
          `invalid hierarchy for ${row.id}: ${parent}`,
        );
        visited.add(parent);
        parent = rows.find((r) => r.id === parent)!.parent;
      }
    });
  hierarchy(d.jurisdictions, geoIds);
  hierarchy(d.industries, industryIds);
  d.jurisdictions.forEach((r) => {
    references([r.sourceId], sourceIds, r.id);
    references(r.members ?? [], geoIds, r.id);
  });
  const canonical = new Set<string>();
  for (const r of d.requirements) {
    references(r.jurisdictions, geoIds, r.id);
    references(r.activities, industryIds, r.id);
    references(
      [
        ...r.sourceIds,
        ...r.documents.map((x) => x.sourceId),
        ...r.changes.flatMap((x) => x.sourceIds),
        ...r.upcoming.map((x) => x.sourceId),
      ],
      sourceIds,
      r.id,
    );
    assert(!canonical.has(r.canonicalPath), `duplicate canonical ${r.canonicalPath}`);
    canonical.add(r.canonicalPath);
    assert(
      !r.canonicalPath.endsWith('/') && !r.canonicalPath.includes('//'),
      `invalid canonical ${r.id}`,
    );
    if (r.canonicalPath.startsWith('/compliance-directory/'))
      assert(
        r.canonicalPath === `/compliance-directory/requirements/${r.id}`,
        `canonical mismatch ${r.id}`,
      );
    assert(
      r.crossSector ? r.activities.length === 0 : r.activities.length > 0,
      `activity scope ${r.id}`,
    );
    assert(r.updatedAt <= today(), `future modification ${r.id}`);
    assert(r.publishedAt <= r.updatedAt, `publication after modification ${r.id}`);
    assert(
      r.quickTrustSupport !== 'confirmed' || r.servicePath === r.canonicalPath,
      `service evidence missing ${r.id}`,
    );
    assert(
      r.quickTrustSupport !== 'educational' || r.servicePath === null,
      `educational service claim ${r.id}`,
    );
    if (r.replacementId) {
      references([r.replacementId], reqIds, r.id);
      assert(r.replacementId !== r.id, `self replacement ${r.id}`);
    }
    assert(r.status !== 'superseded' || r.replacementId, `replacement missing ${r.id}`);
    if (r.status === 'verified') {
      assert(
        r.review && r.reviewedAt && r.reviewedAt <= today() && r.nextReviewAt > r.reviewedAt,
        `review missing or invalid ${r.id}`,
      );
      assert(
        r.applicability &&
          r.exemptions &&
          r.application &&
          r.renewal &&
          r.currentStatus !== 'Not yet verified',
        `substantive fields missing ${r.id}`,
      );
      assert(
        r.sourceIds.every((sid) => {
          const s = d.sources.find((x) => x.id === sid)!;
          return s.reviewedAt && s.reviewedAt <= r.reviewedAt! && s.checkedAt;
        }),
        `unreviewed source ${r.id}`,
      );
      assert(
        (d.content[r.id] ?? '').split(/\s+/).length >= 120,
        `substantive article missing ${r.id}`,
      );
      assert(r.documents.length > 0, `source-linked checklist missing ${r.id}`);
    }
  }
  const coverageKeys = new Set<string>();
  for (const c of d.coverage) {
    const key = `${c.jurisdiction}:${c.activity ?? '*'}`;
    assert(!coverageKeys.has(key), `duplicate coverage ${key}`);
    coverageKeys.add(key);
    references([c.jurisdiction], geoIds, key);
    if (c.activity) references([c.activity], industryIds, key);
    references(c.sourceIds, sourceIds, key);
    assert(
      c.status !== 'verified' || (c.reviewedAt && c.sourceIds.length),
      `coverage review missing ${key}`,
    );
  }
  return d;
}
