import hashlib
import hmac
import json
import time
import urllib.parse

import pytest

from api.core.exceptions import UnauthorizedError
from api.core.security import TelegramAuthService
from tests.conftest import TEST_BOT_TOKEN, build_init_data


@pytest.fixture
def auth_service() -> TelegramAuthService:
    return TelegramAuthService(TEST_BOT_TOKEN)


class TestValidateValidInitData:
    async def test_returns_dict_with_user_fields(self, auth_service):
        init_data = build_init_data(
            bot_token=TEST_BOT_TOKEN,
            telegram_id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            language_code="ru",
        )
        result = auth_service.validate(init_data)
        assert result["id"] == 123456789
        assert result["first_name"] == "John"
        assert result["last_name"] == "Doe"
        assert result["username"] == "johndoe"
        assert result["language_code"] == "ru"
        assert "auth_date" in result


class TestValidateMissingHash:
    async def test_raises_when_hash_absent(self, auth_service):
        params = {
            "user": json.dumps({"id": 1}),
            "auth_date": str(int(time.time())),
        }
        init_data = urllib.parse.urlencode(params)
        with pytest.raises(UnauthorizedError, match="missing_hash"):
            auth_service.validate(init_data)


class TestValidateInvalidHash:
    async def test_raises_on_tampered_hash(self, auth_service):
        init_data = build_init_data(
            bot_token=TEST_BOT_TOKEN,
            telegram_id=123456789,
        )
        init_data = init_data.replace(
            init_data.split("hash=")[1][:10],
            "0000000000",
        )
        with pytest.raises(UnauthorizedError, match="invalid_hash"):
            auth_service.validate(init_data)


class TestValidateExpiredAuthDate:
    async def test_raises_when_auth_date_too_old(self, auth_service):
        expired_time = int(time.time()) - 200000
        init_data = build_init_data(
            bot_token=TEST_BOT_TOKEN,
            telegram_id=123456789,
            auth_date=expired_time,
        )
        with pytest.raises(UnauthorizedError, match="auth_data_expired"):
            auth_service.validate(init_data, max_age=86400)


class TestValidateMissingUserData:
    async def test_raises_when_user_field_absent(self, auth_service):
        auth_date = str(int(time.time()))
        params = {"auth_date": auth_date}

        data_check_string = f"auth_date={auth_date}"
        secret_key = hmac.new(b"WebAppData", TEST_BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        params["hash"] = computed_hash
        init_data = urllib.parse.urlencode(params)

        with pytest.raises(UnauthorizedError, match="missing_user_data"):
            auth_service.validate(init_data)


class TestValidateReturnsUserData:
    async def test_returns_defaults_for_missing_optional_fields(self, auth_service):
        auth_date = int(time.time())
        user_data = json.dumps({"id": 42}, separators=(",", ":"))
        params = {
            "auth_date": str(auth_date),
            "user": user_data,
        }

        data_check_pairs = []
        for key in sorted(params.keys()):
            data_check_pairs.append(f"{key}={params[key]}")
        data_check_string = "\n".join(data_check_pairs)

        secret_key = hmac.new(b"WebAppData", TEST_BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        params["hash"] = computed_hash
        init_data = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

        result = auth_service.validate(init_data)
        assert result["id"] == 42
        assert result["first_name"] == ""
        assert result["last_name"] == ""
        assert result["username"] == ""
        assert result["language_code"] == "en"
        assert result["auth_date"] == auth_date
