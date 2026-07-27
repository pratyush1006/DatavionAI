"""
Selectors for document access logs.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.patient_documents.models import (
    DocumentAccessLog,
)


def list_document_access_logs(
    *,
    document,
) -> QuerySet[DocumentAccessLog]:
    """
    Return access logs for a document.
    """

    return (
        DocumentAccessLog.objects.filter(
            document=document,
        )
        .select_related(
            "user",
        )
        .order_by("-created_at")
    )


def list_document_user_logs(
    *,
    user,
) -> QuerySet[DocumentAccessLog]:
    """
    Return access logs for a user.
    """

    return (
        DocumentAccessLog.objects.filter(
            user=user,
        )
        .select_related(
            "document",
        )
        .order_by("-created_at")
    )


def list_document_action_logs(
    *,
    action: str,
) -> QuerySet[DocumentAccessLog]:
    """
    Return access logs filtered by action.
    """

    return (
        DocumentAccessLog.objects.filter(
            action=action,
        )
        .select_related(
            "document",
            "user",
        )
        .order_by("-created_at")
    )


def count_document_access_logs(
    *,
    document,
) -> int:
    """
    Return the number of access logs for a document.
    """

    return DocumentAccessLog.objects.filter(
        document=document,
    ).count()


__all__ = [
    "count_document_access_logs",
    "list_document_access_logs",
    "list_document_action_logs",
    "list_document_user_logs",
]
