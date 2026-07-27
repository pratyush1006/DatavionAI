"""
Update serializer for the General Ledger application.
"""

from __future__ import annotations

from apps.billing.general_ledger.models import GeneralLedgerAccount
from apps.billing.general_ledger.services import (
    update_general_ledger_account,
)

from .base import GeneralLedgerAccountBaseSerializer
from .fields import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class GeneralLedgerAccountUpdateSerializer(
    GeneralLedgerAccountBaseSerializer,
):
    """
    Serializer used for updating general ledger accounts.
    """

    class Meta(GeneralLedgerAccountBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: GeneralLedgerAccount,
        validated_data: dict[str, object],
    ) -> GeneralLedgerAccount:
        """
        Update a general ledger account.
        """

        return update_general_ledger_account(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "GeneralLedgerAccountUpdateSerializer",
]
