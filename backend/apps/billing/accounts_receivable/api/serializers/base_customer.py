"""
Base serializer for the Customer model.
"""

from __future__ import annotations

from apps.billing.accounts_receivable.models import Customer
from rest_framework import serializers


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
