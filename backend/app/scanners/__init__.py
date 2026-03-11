"""Security scanner implementations."""
from app.scanners.base import BaseScanner
from app.scanners.trivy import TrivyScanner
from app.scanners.semgrep import SemgrepScanner
from app.scanners.gitleaks import GitleaksScanner
from app.scanners.checkov import CheckovScanner
from app.scanners.zap import ZapScanner
from app.scanners.nuclei import NucleiScanner
from app.scanners.prowler import ProwlerScanner

SCANNER_REGISTRY: dict[str, type[BaseScanner]] = {
    "trivy": TrivyScanner,
    "semgrep": SemgrepScanner,
    "gitleaks": GitleaksScanner,
    "checkov": CheckovScanner,
    "zap": ZapScanner,
    "nuclei": NucleiScanner,
    "prowler": ProwlerScanner,
}

__all__ = [
    "BaseScanner",
    "SCANNER_REGISTRY",
    "TrivyScanner",
    "SemgrepScanner",
    "GitleaksScanner",
    "CheckovScanner",
    "ZapScanner",
    "NucleiScanner",
    "ProwlerScanner",
]
