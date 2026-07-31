"""
Storage service layer for DatavionOS.

Provides application services for storage operations.

Responsibilities:

- Upload files
- Download files
- Delete files
- Register storage backends
- Register storage processors

Business domains must depend on this layer.

Storage must not depend on business applications.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.storage.backend import (
    StorageBackend,
)
from apps.common.storage.exceptions import (
    StorageDeleteError,
    StorageDownloadError,
    StorageUploadError,
)
from apps.common.storage.models import (
    StoredFile,
)
from apps.common.storage.registry import (
    StorageProcessor,
    storage_registry,
)


class StorageService:
    """
    Storage application service.

    Provides:

    - Upload
    - Download
    - Delete
    - Backend registration
    - Processor registration
    """

    def upload(
        self,
        file: StoredFile,
        *,
        backend: str,
    ) -> object:
        """
        Upload file.
        """

        try:
            storage_backend = storage_registry.get_backend(
                backend,
            )

            return storage_backend.upload(
                file.path,
                file.metadata,
            )

        except Exception as exc:
            raise StorageUploadError(
                str(exc),
            ) from exc

    def download(
        self,
        storage_key: str,
        *,
        backend: str,
    ) -> object:
        """
        Download file.
        """

        try:
            storage_backend = storage_registry.get_backend(
                backend,
            )

            return storage_backend.download(
                storage_key,
            )

        except Exception as exc:
            raise StorageDownloadError(
                str(exc),
            ) from exc

    def delete(
        self,
        storage_key: str,
        *,
        backend: str,
    ) -> None:
        """
        Delete file.
        """

        try:
            storage_backend = storage_registry.get_backend(
                backend,
            )

            storage_backend.delete(
                storage_key,
            )

        except Exception as exc:
            raise StorageDeleteError(
                str(exc),
            ) from exc

    def register_backend(
        self,
        backend: StorageBackend,
    ) -> None:
        """
        Register storage backend.
        """

        storage_registry.register_backend(
            backend,
        )

    def register_processor(
        self,
        processor: StorageProcessor,
    ) -> None:
        """
        Register storage processor.
        """

        storage_registry.register_processor(
            processor,
        )

    def backends(
        self,
    ) -> Iterable[StorageBackend]:
        """
        Return registered storage backends.
        """

        return storage_registry.backends()

    def processors(
        self,
    ) -> Iterable[StorageProcessor]:
        """
        Return registered processors.
        """

        return storage_registry.processors()


storage_service = StorageService()


__all__: tuple[str, ...] = (
    "StorageService",
    "storage_service",
)
