"""Transactional Document version service."""

from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.documents.constants import DocumentVersionStatus
from apps.documents.models import Document, DocumentVersion


@transaction.atomic
def create_document_version(
    *,
    document: Document,
    storage_key: str,
    original_filename: str = "",
    mime_type: str = "",
    file_size: int = 0,
    checksum: str = "",
    uploaded_by: Any | None = None,
    extraction_metadata: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> DocumentVersion:
    """Create the next immutable version under an aggregate-root lock."""
    if document.pk is None:
        raise ValidationError("Document must be persisted before creating a version.")
    storage_key = str(storage_key or "").strip()
    if not storage_key:
        raise ValidationError("Storage key is required.")
    if file_size < 0:
        raise ValidationError("File size cannot be negative.")
    locked_document = Document.objects.select_for_update().get(pk=document.pk)
    latest = (
        DocumentVersion.objects.select_for_update()
        .filter(document=locked_document)
        .order_by("-version_number")
        .first()
    )
    next_number = latest.version_number + 1 if latest else 1
    DocumentVersion.objects.filter(
        document=locked_document, status=DocumentVersionStatus.CURRENT
    ).update(status=DocumentVersionStatus.SUPERSEDED)
    version = DocumentVersion(
        document=locked_document,
        version_number=next_number,
        status=DocumentVersionStatus.CURRENT,
        storage_key=storage_key,
        original_filename=str(original_filename or "").strip(),
        mime_type=str(mime_type or "").strip(),
        file_size=file_size,
        checksum=str(checksum or "").strip(),
        uploaded_by=uploaded_by,
        extraction_metadata=extraction_metadata or {},
        metadata=metadata or {},
    )
    version.full_clean()
    version.save(force_insert=True)
    version.full_clean()
    return version


__all__ = ("create_document_version",)
