from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt


def create_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)

    if expires_delta is None:
        expires_at = now + timedelta(minutes=15)
    else:
        expires_at = now + expires_delta

    to_encode.update({"iat": now, "exp": expires_at})
    return jwt.encode(to_encode, algorithm="HS256", key="something")
