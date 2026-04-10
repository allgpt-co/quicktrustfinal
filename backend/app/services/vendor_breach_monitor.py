"""Vendor breach monitoring — checks for known breaches of vendors."""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vendor import Vendor

# Seeded known breaches (in production, would query HIBP or similar API)
KNOWN_BREACHES: list[dict] = [
    {
        "vendor": "AT&T",
        "date": "2024-03-30",
        "description": "73M customer records exposed",
        "severity": "critical",
    },
    {
        "vendor": "Ticketmaster",
        "date": "2024-05-28",
        "description": "560M users affected via Snowflake incident",
        "severity": "critical",
    },
    {
        "vendor": "Change Healthcare",
        "date": "2024-02-21",
        "description": "Healthcare data breach affecting millions",
        "severity": "critical",
    },
    {
        "vendor": "Snowflake",
        "date": "2024-05-15",
        "description": "Customer environment compromises via stolen credentials",
        "severity": "high",
    },
    {
        "vendor": "MOVEit",
        "date": "2023-05-31",
        "description": "SQL injection affecting thousands of organizations",
        "severity": "high",
    },
    {
        "vendor": "LastPass",
        "date": "2022-12-22",
        "description": "Password vault data accessed by attackers",
        "severity": "critical",
    },
    {
        "vendor": "Okta",
        "date": "2023-10-20",
        "description": "Support case management system breach",
        "severity": "high",
    },
    {
        "vendor": "CircleCI",
        "date": "2023-01-04",
        "description": "Customer secrets exposed via engineer laptop compromise",
        "severity": "high",
    },
    {
        "vendor": "GitHub",
        "date": "2022-12-19",
        "description": "Code signing certificates exfiltrated",
        "severity": "medium",
    },
    {
        "vendor": "Mailchimp",
        "date": "2023-01-18",
        "description": "Social engineering attack exposed customer data",
        "severity": "high",
    },
    {
        "vendor": "Twilio",
        "date": "2022-08-07",
        "description": "Phishing attack on employees",
        "severity": "high",
    },
    {
        "vendor": "Cloudflare",
        "date": "2023-11-23",
        "description": "Okta-related incident exposed internal systems",
        "severity": "medium",
    },
]


async def check_vendor_breaches(db: AsyncSession, org_id: UUID) -> list[dict]:
    """Check if any of the org's vendors have known breaches.

    Returns a list of alerts, each matching a vendor to a known breach record.
    """
    result = await db.execute(
        select(Vendor).where(
            Vendor.org_id == org_id,
            Vendor.deleted_at.is_(None),
        )
    )
    vendors = list(result.scalars().all())

    alerts: list[dict] = []
    for vendor in vendors:
        name_lower = vendor.name.lower()
        for breach in KNOWN_BREACHES:
            breach_name_lower = breach["vendor"].lower()
            if breach_name_lower in name_lower or name_lower in breach_name_lower:
                alerts.append(
                    {
                        "vendor_id": str(vendor.id),
                        "vendor_name": vendor.name,
                        "breach": breach,
                    }
                )
                break  # one match per vendor
    return alerts
