"""
VendorInvoice selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.billing.accounts_payable.models import VendorInvoice
from apps.platform.organizations.models import Organization
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class VendorInvoiceSelector:
    """
    Read-only queries for vendor_invoice.
    """

    @staticmethod
    def queryset() -> QuerySet[VendorInvoice]:
        """
        Return the base vendor_invoice queryset.
        """

        return VendorInvoice.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[VendorInvoice]:
        """
        Return all vendor_invoice records.
        """

        return VendorInvoiceSelector.queryset()

    @staticmethod
    def get(
        *,
        vendor_invoice_id: UUID,
    ) -> VendorInvoice:
        """
        Return a vendor_invoice by identifier.
        """

        return get_object_or_404(
            VendorInvoiceSelector.queryset(),
            pk=vendor_invoice_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[VendorInvoice]:
        """
        Return all vendor_invoice records for an organization.
        """

        return VendorInvoiceSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        vendor_invoice_id: UUID,
    ) -> bool:
        """
        Determine whether a vendor_invoice exists.
        """

        return (
            VendorInvoiceSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=vendor_invoice_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of vendor_invoice records for an organization.
        """

        return VendorInvoiceSelector.list_by_organization(
            organization=organization,
        ).count()


get_vendor_invoices = VendorInvoiceSelector.list

get_vendor_invoice_by_id = VendorInvoiceSelector.get

get_organization_vendor_invoices = VendorInvoiceSelector.list_by_organization


__all__ = [
    "VendorInvoiceSelector",
    "get_vendor_invoice_by_id",
    "get_vendor_invoices",
    "get_organization_vendor_invoices",
]
