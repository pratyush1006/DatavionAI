"""
Billing Core Invoice selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.billing.exceptions import BillingNotFoundError
from apps.billing.models import Invoice


class InvoiceSelector:
    """Provide tenant and organization scoped invoice reads."""

    @staticmethod
    def queryset(
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> QuerySet[Invoice]:
        """Return invoices inside one tenant and organization."""
        return (
            Invoice.objects.select_related(
                "organization",
                "patient",
            )
            .prefetch_related(
                "items",
                "payments",
                "insurance_claims",
            )
            .filter(
                organization_id=organization_id,
                organization__tenant_id=tenant_id,
            )
        )

    @classmethod
    def list(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> QuerySet[Invoice]:
        """List invoices for one organization."""
        return cls.queryset(
            tenant_id=tenant_id,
            organization_id=organization_id,
        )

    @classmethod
    def get(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        invoice_id: UUID,
    ) -> Invoice:
        """Retrieve one organization-scoped invoice."""
        try:
            return cls.queryset(
                tenant_id=tenant_id,
                organization_id=organization_id,
            ).get(
                pk=invoice_id,
            )
        except Invoice.DoesNotExist as exc:
            raise BillingNotFoundError(
                "Invoice was not found.",
            ) from exc


__all__ = ("InvoiceSelector",)
