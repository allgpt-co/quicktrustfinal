"""Checkov Infrastructure as Code (IaC) scanner."""
import logging
import time

from app.scanners.base import BaseScanner, ScanOutput

logger = logging.getLogger(__name__)

CHECKOV_SEVERITY_MAP = {
    "CRITICAL": "critical",
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low",
    "INFO": "info",
    "NONE": "info",
}


class CheckovScanner(BaseScanner):
    name = "checkov"
    scan_type = "iac"

    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Scan IaC files (Terraform, CloudFormation, K8s, Dockerfile).

        Target should be a directory path containing IaC files.
        """
        output = ScanOutput()
        config = config or {}
        start = time.time()

        timeout_secs = config.get("timeout", 300)
        framework = config.get("framework")  # terraform, cloudformation, kubernetes, dockerfile

        cmd = [
            "checkov",
            "-d", target,
            "--output", "json",
            "--compact",
            "--quiet",
        ]

        if framework:
            cmd.extend(["--framework", framework])

        stdout, stderr, returncode = await self._run_command(cmd, timeout=timeout_secs)
        output.duration_seconds = time.time() - start
        output.raw_output = stdout[:50000]

        if returncode == -1:
            output.error = stderr
            return output

        data = self._parse_json_output(stdout)
        if not data:
            output.error = stderr or "Failed to parse Checkov output"
            return output

        # Checkov can return a list (multi-framework) or single dict
        results_list = data if isinstance(data, list) else [data]

        for results in results_list:
            failed_checks = results.get("results", {}).get("failed_checks", [])
            for check in failed_checks:
                sev_str = check.get("severity") or check.get("check_result", {}).get("severity", "MEDIUM")
                sev = CHECKOV_SEVERITY_MAP.get(sev_str.upper(), "medium")

                file_path = check.get("file_path", "")
                resource = check.get("resource", "")

                output.add_finding(
                    severity=sev,
                    title=f"{check.get('check_id', '')}: {check.get('check_name', 'Unknown check')}",
                    description=check.get("check_name", ""),
                    location=f"{file_path} ({resource})" if resource else file_path,
                    line_number=check.get("file_line_range", [None])[0],
                    rule_id=check.get("check_id"),
                    remediation=check.get("guideline"),
                    metadata={
                        "check_type": check.get("check_type"),
                        "resource": resource,
                        "bc_check_id": check.get("bc_check_id"),
                        "guideline": check.get("guideline"),
                        "file_line_range": check.get("file_line_range"),
                    },
                )

        return output
