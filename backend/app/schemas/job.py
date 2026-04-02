import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.job import JobStatus


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    status: JobStatus
    input_file_id: uuid.UUID
    result_file_id: uuid.UUID | None
    options: dict
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    result_url: str | None = None
