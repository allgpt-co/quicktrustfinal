"""Prowler cloud security scanner (AWS/Azure/GCP)."""
import logging
import time

from app.scanners.base import BaseScanner, ScanOutput

logger = logging.getLogger(__name__)

PROWLER_SEVERITY_MAP = {
    "critical": "critical",
    "high": "high",
    "medium": "medium",
    "low": "low",
    "informational": "info",
}


class ProwlerScanner(BaseScanner):
    name = "prowler"
    scan_type = "cloud"

    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Scan cloud infrastructure using Prowler.

        Target should be an AWS profile name or 'default'.
        Config can include:
          - provider: aws|azure|gcp (default: aws)
          - services: list of services to scan (e.g. ["iam", "s3"])
          - compliance: compliance framework (e.g. "cis_1.5_aws")
        """
        output = ScanOutput()
        config = config or {}
        start = time.time()

        provider = config.get("provider", "aws")
        timeout_secs = config.get("timeout", 600)

        cmd = [
            "prowler", provider,
            "--output-formats", "json",
            "--output-filename", "/dev/stdout",
            "--no-banner",
        ]

        services = config.get("services")
        if services:
            cmd.extend(["--services"] + (services if isinstance(services, list) else [services]))

        compliance = config.get("compliance")
        if compliance:
            cmd.extend(["--compliance", compliance])

        stdout, stderr, returncode = await self._run_command(cmd, timeout=timeout_secs)
        output.duration_seconds = time.time() - start
        output.raw_output = stdout[:50000]

        if returncode == -1:
            output.error = stderr
            return output

        # Prowler outputs JSONL (one finding per line)
        for line in stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            data = self._parse_json_output(line)
            if not data:
                continue

            status = data.get("StatusExtended", data.get("Status", ""))
            # Only include FAIL findings
            if data.get("Status", "").upper() == "PASS":
                continue

            sev = PROWLER_SEVERITY_MAP.get(
                data.get("Severity", "medium").lower(), "medium"
            )

            output.add_finding(
                severity=sev,
                title=data.get("CheckTitle", data.get("CheckID", "Unknown")),
                description=status[:2000] if status else data.get("Description", ""),
                location=data.get("ResourceId", data.get("ResourceArn", "")),
                rule_id=data.get("CheckID"),
                remediation=data.get("Remediation", {}).get("Recommendation", {}).get("Text", "") if isinstance(data.get("Remediation"), dict) else None,
                metadata={
                    "provider": data.get("Provider"),
                    "service": data.get("ServiceName"),
                    "region": data.get("Region"),
                    "account_id": data.get("AccountId"),
                    "resource_type": data.get("ResourceType"),
                    "compliance": data.get("Compliance", {}),
                    "risk": data.get("Risk"),
                },
            )

        return output
