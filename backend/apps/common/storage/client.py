"""
Storage client for DatavionOS.

Provides the application-facing storage API.

Business modules should use StorageClient instead of directly
accessing storage providers.
"""

from __future__ import annotations

from apps.common.storage.backend import (
    StorageBackend,
)
from apps.common.storage.models import (
    StoredFile,
)
from apps.common.storage.types import (
    FileContent,
    StoragePath,
)


class StorageClient:
    """
    Unified storage client.

    Delegates operations to the configured storage backend.

    Example:

        storage.upload(
            "tenant/files/report.pdf",
            data,
        )
    """

    def __init__(
        self,
        backend: StorageBackend,
    ) -> None:
        """
        Initialize storage client.

        Args:
            backend:
                Configured storage provider.
        """

        self.backend = backend

    def upload(
        self,
        path: StoragePath,
        content: FileContent,
        *,
        overwrite: bool = False,
    ) -> StoredFile:
        """
        Upload a file.
        """

        return self.backend.upload(
            path,
            content,
            overwrite=overwrite,
        )

    def download(
        self,
        path: StoragePath,
    ) -> bytes:
        """
        Download a file.
        """

        return self.backend.download(
            path,
        )

    def delete(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Delete a file.
        """

        return self.backend.delete(
            path,
        )

    def exists(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Check file existence.
        """

        return self.backend.exists(
            path,
        )

    def url(
        self,
        path: StoragePath,
        *,
        expires_in: int | None = None,
    ) -> str:
        """
        Generate file access URL.
        """

        return self.backend.get_url(
            path,
            expires_in=expires_in,
        )

    def size(
        self,
        path: StoragePath,
    ) -> int:
        """
        Return file size.
        """

        return self.backend.size(
            path,
        )


__all__: tuple[str, ...] = ("StorageClient",)
