"""Prior Authorization API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationMethod,
    AuthorizationOutcome,
    AuthorizationStatus,
)
from apps.revenue_cycle.prior_authorization.models import PriorAuthorization


class PriorAuthorizationWriteSerializer(serializers.Serializer):
    """Validate create and update authorization payloads."""

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
    procedure_code = serializers.CharField(max_length=50, required=False)
    service_description = serializers.CharField(
        max_length=500, required=False, allow_blank=True
    )
    place_of_service = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )
    rendering_provider_npi = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )
    clinical_indication = serializers.CharField(required=False, allow_blank=True)
    authorization_method = serializers.ChoiceField(
        choices=[item.value for item in AuthorizationMethod],
        required=False,
    )
    eligibility_reference = serializers.UUIDField(required=False, allow_null=True)
    requested_service_date = serializers.DateField(required=False, allow_null=True)
    requested_units = serializers.IntegerField(
        required=False, allow_null=True, min_value=1
    )
    requested_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=False,
        allow_null=True,
        min_value=0,
    )
    authorization_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    effective_date = serializers.DateField(required=False, allow_null=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)
    response_code = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    request_reference = serializers.CharField(max_length=100, required=False)
    idempotency_key = serializers.CharField(max_length=255, required=False)
    decision_reason = serializers.CharField(required=False, allow_blank=True)
    failure_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        """Validate authorization request dates."""

        effective_date = attrs.get("effective_date")
        expiration_date = attrs.get("expiration_date")
        if effective_date and expiration_date and expiration_date < effective_date:
            raise serializers.ValidationError(
                {
                    "expiration_date": "expiration_date cannot be earlier than effective_date."
                }
            )
        return attrs


class PriorAuthorizationLifecycleSerializer(serializers.Serializer):
    """Validate lifecycle transition payloads."""

    target_status = serializers.ChoiceField(
        choices=[item.value for item in AuthorizationStatus]
    )
    outcome = serializers.ChoiceField(
        choices=[item.value for item in AuthorizationOutcome],
        required=False,
    )
    response_code = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)
    authorization_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    decision_reason = serializers.CharField(required=False, allow_blank=True)
    effective_date = serializers.DateField(required=False, allow_null=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)
    approved_units = serializers.IntegerField(
        required=False, allow_null=True, min_value=1
    )
    failure_reason = serializers.CharField(required=False, allow_blank=True)


class PriorAuthorizationDetailSerializer(serializers.ModelSerializer):
    """Serialize Prior Authorization records for API responses."""

    class Meta:
        """Serializer metadata."""

        model = PriorAuthorization
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
            "procedure_code",
            "service_description",
            "place_of_service",
            "rendering_provider_npi",
            "clinical_indication",
            "authorization_method",
            "status",
            "outcome",
            "requested_service_date",
            "requested_units",
            "approved_units",
            "requested_amount",
            "authorization_number",
            "effective_date",
            "expiration_date",
            "requested_at",
            "submitted_at",
            "decided_at",
            "response_code",
            "response_message",
            "response_payload",
            "request_reference",
            "idempotency_key",
            "decision_reason",
            "failure_reason",
            "approved_by",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = (
    "PriorAuthorizationDetailSerializer",
    "PriorAuthorizationLifecycleSerializer",
    "PriorAuthorizationWriteSerializer",
)
