"""Nuclei template-based vulnerability scanner."""
import logging
import time

from app.scanners.base import BaseScanner, ScanOutput

logger = logging.getLogger(__name__)

NUCLEI_SEVERITY_MAP = {
    "critical": "critical",
    "high": "high",
    "medium": "medium",
    "low": "low",
    "info": "info",
    "unknown": "info",
}


class NucleiScanner(BaseScanner):
    name = "nuclei"
    scan_type = "template"

    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Scan a target URL using Nuclei vulnerability templates.

        Target should be a URL, e.g. 'https://myapp.example.com'.
        """
        output = ScanOutput()
        config = config or {}
        start = time.time()

        timeout_secs = config.get("timeout", 600)
        templates = config.get("templates")  # specific template paths
        severity_filter = config.get("severity", "critical,high,medium,low")
        tags = config.get("tags")  # e.g. "cve,exposure,misconfiguration"

        cmd = [
            "nuclei",
            "-u", target,
            "-jsonl",
            "-severity", severity_filter,
            "-silent",
            "-no-color",
        ]

        if templates:
            cmd.extend(["-t", templates])
        if tags:
            cmd.extend(["-tags", tags])

        stdout, stderr, returncode = await self._run_command(cmd, timeout=timeout_secs)
        output.duration_seconds = time.time() - start
        output.raw_output = stdout[:50000]

        if returncode == -1:
            output.error = stderr
            return output

        # Nuclei outputs one JSON object per line (JSONL)
        for line in stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            data = self._parse_json_output(line)
            if not data:
                continue

            info = data.get("info", {})
            sev = NUCLEI_SEVERITY_MAP.get(
                info.get("severity", "info").lower(), "info"
            )

            matcher_name = data.get("matcher-name", "")
            template_id = data.get("template-id", "unknown")

            output.add_finding(
                severity=sev,
                title=f"{info.get('name', template_id)}" + (f" ({matcher_name})" if matcher_name else ""),
                description=info.get("description", "")[:2000],
                location=data.get("matched-at", data.get("host", target)),
                rule_id=template_id,
                cve_id=data.get("cve-id"),
                cwe_id=f"CWE-{info.get('classification', {}).get('cwe-id', [''])[0]}" if info.get("classification", {}).get("cwe-id") else None,
                remediation=info.get("remediation", "")[:2000] or None,
                metadata={
                    "template_url": data.get("template-url"),
                    "type": data.get("type"),
                    "tags": info.get("tags", []),
                    "reference": info.get("reference", [])[:5],
                    "extracted_results": data.get("extracted-results", [])[:5],
                    "curl_command": data.get("curl-command", "")[:500],
                    "matcher_status": data.get("matcher-status"),
                },
            )

        return output
