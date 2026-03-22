"""Data classification framework.

Every piece of data (evidence, policies, reports, vendor docs) is tagged with
a classification level.  Access is restricted based on the user's role.

Levels (ISO 27001 A.5.12):
    PUBLIC       — Anyone can access (trust center docs, published policies)
    INTERNAL     — All authenticated org members
    CONFIDENTIAL — Managers and above (default for most GRC data)
    RESTRICTED   — Admins only (credentials, PII, audit findings)
"""

from __future__ import annotations

from enum import Enum

# Classification levels ordered from least to most sensitive
CLASSIFICATION_LEVELS = ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]


class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


# Roles that can access each classification level
CLASSIFICATION_ACCESS: dict[str, list[str]] = {
    "PUBLIC": [
        "super_admin", "executive", "compliance_manager",
        "control_owner", "employee", "auditor_internal", "auditor_external",
    ],
    "INTERNAL": [
        "super_admin", "executive", "compliance_manager",
        "control_owner", "employee", "auditor_internal",
    ],
    "CONFIDENTIAL": [
        "super_admin", "executive", "compliance_manager", "auditor_internal",
    ],
    "RESTRICTED": [
        "super_admin",
    ],
}


def can_access_classification(user_role: str, classification: str) -> bool:
    """Check if a user role is allowed to access a given classification level."""
    allowed = CLASSIFICATION_ACCESS.get(classification, [])
    return user_role in allowed


def get_max_classification(user_role: str) -> str:
    """Return the highest classification level a role can access."""
    for level in reversed(CLASSIFICATION_LEVELS):
        if can_access_classification(user_role, level):
            return level
    return "PUBLIC"


def require_classification(user_role: str, classification: str) -> None:
    """Raise ValueError if the user cannot access the classification level."""
    if not can_access_classification(user_role, classification):
        raise ValueError(
            f"Role '{user_role}' cannot access {classification} data. "
            f"Minimum required: {CLASSIFICATION_ACCESS.get(classification, ['super_admin'])}"
        )
