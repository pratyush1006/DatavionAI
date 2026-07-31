"""
Employee list serializer.

Optimized representation for:

- Employee listing
- Search results
- Organization dashboards

Avoids expensive nested serialization.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organization.employees.models import (
    Employee,
)


class EmployeeListSerializer(
    serializers.ModelSerializer,
):
    """
    Lightweight employee representation.

    Used by:

        EmployeeListCreateAPIView
    """

    full_name = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Employee

        fields = (
            "id",
            #
            # Identity
            #
            "employee_code",
            "full_name",
            "designation",
            #
            # Employment
            #
            "employment_type",
            "status",
            "joining_date",
            #
            # Contact
            #
            "work_email",
            #
            # Audit
            #
            "created_at",
        )

        read_only_fields = (
            "id",
            "full_name",
            "created_at",
        )
