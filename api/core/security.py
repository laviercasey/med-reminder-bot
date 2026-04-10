import hashlib
import hmac
import json
import time
from urllib.parse import parse_qs, unquote

from api.core.exceptions import UnauthorizedError


class TelegramAuthService:
    def __init__(self, bot_token: str):
        self._bot_token = bot_token
        self._secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()

    def validate(self, init_data: str, max_age: int = 86400) -> dict:
        parsed = parse_qs(init_data, keep_blank_values=True)

        if "hash" not in parsed:
            raise UnauthorizedError("missing_hash")

        received_hash = parsed.pop("hash")[0]

        data_check_pairs = []
        for key in sorted(parsed.keys()):
            value = parsed[key][0]
            data_check_pairs.append(f"{key}={value}")

        data_check_string = "\n".join(data_check_pairs)

        computed_hash = hmac.new(
            self._secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(computed_hash, received_hash):
            raise UnauthorizedError("invalid_hash")

        auth_date_str = parsed.get("auth_date", [None])[0]
        if auth_date_str is None:
            raise UnauthorizedError("missing_auth_date")

        try:
            auth_date = int(auth_date_str)
        except ValueError:
            raise UnauthorizedError("invalid_auth_date")

        if time.time() - auth_date > max_age:
            raise UnauthorizedError("auth_data_expired")

        user_data_str = parsed.get("user", [None])[0]
        if user_data_str is None:
            raise UnauthorizedError("missing_user_data")

        try:
            user_data = json.loads(unquote(user_data_str))
        except (json.JSONDecodeError, TypeError):
            raise UnauthorizedError("invalid_user_data")

        return {
            "id": user_data.get("id"),
            "first_name": user_data.get("first_name", ""),
            "last_name": user_data.get("last_name", ""),
            "username": user_data.get("username", ""),
            "language_code": user_data.get("language_code", "en"),
            "auth_date": auth_date,
        }
