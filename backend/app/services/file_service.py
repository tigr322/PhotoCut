import mimetypes
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.models.file import StoredFile
from app.services.storage import StorageInterface

ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


class FileService:
    def __init__(self, db: Session, storage: StorageInterface, max_upload_size_mb: int):
        self.db = db
        self.storage = storage
        self.max_upload_size_bytes = max_upload_size_mb * 1024 * 1024

    async def create_input_file(self, user_id: int, upload: UploadFile) -> StoredFile:
        mime_type = upload.content_type or ""
        if mime_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type. Use PNG, JPEG or WEBP",
            )

        content = await upload.read()
        if not content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")
        if len(content) > self.max_upload_size_bytes:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

        try:
            Image.open(BytesIO(content)).verify()
        except (UnidentifiedImageError, OSError) as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image payload") from exc

        original_name = Path(upload.filename or "upload").name
        extension = Path(original_name).suffix.lstrip(".")
        if not extension:
            guessed = mimetypes.guess_extension(mime_type)
            extension = (guessed or ".bin").lstrip(".")

        saved = self.storage.save_bytes(content, folder="uploads", extension=extension)

        db_file = StoredFile(
            user_id=user_id,
            original_name=original_name,
            stored_name=saved.stored_name,
            storage_path=saved.storage_path,
            mime_type=mime_type,
            size_bytes=saved.size_bytes,
        )
        self.db.add(db_file)
        self.db.flush()
        return db_file

    def create_result_file(
        self,
        user_id: int,
        original_name: str,
        content: bytes,
        mime_type: str,
        extension: str,
    ) -> StoredFile:
        saved = self.storage.save_bytes(content, folder="results", extension=extension)
        db_file = StoredFile(
            user_id=user_id,
            original_name=original_name,
            stored_name=saved.stored_name,
            storage_path=saved.storage_path,
            mime_type=mime_type,
            size_bytes=saved.size_bytes,
        )
        self.db.add(db_file)
        self.db.flush()
        return db_file
