"""
Employee contract domain services.

Responsibilities:

- Create employee contracts
- Update employee contracts
- Maintain current contract lifecycle

Non-responsibilities:

- RBAC
- Workflow orchestration
- Events
- Notifications
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.organization.employees.models import (
    Employee,
    EmployeeContract,
)

type ContractData = Mapping[str, object]


@transaction.atomic
def create_employee_contract(
    *,
    employee: Employee,
    validated_data: ContractData,
) -> EmployeeContract:
    """
    Create employee contract.

    Previous current contract is closed
    before creating a new current contract.
    """

    EmployeeContract.objects.filter(
        employee=employee,
        is_current=True,
    ).update(
        is_current=False,
    )

    return EmployeeContract.objects.create(
        employee=employee,
        **validated_data,
    )


@transaction.atomic
def update_employee_contract(
    *,
    instance: EmployeeContract,
    validated_data: ContractData,
) -> EmployeeContract:
    """
    Update employee contract.
    """

    if not validated_data:
        return instance

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=tuple(
            validated_data.keys(),
        ),
    )

    instance.refresh_from_db()

    return instance


__all__ = (
    "create_employee_contract",
    "update_employee_contract",
)
