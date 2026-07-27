"""
Base serializer for the TaxFiling model.
"""

from __future__ import annotations

from apps.billing.tax_gst.models import TaxFiling
from rest_framework import serializers


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
