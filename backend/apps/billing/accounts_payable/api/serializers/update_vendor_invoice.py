"""
Update serializer for the VendorInvoice model.
"""

from __future__ import annotations

from apps.billing.accounts_payable.models import VendorInvoice
from apps.billing.accounts_payable.services import update_vendor_invoice

from .base_vendor_invoice import VendorInvoiceBaseSerializer
from .fields_vendor_invoice import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class VendorInvoiceUpdateSerializer(VendorInvoiceBaseSerializer):
    """
    Serializer used for updating vendor_invoice records.
    """

    class Meta(VendorInvoiceBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: VendorInvoice,
        validated_data: dict[str, object],
    ) -> VendorInvoice:
        """
        Update a vendor_invoice.
        """

        return update_vendor_invoice(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "VendorInvoiceUpdateSerializer",
]
