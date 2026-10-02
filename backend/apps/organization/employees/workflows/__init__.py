"""
Employee workflows.

Central export point for employee
domain workflows.
"""

from __future__ import annotations

from apps.organization.employees.workflows.employee_activation import (
    EmployeeActivationData,
    EmployeeActivationRequest,
    EmployeeActivationWorkflow,
)
from apps.organization.employees.workflows.employee_assignment import (
    EmployeeAssignmentData,
    EmployeeAssignmentRequest,
    EmployeeAssignmentWorkflow,
)
from apps.organization.employees.workflows.employee_contract_management import (
    EmployeeContractManagementData,
    EmployeeContractManagementRequest,
    EmployeeContractManagementWorkflow,
)
from apps.organization.employees.workflows.employee_creation import (
    EmployeeCreationData,
    EmployeeCreationRequest,
    EmployeeCreationWorkflow,
)
from apps.organization.employees.workflows.employee_deactivation import (
    EmployeeDeactivationData,
    EmployeeDeactivationRequest,
    EmployeeDeactivationWorkflow,
)
from apps.organization.employees.workflows.employee_deletion import (
    EmployeeDeletionData,
    EmployeeDeletionRequest,
    EmployeeDeletionWorkflow,
)
from apps.organization.employees.workflows.employee_offboarding import (
    EmployeeOffboardingData,
    EmployeeOffboardingRequest,
    EmployeeOffboardingWorkflow,
)
from apps.organization.employees.workflows.employee_onboarding import (
    EmployeeOnboardingData,
    EmployeeOnboardingRequest,
    EmployeeOnboardingWorkflow,
)
from apps.organization.employees.workflows.employee_update import (
    EmployeeUpdateData,
    EmployeeUpdateRequest,
    EmployeeUpdateWorkflow,
)

__all__ = (
    # Creation
    "EmployeeCreationRequest",
    "EmployeeCreationData",
    "EmployeeCreationWorkflow",
    # Update
    "EmployeeUpdateRequest",
    "EmployeeUpdateData",
    "EmployeeUpdateWorkflow",
    # Lifecycle
    "EmployeeActivationRequest",
    "EmployeeActivationData",
    "EmployeeActivationWorkflow",
    "EmployeeDeactivationRequest",
    "EmployeeDeactivationData",
    "EmployeeDeactivationWorkflow",
    # Assignment
    "EmployeeAssignmentRequest",
    "EmployeeAssignmentData",
    "EmployeeAssignmentWorkflow",
    # Contract
    "EmployeeContractManagementRequest",
    "EmployeeContractManagementData",
    "EmployeeContractManagementWorkflow",
    # Delete
    "EmployeeDeletionRequest",
    "EmployeeDeletionData",
    "EmployeeDeletionWorkflow",
    # Onboarding
    "EmployeeOnboardingRequest",
    "EmployeeOnboardingData",
    "EmployeeOnboardingWorkflow",
    # Offboarding
    "EmployeeOffboardingRequest",
    "EmployeeOffboardingData",
    "EmployeeOffboardingWorkflow",
)
