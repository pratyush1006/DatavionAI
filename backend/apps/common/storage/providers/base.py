"""
Base storage backend implementation.

Defines shared behavior for concrete storage backends.

Supported implementations:

- Local filesystem
- AWS S3
- Azure Blob Storage
- Google Cloud Storage
"""

from __future__ import annotations

from abc import (
    abstractmethod,
)

from apps.common.storage.backend import (
    StorageBackend,
)
from apps.common.storage.models import StoredFile
from apps.common.storage.types import FileContent, StoragePath


class BaseStorageBackend(
    StorageBackend,
):
    """
    Abstract base class for storage backends.

    Concrete providers must implement
    storage-specific operations.
    """

    @abstractmethod
    def upload(
        self,
        path: StoragePath,
        content: FileContent,
        *,
        overwrite: bool = False,
    ) -> StoredFile:
        """
        Upload file.

        Returns:
            Storage identifier.
        """

        raise NotImplementedError

    @abstractmethod
    def download(
        self,
        path: StoragePath,
    ) -> bytes:
        """
        Download file.
        """

        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Delete file.
        """

        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Check file existence.
        """

        raise NotImplementedError

    @abstractmethod
    def get_url(
        self,
        path: StoragePath,
        *,
        expires_in: int | None = None,
    ) -> str:
        """
        Generate file URL.

        Private storage may generate
        signed URLs.
        """

        raise NotImplementedError

    @abstractmethod
    def size(
        self,
        path: StoragePath,
    ) -> int:
        """Return file size in bytes."""

        raise NotImplementedError


__all__: tuple[str, ...] = ("BaseStorageBackend",)
