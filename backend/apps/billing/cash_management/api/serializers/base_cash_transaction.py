"""
Base serializer for the CashTransaction model.
"""

from __future__ import annotations

from apps.billing.cash_management.models import CashTransaction
from rest_framework import serializers


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
