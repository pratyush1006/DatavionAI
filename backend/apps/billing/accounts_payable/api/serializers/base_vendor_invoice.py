"""
Base serializer for the VendorInvoice model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.accounts_payable.models import VendorInvoice


class VendorInvoiceBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for vendor_invoice serializers.
    """

    class Meta:
        model = VendorInvoice
        fields: tuple[str, ...] = ()


__all__ = [
    "VendorInvoiceBaseSerializer",
]
