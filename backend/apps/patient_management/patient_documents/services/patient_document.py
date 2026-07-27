"""
Services for Patient Documents.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


@transaction.atomic
def create_patient_document(
    *,
    organization,
    patient,
    document_number: str,
    title: str,
    description: str = "",
    category: str,
    source: str,
    visibility: str,
    storage_backend: str,
    tags: list[str] | None = None,
    expires_at=None,
) -> PatientDocument:
    """
    Create a patient document.
    """

    return PatientDocument.objects.create(
        organization=organization,
        patient=patient,
        document_number=document_number,
        title=title,
        description=description,
        category=category,
        source=source,
        visibility=visibility,
        storage_backend=storage_backend,
        tags=tags or [],
        expires_at=expires_at,
    )


@transaction.atomic
def update_patient_document(
    *,
    document: PatientDocument,
    **kwargs,
) -> PatientDocument:
    """
    Update a patient document.
    """

    for field, value in kwargs.items():
        setattr(
            document,
            field,
            value,
        )

    document.save()

    return document


@transaction.atomic
def archive_patient_document(
    *,
    document: PatientDocument,
) -> PatientDocument:
    """
    Archive a patient document.
    """

    document.is_archived = True
    document.save(
        update_fields=[
            "is_archived",
            "updated_at",
        ],
    )

    return document


@transaction.atomic
def delete_patient_document(
    *,
    document: PatientDocument,
) -> None:
    """
    Soft delete a patient document.
    """

    document.is_deleted = True
    document.save(
        update_fields=[
            "is_deleted",
            "updated_at",
        ],
    )


__all__ = [
    "archive_patient_document",
    "create_patient_document",
    "delete_patient_document",
    "update_patient_document",
]
