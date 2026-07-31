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
        *,
        file,
        storage_key: str,
        content_type: str,
    ):
        """
        Upload file.

        Returns:
            Storage identifier.
        """

        raise NotImplementedError

    @abstractmethod
    def download(
        self,
        *,
        storage_key: str,
    ):
        """
        Download file.
        """

        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        """
        Delete file.
        """

        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        *,
        storage_key: str,
    ) -> bool:
        """
        Check file existence.
        """

        raise NotImplementedError

    @abstractmethod
    def get_url(
        self,
        *,
        storage_key: str,
        expires_in: int | None = None,
    ) -> str:
        """
        Generate file URL.

        Private storage may generate
        signed URLs.
        """

        raise NotImplementedError


__all__: tuple[str, ...] = ("BaseStorageBackend",)
