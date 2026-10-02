"""
Employee lifecycle serializers.

Used for workflow-based employee lifecycle operations.

Responsibilities
----------------
- Validate lifecycle payloads
- Normalize lifecycle input
- Prepare workflow input
- Reject structurally invalid nested lifecycle payloads

Business rules that require domain state remain in workflows/services.
"""

from __future__ import annotations

from datetime import date

from apps.organization.employees.constants import (
    ContractStatus,
    ContractType,
)
from rest_framework import serializers

# =============================================================================
# Status Actions
# =============================================================================


class EmployeeStatusActionSerializer(
    serializers.Serializer,
):
    """
    Serializer for employee status actions.

    Used by:

    - Activate employee
    - Deactivate employee

    The employee identifier comes from the URL, so no request body
    fields are required.
    """


# =============================================================================
# Assignment
# =============================================================================


class EmployeeAssignmentActionSerializer(
    serializers.Serializer,
):
    """
    Serializer for employee assignment changes.

    Assignment remains a separate lifecycle concern from the employee
    aggregate itself.
    """

    department_id = serializers.UUIDField(
        required=True,
        allow_null=False,
    )

    team_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    supervisor_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    effective_from = serializers.DateField(
        required=False,
        allow_null=True,
    )


# =============================================================================
# Contract
# =============================================================================


class EmployeeContractActionSerializer(
    serializers.Serializer,
):
    """
    Serializer for employee contract creation.

    Contract data is validated here before it reaches the contract
    workflow/service layer.

    Required contract fields:

    - contract_number
    - contract_type
    - start_date

    Optional fields:

    - status
    - end_date
    - probation_end_date
    - remarks

    The service/workflow remains responsible for lifecycle/domain
    decisions such as replacing the current contract.
    """

    contract_number = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )

    contract_type = serializers.ChoiceField(
        choices=ContractType.choices,
        required=True,
    )

    status = serializers.ChoiceField(
        choices=ContractStatus.choices,
        required=False,
        default=ContractStatus.ACTIVE,
    )

    start_date = serializers.DateField(
        required=True,
        allow_null=False,
    )

    end_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    probation_end_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
    )

    def to_internal_value(
        self,
        data,
    ):
        # Accept both direct contract fields and contract_data envelopes.
        if isinstance(data, dict):
            nested = data.get("contract_data")
            if isinstance(nested, dict):
                data = nested
        return super().to_internal_value(data)

    def validate_contract_number(
        self,
        value: str,
    ) -> str:
        """
        Normalize contract number.
        """

        normalized = value.strip().upper()

        if not normalized:
            raise serializers.ValidationError(
                "Contract number is required.",
            )

        return normalized

    def validate(
        self,
        attrs: dict,
    ) -> dict:
        """
        Validate contract date relationships.

        Database constraints provide the final integrity guarantee,
        while API validation provides a useful client-facing error
        before workflow execution.
        """

        start_date: date = attrs["start_date"]

        end_date: date | None = attrs.get(
            "end_date",
        )

        probation_end_date: date | None = attrs.get(
            "probation_end_date",
        )

        if end_date is not None and end_date < start_date:
            raise serializers.ValidationError(
                {
                    "end_date": ("Contract end date cannot be before the start date."),
                },
            )

        if probation_end_date is not None and probation_end_date < start_date:
            raise serializers.ValidationError(
                {
                    "probation_end_date": (
                        "Probation end date cannot be before the start date."
                    ),
                },
            )

        return attrs


# =============================================================================
# Onboarding
# =============================================================================


class EmployeeOnboardingSerializer(
    serializers.Serializer,
):
    """
    Serializer for complete employee onboarding.

    Onboarding may optionally create:

    - Employee
    - Contract
    - Assignment

    The nested dictionaries are validated structurally here.
    Domain orchestration remains owned by EmployeeOnboardingWorkflow.
    """

    organization_id = serializers.UUIDField(
        required=True,
    )

    employee_data = serializers.DictField(
        required=True,
        allow_empty=False,
    )

    contract_data = EmployeeContractActionSerializer(
        required=False,
        allow_null=True,
    )

    assignment_data = EmployeeAssignmentActionSerializer(
        required=False,
        allow_null=True,
    )

    def validate_employee_data(
        self,
        value: dict,
    ) -> dict:
        """
        Validate that employee_data is present and non-empty.

        The complete employee creation contract remains owned by
        EmployeeCreateSerializer/EmployeeCreationWorkflow.
        """

        if not value:
            raise serializers.ValidationError(
                "Employee data is required.",
            )

        return value


# =============================================================================
# Offboarding
# =============================================================================


class EmployeeOffboardingSerializer(
    serializers.Serializer,
):
    """
    Serializer for employee offboarding.

    If termination_date is omitted, the workflow may resolve the
    effective termination date according to its domain rules.
    """

    termination_date = serializers.DateField(
        required=False,
        allow_null=True,
    )


# =============================================================================
# Public API
# =============================================================================


__all__ = (
    "EmployeeStatusActionSerializer",
    "EmployeeAssignmentActionSerializer",
    "EmployeeContractActionSerializer",
    "EmployeeOnboardingSerializer",
    "EmployeeOffboardingSerializer",
)
