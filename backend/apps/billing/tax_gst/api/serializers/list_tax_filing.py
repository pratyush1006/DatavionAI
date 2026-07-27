"""
List serializer for the TaxFiling model.
"""

from __future__ import annotations

from .base_tax_filing import TaxFilingBaseSerializer
from .fields_tax_filing import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class TaxFilingListSerializer(TaxFilingBaseSerializer):
    """
    Serializer used for listing tax_filing records.
    """

    class Meta(TaxFilingBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "TaxFilingListSerializer",
]
