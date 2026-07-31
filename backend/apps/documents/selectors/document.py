"""
Document selectors.

Read-only query operations for
Document Management bounded context.

Responsibilities
----------------
- Tenant scoped queries
- Organization scoped queries
- Optimized document retrieval

Non-responsibilities
--------------------
- Business rules
- State changes
- Workflow execution
- Permission decisions

Those belong to:
- services
- workflows
- permissions
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import (
    QuerySet,
)

from apps.documents.models import (
    Document,
)


def get_documents(
    *,
    tenant_id: UUID | None = None,
    organization_id: UUID | None = None,
) -> QuerySet[Document]:
    """
    Return documents filtered by ownership context.

    Supports:

    - Tenant isolation
    - Organization isolation
    - Multi-tenant SaaS queries
    """

    queryset = Document.objects.select_related(
        "tenant",
        "organization",
    ).prefetch_related(
        "versions",
        "access_entries",
    )

    if tenant_id is not None:
        queryset = queryset.filter(
            tenant_id=tenant_id,
        )

    if organization_id is not None:
        queryset = queryset.filter(
            organization_id=organization_id,
        )

    return queryset


def get_document_by_id(
    *,
    document_id: UUID,
) -> Document:
    """
    Retrieve single document by id.
    """

    return (
        Document.objects.select_related(
            "tenant",
            "organization",
        )
        .prefetch_related(
            "versions",
            "access_entries",
        )
        .get(
            id=document_id,
        )
    )


def get_document_versions(
    *,
    document_id: UUID,
):
    """
    Return document versions.
    """

    document = get_document_by_id(
        document_id=document_id,
    )

    return document.versions.all()


def get_document_access_entries(
    *,
    document_id: UUID,
):
    """
    Return document access entries.
    """

    document = get_document_by_id(
        document_id=document_id,
    )

    return document.access_entries.all()


__all__ = (
    "get_documents",
    "get_document_by_id",
    "get_document_versions",
    "get_document_access_entries",
)
