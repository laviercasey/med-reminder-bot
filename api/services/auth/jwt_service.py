import hashlib
import secrets
import time

import jwt as pyjwt

from api.core.config import api_config
from shared.database.models import User

ACCESS_TOKEN_TYPE = "access"
_LEEWAY_SECONDS = 5


class InvalidTokenError(Exception):
    pass


class TokenExpiredError(InvalidTokenError):
    pass


class WrongTokenTypeError(InvalidTokenError):
    pass


def issue_access(user: User) -> tuple[str, int]:
    now = int(time.time())
    expires_at = now + api_config.jwt_access_ttl
    payload = {
        "sub": str(user.telegram_id),
        "uid": user.id,
        "type": ACCESS_TOKEN_TYPE,
        "iat": now,
        "exp": expires_at,
        "iss": api_config.jwt_issuer,
        "aud": api_config.jwt_audience,
    }
    token = pyjwt.encode(payload, api_config.jwt_secret, algorithm="HS256")
    return token, expires_at


def decode_access(token: str) -> dict:
    try:
        claims = pyjwt.decode(
            token,
            api_config.jwt_secret,
            algorithms=["HS256"],
            issuer=api_config.jwt_issuer,
            audience=api_config.jwt_audience,
            leeway=_LEEWAY_SECONDS,
            options={"require": ["exp", "iat", "iss", "aud", "sub"]},
        )
    except pyjwt.ExpiredSignatureError as exc:
        raise TokenExpiredError(str(exc)) from exc
    except pyjwt.InvalidTokenError as exc:
        raise InvalidTokenError(str(exc)) from exc

    if claims.get("type") != ACCESS_TOKEN_TYPE:
        raise WrongTokenTypeError("wrong_token_type")

    return claims


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)


def hash_refresh(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
