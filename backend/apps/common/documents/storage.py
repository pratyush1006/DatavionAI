"""
Document storage abstraction for DatavionOS.

Provides the runtime storage layer for documents.

Responsibilities:

- Upload documents
- Download documents
- Delete documents
- Route operations to registered storage providers

Actual storage implementations remain replaceable:

- Local filesystem
- AWS S3
- Azure Blob Storage
- Google Cloud Storage
"""

from __future__ import annotations

from apps.common.documents.exceptions import (
    DocumentDeleteError,
    DocumentDownloadError,
    DocumentUploadError,
)
from apps.common.documents.models import (
    DocumentMetadataInfo,
)
from apps.common.documents.registry import (
    document_registry,
)


class DocumentStorage:
    """
    Core document storage engine.
    """

    def upload(
        self,
        metadata: DocumentMetadataInfo,
        *,
        backend: str,
    ) -> object:
        """
        Upload document.

        Args:
            metadata:
                Document file metadata.

            backend:
                Registered storage provider.

        Returns:
            Provider upload response.
        """

        try:
            provider = document_registry.get_storage(
                backend,
            )

            return provider.upload(
                metadata,
            )

        except Exception as exc:
            raise DocumentUploadError(
                str(exc),
            ) from exc

    def download(
        self,
        storage_key: str,
        *,
        backend: str,
    ) -> object:
        """
        Download document.
        """

        try:
            provider = document_registry.get_storage(
                backend,
            )

            return provider.download(
                storage_key,
            )

        except Exception as exc:
            raise DocumentDownloadError(
                str(exc),
            ) from exc

    def delete(
        self,
        storage_key: str,
        *,
        backend: str,
    ) -> None:
        """
        Delete document.
        """

        try:
            provider = document_registry.get_storage(
                backend,
            )

            delete_method = getattr(
                provider,
                "delete",
                None,
            )

            if delete_method is not None:
                delete_method(
                    storage_key,
                )

        except Exception as exc:
            raise DocumentDeleteError(
                str(exc),
            ) from exc


document_storage = DocumentStorage()


__all__: tuple[str, ...] = (
    "DocumentStorage",
    "document_storage",
)
