"""
Payment services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.models import Payment


class PaymentService:
    """
    Application service responsible for payment write operations.

    This service is the single entry point for all payment lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - Payment validation
    - Balance recalculation
    - Receipt generation
    - Audit logging
    - Notifications
    - External integrations
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any = None,
    ) -> Payment:
        """
        Create a new payment and update the invoice balance.
        """

        payment = Payment(
            **validated_data,
        )

        payment.full_clean()

        payment.save()

        invoice = payment.invoice

        invoice.paid_amount = invoice.paid_amount + payment.amount

        invoice.balance_amount = invoice.total_amount - invoice.paid_amount

        invoice.update_status()

        invoice.save(
            update_fields=[
                "paid_amount",
                "balance_amount",
                "status",
            ],
        )

        return payment

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: Any = None,
    ) -> list[Payment]:
        """
        Create multiple payments.
        """

        payments: list[Payment] = []

        for validated_data in validated_data_list:
            payment = Payment(
                **validated_data,
            )

            payment.full_clean()

            payment.save()

            invoice = payment.invoice

            invoice.paid_amount = invoice.paid_amount + payment.amount

            invoice.balance_amount = invoice.total_amount - invoice.paid_amount

            invoice.update_status()

            invoice.save(
                update_fields=[
                    "paid_amount",
                    "balance_amount",
                    "status",
                ],
            )

            payments.append(payment)

        return payments


create_payment = PaymentService.create


__all__ = [
    "PaymentService",
    "create_payment",
]
