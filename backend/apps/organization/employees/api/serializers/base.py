"""
Employee API base serializers.

Provides common serializer behavior
for employee representations.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organization.employees.models import (
    Employee,
)


class EmployeeBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Base employee serializer.

    Shared fields:

    - organization
    - identity
    - employment information
    - metadata
    """

    class Meta:
        model = Employee

        fields = (
            "id",
            "organization",
            "user",
            "employee_code",
            "designation",
            "work_email",
            "phone_number",
            "employment_type",
            "status",
            "joining_date",
            "confirmation_date",
            "termination_date",
            "manager",
            "metadata",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "status",
            "termination_date",
            "created_at",
            "updated_at",
        )
