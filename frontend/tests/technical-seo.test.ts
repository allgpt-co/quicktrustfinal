// @vitest-environment node
import { describe, expect, test } from 'vitest';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { serializeJsonLd } from '@/components/marketing/schema/jsonLd';
import { organizationSchema } from '@/components/marketing/schema/OrganizationSchema';
import ServicePageSchema from '@/components/marketing/schema/ServicePageSchema';
import PageBreadcrumbSchema from '@/components/marketing/schema/PageBreadcrumbSchema';
import sitemap from '@/app/sitemap';
import { metadata as privacyMetadata } from '@/app/(marketing)/privacy-policy/page';
import { metadata as termsMetadata } from '@/app/(marketing)/terms-of-service/page';
import { metadata as homepageMetadata } from '@/app/(marketing)/page';

describe('technical SEO safeguards', () => {
  test('escapes script-significant JSON-LD characters while preserving JSON values', () => {
    const value = { answer: '</script><script>alert("x")</script>', ampersand: '&' };
    const serialized = serializeJsonLd(value);

    expect(serialized).not.toContain('</script>');
    expect(serialized).toContain('\\u003c/script\\u003e');
    expect(serialized).toContain('\\u0026');
    expect(JSON.parse(serialized)).toEqual(value);
  });

  test('organization markup contains only verified contact and identity fields', () => {
    expect(organizationSchema.contactPoint).toEqual({
      '@type': 'ContactPoint',
      email: 'hello@quicktrust.io',
      contactType: 'sales',
    });
    expect(organizationSchema).not.toHaveProperty('telephone');
    expect(organizationSchema).not.toHaveProperty('sameAs');
    expect(organizationSchema).not.toHaveProperty('foundingDate');
  });

  test('framework and solution schema components emit service and breadcrumb markup', () => {
    const html = renderToStaticMarkup(
      React.createElement(
        React.Fragment,
        null,
        React.createElement(ServicePageSchema, {
          name: 'SOC 2 Compliance Implementation',
          description: 'Engineer-led SOC 2 readiness.',
          url: 'https://quicktrustapp.com/soc-2-compliance',
          serviceType: 'SOC 2 compliance implementation',
        }),
        React.createElement(PageBreadcrumbSchema, {
          items: [
            { name: 'Home', item: 'https://quicktrustapp.com' },
            { name: 'SOC 2 Compliance', item: 'https://quicktrustapp.com/soc-2-compliance' },
          ],
        }),
      ),
    );

    expect(html).toContain('"@type":"Service"');
    expect(html).toContain('"@type":"BreadcrumbList"');
    expect(html).toContain('soc-2-compliance');
  });

  test('sitemap keeps downloads out and only emits known, non-future article dates', () => {
    const entries = sitemap();
    const urls = entries.map((entry) => entry.url);
    expect(urls.some((url) => new URL(url).pathname.startsWith('/resources/'))).toBe(false);
    for (const entry of entries) {
      const pathname = new URL(entry.url).pathname;
      if (pathname.startsWith('/blog/') && entry.lastModified) {
        expect(new Date(entry.lastModified).getTime()).toBeLessThanOrEqual(Date.now());
      }
    }
  });

  test('legal pages advertise their noindex status and homepage owns one brand suffix', () => {
    expect(privacyMetadata.robots).toMatchObject({ index: false, follow: true });
    expect(termsMetadata.robots).toMatchObject({ index: false, follow: true });
    expect(homepageMetadata.title).toBe('Compliance Automation Platform');
  });
});
