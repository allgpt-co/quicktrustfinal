"""LiteLLM wrapper for configurable LLM access with token tracking.

When ``OPENAI_API_KEY`` (or another provider key) is configured, calls
are routed through LiteLLM to the real model.  When no key is set the
functions return deterministic mock responses so the application still
works in development / CI without an API key.
"""

import json
import logging

import litellm
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Configure LiteLLM
litellm.set_verbose = False

_MOCK_USAGE = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "model": "mock",
}


def _has_api_key() -> bool:
    """Return True if any LLM provider key is configured."""
    return bool(settings.OPENAI_API_KEY)


def _extract_usage(response) -> dict:
    """Extract token usage from LiteLLM response."""
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
    "This is a mock LLM response. Configure OPENAI_API_KEY (or another "
    "LiteLLM-supported provider key) to enable real AI features."
)

_MOCK_JSON: dict = {
    "items": [],
    "summary": "Mock response — no LLM API key configured.",
    "confidence": 0.0,
}


async def call_llm(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> tuple[str, dict]:
    """Returns (content, usage_info).

    Falls back to a mock response when no API key is available.
    """
    if not _has_api_key():
        logger.debug("No LLM API key configured — returning mock text response.")
        return _MOCK_TEXT, _MOCK_USAGE.copy()

    model = model or settings.LITELLM_MODEL
    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=120,
            num_retries=2,
        )
        usage = _extract_usage(response)
        usage["model"] = model
        return response.choices[0].message.content, usage
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {str(e)}") from e


async def call_llm_json(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
) -> tuple[dict, dict]:
    """Call LLM with JSON response format. Returns (parsed_json, usage_info).

    Falls back to a mock JSON response when no API key is available.
    """
    if not _has_api_key():
        logger.debug("No LLM API key configured — returning mock JSON response.")
        return _MOCK_JSON.copy(), _MOCK_USAGE.copy()

    model = model or settings.LITELLM_MODEL
    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
            timeout=120,
            num_retries=2,
        )
        usage = _extract_usage(response)
        usage["model"] = model
        content = response.choices[0].message.content
        return json.loads(content), usage
    except json.JSONDecodeError as e:
        raise RuntimeError(f"LLM returned invalid JSON: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {str(e)}") from e
