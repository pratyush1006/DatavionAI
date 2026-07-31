"""
AWS S3 storage backend for DatavionOS.

Provides an S3-compatible storage adapter.

AWS dependencies remain optional so the kernel
can run without boto3 in local environments.

Production deployments can enable boto3 and configure
credentials through environment variables or secret management.
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


class S3StorageBackend(
    BaseStorageBackend,
):
    """
    AWS S3 storage implementation.

    The S3 client is injected to keep this layer
    testable and provider-independent.
    """

    def __init__(
        self,
        *,
        bucket_name: str,
        client: object,
    ) -> None:
        """
        Initialize S3 storage.
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
        Upload file to S3.
        """

        try:
            if not overwrite and self.exists(path):
                raise FileExistsError(
                    f"File already exists: {path}",
                )

            data = bytes(content)

            self.client.put_object(
                Bucket=self.bucket_name,
                Key=path,
                Body=data,
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
        Download file from S3.
        """

        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=path,
            )

            return response["Body"].read()

        except Exception as exc:
            raise StorageDownloadError(
                str(exc),
            ) from exc

    def delete(
        self,
        path: StoragePath,
    ) -> bool:
        """
        Delete file from S3.
        """

        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=path,
            )

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
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=path,
            )

            return True

        except Exception:
            return False

    def get_url(
        self,
        path: StoragePath,
        *,
        expires_in: int | None = None,
    ) -> str:
        """
        Generate signed S3 URL.
        """

        try:
            return self.client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": path,
                },
                ExpiresIn=expires_in or 3600,
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
        Return S3 object size.
        """

        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=path,
            )

            return int(
                response["ContentLength"],
            )

        except Exception as exc:
            raise StorageNotFoundError(
                str(exc),
            ) from exc


__all__: tuple[str, ...] = ("S3StorageBackend",)
