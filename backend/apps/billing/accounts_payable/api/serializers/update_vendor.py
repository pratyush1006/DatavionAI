"""
Update serializer for the Vendor model.
"""

from __future__ import annotations

from apps.billing.accounts_payable.models import Vendor
from apps.billing.accounts_payable.services import update_vendor

from .base_vendor import VendorBaseSerializer
from .fields_vendor import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class VendorUpdateSerializer(VendorBaseSerializer):
    """
    Serializer used for updating vendor records.
    """

    class Meta(VendorBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: Vendor,
        validated_data: dict[str, object],
    ) -> Vendor:
        """
        Update a vendor.
        """

        return update_vendor(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "VendorUpdateSerializer",
]
