"""Tenant-safe Document selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.documents.models import Document


def _base_queryset() -> QuerySet[Document]:
    return Document.objects.select_related("tenant", "organization").prefetch_related(
        "versions", "access_entries"
    )


def get_documents(
    *, tenant_id: UUID | None = None, organization_id: UUID | None = None
) -> QuerySet[Document]:
    queryset = _base_queryset()
    if tenant_id is not None:
        queryset = queryset.filter(tenant_id=tenant_id)
    if organization_id is not None:
        queryset = queryset.filter(organization_id=organization_id)
    return queryset


def get_document_by_id(*, document_id: UUID) -> Document:
    return _base_queryset().get(id=document_id)


def get_document_by_id_for_tenant(*, document_id: UUID, tenant_id: UUID) -> Document:
    return _base_queryset().get(id=document_id, tenant_id=tenant_id)


def get_document_versions(*, document_id: UUID):
    return get_document_by_id(document_id=document_id).versions.all()


def get_document_access_entries(*, document_id: UUID):
    return get_document_by_id(document_id=document_id).access_entries.all()


__all__ = (
    "get_documents",
    "get_document_by_id",
    "get_document_by_id_for_tenant",
    "get_document_versions",
    "get_document_access_entries",
)
