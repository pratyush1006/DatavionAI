"""
Serializers for the BillingBatch module.
"""

from __future__ import annotations

from apps.revenue_cycle.billing.models import BillingBatch
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "batch_number",
    "status",
    "billing_period_start",
    "billing_period_end",
    "item_count",
    "total_amount",
    "closed_at",
    "created_by",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "batch_number",
    "status",
    "billing_period_start",
    "billing_period_end",
    "item_count",
    "total_amount",
    "closed_at",
    "created_by",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "batch_number",
    "status",
    "billing_period_start",
    "billing_period_end",
    "item_count",
    "total_amount",
    "closed_at",
    "created_by",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class BillingBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingBatch
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class BillingBatchCreateSerializer(BillingBatchSerializer):
    class Meta(BillingBatchSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class BillingBatchUpdateSerializer(BillingBatchSerializer):
    class Meta(BillingBatchSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class BillingBatchListSerializer(BillingBatchSerializer):
    class Meta(BillingBatchSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


BillingBatchDetailSerializer = BillingBatchSerializer


__all__ = [
    "BillingBatchCreateSerializer",
    "BillingBatchDetailSerializer",
    "BillingBatchListSerializer",
    "BillingBatchSerializer",
    "BillingBatchUpdateSerializer",
]
