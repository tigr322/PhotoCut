import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApiKeyCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ApiKeyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    key_prefix: str
    last_used_at: datetime | None
    revoked_at: datetime | None
    created_at: datetime


class ApiKeyCreateResponse(BaseModel):
    id: uuid.UUID
    name: str
    key_prefix: str
    key: str
    created_at: datetime
