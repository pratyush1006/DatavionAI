"""
Storage provider registry.
"""

from __future__ import annotations

from apps.patient_management.patient_documents.storage.base import (
    StorageProvider,
)


class StorageRegistry:
    """
    Registry of storage provider implementations.
    """

    _providers: dict[
        str,
        type[StorageProvider],
    ] = {}

    @classmethod
    def register(
        cls,
        backend: str,
        provider: type[StorageProvider],
    ) -> None:
        """
        Register a storage provider.
        """

        cls._providers[backend] = provider

    @classmethod
    def get(
        cls,
        backend: str,
    ) -> type[StorageProvider]:
        """
        Return a registered provider.
        """

        try:
            return cls._providers[backend]
        except KeyError as exc:
            raise ValueError(
                f"Storage provider '{backend}' is not registered."
            ) from exc

    @classmethod
    def registered_backends(
        cls,
    ) -> tuple[str, ...]:
        """
        Return all registered backends.
        """

        return tuple(
            cls._providers.keys(),
        )


__all__ = [
    "StorageRegistry",
]
