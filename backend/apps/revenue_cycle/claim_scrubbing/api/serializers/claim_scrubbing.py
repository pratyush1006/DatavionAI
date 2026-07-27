"""
Serializers for the ClaimScrubResult module.
"""

from __future__ import annotations

from apps.revenue_cycle.claim_scrubbing.models import ClaimScrubResult
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "claim",
    "result",
    "scrubbed_at",
    "scrubbed_by",
    "errors",
    "warnings",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "result",
    "scrubbed_at",
    "scrubbed_by",
    "errors",
    "warnings",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "result",
    "scrubbed_at",
    "scrubbed_by",
    "errors",
    "warnings",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class ClaimScrubResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimScrubResult
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimScrubResultCreateSerializer(ClaimScrubResultSerializer):
    class Meta(ClaimScrubResultSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimScrubResultUpdateSerializer(ClaimScrubResultSerializer):
    class Meta(ClaimScrubResultSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimScrubResultListSerializer(ClaimScrubResultSerializer):
    class Meta(ClaimScrubResultSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ClaimScrubResultDetailSerializer = ClaimScrubResultSerializer


__all__ = [
    "ClaimScrubResultCreateSerializer",
    "ClaimScrubResultDetailSerializer",
    "ClaimScrubResultListSerializer",
    "ClaimScrubResultSerializer",
    "ClaimScrubResultUpdateSerializer",
]
