from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.agents.common import llm
from app.config import Settings


@pytest.mark.asyncio
async def test_disabled_bedrock_returns_mock_without_calling_provider(
    monkeypatch,
) -> None:
    monkeypatch.setattr(llm.settings, "BEDROCK_ENABLED", False)

    async def unexpected_call(**kwargs):
        raise AssertionError("LiteLLM must not be called while Bedrock is disabled")

    monkeypatch.setattr(llm.litellm, "acompletion", unexpected_call)

    result, usage = await llm.call_llm_json(
        [{"role": "user", "content": "Return JSON"}]
    )

    assert result["summary"].startswith("Mock response")
    assert usage["model"] == "mock"


@pytest.mark.asyncio
async def test_bedrock_claude_sonnet_request_preserves_completion_contract(
    monkeypatch,
) -> None:
    monkeypatch.setattr(llm.settings, "BEDROCK_ENABLED", True)
    monkeypatch.setattr(
        llm.settings,
        "BEDROCK_MODEL_ID",
        "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )
    monkeypatch.setattr(llm.settings, "AWS_REGION", "us-east-1")
    monkeypatch.setattr(llm.settings, "AWS_ACCESS_KEY_ID", "test-access-key")
    monkeypatch.setattr(llm.settings, "AWS_SECRET_ACCESS_KEY", "test-secret-key")
    monkeypatch.setattr(llm.settings, "AWS_SESSION_TOKEN", "test-session-token")

    captured: dict = {}

    async def fake_completion(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(
            usage=SimpleNamespace(
                prompt_tokens=12,
                completion_tokens=8,
                total_tokens=20,
            ),
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='```json\n{"items": ["ok"]}\n```'
                    )
                )
            ],
        )

    monkeypatch.setattr(llm.litellm, "acompletion", fake_completion)
    original_messages = [{"role": "user", "content": "Return the result"}]

    result, usage = await llm.call_llm_json(original_messages)

    assert result == {"items": ["ok"]}
    assert usage == {
        "prompt_tokens": 12,
        "completion_tokens": 8,
        "total_tokens": 20,
        "model": "bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    }
    assert captured["model"] == (
        "bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    )
    assert captured["aws_region_name"] == "us-east-1"
    assert captured["aws_access_key_id"] == "test-access-key"
    assert captured["aws_secret_access_key"] == "test-secret-key"
    assert captured["aws_session_token"] == "test-session-token"
    assert "response_format" not in captured
    assert captured["messages"][0]["role"] == "system"
    assert "valid JSON object" in captured["messages"][0]["content"]
    assert original_messages == [{"role": "user", "content": "Return the result"}]


@pytest.mark.asyncio
async def test_bedrock_rejects_non_sonnet_model(monkeypatch) -> None:
    monkeypatch.setattr(llm.settings, "BEDROCK_ENABLED", True)
    monkeypatch.setattr(llm.settings, "BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")

    with pytest.raises(RuntimeError, match="Only Anthropic Claude Sonnet"):
        await llm.call_llm([{"role": "user", "content": "Hello"}])


def test_bedrock_json_parser_rejects_non_object() -> None:
    with pytest.raises(RuntimeError, match="invalid JSON"):
        llm._parse_json_object('["not", "an", "object"]')


def test_bedrock_uses_default_aws_credential_chain_when_keys_are_absent(
    monkeypatch,
) -> None:
    monkeypatch.setattr(llm.settings, "AWS_ACCESS_KEY_ID", "")
    monkeypatch.setattr(llm.settings, "AWS_SECRET_ACCESS_KEY", "")
    monkeypatch.setattr(llm.settings, "AWS_SESSION_TOKEN", "")
    monkeypatch.setattr(llm.settings, "AWS_REGION", "us-west-2")

    assert llm._bedrock_kwargs() == {"aws_region_name": "us-west-2"}


def test_enabled_bedrock_requires_positive_model_pricing() -> None:
    with pytest.raises(ValidationError, match="must be positive"):
        Settings(
            _env_file=None,
            BEDROCK_ENABLED=True,
            BEDROCK_MODEL_ID=(
                "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
            ),
            BEDROCK_INPUT_COST_PER_MILLION=0,
            BEDROCK_OUTPUT_COST_PER_MILLION=0,
        )
