"""
Document services for DatavionOS.

Provides the application service layer for document operations.

Business applications should use this service instead of
directly accessing storage, registry, or processors.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.documents.models import (
    DocumentMetadataInfo,
)
from apps.common.documents.registry import (
    DocumentProcessor,
    DocumentStorageProvider,
    document_registry,
)
from apps.common.documents.storage import (
    document_storage,
)


class DocumentService:
    """
    Document application service.

    Provides:

    - Document upload
    - Document download
    - Document deletion
    - Storage registration
    - Processor registration
    """

    def upload(
        self,
        metadata: DocumentMetadataInfo,
        *,
        backend: str,
    ) -> object:
        """
        Upload document.
        """

        return document_storage.upload(
            metadata,
            backend=backend,
        )

    def download(
        self,
        storage_key: str,
        *,
        backend: str,
    ) -> object:
        """
        Download document.
        """

        return document_storage.download(
            storage_key,
            backend=backend,
        )

    def delete(
        self,
        storage_key: str,
        *,
        backend: str,
    ) -> None:
        """
        Delete document.
        """

        document_storage.delete(
            storage_key,
            backend=backend,
        )

    def register_storage(
        self,
        provider: DocumentStorageProvider,
    ) -> None:
        """
        Register storage provider.
        """

        document_registry.register_storage(
            provider,
        )

    def register_processor(
        self,
        processor: DocumentProcessor,
    ) -> None:
        """
        Register document processor.
        """

        document_registry.register_processor(
            processor,
        )

    def storage_providers(
        self,
    ) -> Iterable[DocumentStorageProvider]:
        """
        Return registered storage providers.
        """

        return document_registry.storage_providers()

    def processors(
        self,
    ) -> Iterable[DocumentProcessor]:
        """
        Return registered processors.
        """

        return document_registry.processors()


document_service = DocumentService()


__all__: tuple[str, ...] = (
    "DocumentService",
    "document_service",
)
