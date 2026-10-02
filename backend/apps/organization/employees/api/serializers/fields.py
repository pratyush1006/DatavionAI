"""
Employee API reusable serializer fields.

Contains optimized nested representations
used across employee serializers.
"""

from __future__ import annotations

from rest_framework import serializers


class EmployeeUserField(
    serializers.Field,
):
    """
    Serialize linked user information.
    """

    def to_representation(
        self,
        value,
    ):
        if value is None:
            return None

        return {
            "id": value.id,
            "email": value.email,
            "name": value.get_full_name(),
        }


class EmployeeOrganizationField(
    serializers.Field,
):
    """
    Serialize organization summary.

    Expected object:
        apps.platform.organizations.models.Organization
    """

    def to_representation(
        self,
        value,
    ):
        if value is None:
            return None

        return {
            "id": value.id,
            "name": (
                getattr(
                    value,
                    "display_name",
                    None,
                )
                or getattr(
                    value,
                    "name",
                    str(value),
                )
            ),
            "code": getattr(
                value,
                "code",
                None,
            ),
        }


class EmployeeManagerField(
    serializers.Field,
):
    """
    Serialize reporting manager summary.
    """

    def to_representation(
        self,
        value,
    ):
        if value is None:
            return None

        return {
            "id": value.id,
            "employee_code": (value.employee_code),
            "name": (value.full_name),
        }


class EmployeeDisplayField(
    serializers.Field,
):
    """
    Employee display information.

    Used for nested employee references.
    """

    def to_representation(
        self,
        value,
    ):
        if value is None:
            return None

        return {
            "id": value.id,
            "employee_code": (value.employee_code),
            "name": (value.full_name),
            "designation": (value.designation),
        }


__all__ = (
    "EmployeeUserField",
    "EmployeeOrganizationField",
    "EmployeeManagerField",
    "EmployeeDisplayField",
)
