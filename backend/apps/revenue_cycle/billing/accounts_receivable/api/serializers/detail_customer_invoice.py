"""
Detail serializer for the CustomerInvoice model.
"""

from __future__ import annotations

from .base_customer_invoice import CustomerInvoiceBaseSerializer
from .fields_customer_invoice import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class CustomerInvoiceDetailSerializer(CustomerInvoiceBaseSerializer):
    """
    Serializer used for retrieving customer_invoice details.
    """

    class Meta(CustomerInvoiceBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "CustomerInvoiceDetailSerializer",
]
