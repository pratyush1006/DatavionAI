"""
Payment serializers for the Billing application.
"""

from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.billing.models import Payment
from apps.billing.services import create_payment
from apps.common.api.serializers import BaseModelSerializer


class PaymentBaseSerializer(BaseModelSerializer):
    """
    Base serializer containing shared normalization logic for payment serializers.
    """

    class Meta:
        model = Payment
        fields: tuple[str, ...] = ()

    def validate_amount(
        self,
        value: Decimal,
    ) -> Decimal:
        """
        Validate that amount is positive.
        """

        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "Payment amount must be greater than zero."
            )

        return value

    def validate_reference_number(
        self,
        value: str,
    ) -> str:
        """
        Normalize the reference number.
        """

        return self._normalize_text(
            value,
        ).upper()


class PaymentListSerializer(PaymentBaseSerializer):
    """
    Serializer used for listing payments.
    """

    class Meta(PaymentBaseSerializer.Meta):
        fields = (
            "id",
            "invoice",
            "patient",
            "payment_method",
            "amount",
            "payment_date",
            "reference_number",
            "is_active",
            "created_at",
        )
        read_only_fields = (
            "id",
            "is_active",
            "created_at",
            "updated_at",
        )


class PaymentSerializer(PaymentBaseSerializer):
    """
    Serializer used for payment details.
    """

    class Meta(PaymentBaseSerializer.Meta):
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
        read_only_fields = (
            "id",
            "organization",
            "received_by",
            "is_active",
            "created_at",
            "updated_at",
        )


class PaymentCreateSerializer(PaymentBaseSerializer):
    """
    Serializer used for creating payments.
    """

    class Meta(PaymentBaseSerializer.Meta):
        fields = (
            "invoice",
            "patient",
            "payment_method",
            "amount",
            "payment_date",
            "reference_number",
            "notes",
        )
        read_only_fields = (
            "id",
            "organization",
            "received_by",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a payment.
        """

        return create_payment(
            validated_data=validated_data,
        )


__all__ = [
    "PaymentBaseSerializer",
    "PaymentCreateSerializer",
    "PaymentListSerializer",
    "PaymentSerializer",
]
