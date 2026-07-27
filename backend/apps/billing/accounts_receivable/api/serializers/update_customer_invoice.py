"""
Update serializer for the CustomerInvoice model.
"""

from __future__ import annotations

from apps.billing.accounts_receivable.models import CustomerInvoice
from apps.billing.accounts_receivable.services import update_customer_invoice

from .base_customer_invoice import CustomerInvoiceBaseSerializer
from .fields_customer_invoice import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class CustomerInvoiceUpdateSerializer(CustomerInvoiceBaseSerializer):
    """
    Serializer used for updating customer_invoice records.
    """

    class Meta(CustomerInvoiceBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: CustomerInvoice,
        validated_data: dict[str, object],
    ) -> CustomerInvoice:
        """
        Update a customer_invoice.
        """

        return update_customer_invoice(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "CustomerInvoiceUpdateSerializer",
]
