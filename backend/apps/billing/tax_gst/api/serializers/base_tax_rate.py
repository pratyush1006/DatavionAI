"""
Base serializer for the TaxRate model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.tax_gst.models import TaxRate


class TaxRateBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for tax_rate serializers.
    """

    class Meta:
        model = TaxRate
        fields: tuple[str, ...] = ()


__all__ = [
    "TaxRateBaseSerializer",
]
