"""
Services for document versions.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.patient_documents.models import (
    DocumentVersion,
    PatientDocument,
)


@transaction.atomic
def create_document_version(
    *,
    document: PatientDocument,
    file,
    original_filename: str,
    mime_type: str,
    file_size: int,
    checksum: str,
    uploaded_by,
    remarks: str = "",
) -> DocumentVersion:
    """
    Create a new document version.
    """

    DocumentVersion.objects.filter(
        document=document,
        is_current=True,
    ).update(
        is_current=False,
    )

    version = document.current_version + 1

    document.current_version = version
    document.save(
        update_fields=[
            "current_version",
            "updated_at",
        ],
    )

    return DocumentVersion.objects.create(
        document=document,
        version=version,
        file=file,
        original_filename=original_filename,
        mime_type=mime_type,
        file_size=file_size,
        checksum=checksum,
        uploaded_by=uploaded_by,
        remarks=remarks,
        is_current=True,
    )


__all__ = [
    "create_document_version",
]
