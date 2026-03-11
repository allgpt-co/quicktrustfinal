"""Gitleaks secret detection scanner."""
import json
import logging
import os
import tempfile
import time

from app.scanners.base import BaseScanner, ScanOutput

logger = logging.getLogger(__name__)

# Secrets are always high severity; categorise by type
SECRET_TYPE_SEVERITY = {
    "aws-access-token": "critical",
    "aws-secret-access-key": "critical",
    "private-key": "critical",
    "github-pat": "high",
    "github-oauth": "high",
    "generic-api-key": "high",
    "stripe-access-token": "critical",
    "slack-webhook": "high",
    "jwt": "high",
}


class GitleaksScanner(BaseScanner):
    name = "gitleaks"
    scan_type = "secrets"

    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Scan a directory for leaked secrets.

        Target should be a path to a directory or git repository.
        """
        output = ScanOutput()
        config = config or {}
        start = time.time()

        timeout_secs = config.get("timeout", 300)
        scan_mode = config.get("mode", "detect")  # detect or protect

        # Use a temp file for the report instead of /dev/stdout
        report_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, dir="/tmp"
        )
        report_path = report_file.name
        report_file.close()

        try:
            cmd = [
                "gitleaks", scan_mode,
                "--source", target,
                "--report-format", "json",
                "--report-path", report_path,
                "--no-banner",
            ]

            # Auto-detect: add --no-git if target is not a git repo
            if config.get("no_git") or not os.path.isdir(os.path.join(target, ".git")):
                cmd.append("--no-git")

            stdout, stderr, returncode = await self._run_command(cmd, timeout=timeout_secs)
            output.duration_seconds = time.time() - start
            output.raw_output = stderr[:5000]

            # Gitleaks returns exit code 1 when leaks found, 0 when clean
            if returncode == -1:
                output.error = stderr
                return output

            # Read results from the report file
            try:
                with open(report_path, "r") as f:
                    report_content = f.read()
            except FileNotFoundError:
                # No report file = no leaks
                return output

            if not report_content.strip() or report_content.strip() == "[]":
                # No leaks found
                return output

            try:
                data = json.loads(report_content)
            except json.JSONDecodeError:
                if returncode == 0:
                    return output
                output.error = stderr or "Failed to parse Gitleaks output"
                return output

            if not isinstance(data, list):
                data = [data]

            for leak in data:
                rule_id = leak.get("RuleID", "unknown")
                sev = SECRET_TYPE_SEVERITY.get(rule_id, "high")

                output.add_finding(
                    severity=sev,
                    title=f"Secret detected: {leak.get('Description', rule_id)}",
                    description=f"Found {leak.get('Description', 'a secret')} in {leak.get('File', 'unknown file')}",
                    location=leak.get("File", ""),
                    line_number=leak.get("StartLine"),
                    rule_id=rule_id,
                    remediation="Rotate the exposed credential immediately. Remove from git history using git-filter-repo.",
                    metadata={
                        "commit": leak.get("Commit"),
                        "author": leak.get("Author"),
                        "email": leak.get("Email"),
                        "date": leak.get("Date"),
                        "match": leak.get("Match", "")[:200],
                        "entropy": leak.get("Entropy"),
                        "fingerprint": leak.get("Fingerprint"),
                    },
                )

        finally:
            # Clean up temp file
            try:
                os.unlink(report_path)
            except OSError:
                pass

        return output
