"""
Google Cloud Storage backend for DatavionOS.

Provides a Google Cloud Storage adapter.

The GCS client is injected instead of importing
Google SDK directly, keeping the storage kernel
provider-independent.
"""

from __future__ import annotations

from hashlib import sha256

from apps.common.storage.exceptions import (
    StorageConnectionError,
    StorageDownloadError,
    StorageNotFoundError,
    StorageUploadError,
)
from apps.common.storage.models import (
    StoredFile,
)
from apps.common.storage.providers.base import (
    BaseStorageBackend,
)
from apps.common.storage.types import (
    FileContent,
    StoragePath,
)


class GCSStorageBackend(
    BaseStorageBackend,
):
    """
    Google Cloud Storage implementation.

    The bucket client is injected to keep this
    layer testable and avoid mandatory SDK dependency.
    """

    def __init__(
        self,
        *,
        bucket_name: str,
        client: object,
    ) -> None:
        """
        Initialize GCS storage.
        """

        self.bucket_name = bucket_name
        self.client = client

    def upload(
        self,
        path: StoragePath,
        content: FileContent,
        *,
        overwrite: bool = False,
    ) -> StoredFile:
        """
        Upload file to GCS.
        """

        try:
            if not overwrite and self.exists(path):
                raise FileExistsError(
                    f"File already exists: {path}",
                )

            blob = self.client.blob(
                path,
            )

            data = bytes(
                content,
            )

            blob.upload_from_string(
                data,
            )

            return StoredFile(
                path=path,
                name=path.split("/")[-1],
                size=len(data),
                content_type="application/octet-stream",
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
        Download file from GCS.
        """

        try:
            blob = self.client.blob(
                path,
            )

            if not blob.exists():
                raise StorageNotFoundError(
                    path,
                )

            return blob.download_as_bytes()

        except StorageNotFoundError:
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
        Delete file from GCS.
        """

        try:
            blob = self.client.blob(
                path,
            )

            if not blob.exists():
                return False

            blob.delete()

            return True

        except Exception as exc:
            raise StorageConnectionError(
                str(exc),
            ) from exc

    def exists(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Check file existence.
        """

        try:
            blob = self.client.blob(
                path,
            )

            return blob.exists()

        except Exception:
            return False

    def get_url(
        self,
        path: StoragePath,
        *,
        expires_in: int | None = None,
    ) -> str:
        """
        Generate signed GCS URL.
        """

        try:
            blob = self.client.blob(
                path,
            )

            return blob.generate_signed_url(
                expiration=expires_in or 3600,
            )

        except Exception as exc:
            raise StorageConnectionError(
                str(exc),
            ) from exc

    def size(
        self,
        path: StoragePath,
    ) -> int:
        """
        Return GCS object size.
        """

        try:
            blob = self.client.blob(
                path,
            )

            blob.reload()

            return int(
                blob.size,
            )

        except Exception as exc:
            raise StorageNotFoundError(
                str(exc),
            ) from exc


__all__: tuple[str, ...] = ("GCSStorageBackend",)
