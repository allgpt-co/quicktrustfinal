"""Sanitize user input before inserting into LLM prompts."""

import re


_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?above", re.IGNORECASE),
    re.compile(r"system\s*:\s*", re.IGNORECASE),
    re.compile(r"<\|im_start\|>", re.IGNORECASE),
    re.compile(r"<\|im_end\|>", re.IGNORECASE),
    re.compile(r"\[INST\]", re.IGNORECASE),
    re.compile(r"\[/INST\]", re.IGNORECASE),
    re.compile(r"<<SYS>>", re.IGNORECASE),
    re.compile(r"<</SYS>>", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+", re.IGNORECASE),
    re.compile(r"new\s+instructions?\s*:", re.IGNORECASE),
    re.compile(r"forget\s+(all\s+)?(previous|above|prior)", re.IGNORECASE),
]


def sanitize_for_prompt(text: str, max_length: int = 2000) -> str:
    """Sanitize user input before inserting into LLM prompts."""
    if not text:
        return ""
    text = text[:max_length]
    for pattern in _INJECTION_PATTERNS:
        text = pattern.sub("[FILTERED]", text)
    return text


def wrap_user_data(data: str, label: str = "USER_DATA") -> str:
    """Wrap user data in delimiters to separate it from instructions."""
    return f"<{label}>\n{sanitize_for_prompt(data)}\n</{label}>"
