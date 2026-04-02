import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenError(Exception):
    pass


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str | int, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise TokenError("Invalid or expired token") from exc


def generate_api_key() -> tuple[str, str]:
    raw = f"pk_live_{secrets.token_urlsafe(32)}"
    prefix = raw[:16]
    return raw, prefix


def hash_api_key(raw_key: str) -> str:
    return hashlib.sha256(f"{raw_key}{settings.api_key_pepper}".encode("utf-8")).hexdigest()


def verify_api_key(raw_key: str, key_hash: str) -> bool:
    computed = hash_api_key(raw_key)
    return hmac.compare_digest(computed, key_hash)
