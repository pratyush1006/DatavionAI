"""
Serializers for the ClaimDenial module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.denials.models import ClaimDenial

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "claim",
    "denial_reason",
    "payer_reason_code",
    "denial_date",
    "description",
    "is_appealable",
    "resolved",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "denial_reason",
    "payer_reason_code",
    "denial_date",
    "description",
    "is_appealable",
    "resolved",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "denial_reason",
    "payer_reason_code",
    "denial_date",
    "description",
    "is_appealable",
    "resolved",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class ClaimDenialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimDenial
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimDenialCreateSerializer(ClaimDenialSerializer):
    class Meta(ClaimDenialSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimDenialUpdateSerializer(ClaimDenialSerializer):
    class Meta(ClaimDenialSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimDenialListSerializer(ClaimDenialSerializer):
    class Meta(ClaimDenialSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ClaimDenialDetailSerializer = ClaimDenialSerializer


__all__ = [
    "ClaimDenialCreateSerializer",
    "ClaimDenialDetailSerializer",
    "ClaimDenialListSerializer",
    "ClaimDenialSerializer",
    "ClaimDenialUpdateSerializer",
]
