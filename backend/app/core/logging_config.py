"""Structured logging configuration with request correlation IDs.

All log records automatically include the current ``request_id`` from the
context variable so that every line for a single HTTP request can be
filtered with a single grep.
"""

from __future__ import annotations

import logging
import sys

from app.core.request_context import request_id_var


class CorrelationFilter(logging.Filter):
    """Inject ``request_id`` into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get("")  # type: ignore[attr-defined]
        return True


def setup_logging(level: str = "INFO") -> None:
    """Configure root logger with structured format and correlation ID."""
    fmt = (
        "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | %(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%dT%H:%M:%S"))
    handler.addFilter(CorrelationFilter())

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    # Remove default handlers to avoid duplicate output
    root.handlers.clear()
    root.addHandler(handler)

    # Quiet noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("litellm").setLevel(logging.WARNING)
