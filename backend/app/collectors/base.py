"""Base collector interface and registry."""
from abc import ABC, abstractmethod
from typing import Any

COLLECTOR_REGISTRY: dict[str, "BaseCollector"] = {}


def register_collector(collector_type: str):
    """Decorator to register a collector class in the global registry."""
    def decorator(cls):
        COLLECTOR_REGISTRY[collector_type] = cls()
        return cls
    return decorator


class BaseCollector(ABC):
    """Abstract base class for evidence collectors.

    All collectors must implement ``collect()``. The optional methods
    ``authenticate``, ``list_resources``, and ``test_control`` provide
    a richer integration experience when supported by the provider.
    """

    @abstractmethod
    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        """
        Run the collection and return result data.

        Returns a dict with:
          - status: "success" | "failure"
          - data: collected evidence payload
          - summary: human-readable summary
        """
        ...

    async def authenticate(self, credentials: dict) -> dict[str, Any]:
        """Test whether the supplied credentials are valid.

        Returns ``{"status": "ok"}`` on success or raises.
        The default implementation is a no-op that always succeeds.
        """
        return {"status": "ok", "message": "Authentication not implemented for this collector"}

    async def list_resources(self, config: dict, credentials: dict | None = None) -> list[dict]:
        """Discover available resources the collector can pull from.

        Returns a list of resource dicts (e.g. repos, projects, accounts).
        """
        return []

    async def test_control(self, control_id: str, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        """Verify that a specific compliance control passes.

        Returns ``{"pass": True/False, "details": ...}``.
        """
        return {"pass": None, "details": "Control testing not implemented for this collector"}
