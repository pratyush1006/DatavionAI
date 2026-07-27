"""
Update serializer for the CashTransaction model.
"""

from __future__ import annotations

from apps.billing.cash_management.models import CashTransaction
from apps.billing.cash_management.services import update_cash_transaction

from .base_cash_transaction import CashTransactionBaseSerializer
from .fields_cash_transaction import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class CashTransactionUpdateSerializer(CashTransactionBaseSerializer):
    """
    Serializer used for updating cash_transaction records.
    """

    class Meta(CashTransactionBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: CashTransaction,
        validated_data: dict[str, object],
    ) -> CashTransaction:
        """
        Update a cash_transaction.
        """

        return update_cash_transaction(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "CashTransactionUpdateSerializer",
]
