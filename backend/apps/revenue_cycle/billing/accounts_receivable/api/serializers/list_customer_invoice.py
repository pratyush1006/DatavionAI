"""
List serializer for the CustomerInvoice model.
"""

from __future__ import annotations

from .base_customer_invoice import CustomerInvoiceBaseSerializer
from .fields_customer_invoice import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class CustomerInvoiceListSerializer(CustomerInvoiceBaseSerializer):
    """
    Serializer used for listing customer_invoice records.
    """

    class Meta(CustomerInvoiceBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "CustomerInvoiceListSerializer",
]
