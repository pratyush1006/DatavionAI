"""
General Ledger services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.general_ledger.models import (
    GeneralLedgerAccount,
    GeneralLedgerJournalEntry,
)
from apps.platform.accounts.models import User


class GeneralLedgerService:
    """
    Application service for general ledger write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> GeneralLedgerAccount:
        """
        Create a new general ledger account.
        """

        account = GeneralLedgerAccount(
            **validated_data,
        )

        account.full_clean()

        account.save()

        return account

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: GeneralLedgerAccount,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> GeneralLedgerAccount:
        """
        Update an existing general ledger account.
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
        instance: GeneralLedgerAccount,
        performed_by: User | None = None,
    ) -> None:
        """
        Delete a general ledger account.
        """

        instance.hard_delete()

    @staticmethod
    @transaction.atomic
    def post_entry(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> GeneralLedgerJournalEntry:
        """
        Post a journal entry against a ledger account.
        """

        entry = GeneralLedgerJournalEntry(
            **validated_data,
        )

        entry.full_clean()

        entry.save()

        return entry


create_general_ledger_account = GeneralLedgerService.create

update_general_ledger_account = GeneralLedgerService.update

delete_general_ledger_account = GeneralLedgerService.delete


__all__ = [
    "GeneralLedgerService",
    "create_general_ledger_account",
    "update_general_ledger_account",
    "delete_general_ledger_account",
]
