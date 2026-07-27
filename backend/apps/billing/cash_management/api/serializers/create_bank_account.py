"""
Create serializer for the BankAccount model.
"""

from __future__ import annotations

from apps.billing.cash_management.services import create_bank_account

from .base_bank_account import BankAccountBaseSerializer
from .fields_bank_account import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class BankAccountCreateSerializer(BankAccountBaseSerializer):
    """
    Serializer used for creating bank_account records.
    """

    class Meta(BankAccountBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a bank_account.
        """

        return create_bank_account(
            validated_data=validated_data,
        )


__all__ = [
    "BankAccountCreateSerializer",
]
