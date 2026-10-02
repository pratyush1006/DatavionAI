"""
Patient document storage boundary.

The patient document domain owns document metadata, references,
permissions, and document relationships.

Physical file storage is delegated to canonical common storage.
"""

from __future__ import annotations

from apps.common.storage.client import StorageClient
from apps.common.storage.config import get_storage_client


class PatientDocumentStorage:
    """Application-facing patient document storage gateway."""

    @staticmethod
    def _storage() -> StorageClient:
        return get_storage_client()

    def download(
        self,
        *,
        storage_key: str,
    ) -> bytes:
        return self._storage().download(
            storage_key,
        )

    def delete(
        self,
        *,
        storage_key: str,
    ) -> bool:
        return self._storage().delete(
            storage_key,
        )


patient_document_storage = PatientDocumentStorage()


__all__ = (
    "PatientDocumentStorage",
    "patient_document_storage",
)
