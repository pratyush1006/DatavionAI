"""
CashTransaction services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.billing.cash_management.models import CashTransaction
from django.db import transaction


class CashTransactionService:
    """
    Application service for cash_transaction write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> CashTransaction:
        """
        Create a new cash_transaction.
        """

        instance = CashTransaction(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: CashTransaction,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> CashTransaction:
        """
        Update an existing cash_transaction.
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
        instance: CashTransaction,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a cash_transaction.
        """

        instance.hard_delete()


create_cash_transaction = CashTransactionService.create

update_cash_transaction = CashTransactionService.update

delete_cash_transaction = CashTransactionService.delete


__all__ = [
    "CashTransactionService",
    "create_cash_transaction",
    "update_cash_transaction",
    "delete_cash_transaction",
]
