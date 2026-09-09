"""
Employee contract domain services.

Responsibilities
----------------
- Create employee contracts
- Update employee contracts
- Maintain current contract lifecycle
- Maintain contract date invariants

Non-responsibilities
--------------------
- RBAC
- Workflow orchestration
- Events
- Notifications

The service is intentionally independent from API and workflow layers.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, timedelta

from apps.organization.employees.models import (
    Employee,
    EmployeeContract,
)
from django.db import transaction
from django.utils.dateparse import parse_date

type ContractData = Mapping[str, object]


# ============================================================
# Date normalization
# ============================================================


def _coerce_date(
    value: object,
    *,
    field_name: str,
) -> date | None:
    """
    Convert an incoming date value into a Python date.

    Supported inputs:

    - datetime.date
    - ISO date string (YYYY-MM-DD)
    - None

    The API currently accepts contract_data as a generic
    dictionary, so date values may legitimately arrive as
    strings.
    """

    if value is None:
        return None

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        parsed = parse_date(
            value.strip(),
        )

        if parsed is not None:
            return parsed

    raise ValueError(
        f"{field_name} must be a valid date.",
    )


def _get_contract_start_date(
    *,
    validated_data: ContractData,
) -> date:
    """
    Resolve the required contract start date.
    """

    value = validated_data.get(
        "start_date",
    )

    start_date = _coerce_date(
        value,
        field_name="Contract start date",
    )

    if start_date is None:
        raise ValueError(
            "Contract start date is required.",
        )

    return start_date


# ============================================================
# Date validation
# ============================================================


def _validate_contract_dates(
    *,
    start_date: date,
    end_date: date | None,
    probation_end_date: date | None,
) -> None:
    """
    Validate contract date relationships.
    """

    if end_date is not None and end_date < start_date:
        raise ValueError(
            "Contract end date cannot be before the start date.",
        )

    if probation_end_date is not None and probation_end_date < start_date:
        raise ValueError(
            "Probation end date cannot be before the start date.",
        )


# ============================================================
# Current contract management
# ============================================================


def _close_current_contract(
    *,
    employee: Employee,
    new_start_date: date,
) -> EmployeeContract | None:
    """
    Close the employee's current contract.

    The previous contract becomes historical:

        is_current = False
        end_date = new_start_date - 1 day

    The replacement contract therefore starts immediately
    after the historical contract ends.

    A replacement contract cannot start on or before the
    current contract's start date.
    """

    current_contract = (
        EmployeeContract.objects.select_for_update()
        .filter(
            employee=employee,
            is_current=True,
        )
        .first()
    )

    if current_contract is None:
        return None

    if new_start_date <= current_contract.start_date:
        raise ValueError(
            "New contract start date must be after the current contract start date.",
        )

    historical_end_date = new_start_date - timedelta(days=1)

    if historical_end_date < current_contract.start_date:
        raise ValueError(
            "New contract start date would create an invalid contract history.",
        )

    current_contract.end_date = historical_end_date

    current_contract.is_current = False

    current_contract.save(
        update_fields=(
            "end_date",
            "is_current",
            "updated_at",
        ),
    )

    return current_contract


# ============================================================
# Create contract
# ============================================================


@transaction.atomic
def create_employee_contract(
    *,
    employee: Employee,
    validated_data: ContractData,
) -> EmployeeContract:
    """
    Create an employee contract.

    Lifecycle
    ---------
    1. Normalize incoming dates.
    2. Validate date relationships.
    3. Lock the existing current contract.
    4. Close the current contract.
    5. Create the new current contract.
    6. Return the persisted contract.

    Transactionality guarantees that a failure during the
    replacement operation does not leave the employee with
    partially-updated contract history.
    """

    data = dict(
        validated_data,
    )

    start_date = _get_contract_start_date(
        validated_data=data,
    )

    end_date = _coerce_date(
        data.get("end_date"),
        field_name="Contract end date",
    )

    probation_end_date = _coerce_date(
        data.get("probation_end_date"),
        field_name="Probation end date",
    )

    _validate_contract_dates(
        start_date=start_date,
        end_date=end_date,
        probation_end_date=probation_end_date,
    )

    # A newly-created contract is always the current contract.
    #
    # EmployeeContract enforces:
    #
    #     is_current=True -> end_date=NULL
    #
    data["start_date"] = start_date
    data["end_date"] = None
    data["is_current"] = True

    if probation_end_date is not None:
        data["probation_end_date"] = probation_end_date
    elif "probation_end_date" in data:
        data["probation_end_date"] = None

    _close_current_contract(
        employee=employee,
        new_start_date=start_date,
    )

    return EmployeeContract.objects.create(
        employee=employee,
        **data,
    )


# ============================================================
# Update contract
# ============================================================


@transaction.atomic
def update_employee_contract(
    *,
    instance: EmployeeContract,
    validated_data: ContractData,
) -> EmployeeContract:
    """
    Update an employee contract.

    Date values are normalized before persistence.

    Contract invariants are enforced consistently with the
    EmployeeContract database constraints.
    """

    if not validated_data:
        return instance

    data = dict(
        validated_data,
    )

    start_date = _coerce_date(
        data.get(
            "start_date",
            instance.start_date,
        ),
        field_name="Contract start date",
    )

    if start_date is None:
        raise ValueError(
            "Contract start date is required.",
        )

    end_date = _coerce_date(
        data.get(
            "end_date",
            instance.end_date,
        ),
        field_name="Contract end date",
    )

    probation_end_date = _coerce_date(
        data.get(
            "probation_end_date",
            instance.probation_end_date,
        ),
        field_name="Probation end date",
    )

    _validate_contract_dates(
        start_date=start_date,
        end_date=end_date,
        probation_end_date=probation_end_date,
    )

    is_current = bool(
        data.get(
            "is_current",
            instance.is_current,
        ),
    )

    if is_current and end_date is not None:
        raise ValueError(
            "A current employee contract cannot have an end date.",
        )

    if not is_current and end_date is None:
        raise ValueError(
            "A historical employee contract must have an end date.",
        )

    # --------------------------------------------------------
    # Re-activating a historical contract
    # --------------------------------------------------------

    if is_current and not instance.is_current:
        current_contract = (
            EmployeeContract.objects.select_for_update()
            .filter(
                employee=instance.employee,
                is_current=True,
            )
            .exclude(
                pk=instance.pk,
            )
            .first()
        )

        if current_contract is not None:
            raise ValueError(
                "The employee already has a current contract.",
            )

    data["start_date"] = start_date
    data["end_date"] = end_date
    data["probation_end_date"] = probation_end_date
    data["is_current"] = is_current

    for field, value in data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save()

    instance.refresh_from_db()

    return instance


__all__ = (
    "ContractData",
    "create_employee_contract",
    "update_employee_contract",
)
