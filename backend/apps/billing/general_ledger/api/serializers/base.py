"""
Base serializers for the General Ledger application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.general_ledger.models import GeneralLedgerAccount


class GeneralLedgerAccountBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for general ledger accounts.
    """

    class Meta:
        model = GeneralLedgerAccount
        fields: tuple[str, ...] = ()


__all__ = [
    "GeneralLedgerAccountBaseSerializer",
]
