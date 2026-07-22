"""Amazon Bedrock Claude Sonnet access through LiteLLM.

LiteLLM keeps the existing provider-neutral completion response contract while
routing every real request to Amazon Bedrock. When Bedrock is disabled, the
functions return deterministic mock responses so development and CI do not
require AWS model access.
"""

import json
import logging
import re
from typing import Any

import litellm
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Keep provider logging quiet in normal application operation.
litellm.set_verbose = False

_MOCK_USAGE = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "model": "mock",
}


def _bedrock_enabled() -> bool:
    return settings.BEDROCK_ENABLED


def _bedrock_model(model: str | None = None) -> str:
    """Return a LiteLLM Bedrock model route for Claude Sonnet."""
    model_id = (model or settings.BEDROCK_MODEL_ID).strip()
    normalized = model_id.removeprefix("bedrock/")
    lowered = normalized.lower()
    if not normalized:
        raise RuntimeError("BEDROCK_MODEL_ID is required when Bedrock is enabled")
    if (
        "anthropic" not in lowered
        or "claude" not in lowered
        or "sonnet" not in lowered
    ):
        raise RuntimeError("Only Anthropic Claude Sonnet models are supported")
    return f"bedrock/{normalized}"


def _bedrock_kwargs() -> dict[str, str]:
    """Build LiteLLM Bedrock parameters without disabling boto3's IAM chain."""
    kwargs = {"aws_region_name": settings.AWS_REGION}
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
    if settings.AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN
    return kwargs


def _extract_usage(response) -> dict:
    """Extract token usage from a normalized LiteLLM response."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    return {
        "prompt_tokens": getattr(usage, "prompt_tokens", 0) or 0,
        "completion_tokens": getattr(usage, "completion_tokens", 0) or 0,
        "total_tokens": getattr(usage, "total_tokens", 0) or 0,
    }


# ---------------------------------------------------------------------------
# Mock responses for development / CI
# ---------------------------------------------------------------------------

_MOCK_TEXT = (
    "This is a mock LLM response. Enable Amazon Bedrock and configure an "
    "Anthropic Claude Sonnet model to use real AI features."
)

_MOCK_JSON: dict = {
    "items": [],
    "summary": "Mock response — Amazon Bedrock is disabled.",
    "confidence": 0.0,
}

_JSON_INSTRUCTION = (
    "Return only one valid JSON object. Do not wrap it in Markdown or add text "
    "before or after the JSON."
)


def _messages_for_json(messages: list[dict]) -> list[dict]:
    """Copy messages and add the provider-neutral JSON response instruction."""
    prepared = [dict(message) for message in messages]
    for message in prepared:
        if message.get("role") == "system" and isinstance(message.get("content"), str):
            message["content"] = (
                f"{message['content'].rstrip()}\n\n{_JSON_INSTRUCTION}"
            )
            return prepared
    prepared.insert(0, {"role": "system", "content": _JSON_INSTRUCTION})
    return prepared


def _parse_json_object(content: Any) -> dict:
    """Parse a JSON object, tolerating a Markdown fence from the provider."""
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("Bedrock returned an empty JSON response")

    text = content.strip()
    candidates = [text]
    fence = chr(96) * 3
    fenced = re.search(
        rf"{fence}(?:json)?\s*(.*?)\s*{fence}",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if fenced:
        candidates.insert(0, fenced.group(1).strip())

    decoder = json.JSONDecoder()
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            object_start = candidate.find("{")
            if object_start < 0:
                continue
            try:
                parsed, _ = decoder.raw_decode(candidate[object_start:])
            except json.JSONDecodeError:
                continue
        if isinstance(parsed, dict):
            return parsed

    raise RuntimeError("Bedrock returned invalid JSON")


async def call_llm(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> tuple[str, dict]:
    """Return text content and normalized usage information.

    Falls back to a mock response when Amazon Bedrock is disabled.
    """
    if not _bedrock_enabled():
        logger.debug("Amazon Bedrock is disabled — returning mock text response.")
        return _MOCK_TEXT, _MOCK_USAGE.copy()

    model = _bedrock_model(model)
    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=120,
            num_retries=2,
            **_bedrock_kwargs(),
        )
        usage = _extract_usage(response)
        usage["model"] = model
        return response.choices[0].message.content, usage
    except Exception as exc:
        raise RuntimeError(f"Bedrock call failed: {str(exc)}") from exc


async def call_llm_json(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
) -> tuple[dict, dict]:
    """Return a JSON object and normalized usage information.

    Falls back to a mock response when Amazon Bedrock is disabled. The helper
    uses a provider-neutral JSON instruction because Bedrock structured output
    requires a concrete JSON schema, while existing agents return different
    object shapes through this shared function.
    """
    if not _bedrock_enabled():
        logger.debug("Amazon Bedrock is disabled — returning mock JSON response.")
        return _MOCK_JSON.copy(), _MOCK_USAGE.copy()

    model = _bedrock_model(model)
    try:
        response = await litellm.acompletion(
            model=model,
            messages=_messages_for_json(messages),
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=120,
            num_retries=2,
            **_bedrock_kwargs(),
        )
        usage = _extract_usage(response)
        usage["model"] = model
        content = response.choices[0].message.content
        return _parse_json_object(content), usage
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Bedrock call failed: {str(exc)}") from exc
