"""
Canonical Django storage backend.

Connects DatavionOS StorageBackend to Django default_storage.
"""

from __future__ import annotations

import inspect
from typing import Any

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from apps.common.storage.backend import StorageBackend
from apps.common.storage.models import StoredFile
from apps.common.storage.types import FileContent, StoragePath


class DjangoStorageBackend(StorageBackend):
    """StorageBackend implementation backed by Django storage."""

    def __init__(
        self,
        storage: Any = None,
    ) -> None:
        self.storage = default_storage if storage is None else storage

    @staticmethod
    def _to_bytes(
        content: FileContent,
    ) -> bytes:
        if isinstance(content, bytes):
            return content

        if isinstance(content, bytearray):
            return bytes(content)

        if isinstance(content, memoryview):
            return content.tobytes()

        if hasattr(content, "read"):
            position = None

            try:
                position = content.tell()
            except Exception:
                pass

            data = content.read()

            if position is not None:
                try:
                    content.seek(position)
                except Exception:
                    pass

            if isinstance(data, bytes):
                return data

            return bytes(data)

        return bytes(content)

    @staticmethod
    def _build_stored_file(
        path: str,
        size: int,
    ) -> StoredFile:
        parameters = inspect.signature(
            StoredFile,
        ).parameters

        kwargs: dict[str, object] = {}

        if "path" in parameters:
            kwargs["path"] = path

        if "storage_path" in parameters:
            kwargs["storage_path"] = path

        if "size" in parameters:
            kwargs["size"] = size

        if "file_size" in parameters:
            kwargs["file_size"] = size

        if not kwargs:
            raise TypeError(
                "StoredFile does not expose a supported path/size constructor contract."
            )

        return StoredFile(
            **kwargs,
        )

    def upload(
        self,
        path: StoragePath,
        content: FileContent,
        *,
        overwrite: bool = False,
    ) -> StoredFile:
        normalized_path = str(path)

        if self.storage.exists(
            normalized_path,
        ):
            if not overwrite:
                raise FileExistsError(
                    f"Storage object already exists: {normalized_path}"
                )

            self.storage.delete(
                normalized_path,
            )

        payload = self._to_bytes(
            content,
        )

        saved_path = self.storage.save(
            normalized_path,
            ContentFile(payload),
        )

        return self._build_stored_file(
            saved_path,
            len(payload),
        )

    def download(
        self,
        path: StoragePath,
    ) -> bytes:
        with self.storage.open(
            str(path),
            "rb",
        ) as handle:
            return handle.read()

    def delete(
        self,
        path: StoragePath,
    ) -> bool:
        normalized_path = str(path)

        if not self.storage.exists(
            normalized_path,
        ):
            return False

        self.storage.delete(
            normalized_path,
        )

        return not self.storage.exists(
            normalized_path,
        )

    def exists(
        self,
        path: StoragePath,
    ) -> bool:
        return self.storage.exists(
            str(path),
        )

    def get_url(
        self,
        path: StoragePath,
        *,
        expires_in: int | None = None,
    ) -> str:
        del expires_in

        return self.storage.url(
            str(path),
        )

    def size(
        self,
        path: StoragePath,
    ) -> int:
        return self.storage.size(
            str(path),
        )


__all__ = ("DjangoStorageBackend",)
