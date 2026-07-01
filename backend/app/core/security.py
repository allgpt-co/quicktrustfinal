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

        # Accept tokens issued for the API client, web client, or default Keycloak audience.
        # python-jose audience param only accepts a single string, so we verify
        # the audience manually after decoding.
        valid_audiences = {settings.KEYCLOAK_CLIENT_ID, "quicktrust-web", "account"}

        issuers = [issuer]
        if settings.APP_ENV != "production":
            localhost_issuer = f"http://localhost:8080/realms/{settings.KEYCLOAK_REALM}"
            if localhost_issuer != issuer:
                issuers.append(localhost_issuer)

        last_jwt_error: JWTError | None = None
        for allowed_issuer in issuers:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    issuer=allowed_issuer,
                    options={"verify_aud": False},
                )
                break
            except JWTError as e:
                last_jwt_error = e
        else:
            raise last_jwt_error or JWTError("Token issuer is not accepted")

        # Manual audience check: token aud can be a string, list, or absent.
        # Keycloak often omits "aud" and uses "azp" (authorized party) instead.
        token_aud = payload.get("aud") or []
        if isinstance(token_aud, str):
            token_aud = [token_aud]
        azp = payload.get("azp")
        if azp:
            token_aud.append(azp)
        if token_aud and not valid_audiences.intersection(token_aud):
            raise JWTError("Token audience not accepted")

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

        # Check user-level token revocation (password change, admin force-logout)
        sub = payload.get("sub")
        iat = payload.get("iat")
        if sub and iat:
            try:
                from app.core.token_blacklist import is_user_token_revoked

                if await is_user_token_revoked(sub, int(iat)):
                    raise UnauthorizedError("Token has been revoked (user-level)")
            except UnauthorizedError:
                raise
            except Exception:
                pass  # Fail open

        return payload

    except JWTError as e:
        raise UnauthorizedError(f"Invalid token: {str(e)}")
    except httpx.HTTPError:
        raise UnauthorizedError("Could not validate credentials (Keycloak unreachable)")
