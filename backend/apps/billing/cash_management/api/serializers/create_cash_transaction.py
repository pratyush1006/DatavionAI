"""
Create serializer for the CashTransaction model.
"""

from __future__ import annotations

from apps.billing.cash_management.services import create_cash_transaction

from .base_cash_transaction import CashTransactionBaseSerializer
from .fields_cash_transaction import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class CashTransactionCreateSerializer(CashTransactionBaseSerializer):
    """
    Serializer used for creating cash_transaction records.
    """

    class Meta(CashTransactionBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a cash_transaction.
        """

        return create_cash_transaction(
            validated_data=validated_data,
        )


__all__ = [
    "CashTransactionCreateSerializer",
]
