"""
Employee events package.
"""

from apps.organization.employees.events.employee_contract_status_changed import (
    EmployeeContractStatusChangedEvent,
)

from .employee_events import (
    EmployeeAssignmentChangedEvent,
    EmployeeContractCreatedEvent,
    EmployeeContractUpdatedEvent,
    EmployeeCreatedEvent,
    EmployeeDeletedEvent,
    EmployeeOffboardedEvent,
    EmployeeOnboardedEvent,
    EmployeeStatusChangedEvent,
    EmployeeUpdatedEvent,
)

__all__ = (
    "EmployeeCreatedEvent",
    "EmployeeUpdatedEvent",
    "EmployeeDeletedEvent",
    "EmployeeStatusChangedEvent",
    "EmployeeAssignmentChangedEvent",
    "EmployeeContractCreatedEvent",
    "EmployeeContractUpdatedEvent",
    "EmployeeOnboardedEvent",
    "EmployeeOffboardedEvent",
    # Contract lifecycle
    "EmployeeContractCreatedEvent",
    "EmployeeContractUpdatedEvent",
    "EmployeeContractStatusChangedEvent",
)
