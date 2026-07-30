"""
Base serializer for the Budget model.
"""

from __future__ import annotations

from apps.billing.financial_management.models import Budget
from rest_framework import serializers


class BudgetBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for budget serializers.
    """

    class Meta:
        model = Budget
        fields: tuple[str, ...] = ()


__all__ = [
    "BudgetBaseSerializer",
]
