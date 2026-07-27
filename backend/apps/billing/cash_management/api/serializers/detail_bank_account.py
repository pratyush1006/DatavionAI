"""
Detail serializer for the BankAccount model.
"""

from __future__ import annotations

from .base_bank_account import BankAccountBaseSerializer
from .fields_bank_account import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class BankAccountDetailSerializer(BankAccountBaseSerializer):
    """
    Serializer used for retrieving bank_account details.
    """

    class Meta(BankAccountBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "BankAccountDetailSerializer",
]
