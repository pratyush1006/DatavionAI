"""
Platform storage contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from io import BufferedIOBase
from typing import (
    BinaryIO,
    Protocol,
    runtime_checkable,
)


@dataclass(
    frozen=True,
    slots=True,
)
class StorageObject:
    """
    Storage object descriptor.
    """

    bucket: str

    key: str

    content_type: str

    size: int

    etag: str | None = None

    version: str | None = None

    created_at: datetime | None = None

    metadata: dict[str, str] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class UploadOptions:
    """
    Upload options.
    """

    overwrite: bool = False

    versioning: bool = True

    tenant_id: str | None = None

    organization_id: str | None = None

    metadata: dict[str, str] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class SignedUrl:
    """
    Temporary URL for client access.
    """

    url: str

    expires_at: datetime


@runtime_checkable
class StorageProvider(
    Protocol,
):
    """
    Platform storage abstraction.
    """

    def exists(
        self,
        bucket: str,
        key: str,
    ) -> bool:
        """
        Determine whether an object exists.
        """

    def upload(
        self,
        bucket: str,
        key: str,
        stream: BinaryIO,
        *,
        content_type: str,
        options: UploadOptions | None = None,
    ) -> StorageObject:
        """
        Upload an object.
        """

    def download(
        self,
        bucket: str,
        key: str,
    ) -> BufferedIOBase:
        """
        Download an object stream.
        """

    def delete(
        self,
        bucket: str,
        key: str,
    ) -> bool:
        """
        Delete an object.
        """

    def copy(
        self,
        source_bucket: str,
        source_key: str,
        destination_bucket: str,
        destination_key: str,
    ) -> StorageObject:
        """
        Copy an object.
        """

    def move(
        self,
        source_bucket: str,
        source_key: str,
        destination_bucket: str,
        destination_key: str,
    ) -> StorageObject:
        """
        Move an object.
        """

    def list(
        self,
        bucket: str,
        *,
        prefix: str | None = None,
    ) -> list[StorageObject]:
        """
        List objects.
        """

    def metadata(
        self,
        bucket: str,
        key: str,
    ) -> StorageObject:
        """
        Return object metadata.
        """

    def create_signed_download_url(
        self,
        bucket: str,
        key: str,
        *,
        expires_in_seconds: int = 900,
    ) -> SignedUrl:
        """
        Create a temporary download URL.
        """

    def create_signed_upload_url(
        self,
        bucket: str,
        key: str,
        *,
        expires_in_seconds: int = 900,
    ) -> SignedUrl:
        """
        Create a temporary upload URL.
        """


__all__ = [
    "StorageObject",
    "UploadOptions",
    "SignedUrl",
    "StorageProvider",
]
