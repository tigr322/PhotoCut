import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, get_auth_context
from app.core.config import settings
from app.db.session import get_db
from app.models.file import StoredFile
from app.services.storage import LocalStorageService

router = APIRouter()


@router.get("/{file_id}")
def get_file(
    file_id: uuid.UUID,
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
) -> FileResponse:
    db_file = db.get(StoredFile, file_id)
    if not db_file or db_file.user_id != auth.user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    storage = LocalStorageService(settings.storage_root)
    try:
        full_path = storage.absolute_path(db_file.storage_path)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file path") from exc

    if not full_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on disk")

    return FileResponse(
        path=str(full_path),
        media_type=db_file.mime_type,
        filename=db_file.original_name,
    )
