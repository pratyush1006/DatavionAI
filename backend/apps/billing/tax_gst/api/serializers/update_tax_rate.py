"""
Update serializer for the TaxRate model.
"""

from __future__ import annotations

from apps.billing.tax_gst.models import TaxRate
from apps.billing.tax_gst.services import update_tax_rate

from .base_tax_rate import TaxRateBaseSerializer
from .fields_tax_rate import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class TaxRateUpdateSerializer(TaxRateBaseSerializer):
    """
    Serializer used for updating tax_rate records.
    """

    class Meta(TaxRateBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: TaxRate,
        validated_data: dict[str, object],
    ) -> TaxRate:
        """
        Update a tax_rate.
        """

        return update_tax_rate(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "TaxRateUpdateSerializer",
]
