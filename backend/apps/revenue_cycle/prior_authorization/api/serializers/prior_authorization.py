"""
Serializers for the PriorAuthorizationRequest module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.prior_authorization.models import PriorAuthorizationRequest

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "authorization",
    "requested_by",
    "submitted_to_payer_at",
    "decision_received_at",
    "payer_reference",
    "clinical_notes",
    "follow_up_date",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "authorization",
    "requested_by",
    "submitted_to_payer_at",
    "decision_received_at",
    "payer_reference",
    "clinical_notes",
    "follow_up_date",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "authorization",
    "requested_by",
    "submitted_to_payer_at",
    "decision_received_at",
    "payer_reference",
    "clinical_notes",
    "follow_up_date",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class PriorAuthorizationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorAuthorizationRequest
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PriorAuthorizationRequestCreateSerializer(PriorAuthorizationRequestSerializer):
    class Meta(PriorAuthorizationRequestSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PriorAuthorizationRequestUpdateSerializer(PriorAuthorizationRequestSerializer):
    class Meta(PriorAuthorizationRequestSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PriorAuthorizationRequestListSerializer(PriorAuthorizationRequestSerializer):
    class Meta(PriorAuthorizationRequestSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


PriorAuthorizationRequestDetailSerializer = PriorAuthorizationRequestSerializer


__all__ = [
    "PriorAuthorizationRequestCreateSerializer",
    "PriorAuthorizationRequestDetailSerializer",
    "PriorAuthorizationRequestListSerializer",
    "PriorAuthorizationRequestSerializer",
    "PriorAuthorizationRequestUpdateSerializer",
]
