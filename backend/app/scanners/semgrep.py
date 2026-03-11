"""Semgrep SAST (Static Application Security Testing) scanner."""
import logging
import time

from app.scanners.base import BaseScanner, ScanOutput

logger = logging.getLogger(__name__)

SEMGREP_SEVERITY_MAP = {
    "ERROR": "high",
    "WARNING": "medium",
    "INFO": "low",
}

SEMGREP_IMPACT_MAP = {
    "HIGH": "critical",
    "MEDIUM": "high",
    "LOW": "medium",
}


class SemgrepScanner(BaseScanner):
    name = "semgrep"
    scan_type = "sast"

    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Scan source code for security vulnerabilities using Semgrep.

        Target should be a directory path containing source code.
        """
        output = ScanOutput()
        config = config or {}
        start = time.time()

        ruleset = config.get("config", "p/security-audit")
        timeout_secs = config.get("timeout", 300)

        cmd = [
            "semgrep", "scan",
            "--config", ruleset,
            "--json",
            "--no-git-ignore",
            "--timeout", str(config.get("rule_timeout", 30)),
            target,
        ]

        stdout, stderr, returncode = await self._run_command(cmd, timeout=timeout_secs)
        output.duration_seconds = time.time() - start
        output.raw_output = stdout[:50000]

        data = self._parse_json_output(stdout)
        if not data:
            output.error = stderr or "Failed to parse Semgrep output"
            return output

        results = data.get("results") or []
        for result in results:
            check_id = result.get("check_id", "")
            extra = result.get("extra", {})
            meta = extra.get("metadata", {})

            # Use impact for severity if available, otherwise fall back to Semgrep severity
            impact = meta.get("impact")
            if impact and impact.upper() in SEMGREP_IMPACT_MAP:
                sev = SEMGREP_IMPACT_MAP[impact.upper()]
            else:
                sev = SEMGREP_SEVERITY_MAP.get(extra.get("severity", ""), "medium")

            output.add_finding(
                severity=sev,
                title=extra.get("message", check_id)[:500],
                description=f"Rule: {check_id}\n{extra.get('message', '')}",
                location=result.get("path", ""),
                line_number=result.get("start", {}).get("line"),
                rule_id=check_id,
                cwe_id=", ".join(meta.get("cwe", [])) if meta.get("cwe") else None,
                remediation=extra.get("fix") or meta.get("fix"),
                confidence=meta.get("confidence", "").lower() or None,
                metadata={
                    "category": meta.get("category"),
                    "technology": meta.get("technology"),
                    "owasp": meta.get("owasp"),
                    "references": meta.get("references", [])[:5],
                    "fingerprint": result.get("extra", {}).get("fingerprint"),
                },
            )

        return output
