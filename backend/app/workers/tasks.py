import uuid
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.file import StoredFile
from app.models.job import Job, JobStatus
from app.services.file_service import FileService
from app.services.image_processing_service import ImageProcessingService
from app.services.storage import LocalStorageService


def process_remove_background_job(job_id: str) -> None:
    db: Session = SessionLocal()
    job_uuid = uuid.UUID(job_id)
    storage = LocalStorageService(settings.storage_root)

    try:
        job = db.get(Job, job_uuid)
        if job is None:
            return

        job.status = JobStatus.PROCESSING
        job.started_at = datetime.now(UTC)
        db.commit()

        input_file = db.get(StoredFile, job.input_file_id)
        if input_file is None:
            raise RuntimeError("Input file not found")

        source_bytes = storage.read_bytes(input_file.storage_path)
        processed = ImageProcessingService.remove_background(source_bytes, job.options_json or {})

        original_stem = Path(input_file.original_name).stem or "image"
        result_name = f"{original_stem}_processed.{processed.extension}"

        file_service = FileService(db, storage, settings.max_upload_size_mb)
        result_file = file_service.create_result_file(
            user_id=job.user_id,
            original_name=result_name,
            content=processed.content,
            mime_type=processed.mime_type,
            extension=processed.extension,
        )

        job.result_file_id = result_file.id
        job.status = JobStatus.COMPLETED
        job.error_message = None
        job.completed_at = datetime.now(UTC)

        db.commit()
    except Exception as exc:
        db.rollback()
        failed_job = db.get(Job, job_uuid)
        if failed_job is not None:
            failed_job.status = JobStatus.FAILED
            failed_job.error_message = str(exc)[:1000]
            failed_job.completed_at = datetime.now(UTC)
            db.commit()
        raise
    finally:
        db.close()
