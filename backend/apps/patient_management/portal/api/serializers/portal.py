"""
Serializers for the Patient Portal module.
"""

from __future__ import annotations

from apps.patient_management.portal.models import PatientPortalAccount
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "username",
    "email",
    "status",
    "auth_provider",
    "invitation_sent_at",
    "activated_at",
    "last_login_at",
    "email_verified",
    "two_factor_enabled",
    "preferred_language",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "id",
    "organization",
    "patient",
    "username",
    "email",
    "status",
    "auth_provider",
    "invitation_sent_at",
    "activated_at",
    "last_login_at",
    "email_verified",
    "two_factor_enabled",
    "preferred_language",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "id",
    "patient",
    "username",
    "status",
    "auth_provider",
    "email_verified",
    "is_active",
)

READ_ONLY_FIELDS: tuple[str, ...] = (
    "id",
    "created_at",
    "updated_at",
)


class PatientPortalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPortalAccount
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientPortalAccountCreateSerializer(
    PatientPortalAccountSerializer,
):
    class Meta(PatientPortalAccountSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientPortalAccountUpdateSerializer(
    PatientPortalAccountSerializer,
):
    class Meta(PatientPortalAccountSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PatientPortalAccountListSerializer(
    PatientPortalAccountSerializer,
):
    class Meta(PatientPortalAccountSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


PatientPortalAccountDetailSerializer = PatientPortalAccountSerializer


__all__ = [
    "PatientPortalAccountCreateSerializer",
    "PatientPortalAccountDetailSerializer",
    "PatientPortalAccountListSerializer",
    "PatientPortalAccountSerializer",
    "PatientPortalAccountUpdateSerializer",
]
