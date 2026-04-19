import time
from unittest.mock import MagicMock

import jwt as pyjwt
import pytest

from api.core.config import api_config
from api.services.auth import jwt_service


@pytest.fixture
def fake_user():
    user = MagicMock()
    user.id = 42
    user.telegram_id = 123456789
    return user


class TestIssueAccessToken:
    def test_contains_required_claims(self, fake_user):
        token, expires_at = jwt_service.issue_access(fake_user)
        decoded = pyjwt.decode(
            token,
            api_config.jwt_secret,
            algorithms=["HS256"],
            issuer=api_config.jwt_issuer,
            audience=api_config.jwt_audience,
        )
        assert decoded["sub"] == str(fake_user.telegram_id)
        assert decoded["uid"] == fake_user.id
        assert decoded["type"] == "access"
        assert decoded["iss"] == api_config.jwt_issuer
        assert decoded["aud"] == api_config.jwt_audience
        assert "iat" in decoded
        assert "exp" in decoded
        assert decoded["exp"] - decoded["iat"] == api_config.jwt_access_ttl
        assert isinstance(expires_at, int)
        assert expires_at == decoded["exp"]

    def test_verifies_with_same_secret(self, fake_user):
        token, _ = jwt_service.issue_access(fake_user)
        claims = jwt_service.decode_access(token)
        assert claims["sub"] == str(fake_user.telegram_id)


class TestDecodeAccess:
    def test_rejects_wrong_signature(self, fake_user):
        token, _ = jwt_service.issue_access(fake_user)
        tampered = token[:-4] + ("AAAA" if token[-4:] != "AAAA" else "BBBB")
        with pytest.raises(jwt_service.InvalidTokenError):
            jwt_service.decode_access(tampered)

    def test_rejects_expired_token(self, fake_user, monkeypatch):
        real_time = time.time
        past = int(real_time()) - api_config.jwt_access_ttl - 60
        monkeypatch.setattr(jwt_service.time, "time", lambda: past)
        token, _ = jwt_service.issue_access(fake_user)
        monkeypatch.setattr(jwt_service.time, "time", real_time)
        with pytest.raises(jwt_service.TokenExpiredError):
            jwt_service.decode_access(token)

    def test_rejects_wrong_issuer(self, fake_user):
        now = int(time.time())
        payload = {
            "sub": str(fake_user.telegram_id),
            "uid": fake_user.id,
            "type": "access",
            "iat": now,
            "exp": now + 900,
            "iss": "evil-issuer",
            "aud": api_config.jwt_audience,
        }
        token = pyjwt.encode(payload, api_config.jwt_secret, algorithm="HS256")
        with pytest.raises(jwt_service.InvalidTokenError):
            jwt_service.decode_access(token)

    def test_rejects_wrong_audience(self, fake_user):
        now = int(time.time())
        payload = {
            "sub": str(fake_user.telegram_id),
            "uid": fake_user.id,
            "type": "access",
            "iat": now,
            "exp": now + 900,
            "iss": api_config.jwt_issuer,
            "aud": "evil-audience",
        }
        token = pyjwt.encode(payload, api_config.jwt_secret, algorithm="HS256")
        with pytest.raises(jwt_service.InvalidTokenError):
            jwt_service.decode_access(token)

    def test_rejects_non_access_type(self, fake_user):
        now = int(time.time())
        payload = {
            "sub": str(fake_user.telegram_id),
            "uid": fake_user.id,
            "type": "refresh",
            "iat": now,
            "exp": now + 900,
            "iss": api_config.jwt_issuer,
            "aud": api_config.jwt_audience,
        }
        token = pyjwt.encode(payload, api_config.jwt_secret, algorithm="HS256")
        with pytest.raises(jwt_service.WrongTokenTypeError):
            jwt_service.decode_access(token)


class TestGenerateRefreshToken:
    def test_is_url_safe_and_long_enough(self):
        token = jwt_service.generate_refresh_token()
        assert len(token) >= 40
        allowed = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        )
        assert set(token).issubset(allowed)

    def test_is_unique(self):
        tokens = {jwt_service.generate_refresh_token() for _ in range(10)}
        assert len(tokens) == 10


class TestHashRefresh:
    def test_is_deterministic_sha256_hex(self):
        token = "kQ3Z-example-refresh-token-value-1234567890"
        hashed_a = jwt_service.hash_refresh(token)
        hashed_b = jwt_service.hash_refresh(token)
        assert hashed_a == hashed_b
        assert len(hashed_a) == 64
        assert all(c in "0123456789abcdef" for c in hashed_a)

    def test_different_inputs_yield_different_hashes(self):
        a = jwt_service.hash_refresh("token-a")
        b = jwt_service.hash_refresh("token-b")
        assert a != b
