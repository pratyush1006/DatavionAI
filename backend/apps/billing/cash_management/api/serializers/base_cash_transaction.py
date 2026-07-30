"""
Base serializer for the CashTransaction model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.cash_management.models import CashTransaction


class CashTransactionBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for cash_transaction serializers.
    """

    class Meta:
        model = CashTransaction
        fields: tuple[str, ...] = ()


__all__ = [
    "CashTransactionBaseSerializer",
]
