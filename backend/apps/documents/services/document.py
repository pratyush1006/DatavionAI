"""
Document services.

Business operations for the
Document Management bounded context.

Responsibilities
----------------
- Create documents
- Update document metadata
- Archive documents
- Apply document state changes

Non-responsibilities
--------------------
- API handling
- Permissions
- Workflow orchestration
- Background processing
"""

from __future__ import annotations

from uuid import UUID

from django.db import transaction

from apps.documents.constants import (
    DocumentStatus,
)
from apps.documents.models import (
    Document,
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
    """
    Create a document.

    Used by workflows.

    Flow:

        Workflow
            |
            v
        Service
            |
            v
        Model
    """

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
def update_document(
    *,
    instance: Document,
    data: dict,
) -> Document:
    """
    Update document metadata.
    """

    allowed_fields = {
        "title",
        "document_type",
        "access_level",
        "metadata",
        "ai_metadata",
    }

    for field, value in data.items():
        if field in allowed_fields:
            setattr(
                instance,
                field,
                value,
            )

    instance.save(
        update_fields=[field for field in allowed_fields if field in data],
    )

    return instance


@transaction.atomic
def archive_document(
    *,
    instance: Document,
) -> Document:
    """
    Archive document.
    """

    instance.status = DocumentStatus.ARCHIVED

    instance.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return instance


@transaction.atomic
def delete_document(
    *,
    instance: Document,
) -> Document:
    """
    Soft delete document.

    Actual file removal is handled
    by storage lifecycle services.
    """

    instance.status = DocumentStatus.DELETED

    instance.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return instance


__all__ = (
    "create_document",
    "update_document",
    "archive_document",
    "delete_document",
)
