"""
Serializers for the ClaimSubmission module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.claim_submission.models import ClaimSubmission

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "claim",
    "submission_method",
    "priority",
    "submitted_at",
    "submitted_by",
    "clearinghouse",
    "acknowledgement_code",
    "payer_control_number",
    "transmission_status",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "submission_method",
    "priority",
    "submitted_at",
    "submitted_by",
    "clearinghouse",
    "acknowledgement_code",
    "payer_control_number",
    "transmission_status",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "claim",
    "submission_method",
    "priority",
    "submitted_at",
    "submitted_by",
    "clearinghouse",
    "acknowledgement_code",
    "payer_control_number",
    "transmission_status",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class ClaimSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimSubmission
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimSubmissionCreateSerializer(ClaimSubmissionSerializer):
    class Meta(ClaimSubmissionSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimSubmissionUpdateSerializer(ClaimSubmissionSerializer):
    class Meta(ClaimSubmissionSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ClaimSubmissionListSerializer(ClaimSubmissionSerializer):
    class Meta(ClaimSubmissionSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ClaimSubmissionDetailSerializer = ClaimSubmissionSerializer


__all__ = [
    "ClaimSubmissionCreateSerializer",
    "ClaimSubmissionDetailSerializer",
    "ClaimSubmissionListSerializer",
    "ClaimSubmissionSerializer",
    "ClaimSubmissionUpdateSerializer",
]
