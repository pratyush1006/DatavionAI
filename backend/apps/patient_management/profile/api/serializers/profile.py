"""
Serializers for the Patient Profile module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.profile.models import PatientProfile

WRITE_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "preferred_language",
    "language_proficiency",
    "nationality",
    "religion",
    "occupation",
    "employment_status",
    "education_level",
    "income_bracket",
    "ethnicity",
    "preferred_pharmacy",
    "biography",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "id",
    "organization",
    "patient",
    "preferred_language",
    "language_proficiency",
    "nationality",
    "religion",
    "occupation",
    "employment_status",
    "education_level",
    "income_bracket",
    "ethnicity",
    "preferred_pharmacy",
    "biography",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "id",
    "patient",
    "preferred_language",
    "employment_status",
    "education_level",
    "is_active",
)

READ_ONLY_FIELDS: tuple[str, ...] = (
    "id",
    "created_at",
    "updated_at",
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ProfileCreateSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ProfileUpdateSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ProfileListSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ProfileDetailSerializer = ProfileSerializer


__all__ = [
    "ProfileCreateSerializer",
    "ProfileDetailSerializer",
    "ProfileListSerializer",
    "ProfileSerializer",
    "ProfileUpdateSerializer",
]
