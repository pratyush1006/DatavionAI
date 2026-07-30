"""
CustomerInvoice selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.billing.accounts_receivable.models import CustomerInvoice
from apps.platform.organizations.models import Organization


class CustomerInvoiceSelector:
    """
    Read-only queries for customer_invoice.
    """

    @staticmethod
    def queryset() -> QuerySet[CustomerInvoice]:
        """
        Return the base customer_invoice queryset.
        """

        return CustomerInvoice.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[CustomerInvoice]:
        """
        Return all customer_invoice records.
        """

        return CustomerInvoiceSelector.queryset()

    @staticmethod
    def get(
        *,
        customer_invoice_id: UUID,
    ) -> CustomerInvoice:
        """
        Return a customer_invoice by identifier.
        """

        return get_object_or_404(
            CustomerInvoiceSelector.queryset(),
            pk=customer_invoice_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[CustomerInvoice]:
        """
        Return all customer_invoice records for an organization.
        """

        return CustomerInvoiceSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        customer_invoice_id: UUID,
    ) -> bool:
        """
        Determine whether a customer_invoice exists.
        """

        return (
            CustomerInvoiceSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=customer_invoice_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of customer_invoice records for an organization.
        """

        return CustomerInvoiceSelector.list_by_organization(
            organization=organization,
        ).count()


get_customer_invoices = CustomerInvoiceSelector.list

get_customer_invoice_by_id = CustomerInvoiceSelector.get

get_organization_customer_invoices = CustomerInvoiceSelector.list_by_organization


__all__ = [
    "CustomerInvoiceSelector",
    "get_customer_invoice_by_id",
    "get_customer_invoices",
    "get_organization_customer_invoices",
]
