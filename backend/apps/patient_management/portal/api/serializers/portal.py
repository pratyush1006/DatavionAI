"""
Patient Portal API serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.portal.constants import PortalAccountStatus
from apps.patient_management.portal.models import PatientPortalAccount


class PatientPortalAccountListSerializer(serializers.ModelSerializer):
    """Serialize portal accounts for collection responses."""

    class Meta:
        """Serializer metadata."""

        model = PatientPortalAccount
        fields = (
            "id",
            "patient",
            "username",
            "email",
            "status",
            "auth_provider",
            "email_verified",
            "two_factor_enabled",
            "preferred_language",
        )


class PatientPortalAccountDetailSerializer(
    PatientPortalAccountListSerializer,
):
    """Serialize a complete portal account representation."""

    class Meta(PatientPortalAccountListSerializer.Meta):
        """Serializer metadata."""

        fields = PatientPortalAccountListSerializer.Meta.fields + (
            "organization",
            "invitation_sent_at",
            "activated_at",
            "last_login_at",
            "created_at",
            "updated_at",
        )


class PatientPortalAccountCreateSerializer(serializers.Serializer):
    """Validate portal account creation input."""

    patient_id = serializers.UUIDField()
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    auth_provider = serializers.ChoiceField(
        choices=("LOCAL", "GOOGLE", "MICROSOFT", "SSO"),
        default="LOCAL",
    )
    preferred_language = serializers.CharField(
        max_length=50,
        default="English",
    )


class PatientPortalAccountUpdateSerializer(serializers.Serializer):
    """Validate mutable portal account metadata."""

    username = serializers.CharField(
        max_length=150,
        required=False,
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    auth_provider = serializers.ChoiceField(
        choices=("LOCAL", "GOOGLE", "MICROSOFT", "SSO"),
        required=False,
    )
    preferred_language = serializers.CharField(
        max_length=50,
        required=False,
    )
    email_verified = serializers.BooleanField(required=False)
    two_factor_enabled = serializers.BooleanField(required=False)


class PatientPortalLifecycleSerializer(serializers.Serializer):
    """Validate a strict lifecycle transition."""

    status = serializers.ChoiceField(
        choices=PortalAccountStatus.choices,
    )


__all__ = (
    "PatientPortalAccountCreateSerializer",
    "PatientPortalAccountDetailSerializer",
    "PatientPortalAccountListSerializer",
    "PatientPortalAccountUpdateSerializer",
    "PatientPortalLifecycleSerializer",
)
