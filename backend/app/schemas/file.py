import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    original_name: str
    mime_type: str
    size_bytes: int
    created_at: datetime
