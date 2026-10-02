"""Transactional Document lifecycle services."""

from __future__ import annotations

from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.documents.constants import DocumentStatus
from apps.documents.models import Document

UPDATEABLE_FIELDS = frozenset(
    {"title", "document_type", "access_level", "metadata", "ai_metadata"}
)


@transaction.atomic
def create_document(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    title: str,
    storage_key: str,
    document_type: str,
    original_filename: str = "",
    mime_type: str = "",
    file_size: int = 0,
    checksum: str = "",
    metadata: dict | None = None,
    ai_metadata: dict | None = None,
) -> Document:
    return Document.objects.create(
        tenant_id=tenant_id,
        organization_id=organization_id,
        title=title,
        storage_key=storage_key,
        document_type=document_type,
        original_filename=original_filename,
        mime_type=mime_type,
        file_size=file_size,
        checksum=checksum,
        metadata=metadata or {},
        ai_metadata=ai_metadata or {},
    )


@transaction.atomic
def update_document(*, instance: Document, data: dict) -> Document:
    if instance.pk is None:
        raise ValidationError("Document must be persisted before update.")
    if not data:
        raise ValidationError("At least one document field is required.")
    unknown = set(data) - UPDATEABLE_FIELDS
    if unknown:
        raise ValidationError(
            "Unsupported document fields: " + ", ".join(sorted(unknown))
        )
    locked = Document.objects.select_for_update().get(pk=instance.pk)
    if locked.status == DocumentStatus.DELETED:
        raise ValidationError("Deleted documents cannot be updated.")
    for field, value in data.items():
        setattr(locked, field, value)
    locked.full_clean()
    locked.save(update_fields=tuple(data.keys()) + ("updated_at",))
    return locked


@transaction.atomic
def archive_document(*, instance: Document) -> Document:
    if instance.pk is None:
        raise ValidationError("Document must be persisted before archival.")
    locked = Document.objects.select_for_update().get(pk=instance.pk)
    if locked.status == DocumentStatus.DELETED:
        raise ValidationError("Deleted documents cannot be archived.")
    if locked.status == DocumentStatus.ARCHIVED:
        return locked
    locked.status = DocumentStatus.ARCHIVED
    locked.full_clean()
    locked.save(update_fields=("status", "updated_at"))
    return locked


@transaction.atomic
def delete_document(*, instance: Document) -> Document:
    if instance.pk is None:
        raise ValidationError("Document must be persisted before deletion.")
    locked = Document.objects.select_for_update().get(pk=instance.pk)
    if locked.status == DocumentStatus.DELETED:
        return locked
    locked.status = DocumentStatus.DELETED
    locked.full_clean()
    locked.save(update_fields=("status", "updated_at"))
    return locked


__all__ = ("create_document", "update_document", "archive_document", "delete_document")
