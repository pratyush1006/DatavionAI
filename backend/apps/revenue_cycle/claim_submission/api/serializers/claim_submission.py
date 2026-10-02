"""Serializers for claim submission APIs."""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.claim_submission.constants import (
    SubmissionMethod,
    SubmissionStatus,
)
from apps.revenue_cycle.claim_submission.models import ClaimSubmission


class ClaimSubmissionSerializer(serializers.ModelSerializer):
    """Serialize a claim submission."""

    class Meta:
        """Define serializer metadata."""

        model = ClaimSubmission
        fields = (
            "id",
            "patient",
            "claim_reference",
            "payer_id",
            "payer_name",
            "submission_method",
            "status",
            "payload",
            "response_data",
            "external_submission_id",
            "rejection_code",
            "rejection_reason",
            "submitted_at",
            "accepted_at",
            "failed_at",
            "cancelled_at",
            "idempotency_key",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "response_data",
            "external_submission_id",
            "rejection_code",
            "rejection_reason",
            "submitted_at",
            "accepted_at",
            "failed_at",
            "cancelled_at",
            "created_at",
            "updated_at",
        )


class CreateClaimSubmissionSerializer(serializers.Serializer):
    """Validate claim submission creation commands."""

    patient_id = serializers.UUIDField()
    claim_reference = serializers.CharField(max_length=100)
    payer_id = serializers.CharField(max_length=100)
    payer_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    submission_method = serializers.ChoiceField(
        choices=SubmissionMethod.choices, default=SubmissionMethod.EDI
    )
    idempotency_key = serializers.CharField(max_length=150)
    payload = serializers.JSONField(required=False)


class UpdateClaimSubmissionSerializer(serializers.Serializer):
    """Validate mutable claim submission fields."""

    payer_name = serializers.CharField(max_length=200, required=False)
    response_data = serializers.JSONField(required=False)


class TransitionClaimSubmissionSerializer(serializers.Serializer):
    """Validate lifecycle transition commands."""

    target_status = serializers.ChoiceField(choices=SubmissionStatus.choices)
    response_data = serializers.JSONField(required=False)
    external_submission_id = serializers.CharField(
        max_length=150, required=False, allow_blank=True
    )
    rejection_code = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    rejection_reason = serializers.CharField(required=False, allow_blank=True)


__all__ = (
    "ClaimSubmissionSerializer",
    "CreateClaimSubmissionSerializer",
    "UpdateClaimSubmissionSerializer",
    "TransitionClaimSubmissionSerializer",
)
