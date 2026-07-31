"""
Serializers for the ChargeCapture module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.charge_capture.models import ChargeCapture

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "encounter_reference",
    "service_date",
    "description",
    "procedure_code",
    "quantity",
    "unit_price",
    "total_charge",
    "captured_by",
    "is_coded",
    "notes",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "encounter_reference",
    "service_date",
    "description",
    "procedure_code",
    "quantity",
    "unit_price",
    "total_charge",
    "captured_by",
    "is_coded",
    "notes",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "encounter_reference",
    "service_date",
    "description",
    "procedure_code",
    "quantity",
    "unit_price",
    "total_charge",
    "captured_by",
    "is_coded",
    "notes",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class ChargeCaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCapture
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ChargeCaptureCreateSerializer(ChargeCaptureSerializer):
    class Meta(ChargeCaptureSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ChargeCaptureUpdateSerializer(ChargeCaptureSerializer):
    class Meta(ChargeCaptureSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ChargeCaptureListSerializer(ChargeCaptureSerializer):
    class Meta(ChargeCaptureSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ChargeCaptureDetailSerializer = ChargeCaptureSerializer


__all__ = [
    "ChargeCaptureCreateSerializer",
    "ChargeCaptureDetailSerializer",
    "ChargeCaptureListSerializer",
    "ChargeCaptureSerializer",
    "ChargeCaptureUpdateSerializer",
]
