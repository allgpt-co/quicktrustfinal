import { ImageResponse } from 'next/og';

export const runtime = 'edge';

const OG_CONFIG: Record<string, { title: string; subtitle: string }> = {
  home: {
    title: 'QuickTrust',
    subtitle: 'Compliance Automation Platform',
  },
  soc2: {
    title: 'SOC 2 Compliance',
    subtitle: 'Get Audit-Ready in Weeks',
  },
  iso27001: {
    title: 'ISO 27001 Certification',
    subtitle: 'Fast-Track Your Implementation',
  },
  hipaa: {
    title: 'HIPAA Compliance',
    subtitle: 'For Healthcare Technology',
  },
  'vs-vanta': {
    title: 'QuickTrust vs Vanta',
    subtitle: 'Compliance Platform Comparison',
  },
  'vs-drata': {
    title: 'QuickTrust vs Drata',
    subtitle: 'Compliance Platform Comparison',
  },
  'vs-secureframe': {
    title: 'QuickTrust vs Secureframe',
    subtitle: 'Compliance Platform Comparison',
  },
  'vs-sprinto': {
    title: 'QuickTrust vs Sprinto',
    subtitle: 'Compliance Platform Comparison',
  },
  'vs-thoropass': {
    title: 'QuickTrust vs Thoropass',
    subtitle: 'Compliance Platform Comparison',
  },
  pricing: {
    title: 'Pricing',
    subtitle: 'Transparent Compliance Packages',
  },
  about: {
    title: 'About QuickTrust',
    subtitle: 'Platform + Engineers',
  },
  blog: {
    title: 'Compliance Blog',
    subtitle: 'Guides, Checklists & Best Practices',
  },
  questionnaire: {
    title: 'Security Questionnaire',
    subtitle: 'Automation',
  },
  contact: {
    title: 'Contact Us',
    subtitle: 'Get a Free Readiness Snapshot',
  },
};

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params;
  const config = OG_CONFIG[slug] || {
    title: 'QuickTrust',
    subtitle: 'Compliance Automation Platform',
  };

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: '60px 80px',
          background: 'linear-gradient(135deg, #111827 0%, #1f2937 100%)',
          color: 'white',
          fontFamily: 'system-ui, -apple-system, sans-serif',
        }}
      >
        {/* Logo area */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '40px',
          }}
        >
          <div
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'white',
              marginRight: '16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#111827',
              fontWeight: 900,
              fontSize: '24px',
            }}
          >
            QT
          </div>
          <span style={{ fontSize: '24px', fontWeight: 600, opacity: 0.8 }}>
            quicktrustapp.com
          </span>
        </div>

        {/* Title */}
        <div
          style={{
            fontSize: '64px',
            fontWeight: 800,
            lineHeight: 1.1,
            marginBottom: '16px',
            maxWidth: '900px',
          }}
        >
          {config.title}
        </div>

        {/* Subtitle */}
        <div
          style={{
            fontSize: '32px',
            fontWeight: 400,
            opacity: 0.7,
            maxWidth: '800px',
          }}
        >
          {config.subtitle}
        </div>

        {/* Bottom bar */}
        <div
          style={{
            position: 'absolute',
            bottom: '60px',
            left: '80px',
            right: '80px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderTop: '1px solid rgba(255,255,255,0.2)',
            paddingTop: '24px',
          }}
        >
          <span style={{ fontSize: '18px', opacity: 0.6 }}>
            Platform + Engineers
          </span>
          <span style={{ fontSize: '18px', opacity: 0.6 }}>
            SOC 2 | ISO 27001 | HIPAA | PCI DSS
          </span>
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
