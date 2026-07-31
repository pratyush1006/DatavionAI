"""
Base serializer for the TaxFiling model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.tax_gst.models import TaxFiling


class TaxFilingBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for tax_filing serializers.
    """

    class Meta:
        model = TaxFiling
        fields: tuple[str, ...] = ()


__all__ = [
    "TaxFilingBaseSerializer",
]
