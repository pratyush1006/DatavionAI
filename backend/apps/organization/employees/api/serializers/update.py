"""
Employee update serializer.

Responsible for:

- Validating employee profile updates
- Preparing workflow payload

Business operations are handled by:

    EmployeeUpdateWorkflow
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organization.employees.models import (
    Employee,
)


class EmployeeUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Employee update serializer.

    Workflow:

        Serializer
             |
             v
        EmployeeUpdateRequest
             |
             v
        EmployeeUpdateWorkflow
    """

    class Meta:
        model = Employee

        fields = (
            "designation",
            "work_email",
            "phone_number",
            "employment_type",
            "confirmation_date",
            "metadata",
        )

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

    def validate_metadata(
        self,
        value,
    ):
        """
        Ensure metadata remains JSON compatible.
        """

        if value is None:
            return {}

        return value
