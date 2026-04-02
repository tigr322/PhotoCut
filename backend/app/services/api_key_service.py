import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import generate_api_key, hash_api_key
from app.models.api_key import ApiKey


class ApiKeyService:
    def __init__(self, db: Session):
        self.db = db

    def list_keys(self, user_id: int) -> list[ApiKey]:
        return list(
            self.db.scalars(
                select(ApiKey)
                .where(ApiKey.user_id == user_id)
                .order_by(ApiKey.created_at.desc())
            )
        )

    def create_key(self, user_id: int, name: str) -> tuple[ApiKey, str]:
        raw_key, key_prefix = generate_api_key()
        key = ApiKey(
            user_id=user_id,
            name=name,
            key_prefix=key_prefix,
            key_hash=hash_api_key(raw_key),
        )
        self.db.add(key)
        self.db.commit()
        self.db.refresh(key)
        return key, raw_key

    def revoke_key(self, user_id: int, key_id: uuid.UUID) -> None:
        key = self.db.get(ApiKey, key_id)
        if not key or key.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
        if key.revoked_at is not None:
            return
        key.revoked_at = datetime.now(UTC)
        self.db.commit()
