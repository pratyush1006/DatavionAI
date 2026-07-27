"""
Detail serializer for the TaxFiling model.
"""

from __future__ import annotations

from .base_tax_filing import TaxFilingBaseSerializer
from .fields_tax_filing import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class TaxFilingDetailSerializer(TaxFilingBaseSerializer):
    """
    Serializer used for retrieving tax_filing details.
    """

    class Meta(TaxFilingBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "TaxFilingDetailSerializer",
]
