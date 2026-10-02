"""
Serializer for updating patient family members.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.family_members.models import FamilyMember


class FamilyMemberUpdateSerializer(serializers.ModelSerializer):
    """Validate client input for family member updates."""

    class Meta:
        model = FamilyMember
        fields = (
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


__all__ = ("FamilyMemberUpdateSerializer",)
