"""
Base serializer for the Departments application.
"""

from __future__ import annotations

from apps.organization.departments.models import Department
from rest_framework import serializers


class DepartmentBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer shared by all Department serializers.
    """

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Department
        fields = "__all__"


__all__ = [
    "DepartmentBaseSerializer",
]
