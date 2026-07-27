"""
List serializer for the BankAccount model.
"""

from __future__ import annotations

from .base_bank_account import BankAccountBaseSerializer
from .fields_bank_account import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class BankAccountListSerializer(BankAccountBaseSerializer):
    """
    Serializer used for listing bank_account records.
    """

    class Meta(BankAccountBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "BankAccountListSerializer",
]
