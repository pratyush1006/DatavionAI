"""
Employee API serializers.

Central export point for employee
API representations.
"""

from __future__ import annotations

from apps.organization.employees.api.serializers.base import (
    EmployeeBaseSerializer,
)
from apps.organization.employees.api.serializers.create import (
    EmployeeCreateSerializer,
)
from apps.organization.employees.api.serializers.detail import (
    EmployeeDetailSerializer,
)
from apps.organization.employees.api.serializers.lifecycle import (
    EmployeeAssignmentActionSerializer,
    EmployeeContractActionSerializer,
    EmployeeOffboardingSerializer,
    EmployeeOnboardingSerializer,
    EmployeeStatusActionSerializer,
)
from apps.organization.employees.api.serializers.list import (
    EmployeeListSerializer,
)
from apps.organization.employees.api.serializers.update import (
    EmployeeUpdateSerializer,
)

__all__ = (
    "EmployeeBaseSerializer",
    "EmployeeCreateSerializer",
    "EmployeeDetailSerializer",
    "EmployeeListSerializer",
    "EmployeeUpdateSerializer",
    "EmployeeStatusActionSerializer",
    "EmployeeAssignmentActionSerializer",
    "EmployeeContractActionSerializer",
    "EmployeeOnboardingSerializer",
    "EmployeeOffboardingSerializer",
)
