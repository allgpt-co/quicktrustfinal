"""Azure collectors for cloud security evidence.

Supports:
  - Azure AD / Entra ID: users, groups, MFA status, conditional access
  - Azure Key Vault: configuration audit
  - NSG (Network Security Groups): firewall rules check

Falls back to mock data when Azure credentials are missing.
"""
import logging
from datetime import datetime, timezone
from typing import Any

import httpx

from app.collectors.base import BaseCollector, register_collector

logger = logging.getLogger(__name__)

GRAPH_API = "https://graph.microsoft.com/v1.0"
MGMT_API = "https://management.azure.com"


async def _get_azure_token(credentials: dict) -> str:
    """Get an OAuth2 access token using client_credentials flow."""
    tenant_id = credentials.get("tenant_id")
    client_id = credentials.get("client_id")
    client_secret = credentials.get("client_secret")
    if not all([tenant_id, client_id, client_secret]):
        raise ValueError("tenant_id, client_id, and client_secret required")

    resource = credentials.get("resource", "https://graph.microsoft.com")
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(token_url, data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": f"{resource}/.default",
        })
        if resp.status_code != 200:
            raise RuntimeError(f"Azure token failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()["access_token"]


def _azure_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# ---------------------------------------------------------------------------
# Azure AD Users & MFA
# ---------------------------------------------------------------------------

@register_collector("azure_ad_users_mfa")
class AzureADUsersMFA(BaseCollector):
    """Collect Azure AD users and their MFA registration status."""

    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            token = await _get_azure_token(credentials or {})
            headers = _azure_headers(token)

            async with httpx.AsyncClient(timeout=20.0) as client:
                # Get users
                users_resp = await client.get(
                    f"{GRAPH_API}/users",
                    headers=headers,
                    params={"$select": "id,displayName,userPrincipalName,accountEnabled", "$top": 200},
                )
                users_data = users_resp.json().get("value", [])

                # Get MFA registration details
                mfa_resp = await client.get(
                    f"{GRAPH_API}/reports/authenticationMethods/userRegistrationDetails",
                    headers=headers,
                    params={"$top": 200},
                )
                mfa_data = {
                    r.get("userPrincipalName"): r
                    for r in mfa_resp.json().get("value", [])
                }

            total_users = len(users_data)
            mfa_enrolled = 0
            non_compliant = []

            for user in users_data:
                upn = user.get("userPrincipalName", "")
                mfa_info = mfa_data.get(upn, {})
                is_mfa = mfa_info.get("isMfaRegistered", False)
                if is_mfa:
                    mfa_enrolled += 1
                elif user.get("accountEnabled"):
                    non_compliant.append({
                        "user": user.get("displayName"),
                        "upn": upn,
                        "enabled": user.get("accountEnabled"),
                    })

            compliance_rate = round(mfa_enrolled / max(total_users, 1) * 100, 1)
            logger.info("Azure AD MFA evidence: %d/%d enrolled", mfa_enrolled, total_users)
            return {
                "status": "success",
                "summary": f"Azure AD MFA: {mfa_enrolled}/{total_users} enrolled ({compliance_rate}%)",
                "data_source": "live",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "total_users": total_users,
                    "mfa_enrolled": mfa_enrolled,
                    "mfa_not_enrolled": total_users - mfa_enrolled,
                    "compliance_rate": compliance_rate,
                    "non_compliant_users": non_compliant[:20],
                },
            }
        except Exception as exc:
            logger.warning("Azure AD MFA collection failed, using mock: %s", exc)
            return self._mock_response()

    async def authenticate(self, credentials: dict) -> dict[str, Any]:
        token = await _get_azure_token(credentials)
        headers = _azure_headers(token)
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{GRAPH_API}/organization", headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"Azure auth failed: {resp.status_code}")
            orgs = resp.json().get("value", [])
        return {"status": "ok", "tenant": orgs[0].get("displayName") if orgs else "unknown"}

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Azure AD MFA compliance (mock): 95.2%",
            "data_source": "mock",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "total_users": 83,
                "mfa_enrolled": 79,
                "mfa_not_enrolled": 4,
                "compliance_rate": 95.2,
                "non_compliant_users": [
                    {"user": "Service Account - Legacy", "upn": "svc-legacy@contoso.com", "enabled": True},
                    {"user": "Temp Contractor", "upn": "temp@contoso.com", "enabled": True},
                ],
            },
        }


# ---------------------------------------------------------------------------
# Azure Key Vault Audit
# ---------------------------------------------------------------------------

@register_collector("azure_keyvault_audit")
class AzureKeyVaultAudit(BaseCollector):
    """Audit Azure Key Vault configuration (soft delete, purge protection, access policies)."""

    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            creds = credentials or {}
            creds_mgmt = {**creds, "resource": "https://management.azure.com"}
            token = await _get_azure_token(creds_mgmt)
            headers = _azure_headers(token)

            subscription_id = creds.get("subscription_id")
            if not subscription_id:
                raise ValueError("subscription_id required for Key Vault audit")

            api_version = "2023-07-01"
            url = f"{MGMT_API}/subscriptions/{subscription_id}/providers/Microsoft.KeyVault/vaults?api-version={api_version}"

            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    raise RuntimeError(f"Key Vault list failed: {resp.status_code}")
                vaults_data = resp.json().get("value", [])

            vaults = []
            compliant = 0
            for vault in vaults_data:
                props = vault.get("properties", {})
                v = {
                    "name": vault.get("name"),
                    "location": vault.get("location"),
                    "soft_delete_enabled": props.get("enableSoftDelete", False),
                    "purge_protection_enabled": props.get("enablePurgeProtection", False),
                    "rbac_authorization": props.get("enableRbacAuthorization", False),
                    "sku": props.get("sku", {}).get("name", ""),
                }
                v["compliant"] = v["soft_delete_enabled"] and v["purge_protection_enabled"]
                if v["compliant"]:
                    compliant += 1
                vaults.append(v)

            logger.info("Azure Key Vault audit: %d/%d compliant", compliant, len(vaults))
            return {
                "status": "success",
                "summary": f"Key Vault audit: {compliant}/{len(vaults)} compliant",
                "data_source": "live",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "total_vaults": len(vaults),
                    "compliant_vaults": compliant,
                    "compliance_rate": round(compliant / max(len(vaults), 1) * 100, 1),
                    "vaults": vaults[:20],
                },
            }
        except Exception as exc:
            logger.warning("Azure Key Vault audit failed, using mock: %s", exc)
            return self._mock_response()

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "Key Vault audit (mock): 3/3 compliant",
            "data_source": "mock",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "total_vaults": 3,
                "compliant_vaults": 3,
                "compliance_rate": 100.0,
                "vaults": [
                    {"name": "prod-secrets", "location": "eastus", "soft_delete_enabled": True,
                     "purge_protection_enabled": True, "rbac_authorization": True, "sku": "standard", "compliant": True},
                    {"name": "dev-secrets", "location": "eastus", "soft_delete_enabled": True,
                     "purge_protection_enabled": True, "rbac_authorization": False, "sku": "standard", "compliant": True},
                ],
            },
        }


# ---------------------------------------------------------------------------
# Azure NSG Rules
# ---------------------------------------------------------------------------

@register_collector("azure_nsg_rules")
class AzureNSGRules(BaseCollector):
    """Check Azure Network Security Group rules for overly permissive access."""

    async def collect(self, config: dict, credentials: dict | None = None) -> dict[str, Any]:
        try:
            creds = credentials or {}
            creds_mgmt = {**creds, "resource": "https://management.azure.com"}
            token = await _get_azure_token(creds_mgmt)
            headers = _azure_headers(token)

            subscription_id = creds.get("subscription_id")
            if not subscription_id:
                raise ValueError("subscription_id required for NSG audit")

            api_version = "2023-11-01"
            url = f"{MGMT_API}/subscriptions/{subscription_id}/providers/Microsoft.Network/networkSecurityGroups?api-version={api_version}"

            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    raise RuntimeError(f"NSG list failed: {resp.status_code}")
                nsgs_data = resp.json().get("value", [])

            findings = []
            total_rules = 0
            risky_rules = 0

            for nsg in nsgs_data:
                props = nsg.get("properties", {})
                rules = props.get("securityRules", [])
                total_rules += len(rules)

                for rule in rules:
                    rprops = rule.get("properties", {})
                    # Flag rules allowing all inbound from internet
                    if (rprops.get("direction") == "Inbound"
                            and rprops.get("access") == "Allow"
                            and rprops.get("sourceAddressPrefix") in ("*", "0.0.0.0/0", "Internet")):
                        risky_rules += 1
                        findings.append({
                            "nsg": nsg.get("name"),
                            "rule": rule.get("name"),
                            "direction": "Inbound",
                            "source": rprops.get("sourceAddressPrefix"),
                            "destination_port": rprops.get("destinationPortRange"),
                            "protocol": rprops.get("protocol"),
                            "severity": "high" if rprops.get("destinationPortRange") in ("*", "22", "3389") else "medium",
                        })

            logger.info("Azure NSG audit: %d risky rules in %d NSGs", risky_rules, len(nsgs_data))
            return {
                "status": "success",
                "summary": f"NSG audit: {risky_rules} risky rules found across {len(nsgs_data)} NSGs",
                "data_source": "live",
                "data": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "total_nsgs": len(nsgs_data),
                    "total_rules": total_rules,
                    "risky_rules": risky_rules,
                    "compliant": risky_rules == 0,
                    "findings": findings[:30],
                },
            }
        except Exception as exc:
            logger.warning("Azure NSG audit failed, using mock: %s", exc)
            return self._mock_response()

    @staticmethod
    def _mock_response() -> dict[str, Any]:
        return {
            "status": "success",
            "summary": "NSG audit (mock): 2 risky rules found",
            "data_source": "mock",
            "data": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "total_nsgs": 5,
                "total_rules": 34,
                "risky_rules": 2,
                "compliant": False,
                "findings": [
                    {"nsg": "web-nsg", "rule": "AllowSSH", "direction": "Inbound",
                     "source": "0.0.0.0/0", "destination_port": "22", "protocol": "TCP", "severity": "high"},
                    {"nsg": "db-nsg", "rule": "AllowAll", "direction": "Inbound",
                     "source": "*", "destination_port": "*", "protocol": "*", "severity": "high"},
                ],
            },
        }
