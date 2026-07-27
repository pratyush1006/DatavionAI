"""
Detail serializer for the CashTransaction model.
"""

from __future__ import annotations

from .base_cash_transaction import CashTransactionBaseSerializer
from .fields_cash_transaction import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class CashTransactionDetailSerializer(CashTransactionBaseSerializer):
    """
    Serializer used for retrieving cash_transaction details.
    """

    class Meta(CashTransactionBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "CashTransactionDetailSerializer",
]
