"""
List serializer for the CashTransaction model.
"""

from __future__ import annotations

from .base_cash_transaction import CashTransactionBaseSerializer
from .fields_cash_transaction import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class CashTransactionListSerializer(CashTransactionBaseSerializer):
    """
    Serializer used for listing cash_transaction records.
    """

    class Meta(CashTransactionBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "CashTransactionListSerializer",
]
