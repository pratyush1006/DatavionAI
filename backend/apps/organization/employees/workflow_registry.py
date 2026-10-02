"""
Employee workflow registration.

Registers employee workflows into the DatavionOS
core workflow registry.
"""

from __future__ import annotations

from apps.core.workflows import (
    workflow_registry,
)
from apps.organization.employees.workflows import (
    EmployeeActivationWorkflow,
    EmployeeAssignmentWorkflow,
    EmployeeContractManagementWorkflow,
    EmployeeCreationWorkflow,
    EmployeeDeactivationWorkflow,
    EmployeeDeletionWorkflow,
    EmployeeOffboardingWorkflow,
    EmployeeOnboardingWorkflow,
    EmployeeUpdateWorkflow,
)


def register_employee_workflows() -> None:
    """
    Register employee workflows.

    Workflow naming convention:

    <domain>.<capability>

    Examples:

        employee.create
        employee.assign
        employee.onboard
    """

    workflows = {
        #
        # Employee lifecycle
        #
        "employee.create": (EmployeeCreationWorkflow),
        "employee.update": (EmployeeUpdateWorkflow),
        "employee.activate": (EmployeeActivationWorkflow),
        "employee.deactivate": (EmployeeDeactivationWorkflow),
        #
        # Organization structure
        #
        "employee.assign": (EmployeeAssignmentWorkflow),
        #
        # Employment contract lifecycle
        #
        "employee.contract.manage": (EmployeeContractManagementWorkflow),
        #
        # HR lifecycle
        #
        "employee.onboard": (EmployeeOnboardingWorkflow),
        "employee.offboard": (EmployeeOffboardingWorkflow),
        #
        # Removal lifecycle
        #
        "employee.delete": (EmployeeDeletionWorkflow),
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__: tuple[str, ...] = ("register_employee_workflows",)
