"""
Billing Core Payment API serializers.
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.billing.constants import PaymentMethod
from apps.billing.models import Payment


class PaymentCreateSerializer(serializers.Serializer):
    """Validate payment creation input."""

    invoice = serializers.UUIDField()
    patient = serializers.UUIDField()
    payment_method = serializers.ChoiceField(choices=PaymentMethod.choices)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )
    payment_date = serializers.DateField()
    reference_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_reference_number(self, value: str) -> str:
        """Normalize payment reference."""
        return value.strip().upper()


class PaymentListSerializer(serializers.ModelSerializer):
    """Serialize payment collections."""

    class Meta:
        """Serializer metadata."""

        model = Payment
        fields = (
            "id",
            "organization",
            "invoice",
            "patient",
            "payment_method",
            "amount",
            "payment_date",
            "reference_number",
            "notes",
            "received_by",
            "is_active",
            "created_at",
            "updated_at",
        )


class PaymentSerializer(PaymentListSerializer):
    """Serialize one payment."""


__all__ = ("PaymentCreateSerializer", "PaymentListSerializer", "PaymentSerializer")
