"""
CustomerInvoice services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.billing.accounts_receivable.models import CustomerInvoice
from django.db import transaction


class CustomerInvoiceService:
    """
    Application service for customer_invoice write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> CustomerInvoice:
        """
        Create a new customer_invoice.
        """

        instance = CustomerInvoice(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: CustomerInvoice,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> CustomerInvoice:
        """
        Update an existing customer_invoice.
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
        instance: CustomerInvoice,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a customer_invoice.
        """

        instance.hard_delete()


create_customer_invoice = CustomerInvoiceService.create

update_customer_invoice = CustomerInvoiceService.update

delete_customer_invoice = CustomerInvoiceService.delete


__all__ = [
    "CustomerInvoiceService",
    "create_customer_invoice",
    "update_customer_invoice",
    "delete_customer_invoice",
]
