"""Trivy container vulnerability scanner."""
import logging
import time

from app.scanners.base import BaseScanner, ScanOutput

logger = logging.getLogger(__name__)

# Trivy severity mapping
TRIVY_SEVERITY_MAP = {
    "CRITICAL": "critical",
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low",
    "UNKNOWN": "info",
}


class TrivyScanner(BaseScanner):
    name = "trivy"
    scan_type = "container"

    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Scan for vulnerabilities using Trivy.

        Target can be:
        - A directory path (e.g. '/app') → uses 'trivy fs'
        - A Docker image name (e.g. 'python:3.11-slim') → uses 'trivy image'
        """
        output = ScanOutput()
        config = config or {}
        start = time.time()

        severity = config.get("severity", "CRITICAL,HIGH,MEDIUM,LOW")
        timeout_secs = config.get("timeout", 300)

        # Auto-detect scan mode: use 'rootfs' for paths, 'image' for Docker images
        scan_mode = config.get("mode", "auto")
        if scan_mode == "auto":
            scan_mode = "rootfs" if target.startswith("/") else "image"

        cmd = [
            "trivy", scan_mode,
            "--format", "json",
            "--severity", severity,
            "--no-progress",
            "--exit-code", "0",
            target,
        ]

        stdout, stderr, returncode = await self._run_command(cmd, timeout=timeout_secs)
        output.duration_seconds = time.time() - start
        output.raw_output = stdout[:50000]  # Cap stored output

        if returncode == -1:
            output.error = stderr
            return output

        data = self._parse_json_output(stdout)
        if not data:
            output.error = stderr or "Failed to parse Trivy output"
            return output

        # Parse Trivy JSON output
        results = data.get("Results") or []
        for result in results:
            target_name = result.get("Target", "")
            vulns = result.get("Vulnerabilities") or []
            for vuln in vulns:
                sev = TRIVY_SEVERITY_MAP.get(vuln.get("Severity", ""), "info")
                output.add_finding(
                    severity=sev,
                    title=f"{vuln.get('VulnerabilityID', 'Unknown')} in {vuln.get('PkgName', 'unknown')}",
                    description=vuln.get("Description", "")[:2000],
                    location=target_name,
                    rule_id=vuln.get("VulnerabilityID"),
                    cve_id=vuln.get("VulnerabilityID"),
                    remediation=f"Upgrade {vuln.get('PkgName')} to {vuln.get('FixedVersion', 'latest')}" if vuln.get("FixedVersion") else None,
                    package_name=vuln.get("PkgName"),
                    package_version=vuln.get("InstalledVersion"),
                    fixed_version=vuln.get("FixedVersion"),
                    metadata={
                        "primary_url": vuln.get("PrimaryURL"),
                        "data_source": vuln.get("DataSource", {}).get("Name"),
                        "published_date": vuln.get("PublishedDate"),
                        "last_modified_date": vuln.get("LastModifiedDate"),
                    },
                )

        return output
