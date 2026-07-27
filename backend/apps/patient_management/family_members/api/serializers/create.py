"""
Create serializer for the Family Members module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.services import (
    create_family_member,
)

__all__ = [
    "FamilyMemberCreateSerializer",
]


class FamilyMemberCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for creating a family member.
    """

    class Meta:
        model = FamilyMember

        fields = (
            "id",
            "organization",
            "patient",
            "family_member_number",
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
            "status",
        )

        read_only_fields = ("id",)

    def create(
        self,
        validated_data,
    ) -> FamilyMember:
        """
        Create a family member.
        """
        return create_family_member(
            **validated_data,
        )
