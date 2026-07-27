"""
Serializers for the InsuranceVerification module.
"""

from __future__ import annotations

from apps.revenue_cycle.insurance_verification.models import InsuranceVerification
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "enrollment",
    "verification_date",
    "status",
    "verified_by",
    "member_id",
    "plan_name",
    "coverage_active",
    "deductible_remaining",
    "copay",
    "coinsurance_percent",
    "notes",
    "reference_number",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "enrollment",
    "verification_date",
    "status",
    "verified_by",
    "member_id",
    "plan_name",
    "coverage_active",
    "deductible_remaining",
    "copay",
    "coinsurance_percent",
    "notes",
    "reference_number",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "enrollment",
    "verification_date",
    "status",
    "verified_by",
    "member_id",
    "plan_name",
    "coverage_active",
    "deductible_remaining",
    "copay",
    "coinsurance_percent",
    "notes",
    "reference_number",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class InsuranceVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceVerification
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class InsuranceVerificationCreateSerializer(InsuranceVerificationSerializer):
    class Meta(InsuranceVerificationSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class InsuranceVerificationUpdateSerializer(InsuranceVerificationSerializer):
    class Meta(InsuranceVerificationSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class InsuranceVerificationListSerializer(InsuranceVerificationSerializer):
    class Meta(InsuranceVerificationSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


InsuranceVerificationDetailSerializer = InsuranceVerificationSerializer


__all__ = [
    "InsuranceVerificationCreateSerializer",
    "InsuranceVerificationDetailSerializer",
    "InsuranceVerificationListSerializer",
    "InsuranceVerificationSerializer",
    "InsuranceVerificationUpdateSerializer",
]
