from unittest.mock import AsyncMock, patch

import pytest

from app.services.keycloak_service import KeycloakService


class _Response:
    def raise_for_status(self):
        return None

    def json(self):
        return {"access_token": "token"}


@pytest.mark.asyncio
async def test_exchange_token_uses_configured_confidential_client():
    service = KeycloakService()

    mock_client = AsyncMock()
    mock_client.post.return_value = _Response()

    with patch("app.services.keycloak_service.httpx.AsyncClient") as async_client:
        async_client.return_value.__aenter__.return_value = mock_client

        result = await service.exchange_token("admin@quicktrust.dev", "user-supplied-password")

    assert result == {"access_token": "token"}
    _, kwargs = mock_client.post.call_args
    assert kwargs["data"]["grant_type"] == "password"
    assert kwargs["data"]["client_id"] == service.client_id
    assert kwargs["data"]["client_secret"] == service.client_secret
    assert kwargs["data"]["username"] == "admin@quicktrust.dev"
    assert kwargs["data"]["password"] == "user-supplied-password"
