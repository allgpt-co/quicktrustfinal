"""Field-level encryption for PII using AES-256-GCM.

Encrypts sensitive fields (emails, names, credentials) before database storage.
Decrypts on retrieval.  If no key is configured, fields are stored in plaintext
with a warning.

Encrypted values are prefixed with ``enc:`` so legacy plaintext data is handled
transparently during migration.

Usage:
    from app.core.field_encryption import encrypt_field, decrypt_field

    encrypted = encrypt_field("user@example.com")
    # => "enc:<iv_hex>:<tag_hex>:<ciphertext_hex>"

    original = decrypt_field(encrypted)
    # => "user@example.com"

Config:
    FIELD_ENCRYPTION_KEY  — 64-char hex string (32 bytes).
        Generate with: python -c "import os; print(os.urandom(32).hex())"
    FIELD_HMAC_KEY        — 64-char hex string for blind indexes.
        Generate with: python -c "import os; print(os.urandom(32).hex())"
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.config import get_settings

logger = logging.getLogger(__name__)

ALGORITHM = "aes-256-gcm"
PREFIX = "enc:"


def _get_key() -> bytes | None:
    settings = get_settings()
    key_hex = getattr(settings, "FIELD_ENCRYPTION_KEY", "")
    if not key_hex:
        return None
    try:
        key = bytes.fromhex(key_hex)
        if len(key) != 32:
            logger.error("FIELD_ENCRYPTION_KEY must be 32 bytes (64 hex chars), got %d", len(key))
            return None
        return key
    except ValueError:
        logger.error("FIELD_ENCRYPTION_KEY is not valid hex")
        return None


def _get_hmac_key() -> bytes | None:
    settings = get_settings()
    key_hex = getattr(settings, "FIELD_HMAC_KEY", "")
    if not key_hex:
        return None
    try:
        return bytes.fromhex(key_hex)
    except ValueError:
        return None


def encrypt_field(plaintext: str) -> str:
    """Encrypt a string using AES-256-GCM. Returns prefixed ciphertext."""
    if not plaintext:
        return plaintext

    key = _get_key()
    if key is None:
        logger.debug("No encryption key configured, storing plaintext")
        return plaintext

    nonce = os.urandom(12)  # 96-bit nonce for GCM
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

    # Format: enc:<nonce_hex>:<ciphertext_hex>
    return f"{PREFIX}{nonce.hex()}:{ciphertext.hex()}"


def decrypt_field(ciphertext: str) -> str:
    """Decrypt an AES-256-GCM encrypted field. Handles legacy plaintext."""
    if not ciphertext:
        return ciphertext

    if not ciphertext.startswith(PREFIX):
        return ciphertext  # Legacy plaintext — return as-is

    key = _get_key()
    if key is None:
        raise ValueError("FIELD_ENCRYPTION_KEY required to decrypt data")

    stripped = ciphertext[len(PREFIX):]
    parts = stripped.split(":", 1)
    if len(parts) != 2:
        raise ValueError("Invalid encrypted field format")

    nonce_hex, ct_hex = parts
    nonce = bytes.fromhex(nonce_hex)
    ct = bytes.fromhex(ct_hex)

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ct, None)
    return plaintext.decode("utf-8")


def create_blind_index(value: str) -> str:
    """Create an HMAC-SHA256 blind index for searchable encrypted fields.

    Used for email lookups: store the hash alongside the encrypted email
    so you can do ``WHERE email_hash = create_blind_index(email)`` without
    decrypting every row.
    """
    hmac_key = _get_hmac_key()
    if hmac_key is None:
        # Fallback: SHA-256 hash (deterministic but less secure without HMAC key)
        return hashlib.sha256(value.lower().strip().encode("utf-8")).hexdigest()

    return hmac.new(
        hmac_key, value.lower().strip().encode("utf-8"), hashlib.sha256
    ).hexdigest()


def encrypt_sensitive_fields(data: dict, fields: list[str]) -> dict:
    """Encrypt specified fields in a dictionary before DB storage."""
    result = {**data}
    for field in fields:
        if field in result and isinstance(result[field], str) and result[field]:
            result[field] = encrypt_field(result[field])
    return result


def decrypt_sensitive_fields(data: dict, fields: list[str]) -> dict:
    """Decrypt specified fields in a dictionary after DB retrieval."""
    result = {**data}
    for field in fields:
        if field in result and isinstance(result[field], str) and result[field]:
            result[field] = decrypt_field(result[field])
    return result
