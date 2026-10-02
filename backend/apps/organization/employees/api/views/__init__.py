"""
Employee API views.

Central export point for employee
API views.
"""

from __future__ import annotations

from apps.organization.employees.api.views.lifecycle import (
    EmployeeActivateAPIView,
    EmployeeAssignmentAPIView,
    EmployeeContractAPIView,
    EmployeeDeactivateAPIView,
    EmployeeOffboardingAPIView,
    EmployeeOnboardingAPIView,
)
from apps.organization.employees.api.views.list_create import (
    EmployeeListCreateAPIView,
)
from apps.organization.employees.api.views.retrieve_update_destroy import (
    EmployeeRetrieveUpdateDestroyAPIView,
)

__all__ = (
    # CRUD
    "EmployeeListCreateAPIView",
    "EmployeeRetrieveUpdateDestroyAPIView",
    # Lifecycle workflows
    "EmployeeActivateAPIView",
    "EmployeeDeactivateAPIView",
    "EmployeeAssignmentAPIView",
    "EmployeeContractAPIView",
    "EmployeeOnboardingAPIView",
    "EmployeeOffboardingAPIView",
)
