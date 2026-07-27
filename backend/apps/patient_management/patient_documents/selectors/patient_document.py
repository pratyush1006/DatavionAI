"""
Selectors for Patient Documents.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


def get_patient_document_by_id(
    *,
    document_id,
) -> PatientDocument:
    """
    Return a patient document by ID.
    """

    return PatientDocument.objects.get(
        id=document_id,
    )


def list_patient_documents() -> QuerySet[PatientDocument]:
    """
    Return all patient documents.
    """

    return PatientDocument.objects.all()


def list_organization_documents(
    *,
    organization,
) -> QuerySet[PatientDocument]:
    """
    Return documents for an organization.
    """

    return PatientDocument.objects.for_organization(
        organization,
    ).active()


def list_patient_documents_by_patient(
    *,
    patient,
) -> QuerySet[PatientDocument]:
    """
    Return documents for a patient.
    """

    return PatientDocument.objects.for_patient(
        patient,
    ).active()


def list_documents_by_category(
    *,
    category: str,
) -> QuerySet[PatientDocument]:
    """
    Return documents by category.
    """

    return PatientDocument.objects.by_category(
        category,
    ).active()


def list_documents_by_status(
    *,
    status: str,
) -> QuerySet[PatientDocument]:
    """
    Return documents by status.
    """

    return PatientDocument.objects.by_status(
        status,
    )


def count_patient_documents(
    *,
    patient,
) -> int:
    """
    Return the number of active documents
    for a patient.
    """

    return (
        PatientDocument.objects.for_patient(
            patient,
        )
        .active()
        .count()
    )


__all__ = [
    "count_patient_documents",
    "get_patient_document_by_id",
    "list_documents_by_category",
    "list_documents_by_status",
    "list_organization_documents",
    "list_patient_documents",
    "list_patient_documents_by_patient",
]
