import hashlib


def compute_sha256(data: bytes) -> str:
    """Compute SHA-256 hash of data and return as hex string with algorithm prefix."""
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def verify_hash(data: bytes, expected_hash: str) -> bool:
    """Verify data integrity against stored hash."""
    if not expected_hash:
        return False
    actual = compute_sha256(data)
    return actual == expected_hash
