"""
Serializers for the RcmMetric module.
"""

from __future__ import annotations

from apps.revenue_cycle.analytics.models import RcmMetric
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "category",
    "name",
    "value",
    "unit",
    "period_start",
    "period_end",
    "computed_at",
    "dimensions",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "category",
    "name",
    "value",
    "unit",
    "period_start",
    "period_end",
    "computed_at",
    "dimensions",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "category",
    "name",
    "value",
    "unit",
    "period_start",
    "period_end",
    "computed_at",
    "dimensions",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class RcmMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = RcmMetric
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class RcmMetricCreateSerializer(RcmMetricSerializer):
    class Meta(RcmMetricSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class RcmMetricUpdateSerializer(RcmMetricSerializer):
    class Meta(RcmMetricSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class RcmMetricListSerializer(RcmMetricSerializer):
    class Meta(RcmMetricSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


RcmMetricDetailSerializer = RcmMetricSerializer


__all__ = [
    "RcmMetricCreateSerializer",
    "RcmMetricDetailSerializer",
    "RcmMetricListSerializer",
    "RcmMetricSerializer",
    "RcmMetricUpdateSerializer",
]
