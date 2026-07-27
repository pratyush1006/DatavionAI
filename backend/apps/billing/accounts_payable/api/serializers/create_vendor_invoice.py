"""
Create serializer for the VendorInvoice model.
"""

from __future__ import annotations

from apps.billing.accounts_payable.services import create_vendor_invoice

from .base_vendor_invoice import VendorInvoiceBaseSerializer
from .fields_vendor_invoice import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class VendorInvoiceCreateSerializer(VendorInvoiceBaseSerializer):
    """
    Serializer used for creating vendor_invoice records.
    """

    class Meta(VendorInvoiceBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a vendor_invoice.
        """

        return create_vendor_invoice(
            validated_data=validated_data,
        )


__all__ = [
    "VendorInvoiceCreateSerializer",
]
