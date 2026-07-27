"""
Detail serializer for the Vendor model.
"""

from __future__ import annotations

from .base_vendor import VendorBaseSerializer
from .fields_vendor import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class VendorDetailSerializer(VendorBaseSerializer):
    """
    Serializer used for retrieving vendor details.
    """

    class Meta(VendorBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "VendorDetailSerializer",
]
