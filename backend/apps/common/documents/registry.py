"""
Document registry for DatavionOS.

Maintains registered document storage providers and processors.

The registry keeps the document framework extensible without
coupling to specific storage vendors or AI processors.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from apps.common.documents.exceptions import (
    DocumentAlreadyRegisteredError,
    DocumentHandlerNotFoundError,
)


class DocumentStorageProvider(
    Protocol,
):
    """
    Contract for document storage providers.
    """

    name: str

    def upload(
        self,
        document: object,
    ) -> object:
        """
        Upload document.
        """

    def download(
        self,
        storage_key: str,
    ) -> object:
        """
        Download document.
        """


class DocumentProcessor(
    Protocol,
):
    """
    Contract for document processors.

    Examples:

    - OCR
    - AI extraction
    - Classification
    - Embedding generation
    """

    name: str

    def process(
        self,
        document: object,
    ) -> object:
        """
        Process document.
        """


class DocumentRegistry:
    """
    Central document registry.

    Supports:

    - Storage provider registration
    - Processor registration
    - Runtime discovery
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._storage_providers: dict[
            str,
            DocumentStorageProvider,
        ] = {}

        self._processors: dict[
            str,
            DocumentProcessor,
        ] = {}

    def register_storage(
        self,
        provider: DocumentStorageProvider,
    ) -> None:
        """
        Register storage provider.
        """

        if provider.name in self._storage_providers:
            raise DocumentAlreadyRegisteredError(
                (f"Document storage provider '{provider.name}' already registered."),
            )

        self._storage_providers[provider.name] = provider

    def register_processor(
        self,
        processor: DocumentProcessor,
    ) -> None:
        """
        Register document processor.
        """

        if processor.name in self._processors:
            raise DocumentAlreadyRegisteredError(
                (f"Document processor '{processor.name}' already registered."),
            )

        self._processors[processor.name] = processor

    def get_storage(
        self,
        name: str,
    ) -> DocumentStorageProvider:
        """
        Return storage provider.
        """

        provider = self._storage_providers.get(
            name,
        )

        if provider is None:
            raise DocumentHandlerNotFoundError(
                (f"Document storage provider '{name}' does not exist."),
            )

        return provider

    def get_processor(
        self,
        name: str,
    ) -> DocumentProcessor:
        """
        Return document processor.
        """

        processor = self._processors.get(
            name,
        )

        if processor is None:
            raise DocumentHandlerNotFoundError(
                (f"Document processor '{name}' does not exist."),
            )

        return processor

    def storage_providers(
        self,
    ) -> Iterable[DocumentStorageProvider]:
        """
        Return storage providers.
        """

        return self._storage_providers.values()

    def processors(
        self,
    ) -> Iterable[DocumentProcessor]:
        """
        Return processors.
        """

        return self._processors.values()

    def clear(
        self,
    ) -> None:
        """
        Remove all registrations.
        """

        self._storage_providers.clear()

        self._processors.clear()


document_registry = DocumentRegistry()


__all__: tuple[str, ...] = (
    "DocumentProcessor",
    "DocumentRegistry",
    "DocumentStorageProvider",
    "document_registry",
)
