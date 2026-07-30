"""
VendorInvoice services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.accounts_payable.models import VendorInvoice


class VendorInvoiceService:
    """
    Application service for vendor_invoice write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> VendorInvoice:
        """
        Create a new vendor_invoice.
        """

        instance = VendorInvoice(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: VendorInvoice,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> VendorInvoice:
        """
        Update an existing vendor_invoice.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: VendorInvoice,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a vendor_invoice.
        """

        instance.hard_delete()


create_vendor_invoice = VendorInvoiceService.create

update_vendor_invoice = VendorInvoiceService.update

delete_vendor_invoice = VendorInvoiceService.delete


__all__ = [
    "VendorInvoiceService",
    "create_vendor_invoice",
    "update_vendor_invoice",
    "delete_vendor_invoice",
]
