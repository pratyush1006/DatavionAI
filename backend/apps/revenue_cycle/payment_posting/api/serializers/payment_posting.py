"""Serializers for payment posting APIs."""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from ...models import PaymentPosting


class PaymentPostingSerializer(serializers.ModelSerializer):
    """Serialize payment posting resources."""

    class Meta:
        """Configure the resource serializer."""

        model = PaymentPosting
        fields = (
            "id",
            "patient",
            "invoice",
            "payer_name",
            "payer_claim_reference",
            "source",
            "status",
            "amount",
            "adjustment_amount",
            "posted_at",
            "reversed_at",
            "external_reference",
            "idempotency_key",
            "notes",
            "posted_by",
            "reversal_reason",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "posted_at",
            "reversed_at",
            "posted_by",
            "created_at",
            "updated_at",
        )


class PaymentPostingCreateSerializer(serializers.Serializer):
    """Validate payment posting creation input."""

    patient = serializers.UUIDField()
    invoice = serializers.UUIDField(required=False, allow_null=True)
    payer_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    payer_claim_reference = serializers.CharField(
        required=False, allow_blank=True, max_length=100
    )
    source = serializers.ChoiceField(
        choices=[
            choice.value
            for choice in __import__(
                "apps.revenue_cycle.payment_posting.constants",
                fromlist=["PaymentPostingSource"],
            ).PaymentPostingSource
        ]
    )
    amount = serializers.DecimalField(
        max_digits=14, decimal_places=2, min_value=Decimal("0.01")
    )
    adjustment_amount = serializers.DecimalField(
        max_digits=14, decimal_places=2, min_value=Decimal("0.00"), required=False
    )
    external_reference = serializers.CharField(
        required=False, allow_blank=True, max_length=150
    )
    idempotency_key = serializers.CharField(max_length=150)
    notes = serializers.CharField(required=False, allow_blank=True)


class PaymentPostingUpdateSerializer(serializers.Serializer):
    """Validate mutable payment posting input."""

    payer_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    payer_claim_reference = serializers.CharField(
        required=False, allow_blank=True, max_length=100
    )
    source = serializers.CharField(required=False, max_length=20)
    amount = serializers.DecimalField(
        max_digits=14, decimal_places=2, min_value=Decimal("0.01"), required=False
    )
    adjustment_amount = serializers.DecimalField(
        max_digits=14, decimal_places=2, min_value=Decimal("0.00"), required=False
    )
    external_reference = serializers.CharField(
        required=False, allow_blank=True, max_length=150
    )
    notes = serializers.CharField(required=False, allow_blank=True)


__all__ = (
    "PaymentPostingCreateSerializer",
    "PaymentPostingSerializer",
    "PaymentPostingUpdateSerializer",
)
