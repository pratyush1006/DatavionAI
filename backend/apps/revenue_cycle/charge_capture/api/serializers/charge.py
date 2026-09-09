"""Charge Capture API serializers."""

from __future__ import annotations

from rest_framework import serializers

from ...constants import ChargeStatus
from ...models import Charge

__all__ = (
    "ChargeSerializer",
    "ChargeCreateSerializer",
    "ChargeTransitionSerializer",
    "ChargeVoidSerializer",
)


class ChargeSerializer(serializers.ModelSerializer):
    """Serialize a Charge domain object."""

    class Meta:
        """Configure the serializer."""

        model = Charge
        fields = (
            "id",
            "patient",
            "organization",
            "service_code",
            "description",
            "quantity",
            "unit_price",
            "total_amount",
            "status",
            "idempotency_key",
            "captured_at",
            "voided_at",
            "void_reason",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "total_amount",
            "status",
            "captured_at",
            "voided_at",
            "void_reason",
            "created_at",
            "updated_at",
        )


class ChargeCreateSerializer(serializers.Serializer):
    """Validate charge creation input."""

    patient_id = serializers.UUIDField()
    service_code = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=500)
    quantity = serializers.DecimalField(max_digits=12, decimal_places=3)
    unit_price = serializers.DecimalField(max_digits=14, decimal_places=2)
    idempotency_key = serializers.CharField(
        max_length=128, required=False, allow_blank=False
    )


class ChargeTransitionSerializer(serializers.Serializer):
    """Validate lifecycle transition input."""

    target_status = serializers.ChoiceField(
        choices=(
            ChargeStatus.READY.value,
            ChargeStatus.SUBMITTED.value,
        )
    )


class ChargeVoidSerializer(serializers.Serializer):
    """Validate charge void input."""

    reason = serializers.CharField(max_length=500)
