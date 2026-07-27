"""
Create serializer for the General Ledger application.
"""

from __future__ import annotations

from apps.billing.general_ledger.services import (
    create_general_ledger_account,
)

from .base import GeneralLedgerAccountBaseSerializer
from .fields import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class GeneralLedgerAccountCreateSerializer(
    GeneralLedgerAccountBaseSerializer,
):
    """
    Serializer used for creating general ledger accounts.
    """

    class Meta(GeneralLedgerAccountBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a general ledger account.
        """

        return create_general_ledger_account(
            validated_data=validated_data,
        )


__all__ = [
    "GeneralLedgerAccountCreateSerializer",
]
