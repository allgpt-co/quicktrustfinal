"""Base scanner interface that all scanners implement."""
import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

logger = logging.getLogger(__name__)


class ScanOutput:
    """Standardised output from any scanner."""

    def __init__(self):
        self.findings: list[dict] = []
        self.error: str | None = None
        self.raw_output: str | None = None
        self.duration_seconds: float = 0.0

    def add_finding(
        self,
        severity: str,
        title: str,
        description: str | None = None,
        location: str | None = None,
        line_number: int | None = None,
        rule_id: str | None = None,
        cve_id: str | None = None,
        cwe_id: str | None = None,
        remediation: str | None = None,
        package_name: str | None = None,
        package_version: str | None = None,
        fixed_version: str | None = None,
        confidence: str | None = None,
        metadata: dict | None = None,
    ):
        self.findings.append({
            "severity": severity.lower(),
            "title": title,
            "description": description,
            "location": location,
            "line_number": line_number,
            "rule_id": rule_id,
            "cve_id": cve_id,
            "cwe_id": cwe_id,
            "remediation": remediation,
            "package_name": package_name,
            "package_version": package_version,
            "fixed_version": fixed_version,
            "confidence": confidence,
            "metadata": metadata or {},
        })

    @property
    def severity_counts(self) -> dict[str, int]:
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in self.findings:
            sev = f["severity"]
            if sev in counts:
                counts[sev] += 1
        return counts


class BaseScanner(ABC):
    """Abstract base class for all security scanners."""

    name: str = "base"
    scan_type: str = "generic"

    @abstractmethod
    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Execute the scan against the target and return findings."""
        ...

    async def _run_command(
        self, cmd: list[str], timeout: int = 300
    ) -> tuple[str, str, int]:
        """Run a shell command asynchronously with timeout."""
        logger.info("[%s] Running: %s", self.name, " ".join(cmd))
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout
            )
            return (
                stdout.decode(errors="replace"),
                stderr.decode(errors="replace"),
                proc.returncode or 0,
            )
        except asyncio.TimeoutError:
            proc.kill()  # type: ignore[union-attr]
            return "", f"Command timed out after {timeout}s", -1
        except FileNotFoundError:
            return "", f"Command not found: {cmd[0]}", -1

    def _parse_json_output(self, raw: str) -> Any:
        """Safely parse JSON output from scanner."""
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("[%s] Failed to parse JSON output", self.name)
            return None
