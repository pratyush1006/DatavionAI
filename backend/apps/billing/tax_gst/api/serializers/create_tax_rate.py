"""
Create serializer for the TaxRate model.
"""

from __future__ import annotations

from apps.billing.tax_gst.services import create_tax_rate

from .base_tax_rate import TaxRateBaseSerializer
from .fields_tax_rate import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class TaxRateCreateSerializer(TaxRateBaseSerializer):
    """
    Serializer used for creating tax_rate records.
    """

    class Meta(TaxRateBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a tax_rate.
        """

        return create_tax_rate(
            validated_data=validated_data,
        )


__all__ = [
    "TaxRateCreateSerializer",
]
