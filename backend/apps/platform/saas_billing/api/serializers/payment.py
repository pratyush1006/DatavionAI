"""
SaaS Billing Payment API serializers.

Handles:

- Payment representation
- Payment processing requests
- Payment reconciliation
- Refund requests
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.platform.saas_billing.models import (
    Payment,
)


class PaymentSerializer(
    serializers.ModelSerializer,
):
    """
    Payment read serializer.

    Used for:

    - Payment history
    - Billing dashboard
    - Transaction details
    """

    invoice_number = serializers.CharField(
        source="invoice.invoice_number",
        read_only=True,
    )

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Payment

        fields = [
            "id",
            "organization",
            "organization_name",
            "invoice",
            "invoice_number",
            "amount",
            "currency",
            "provider",
            "payment_method",
            "transaction_id",
            "gateway_order_id",
            "gateway_payment_id",
            "status",
            "gateway_response",
            "reconciliation_data",
            "refunded_amount",
            "paid_at",
            "failed_at",
            "refunded_at",
            "failure_reason",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "organization",
            "invoice",
            "amount",
            "currency",
            "status",
            "gateway_response",
            "reconciliation_data",
            "refunded_amount",
            "paid_at",
            "failed_at",
            "refunded_at",
            "created_at",
            "updated_at",
        ]


class PaymentCreateSerializer(
    serializers.Serializer,
):
    """
    Payment creation serializer.

    Used by:

    ProcessPaymentWorkflow
    """

    provider = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    payment_method = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    transaction_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    gateway_order_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    gateway_payment_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class PaymentReconcileSerializer(
    serializers.Serializer,
):
    """
    Gateway reconciliation serializer.

    Used by:

    ReconcilePaymentWorkflow
    """

    gateway_response = serializers.JSONField()

    success = serializers.BooleanField(
        default=True,
    )


class PaymentRefundSerializer(
    serializers.Serializer,
):
    """
    Payment refund serializer.

    Supports:

    - Full refund
    - Partial refund
    """

    refund_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    def validate_refund_amount(
        self,
        value: Decimal | None,
    ):
        """
        Validate refund amount.
        """

        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Refund amount must be greater than zero."
            )

        return value


__all__ = (
    "PaymentSerializer",
    "PaymentCreateSerializer",
    "PaymentReconcileSerializer",
    "PaymentRefundSerializer",
)
