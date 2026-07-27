"""
Selectors for document versions.
"""

from __future__ import annotations

from typing import Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.patient_documents.models import (
    DocumentVersion,
)


def get_document_version_by_id(
    *,
    version_id: Any,
) -> DocumentVersion:
    """
    Return a document version by its primary key.
    """

    return get_object_or_404(
        DocumentVersion.objects.select_related(
            "document",
            "created_by",
            "updated_by",
        ),
        pk=version_id,
    )


def get_current_document_version(
    *,
    document: Any,
) -> DocumentVersion:
    """
    Return the current version for a document.
    """

    return get_object_or_404(
        DocumentVersion.objects.select_related(
            "document",
            "created_by",
            "updated_by",
        ),
        document=document,
        is_current=True,
    )


def list_document_versions(
    *,
    document: Any,
) -> QuerySet[DocumentVersion]:
    """
    Return all versions for a document ordered from newest to oldest.
    """

    return (
        DocumentVersion.objects.select_related(
            "document",
            "created_by",
            "updated_by",
        )
        .filter(
            document=document,
        )
        .order_by(
            "-version",
            "-created_at",
        )
    )


def get_latest_document_version(
    *,
    document: Any,
) -> DocumentVersion | None:
    """
    Return the latest document version.
    """

    return (
        DocumentVersion.objects.select_related(
            "document",
            "created_by",
            "updated_by",
        )
        .filter(
            document=document,
        )
        .order_by(
            "-version",
            "-created_at",
        )
        .first()
    )


def list_current_document_versions() -> QuerySet[DocumentVersion]:
    """
    Return all current document versions.
    """

    return (
        DocumentVersion.objects.select_related(
            "document",
            "created_by",
            "updated_by",
        )
        .filter(
            is_current=True,
        )
        .order_by(
            "-created_at",
        )
    )


def count_document_versions(
    *,
    document: Any,
) -> int:
    """
    Return the number of versions for a document.
    """

    return DocumentVersion.objects.filter(
        document=document,
    ).count()


def document_version_exists(
    *,
    document: Any,
    version: int,
) -> bool:
    """
    Return whether a specific version exists.
    """

    return DocumentVersion.objects.filter(
        document=document,
        version=version,
    ).exists()


__all__ = (
    "count_document_versions",
    "document_version_exists",
    "get_current_document_version",
    "get_document_version_by_id",
    "get_latest_document_version",
    "list_current_document_versions",
    "list_document_versions",
)
