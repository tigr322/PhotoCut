import abc
import os
import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StoredObject:
    stored_name: str
    storage_path: str
    size_bytes: int


class StorageInterface(abc.ABC):
    @abc.abstractmethod
    def save_bytes(self, content: bytes, folder: str, extension: str) -> StoredObject:
        raise NotImplementedError

    @abc.abstractmethod
    def read_bytes(self, storage_path: str) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def absolute_path(self, storage_path: str) -> Path:
        raise NotImplementedError


class LocalStorageService(StorageInterface):
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.root_path.mkdir(parents=True, exist_ok=True)

    def _safe_extension(self, extension: str) -> str:
        ext = extension.lower().strip().lstrip(".")
        return ext or "bin"

    def save_bytes(self, content: bytes, folder: str, extension: str) -> StoredObject:
        folder_clean = folder.strip("/") or "uploads"
        ext = self._safe_extension(extension)
        stored_name = f"{uuid.uuid4().hex}.{ext}"

        target_folder = (self.root_path / folder_clean).resolve()
        if not str(target_folder).startswith(str(self.root_path)):
            raise ValueError("Invalid storage folder")

        target_folder.mkdir(parents=True, exist_ok=True)
        full_path = target_folder / stored_name

        with full_path.open("wb") as f:
            f.write(content)

        storage_path = os.path.relpath(full_path, self.root_path)
        return StoredObject(stored_name=stored_name, storage_path=storage_path, size_bytes=len(content))

    def read_bytes(self, storage_path: str) -> bytes:
        full_path = self.absolute_path(storage_path)
        with full_path.open("rb") as f:
            return f.read()

    def absolute_path(self, storage_path: str) -> Path:
        candidate = (self.root_path / storage_path).resolve()
        if not str(candidate).startswith(str(self.root_path)):
            raise ValueError("Invalid storage path")
        return candidate
