"""
Document version services.

Handles document version lifecycle.
"""

from __future__ import annotations

from uuid import UUID

from django.db import transaction

from apps.documents.constants import (
    DocumentVersionStatus,
)
from apps.documents.models import (
    DocumentVersion,
)


@transaction.atomic
def create_document_version(
    *,
    document_id: UUID,
    storage_key: str,
    version_number: int,
    uploaded_by_id: UUID | None = None,
    original_filename: str = "",
    mime_type: str = "",
    file_size: int = 0,
    checksum: str = "",
    metadata: dict | None = None,
) -> DocumentVersion:
    """
    Create document version.

    Previous current version becomes
    superseded.
    """

    DocumentVersion.objects.filter(
        document_id=document_id,
        status=(DocumentVersionStatus.CURRENT),
    ).update(
        status=(DocumentVersionStatus.SUPERSEDED),
    )

    return DocumentVersion.objects.create(
        document_id=document_id,
        version_number=version_number,
        storage_key=storage_key,
        uploaded_by_id=uploaded_by_id,
        original_filename=original_filename,
        mime_type=mime_type,
        file_size=file_size,
        checksum=checksum,
        metadata=metadata or {},
        status=(DocumentVersionStatus.CURRENT),
    )


__all__ = ("create_document_version",)
