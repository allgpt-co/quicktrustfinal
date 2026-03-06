"""LiteLLM wrapper for configurable LLM access with token tracking."""
import json

import litellm
from app.config import get_settings

settings = get_settings()

# Configure LiteLLM
litellm.set_verbose = False


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


async def call_llm(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> tuple[str, dict]:
    """Returns (content, usage_info)."""
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
    """Call LLM with JSON response format. Returns (parsed_json, usage_info)."""
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
