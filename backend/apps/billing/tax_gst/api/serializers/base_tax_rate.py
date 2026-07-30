"""
Base serializer for the TaxRate model.
"""

from __future__ import annotations

from apps.billing.tax_gst.models import TaxRate
from rest_framework import serializers


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
