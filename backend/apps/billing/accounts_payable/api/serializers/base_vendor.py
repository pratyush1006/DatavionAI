"""
Base serializer for the Vendor model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.accounts_payable.models import Vendor


class VendorBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for vendor serializers.
    """

    class Meta:
        model = Vendor
        fields: tuple[str, ...] = ()


__all__ = [
    "VendorBaseSerializer",
]
