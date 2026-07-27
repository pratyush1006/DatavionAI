"""
Base serializer for the Departments application.
"""

from __future__ import annotations

from apps.organization.departments.models import Department
from rest_framework import serializers


class DepartmentBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer shared by all Department serializers.
    """

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        """
        Serializer configuration.
        """

        model = Department

        fields = (
            "id",
            "organization",
            "organization_name",
            "name",
            "code",
            "description",
            "department_type",
            "head",
            "phone",
            "email",
            "location",
            "status",
            "is_clinical",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "organization_name",
            "created_at",
            "updated_at",
        )


__all__ = [
    "DepartmentBaseSerializer",
]
