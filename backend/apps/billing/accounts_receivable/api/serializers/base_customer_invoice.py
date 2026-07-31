"""
Base serializer for the CustomerInvoice model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.billing.accounts_receivable.models import CustomerInvoice


class CustomerInvoiceBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared logic for customer_invoice serializers.
    """

    class Meta:
        model = CustomerInvoice
        fields: tuple[str, ...] = ()


__all__ = [
    "CustomerInvoiceBaseSerializer",
]
