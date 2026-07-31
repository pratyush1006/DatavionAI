"""
Employee lifecycle serializers.

Used for workflow based employee
lifecycle operations.

Responsibilities:

- Validate lifecycle payloads
- Prepare workflow input

Business rules belong to workflows.
"""

from __future__ import annotations

from rest_framework import serializers


class EmployeeStatusActionSerializer(
    serializers.Serializer,
):
    """
    Serializer for:

    - Activate employee
    - Deactivate employee

    These actions require only employee_id
    from URL.
    """


class EmployeeAssignmentActionSerializer(
    serializers.Serializer,
):
    """
    Serializer for employee assignment changes.
    """

    department_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    team_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    supervisor_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )


class EmployeeContractActionSerializer(
    serializers.Serializer,
):
    """
    Serializer for employee contract creation.
    """

    contract_data = serializers.DictField(
        required=True,
    )


class EmployeeOnboardingSerializer(
    serializers.Serializer,
):
    """
    Serializer for complete employee onboarding.
    """

    organization_id = serializers.UUIDField()

    employee_data = serializers.DictField()

    contract_data = serializers.DictField(
        required=False,
        allow_null=True,
    )

    assignment_data = serializers.DictField(
        required=False,
        allow_null=True,
    )


class EmployeeOffboardingSerializer(
    serializers.Serializer,
):
    """
    Serializer for employee offboarding.
    """

    termination_date = serializers.DateField(
        required=False,
        allow_null=True,
    )


__all__ = (
    "EmployeeStatusActionSerializer",
    "EmployeeAssignmentActionSerializer",
    "EmployeeContractActionSerializer",
    "EmployeeOnboardingSerializer",
    "EmployeeOffboardingSerializer",
)
