"""
Create serializer for the CustomerInvoice model.
"""

from __future__ import annotations

from apps.billing.accounts_receivable.services import create_customer_invoice

from .base_customer_invoice import CustomerInvoiceBaseSerializer
from .fields_customer_invoice import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class CustomerInvoiceCreateSerializer(CustomerInvoiceBaseSerializer):
    """
    Serializer used for creating customer_invoice records.
    """

    class Meta(CustomerInvoiceBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a customer_invoice.
        """

        return create_customer_invoice(
            validated_data=validated_data,
        )


__all__ = [
    "CustomerInvoiceCreateSerializer",
]
