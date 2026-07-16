"""
Local filesystem storage provider.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO

from django.conf import settings

from .base import BaseStorageProvider


class LocalStorageProvider(BaseStorageProvider):
    """
    Local filesystem implementation of the storage provider.
    """

    @property
    def media_root(self) -> Path:
        """
        Return the configured media root.
        """
        return Path(settings.MEDIA_ROOT)

    def upload(
        self,
        *,
        file: BinaryIO,
        storage_key: str,
        content_type: str,
    ) -> str:
        """
        Upload a file to the local filesystem.
        """

        destination = self.media_root / storage_key
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with destination.open("wb") as output:
            shutil.copyfileobj(
                file,
                output,
            )

        return str(destination)

    def download(
        self,
        *,
        storage_key: str,
    ) -> BinaryIO:
        """
        Open a local file for reading.
        """

        return (self.media_root / storage_key).open("rb")

    def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        """
        Delete a local file.
        """

        file_path = self.media_root / storage_key

        if file_path.exists():
            file_path.unlink()

    def exists(
        self,
        *,
        storage_key: str,
    ) -> bool:
        """
        Check whether a file exists.
        """

        return (self.media_root / storage_key).exists()

    def url(
        self,
        *,
        storage_key: str,
        expires_in: int | None = None,
    ) -> str:
        """
        Return the public media URL.

        The ``expires_in`` argument is ignored for local storage.
        """

        return f"{settings.MEDIA_URL.rstrip('/')}/{storage_key}"
