"""
Create serializer for the Vendor model.
"""

from __future__ import annotations

from apps.billing.accounts_payable.services import create_vendor

from .base_vendor import VendorBaseSerializer
from .fields_vendor import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class VendorCreateSerializer(VendorBaseSerializer):
    """
    Serializer used for creating vendor records.
    """

    class Meta(VendorBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a vendor.
        """

        return create_vendor(
            validated_data=validated_data,
        )


__all__ = [
    "VendorCreateSerializer",
]
