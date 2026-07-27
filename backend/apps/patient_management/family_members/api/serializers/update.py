"""
Update serializer for the Family Members module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.family_members.models import (
    FamilyMember,
)
from apps.patient_management.family_members.services import (
    update_family_member,
)

__all__ = [
    "FamilyMemberUpdateSerializer",
]


class FamilyMemberUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for updating a family member.
    """

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
            "status",
        )

    def update(
        self,
        instance: FamilyMember,
        validated_data: dict,
    ) -> FamilyMember:
        """
        Update a family member.
        """
        return update_family_member(
            family_member=instance,
            **validated_data,
        )
