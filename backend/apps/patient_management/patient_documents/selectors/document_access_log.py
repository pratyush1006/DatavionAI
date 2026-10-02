"""Selectors for Patient Document access audit records."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    PatientDocumentAccessLog,
)


def list_document_access_logs(
    *,
    document_id: UUID,
    tenant_id: UUID,
    organization_id: UUID,
) -> QuerySet[PatientDocumentAccessLog]:
    """Return access logs inside the tenant boundary."""
    return (
        PatientDocumentAccessLog.objects.filter(
            patient_document_id=document_id,
            patient_document__organization_id=organization_id,
            patient_document__organization__tenant_id=tenant_id,
        )
        .select_related(
            "user",
            "patient_document",
        )
        .order_by(
            "-accessed_at",
        )
    )


__all__ = ("list_document_access_logs",)
