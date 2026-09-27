// @vitest-environment node
import { afterAll, describe, expect, test, vi } from 'vitest';
import {
  getDirectory,
  getCatalogue,
  getImports,
  checklistText,
  directorySitemapEntries,
} from '@/lib/compliance-directory';
import { isVerified, validateDirectory } from '@/lib/directory-model';
import { ancestors, coverageFor, filterRequirements } from '@/lib/directory-search';
import { sitemapIndexXml, sitemapPageXml } from '@/lib/directory-sitemap';
import { generateMetadata } from '@/app/(marketing)/compliance-directory/[[...segments]]/page';
import { GET as checklist } from '@/app/compliance-directory/checklists/[id]/route';
import sitemap from '@/app/sitemap';
import { isMarketingPath } from '@/lib/marketing-routes';

vi.useFakeTimers();
vi.setSystemTime(new Date('2026-09-27T12:00:00Z'));
afterAll(() => vi.useRealTimers());
const d = getDirectory();
const fixture = () => JSON.parse(JSON.stringify(d)) as typeof d;
describe('global directory publication controls', () => {
  test('reference imports reconcile to their recorded denominators and valid hierarchies', () => {
    expect(d.jurisdictions.filter((j) => j.kind === 'country')).toHaveLength(249);
    expect(d.jurisdictions.filter((j) => j.kind === 'subdivision')).toHaveLength(5046);
    expect(d.industries).toHaveLength(getImports().find((x) => x.dataset.includes('ISIC'))!.count);
    expect(getCatalogue()).toHaveLength(452);
    expect(ancestors('US-NY-NYC', d.jurisdictions)).toEqual(['US-NY-NYC', 'US-NY', 'US']);
    expect(
      d.industries
        .filter((i) => i.level === 'class')
        .every((i) => ancestors(i.id, d.industries).length === 4),
    ).toBe(true);
  });
  test('unknown coverage never means no obligations', () => {
    expect(coverageFor(d, 'JP', '0111')).toMatchObject({ status: 'unreviewed', reviewedAt: null });
    expect(coverageFor(d, 'JP', '0111').note).toContain('does not mean no obligations');
    expect(filterRequirements(d, { query: 'unrecorded-activity-with-no-matches' })).toEqual([]);
  });
  test('finder includes parent rules, local candidates, international standards and EU markets', () => {
    const ids = (location: string, market?: string, activity?: string) =>
      filterRequirements(d, { location, market, activity }).map((r) => r.id);
    expect(ids('US-NY-NYC', undefined, 'I')).toContain('nyc-food-service');
    expect(ids('US-NY-NYC')).toContain('us-osha');
    expect(ids('US')).toContain('california-contractor');
    expect(ids('FR')).toContain('gdpr');
    expect(ids('US', 'DE')).toContain('dora');
    expect(ids('SG', undefined, 'I')).toContain('iso-9001');
    expect(ids('SG', undefined, 'I')).not.toContain('mas-payment-services');
  });
  test('only current reviewed pages enter the directory sitemap; existing SEO is preserved', () => {
    const entries = directorySitemapEntries('2026-09-27');
    expect(entries).toHaveLength(4);
    expect(entries.some((x) => x.path.endsWith('/iso-9001'))).toBe(true);
    expect(
      entries.some(
        (x) =>
          x.path.includes('jurisdictions') ||
          x.path.includes('finder') ||
          x.path.endsWith('/fssai') ||
          x.path.endsWith('/iso-9001-2015'),
      ),
    ).toBe(false);
    expect(directorySitemapEntries('2027-01-01')).toHaveLength(2);
    expect(sitemap()).toHaveLength(197);
    expect(sitemapIndexXml()).toContain('/sitemaps/0.xml');
    expect(sitemapPageXml(0, '2026-09-27')).toContain('<lastmod>2026-09-27</lastmod>');
    expect(sitemapPageXml(1)).toBeNull();
  });
  test('draft hubs and records are noindex; verified overviews have self canonicals', async () => {
    for (const segments of [
      ['jurisdictions', 'us'],
      ['industries', 'a'],
      ['requirements', 'fssai'],
      ['requirements', 'iso-9001-2015'],
    ]) {
      expect(
        (await generateMetadata({ params: Promise.resolve({ segments }) })).robots,
      ).toMatchObject({ index: false, follow: true });
    }
    const meta = await generateMetadata({
      params: Promise.resolve({ segments: ['requirements', 'iso-9001'] }),
    });
    expect(meta.robots).toMatchObject({ index: true, follow: true });
    expect(meta.alternates?.canonical).toBe(
      'https://quicktrustapp.com/compliance-directory/requirements/iso-9001',
    );
    expect(d.requirements.find((r) => r.id === 'soc-2')!.canonicalPath).toBe('/soc-2-compliance');
    expect(d.requirements.find((r) => r.id === 'nist-csf')!.canonicalPath).toBe(
      '/blog/pillar-nist-cybersecurity-framework-guide',
    );
    expect(d.requirements.find((r) => r.id === 'gdpr')!.canonicalPath).toBe(
      '/blog/gdpr-compliance-us-saas-guide',
    );
  });
  test('source-linked downloads require current verification and identify their review scope', async () => {
    const r = d.requirements.find((r) => r.id === 'iso-9001')!;
    expect(checklistText(r, '2026-09-27')).toContain('Reviewed: 2026-09-27');
    expect(checklistText(r, '2026-09-27')).toContain('https://www.iso.org/');
    expect(checklistText(r, '2027-01-01')).toBeNull();
    for (const [id, status] of [
      ['iso-9001', 200],
      ['fssai', 409],
      ['iso-9001-2015', 409],
      ['unknown', 404],
    ] as const) {
      const response = await checklist(new Request('https://quicktrustapp.com/'), {
        params: Promise.resolve({ id }),
      });
      expect(response.status).toBe(status);
      expect(response.headers.get('x-robots-tag')).toContain('noindex');
    }
  });
  test('promotion rejects missing review, unreviewed sources and missing substantive content', () => {
    const x = fixture(),
      r = x.requirements.find((r) => r.id === 'fssai')!;
    r.status = 'verified';
    expect(() => validateDirectory(x)).toThrow(/review missing/);
    const y = fixture();
    y.sources.find((s) => s.id === 'iso-9001-official')!.reviewedAt = null;
    expect(() => validateDirectory(y)).toThrow(/unreviewed source/);
    const checklistSource = fixture();
    checklistSource.requirements.find((r) => r.id === 'iso-9001')!.documents[0].sourceId =
      'fssai-official';
    expect(() => validateDirectory(checklistSource)).toThrow(/unreviewed source/);
    const z = fixture();
    delete z.content['iso-9001'];
    expect(() => validateDirectory(z)).toThrow(/substantive article/);
  });
  test('withdrawal stops indexing eligibility and replacements must exist', () => {
    const x = fixture(),
      r = x.requirements.find((r) => r.id === 'iso-9001')!;
    r.status = 'withdrawn';
    expect(isVerified(r)).toBe(false);
    r.status = 'superseded';
    r.replacementId = 'missing';
    expect(() => validateDirectory(x)).toThrow(/unknown missing/);
  });
  test('invalid IDs, sources, geography, activities and duplicate canonicals fail validation', () => {
    for (const mutate of [
      (x: typeof d) => {
        x.requirements[0].jurisdictions = ['nonexistent'];
      },
      (x: typeof d) => {
        x.requirements[0].activities = ['99999'];
      },
      (x: typeof d) => {
        x.requirements[0].sourceIds = ['missing-source'];
      },
      (x: typeof d) => {
        x.requirements[0].canonicalPath = x.requirements[1].canonicalPath;
      },
      (x: typeof d) => {
        x.jurisdictions[0].parent = x.jurisdictions[0].id;
      },
    ]) {
      const x = fixture();
      mutate(x);
      expect(() => validateDirectory(x)).toThrow();
    }
  });
  test('only the dedicated directory namespace is public; application frameworks remain protected', () => {
    expect(isMarketingPath('/compliance-directory/jurisdictions/us')).toBe(true);
    for (const path of [
      '/frameworks',
      '/frameworks/iso-9001',
      '/compliance-directory-private',
      '/settings/integrations',
      '/integrations/private',
    ])
      expect(isMarketingPath(path)).toBe(false);
  });
});
