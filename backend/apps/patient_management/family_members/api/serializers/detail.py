"""
Serializer for retrieving patient family members.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.family_members.models import FamilyMember


class FamilyMemberDetailSerializer(serializers.ModelSerializer):
    """Read-only Family Member detail representation."""

    full_name = serializers.ReadOnlyField()
    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )
    patient_number = serializers.CharField(
        source="patient.patient_number",
        read_only=True,
    )
    organization_name = serializers.CharField(
        source="organization.name",
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
            "organization",
            "organization_name",
            "patient",
            "patient_number",
            "patient_name",
            "family_member_number",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "relationship",
            "relationship_display",
            "gender",
            "gender_display",
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
            "is_next_of_kin",
            "is_emergency_contact",
            "notes",
            "status",
            "status_display",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        )
        read_only_fields = fields


__all__ = ("FamilyMemberDetailSerializer",)
