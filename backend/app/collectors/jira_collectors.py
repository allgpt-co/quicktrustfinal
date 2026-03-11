"""Jira collectors for change management and remediation tracking.

Supports:
  - Creating tickets from scan findings
  - Collecting change management evidence (tickets, approvals, SLA)
  - Tracking remediation tasks

Falls back to mock data when Jira credentials are missing.
"""
import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from app.collectors.base import BaseCollector, register_collector

logger = logging.getLogger(__name__)


def _jira_client(credentials: dict | None) -> tuple[str, dict[str, str]]:
    """Return (base_url, headers) for Jira REST API v3."""
    if not credentials:
        raise ValueError("No credentials provided")
    base_url = credentials.get("jira_url") or credentials.get("url", "")
    if not base_url:
        raise ValueError("No jira_url in credentials")
    base_url = base_url.rstrip("/")

    email = credentials.get("jira_email") or credentials.get("email", "")
    api_token = credentials.get("jira_api_token") or credentials.get("api_token", "")
    if not email or not api_token:
        raise ValueError("jira_email and jira_api_token required")

    import base64
    auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    return base_url, headers


# ---------------------------------------------------------------------------
# Create Ticket from Finding
# ---------------------------------------------------------------------------

@register_collector("jira_create_ticket")
class JiraCreateTicket(BaseCollector):
    """Create a Jira issue from a scan finding or compliance gap."""

    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            base_url, headers = _jira_client(credentials)

            project_key = config.get("project_key", "SEC")
            issue_type = config.get("issue_type", "Bug")
            summary = config.get("summary", "Security finding from QuickTrust")
            description = config.get("description", "")
            priority = config.get("priority", "Medium")
            labels = config.get("labels", ["quicktrust", "security"])

            payload = {
                "fields": {
                    "project": {"key": project_key},
                    "issuetype": {"name": issue_type},
                    "summary": summary,
                    "description": {
                        "type": "doc", "version": 1,
                        "content": [{"type": "paragraph", "content": [
                            {"type": "text", "text": description or summary}
                        ]}],
                    },
                    "priority": {"name": priority},
                    "labels": labels,
                },
            }

            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(f"{base_url}/rest/api/3/issue", headers=headers, json=payload)
                if resp.status_code not in (200, 201):
                    raise RuntimeError(f"Jira API {resp.status_code}: {resp.text[:200]}")
                data = resp.json()

            issue_key = data.get("key", "")
            logger.info("Jira ticket created: %s", issue_key)
            return {
                "status": "success",
                "summary": f"Jira ticket created: {issue_key}",
                "data_source": "live",
                "data": {
                    "issue_key": issue_key,
                    "issue_id": data.get("id"),
                    "url": f"{base_url}/browse/{issue_key}",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
            }
        except Exception as exc:
            logger.warning("Jira ticket creation failed, using mock: %s", exc)
            return self._mock_response(config)

    async def authenticate(self, credentials: dict) -> dict[str, Any]:
        base_url, headers = _jira_client(credentials)
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{base_url}/rest/api/3/myself", headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"Jira auth failed: {resp.status_code}")
            data = resp.json()
        return {"status": "ok", "user": data.get("displayName"), "email": data.get("emailAddress")}

    @staticmethod
    def _mock_response(config: dict) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Jira ticket created (mock): SEC-142",
            "data_source": "mock",
            "data": {
                "issue_key": "SEC-142",
                "issue_id": "10142",
                "url": "https://yourcompany.atlassian.net/browse/SEC-142",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
        }


# ---------------------------------------------------------------------------
# Collect Change Management Evidence
# ---------------------------------------------------------------------------

@register_collector("jira_change_management")
class JiraChangeManagement(BaseCollector):
    """Collect change management evidence from Jira (tickets, approvals, SLAs)."""

    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            base_url, headers = _jira_client(credentials)

            project_key = config.get("project_key", "SEC")
            jql = config.get("jql", f'project = "{project_key}" ORDER BY created DESC')
            max_results = config.get("max_results", 50)

            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.get(
                    f"{base_url}/rest/api/3/search",
                    headers=headers,
                    params={"jql": jql, "maxResults": max_results, "fields": "summary,status,priority,created,resolutiondate,assignee,labels"},
                )
                if resp.status_code != 200:
                    raise RuntimeError(f"Jira search failed: {resp.status_code}")
                data = resp.json()

            issues = data.get("issues", [])
            total = data.get("total", 0)

            # Calculate stats
            status_counts: dict[str, int] = {}
            resolved_count = 0
            for issue in issues:
                fields = issue.get("fields", {})
                status_name = fields.get("status", {}).get("name", "Unknown")
                status_counts[status_name] = status_counts.get(status_name, 0) + 1
                if fields.get("resolutiondate"):
                    resolved_count += 1

            tickets = [
                {
                    "key": issue.get("key"),
                    "summary": issue.get("fields", {}).get("summary", "")[:100],
                    "status": issue.get("fields", {}).get("status", {}).get("name"),
                    "priority": issue.get("fields", {}).get("priority", {}).get("name"),
                    "created": issue.get("fields", {}).get("created"),
                    "resolved": issue.get("fields", {}).get("resolutiondate"),
                    "assignee": (issue.get("fields", {}).get("assignee") or {}).get("displayName"),
                }
                for issue in issues[:50]
            ]

            logger.info("Jira change management evidence: %d tickets from %s", len(tickets), project_key)
            return {
                "status": "success",
                "summary": f"Change management evidence: {total} tickets from {project_key}",
                "data_source": "live",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "project_key": project_key,
                    "total_tickets": total,
                    "resolved_count": resolved_count,
                    "resolution_rate": round(resolved_count / max(total, 1) * 100, 1),
                    "status_breakdown": status_counts,
                    "tickets": tickets,
                },
            }
        except Exception as exc:
            logger.warning("Jira change management failed, using mock: %s", exc)
            return self._mock_response()

    async def list_resources(self, config: dict, credentials: dict | None = None) -> list[dict]:
        try:
            base_url, headers = _jira_client(credentials)
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{base_url}/rest/api/3/project", headers=headers)
                data = resp.json()
            return [{"id": p["id"], "key": p["key"], "name": p["name"], "type": "project"} for p in data[:50]]
        except Exception:
            return []

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Change management evidence (mock): 23 tickets",
            "data_source": "mock",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "project_key": "SEC",
                "total_tickets": 23,
                "resolved_count": 18,
                "resolution_rate": 78.3,
                "status_breakdown": {"Done": 18, "In Progress": 3, "To Do": 2},
                "tickets": [
                    {"key": "SEC-140", "summary": "Fix SQL injection in /api/users", "status": "Done",
                     "priority": "Critical", "created": "2026-02-01", "resolved": "2026-02-03", "assignee": "Jane Dev"},
                    {"key": "SEC-141", "summary": "Update OpenSSL to patch CVE-2025-XXXX", "status": "In Progress",
                     "priority": "High", "created": "2026-02-15", "resolved": None, "assignee": "Bob Ops"},
                ],
            },
        }
