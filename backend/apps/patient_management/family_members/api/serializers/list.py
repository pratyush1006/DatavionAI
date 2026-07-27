"""
List serializer for the Family Members module.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.family_members.models import (
    FamilyMember,
)

__all__ = [
    "FamilyMemberListSerializer",
]


class FamilyMemberListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing family members.
    """

    full_name = serializers.ReadOnlyField()

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    relationship_display = serializers.CharField(
        source="get_relationship_display",
        read_only=True,
    )

    gender_display = serializers.CharField(
        source="get_gender_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = FamilyMember

        fields = (
            "id",
            "family_member_number",
            "full_name",
            "patient",
            "patient_name",
            "relationship",
            "relationship_display",
            "gender",
            "gender_display",
            "mobile_number",
            "email",
            "is_living",
            "is_next_of_kin",
            "is_emergency_contact",
            "status",
            "status_display",
            "created_at",
        )

        read_only_fields = fields
