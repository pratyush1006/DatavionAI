"""Insurance Verification API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.insurance_verification.constants import (
    VerificationMethod,
    VerificationOutcome,
    VerificationStatus,
)
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification


class InsuranceVerificationWriteSerializer(serializers.Serializer):
    """Validate create and update payloads."""

    patient_id = serializers.UUIDField(required=False)
    payer_id = serializers.CharField(max_length=100, required=False)
    payer_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    member_id = serializers.CharField(max_length=100, required=False)
    policy_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    group_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    subscriber_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    subscriber_relationship = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    verification_method = serializers.ChoiceField(
        choices=[item.value for item in VerificationMethod],
        required=False,
    )
    eligibility_reference = serializers.UUIDField(required=False, allow_null=True)
    coverage_start = serializers.DateField(required=False, allow_null=True)
    coverage_end = serializers.DateField(required=False, allow_null=True)
    copay_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    deductible_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    coinsurance_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    prior_authorization_required = serializers.BooleanField(required=False)
    response_code = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    request_reference = serializers.CharField(max_length=100, required=False)
    idempotency_key = serializers.CharField(max_length=255, required=False)
    failure_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        """Validate cross-field coverage and monetary constraints."""

        coverage_start = attrs.get("coverage_start")
        coverage_end = attrs.get("coverage_end")
        if coverage_start and coverage_end and coverage_end < coverage_start:
            raise serializers.ValidationError(
                {"coverage_end": "coverage_end cannot be earlier than coverage_start."}
            )

        coinsurance = attrs.get("coinsurance_percent")
        if coinsurance is not None and not 0 <= coinsurance <= 100:
            raise serializers.ValidationError(
                {"coinsurance_percent": "Must be between 0 and 100."}
            )

        for field in ("copay_amount", "deductible_amount"):
            amount = attrs.get(field)
            if amount is not None and amount < 0:
                raise serializers.ValidationError({field: "Amount cannot be negative."})
        return attrs


class InsuranceVerificationLifecycleSerializer(serializers.Serializer):
    """Validate lifecycle transition payloads."""

    target_status = serializers.ChoiceField(
        choices=[item.value for item in VerificationStatus]
    )
    outcome = serializers.ChoiceField(
        choices=[item.value for item in VerificationOutcome],
        required=False,
    )
    response_code = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    request_reference = serializers.CharField(max_length=100, required=False)
    idempotency_key = serializers.CharField(max_length=255, required=False)
    failure_reason = serializers.CharField(required=False, allow_blank=True)


class InsuranceVerificationDetailSerializer(serializers.ModelSerializer):
    """Serialize Insurance Verification records for API responses."""

    class Meta:
        """Serializer metadata."""

        model = InsuranceVerification
        fields = (
            "id",
            "organization",
            "patient",
            "eligibility_reference",
            "payer_id",
            "payer_name",
            "member_id",
            "policy_number",
            "group_number",
            "subscriber_name",
            "subscriber_relationship",
            "verification_method",
            "status",
            "outcome",
            "requested_at",
            "verified_at",
            "coverage_start",
            "coverage_end",
            "copay_amount",
            "deductible_amount",
            "coinsurance_percent",
            "prior_authorization_required",
            "response_code",
            "response_message",
            "response_payload",
            "request_reference",
            "idempotency_key",
            "failure_reason",
            "verified_by",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = (
    "InsuranceVerificationDetailSerializer",
    "InsuranceVerificationLifecycleSerializer",
    "InsuranceVerificationWriteSerializer",
)
