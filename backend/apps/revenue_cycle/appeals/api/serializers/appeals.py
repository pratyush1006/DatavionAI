"""
Serializers for the ClaimAppeal module.
"""

from __future__ import annotations

from apps.revenue_cycle.appeals.models import ClaimAppeal
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "claim",
    "denial",
    "status",
    "appeal_reason",
    "submitted_at",
    "decided_at",
    "decision_notes",
    "filed_by",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "denial",
    "status",
    "appeal_reason",
    "submitted_at",
    "decided_at",
    "decision_notes",
    "filed_by",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "denial",
    "status",
    "appeal_reason",
    "submitted_at",
    "decided_at",
    "decision_notes",
    "filed_by",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class ClaimAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimAppeal
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimAppealCreateSerializer(ClaimAppealSerializer):
    class Meta(ClaimAppealSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimAppealUpdateSerializer(ClaimAppealSerializer):
    class Meta(ClaimAppealSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimAppealListSerializer(ClaimAppealSerializer):
    class Meta(ClaimAppealSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ClaimAppealDetailSerializer = ClaimAppealSerializer


__all__ = [
    "ClaimAppealCreateSerializer",
    "ClaimAppealDetailSerializer",
    "ClaimAppealListSerializer",
    "ClaimAppealSerializer",
    "ClaimAppealUpdateSerializer",
]
