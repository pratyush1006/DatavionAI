"""
Services for document access logs.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.patient_documents.models import (
    DocumentAccessLog,
    PatientDocument,
)


@transaction.atomic
def create_document_access_log(
    *,
    document: PatientDocument,
    user,
    action: str,
    ip_address: str | None = None,
    user_agent: str = "",
    remarks: str = "",
) -> DocumentAccessLog:
    """
    Create a document access log entry.
    """

    return DocumentAccessLog.objects.create(
        document=document,
        user=user,
        action=action,
        ip_address=ip_address,
        user_agent=user_agent,
        remarks=remarks,
    )


__all__ = [
    "create_document_access_log",
]
