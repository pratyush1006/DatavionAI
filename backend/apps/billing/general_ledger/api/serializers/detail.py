"""
Detail serializer for the General Ledger application.
"""

from __future__ import annotations

from .base import GeneralLedgerAccountBaseSerializer
from .fields import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class GeneralLedgerAccountDetailSerializer(
    GeneralLedgerAccountBaseSerializer,
):
    """
    Serializer used for retrieving general ledger account details.
    """

    class Meta(GeneralLedgerAccountBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "GeneralLedgerAccountDetailSerializer",
]
