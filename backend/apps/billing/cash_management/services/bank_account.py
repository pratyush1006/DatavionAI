"""
BankAccount services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.billing.cash_management.models import BankAccount
from django.db import transaction


class BankAccountService:
    """
    Application service for bank_account write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> BankAccount:
        """
        Create a new bank_account.
        """

        instance = BankAccount(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: BankAccount,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> BankAccount:
        """
        Update an existing bank_account.
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
        instance: BankAccount,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a bank_account.
        """

        instance.hard_delete()


create_bank_account = BankAccountService.create

update_bank_account = BankAccountService.update

delete_bank_account = BankAccountService.delete


__all__ = [
    "BankAccountService",
    "create_bank_account",
    "update_bank_account",
    "delete_bank_account",
]
