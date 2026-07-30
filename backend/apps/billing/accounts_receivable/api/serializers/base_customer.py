"""
Base serializer for the Customer model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.accounts_receivable.models import Customer


class CustomerBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for customer serializers.
    """

    class Meta:
        model = Customer
        fields: tuple[str, ...] = ()


__all__ = [
    "CustomerBaseSerializer",
]
