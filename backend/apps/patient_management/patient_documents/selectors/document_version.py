"""Selectors for patient document versions."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    PatientDocumentVersion,
)


def list_document_versions(
    *,
    document_id: UUID,
    tenant_id: UUID,
    organization_id: UUID,
) -> QuerySet[PatientDocumentVersion]:
    """Return versions for an organization-scoped patient document."""
    return (
        PatientDocumentVersion.objects.filter(
            patient_document_id=document_id,
            patient_document__organization_id=organization_id,
            patient_document__organization__tenant_id=tenant_id,
        )
        .select_related(
            "patient_document",
            "created_by",
        )
        .order_by(
            "-version_number",
        )
    )


__all__ = ("list_document_versions",)
