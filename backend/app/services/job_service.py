import uuid

from fastapi import HTTPException, status
from rq import Queue
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.redis import get_redis_connection
from app.models.job import Job, JobStatus


class JobService:
    def __init__(self, db: Session):
        self.db = db

    def create_remove_background_job(
        self,
        user_id: int,
        api_key_id: uuid.UUID | None,
        input_file_id: uuid.UUID,
        options: dict,
    ) -> Job:
        job = Job(
            user_id=user_id,
            api_key_id=api_key_id,
            type="remove_background",
            status=JobStatus.PENDING,
            input_file_id=input_file_id,
            options_json=options,
        )
        self.db.add(job)
        self.db.flush()

        queue = Queue(settings.rq_queue, connection=get_redis_connection())
        queue.enqueue("app.workers.tasks.process_remove_background_job", str(job.id), job_timeout=1800)

        job.status = JobStatus.QUEUED
        self.db.commit()
        self.db.refresh(job)
        return job

    def list_jobs(self, user_id: int, limit: int = 50, offset: int = 0) -> list[Job]:
        return list(
            self.db.scalars(
                select(Job)
                .where(Job.user_id == user_id)
                .order_by(Job.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )

    def get_job(self, user_id: int, job_id: uuid.UUID) -> Job:
        job = self.db.get(Job, job_id)
        if not job or job.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        return job
