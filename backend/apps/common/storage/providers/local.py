"""
Local filesystem storage provider for DatavionOS.

Provides a development and self-hosted storage backend.

Production deployments may replace this provider with:

- AWS S3
- Azure Blob Storage
- Google Cloud Storage
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from apps.common.storage.backend import (
    StorageBackend,
)
from apps.common.storage.exceptions import (
    StorageDeleteError,
    StorageDownloadError,
    StorageFileNotFoundError,
    StorageUploadError,
)
from apps.common.storage.models import (
    StoredFile,
)
from apps.common.storage.types import (
    FileContent,
    StoragePath,
)


class LocalStorageProvider(
    StorageBackend,
):
    """
    Local filesystem storage implementation.
    """

    def __init__(
        self,
        root_path: str | Path,
    ) -> None:
        """
        Initialize local storage.

        Args:
            root_path:
                Base filesystem directory.
        """

        self.root_path = Path(
            root_path,
        )

        self.root_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _resolve_path(
        self,
        path: StoragePath,
    ) -> Path:
        """
        Resolve a storage path safely.
        """

        resolved = (self.root_path / path).resolve()

        if not str(resolved).startswith(
            str(self.root_path.resolve()),
        ):
            raise ValueError(
                "Invalid storage path.",
            )

        return resolved

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

        try:
            destination = self._resolve_path(
                path,
            )

            if destination.exists() and not overwrite:
                raise FileExistsError(
                    f"File already exists: {path}",
                )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = bytes(
                content,
            )

            destination.write_bytes(
                data,
            )

            return StoredFile(
                path=path,
                name=destination.name,
                size=len(data),
                checksum=sha256(
                    data,
                ).hexdigest(),
            )

        except Exception as exc:
            raise StorageUploadError(
                str(exc),
            ) from exc

    def download(
        self,
        path: StoragePath,
    ) -> bytes:
        """
        Download file content.
        """

        try:
            source = self._resolve_path(
                path,
            )

            if not source.exists():
                raise StorageFileNotFoundError(
                    path,
                )

            return source.read_bytes()

        except StorageFileNotFoundError:
            raise

        except Exception as exc:
            raise StorageDownloadError(
                str(exc),
            ) from exc

    def delete(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Delete a file.
        """

        try:
            target = self._resolve_path(
                path,
            )

            if not target.exists():
                return False

            target.unlink()

            return True

        except Exception as exc:
            raise StorageDeleteError(
                str(exc),
            ) from exc

    def exists(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Check file existence.
        """

        return self._resolve_path(
            path,
        ).exists()

    def get_url(
        self,
        path: StoragePath,
        *,
        expires_in: int | None = None,
    ) -> str:
        """
        Return local file reference.

        Local storage does not generate signed URLs.
        """

        del expires_in

        return str(
            self._resolve_path(
                path,
            ),
        )

    def size(
        self,
        path: StoragePath,
    ) -> int:
        """
        Return file size.
        """

        target = self._resolve_path(
            path,
        )

        if not target.exists():
            raise StorageFileNotFoundError(
                path,
            )

        return target.stat().st_size


__all__: tuple[str, ...] = ("LocalStorageProvider",)
