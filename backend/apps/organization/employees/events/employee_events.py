"""
Employee domain events.

Central export point for employee
domain events.
"""

from __future__ import annotations

from apps.organization.employees.events.employee_assignment_changed import (
    EmployeeAssignmentChangedEvent,
)

#
# Contract lifecycle events
#
from apps.organization.employees.events.employee_contract_created import (
    EmployeeContractCreatedEvent,
)
from apps.organization.employees.events.employee_contract_updated import (
    EmployeeContractUpdatedEvent,
)
from apps.organization.employees.events.employee_created import (
    EmployeeCreatedEvent,
)
from apps.organization.employees.events.employee_deleted import (
    EmployeeDeletedEvent,
)
from apps.organization.employees.events.employee_offboarded import (
    EmployeeOffboardedEvent,
)

#
# Workforce lifecycle events
#
from apps.organization.employees.events.employee_onboarded import (
    EmployeeOnboardedEvent,
)
from apps.organization.employees.events.employee_status_changed import (
    EmployeeStatusChangedEvent,
)
from apps.organization.employees.events.employee_updated import (
    EmployeeUpdatedEvent,
)

__all__ = (
    # Core employee lifecycle
    "EmployeeCreatedEvent",
    "EmployeeUpdatedEvent",
    "EmployeeDeletedEvent",
    "EmployeeStatusChangedEvent",
    # Organization assignment
    "EmployeeAssignmentChangedEvent",
    # Contract lifecycle
    "EmployeeContractCreatedEvent",
    "EmployeeContractUpdatedEvent",
    # HR lifecycle
    "EmployeeOnboardedEvent",
    "EmployeeOffboardedEvent",
)
