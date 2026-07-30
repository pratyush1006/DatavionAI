"""
Base serializer for the BankAccount model.
"""

from __future__ import annotations

from apps.billing.cash_management.models import BankAccount
from rest_framework import serializers


class BankAccountBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for bank_account serializers.
    """

    class Meta:
        model = BankAccount
        fields: tuple[str, ...] = ()


__all__ = [
    "BankAccountBaseSerializer",
]
