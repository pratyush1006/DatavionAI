"""Domain service for Patient Document access auditing."""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.patient_documents.models import (
    PatientDocumentAccessLog,
)


class PatientDocumentAccessLogService:
    """Persist auditable document-access records."""

    @staticmethod
    @transaction.atomic
    def record(
        *,
        patient_document,
        user,
        action: str,
        ip_address: str | None = None,
        user_agent: str = "",
        metadata: dict | None = None,
    ) -> PatientDocumentAccessLog:
        """Record one document access event."""
        return PatientDocumentAccessLog.objects.create(
            patient_document=patient_document,
            user=user,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent[:1000],
            metadata=metadata or {},
        )


__all__ = ("PatientDocumentAccessLogService",)
