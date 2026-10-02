"""
Storage registry for DatavionOS.

Maintains registered storage backends and processors.

The registry keeps storage infrastructure extensible without
coupling to specific storage vendors.

Examples:

Storage Backends:
- Local filesystem
- AWS S3
- Azure Blob Storage
- Google Cloud Storage

Storage Processors:
- Encryption
- Compression
- Checksum generation
- File validation
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from apps.common.storage.backend import (
    StorageBackend,
)
from apps.common.storage.exceptions import (
    StorageAlreadyRegisteredError,
    StorageHandlerNotFoundError,
)


class StorageProcessor(
    Protocol,
):
    """
    Contract for storage processors.

    Examples:

    - Encryption
    - Compression
    - Validation
    - Checksum generation
    """

    name: str

    def process(
        self,
        file: object,
    ) -> object:
        """
        Process stored file.
        """


class StorageRegistry:
    """
    Central storage registry.

    Supports:

    - Storage backend registration
    - Storage processor registration
    - Runtime discovery
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._backends: dict[
            str,
            StorageBackend,
        ] = {}

        self._processors: dict[
            str,
            StorageProcessor,
        ] = {}

    def register_backend(
        self,
        backend: StorageBackend,
    ) -> None:
        """
        Register storage backend.
        """

        name = backend.__class__.__name__

        if name in self._backends:
            raise StorageAlreadyRegisteredError(
                (f"Storage backend '{name}' already registered."),
            )

        self._backends[name] = backend

    def register_processor(
        self,
        processor: StorageProcessor,
    ) -> None:
        """
        Register storage processor.
        """

        if processor.name in self._processors:
            raise StorageAlreadyRegisteredError(
                (f"Storage processor '{processor.name}' already registered."),
            )

        self._processors[processor.name] = processor

    def get_backend(
        self,
        name: str,
    ) -> StorageBackend:
        """
        Return storage backend.
        """

        backend = self._backends.get(
            name,
        )

        if backend is None:
            raise StorageHandlerNotFoundError(
                (f"Storage backend '{name}' does not exist."),
            )

        return backend

    def get_processor(
        self,
        name: str,
    ) -> StorageProcessor:
        """
        Return storage processor.
        """

        processor = self._processors.get(
            name,
        )

        if processor is None:
            raise StorageHandlerNotFoundError(
                (f"Storage processor '{name}' does not exist."),
            )

        return processor

    def backends(
        self,
    ) -> Iterable[StorageBackend]:
        """
        Return registered storage backends.
        """

        return self._backends.values()

    def processors(
        self,
    ) -> Iterable[StorageProcessor]:
        """
        Return registered storage processors.
        """

        return self._processors.values()

    def clear(
        self,
    ) -> None:
        """
        Remove all registrations.
        """

        self._backends.clear()
        self._processors.clear()


storage_registry = StorageRegistry()


__all__: tuple[str, ...] = (
    "StorageProcessor",
    "StorageRegistry",
    "storage_registry",
)
