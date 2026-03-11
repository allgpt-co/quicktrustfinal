"""OWASP ZAP (Zed Attack Proxy) DAST scanner."""
import logging
import time

from app.scanners.base import BaseScanner, ScanOutput

logger = logging.getLogger(__name__)

ZAP_RISK_MAP = {
    "0": "info",
    "1": "low",
    "2": "medium",
    "3": "high",
}

ZAP_CONFIDENCE_MAP = {
    "0": "false_positive",
    "1": "low",
    "2": "medium",
    "3": "high",
    "4": "confirmed",
}


class ZapScanner(BaseScanner):
    name = "zap"
    scan_type = "dast"

    async def run(self, target: str, config: dict | None = None) -> ScanOutput:
        """Scan a running web application using OWASP ZAP baseline scan.

        Target should be a URL, e.g. 'https://myapp.example.com'.
        """
        output = ScanOutput()
        config = config or {}
        start = time.time()

        timeout_secs = config.get("timeout", 600)
        scan_mode = config.get("mode", "baseline")  # baseline, full, api

        if scan_mode == "baseline":
            script = "zap-baseline.py"
        elif scan_mode == "full":
            script = "zap-full-scan.py"
        else:
            script = "zap-api-scan.py"

        cmd = [
            "zap-" + scan_mode.replace("_", "-") + ".py" if scan_mode != "full" else script,
            "-t", target,
            "-J", "report.json",
            "-I",  # Don't return non-zero for warnings
        ]

        # For Docker-based ZAP:
        cmd = [
            "docker", "run", "--rm",
            "--network", "host",
            "zaproxy/zap-stable",
            script,
            "-t", target,
            "-J", "/dev/stdout",
            "-I",
        ]

        stdout, stderr, returncode = await self._run_command(cmd, timeout=timeout_secs)
        output.duration_seconds = time.time() - start
        output.raw_output = stdout[:50000]

        if returncode == -1:
            output.error = stderr
            return output

        data = self._parse_json_output(stdout)
        if not data:
            output.error = stderr or "Failed to parse ZAP output"
            return output

        # Parse ZAP JSON report
        site_list = data.get("site", [])
        if not isinstance(site_list, list):
            site_list = [site_list]

        for site in site_list:
            alerts = site.get("alerts", [])
            for alert in alerts:
                risk_code = str(alert.get("riskcode", "0"))
                sev = ZAP_RISK_MAP.get(risk_code, "info")
                conf_code = str(alert.get("confidence", "1"))
                conf = ZAP_CONFIDENCE_MAP.get(conf_code, "medium")

                instances = alert.get("instances", [])
                urls = [inst.get("uri", "") for inst in instances[:5]]

                output.add_finding(
                    severity=sev,
                    title=alert.get("name", "Unknown alert"),
                    description=alert.get("desc", "")[:2000],
                    location=", ".join(urls) if urls else target,
                    rule_id=str(alert.get("pluginid", "")),
                    cwe_id=f"CWE-{alert.get('cweid')}" if alert.get("cweid") else None,
                    remediation=alert.get("solution", "")[:2000],
                    confidence=conf,
                    metadata={
                        "wascid": alert.get("wascid"),
                        "reference": alert.get("reference", "")[:1000],
                        "alert_count": alert.get("count", len(instances)),
                        "attack": instances[0].get("attack", "") if instances else "",
                        "evidence": instances[0].get("evidence", "")[:200] if instances else "",
                    },
                )

        return output
