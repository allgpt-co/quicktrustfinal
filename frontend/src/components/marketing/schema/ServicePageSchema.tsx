import { serializeJsonLd } from './jsonLd';

interface ServicePageSchemaProps {
  name: string;
  description: string;
  url: string;
  serviceType: string;
}

/** Service markup for an individual framework or solution landing page. */
export default function ServicePageSchema({
  name,
  description,
  url,
  serviceType,
}: ServicePageSchemaProps) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    '@id': `${url}#service`,
    name,
    description,
    url,
    serviceType,
    provider: { '@id': 'https://quicktrustapp.com/#organization' },
    areaServed: { '@type': 'Country', name: 'United States' },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: serializeJsonLd(schema) }}
    />
  );
}
