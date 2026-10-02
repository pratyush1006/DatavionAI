"""Read-side selectors for Patient Documents."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


def patient_document_queryset(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    patient_id=None,
    include_deleted: bool = False,
) -> QuerySet[PatientDocument]:
    """Return an optimized organization and tenant scoped queryset."""
    manager = (
        PatientDocument.all_objects if include_deleted else PatientDocument.objects
    )

    queryset = (
        manager.filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
        .select_related(
            "organization",
            "patient",
            "created_by",
        )
        .prefetch_related(
            "versions",
        )
    )

    if patient_id is not None:
        queryset = queryset.filter(
            patient_id=patient_id,
        )

    return queryset


def get_patient_document(
    *,
    document_id: UUID,
    tenant_id: UUID,
    organization_id: UUID,
    include_deleted: bool = False,
) -> PatientDocument:
    """Resolve one patient document inside the tenant boundary."""
    return patient_document_queryset(
        tenant_id=tenant_id,
        organization_id=organization_id,
        include_deleted=include_deleted,
    ).get(
        pk=document_id,
    )


__all__ = (
    "get_patient_document",
    "patient_document_queryset",
)
