"""
Update serializer for the BankAccount model.
"""

from __future__ import annotations

from apps.billing.cash_management.models import BankAccount
from apps.billing.cash_management.services import update_bank_account

from .base_bank_account import BankAccountBaseSerializer
from .fields_bank_account import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class BankAccountUpdateSerializer(BankAccountBaseSerializer):
    """
    Serializer used for updating bank_account records.
    """

    class Meta(BankAccountBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: BankAccount,
        validated_data: dict[str, object],
    ) -> BankAccount:
        """
        Update a bank_account.
        """

        return update_bank_account(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "BankAccountUpdateSerializer",
]
