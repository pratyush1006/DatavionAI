"""
Serializers for the RemittanceAdvice module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.era.models import RemittanceAdvice

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "claim",
    "payment",
    "remittance_type",
    "payer_name",
    "payer_claim_control_number",
    "payment_amount",
    "patient_responsibility",
    "adjustment_amount",
    "remittance_date",
    "reference_number",
    "raw_content",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "payment",
    "remittance_type",
    "payer_name",
    "payer_claim_control_number",
    "payment_amount",
    "patient_responsibility",
    "adjustment_amount",
    "remittance_date",
    "reference_number",
    "raw_content",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "payment",
    "remittance_type",
    "payer_name",
    "payer_claim_control_number",
    "payment_amount",
    "patient_responsibility",
    "adjustment_amount",
    "remittance_date",
    "reference_number",
    "raw_content",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class RemittanceAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemittanceAdvice
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class RemittanceAdviceCreateSerializer(RemittanceAdviceSerializer):
    class Meta(RemittanceAdviceSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class RemittanceAdviceUpdateSerializer(RemittanceAdviceSerializer):
    class Meta(RemittanceAdviceSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class RemittanceAdviceListSerializer(RemittanceAdviceSerializer):
    class Meta(RemittanceAdviceSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


RemittanceAdviceDetailSerializer = RemittanceAdviceSerializer


__all__ = [
    "RemittanceAdviceCreateSerializer",
    "RemittanceAdviceDetailSerializer",
    "RemittanceAdviceListSerializer",
    "RemittanceAdviceSerializer",
    "RemittanceAdviceUpdateSerializer",
]
