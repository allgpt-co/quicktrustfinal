"""Normalize scanner findings into a unified format."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field

logger = logging.getLogger(__name__)

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


@dataclass(frozen=True)
class NormalizedFinding:
    """Unified finding format across all scanners."""

    title: str
    severity: str  # critical, high, medium, low, info
    scanner: str
    category: str  # vulnerability, misconfiguration, secret, code_quality
    cve: str | None = None
    file_path: str | None = None
    line_number: int | None = None
    description: str = ""
    remediation: str | None = None
    raw_data: dict = field(default_factory=dict)


def _normalize_severity(raw: str | None) -> str:
    """Normalize severity string to one of the standard levels."""
    if not raw:
        return "info"
    lower = raw.lower().strip()
    mapping = {
        "critical": "critical",
        "crit": "critical",
        "high": "high",
        "medium": "medium",
        "med": "medium",
        "moderate": "medium",
        "low": "low",
        "info": "info",
        "informational": "info",
        "negligible": "info",
        "unknown": "info",
    }
    return mapping.get(lower, "info")


def normalize_trivy(raw_finding: dict) -> dict:
    """Normalize a Trivy vulnerability finding."""
    finding = NormalizedFinding(
        title=raw_finding.get("VulnerabilityID", raw_finding.get("Title", "Unknown")),
        severity=_normalize_severity(raw_finding.get("Severity")),
        scanner="trivy",
        category="vulnerability",
        cve=raw_finding.get("VulnerabilityID"),
        file_path=raw_finding.get("Target"),
        line_number=None,
        description=raw_finding.get("Description", ""),
        remediation=raw_finding.get("FixedVersion", raw_finding.get("Resolution")),
        raw_data=raw_finding,
    )
    return asdict(finding)


def normalize_semgrep(raw_finding: dict) -> dict:
    """Normalize a Semgrep SAST finding."""
    extra = raw_finding.get("extra", {})
    finding = NormalizedFinding(
        title=raw_finding.get("check_id", "Unknown rule"),
        severity=_normalize_severity(extra.get("severity")),
        scanner="semgrep",
        category="code_quality",
        cve=None,
        file_path=raw_finding.get("path"),
        line_number=raw_finding.get("start", {}).get("line"),
        description=extra.get("message", ""),
        remediation=extra.get("fix"),
        raw_data=raw_finding,
    )
    return asdict(finding)


def normalize_gitleaks(raw_finding: dict) -> dict:
    """Normalize a Gitleaks secret detection finding."""
    finding = NormalizedFinding(
        title=raw_finding.get("Description", raw_finding.get("RuleID", "Secret found")),
        severity="high",  # secrets are always high severity
        scanner="gitleaks",
        category="secret",
        cve=None,
        file_path=raw_finding.get("File"),
        line_number=raw_finding.get("StartLine"),
        description=f"Secret detected: {raw_finding.get('RuleID', 'unknown rule')}",
        remediation="Rotate the exposed credential and remove it from the codebase.",
        raw_data=raw_finding,
    )
    return asdict(finding)


def normalize_checkov(raw_finding: dict) -> dict:
    """Normalize a Checkov IaC misconfiguration finding."""
    severity_map = {"CRITICAL": "critical", "HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
    raw_sev = raw_finding.get("severity", "MEDIUM")
    finding = NormalizedFinding(
        title=raw_finding.get("check_id", raw_finding.get("name", "Unknown check")),
        severity=severity_map.get(raw_sev.upper(), "medium") if raw_sev else "medium",
        scanner="checkov",
        category="misconfiguration",
        cve=None,
        file_path=raw_finding.get("file_path"),
        line_number=raw_finding.get("file_line_range", [None])[0],
        description=raw_finding.get("name", raw_finding.get("check_id", "")),
        remediation=raw_finding.get("guideline"),
        raw_data=raw_finding,
    )
    return asdict(finding)


def normalize_nuclei(raw_finding: dict) -> dict:
    """Normalize a Nuclei template-based finding."""
    info = raw_finding.get("info", {})
    finding = NormalizedFinding(
        title=info.get("name", raw_finding.get("template-id", "Unknown")),
        severity=_normalize_severity(info.get("severity")),
        scanner="nuclei",
        category="vulnerability",
        cve=None,
        file_path=raw_finding.get("matched-at"),
        line_number=None,
        description=info.get("description", ""),
        remediation=info.get("remediation"),
        raw_data=raw_finding,
    )
    return asdict(finding)


def normalize_zap(raw_finding: dict) -> dict:
    """Normalize a ZAP DAST finding."""
    risk_map = {"3": "high", "2": "medium", "1": "low", "0": "info"}
    finding = NormalizedFinding(
        title=raw_finding.get("alert", raw_finding.get("name", "Unknown")),
        severity=risk_map.get(str(raw_finding.get("riskcode", "0")), "info"),
        scanner="zap",
        category="vulnerability",
        cve=raw_finding.get("cweid"),
        file_path=raw_finding.get("url"),
        line_number=None,
        description=raw_finding.get("desc", raw_finding.get("description", "")),
        remediation=raw_finding.get("solution"),
        raw_data=raw_finding,
    )
    return asdict(finding)


def normalize_prowler(raw_finding: dict) -> dict:
    """Normalize a Prowler cloud security finding."""
    finding = NormalizedFinding(
        title=raw_finding.get("CheckTitle", raw_finding.get("CheckID", "Unknown")),
        severity=_normalize_severity(raw_finding.get("Severity")),
        scanner="prowler",
        category="misconfiguration",
        cve=None,
        file_path=raw_finding.get("ResourceArn", raw_finding.get("ResourceId")),
        line_number=None,
        description=raw_finding.get("StatusExtended", raw_finding.get("Description", "")),
        remediation=raw_finding.get("Remediation", {}).get("Recommendation", {}).get("Text")
        if isinstance(raw_finding.get("Remediation"), dict)
        else None,
        raw_data=raw_finding,
    )
    return asdict(finding)


def _normalize_generic(raw_finding: dict) -> dict:
    """Generic normalizer for unknown scanner types."""
    finding = NormalizedFinding(
        title=raw_finding.get("title", raw_finding.get("name", "Unknown finding")),
        severity=_normalize_severity(raw_finding.get("severity")),
        scanner=raw_finding.get("scanner", "unknown"),
        category=raw_finding.get("category", "vulnerability"),
        cve=raw_finding.get("cve"),
        file_path=raw_finding.get("file_path", raw_finding.get("location")),
        line_number=raw_finding.get("line_number"),
        description=raw_finding.get("description", ""),
        remediation=raw_finding.get("remediation"),
        raw_data=raw_finding,
    )
    return asdict(finding)


_NORMALIZERS = {
    "trivy": normalize_trivy,
    "semgrep": normalize_semgrep,
    "gitleaks": normalize_gitleaks,
    "checkov": normalize_checkov,
    "nuclei": normalize_nuclei,
    "zap": normalize_zap,
    "prowler": normalize_prowler,
}


def normalize_finding(scanner: str, raw_finding: dict) -> dict:
    """Route to the correct normalizer based on scanner name."""
    normalizer = _NORMALIZERS.get(scanner.lower(), _normalize_generic)
    return normalizer(raw_finding)
