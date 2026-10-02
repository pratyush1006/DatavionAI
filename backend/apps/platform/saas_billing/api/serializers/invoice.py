"""
SaaS Billing Invoice API serializers.

Handles:

- Invoice representation
- Invoice lifecycle actions
- Invoice payment operations
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.saas_billing.models import (
    Invoice,
)


class InvoiceSerializer(
    serializers.ModelSerializer,
):
    """
    Invoice read serializer.

    Used for:

    - Billing dashboard
    - Invoice listing
    - Invoice details
    """

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    subscription_id = serializers.UUIDField(
        source="subscription.id",
        read_only=True,
    )

    class Meta:
        model = Invoice

        fields = [
            "id",
            "organization",
            "organization_name",
            "subscription",
            "subscription_id",
            "invoice_number",
            "invoice_type",
            "status",
            "billing_period_start",
            "billing_period_end",
            "subtotal",
            "tax_amount",
            "discount_amount",
            "total_amount",
            "paid_amount",
            "currency",
            "issued_at",
            "paid_at",
            "payment_reference",
            "invoice_data",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "organization",
            "subscription",
            "invoice_number",
            "status",
            "issued_at",
            "paid_at",
            "paid_amount",
            "payment_reference",
            "invoice_data",
            "created_at",
            "updated_at",
        ]


class InvoiceLifecycleSerializer(
    serializers.Serializer,
):
    """
    Invoice lifecycle action serializer.

    Supports:

    - Issue
    - Finalize
    - Cancel
    - Refund
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class InvoicePaymentSerializer(
    serializers.Serializer,
):
    """
    Invoice payment request serializer.

    Used by payment workflow.
    """

    provider = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    transaction_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    payment_method = serializers.CharField(
        required=False,
        allow_blank=True,
    )


__all__ = (
    "InvoiceSerializer",
    "InvoiceLifecycleSerializer",
    "InvoicePaymentSerializer",
)
