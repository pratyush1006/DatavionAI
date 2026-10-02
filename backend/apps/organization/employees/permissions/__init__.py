"""
Employee RBAC permissions.
"""

from .employee import (
    CanActivateEmployee,
    CanAssignEmployee,
    CanCreateEmployee,
    CanDeactivateEmployee,
    CanDeleteEmployee,
    CanManageEmployeeContracts,
    CanOffboardEmployee,
    CanOnboardEmployee,
    CanUpdateEmployee,
    CanViewEmployee,
)

__all__ = (
    "CanViewEmployee",
    "CanCreateEmployee",
    "CanUpdateEmployee",
    "CanDeleteEmployee",
    "CanActivateEmployee",
    "CanDeactivateEmployee",
    "CanAssignEmployee",
    "CanManageEmployeeContracts",
    "CanOnboardEmployee",
    "CanOffboardEmployee",
)
