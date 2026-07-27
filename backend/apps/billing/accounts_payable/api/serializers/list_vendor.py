"""
List serializer for the Vendor model.
"""

from __future__ import annotations

from .base_vendor import VendorBaseSerializer
from .fields_vendor import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class VendorListSerializer(VendorBaseSerializer):
    """
    Serializer used for listing vendor records.
    """

    class Meta(VendorBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "VendorListSerializer",
]
