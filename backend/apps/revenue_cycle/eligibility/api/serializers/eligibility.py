"""DRF serializers for Eligibility."""

from __future__ import annotations

from rest_framework import serializers

from apps.revenue_cycle.eligibility.models import Eligibility


class EligibilityCreateSerializer(serializers.Serializer):
    """Validate Eligibility creation input."""

    patient_id = serializers.UUIDField()
    payer_id = serializers.CharField(max_length=100)
    payer_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    member_id = serializers.CharField(max_length=100)
    group_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    subscriber_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    subscriber_relationship = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    request_reference = serializers.CharField(max_length=100)
    idempotency_key = serializers.CharField(max_length=255)
    response_payload = serializers.JSONField(required=False)

    def validate(self, attrs):
        """Reject blank required identifiers."""
        for field in ("payer_id", "member_id", "request_reference", "idempotency_key"):
            attrs[field] = attrs[field].strip()
            if not attrs[field]:
                raise serializers.ValidationError(
                    {field: "This field cannot be blank."}
                )
        return attrs


class EligibilityUpdateSerializer(serializers.Serializer):
    """Validate mutable Eligibility metadata."""

    payer_id = serializers.CharField(max_length=100, required=False)
    payer_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    member_id = serializers.CharField(max_length=100, required=False)
    group_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    subscriber_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    subscriber_relationship = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    response_code = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    response_message = serializers.CharField(required=False, allow_blank=True)
    response_payload = serializers.JSONField(required=False)


class EligibilityLifecycleSerializer(serializers.Serializer):
    """Validate a lifecycle transition."""

    status = serializers.CharField(max_length=30)


class EligibilityListSerializer(serializers.ModelSerializer):
    """Serialize Eligibility list data."""

    class Meta:
        """Serializer metadata."""

        model = Eligibility
        fields = (
            "id",
            "patient",
            "payer_id",
            "payer_name",
            "member_id",
            "status",
            "coverage_status",
            "requested_at",
            "verified_at",
            "request_reference",
        )


class EligibilityDetailSerializer(serializers.ModelSerializer):
    """Serialize complete Eligibility data."""

    class Meta:
        """Serializer metadata."""

        model = Eligibility
        fields = "__all__"


__all__ = (
    "EligibilityCreateSerializer",
    "EligibilityDetailSerializer",
    "EligibilityLifecycleSerializer",
    "EligibilityListSerializer",
    "EligibilityUpdateSerializer",
)
