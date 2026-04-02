from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import TokenError, decode_access_token, verify_api_key
from app.db.session import get_db
from app.models.api_key import ApiKey
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class AuthContext:
    user: User
    api_key: ApiKey | None = None


def _get_user_from_token(db: Session, token: str) -> User:
    try:
        payload = decode_access_token(token)
    except TokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.get(User, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth scheme")
    return _get_user_from_token(db, credentials.credentials)


def get_auth_context(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> AuthContext:
    if credentials:
        if credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth scheme")
        user = _get_user_from_token(db, credentials.credentials)
        return AuthContext(user=user, api_key=None)

    if x_api_key:
        key_prefix = x_api_key[:16]
        api_key = db.scalar(
            select(ApiKey)
            .where(ApiKey.key_prefix == key_prefix)
            .where(ApiKey.revoked_at.is_(None))
            .limit(1)
        )
        if api_key and verify_api_key(x_api_key, api_key.key_hash):
            user = db.get(User, api_key.user_id)
            if not user or not user.is_active:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

            api_key.last_used_at = datetime.now(UTC)
            db.commit()
            return AuthContext(user=user, api_key=api_key)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
