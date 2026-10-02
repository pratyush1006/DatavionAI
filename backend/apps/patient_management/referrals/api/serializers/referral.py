"""
Serializers for Patient Referrals.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.referrals.models import PatientReferral


class PatientReferralListSerializer(serializers.ModelSerializer):
    """Serialize referrals for collection responses."""

    class Meta:
        """Serializer metadata."""

        model = PatientReferral
        fields = (
            "id",
            "patient",
            "referral_number",
            "referred_to",
            "priority",
            "urgency",
            "status",
            "requested_date",
            "appointment_date",
            "created_at",
        )
        read_only_fields = fields


class PatientReferralDetailSerializer(serializers.ModelSerializer):
    """Serialize complete referral details."""

    class Meta:
        """Serializer metadata."""

        model = PatientReferral
        fields = (
            "id",
            "organization",
            "patient",
            "referral_number",
            "referring_provider",
            "referred_to",
            "referred_to_organization",
            "reason",
            "priority",
            "urgency",
            "status",
            "clinical_notes",
            "requested_date",
            "appointment_date",
            "completed_date",
            "accepted_at",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "status",
            "accepted_at",
            "completed_at",
            "created_at",
            "updated_at",
        )


class PatientReferralCreateSerializer(serializers.Serializer):
    """Validate referral creation input."""

    patient_id = serializers.UUIDField()
    organization_id = serializers.UUIDField()
    referral_number = serializers.CharField(max_length=40)
    referred_to = serializers.CharField(max_length=150)
    reason = serializers.CharField()
    priority = serializers.ChoiceField(
        choices=PatientReferral._meta.get_field("priority").choices,
    )
    urgency = serializers.ChoiceField(
        choices=PatientReferral._meta.get_field("urgency").choices,
    )
    referring_provider = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )
    referred_to_organization = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    clinical_notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    requested_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    def validate_referral_number(self, value: str) -> str:
        """Reject blank or whitespace-only referral numbers."""

        value = value.strip()
        if not value:
            raise serializers.ValidationError("Referral number is required.")
        return value

    def validate_referred_to(self, value: str) -> str:
        """Reject blank or whitespace-only referral destinations."""

        value = value.strip()
        if not value:
            raise serializers.ValidationError("Referral destination is required.")
        return value

    def validate_reason(self, value: str) -> str:
        """Reject blank or whitespace-only referral reasons."""

        value = value.strip()
        if not value:
            raise serializers.ValidationError("Referral reason is required.")
        return value


class PatientReferralUpdateSerializer(serializers.Serializer):
    """Validate mutable referral updates."""

    referring_provider = serializers.CharField(
        max_length=150,
        required=False,
    )
    referred_to = serializers.CharField(
        max_length=150,
        required=False,
    )
    referred_to_organization = serializers.CharField(
        max_length=255,
        required=False,
    )
    reason = serializers.CharField(
        required=False,
    )
    priority = serializers.ChoiceField(
        choices=PatientReferral._meta.get_field("priority").choices,
        required=False,
    )
    urgency = serializers.ChoiceField(
        choices=PatientReferral._meta.get_field("urgency").choices,
        required=False,
    )
    clinical_notes = serializers.CharField(
        required=False,
    )
    requested_date = serializers.DateField(
        required=False,
        allow_null=True,
    )
    appointment_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    def validate_referred_to(self, value: str) -> str:
        """Reject blank or whitespace-only referral destinations."""

        value = value.strip()
        if not value:
            raise serializers.ValidationError("Referral destination is required.")
        return value

    def validate_reason(self, value: str) -> str:
        """Reject blank or whitespace-only referral reasons."""

        value = value.strip()
        if not value:
            raise serializers.ValidationError("Referral reason is required.")
        return value


class PatientReferralTransitionSerializer(serializers.Serializer):
    """Validate a lifecycle transition request."""

    target_status = serializers.ChoiceField(
        choices=PatientReferral._meta.get_field("status").choices,
    )


__all__ = (
    "PatientReferralCreateSerializer",
    "PatientReferralDetailSerializer",
    "PatientReferralListSerializer",
    "PatientReferralTransitionSerializer",
    "PatientReferralUpdateSerializer",
)
