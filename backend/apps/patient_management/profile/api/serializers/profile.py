"""
Serializers for the Patient Profile module.

Write operations are validated here and executed by workflows.
The workflow remains responsible for authorization and orchestration.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.profile.models import (
    PatientProfile,
)

CREATE_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "preferred_language",
    "language_proficiency",
    "nationality",
    "religion",
    "ethnicity",
    "occupation",
    "employment_status",
    "education_level",
    "income_bracket",
    "interpreter_required",
)

UPDATE_FIELDS: tuple[str, ...] = (
    "preferred_language",
    "language_proficiency",
    "nationality",
    "religion",
    "ethnicity",
    "occupation",
    "employment_status",
    "education_level",
    "income_bracket",
    "interpreter_required",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "id",
    "organization",
    "patient",
    "preferred_language",
    "language_proficiency",
    "nationality",
    "religion",
    "ethnicity",
    "occupation",
    "employment_status",
    "education_level",
    "income_bracket",
    "interpreter_required",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "id",
    "patient",
    "preferred_language",
    "language_proficiency",
    "employment_status",
    "education_level",
    "interpreter_required",
    "is_active",
)

READ_ONLY_FIELDS: tuple[str, ...] = (
    "id",
    "created_at",
    "updated_at",
)


class ProfileSerializer(
    serializers.ModelSerializer,
):
    """
    Detailed patient profile serializer.
    """

    class Meta:
        model = PatientProfile
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ProfileCreateSerializer(
    ProfileSerializer,
):
    """
    Serializer for profile creation.
    """

    class Meta(ProfileSerializer.Meta):
        fields = CREATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ProfileUpdateSerializer(
    ProfileSerializer,
):
    """
    Serializer for profile updates.

    Organization and patient identity are immutable after creation.
    """

    class Meta(ProfileSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class ProfileListSerializer(
    ProfileSerializer,
):
    """
    Lightweight profile list serializer.
    """

    class Meta(ProfileSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


ProfileDetailSerializer = ProfileSerializer


__all__ = (
    "ProfileCreateSerializer",
    "ProfileDetailSerializer",
    "ProfileListSerializer",
    "ProfileSerializer",
    "ProfileUpdateSerializer",
)
