"""Patient Document storage boundary.

Physical storage remains owned by the common document-storage infrastructure.
This bounded context stores only references and metadata.
"""

from __future__ import annotations

from django.conf import settings

from apps.common.storage.service import (
    document_storage,
)

DEFAULT_BACKEND = "local"


def _backend_name() -> str:
    """Return the configured document-storage provider name."""
    return str(
        getattr(
            settings,
            "DOCUMENT_STORAGE_BACKEND",
            DEFAULT_BACKEND,
        ),
    )


class PatientDocumentStorage:
    """Application-facing storage gateway for patient documents."""

    def download(
        self,
        *,
        storage_key: str,
    ) -> object:
        """Download a stored document through common storage."""
        return document_storage.download(
            storage_key,
            backend=_backend_name(),
        )

    def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        """Delete a stored object through common storage."""
        document_storage.delete(
            storage_key,
            backend=_backend_name(),
        )


patient_document_storage = PatientDocumentStorage()


__all__ = (
    "PatientDocumentStorage",
    "patient_document_storage",
)
