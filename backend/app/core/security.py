"""Application-managed password hashing and JWT access-token security."""

from datetime import datetime, timedelta, timezone
import re
import uuid

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError, VerificationError
from argon2.low_level import Type
from jose import JWTError, jwt

from app.config import get_settings
from app.core.exceptions import BadRequestError, UnauthorizedError

settings = get_settings()

JWT_ALGORITHM = "HS256"
_password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
    type=Type.ID,
)
# Used for nonexistent/unset accounts so authentication performs a password hash
# verification regardless of whether the email is registered.
_DUMMY_PASSWORD_HASH = _password_hasher.hash("QuickTrust dummy password 9! do not use")


def validate_password_strength(password: str, email: str | None = None) -> None:
    """Enforce the password policy formerly configured in the identity provider."""
    errors: list[str] = []
    if len(password) < 12:
        errors.append("at least 12 characters")
    if not re.search(r"[A-Z]", password):
        errors.append("an uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("a lowercase letter")
    if not re.search(r"\d", password):
        errors.append("a number")
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("a special character")
    if email and password.casefold() in {email.casefold(), email.split("@", 1)[0].casefold()}:
        errors.append("a value different from your email")
    if errors:
        raise BadRequestError("Password must contain " + ", ".join(errors) + ".")


def hash_password(password: str, email: str | None = None) -> str:
    validate_password_strength(password, email)
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str | None) -> bool:
    """Verify an Argon2id hash while using a dummy hash for unset credentials."""
    encoded_hash = password_hash or _DUMMY_PASSWORD_HASH
    try:
        return _password_hasher.verify(encoded_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def password_needs_rehash(password_hash: str) -> bool:
    try:
        return _password_hasher.check_needs_rehash(password_hash)
    except (InvalidHashError, VerificationError):
        return True


def create_access_token(user) -> tuple[str, int]:
    """Create a short-lived signed JWT containing stable authorization claims."""
    if not settings.SECRET_KEY:
        raise RuntimeError("SECRET_KEY must be configured before issuing access tokens")

    now = datetime.now(timezone.utc)
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.full_name,
        "role": user.role,
        "org_id": str(user.org_id),
        "type": "access",
        "jti": str(uuid.uuid4()),
        "iat": now.timestamp(),
        "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM), expires_in


async def decode_token(token: str) -> dict:
    """Validate a QuickTrust access token and its revocation status."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
            options={"require_exp": True, "require_iat": True, "require_sub": True},
        )
        if payload.get("type") != "access":
            raise JWTError("Token is not an access token")

        jti = payload.get("jti")
        if jti:
            try:
                from app.core.token_blacklist import is_token_blacklisted

                if await is_token_blacklisted(jti):
                    raise UnauthorizedError("Token has been revoked")
            except UnauthorizedError:
                raise
            except Exception:
                pass

        subject = payload.get("sub")
        issued_at = payload.get("iat")
        if subject and issued_at:
            try:
                from app.core.token_blacklist import is_user_token_revoked

                if await is_user_token_revoked(subject, float(issued_at)):
                    raise UnauthorizedError("Token has been revoked")
            except UnauthorizedError:
                raise
            except Exception:
                pass

        return payload
    except UnauthorizedError:
        raise
    except JWTError as exc:
        raise UnauthorizedError(f"Invalid token: {exc}") from exc
