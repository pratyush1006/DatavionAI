"""
List serializer for the TaxRate model.
"""

from __future__ import annotations

from .base_tax_rate import TaxRateBaseSerializer
from .fields_tax_rate import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class TaxRateListSerializer(TaxRateBaseSerializer):
    """
    Serializer used for listing tax_rate records.
    """

    class Meta(TaxRateBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "TaxRateListSerializer",
]
