"""
Employee creation serializer.

Responsible for:

- Validating employee creation payload
- Preparing workflow input
- Delegating business logic to EmployeeCreationWorkflow

Business rules do not belong here.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organization.employees.models import (
    Employee,
)


class EmployeeCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Employee creation serializer.

    Used by:

        EmployeeListCreateAPIView
                |
                v
        EmployeeCreationWorkflow
    """

    class Meta:
        model = Employee

        fields = (
            "organization",
            "user",
            "employee_code",
            "designation",
            "work_email",
            "phone_number",
            "employment_type",
            "joining_date",
        )

    def validate_employee_code(
        self,
        value,
    ):
        """
        Normalize employee code.
        """

        return value.strip().upper()

    def validate_work_email(
        self,
        value,
    ):
        """
        Normalize work email.
        """

        if value:
            return value.lower()

        return value
