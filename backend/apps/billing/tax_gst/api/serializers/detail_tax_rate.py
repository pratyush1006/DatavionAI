"""
Detail serializer for the TaxRate model.
"""

from __future__ import annotations

from .base_tax_rate import TaxRateBaseSerializer
from .fields_tax_rate import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class TaxRateDetailSerializer(TaxRateBaseSerializer):
    """
    Serializer used for retrieving tax_rate details.
    """

    class Meta(TaxRateBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "TaxRateDetailSerializer",
]
