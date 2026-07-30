"""
Serializers for the EligibilityCheck module.
"""

from __future__ import annotations

from apps.revenue_cycle.eligibility.models import EligibilityCheck
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "enrollment",
    "check_date",
    "service_code",
    "status",
    "checked_by",
    "benefit_details",
    "notes",
    "reference_number",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "enrollment",
    "check_date",
    "service_code",
    "status",
    "checked_by",
    "benefit_details",
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
    "check_date",
    "service_code",
    "status",
    "checked_by",
    "benefit_details",
    "notes",
    "reference_number",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class EligibilityCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityCheck
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class EligibilityCheckCreateSerializer(EligibilityCheckSerializer):
    class Meta(EligibilityCheckSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class EligibilityCheckUpdateSerializer(EligibilityCheckSerializer):
    class Meta(EligibilityCheckSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class EligibilityCheckListSerializer(EligibilityCheckSerializer):
    class Meta(EligibilityCheckSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


EligibilityCheckDetailSerializer = EligibilityCheckSerializer


__all__ = [
    "EligibilityCheckCreateSerializer",
    "EligibilityCheckDetailSerializer",
    "EligibilityCheckListSerializer",
    "EligibilityCheckSerializer",
    "EligibilityCheckUpdateSerializer",
]
