"""
List serializer for the VendorInvoice model.
"""

from __future__ import annotations

from .base_vendor_invoice import VendorInvoiceBaseSerializer
from .fields_vendor_invoice import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class VendorInvoiceListSerializer(VendorInvoiceBaseSerializer):
    """
    Serializer used for listing vendor_invoice records.
    """

    class Meta(VendorInvoiceBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "VendorInvoiceListSerializer",
]
