"""
Storage backend abstraction for DatavionOS.

Defines the contract that all storage providers must implement.

Supported future providers:

- Local filesystem
- AWS S3
- Azure Blob Storage
- Google Cloud Storage

Business applications should use StorageClient instead of
directly interacting with providers.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)

from apps.common.storage.models import (
    StoredFile,
)
from apps.common.storage.types import (
    FileContent,
    StoragePath,
)


class StorageBackend(
    ABC,
):
    """
    Abstract storage backend.

    All storage providers must implement this interface.
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
        Upload a file.

        Returns:
            Stored file metadata.
        """

    @abstractmethod
    def download(
        self,
        path: StoragePath,
    ) -> bytes:
        """
        Download file content.
        """

    @abstractmethod
    def delete(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Delete a stored file.
        """

    @abstractmethod
    def exists(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Check whether a file exists.
        """

    @abstractmethod
    def get_url(
        self,
        path: StoragePath,
        *,
        expires_in: int | None = None,
    ) -> str:
        """
        Generate an access URL.

        Providers may return signed URLs.
        """

    @abstractmethod
    def size(
        self,
        path: StoragePath,
    ) -> int:
        """
        Return file size in bytes.
        """


__all__: tuple[str, ...] = ("StorageBackend",)
