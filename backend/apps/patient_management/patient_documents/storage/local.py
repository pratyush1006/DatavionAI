"""
Local filesystem storage provider.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from django.conf import settings

from apps.patient_management.patient_documents.constants import (
    StorageBackend,
)
from apps.patient_management.patient_documents.storage.base import (
    StorageProvider,
)
from apps.patient_management.patient_documents.storage.exceptions import (
    FileNotFound,
)
from apps.patient_management.patient_documents.storage.registry import (
    StorageRegistry,
)
from apps.patient_management.patient_documents.storage.types import (
    StorageObject,
)
from apps.patient_management.patient_documents.storage.utils import (
    guess_content_type,
)


class LocalStorageProvider(StorageProvider):
    """
    Local filesystem implementation.
    """

    @property
    def media_root(self) -> Path:
        return Path(
            settings.MEDIA_ROOT,
        )

    def upload(
        self,
        *,
        path: str,
        file,
        content_type: str,
    ) -> StorageObject:
        destination = self.media_root / path

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with destination.open("wb") as output:
            for chunk in file.chunks():
                output.write(
                    chunk,
                )

        return self.metadata(
            path=path,
        )

    def download(
        self,
        *,
        path: str,
    ):
        file_path = self.media_root / path

        if not file_path.exists():
            raise FileNotFound(path)

        return file_path.open("rb")

    def delete(
        self,
        *,
        path: str,
    ) -> None:
        file_path = self.media_root / path

        if file_path.exists():
            file_path.unlink()

    def exists(
        self,
        *,
        path: str,
    ) -> bool:
        return (self.media_root / path).exists()

    def metadata(
        self,
        *,
        path: str,
    ) -> StorageObject:
        file_path = self.media_root / path

        if not file_path.exists():
            raise FileNotFound(path)

        return StorageObject(
            path=path,
            size=file_path.stat().st_size,
            mime_type=guess_content_type(
                file_path.name,
            ),
        )

    def generate_signed_url(
        self,
        *,
        path: str,
        expires_in: int = 300,
    ) -> str:
        """
        Local storage uses streaming responses.
        """

        return ""

    def copy(
        self,
        *,
        source: str,
        destination: str,
    ) -> StorageObject:
        shutil.copy2(
            self.media_root / source,
            self.media_root / destination,
        )

        return self.metadata(
            path=destination,
        )

    def move(
        self,
        *,
        source: str,
        destination: str,
    ) -> StorageObject:
        shutil.move(
            self.media_root / source,
            self.media_root / destination,
        )

        return self.metadata(
            path=destination,
        )


StorageRegistry.register(
    StorageBackend.LOCAL,
    LocalStorageProvider,
)


__all__ = [
    "LocalStorageProvider",
]
