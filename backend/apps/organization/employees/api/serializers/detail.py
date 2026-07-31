"""
Employee detail serializer.

Provides complete employee aggregate representation.

Used for:

- Employee retrieve API
- Nested employee references
- Future HR modules

Read operations only.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organization.employees.api.serializers.fields import (
    EmployeeManagerField,
    EmployeeOrganizationField,
    EmployeeUserField,
)
from apps.organization.employees.models import (
    Employee,
)


class EmployeeDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Detailed employee representation.
    """

    user = EmployeeUserField()

    organization = EmployeeOrganizationField()

    manager = EmployeeManagerField()

    full_name = serializers.CharField(
        read_only=True,
    )

    is_active_employee = serializers.BooleanField(
        read_only=True,
    )

    is_terminated = serializers.BooleanField(
        read_only=True,
    )

    class Meta:
        model = Employee

        fields = (
            "id",
            #
            # Organization
            #
            "organization",
            #
            # Identity
            #
            "user",
            "employee_code",
            "full_name",
            "designation",
            #
            # Contact
            #
            "work_email",
            "phone_number",
            #
            # Employment
            #
            "employment_type",
            "status",
            "joining_date",
            "confirmation_date",
            "termination_date",
            #
            # Hierarchy
            #
            "manager",
            #
            # Extension
            #
            "metadata",
            #
            # Computed
            #
            "is_active_employee",
            "is_terminated",
            #
            # Audit
            #
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "status",
            "termination_date",
            "full_name",
            "is_active_employee",
            "is_terminated",
            "created_at",
            "updated_at",
        )
