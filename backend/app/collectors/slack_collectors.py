"""Slack collectors for notifications and evidence collection.

Supports:
  - Sending notifications (scan results, policy approvals, finding alerts)
  - Collecting evidence (workspace info, channel list, retention settings)
  - Interactive approvals via Slack (webhook-based)

Falls back to mock data when Slack credentials are missing.
"""
import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from app.collectors.base import BaseCollector, register_collector

logger = logging.getLogger(__name__)

SLACK_API_BASE = "https://slack.com/api"


def _slack_headers(credentials: dict | None) -> dict[str, str]:
    if not credentials:
        raise ValueError("No credentials provided")
    token = credentials.get("slack_bot_token") or credentials.get("token")
    if not token:
        raise ValueError("No slack_bot_token in credentials")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# ---------------------------------------------------------------------------
# Send Notification
# ---------------------------------------------------------------------------

@register_collector("slack_send_notification")
class SlackSendNotification(BaseCollector):
    """Send a notification message to a Slack channel."""

    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            # Support both webhook URL and Bot Token approaches
            webhook_url = (credentials or {}).get("webhook_url")
            if webhook_url:
                return await self._send_via_webhook(webhook_url, config)
            return await self._send_via_api(config, credentials)
        except Exception as exc:
            logger.warning("Slack notification failed, using mock: %s", exc)
            return self._mock_response(config)

    async def _send_via_webhook(self, webhook_url: str, config: dict) -> dict[str, Any]:
        channel = config.get("channel", "#compliance")
        message = config.get("message", "QuickTrust notification")
        blocks = config.get("blocks") or [
            {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        ]
        payload = {"channel": channel, "text": message, "blocks": blocks}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(webhook_url, json=payload)
            resp.raise_for_status()
        logger.info("Slack notification sent via webhook to %s", channel)
        return {
            "status": "success",
            "summary": f"Notification sent to {channel}",
            "data_source": "live",
            "data": {"channel": channel, "sent_at": datetime.now(timezone.utc).isoformat()},
        }

    async def _send_via_api(self, config: dict, credentials: dict | None) -> dict[str, Any]:
        headers = _slack_headers(credentials)
        channel = config.get("channel", "#compliance")
        message = config.get("message", "QuickTrust notification")
        blocks = config.get("blocks")

        payload: dict[str, Any] = {"channel": channel, "text": message}
        if blocks:
            payload["blocks"] = blocks

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{SLACK_API_BASE}/chat.postMessage", headers=headers, json=payload)
            data = resp.json()
            if not data.get("ok"):
                raise RuntimeError(f"Slack API error: {data.get('error', 'unknown')}")

        logger.info("Slack notification sent via API to %s", channel)
        return {
            "status": "success",
            "summary": f"Notification sent to {channel}",
            "data_source": "live",
            "data": {
                "channel": channel,
                "ts": data.get("ts"),
                "sent_at": datetime.now(timezone.utc).isoformat(),
            },
        }

    async def authenticate(self, credentials: dict) -> dict[str, Any]:
        webhook_url = credentials.get("webhook_url")
        if webhook_url:
            return {"status": "ok", "message": "Webhook URL configured"}
        headers = _slack_headers(credentials)
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{SLACK_API_BASE}/auth.test", headers=headers)
            data = resp.json()
            if not data.get("ok"):
                raise RuntimeError(f"Slack auth failed: {data.get('error')}")
        return {"status": "ok", "team": data.get("team"), "user": data.get("user")}

    @staticmethod
    def _mock_response(config: dict) -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Notification sent (mock)",
            "data_source": "mock",
            "data": {
                "channel": config.get("channel", "#compliance"),
                "sent_at": datetime.now(timezone.utc).isoformat(),
            },
        }


# ---------------------------------------------------------------------------
# Collect Workspace Evidence
# ---------------------------------------------------------------------------

@register_collector("slack_workspace_evidence")
class SlackWorkspaceEvidence(BaseCollector):
    """Collect Slack workspace info: channels, retention, DLP settings."""

    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            headers = _slack_headers(credentials)
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Team info
                team_resp = await client.post(f"{SLACK_API_BASE}/team.info", headers=headers)
                team_data = team_resp.json()

                # Channel list
                channels_resp = await client.post(
                    f"{SLACK_API_BASE}/conversations.list",
                    headers=headers,
                    json={"types": "public_channel,private_channel", "limit": 200},
                )
                channels_data = channels_resp.json()

            team = team_data.get("team", {})
            channels = channels_data.get("channels", [])

            return {
                "status": "success",
                "summary": f"Workspace evidence collected: {len(channels)} channels",
                "data_source": "live",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "team_name": team.get("name", "unknown"),
                    "team_domain": team.get("domain", ""),
                    "total_channels": len(channels),
                    "public_channels": sum(1 for c in channels if not c.get("is_private")),
                    "private_channels": sum(1 for c in channels if c.get("is_private")),
                    "channels": [
                        {"name": c.get("name"), "is_private": c.get("is_private", False),
                         "num_members": c.get("num_members", 0)}
                        for c in channels[:50]
                    ],
                },
            }
        except Exception as exc:
            logger.warning("Slack workspace evidence failed, using mock: %s", exc)
            return self._mock_response()

    async def list_resources(self, config: dict, credentials: dict | None = None) -> list[dict]:
        try:
            headers = _slack_headers(credentials)
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{SLACK_API_BASE}/conversations.list",
                    headers=headers,
                    json={"types": "public_channel", "limit": 100},
                )
                data = resp.json()
            return [
                {"id": c["id"], "name": c["name"], "type": "channel"}
                for c in data.get("channels", [])
            ]
        except Exception:
            return []

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Workspace evidence collected (mock)",
            "data_source": "mock",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "team_name": "AcmeCorp",
                "team_domain": "acmecorp",
                "total_channels": 45,
                "public_channels": 32,
                "private_channels": 13,
                "channels": [
                    {"name": "general", "is_private": False, "num_members": 120},
                    {"name": "security-alerts", "is_private": False, "num_members": 15},
                    {"name": "compliance", "is_private": True, "num_members": 8},
                    {"name": "incident-response", "is_private": True, "num_members": 12},
                ],
            },
        }
