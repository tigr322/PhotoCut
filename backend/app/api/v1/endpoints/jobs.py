import uuid

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, get_auth_context
from app.core.config import settings
from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobOut
from app.services.file_service import FileService
from app.services.job_service import JobService
from app.services.storage import LocalStorageService

router = APIRouter()


def _to_job_out(job: Job) -> JobOut:
    result_url = f"{settings.api_v1_prefix}/files/{job.result_file_id}" if job.result_file_id else None
    return JobOut(
        id=job.id,
        type=job.type,
        status=job.status,
        input_file_id=job.input_file_id,
        result_file_id=job.result_file_id,
        options=job.options_json or {},
        error_message=job.error_message,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        result_url=result_url,
    )


@router.post("/remove-background", response_model=JobOut)
async def remove_background_job(
    file: UploadFile = File(...),
    output_format: str = Form(default="png"),
    resize_width: int | None = Form(default=None, ge=1, le=10000),
    resize_height: int | None = Form(default=None, ge=1, le=10000),
    crop_x: int | None = Form(default=None, ge=0),
    crop_y: int | None = Form(default=None, ge=0),
    crop_width: int | None = Form(default=None, ge=1, le=10000),
    crop_height: int | None = Form(default=None, ge=1, le=10000),
    fit_width: int | None = Form(default=None, ge=1, le=10000),
    fit_height: int | None = Form(default=None, ge=1, le=10000),
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
) -> JobOut:
    storage = LocalStorageService(settings.storage_root)
    file_service = FileService(db, storage, settings.max_upload_size_mb)
    input_file = await file_service.create_input_file(user_id=auth.user.id, upload=file)

    options = {
        "output_format": output_format.lower(),
        "resize_width": resize_width,
        "resize_height": resize_height,
        "crop_x": crop_x,
        "crop_y": crop_y,
        "crop_width": crop_width,
        "crop_height": crop_height,
        "fit_width": fit_width,
        "fit_height": fit_height,
    }
    options = {key: value for key, value in options.items() if value is not None}

    job = JobService(db).create_remove_background_job(
        user_id=auth.user.id,
        api_key_id=auth.api_key.id if auth.api_key else None,
        input_file_id=input_file.id,
        options=options,
    )
    return _to_job_out(job)


@router.get("", response_model=list[JobOut])
def list_jobs(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
) -> list[JobOut]:
    jobs = JobService(db).list_jobs(user_id=auth.user.id, limit=limit, offset=offset)
    return [_to_job_out(job) for job in jobs]


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: uuid.UUID, auth: AuthContext = Depends(get_auth_context), db: Session = Depends(get_db)) -> JobOut:
    job = JobService(db).get_job(user_id=auth.user.id, job_id=job_id)
    return _to_job_out(job)
