"""
Serializer for creating patient family members.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.family_members.models import FamilyMember


class FamilyMemberCreateSerializer(serializers.ModelSerializer):
    """Validate client input for family member creation."""

    patient_id = serializers.UUIDField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = FamilyMember
        fields = (
            "patient_id",
            "first_name",
            "middle_name",
            "last_name",
            "relationship",
            "gender",
            "date_of_birth",
            "mobile_number",
            "email",
            "blood_group",
            "occupation",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "is_living",
            "is_emergency_contact",
            "is_next_of_kin",
            "notes",
        )

    def validate_email(self, value: str) -> str:
        return value.strip().lower()


__all__ = ("FamilyMemberCreateSerializer",)
