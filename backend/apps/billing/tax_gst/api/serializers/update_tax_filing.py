"""
Update serializer for the TaxFiling model.
"""

from __future__ import annotations

from apps.billing.tax_gst.models import TaxFiling
from apps.billing.tax_gst.services import update_tax_filing

from .base_tax_filing import TaxFilingBaseSerializer
from .fields_tax_filing import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class TaxFilingUpdateSerializer(TaxFilingBaseSerializer):
    """
    Serializer used for updating tax_filing records.
    """

    class Meta(TaxFilingBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: TaxFiling,
        validated_data: dict[str, object],
    ) -> TaxFiling:
        """
        Update a tax_filing.
        """

        return update_tax_filing(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "TaxFilingUpdateSerializer",
]
