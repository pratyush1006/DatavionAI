"""
Invoice services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.constants import InvoiceStatus
from apps.billing.models import Invoice, InvoiceItem


class InvoiceService:
    """
    Application service responsible for invoice write operations.

    This service is the single entry point for all invoice lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - Invoice number generation
    - Balance calculation
    - Status transitions
    - Audit logging
    - Notifications
    - External integrations
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        items: list[Mapping[str, Any]] | None = None,
        performed_by: Any = None,
    ) -> Invoice:
        """
        Create a new invoice with optional line items.
        """

        invoice = Invoice(
            **validated_data,
        )

        invoice.full_clean()

        invoice.save()

        if items:
            for item_data in items:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    **item_data,
                )

            invoice.update_status()

            invoice.save(
                update_fields=[
                    "balance_amount",
                    "status",
                ],
            )

        return invoice

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Invoice,
        validated_data: Mapping[str, Any],
        performed_by: Any = None,
    ) -> Invoice:
        """
        Update an existing invoice.
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
    def void(
        *,
        instance: Invoice,
        performed_by: Any = None,
    ) -> Invoice:
        """
        Void an invoice.
        """

        instance.status = InvoiceStatus.VOID

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: Any = None,
    ) -> list[Invoice]:
        """
        Create multiple invoices.
        """

        invoices: list[Invoice] = []

        for validated_data in validated_data_list:
            items = validated_data.pop(
                "items",
                None,
            )

            invoice = Invoice(
                **validated_data,
            )

            invoice.full_clean()

            invoice.save()

            if items:
                for item_data in items:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        **item_data,
                    )

                invoice.update_status()

                invoice.save(
                    update_fields=[
                        "balance_amount",
                        "status",
                    ],
                )

            invoices.append(invoice)

        return invoices


create_invoice = InvoiceService.create
update_invoice = InvoiceService.update
void_invoice = InvoiceService.void


__all__ = [
    "InvoiceService",
    "create_invoice",
    "update_invoice",
    "void_invoice",
]
