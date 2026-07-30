"""
Serializers for the ChargeCoding module.
"""

from __future__ import annotations

from apps.revenue_cycle.coding.models import ChargeCoding
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "code_system",
    "code",
    "description",
    "encoded_at",
    "coded_by",
    "is_primary",
    "modifier",
    "notes",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "code_system",
    "code",
    "description",
    "encoded_at",
    "coded_by",
    "is_primary",
    "modifier",
    "notes",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "code_system",
    "code",
    "description",
    "encoded_at",
    "coded_by",
    "is_primary",
    "modifier",
    "notes",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class ChargeCodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCoding
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ChargeCodingCreateSerializer(ChargeCodingSerializer):
    class Meta(ChargeCodingSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ChargeCodingUpdateSerializer(ChargeCodingSerializer):
    class Meta(ChargeCodingSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ChargeCodingListSerializer(ChargeCodingSerializer):
    class Meta(ChargeCodingSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ChargeCodingDetailSerializer = ChargeCodingSerializer


__all__ = [
    "ChargeCodingCreateSerializer",
    "ChargeCodingDetailSerializer",
    "ChargeCodingListSerializer",
    "ChargeCodingSerializer",
    "ChargeCodingUpdateSerializer",
]
