import time

import httpx
from jose import JWTError, jwt

from app.config import get_settings
from app.core.exceptions import UnauthorizedError

settings = get_settings()

_jwks_cache: dict | None = None
_jwks_cache_time: float = 0
JWKS_CACHE_TTL = 300  # 5 minutes


async def get_jwks() -> dict:
    global _jwks_cache, _jwks_cache_time
    if _jwks_cache is not None and (time.monotonic() - _jwks_cache_time) < JWKS_CACHE_TTL:
        return _jwks_cache

    jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    async with httpx.AsyncClient() as client:
        resp = await client.get(jwks_url)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        _jwks_cache_time = time.monotonic()
        return _jwks_cache


def clear_jwks_cache():
    global _jwks_cache, _jwks_cache_time
    _jwks_cache = None
    _jwks_cache_time = 0


async def decode_token(token: str) -> dict:
    try:
        jwks = await get_jwks()
        # Get the header to find the key id
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # Find the matching key
        rsa_key = None
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                rsa_key = key
                break

        if rsa_key is None:
            # Try refreshing JWKS cache
            clear_jwks_cache()
            jwks = await get_jwks()
            for key in jwks.get("keys", []):
                if key.get("kid") == kid:
                    rsa_key = key
                    break

        if rsa_key is None:
            raise UnauthorizedError("Unable to find signing key")

        issuer = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"

        # Accept tokens issued for the API client, web client, or default Keycloak audience
        valid_audiences = [settings.KEYCLOAK_CLIENT_ID, "quicktrust-web", "account"]

        # Accept tokens issued by localhost (browser) or Docker hostname (internal)
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=valid_audiences,
                issuer=issuer,
                options={"verify_aud": True},
            )
        except JWTError:
            # Retry with localhost issuer for Docker environments
            localhost_issuer = f"http://localhost:8080/realms/{settings.KEYCLOAK_REALM}"
            if localhost_issuer != issuer:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=valid_audiences,
                    issuer=localhost_issuer,
                    options={"verify_aud": True},
                )
            else:
                raise

        # Check token blacklist (revoked tokens)
        jti = payload.get("jti")
        if jti:
            try:
                from app.core.token_blacklist import is_token_blacklisted

                if await is_token_blacklisted(jti):
                    raise UnauthorizedError("Token has been revoked")
            except UnauthorizedError:
                raise
            except Exception:
                pass  # Redis unavailable — allow token (fail open for availability)

        return payload

    except JWTError as e:
        raise UnauthorizedError(f"Invalid token: {str(e)}")
    except httpx.HTTPError:
        raise UnauthorizedError("Could not validate credentials (Keycloak unreachable)")
