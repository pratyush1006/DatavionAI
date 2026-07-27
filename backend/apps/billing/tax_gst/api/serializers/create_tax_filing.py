"""
Create serializer for the TaxFiling model.
"""

from __future__ import annotations

from apps.billing.tax_gst.services import create_tax_filing

from .base_tax_filing import TaxFilingBaseSerializer
from .fields_tax_filing import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class TaxFilingCreateSerializer(TaxFilingBaseSerializer):
    """
    Serializer used for creating tax_filing records.
    """

    class Meta(TaxFilingBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a tax_filing.
        """

        return create_tax_filing(
            validated_data=validated_data,
        )


__all__ = [
    "TaxFilingCreateSerializer",
]
