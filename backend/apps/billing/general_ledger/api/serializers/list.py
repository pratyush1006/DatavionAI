"""
List serializer for the General Ledger application.
"""

from __future__ import annotations

from .base import GeneralLedgerAccountBaseSerializer
from .fields import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class GeneralLedgerAccountListSerializer(
    GeneralLedgerAccountBaseSerializer,
):
    """
    Serializer used for listing general ledger accounts.
    """

    class Meta(GeneralLedgerAccountBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "GeneralLedgerAccountListSerializer",
]
