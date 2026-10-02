"""Tenant-safe selectors for payment posting."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from .models import PaymentPosting


def payment_postings_for_organization(
    *,
    organization_id: UUID,
    tenant_id: UUID,
) -> QuerySet[PaymentPosting]:
    """Return active payment postings within explicit organization and tenant scope."""

    return PaymentPosting.objects.filter(
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


def get_payment_posting(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    posting_id: UUID,
) -> PaymentPosting:
    """Return one active payment posting in tenant scope."""

    return payment_postings_for_organization(
        organization_id=organization_id,
        tenant_id=tenant_id,
    ).get(pk=posting_id)


def get_payment_posting_for_update(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    posting_id: UUID,
) -> PaymentPosting:
    """Return one active payment posting with a database row lock."""

    return (
        payment_postings_for_organization(
            organization_id=organization_id,
            tenant_id=tenant_id,
        )
        .select_for_update()
        .get(pk=posting_id)
    )


def get_deleted_payment_posting_for_update(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    posting_id: UUID,
) -> PaymentPosting:
    """Return one deleted payment posting with a database row lock."""

    return (
        PaymentPosting.all_objects.filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
            pk=posting_id,
            is_deleted=True,
        )
        .select_for_update()
        .get()
    )


__all__ = (
    "get_deleted_payment_posting_for_update",
    "get_payment_posting",
    "get_payment_posting_for_update",
    "payment_postings_for_organization",
)
