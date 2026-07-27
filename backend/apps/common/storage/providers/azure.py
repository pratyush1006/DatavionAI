"""
Azure Blob Storage provider for DatavionOS.

Provides an Azure Blob Storage adapter.

The Azure SDK is injected instead of being imported directly,
keeping the storage kernel provider-independent.
"""

from __future__ import annotations

from hashlib import sha256

from apps.common.storage.backend import (
    StorageBackend,
)
from apps.common.storage.exceptions import (
    StorageConnectionError,
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


class AzureBlobStorageProvider(
    StorageBackend,
):
    """
    Azure Blob Storage implementation.

    The container client is injected to avoid hard dependency
    on Azure SDK during local development.
    """

    def __init__(
        self,
        *,
        container_name: str,
        client: object,
    ) -> None:
        """
        Initialize Azure Blob storage.

        Args:
            container_name:
                Azure blob container.

            client:
                Azure container client.
        """

        self.container_name = container_name
        self.client = client

    def upload(
        self,
        path: StoragePath,
        content: FileContent,
        *,
        overwrite: bool = False,
    ) -> StoredFile:
        """
        Upload file to Azure Blob Storage.
        """

        try:
            blob = self.client.get_blob_client(
                blob=path,
            )

            data = bytes(content)

            blob.upload_blob(
                data,
                overwrite=overwrite,
            )

            return StoredFile(
                path=path,
                name=path.split("/")[-1],
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
            blob = self.client.get_blob_client(
                blob=path,
            )

            return blob.download_blob().readall()

        except Exception as exc:
            raise StorageDownloadError(
                str(exc),
            ) from exc

    def delete(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Delete a blob.
        """

        try:
            blob = self.client.get_blob_client(
                blob=path,
            )

            blob.delete_blob()

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
        Check blob existence.
        """

        try:
            blob = self.client.get_blob_client(
                blob=path,
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
        Return blob URL.

        Signed URL generation can be added through Azure SAS
        tokens.
        """

        del expires_in

        try:
            blob = self.client.get_blob_client(
                blob=path,
            )

            return blob.url

        except Exception as exc:
            raise StorageConnectionError(
                str(exc),
            ) from exc

    def size(
        self,
        path: StoragePath,
    ) -> int:
        """
        Return blob size.
        """

        try:
            blob = self.client.get_blob_client(
                blob=path,
            )

            properties = blob.get_blob_properties()

            return int(
                properties.size,
            )

        except Exception as exc:
            raise StorageFileNotFoundError(
                str(exc),
            ) from exc


__all__: tuple[str, ...] = ("AzureBlobStorageProvider",)
