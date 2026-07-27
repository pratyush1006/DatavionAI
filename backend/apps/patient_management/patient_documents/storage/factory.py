"""
Storage provider factory.
"""

from __future__ import annotations

from django.conf import settings

from apps.patient_management.patient_documents.storage.base import (
    StorageProvider,
)
from apps.patient_management.patient_documents.storage.registry import (
    StorageRegistry,
)


class StorageProviderFactory:
    """
    Factory responsible for resolving the configured
    storage provider.
    """

    @classmethod
    def get_provider(
        cls,
        backend: str | None = None,
    ) -> StorageProvider:
        """
        Return the configured storage provider.
        """

        backend = backend or settings.DOCUMENT_STORAGE_BACKEND

        provider_class = StorageRegistry.get(
            backend,
        )

        return provider_class()


__all__ = [
    "StorageProviderFactory",
]
