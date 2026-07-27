"""
Detail serializer for the VendorInvoice model.
"""

from __future__ import annotations

from .base_vendor_invoice import VendorInvoiceBaseSerializer
from .fields_vendor_invoice import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class VendorInvoiceDetailSerializer(VendorInvoiceBaseSerializer):
    """
    Serializer used for retrieving vendor_invoice details.
    """

    class Meta(VendorInvoiceBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "VendorInvoiceDetailSerializer",
]
